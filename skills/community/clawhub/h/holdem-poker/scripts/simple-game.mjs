#!/usr/bin/env node

import fs from 'fs';
import path from 'path';

// Card values and suits
const VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'];
const SUITS = ['❤️', '♦️', '♣️', '♠️'];

// Simple hand evaluation
function evaluateHand(cards) {
  const values = cards.map(c => c.value);
  const suits = cards.map(c => c.suit);
  
  const valueCounts = {};
  const suitCounts = {};
  
  cards.forEach(card => {
    valueCounts[card.value] = (valueCounts[card.value] || 0) + 1;
    suitCounts[card.suit] = (suitCounts[card.suit] || 0) + 1;
  });
  
  const pairs = [];
  const threeOfKinds = [];
  let flush = false;
  let straight = false;
  
  for (const [suit, count] of Object.entries(suitCounts)) {
    if (count >= 5) flush = true;
  }
  
  const sortedValues = [...new Set(values.map(v => VALUES.indexOf(v)).sort((a, b) => a - b))];
  if (sortedValues.length >= 5) {
    for (let i = 0; i <= sortedValues.length - 5; i++) {
      if (sortedValues[i+4] - sortedValues[i] === 4) {
        straight = true;
        break;
      }
    }
  }
  
  for (const [value, count] of Object.entries(valueCounts)) {
    if (count === 2) pairs.push(value);
    else if (count === 3) threeOfKinds.push(value);
  }
  
  pairs.sort((a, b) => VALUES.indexOf(b) - VALUES.indexOf(a));
  
  if (flush && straight && values.includes('A')) return { rank: 1, name: 'Royal Flush' };
  if (flush && straight) return { rank: 2, name: 'Straight Flush' };
  if (Object.values(valueCounts).includes(4)) return { rank: 3, name: 'Four of a Kind' };
  if (threeOfKinds.length > 0 && pairs.length > 0) return { rank: 4, name: 'Full House' };
  if (flush) return { rank: 5, name: 'Flush' };
  if (straight) return { rank: 6, name: 'Straight' };
  if (threeOfKinds.length > 0) return { rank: 7, name: 'Three of a Kind' };
  if (pairs.length >= 2) return { rank: 8, name: 'Two Pair' };
  if (pairs.length === 1) return { rank: 9, name: 'One Pair' };
  
  return { rank: 10, name: 'High Card' };
}

class Player {
  constructor(id, position, chips, isHuman = false) {
    this.id = id;
    this.position = position;
    this.chips = chips;
    this.hand = [];
    this.isHuman = isHuman;
    this.isActive = true;
    this.currentBet = 0;
  }
  
  getCardString(showAll = false) {
    if (this.hand.length === 0) return '??';
    // Always hide AI cards until showdown
    if (!this.isHuman && !showAll) return '??';
    return this.hand.map(card => `${card.value}${card.suit}`).join(' ');
  }
}

class PokerGame {
  constructor() {
    this.players = [];
    this.deck = [];
    this.communityCards = [];
    this.pot = 0;
    this.currentBet = 0;
    this.round = 0;
    this.gamePhase = 'waiting';
    this.humanPlayer = null;
    this.initializeGame();
  }
  
  initializeGame() {
    this.deck = [];
    for (const suit of SUITS) {
      for (const value of VALUES) {
        this.deck.push({ value, suit });
      }
    }
    
    for (let i = this.deck.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [this.deck[i], this.deck[j]] = [this.deck[j], this.deck[i]];
    }
    
    this.players = [];
    for (let i = 0; i < 3; i++) {
      const isHuman = (i === 0);
      const player = new Player(`player${i}`, i, 100, isHuman);
      if (isHuman) this.humanPlayer = player;
      this.players.push(player);
    }
  }
  
  startNewRound() {
    this.round++;
    this.communityCards = [];
    this.currentBet = 0;
    this.pot = 0;
    this.gamePhase = 'pre-flop';
    
    this.players.forEach(p => {
      p.hand = [];
      p.isActive = true;
      p.currentBet = 0;
    });
    
    for (let i = 0; i < 2; i++) {
      this.players.forEach(p => {
        p.hand.push(this.deck.pop());
      });
    }
    
    this.players[0].chips -= 1;
    this.players[0].currentBet = 1;
    this.players[1].chips -= 2;
    this.players[1].currentBet = 2;
    this.pot = 3;
    this.currentBet = 2;
    
    return this.getGameState();
  }
  
  getGameState() {
    return {
      round: this.round,
      phase: this.gamePhase,
      players: this.players.map(p => ({
        id: p.id,
        position: p.position,
        chips: p.chips,
        hand: p.getCardString(this.gamePhase === 'showdown'),
        isHuman: p.isHuman,
        isActive: p.isActive,
        currentBet: p.currentBet
      })),
      communityCards: this.communityCards.map(c => `${c.value}${c.suit}`),
      pot: this.pot,
      currentBet: this.currentBet
    };
  }
  
  playerAction(action, amount = 0) {
    const humanPlayer = this.players.find(p => p.isHuman);
    if (!humanPlayer || !humanPlayer.isActive) return { success: false, message: 'Cannot act' };
    
    switch (action) {
      case 'fold':
        humanPlayer.isActive = false;
        return { success: true, message: 'You folded' };
        
      case 'check':
        if (humanPlayer.currentBet < this.currentBet) return { success: false, message: 'Cannot check' };
        return { success: true, message: 'You checked' };
        
      case 'call':
        const callAmount = this.currentBet - humanPlayer.currentBet;
        if (humanPlayer.chips < callAmount) return { success: false, message: 'Not enough chips' };
        humanPlayer.chips -= callAmount;
        humanPlayer.currentBet = this.currentBet;
        this.pot += callAmount;
        return { success: true, message: `You called $${callAmount}` };
        
      case 'bet':
        if (amount <= this.currentBet) return { success: false, message: 'Bet must be higher than current bet' };
        if (humanPlayer.chips < amount) return { success: false, message: 'Not enough chips' };
        const betAmount = amount - humanPlayer.currentBet;
        humanPlayer.chips -= betAmount;
        humanPlayer.currentBet = amount;
        this.pot += betAmount;
        this.currentBet = amount;
        return { success: true, message: `You bet $${amount}` };
        
      case 'allin':
        const allinAmount = humanPlayer.chips;
        humanPlayer.chips = 0;
        humanPlayer.currentBet += allinAmount;
        this.pot += allinAmount;
        if (humanPlayer.currentBet > this.currentBet) {
          this.currentBet = humanPlayer.currentBet;
        }
        return { success: true, message: `You went all-in with $${allinAmount}` };
        
      default:
        return { success: false, message: 'Invalid action' };
    }
  }
  
  async playAIActions() {
    const activeAIPlayers = this.players.filter(p => !p.isHuman && p.isActive);
    
    for (const player of activeAIPlayers) {
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      if (player.currentBet < this.currentBet && Math.random() > 0.3) {
        // Call or fold
        const callAmount = this.currentBet - player.currentBet;
        if (player.chips >= callAmount) {
          player.chips -= callAmount;
          player.currentBet = this.currentBet;
          this.pot += callAmount;
        } else {
          player.isActive = false;
        }
      }
    }
    
    // Move to next phase if all bets are equal
    const activePlayers = this.players.filter(p => p.isActive);
    const maxBet = Math.max(...this.players.map(p => p.currentBet));
    const allBetEqual = activePlayers.every(p => p.currentBet === maxBet);
    
    if (allBetEqual && activePlayers.length > 1) {
      if (this.gamePhase === 'pre-flop') {
        this.gamePhase = 'flop';
        this.communityCards.push(this.deck.pop(), this.deck.pop(), this.deck.pop());
      } else if (this.gamePhase === 'flop') {
        this.gamePhase = 'turn';
        this.communityCards.push(this.deck.pop());
      } else if (this.gamePhase === 'turn') {
        this.gamePhase = 'river';
        this.communityCards.push(this.deck.pop());
      } else if (this.gamePhase === 'river') {
        this.gamePhase = 'showdown';
        return this.calculateResults();
      }
      
      this.players.forEach(p => p.currentBet = 0);
      this.currentBet = 0;
    }
    
    return this.getGameState();
  }
  
  calculateResults() {
    const activePlayers = this.players.filter(p => p.isActive);
    
    if (activePlayers.length === 0) {
      return { winner: null, pot: this.pot, message: 'All players folded' };
    }
    
    if (activePlayers.length === 1) {
      activePlayers[0].chips += this.pot;
      return {
        winner: activePlayers[0].id,
        pot: this.pot,
        message: `${activePlayers[0].id} wins $${this.pot} by default`
      };
    }
    
    const evaluations = activePlayers.map(player => {
      const allCards = [...player.hand, ...this.communityCards];
      const evaluation = evaluateHand(allCards);
      return { player, evaluation };
    });
    
    evaluations.sort((a, b) => {
      if (a.evaluation.rank !== b.evaluation.rank) {
        return a.evaluation.rank - b.evaluation.rank;
      }
      return 0;
    });
    
    const winner = evaluations[0];
    winner.player.chips += this.pot;
    
    return {
      winner: winner.player.id,
      pot: this.pot,
      evaluations: evaluations.map(e => ({
        player: e.player.id,
        hand: e.evaluation.name,
        cards: e.player.getCardString(true)
      })),
      message: `${winner.player.id} wins $${this.pot} with ${winner.evaluation.name}`
    };
  }
}

export { PokerGame, Player };