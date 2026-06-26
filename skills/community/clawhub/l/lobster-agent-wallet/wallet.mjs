#!/usr/bin/env node

/**
 * Agent Wallet — CLI
 * 
 * Commands:
 *   balance   — Check USDC + ETH balance (read-only, zero deps)
 *   status    — Show wallet configuration (no secrets)
 *   pay       — Pay x402 resource (requires viem + --confirm)
 * 
 * SECURITY:
 *   - Address from WALLET_ADDRESS env var for read-only queries
 *   - Private key from WALLET_PRIVATE_KEY env var for signed operations
 *   - Private key NEVER logged, serialized, or exposed
 *   - Payments require --confirm flag for explicit authorization
 */

import { getWallet, getBalances, getStatus } from './lib/core.mjs';

// ─── Helpers ─────────────────────────────────────────────────────────

function printBanner() {
  console.log('\n  🦞 Agent Wallet — USDC Wallet for AI Agents on Base\n');
}

async function cmdBalance(wallet) {
  const b = await getBalances(wallet);
  console.log('Address:  ' + b.address);
  console.log('Network:  ' + b.network);
  console.log('ETH:      ' + b.eth);
  console.log('USDC:     ' + b.usdc + ' ' + b.usdcSymbol);
  console.log('Explorer: ' + wallet.net.explorer + '/address/' + b.address + '\n');
}

async function cmdStatus(wallet) {
  const s = getStatus(wallet);
  const pk = process.env.WALLET_PRIVATE_KEY;
  console.log('Address:    ' + s.address);
  console.log('Network:    ' + s.network);
  console.log('Chain ID:   ' + s.chainId);
  console.log('USDC Addr:  ' + s.usdcAddress);
  console.log('Payments:   ' + (pk ? '✅ x402 ready' : '⏸️  read-only (no private key)'));
  console.log('Explorer:   ' + s.explorer + '\n');
}

async function cmdPay(url) {
  const pk = process.env.WALLET_PRIVATE_KEY;
  if (!pk) {
    throw new Error(
      'x402 payments require WALLET_PRIVATE_KEY.\n' +
      'Set it in .env or as an environment variable.'
    );
  }

  const confirm = process.argv.includes('--confirm');
  if (!confirm) {
    throw new Error(
      'SECURITY: Payment requires --confirm flag.\n' +
      'This will sign a USDC transfer authorization.\n' +
      'Re-run: node wallet.mjs pay "' + url + '" --confirm'
    );
  }

  const wallet = await getWallet();
  const balances = await getBalances(wallet);

  // Show payment preview
  console.log('\n=== x402 Payment Request ===');
  console.log('From:     ' + wallet.address);
  console.log('Network:  ' + wallet.net.name);
  console.log('Balance:  ' + balances.usdc + ' USDC');
  console.log('Target:   ' + url);

  // Do the payment
  console.log('\n⏳ Signing EIP-3009 authorization...');
  const { payX402 } = await import('./lib/x402-client.mjs');
  const result = await payX402(url, pk, { confirm: true });

  if (result.paid) {
    console.log('✅ Payment sent. Server: ' + result.status + '\n');
  } else {
    console.log('ℹ️  No payment needed. Server: ' + result.status + '\n');
  }
}

// ─── Main ────────────────────────────────────────────────────────────

async function main() {
  const cmd = process.argv[2] || 'status';
  printBanner();

  try {
    switch (cmd) {
      case 'balance': {
        const w = await getWallet();
        await cmdBalance(w);
        break;
      }

      case 'status': {
        const w = await getWallet();
        await cmdStatus(w);
        break;
      }

      case 'pay': {
        const url = process.argv[3];
        if (!url) throw new Error('Usage: node wallet.mjs pay <url> [--confirm]');
        await cmdPay(url);
        break;
      }

      default:
        throw new Error('Usage: node wallet.mjs [balance|status|pay]');
    }
  } catch (e) {
    console.error('\n❌ ' + e.message + '\n');
    process.exit(1);
  }
}

main();
