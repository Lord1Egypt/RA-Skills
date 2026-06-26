#!/usr/bin/env node

import { PokerGame } from './simple-game.mjs';

const game = new PokerGame();
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

async function main() {
  const readline = await import('readline');
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
  
  console.log('🃏 Texas Hold\'em Poker for OpenClaw');
  console.log('Type "help" for commands, "start" to begin\n');
  
  rl.on('line', async (input) => {
    if (!currentState && input.trim().toLowerCase() !== 'start') {
      console.log('Please type "start" to begin the game.');
      return;
    }
    
    const shouldProcessAI = processCommand(input);
    
    if (shouldProcessAI && currentState) {
      setTimeout(async () => {
        const newState = await game.playAIActions();
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