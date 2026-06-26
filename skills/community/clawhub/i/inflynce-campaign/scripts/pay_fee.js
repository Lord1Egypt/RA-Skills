#!/usr/bin/env node
/**
 * Pay 0.25 USDC platform fee (required per campaign) to Inflynce on Base.
 * Sends USDC.transfer(INFLYNCE_RECIPIENT, 0.25). Use before create_campaign.js.
 *
 * Usage:
 *   PRIVATE_KEY=0x... node pay_fee.js
 *   node pay_fee.js --private-key 0x...
 */

import { createWalletClient, http, parseUnits } from 'viem';
import { privateKeyToAccount } from 'viem/accounts';
import { base } from 'viem/chains';

const USDC_BASE = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913';
const INFLYNCE_RECIPIENT = '0xA61529732F4E71ef1586252dDC97202Ce198A38A';
const FEE_USDC = 0.25;
const ERC20_ABI = [
  { inputs: [{ name: 'to', type: 'address' }, { name: 'amount', type: 'uint256' }], name: 'transfer', outputs: [{ name: '', type: 'bool' }], stateMutability: 'nonpayable', type: 'function' },
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

async function payFee() {
  const params = parseArgs();
  const privateKey = params.private_key || process.env.PRIVATE_KEY;

  if (!privateKey) {
    throw new Error('Private key required: set PRIVATE_KEY env or pass --private-key');
  }

  const account = privateKeyToAccount(privateKey.startsWith('0x') ? privateKey : `0x${privateKey}`);
  const client = createWalletClient({
    account,
    chain: base,
    transport: http(),
  });

  const amountWei = parseUnits(FEE_USDC.toFixed(6), 6);
  const hash = await client.writeContract({
    address: USDC_BASE,
    abi: ERC20_ABI,
    functionName: 'transfer',
    args: [INFLYNCE_RECIPIENT, amountWei],
  });

  console.log(JSON.stringify({ txHash: hash, amount: FEE_USDC, chain: 'base' }));
}

payFee().catch((e) => {
  console.error(e.message);
  process.exit(1);
});
