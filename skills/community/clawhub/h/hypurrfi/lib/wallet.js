/**
 * Wallet utilities for HypurrFi skill
 */

import { createPublicClient, createWalletClient, http } from 'viem';
import { privateKeyToAccount } from 'viem/accounts';
import { readFileSync, existsSync, writeFileSync, chmodSync } from 'fs';
import { CHAIN, WALLET_PATH } from './config.js';

// Custom chain definition for HyperEVM
const hyperEvm = {
  id: CHAIN.id,
  name: CHAIN.name,
  nativeCurrency: {
    decimals: 18,
    name: 'HYPE',
    symbol: 'HYPE'
  },
  rpcUrls: {
    default: { http: [CHAIN.rpc] }
  },
  blockExplorers: {
    default: { name: 'Explorer', url: CHAIN.explorer }
  }
};

/**
 * Check if wallet exists
 */
export function walletExists() {
  return existsSync(WALLET_PATH);
}

/**
 * Get wallet address without loading private key
 */
export function getAddress() {
  if (!walletExists()) return null;
  try {
    const data = JSON.parse(readFileSync(WALLET_PATH, 'utf8'));
    return data.address;
  } catch {
    return null;
  }
}

/**
 * Load wallet and create clients
 */
export function getClients() {
  if (!walletExists()) {
    throw new Error('No wallet found. Run setup first: node scripts/setup.js');
  }
  
  const data = JSON.parse(readFileSync(WALLET_PATH, 'utf8'));
  const account = privateKeyToAccount(data.privateKey);
  
  const publicClient = createPublicClient({
    chain: hyperEvm,
    transport: http(CHAIN.rpc)
  });
  
  const walletClient = createWalletClient({
    account,
    chain: hyperEvm,
    transport: http(CHAIN.rpc)
  });
  
  return {
    public: publicClient,
    wallet: walletClient,
    account,
    address: account.address
  };
}

/**
 * Create a new wallet
 */
export function createWallet() {
  const { generatePrivateKey, privateKeyToAccount } = require('viem/accounts');
  const privateKey = generatePrivateKey();
  const account = privateKeyToAccount(privateKey);
  
  const walletData = {
    address: account.address,
    privateKey: privateKey,
    createdAt: new Date().toISOString()
  };
  
  writeFileSync(WALLET_PATH, JSON.stringify(walletData, null, 2));
  chmodSync(WALLET_PATH, 0o600);
  
  return { address: account.address };
}

/**
 * Get public client only (no wallet needed)
 */
export function getPublicClient() {
  return createPublicClient({
    chain: hyperEvm,
    transport: http(CHAIN.rpc)
  });
}
