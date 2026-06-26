#!/usr/bin/env node

import { createInterface } from 'readline';

// Card values and suits
const VALUES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'];
const SUITS = ['❤️', '♦️', '♣️', '♠️'];

// Simple hand evaluation
function evaluateHand(cards) {
  const values = cards.map(c => c.value);
  const valueCounts = {};
  const suitCounts = {};
  
  cards.forEach(card => {
    valueCounts[card.value] = (valueCounts[card.value] || 0) + 1;
    suitCounts[card.suit] = (suitCounts[card.suit] || 0) + 1;
  });
  
  const pairs = [];
  const threeOfKinds = [];
  
  for (const [value, count] of Object.entries(valueCounts)) {
    if (count === 2) pairs.push(value);
    else if (count === 3) threeOfKinds.push(value);
  }
  
  pairs.sort((a, b) => VALUES.indexOf(b) - VALUES.indexOf(a));
  
  if (Object.values(valueCounts).includes(4)) return { rank: 3, name: 'Four of a Kind' };
  if (threeOfKinds.length > 0 && pairs.length > 0) return { rank: 4, name: 'Full House' };
  if (Object.values(suitCounts).some(count => count >= 5)) return { rank: 5, name: 'Flush' };
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
    
    // 发所有玩家的底牌（包括AI）
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
    
    // 预计算AI底牌信息（优化用）
    this.aiHands = this.players
      .filter(p => !p.isHuman)
      .map(p => ({
        playerId: p.id,
        hand: p.hand.map(card => `${card.value}${card.suit}`)
      }));
    
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
        if (humanPlayer.currentBet < this.currentBet) return { success: false, message: 'Cannot check, need to call or fold' };
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
  
  async processAITurns() {
    const activePlayers = this.players.filter(p => p.isActive);
    if (activePlayers.length <= 1) return this.calculateResults();
    
    // Check if betting round is complete
    const maxBet = Math.max(...this.players.map(p => p.currentBet));
    const allBetEqual = activePlayers.every(p => p.currentBet === maxBet);
    
    if (allBetEqual) {
      // Move to next phase
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
    
    // AI makes decisions
    const aiPlayers = this.players.filter(p => !p.isHuman && p.isActive);
    for (const player of aiPlayers) {
      await new Promise(resolve => setTimeout(resolve, 500));
      
      const handStrength = this.evaluateHandStrength(player);
      
      if (player.currentBet < this.currentBet) {
        // Need to call or fold
        if (handStrength > 0.3 || Math.random() > 0.5) {
          const callAmount = this.currentBet - player.currentBet;
          if (player.chips >= callAmount) {
            player.chips -= callAmount;
            player.currentBet = this.currentBet;
            this.pot += callAmount;
          } else {
            // 全下
            const allinAmount = player.chips;
            player.chips = 0;
            player.currentBet += allinAmount;
            this.pot += allinAmount;
          }
        } else {
          // 弃牌：保留已投入的筹码在底池
          player.isActive = false;
          // 已投入的筹码 already in pot, don't return
        }
      }
    }
    
    return this.getGameState();
  }
  
  evaluateHandStrength(player) {
    const allCards = [...player.hand, ...this.communityCards];
    const evaluation = evaluateHand(allCards);
    return 1 / evaluation.rank;
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
    
    // 使用预先保存的AI底牌信息，避免重复计算
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
    
    // 构建AI底牌揭示信息（使用预先保存的数据）
    const aiReveals = this.aiHands || [];
    
    return {
      winner: winner.player.id,
      pot: this.pot,
      evaluations: evaluations.map(e => ({
        player: e.player.id,
        hand: e.evaluation.name,
        cards: e.player.getCardString(true)
      })),
      aiReveals: aiReveals,
      message: `${winner.player.id} wins $${this.pot} with ${winner.evaluation.name}`
    };
  }
}

async function main() {
  const game = new PokerGame();
  const rl = createInterface({
    input: process.stdin,
    output: process.stdout
  });
  
  console.log('🃏 Texas Hold\'em Poker for OpenClaw');
  console.log('Type "help" for commands, "start" to begin\n');
  
  let currentState = null;
  
  function printGameState(state) {
    console.log(`\n🃏 Round ${state.round} - ${state.phase.toUpperCase()}`);
    console.log(`💰 Pot: $${state.pot} | Current Bet: $${state.currentBet}`);
    console.log(`🃏 Community: ${state.communityCards.join(' ')}`);
    console.log('👥 Players:');
    
    state.players.forEach(p => {
      const marker = p.isHuman ? '👤 YOU' : '🤖 AI';
      const active = p.isActive ? '' : ' (FOLDED)';
      console.log(`  ${marker} ${p.position}: ${p.hand} | $${p.chips}${active}`);
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
        const foldResult = game.playerAction('fold');
        console.log(foldResult.message);
        return true;
        
      case 'check':
        if (!currentState) return false;
        const checkResult = game.playerAction('check');
        console.log(checkResult.message);
        return true;
        
      case 'call':
        if (!currentState) return false;
        const callResult = game.playerAction('call');
        console.log(callResult.message);
        return true;
        
      case 'bet':
        if (!currentState) return false;
        const amount = parseInt(arg);
        if (isNaN(amount)) {
          console.log('Invalid bet amount');
          return false;
        }
        const betResult = game.playerAction('bet', amount);
        console.log(betResult.message);
        return true;
        
      case 'allin':
        if (!currentState) return false;
        const allinResult = game.playerAction('allin');
        console.log(allinResult.message);
        return true;
        
      case 'next':
        if (currentState?.phase === 'showdown') {
          currentState = game.startNewRound();
          printGameState(currentState);
        }
        return true;
        
      case 'help':
        console.log('\n📋 Commands:');
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
        console.log('Thanks for playing Texas Hold\'em Poker! 🃏');
        process.exit(0);
        return false;
        
      default:
        console.log('Unknown command. Type "help" for commands.');
        return false;
    }
  }
  
  rl.on('line', async (input) => {
    if (!currentState && input.trim().toLowerCase() !== 'start') {
      console.log('Please type "start" to begin the game.');
      return;
    }
    
    const shouldProcessAI = processCommand(input);
    
    if (shouldProcessAI && currentState) {
      setTimeout(async () => {
        const newState = await game.processAITurns();
        if (newState) {
          currentState = newState;
          printGameState(currentState);
          
          if (currentState.phase === 'showdown') {
            console.log(`\n🎯 Game Over!`);
            console.log(`💰 ${currentState.message}`);
            if (currentState.evaluations) {
              console.log('\n🏆 Showdown Results:');
              currentState.evaluations.forEach(e => {
                console.log(`  ${e.player}: ${e.hand} (${e.cards})`);
              });
            }
            console.log('\nType "next" for a new round or "quit" to exit.');
          }
        }
      }, 1000);
    }
  });
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(err => {
    console.error('Game error:', err);
    process.exit(1);
  });
}