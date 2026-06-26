#!/usr/bin/env node

/**
 * Wallet Setup - Create or check HypurrFi wallet
 * Usage: node scripts/setup.js [--json]
 */

import { generatePrivateKey, privateKeyToAccount } from 'viem/accounts';
import { existsSync, writeFileSync, chmodSync, readFileSync } from 'fs';
import { WALLET_PATH, CHAIN } from '../lib/config.js';

const jsonFlag = process.argv.includes('--json');

function output(data) {
  if (jsonFlag) {
    console.log(JSON.stringify(data, null, 2));
  } else {
    if (data.exists) {
      console.log('✅ Wallet already exists');
      console.log('');
      console.log('Address:', data.address);
      console.log('Location:', WALLET_PATH);
    } else if (data.created) {
      console.log('✅ Wallet created!');
      console.log('');
      console.log('Address:', data.address);
      console.log('Location:', WALLET_PATH);
      console.log('');
      console.log('⚠️  Fund this address with HYPE or stablecoins before using.');
      console.log('Bridge: https://cctp.to → Hyperliquid');
    }
  }
}

async function main() {
  try {
    // Check if wallet already exists
    if (existsSync(WALLET_PATH)) {
      const data = JSON.parse(readFileSync(WALLET_PATH, 'utf8'));
      output({
        exists: true,
        address: data.address,
        path: WALLET_PATH
      });
      return;
    }
    
    // Create new wallet
    const privateKey = generatePrivateKey();
    const account = privateKeyToAccount(privateKey);
    
    const walletData = {
      address: account.address,
      privateKey: privateKey,
      chain: CHAIN.name,
      chainId: CHAIN.id,
      createdAt: new Date().toISOString()
    };
    
    writeFileSync(WALLET_PATH, JSON.stringify(walletData, null, 2));
    chmodSync(WALLET_PATH, 0o600);
    
    output({
      created: true,
      address: account.address,
      path: WALLET_PATH
    });
    
  } catch (error) {
    if (jsonFlag) {
      console.log(JSON.stringify({ error: error.message }));
    } else {
      console.error('❌ Error:', error.message);
    }
    process.exit(1);
  }
}

main();
