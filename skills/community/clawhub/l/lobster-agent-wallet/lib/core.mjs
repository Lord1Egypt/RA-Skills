/**
 * Agent Wallet — Core Module
 * 
 * Zero-dependency USDC wallet for AI agents on Base.
 * Uses native fetch for all RPC calls. No npm install needed for Phase 1.
 * 
 * SECURITY: Private key is NEVER logged, stored, or exposed.
 * Phase 1: Read-only balance queries (safe, no signing).
 * Phase 2: x402 payments with explicit confirmation.
 */

import { privateKeyToAddress } from './crypto.mjs';

// ─── Network Configuration ───────────────────────────────────────────

const NETWOR = {
  'base': {
    name: 'Base Mainnet',
    chainId: 8453,
    rpc: 'https://mainnet.base.org',
    usdc: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
    explorer: 'https://basescan.org',
  },
  'base-sepolia': {
    name: 'Base Sepolia (Testnet)',
    chainId: 84532,
    rpc: 'https://sepolia.base.org',
    usdc: '0x036CbD53842c5426634e7929541eC2318f3dCF7e',
    explorer: 'https://sepolia.basescan.org',
  },
};

// ─── JSON-RPC Helper ─────────────────────────────────────────────────

async function rpcCall(rpcUrl, method, params = []) {
  const res = await fetch(rpcUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      jsonrpc: '2.0',
      id: 1,
      method,
      params,
    }),
  });
  const data = await res.json();
  if (data.error) throw new Error(`RPC error: ${data.error.message}`);
  return data.result;
}

// USDC balanceOf encoded calldata: 0x70a08231 + padded address
function balanceOfCalldata(address) {
  const addr = address.replace('0x', '').toLowerCase().padStart(64, '0');
  return '0x70a08231000000000000000000000000' + addr;
}

// ─── Wallet Factory ──────────────────────────────────────────────────

/**
 * Create wallet from environment.
 * Private key loaded into memory — NEVER logged or persisted.
 */
export async function getWallet() {
  const pk = process.env.WALLET_PRIVATE_KEY || '';
  const addr = process.env.WALLET_ADDRESS;

  if (!addr && !pk) {
    throw new Error(
      'Set WALLET_ADDRESS for read-only mode, or WALLET_PRIVATE_KEY for full mode.\n' +
      '  export WALLET_ADDRESS=0x...'
    );
  }

  const netName = process.env.WALLET_NETWORK || 'base-sepolia';
  const net = NETWOR[netName];
  if (!net) throw new Error(`Unknown network: ${netName}`);

  const address = addr ? addr.toLowerCase() : privateKeyToAddress(pk);
  return { address, net, pk };
}

// ─── Balance Queries (Read-Only, Zero Dependencies) ──────────────────

/**
 * Get ETH and USDC balances.
 * Uses native JSON-RPC via fetch. No signing, no gas cost, always safe.
 */
export async function getBalances(wallet) {
  const [ethWei, usdcRaw, usdcName] = await Promise.all([
    rpcCall(wallet.net.rpc, 'eth_getBalance', [wallet.address, 'latest']),
    rpcCall(wallet.net.rpc, 'eth_call', [{
      to: wallet.net.usdc,
      data: balanceOfCalldata(wallet.address),
    }, 'latest']),
    rpcCall(wallet.net.rpc, 'eth_call', [{
      to: wallet.net.usdc,
      data: '0x95d89b41', // symbol()
    }, 'latest']),
  ]);

  return {
    address: wallet.address,
    network: wallet.net.name,
    chainId: wallet.net.chainId,
    eth: (BigInt(ethWei) / 10n ** 18n).toString(),
    usdc: (BigInt(usdcRaw) / 10n ** 6n).toString(),
    usdcSymbol: hexToString(usdcName) || 'USDC',
  };
}

// ─── Status (Safe for Display) ───────────────────────────────────────

export function getStatus(wallet) {
  return {
    configured: true,
    address: wallet.address,
    network: wallet.net.name,
    chainId: wallet.net.chainId,
    usdcAddress: wallet.net.usdc,
    explorer: wallet.net.explorer,
  };
}

// ─── Helper ───────────────────────────────────────────────────────────

function hexToString(hex) {
  const s = hex.replace('0x', '');
  let out = '';
  for (let i = 0; i < s.length; i += 2) {
    const c = parseInt(s.substring(i, i + 2), 16);
    if (c > 0 && c < 128) out += String.fromCharCode(c);
  }
  return out;
}
