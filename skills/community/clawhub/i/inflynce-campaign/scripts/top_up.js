#!/usr/bin/env node
/**
 * Top up spending limit for Inflynce Boost campaigns.
 * Sends ERC-20 approve tx: USDC.approve(BOOSTS_CONTRACT, amount) on Base.
 * Agent needs the wallet private key to sign.
 *
 * Usage:
 *   PRIVATE_KEY=0x... node top_up.js --amount 50
 *   node top_up.js --private-key 0x... --amount 50
 */

import { createWalletClient, http, parseUnits } from 'viem';
import { privateKeyToAccount } from 'viem/accounts';
import { base } from 'viem/chains';

const USDC_BASE = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913';
const BOOSTS_CONTRACT = '0x6e6A6128bB0c175989066eb0e2bf54F06688207b';
const ERC20_ABI = [
  { inputs: [{ name: 'spender', type: 'address' }, { name: 'amount', type: 'uint256' }], name: 'approve', outputs: [{ name: '', type: 'bool' }], stateMutability: 'nonpayable', type: 'function' },
];

function parseArgs() {
  const args = process.argv.slice(2);
  const out = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--') && args[i + 1]) {
      const key = args[i].slice(2).replace(/-/g, '_');
      out[key] = args[++i];
    }
  }
  return out;
}

async function topUp() {
  const params = parseArgs();
  const privateKey = params.private_key || process.env.PRIVATE_KEY;
  const amountStr = params.amount || '50';

  if (!privateKey) {
    throw new Error('Private key required: set PRIVATE_KEY env or pass --private-key');
  }

  const amount = parseFloat(amountStr);
  if (isNaN(amount) || amount < 5) {
    throw new Error('Amount must be at least 5 USDC');
  }

  const account = privateKeyToAccount(privateKey.startsWith('0x') ? privateKey : `0x${privateKey}`);
  const client = createWalletClient({
    account,
    chain: base,
    transport: http(),
  });

  const hash = await client.writeContract({
    address: USDC_BASE,
    abi: ERC20_ABI,
    functionName: 'approve',
    args: [BOOSTS_CONTRACT, parseUnits(amount.toFixed(6), 6)],
  });

  console.log(JSON.stringify({ txHash: hash, amount, chain: 'base' }));
}

topUp().catch((e) => {
  console.error(e.message);
  process.exit(1);
});
