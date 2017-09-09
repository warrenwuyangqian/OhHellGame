import random
def bid(hand, player_no, phase_no, deck_top, reshuffled=False,
        player_data=None, suppress_player_data=True):
    '''
    bid function takes 7 arguments:
    hand which is a tuple of cards that you have been dealt for the current
    phase, in the case of phase 1 and 19, it represents the cards of other
    players.
    player_no indicates your player order in the current phase.
    phase_no an integer indicates the phase number of the current hand.
    deck_top which is used to determine the trumps for the current phase.
    reshuffled indicates whether the deck was reshuffled, defaulted to False.
    plyaer_data, indicate the cards in the deck in current phase.
    suppress_player_data indicates whether the function should return only
    the bid or with player_data, defaulted to True.
    bid funtion then reutns an integer between 0 and 10 inclusive indicating
    the number of tricks you predict you will win in current phase.
    '''

    # card_value library takes values of the cards as key and rank of each
    # as value
    card_value = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,
                  '9': 8, '0': 9, 'J': 10, 'Q': 11, 'K': 12, 'A': 13}
    # second element of deck_top represents the trump suit
    trump_suit = deck_top[1]
    # initialise the bid to zero
    bid = 0
    # create a full deck
    suits = ['C', 'D', 'H', 'S']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '0', 'J', 'Q', 'K', 'A']
    DECK = []
    for suit in suits:
        for value in values:
            card = value + suit
            DECK.append(card)

    # if reshuffled is Ture, the deck should be a full deck
    if reshuffled:
        player_data = DECK.copy()

    # play_data is the deck passed on by preceding function call
    if player_data is not None:
        deck = player_data.copy()
        # remove the deck top trump card and cards in hand
        deck.remove(deck_top)
        for card in hand:
            deck.remove(card)
    else:
        deck = DECK.copy()

    # phase 1
    if phase_no == 1:
        card_suit = [card[1] for card in hand]
        # find any one the player has trump, bid zero straight away
        if trump_suit in card_suit:
            bid = 0
        # if i am the lead and no one has trump card
        elif player_no == 0:
            bid = 1
        # bid zero for any other exceptions
        else:
            bid = 0

    # phase 2 to phase 9 (except 4 and 8) or phase 11 to 18 (except 12 and 16)
    elif (2 <= phase_no <= 9 and phase_no != 4 and phase_no != 8) or (11 <=
                        phase_no <= 18 and phase_no != 12 and phase_no != 16):
        # determine the bid if i have a trump card
        # a list of cards of trumps left in deck
        trump_left = [card for card in deck if card[1] == trump_suit]
        # a list of cards of other suits left in deck
        other_suit_left = [card for card in deck if card[1] != trump_suit]
        # a list of the trump cards i have in hand
        my_trump = [card for card in hand if card[1] == trump_suit]
        # a list of cards of other suits i have in hand
        my_other_suit = [card for card in hand if card[1] != trump_suit]
        
        lst_bad_trump = []
        
        # determine the bid in a trick for trump cards i have
        for card in hand:
            if card in my_trump:
                # win_one indicates how many cards my card can win over
                win_one = 0
                for card_left in trump_left:
                    if card_value[card[0]] > card_value[card_left[0]]:
                        win_one += 1
                prob = win_one / len(trump_left)
                if 15 >= phase_no >= 5:
                    if prob > 0.65:
                        bid += 1
                    else:
                        lst_bad_trump.append(card)
                else:
                    if prob > 0.6:
                        bid += 1
                    else:
                        if len(my_trump) >= 2:
                            bid += 1
                if len(lst_bad_trump) >= 2:
                    bid += 1
            # determine the bid in a trick for cards of other suits i have
            elif card in my_other_suit:
                win_one = 0
                same_suit_left = [card_left for card_left in other_suit_left
                                  if card_left[1] == card[1]]
                for card_left in same_suit_left:
                    if card_value[card[0]] > card_value[card_left[0]]:
                        win_one += 1
                # in case i have lowest value card
                if win_one != 0 and len(same_suit_left) != 0:
                    prob = win_one/len(same_suit_left)
                    # if my card of other suit can win over certain percentages
                    # of cards of same suit for safe play
                    if 15 >= phase_no >= 5:
                        if prob >= 0.9:
                            bid += 1
                    elif phase_no == 4 or phase_no == 16:
                        if prob >= 0.8:
                            bid += 1
                    else:
                        if prob >= 0.75:
                            bid += 1
                # if my card has smallest value among cards of same suit left
                elif win_one == 0:
                    bid = 0
                # if there is no same suit left
                else:
                    bid += 1

    # phases 4, 8 and 10
    elif phase_no == 4 or phase_no == 8:
        bid = int(phase_no/4)
    elif phase_no == 10:
        bid = 0
    # phases 12 and 16
    elif phase_no == 12 or phase_no == 16:
        bid = int((20-phase_no)/4)

    # phase 19
    else:
        card_suit = [card[1] for card in hand]
        # find any one the player has trump, bid zero straight away
        if trump_suit in card_suit:
            bid = 0
        # if i am the lead and no one has trump card
        elif player_no == 0:
            bid = 1
        else:
            bid = 0




def is_valid_play(play, curr_trick, hand):
    '''
    function is valid play takes 3 arguments:
    play which is a single card representing a potential play.
    curr_trick which is a tuple of cards  that have been played in the
    curent round, with the first card being the card that was led, and an empty
    tuple indicating that you have lead.
    hand which is a tuple of cards that currently hold in your hands.
    the function then returns True if play is valid and False otherwise.
    '''

    # valid_play indicates whether the play is valid
    # initialise valid_play to False
    valid_play = False
    if play in hand:
        # if i have the lead, any play will be valid
        if len(curr_trick) == 0:
            valid_play = True
        # if i dont have the lead
        else:
            lead_suit = curr_trick[0][1]
            # a list of cards of lead suit
            matching_list = [card for card in hand if card[1] == lead_suit]
            # if i have no cards of lead suit, any card is a valid play
            if len(matching_list) == 0:
                valid_play = True
            # if i do, play is valid if it is card of lead suit
            else:
                if play in matching_list:
                    valid_play = True
            
    return valid_play




def score_phase(bids, tricks, deck_top, player_data=None,
                suppress_player_data=True):
    '''
    function score_phase takes 5 arguments:
    bids which is  4-tuple containing the bids of the players, in order of
    player_no.
    tricks which is a tuple of 4-tuples, each representing a single trick in
    the order of play, starting with the lead card, and with player number 0
    leading the first trick.
    deck_top which A string representing the card that was turned up on top
    of the deck at the start of play, which determins the trump suit for the
    phase.
    player_data which is a list of cards left in current deck, defaulted to
    None.
    suppress_player_data indicates whether the player_data will be returned,
    defaulted to True.
    the function then returns a 4_tuple of integers representing the score for
    each of the four players in the order of player_no. Or a 2-tuple containing
    the 4-tuple and the list, player_data if suppress_player_data is False.
    '''

    # trump suit is the second element of top card in the deck
    trump_suit = deck_top[1]
    # the library determins the rank of different values of cards
    value = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8,
             '0': 9, 'J': 10, 'Q': 11, 'K': 12, 'A': 13}
    # the library takes player_no as key and score of each player as values
    score = {0: 0, 1: 0, 2: 0, 3: 0}
    # list of the player_no which changes after every trick
    mylist = [0, 1, 2, 3]

    # determine who wins each trick
    for each_trick in tricks:
        lead_card = each_trick[0]
        lead_suit = each_trick[0][1]
        lead_value = each_trick[0][0]
        # initialise winning card as the first played card, card with lead suit
        win_card = lead_card
        for following_card in each_trick[1:]:
            # if the following card is a trump card
            if following_card[1] == trump_suit:
                # compare the value if previous winning card is a trump card
                if win_card[1] == trump_suit:
                    # if the following card has larger value, it becomes the
                    # winning card, otherwise, winning card remains
                    if value[following_card[0]] > value[win_card[0]]:
                        win_card = following_card
                # if no trump card played, the trump card becomes winning card
                else:
                    win_card = following_card
            # if following card's suit is same as lead suit
            elif following_card[1] == lead_suit:
                # if current winning card is not a trump card,
                # compare the value of two cards with lead suit
                if win_card[1] != trump_suit:
                    if value[following_card[0]] > value[lead_value]:
                        win_card = following_card
                # if current winning card is a trump card,
                # it remains as winning card
                else:
                    continue
            else:
                continue

        # obtain the winner number of each trick
        win_player_no = list(each_trick).index(win_card)
        # score one for winning a trick by calling the library
        score[mylist[win_player_no]] += 1
        # update the player order
        if win_player_no == 1:
            neworder = [1, 2, 3, 0]
            mylist = [mylist[i] for i in neworder]
        elif win_player_no == 2:
            neworder = [2, 3, 0, 1]
            mylist = [mylist[i] for i in neworder]
        elif win_player_no == 3:
            neworder = [3, 0, 1, 2]
            mylist = [mylist[i] for i in neworder]
        else:
            continue

    # score the bid at the end if the trick players have won equals to the bid
    for n in range(4):
        if bids[n] == score[n]:
            score[n] += 10
    scores = tuple(score.values())

    # remove the card from the deck(player_data) and pass on to next function
    if player_data is not None:
        for each_trick in tricks:
            for card in each_trick:
                player_data.remove(card)
        player_data.remove(deck_top)

    if suppress_player_data is False:
        return (scores, player_data)
    else:
        return scores







def bid(hand, player_no, phase_no, deck_top, reshuffled=False,
        player_data=None, suppress_player_data=True):
    '''
    bid function takes 7 arguments:
    hand which is a tuple of cards that you have been dealt for the current
    phase, in the case of phase 1 and 19, it represents the cards of other
    players.
    player_no indicates your player order in the current phase.
    phase_no an integer indicates the phase number of the current hand.
    deck_top which is used to determine the trumps for the current phase.
    reshuffled indicates whether the deck was reshuffled, defaulted to False.
    plyaer_data, indicate the cards in the deck in current phase.
    suppress_player_data indicates whether the function should return only
    the bid or with player_data, defaulted to True.
    bid funtion then reutns an integer between 0 and 10 inclusive indicating
    the number of tricks you predict you will win in current phase.
    '''

    # card_value library takes values of the cards as key and rank of each
    # as value
    card_value = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,
                  '9': 8, '0': 9, 'J': 10, 'Q': 11, 'K': 12, 'A': 13}
    # second element of deck_top represents the trump suit
    trump_suit = deck_top[1]
    # initialise the bid to zero
    bid = 0
    # create a full deck
    suits = ['C', 'D', 'H', 'S']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '0', 'J', 'Q', 'K', 'A']
    DECK = []
    for suit in suits:
        for value in values:
            card = value + suit
            DECK.append(card)

    # if reshuffled is Ture, the deck should be a full deck
    if reshuffled:
        player_data = DECK.copy()

    # play_data is the deck passed on by preceding function call
    if player_data is not None:
        deck = player_data.copy()
        # remove the deck top trump card and cards in hand
        deck.remove(deck_top)
        for card in hand:
            deck.remove(card)
    else:
        deck = DECK.copy()

    # phase 1
    if phase_no == 1:
        card_suit = [card[1] for card in hand]
        # find any one the player has trump, bid zero straight away
        if trump_suit in card_suit:
            bid = 0
        # if i am the lead and no one has trump card
        elif player_no == 0:
            bid = 1
        # bid zero for any other exceptions
        else:
            bid = 0

    # phase 2 to phase 9 (except 4 and 8) or phase 11 to 18 (except 12 and 16)
    elif (2 <= phase_no <= 9 and phase_no != 4 and phase_no != 8) or (11 <=
                        phase_no <= 18 and phase_no != 12 and phase_no != 16):
        # determine the bid if i have a trump card
        # a list of cards of trumps left in deck
        trump_left = [card for card in deck if card[1] == trump_suit]
        # a list of cards of other suits left in deck
        other_suit_left = [card for card in deck if card[1] != trump_suit]
        # a list of the trump cards i have in hand
        my_trump = [card for card in hand if card[1] == trump_suit]
        # a list of cards of other suits i have in hand
        my_other_suit = [card for card in hand if card[1] != trump_suit]

        small_trump = []
        # determine the bid in a trick for trump cards i have
        for card in hand:
            if card in my_trump:
                # win_one indicates how many cards my card can win over
                win_one = 0
                for card_left in trump_left:
                    if card_value[card[0]] > card_value[card_left[0]]:
                        win_one += 1
                prob = win_one / len(trump_left)
                if 15 >= phase_no >= 5:
                    if prob > 0.65:
                        bid += 1
                    else:
                        small_trump.append(card)
                else:
                    if prob > 0.6:
                        bid += 1
                if len(small_trump) >= 2:
                    bid += 1

            # determine the bid in a trick for cards of other suits i have
            elif card in my_other_suit:
                win_one = 0
                same_suit_left = [card_left for card_left in other_suit_left
                                  if card_left[1] == card[1]]
                for card_left in same_suit_left:
                    if card_value[card[0]] > card_value[card_left[0]]:
                        win_one += 1
                # in case i have lowest value card
                if win_one != 0 and len(same_suit_left) != 0:
                    prob = win_one/len(same_suit_left)
                    # if my card of other suit can win over certain percentages
                    # of cards of same suit for safe play
                    if 15 >= phase_no >= 5:
                        if prob >= 0.9:
                            bid += 1
                    elif phase_no == 4 or phase_no == 16:
                        if prob >= 0.8:
                            bid += 1
                    else:
                        if prob >= 0.75:
                            bid += 1
                # if my card has smallest value among cards of same suit left
                elif win_one == 0:
                    bid = 0
                # if there is no same suit left
                else:
                    bid += 1

    # phases 4, 8 and 10
    elif phase_no == 4 or phase_no == 8:
        bid = int(phase_no/4)
    elif phase_no == 10:
        bid = 0
    # phases 12 and 16
    elif phase_no == 12 or phase_no == 16:
        bid = int((20-phase_no)/4)

    # phase 19
    else:
        card_suit = [card[1] for card in hand]
        # find any one the player has trump, bid zero straight away
        if trump_suit in card_suit:
            bid = 0
        # if i am the lead and no one has trump card
        elif player_no == 0:
            bid = 1
        else:
            bid = 0

    # suppress_player_data indicates whether player_data should be returned
    if suppress_player_data is False:
        return (bid, player_data)
    else:
        return bid






def is_valid_play(play, curr_trick, hand):
    '''
    function is valid play takes 3 arguments:
    play which is a single card representing a potential play.
    curr_trick which is a tuple of cards  that have been played in the
    curent round, with the first card being the card that was led, and an empty
    tuple indicating that you have lead.
    hand which is a tuple of cards that currently hold in your hands.
    the function then returns True if play is valid and False otherwise.
    '''

    # valid_play indicates whether the play is valid
    # initialise valid_play to False
    valid_play = False
    if play in hand:
        # if i have the lead, any play will be valid
        if len(curr_trick) == 0:
            valid_play = True
        # if i dont have the lead
        else:
            lead_suit = curr_trick[0][1]
            # a list of cards of lead suit
            matching_list = [card for card in hand if card[1] == lead_suit]
            # if i have no cards of lead suit, any card is a valid play
            if len(matching_list) == 0:
                valid_play = True
            # if i do, play is valid if it is card of lead suit
            else:
                if play in matching_list:
                    valid_play = True
            
    return valid_play

def score_phase(bids, tricks, deck_top, player_data=None,
                suppress_player_data=True):
    '''
    function score_phase takes 5 arguments:
    bids which is  4-tuple containing the bids of the players, in order of
    player_no.
    tricks which is a tuple of 4-tuples, each representing a single trick in
    the order of play, starting with the lead card, and with player number 0
    leading the first trick.
    deck_top which A string representing the card that was turned up on top
    of the deck at the start of play, which determins the trump suit for the
    phase.
    player_data which is a list of cards left in current deck, defaulted to
    None.
    suppress_player_data indicates whether the player_data will be returned,
    defaulted to True.
    the function then returns a 4_tuple of integers representing the score for
    each of the four players in the order of player_no. Or a 2-tuple containing
    the 4-tuple and the list, player_data if suppress_player_data is False.
    '''

    # trump suit is the second element of top card in the deck
    trump_suit = deck_top[1]
    # the library determins the rank of different values of cards
    value = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8,
             '0': 9, 'J': 10, 'Q': 11, 'K': 12, 'A': 13}
    # the library takes player_no as key and score of each player as values
    score = {0: 0, 1: 0, 2: 0, 3: 0}
    # list of the player_no which changes after every trick
    mylist = [0, 1, 2, 3]

    # determine who wins each trick
    for each_trick in tricks:
        lead_card = each_trick[0]
        lead_suit = each_trick[0][1]
        lead_value = each_trick[0][0]
        # initialise winning card as the first played card, card with lead suit
        win_card = lead_card
        for following_card in each_trick[1:]:
            # if the following card is a trump card
            if following_card[1] == trump_suit:
                # compare the value if previous winning card is a trump card
                if win_card[1] == trump_suit:
                    # if the following card has larger value, it becomes the
                    # winning card, otherwise, winning card remains
                    if value[following_card[0]] > value[win_card[0]]:
                        win_card = following_card
                # if no trump card played, the trump card becomes winning card
                else:
                    win_card = following_card
            # if following card's suit is same as lead suit
            elif following_card[1] == lead_suit:
                # if current winning card is not a trump card,
                # compare the value of two cards with lead suit
                if win_card[1] != trump_suit:
                    if value[following_card[0]] > value[lead_value]:
                        win_card = following_card
                # if current winning card is a trump card,
                # it remains as winning card
                else:
                    continue
            else:
                continue

        # obtain the winner number of each trick
        win_player_no = list(each_trick).index(win_card)
        # score one for winning a trick by calling the library
        score[mylist[win_player_no]] += 1
        # update the player order
        if win_player_no == 1:
            neworder = [1, 2, 3, 0]
            mylist = [mylist[i] for i in neworder]
        elif win_player_no == 2:
            neworder = [2, 3, 0, 1]
            mylist = [mylist[i] for i in neworder]
        elif win_player_no == 3:
            neworder = [3, 0, 1, 2]
            mylist = [mylist[i] for i in neworder]
        else:
            continue

    # score the bid at the end if the trick players have won equals to the bid
    for n in range(4):
        if bids[n] == score[n]:
            score[n] += 10
    scores = tuple(score.values())

    # remove the card from the deck(player_data) and pass on to next function
    if player_data is not None:
        for each_trick in tricks:
            for card in each_trick:
                player_data.remove(card)
        player_data.remove(deck_top)

    if suppress_player_data is False:
        return (scores, player_data)
    else:
        return scores

def pick_smallest(card_lst):
    '''
    pick_smallest function is a helper function used in play, which takes a 
    list of cards and return a card with the smallest value.
    '''
    # card_value is a dictionary that takes values of cards as keys and ranks
    # of them as values
    card_value = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,
                  '9': 8, '0': 9, 'J': 10, 'Q': 11, 'K': 12, 'A': 13}
    # the card with smallest value is initialised as first card in the list
    smallest = card_lst[0]
    for card in card_lst[1:]:
        if card_value[card[0]] < card_value[smallest[0]]:
            smallest = card
    play_card = smallest
    return play_card

def pick_largest(card_lst):
    '''
    pick_largest function is a helper function used in play, which takes a 
    list of cards and return a card with the largest value.
    '''
    # card_value is a dictionary that takes values of cards as keys and ranks
    # of them as values
    card_value = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,
                  '9': 8, '0': 9, 'J': 10, 'Q': 11, 'K': 12, 'A': 13}
    # the card with largest value is initialised as first card in the list
    largest = card_lst[0]
    for card in card_lst[1:]:
        if card_value[card[0]] > card_value[largest[0]]:
            largest = card
    play_card = largest
    return play_card

def play(curr_trick, hand, prev_tricks, player_no, deck_top, phase_bids,
         player_data=None, suppress_player_data=True, is_valid=is_valid_play,
         score=score_phase):
    '''
    play function takes 9 arguments:
    curr_trick is a tuple containing the cards played in the current incomplete
    trick.
    hand is a tuple of cards (each in the form of a string) remaining in your
    hand for the current phase.
    prev_tricks is a tuple of 4-tuples, which are the completed tricks of the
    current phase.
    player_no is an integer between 0 and 3 inclusive indicating player order
    for the current phase.
    deck_top is the top card of the deck, used to determine trumps for the
    current phase.
    phase_bids is a 4-tuple containing the bids of the players for the current
    phase, in order of player_no.
    player_data is a list of cards left in the current deck, defaulted to None.
    suppress_player_data indicates whether the player_data should be returned,
    defaulted to True.
    is_valid is defaulted to is_valid_play function.
    score is defaulted to score_phase function.
    the function then returns a single card representing your next play, either
    as a string, or as the first element of a 2-tuple, with the second element
    being the updated player_data.
    '''

    # card_value is a dictionary that takes values of cards as keys and ranks
    # of them as values
    card_value = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,
                  '9': 8, '0': 9, 'J': 10, 'Q': 11, 'K': 12, 'A': 13}
    # play_card is the card returned at the end, initialised to an empty string
    play_card = ''

    # create a list of valid cards and sublist of trump cards and cards of
    # other suits
    for card in hand:
        valid_cards = [card for card in hand if is_valid(card, curr_trick,
                                                         hand) is True]
    trump_suit = deck_top[1]
    trump_suit_lst = [card for card in valid_cards if card[1] == trump_suit]
    other_suit_lst = [card for card in valid_cards if card[1] != trump_suit]

    # pass the deck on from player_data
    if player_data is not None:
        deck = player_data.copy()
    else:
        suits = ['C', 'H', 'D', 'S']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '0', 'J', 'Q', 'K',
                  'A']
        deck = []
        for suit in suits:
            for value in values:
                card = value+suit
                deck.append(card)

    # use score_phase function to get the score for players for each trick
    # and get my score using index with play_no
    each_round = score(phase_bids, prev_tricks, deck_top, deck)
    current_score = each_round[player_no]

    # i have not got my bid if my score is less than 10
    # (if i have got my bid, i will be socred 10 therefore the current_score
    # will be great or equal to 10)
    if current_score < 10:
        for valid_card in valid_cards:
            # if i have the lead
            if len(curr_trick) == 0:
                # play card of other suits with larger value first
                if len(other_suit_lst) != 0:
                    for card in other_suit_lst:
                        # if i have card with large value
                        if card[0] in '890JQKA':
                            play_card = card
                        # if i don't, try to play the smallest trump card first
                        # if fail, play random card of other suit
                        else:
                            if len(trump_suit_lst) != 0:
                                play_card = pick_smallest(trump_suit_lst)
                            else:
                                play_card = random.choice(other_suit_lst)
                # if i don't have card of other suits to play
                # play random trump card
                else:
                    play_card = pick_smallest(trump_suit_lst)

            # if i don't have the lead
            # determine card to play based on played cards in current trick
            else:
                lead_suit = curr_trick[0][1]
                # if the lead played trump card
                if lead_suit == trump_suit:
                    trump_card_played = [played_card for played_card in
                                         curr_trick if played_card[1] ==
                                         trump_suit]
                    largest = pick_largest(trump_card_played)
                    # if i have trump card(s)
                    # make a list of trump card(s) i have and play the smallest
                    # one among those that are larger than the largest one
                    # played
                    if len(trump_suit_lst) != 0:
                        potential_play = [my_card for my_card in trump_suit_lst
                                          if card_value[my_card[0]] >
                                          card_value[largest[0]]]
                        # if i have greater trump card(s)
                        if len(potential_play) != 0:
                            play_card = pick_smallest(potential_play)
                        # if i don't have greater trump card
                        else:
                            play_card = pick_smallest(trump_suit_lst)
                    # if i don't have trump card
                    # play the card of other suit with smallest value
                    else:
                        play_card = pick_smallest(other_suit_lst)

                # if the lead didn't play trump card
                else:
                    # trump_played indicates whether someone in the trick
                    # played trump, defaulted to False
                    trump_played = False
                    trump_lst = []
                    lead_card_played = [card for card in curr_trick if card[1]
                                        == lead_suit]
                    lead_card_lst = [card for card in valid_cards if card[1]
                                     == lead_suit]
                    # make a list of trump card(s) played if there are any
                    for card in curr_trick:
                        if card[1] == trump_suit:
                            trump_lst.append(card)
                            trump_played = True
                    # if someone played trump
                    if trump_played:
                        # if i have card(s) of lead suit
                        # play the smallest one to save larger value for later
                        if len(lead_card_lst) != 0:
                            play_card = pick_smallest(lead_card_lst)
                        # if i don't have card of lead suit
                        else:
                            # if i have trump card(s)
                            if len(trump_suit_lst) != 0:
                                largest = pick_largest(trump_lst)
                                potential_play = [card for card in
                                                  trump_suit_lst if
                                                  card_value[card[0]] >
                                                  card_value[largest[0]]]
                                # if i have greater trump card(s)
                                if len(potential_play) != 0:
                                    play_card = pick_smallest(potential_play)
                                else:
                                    # if i don't have greater trump card
                                    # choose to play card of other suits first
                                    if len(other_suit_lst) != 0:
                                        play_card = pick_smallest(other_suit_lst)
                                    else:
                                        play_card = pick_smallest(trump_suit_lst)
                            # if i don't have trump card
                            # play smallest card to save other cards
                            else:
                                play_card = pick_smallest(other_suit_lst)

                    # if no one played trump card
                    else:
                        largest = pick_largest(lead_card_played)
                        # if i have card(s) of lead suit
                        if len(lead_card_lst) != 0:
                            potential_play = [card for card in lead_card_lst if
                                            card_value[card[0]] >
                                            card_value[largest[0]]]
                            # if i have larger card(s) of lead suit
                            if len(potential_play) != 0:
                                play_card = pick_largest(potential_play)
                            # if i don't have larger lead suit card
                            else:
                                # i can play trump card
                                if len(trump_suit_lst) != 0:
                                    play_card = pick_smallest(trump_suit_lst)
                                # if i don't have trump card
                                # play the smallest valid card
                                else:
                                    play_card = pick_smallest(other_suit_lst)
                        # if i don't have card(s) of lead suit
                        else:
                            # if i have trump cards
                            if len(trump_suit_lst) != 0:
                                play_card = pick_smallest(trump_suit_lst)
                            # if i don't have trump cards
                            # play the smallest of valid cards
                            else:
                                play_card = pick_smallest(other_suit_lst)

    # if i have gotten my bid
    else:
        # if i am the lead
        if len(curr_trick) == 0:
            play_card = random.choice(valid_cards)
        # if i am not the lead
        else:
            lead_suit = curr_trick[0][1]
            trump_card_played = [played_card for played_card in curr_trick
                                 if played_card[1] == trump_suit]
            # if the lead played trump card
            if lead_suit == trump_suit:
                # if i have trump cards
                if len(trump_suit_lst) != 0:
                    temp_lst = trump_suit_lst.copy()
                    # if i have trump card
                    while len(temp_lst) >= 1:
                        if len(temp_lst) == 1:
                            play_card = temp_lst[0]
                            break
                        else:
                            my_largest_trump = pick_largest(temp_lst)
                            if card_value[my_largest_trump[0]] <\
                            card_value[pick_largest(trump_card_played)[0]]:
                                play_card = pick_largest(temp_lst)
                                break
                            else:
                                temp_lst.remove(my_largest_trump)
                # if i do not have trump cards
                else:
                    play_card = pick_largest(other_suit_lst)

            # if the lead didn't play trump card
            else:
                lead_card_played = [played_card for played_card in curr_trick
                                    if played_card[1] == lead_suit]
                lead_cards = [card for card in other_suit_lst if card[1] ==
                              lead_suit]
                # if i have cards of lead suit
                if len(lead_cards) != 0:
                    # if someone played trump card
                    if len(trump_card_played) != 0:
                        play_card = pick_largest(lead_cards)
                    else:
                        temp_lst = lead_cards.copy()
                        while len(temp_lst) >= 1:
                            if len(temp_lst) == 1:
                                play_card = temp_lst[0]
                                break
                            else:
                                my_largest_lead = pick_largest(temp_lst)
                                if card_value[my_largest_lead[0]] <\
                                card_value[pick_largest(lead_card_played)[0]]:
                                    play_card = pick_largest(temp_lst)
                                    break
                                else:
                                    temp_lst.remove(my_largest_lead)

                # if i do not have card of lead suit
                else:
                    # if someone played trump card
                    if len(trump_card_played) != 0:
                        # if i have trump cards
                        if len(trump_suit_lst) != 0:
                            temp_lst = trump_suit_lst.copy()
                            # play the as large value as possible but still
                            # smaller than played trump cards
                            while len(temp_lst) >= 1:
                                if len(temp_lst) == 1:
                                    if card_value[temp_lst[0][0]] < card_value\
                                    [pick_largest(trump_card_played)[0]]:
                                        play_card = temp_lst[0]
                                        break
                                    else:
                                        if len(other_suit_lst) != 0:
                                            play_card = pick_largest(other_suit_lst)
                                            break
                                        else:
                                            play_card = random.choice(valid_cards)
                                            break
                                else:
                                    my_largest_trump = pick_largest(temp_lst)
                                    if card_value[my_largest_trump[0]] <\
                                    card_value[pick_largest(trump_card_played)[0]]:
                                        play_card = pick_largest(temp_lst)
                                        break
                                    else:
                                        temp_lst.remove(my_largest_trump)
                        # if i do not have trump card
                        # play the largest value of other suits
                        else:
                            play_card = pick_largest(other_suit_lst)
                    # if no one played trump card
                    else:
                        if len(other_suit_lst) != 0:
                            play_card = pick_largest(other_suit_lst)
                        else:
                            play_card = random.choice(valid_cards)

    if suppress_player_data is False:
        return (play_card, player_data)
    else:
        return play_card







def bonus_bid(hand, prev_bids, phase_no, deck_top, reshuffled=False,
              player_data=None, suppress_player_data=True):
    '''
    bonus_bid function takes 7 arguments:
    hand which is a tuple of cards that you have been dealt for the current
    phase, in the case of phase 1 and 19, it represents the cards of other
    players.
    prev_bids is a tuple of non-negative integers representing the bids of the
    preceeding players.
    phase_no an integer indicates the phase number of the current hand.
    deck_top which is used to determine the trumps for the current phase.
    reshuffled indicates whether the deck was reshuffled, defaulted to False.
    plyaer_data, indicate the cards in the deck in current phase.
    suppress_player_data indicates whether the function should return only
    the bid or with player_data, defaulted to True.
    bid funtion then reutns an integer between 0 and 10 inclusive indicating
    the number of tricks you predict you will win in current phase.
    '''

    # card_value library takes values of the cards as key and rank of each
    # as value
    card_value = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,
                  '9': 8, '0': 9, 'J': 10, 'Q': 11, 'K': 12, 'A': 13}
    # second element of deck_top represents the trump suit
    trump_suit = deck_top[1]
    # initialise the bid to zero
    bid = 0
    # create a full deck
    suits = ['C', 'D', 'H', 'S']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '0', 'J', 'Q', 'K', 'A']
    DECK = []
    for suit in suits:
        for value in values:
            card = value + suit
            DECK.append(card)

    # if reshuffled is Ture, the deck should be a full deck
    if reshuffled:
        player_data = DECK.copy()
    
    # play_data is the deck passed on by preceding function call
    if player_data is not None:
        deck = player_data.copy()
        # remove the deck top trump card and cards in hand
        deck.remove(deck_top)
        for card in hand:
            deck.remove(card)
    else:
        deck = DECK.copy()
    
    player_no = len(prev_bids)
    # phase 1
    if phase_no == 1:
        if player_no == 3:
            count_bid = 0
            for bid in prev_bids:
                if bid == 0:
                    count_bid += 1
            if count_bid == 3:
                bid = 1
            else:
                bid = 0
        # find any one the player has trump, bid zero straight away
        else:
            card_suit = [card[1] for card in hand]
            if trump_suit in card_suit:
                bid = 0
            # if i am the lead and no one has trump card
            elif player_no == 0:
                bid = 1
            # bid zero for any other exceptions
            else:
                bid = 0

    # phase 2 to phase 9 (except 4 and 8) or phase 11 to 18 (except 12 and 16)
    elif (2 <= phase_no <= 9 and phase_no != 4 and phase_no != 8) or (11 <=
                        phase_no <= 18 and phase_no != 12 and phase_no != 16):
        # a list of cards of trumps left in deck
        trump_left = [card for card in deck if card[1] == trump_suit]
        # a list of cards of other suits left in deck
        other_suit_left = [card for card in deck if card[1] != trump_suit]
        # a list of the trump cards i have in hand
        my_trump = [card for card in hand if card[1] == trump_suit]
        # a list of cards of other suits i have in hand
        my_other_suit = [card for card in hand if card[1] != trump_suit]

        count_risk = 0
        for bid in prev_bids:
            count_risk += bid
        count_risk = count_risk * 0.5
        trump_risk = count_risk * 3 / 5
        other_suit_risk = count_risk - trump_risk
        
        small_trump = []
        # determine the bid in a trick for trump cards i have
        for card in hand:
            if card in my_trump:
                # win_one indicates how many cards my card can win over
                win_one = 0
                for card_left in trump_left:
                    if card_value[card[0]] > card_value[card_left[0]]:
                        win_one += 1
                prob = (win_one - trump_risk)/len(trump_left)
                if 15 >= phase_no >= 5:
                    if prob > 0.65:
                        bid += 1
                    else:
                        small_trump.append(card)
                else:
                    if prob > 0.6:
                        bid += 1
                if len(small_trump) >= 2:
                    bid += 1
            # determine the bid in a trick for cards of other suits i have
            elif card in my_other_suit:
                win_one = 0
                same_suit_left = [card_left for card_left in other_suit_left
                                  if card_left[1] == card[1]]
                for card_left in same_suit_left:
                    if card_value[card[0]] > card_value[card_left[0]]:
                        win_one += 1
                # in case i have lowest value card
                if win_one != 0 and len(same_suit_left) != 0:
                    prob = (win_one - other_suit_risk)/len(same_suit_left)
                    # if my card of other suit can win over certain percentages
                    # of cards of same suit for safe play
                    if 15 >= phase_no >= 5:
                        if prob >= 0.9:
                            bid += 1
                    elif phase_no == 4 or phase_no == 16:
                        if prob >= 0.8:
                            bid += 1
                    else:
                        if prob >= 0.75:
                            bid += 1
                # if my card has smallest value among cards of same suit left
                elif win_one == 0:
                    bid = 0
                # if there is no same suit left
                else:
                    bid += 1

    # phases 4, 8 and 10
    elif phase_no == 4 or phase_no == 8:
        bid = int(phase_no/4)
    elif phase_no == 10:
        bid = 0
    # phases 12 and 16
    elif phase_no == 12 or phase_no == 16:
        bid = int((20-phase_no)/4)

    # phase 19
    else:
        card_suit = [card[1] for card in hand]
        # find any one the player has trump, bid zero straight away
        if trump_suit in card_suit:
            bid = 0
        # if i am the lead and no one has trump card
        elif player_no == 0:
            bid = 1
        else:
            bid = 0

    # suppress_player_data indicates whether player_data should be returned
    if suppress_player_data is False:
        return (bid, player_data)
    else:
        return bid

def is_valid_play(play, curr_trick, hand):
    '''
    function is valid play takes 3 arguments:
    play which is a single card representing a potential play.
    curr_trick which is a tuple of cards  that have been played in the
    curent round, with the first card being the card that was led, and an empty
    tuple indicating that you have lead.
    hand which is a tuple of cards that currently hold in your hands.
    the function then returns True if play is valid and False otherwise.
    '''

    # valid_play indicates whether the play is valid
    # initialise valid_play to False
    valid_play = False
    if play in hand:
        # if i have the lead, any play will be valid
        if len(curr_trick) == 0:
            valid_play = True
        # if i dont have the lead
        else:
            lead_suit = curr_trick[0][1]
            # a list of cards of lead suit
            matching_list = [card for card in hand if card[1] == lead_suit]
            # if i have no cards of lead suit, any card is a valid play
            if len(matching_list) == 0:
                valid_play = True
            # if i do, play is valid if it is card of lead suit
            else:
                if play in matching_list:
                    valid_play = True
            
    return valid_play

def score_phase(bids, tricks, deck_top, player_data=None,
                suppress_player_data=True):
    '''
    function score_phase takes 5 arguments:
    bids which is  4-tuple containing the bids of the players, in order of
    player_no.
    tricks which is a tuple of 4-tuples, each representing a single trick in
    the order of play, starting with the lead card, and with player number 0
    leading the first trick.
    deck_top which A string representing the card that was turned up on top
    of the deck at the start of play, which determins the trump suit for the
    phase.
    player_data which is a list of cards left in current deck, defaulted to
    None.
    suppress_player_data indicates whether the player_data will be returned,
    defaulted to True.
    the function then returns a 4_tuple of integers representing the score for
    each of the four players in the order of player_no. Or a 2-tuple containing
    the 4-tuple and the list, player_data if suppress_player_data is False.
    '''

    # trump suit is the second element of top card in the deck
    trump_suit = deck_top[1]
    # the library determins the rank of different values of cards
    value = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8,
             '0': 9, 'J': 10, 'Q': 11, 'K': 12, 'A': 13}
    # the library takes player_no as key and score of each player as values
    score = {0: 0, 1: 0, 2: 0, 3: 0}
    # list of the player_no which changes after every trick
    mylist = [0, 1, 2, 3]

    # determine who wins each trick
    for each_trick in tricks:
        lead_card = each_trick[0]
        lead_suit = each_trick[0][1]
        lead_value = each_trick[0][0]
        # initialise winning card as the first played card, card with lead suit
        win_card = lead_card
        for following_card in each_trick[1:]:
            # if the following card is a trump card
            if following_card[1] == trump_suit:
                # compare the value if previous winning card is a trump card
                if win_card[1] == trump_suit:
                    # if the following card has larger value, it becomes the
                    # winning card, otherwise, winning card remains
                    if value[following_card[0]] > value[win_card[0]]:
                        win_card = following_card
                # if no trump card played, the trump card becomes winning card
                else:
                    win_card = following_card
            # if following card's suit is same as lead suit
            elif following_card[1] == lead_suit:
                # if current winning card is not a trump card,
                # compare the value of two cards with lead suit
                if win_card[1] != trump_suit:
                    if value[following_card[0]] > value[lead_value]:
                        win_card = following_card
                # if current winning card is a trump card,
                # it remains as winning card
                else:
                    continue
            else:
                continue

        # obtain the winner number of each trick
        win_player_no = list(each_trick).index(win_card)
        # score one for winning a trick by calling the library
        score[mylist[win_player_no]] += 1
        # update the player order
        if win_player_no == 1:
            neworder = [1, 2, 3, 0]
            mylist = [mylist[i] for i in neworder]
        elif win_player_no == 2:
            neworder = [2, 3, 0, 1]
            mylist = [mylist[i] for i in neworder]
        elif win_player_no == 3:
            neworder = [3, 0, 1, 2]
            mylist = [mylist[i] for i in neworder]
        else:
            continue

    # score the bid at the end if the trick players have won equals to the bid
    for n in range(4):
        if bids[n] == score[n]:
            score[n] += 10
    scores = tuple(score.values())

    # remove the card from the deck(player_data) and pass on to next function
    if player_data is not None:
        for each_trick in tricks:
            for card in each_trick:
                player_data.remove(card)
        player_data.remove(deck_top)

    if suppress_player_data is False:
        return (scores, player_data)
    else:
        return scores

def pick_smallest(card_lst):
    '''
    pick_smallest function is a helper function used in play, which takes a 
    list of cards and return a card with the smallest value.
    '''
    # card_value is a dictionary that takes values of cards as keys and ranks
    # of them as values
    card_value = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,
                  '9': 8, '0': 9, 'J': 10, 'Q': 11, 'K': 12, 'A': 13}
    # the card with smallest value is initialised as first card in the list
    smallest = card_lst[0]
    for card in card_lst[1:]:
        if card_value[card[0]] < card_value[smallest[0]]:
            smallest = card
    play_card = smallest
    return play_card

def pick_largest(card_lst):
    '''
    pick_largest function is a helper function used in play, which takes a 
    list of cards and return a card with the largest value.
    '''
    # card_value is a dictionary that takes values of cards as keys and ranks
    # of them as values
    card_value = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,
                  '9': 8, '0': 9, 'J': 10, 'Q': 11, 'K': 12, 'A': 13}
    # the card with largest value is initialised as first card in the list
    largest = card_lst[0]
    for card in card_lst[1:]:
        if card_value[card[0]] > card_value[largest[0]]:
            largest = card
    play_card = largest
    return play_card

def play(curr_trick, hand, prev_tricks, player_no, deck_top, phase_bids,
         player_data=None, suppress_player_data=True, is_valid=is_valid_play,
         score=score_phase):
    '''
    play function takes 9 arguments:
    curr_trick is a tuple containing the cards played in the current incomplete
    trick.
    hand is a tuple of cards (each in the form of a string) remaining in your
    hand for the current phase.
    prev_tricks is a tuple of 4-tuples, which are the completed tricks of the
    current phase.
    player_no is an integer between 0 and 3 inclusive indicating player order
    for the current phase.
    deck_top is the top card of the deck, used to determine trumps for the
    current phase.
    phase_bids is a 4-tuple containing the bids of the players for the current
    phase, in order of player_no.
    player_data is a list of cards left in the current deck, defaulted to None.
    suppress_player_data indicates whether the player_data should be returned,
    defaulted to True.
    is_valid is defaulted to is_valid_play function.
    score is defaulted to score_phase function.
    the function then returns a single card representing your next play, either
    as a string, or as the first element of a 2-tuple, with the second element
    being the updated player_data.
    '''

    # card_value is a dictionary that takes values of cards as keys and ranks
    # of them as values
    card_value = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7,
                  '9': 8, '0': 9, 'J': 10, 'Q': 11, 'K': 12, 'A': 13}
    # play_card is the card returned at the end, initialised to an empty string
    play_card = ''

    # create a list of valid cards and sublist of trump cards and cards of
    # other suits
    for card in hand:
        valid_cards = [card for card in hand if is_valid(card, curr_trick,
                                                         hand) is True]
    trump_suit = deck_top[1]
    trump_suit_lst = [card for card in valid_cards if card[1] == trump_suit]
    other_suit_lst = [card for card in valid_cards if card[1] != trump_suit]

    # pass the deck on from player_data
    if player_data is not None:
        deck = player_data.copy()
    else:
        suits = ['C', 'H', 'D', 'S']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '0', 'J', 'Q', 'K',
                  'A']
        deck = []
        for suit in suits:
            for value in values:
                card = value+suit
                deck.append(card)

    # use score_phase function to get the score for players for each trick
    # and get my score using index with play_no
    each_round = score(phase_bids, prev_tricks, deck_top, deck)
    current_score = each_round[player_no]

    # i have not got my bid if my score is less than 10
    # (if i have got my bid, i will be socred 10 therefore the current_score
    # will be great or equal to 10)
    if current_score < 10:
        for valid_card in valid_cards:
            # if i have the lead
            if len(curr_trick) == 0:
                # play card of other suits with larger value first
                if len(other_suit_lst) != 0:
                    for card in other_suit_lst:
                        # if i have card with large value
                        if card[0] in '890JQKA':
                            play_card = card
                        # if i don't, try to play the smallest trump card first
                        # if fail, play random card of other suit
                        else:
                            if len(trump_suit_lst) != 0:
                                play_card = pick_smallest(trump_suit_lst)
                            else:
                                play_card = random.choice(other_suit_lst)
                # if i don't have card of other suits to play
                # play random trump card
                else:
                    play_card = pick_smallest(trump_suit_lst)

            # if i don't have the lead
            # determine card to play based on played cards in current trick
            else:
                lead_suit = curr_trick[0][1]
                # if the lead played trump card
                if lead_suit == trump_suit:
                    trump_card_played = [played_card for played_card in
                                         curr_trick if played_card[1] ==
                                         trump_suit]
                    largest = pick_largest(trump_card_played)
                    # if i have trump card(s)
                    # make a list of trump card(s) i have and play the smallest
                    # one among those that are larger than the largest one
                    # played
                    if len(trump_suit_lst) != 0:
                        potential_play = [my_card for my_card in trump_suit_lst
                                          if card_value[my_card[0]] >
                                          card_value[largest[0]]]
                        # if i have greater trump card(s)
                        if len(potential_play) != 0:
                            play_card = pick_smallest(potential_play)
                        # if i don't have greater trump card
                        else:
                            play_card = pick_smallest(trump_suit_lst)
                    # if i don't have trump card
                    # play the card of other suit with smallest value
                    else:
                        play_card = pick_smallest(other_suit_lst)

                # if the lead didn't play trump card
                else:
                    # trump_played indicates whether someone in the trick
                    # played trump, defaulted to False
                    trump_played = False
                    trump_lst = []
                    lead_card_played = [card for card in curr_trick if card[1]
                                        == lead_suit]
                    lead_card_lst = [card for card in valid_cards if card[1]
                                     == lead_suit]
                    # make a list of trump card(s) played if there are any
                    for card in curr_trick:
                        if card[1] == trump_suit:
                            trump_lst.append(card)
                            trump_played = True
                    # if someone played trump
                    if trump_played:
                        # if i have card(s) of lead suit
                        # play the smallest one to save larger value for later
                        if len(lead_card_lst) != 0:
                            play_card = pick_smallest(lead_card_lst)
                        # if i don't have card of lead suit
                        else:
                            # if i have trump card(s)
                            if len(trump_suit_lst) != 0:
                                largest = pick_largest(trump_lst)
                                potential_play = [card for card in
                                                  trump_suit_lst if
                                                  card_value[card[0]] >
                                                  card_value[largest[0]]]
                                # if i have greater trump card(s)
                                if len(potential_play) != 0:
                                    play_card = pick_smallest(potential_play)
                                else:
                                    # if i don't have greater trump card
                                    # choose to play card of other suits first
                                    if len(other_suit_lst) != 0:
                                        play_card = pick_smallest(other_suit_lst)
                                    else:
                                        play_card = pick_smallest(trump_suit_lst)
                            # if i don't have trump card
                            # play smallest card to save other cards
                            else:
                                play_card = pick_smallest(other_suit_lst)

                    # if no one played trump card
                    else:
                        largest = pick_largest(lead_card_played)
                        # if i have card(s) of lead suit
                        if len(lead_card_lst) != 0:
                            potential_play = [card for card in lead_card_lst if
                                            card_value[card[0]] >
                                            card_value[largest[0]]]
                            # if i have larger card(s) of lead suit
                            if len(potential_play) != 0:
                                play_card = pick_largest(potential_play)
                            # if i don't have larger lead suit card
                            else:
                                # i can play trump card
                                if len(trump_suit_lst) != 0:
                                    play_card = pick_smallest(trump_suit_lst)
                                # if i don't have trump card
                                # play the smallest valid card
                                else:
                                    play_card = pick_smallest(other_suit_lst)
                        # if i don't have card(s) of lead suit
                        else:
                            # if i have trump cards
                            if len(trump_suit_lst) != 0:
                                play_card = pick_smallest(trump_suit_lst)
                            # if i don't have trump cards
                            # play the smallest of valid cards
                            else:
                                play_card = pick_smallest(other_suit_lst)

    # if i have gotten my bid
    else:
        # if i am the lead
        if len(curr_trick) == 0:
            play_card = random.choice(valid_cards)
        # if i am not the lead
        else:
            lead_suit = curr_trick[0][1]
            trump_card_played = [played_card for played_card in curr_trick
                                 if played_card[1] == trump_suit]
            # if the lead played trump card
            if lead_suit == trump_suit:
                # if i have trump cards
                if len(trump_suit_lst) != 0:
                    temp_lst = trump_suit_lst.copy()
                    # if i have trump card
                    while len(temp_lst) >= 1:
                        if len(temp_lst) == 1:
                            play_card = temp_lst[0]
                            break
                        else:
                            my_largest_trump = pick_largest(temp_lst)
                            if card_value[my_largest_trump[0]] <\
                            card_value[pick_largest(trump_card_played)[0]]:
                                play_card = pick_largest(temp_lst)
                                break
                            else:
                                temp_lst.remove(my_largest_trump)
                # if i do not have trump cards
                else:
                    play_card = pick_largest(other_suit_lst)

            # if the lead didn't play trump card
            else:
                lead_card_played = [played_card for played_card in curr_trick
                                    if played_card[1] == lead_suit]
                lead_cards = [card for card in other_suit_lst if card[1] ==
                              lead_suit]
                # if i have cards of lead suit
                if len(lead_cards) != 0:
                    # if someone played trump card
                    if len(trump_card_played) != 0:
                        play_card = pick_largest(lead_cards)
                    else:
                        temp_lst = lead_cards.copy()
                        while len(temp_lst) >= 1:
                            if len(temp_lst) == 1:
                                play_card = temp_lst[0]
                                break
                            else:
                                my_largest_lead = pick_largest(temp_lst)
                                if card_value[my_largest_lead[0]] <\
                                card_value[pick_largest(lead_card_played)[0]]:
                                    play_card = pick_largest(temp_lst)
                                    break
                                else:
                                    temp_lst.remove(my_largest_lead)

                # if i do not have card of lead suit
                else:
                    # if someone played trump card
                    if len(trump_card_played) != 0:
                        # if i have trump cards
                        if len(trump_suit_lst) != 0:
                            temp_lst = trump_suit_lst.copy()
                            # play the as large value as possible but still
                            # smaller than played trump cards
                            while len(temp_lst) >= 1:
                                if len(temp_lst) == 1:
                                    if card_value[temp_lst[0][0]] < card_value\
                                    [pick_largest(trump_card_played)[0]]:
                                        play_card = temp_lst[0]
                                        break
                                    else:
                                        if len(other_suit_lst) != 0:
                                            play_card = pick_largest(other_suit_lst)
                                            break
                                        else:
                                            play_card = random.choice(valid_cards)
                                            break
                                else:
                                    my_largest_trump = pick_largest(temp_lst)
                                    if card_value[my_largest_trump[0]] <\
                                    card_value[pick_largest(trump_card_played)[0]]:
                                        play_card = pick_largest(temp_lst)
                                        break
                                    else:
                                        temp_lst.remove(my_largest_trump)
                        # if i do not have trump card
                        # play the largest value of other suits
                        else:
                            play_card = pick_largest(other_suit_lst)
                    # if no one played trump card
                    else:
                        if len(other_suit_lst) != 0:
                            play_card = pick_largest(other_suit_lst)
                        else:
                            play_card = random.choice(valid_cards)

    if suppress_player_data is False:
        return (play_card, player_data)
    else:
        return play_card
