#!/usr/bin/env node
/**
 * MoltsPay Skill Setup - Cross-platform (Windows/Mac/Linux)
 * Installs moltspay globally and initializes wallet
 */

const { execSync, spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

const WALLET_PATH = path.join(os.homedir(), '.moltspay', 'wallet.json');

function run(cmd, silent = false) {
  try {
    return execSync(cmd, { 
      encoding: 'utf8', 
      stdio: silent ? 'pipe' : 'inherit' 
    });
  } catch (e) {
    return null;
  }
}

function commandExists(cmd) {
  const isWin = process.platform === 'win32';
  const result = spawnSync(isWin ? 'where' : 'which', [cmd], { encoding: 'utf8' });
  return result.status === 0;
}

console.log('🔧 Setting up MoltsPay skill...\n');

// 1. Install moltspay globally if not present
if (!commandExists('moltspay')) {
  console.log('📦 Installing moltspay...');
  run('npm install -g moltspay');
  console.log('✅ moltspay installed\n');
} else {
  console.log('✅ moltspay already installed\n');
}

// 2. Initialize wallet if not exists
if (!fs.existsSync(WALLET_PATH)) {
  console.log('🔐 Initializing wallet...');
  run('moltspay init --chain base --max-per-tx 2 --max-per-day 10');
  
  if (fs.existsSync(WALLET_PATH)) {
    try {
      const wallet = JSON.parse(fs.readFileSync(WALLET_PATH, 'utf8'));
      console.log('\n✅ Setup complete!');
      console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
      console.log(`📍 Wallet: ${wallet.address}`);
      console.log('⛓️  Chain: Base (mainnet)');
      console.log('💰 Limits: $2/tx, $10/day');
      console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
      console.log('⚠️  Fund wallet with USDC on Base to use services.');
    } catch (e) {
      console.log('✅ Wallet created');
    }
  }
} else {
  console.log('✅ Wallet already exists');
  run('moltspay status');
}

console.log('\n🎉 MoltsPay skill ready!');
