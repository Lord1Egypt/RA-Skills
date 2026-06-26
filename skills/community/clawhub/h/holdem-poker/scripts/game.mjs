#!/usr/bin/env node

import fs from 'fs';
import path from 'path';

// Game configuration
const CONFIG = {
  STARTING_CHIPS: 100,
  SMALL_BLIND: 1,
  BIG_BLIND: 2,
  NUM_PLAYERS: 3,
  AUTO_DELAY: 1000
};

// Card values and suits
const VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'];
const SUITS = ['❤️', '♦️', '♣️', '♠️'];
const SUIT_NAMES = { '❤️': 'Hearts', '♦️': 'Diamonds', '♣️': 'Clubs', '♠️': 'Spades' };

// Hand ranking functions
function evaluateHand(cards) {
  const values = cards.map(c => c.value).sort((a, b) => VALUES.indexOf(b) - VALUES.indexOf(a));
  const suits = cards.map(c => c.suit);
  
  // Count values and suits
  const valueCounts = {};
  const suitCounts = {};
  
  cards.forEach(card => {
    valueCounts[card.value] = (valueCounts[card.value] || 0) + 1;
    suitCounts[card.suit] = (suitCounts[card.suit] || 0) + 1;
  });
  
  const pairs = [];
  const threeOfKinds = [];
  const fourOfKinds = [];
  let flush = false;
  let straight = false;
  
  // Check for flush
  for (const [suit, count] of Object.entries(suitCounts)) {
    if (count >= 5) flush = true;
  }
  
  // Check for straight and pairs
  const sortedValues = [...new Set(values.map(v => VALUES.indexOf(v)).sort((a, b) => a - b))];
  if (sortedValues.length >= 5) {
    for (let i = 0; i <= sortedValues.length - 5; i++) {
      if (sortedValues[i+4] - sortedValues[i] === 4) {
        straight = true;
        break;
      }
    }
  }
  
  // Count pairs, three of kinds, four of kinds
  for (const [value, count] of Object.entries(valueCounts)) {
    if (count === 2) pairs.push(value);
    else if (count === 3) threeOfKinds.push(value);
    else if (count === 4) fourOfKinds.push(value);
  }
  
  pairs.sort((a, b) => VALUES.indexOf(b) - VALUES.indexOf(a));
  
  // Determine hand rank
  if (flush && straight && values.includes('A') && values.includes('K')) return { rank: 1, name: 'Royal Flush', values };
  if (flush && straight) return { rank: 2, name: 'Straight Flush', values };
  if (fourOfKinds.length > 0) return { rank: 3, name: 'Four of a Kind', values: [fourOfKinds[0], ...values] };
  if (threeOfKinds.length > 0 && pairs.length > 0) return { rank: 4, name: 'Full House', values: [threeOfKinds[0], pairs[0]] };
  if (flush) return { rank: 5, name: 'Flush', values };
  if (straight) return { rank: 6, name: 'Straight', values };
  if (threeOfKinds.length > 0) return { rank: 7, name: 'Three of a Kind', values: [threeOfKinds[0], ...values] };
  if (pairs.length >= 2) return { rank: 8, name: 'Two Pair', values: [pairs[0], pairs[1], ...values] };
  if (pairs.length === 1) return { rank: 9, name: 'One Pair', values: [pairs[0], ...values] };
  
  return { rank: 10, name: 'High Card', values };
}

// Player class
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
    if (!showAll && !this.isHuman) return '??';
    return this.hand.map(card => `${card.value}${card.suit}`).join(' ');
  }
  
  makeDecision(gameState) {
    if (this.isHuman) return null; // Human player will decide via input
    
    // Simple AI logic
    const handStrength = this.evaluateHandStrength(gameState.communityCards);
    const potOdds = gameState.currentBet / gameState.pot;
    
    // AI decision making based on hand strength and pot odds
    if (handStrength > 0.7) {
      return Math.random() > 0.5 ? 'bet' : 'call';
    } else if (handStrength > 0.4) {
      return potOdds < 0.3 ? 'call' : 'fold';
    } else {
      return Math.random() > 0.3 ? 'fold' : 'check';
    }
  }
  
  evaluateHandStrength(communityCards) {
    const allCards = [...this.hand, ...communityCards];
    const evaluation = evaluateHand(allCards);
    return 1 / evaluation.rank; // Simple strength metric
  }
}

// Game class
class PokerGame {
  constructor() {
    this.players = [];
    this.deck = [];
    this.communityCards = [];
    this.pot = 0;
    this.currentBet = 0;
    this.round = 0;
    this.gamePhase = 'waiting';
    this.smallBlindPos = 0;
    this.buttonPos = 0;
    this.humanPlayer = null;
    this.initializeGame();
  }
  
  initializeGame() {
    // Create deck
    this.deck = [];
    for (const suit of SUITS) {
      for (const value of VALUES) {
        this.deck.push({ value, suit });
      }
    }
    
    // Shuffle deck
    this.shuffleDeck();
    
    // Create players
    this.players = [];
    for (let i = 0; i < CONFIG.NUM_PLAYERS; i++) {
      const isHuman = (i === 0); // First player is human (small blind)
      const player = new Player(`player${i}`, i, CONFIG.STARTING_CHIPS, isHuman);
      if (isHuman) this.humanPlayer = player;
      this.players.push(player);
    }
    
    this.smallBlindPos = 0;
    this.buttonPos = CONFIG.NUM_PLAYERS - 1;
  }
  
  shuffleDeck() {
    for (let i = this.deck.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [this.deck[i], this.deck[j]] = [this.deck[j], this.deck[i]];
    }
  }
  
  startNewRound() {
    this.round++;
    this.communityCards = [];
    this.currentBet = 0;
    this.pot = 0;
    this.gamePhase = 'pre-flop';
    
    // Reset player states
    this.players.forEach(p => {
      p.hand = [];
      p.isActive = true;
      p.currentBet = 0;
    });
    
    // Deal hole cards
    for (let i = 0; i < 2; i++) {
      this.players.forEach(p => {
        p.hand.push(this.deck.pop());
      });
    }
    
    // Post blinds
    this.players[0].chips -= CONFIG.SMALL_BLIND;
    this.players[0].currentBet = CONFIG.SMALL_BLIND;
    this.players[1].chips -= CONFIG.BIG_BLIND;
    this.players[1].currentBet = CONFIG.BIG_BLIND;
    this.pot = CONFIG.SMALL_BLIND + CONFIG.BIG_BLIND;
    this.currentBet = CONFIG.BIG_BLIND;
    
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
        hand: p.getCardString(!p.isHuman && this.gamePhase !== 'showdown'),
        isHuman: p.isHuman,
        isActive: p.isActive,
        currentBet: p.currentBet
      })),
      communityCards: this.communityCards.map(c => `${c.value}${c.suit}`),
      pot: this.pot,
      currentBet: this.currentBet,
      humanPosition: this.smallBlindPos
    };
  }
  
  async playNextAction() {
    if (this.gamePhase === 'showdown') {
      return this.calculateResults();
    }
    
    // Find next active player
    const activePlayers = this.players.filter(p => p.isActive);
    if (activePlayers.length <= 1) {
      return this.calculateResults();
    }
    
    // Check if betting round is complete
    const maxBet = Math.max(...this.players.map(p => p.currentBet));
    const allBetEqual = this.players.filter(p => p.isActive).every(p => p.currentBet === maxBet);
    
    if (allBetEqual) {
      // Move to next phase
      if (this.gamePhase === 'pre-flop') {
        this.gamePhase = 'flop';
        // Deal 3 community cards
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
      
      // Reset bets for new round
      this.players.forEach(p => p.currentBet = 0);
      this.currentBet = 0;
    }
    
    return this.getGameState();
  }
  
  playerAction(action, amount = 0) {
    const humanPlayer = this.players.find(p => p.isHuman);
    if (!humanPlayer || !humanPlayer.isActive) return false;
    
    switch (action) {
      case 'fold':
        humanPlayer.isActive = false;
        return true;
        
      case 'check':
        if (humanPlayer.currentBet < this.currentBet) return false;
        return true;
        
      case 'call':
        const callAmount = this.currentBet - humanPlayer.currentBet;
        if (humanPlayer.chips < callAmount) return false;
        humanPlayer.chips -= callAmount;
        humanPlayer.currentBet = this.currentBet;
        this.pot += callAmount;
        return true;
        
      case 'bet':
        if (amount <= this.currentBet) return false;
        if (humanPlayer.chips < amount) return false;
        const betAmount = amount - humanPlayer.currentBet;
        humanPlayer.chips -= betAmount;
        humanPlayer.currentBet = amount;
        this.pot += betAmount;
        this.currentBet = amount;
        return true;
        
      case 'allin':
        const allinAmount = humanPlayer.chips;
        humanPlayer.chips = 0;
        humanPlayer.currentBet += allinAmount;
        this.pot += allinAmount;
        if (humanPlayer.currentBet > this.currentBet) {
          this.currentBet = humanPlayer.currentBet;
        }
        return true;
        
      default:
        return false;
    }
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
    
    // Showdown - evaluate hands
    const evaluations = activePlayers.map(player => {
      const allCards = [...player.hand, ...this.communityCards];
      const evaluation = evaluateHand(allCards);
      return { player, evaluation };
    });
    
    // Sort by hand rank (lower rank = better hand)
    evaluations.sort((a, b) => {
      if (a.evaluation.rank !== b.evaluation.rank) {
        return a.evaluation.rank - b.evaluation.rank;
      }
      // Tie breaker - compare card values
      for (let i = 0; i < Math.min(a.evaluation.values.length, b.evaluation.values.length); i++) {
        const aVal = VALUES.indexOf(a.evaluation.values[i]);
        const bVal = VALUES.indexOf(b.evaluation.values[i]);
        if (aVal !== bVal) return bVal - aVal;
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
        cards: e.player.getCardString()
      })),
      message: `${winner.player.id} wins $${this.pot} with ${winner.evaluation.name}`
    };
  }
}

// Main game loop
async function main() {
  const game = new PokerGame();
  const { createInterface } = await import('readline');
  const readline = createInterface({
    input: process.stdin,
    output: process.stdout
  });
  
  // Check for command line arguments
  const args = process.argv.slice(2);
  if (args.includes('--help')) {
    console.log("Texas Hold'em Poker Game");
    console.log('Usage: node game.mjs [options]');
    console.log('Options:');
    console.log('  --start    Start a new game immediately');
    console.log('  --help     Show this help message');
    return;
  }
  
  console.log('🃏 Texas Hold\'em Poker');
  console.log('Type "help" for commands, "start" to begin');
  
  let currentState = null;
  
  function printGameState(state) {
    console.clear();
    console.log(`\n=== Round ${state.round} - ${state.phase.toUpperCase()} ===`);
    console.log(`Pot: $${state.pot} | Current Bet: $${state.currentBet}`);
    console.log(`Community: ${state.communityCards.join(' ')}`);
    console.log('\\nPlayers:');
    
    state.players.forEach(p => {
      const marker = p.isHuman ? '👤 YOU' : '🤖 AI';
      const active = p.isActive ? '' : ' (FOLDED)';
      console.log(`${marker} ${p.position}: ${p.hand} | $${p.chips}${active}`);
    });
  }
  
  function processCommand(input) {
    const parts = input.toLowerCase().trim().split(' ');
    const command = parts[0];
    const arg = parts[1];
    
    switch (command) {
      case 'start':
        currentState = game.startNewRound();
        printGameState(currentState);
        return true;
        
      case 'fold':
        if (!currentState) return false;
        game.playerAction('fold');
        return true;
        
      case 'check':
        if (!currentState) return false;
        game.playerAction('check');
        return true;
        
      case 'call':
        if (!currentState) return false;
        game.playerAction('call');
        return true;
        
      case 'bet':
        if (!currentState) return false;
        const amount = parseInt(arg);
        if (isNaN(amount)) {
          console.log('Invalid bet amount');
          return false;
        }
        return game.playerAction('bet', amount);
        
      case 'allin':
        if (!currentState) return false;
        return game.playerAction('allin');
        
      case 'next':
        if (currentState?.phase === 'showdown') {
          currentState = game.startNewRound();
          printGameState(currentState);
        }
        return true;
        
      case 'help':
        console.log('\\nCommands:');
        console.log('  start     Start a new game');
        console.log('  fold      Fold your hand');
        console.log('  check     Check (pass without betting)');
        console.log('  call      Call the current bet');
        console.log('  bet N     Bet N chips');
        console.log('  allin     Go all-in');
        console.log('  next      Start next round');
        console.log('  quit      Exit game');
        console.log('  help      Show this help');
        return false;
        
      case 'quit':
        console.log('Thanks for playing!');
        process.exit(0);
        return false;
        
      default:
        console.log('Unknown command. Type "help" for commands.');
        return false;
    }
  }
  
  // Start game if --start flag is provided
  if (args.includes('--start')) {
    currentState = game.startNewRound();
    printGameState(currentState);
  }
  
  // Main input loop
  readline.on('line', async (input) => {
    if (!currentState && input.trim().toLowerCase() !== 'start') {
      console.log('Please type "start" to begin the game.');
      return;
    }
    
    const shouldProcessAI = processCommand(input);
    
    if (shouldProcessAI && currentState) {
      // Process AI moves
      setTimeout(async () => {
        const newState = await game.playNextAction();
        if (newState) {
          currentState = newState;
          printGameState(currentState);
          
          if (currentState.phase === 'showdown') {
            console.log(`\\n🎯 ${currentState.message}`);
            if (currentState.evaluations) {
              console.log('\\nShowdown Results:');
              currentState.evaluations.forEach(e => {
                console.log(`${e.player}: ${e.hand} (${e.cards})`);
              });
            }
            console.log('\\nType "next" for a new round or "quit" to exit.');
          }
        }
      }, CONFIG.AUTO_DELAY);
    }
  });
}

// Handle graceful shutdown
process.on('SIGINT', () => {
  console.log('\\nThanks for playing Texas Hold\'em Poker!');
  process.exit(0);
});

// Run main if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(err => {
    console.error('Game error:', err);
    process.exit(1);
  });
}

export { PokerGame, Player, evaluateHand };