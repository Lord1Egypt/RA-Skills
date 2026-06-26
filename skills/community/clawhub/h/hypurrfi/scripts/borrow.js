#!/usr/bin/env node

/**
 * Borrow from HypurrFi markets
 * Usage: node scripts/borrow.js <market> <token> <amount> [--yes] [--json]
 * 
 * Examples:
 *   node scripts/borrow.js pooled usdt0 1000 --json
 */

import { formatUnits, parseUnits, parseAbi, encodeFunctionData } from 'viem';
import { getClients, walletExists } from '../lib/wallet.js';
import { CHAIN, MARKETS, TOKENS, AAVE_POOL_ABI, WRAPPED_HYPE_GATEWAY_ABI } from '../lib/config.js';

const args = process.argv.slice(2);
const jsonFlag = args.includes('--json');
const yesFlag = args.includes('--yes');

const positionalArgs = args.filter(a => !a.startsWith('--'));
const marketKey = positionalArgs[0]?.toLowerCase();
const tokenKey = positionalArgs[1]?.toLowerCase();
const amountStr = positionalArgs[2];

function output(data) {
  if (jsonFlag) {
    console.log(JSON.stringify(data, null, 2));
  } else {
    if (data.error) {
      console.error('❌', data.error);
    } else if (data.success) {
      console.log('✅ Borrow successful!');
      console.log('');
      console.log('Market:', data.market);
      console.log('Asset:', data.asset);
      console.log('Amount:', data.amount);
      console.log('New Health Factor:', data.healthFactor);
      console.log('TX:', `${CHAIN.explorer}/tx/${data.txHash}`);
    } else if (data.preview) {
      console.log('📋 Borrow Preview');
      console.log('');
      console.log('Market:', data.market);
      console.log('Asset:', data.token);
      console.log('Amount:', data.amount);
      console.log('Current Health:', data.currentHealth);
      console.log('Available to Borrow: $' + data.availableBorrows);
      console.log('');
      if (data.warning) console.log('⚠️ ', data.warning);
      console.log('Run with --yes to execute.');
    }
  }
}

async function main() {
  try {
    if (!marketKey || !tokenKey || !amountStr) {
      console.log('Usage: node scripts/borrow.js <market> <token> <amount> [--yes] [--json]');
      process.exit(1);
    }
    
    if (!walletExists()) {
      output({ error: 'No wallet found. Run: node scripts/setup.js' });
      process.exit(1);
    }
    
    const market = MARKETS[marketKey];
    const token = TOKENS[tokenKey];
    
    if (!market) {
      output({ error: `Unknown market: ${marketKey}` });
      process.exit(1);
    }
    
    if (!token) {
      output({ error: `Unknown token: ${tokenKey}` });
      process.exit(1);
    }
    
    if (market.type !== 'aave') {
      output({ error: `Borrowing only supported in Pooled market currently` });
      process.exit(1);
    }
    
    const { public: publicClient, wallet: walletClient, account } = getClients();
    const amount = parseUnits(amountStr, token.decimals);
    const poolAbi = parseAbi(AAVE_POOL_ABI);
    
    // Check current health and available borrows
    const accountData = await publicClient.readContract({
      address: market.pool,
      abi: poolAbi,
      functionName: 'getUserAccountData',
      args: [account.address]
    });
    
    const [totalCollateral, totalDebt, availableBorrows, , , healthFactor] = accountData;
    
    const healthNum = Number(formatUnits(healthFactor, 18));
    const healthDisplay = healthNum > 1000 ? '∞' : healthNum.toFixed(2);
    const availableUSD = formatUnits(availableBorrows, 8);
    
    // Preview mode
    if (!yesFlag) {
      let warning = null;
      if (healthNum < 1.5 && healthNum < 1000) {
        warning = 'Health factor is low. Adding debt increases liquidation risk.';
      }
      
      output({
        preview: true,
        market: market.name,
        token: token.symbol,
        amount: amountStr,
        currentHealth: healthDisplay,
        availableBorrows: Number(availableUSD).toFixed(2),
        warning
      });
      return;
    }
    
    // Execute borrow
    let txHash;
    
    if (tokenKey === 'hype') {
      // Borrow native HYPE via gateway
      const gatewayAbi = parseAbi(WRAPPED_HYPE_GATEWAY_ABI);
      txHash = await walletClient.sendTransaction({
        to: market.wrappedHypeGateway,
        data: encodeFunctionData({
          abi: gatewayAbi,
          functionName: 'borrowETH',
          args: [market.pool, amount, 2, 0] // 2 = variable rate
        }),
        chain: { id: CHAIN.id, name: CHAIN.name }
      });
    } else {
      // Borrow ERC20
      txHash = await walletClient.sendTransaction({
        to: market.pool,
        data: encodeFunctionData({
          abi: poolAbi,
          functionName: 'borrow',
          args: [token.address, amount, 2, 0, account.address] // 2 = variable rate
        }),
        chain: { id: CHAIN.id, name: CHAIN.name }
      });
    }
    
    const receipt = await publicClient.waitForTransactionReceipt({ hash: txHash });
    
    if (receipt.status !== 'success') {
      output({ error: 'Transaction failed', txHash });
      process.exit(1);
    }
    
    // Get new health factor
    const newAccountData = await publicClient.readContract({
      address: market.pool,
      abi: poolAbi,
      functionName: 'getUserAccountData',
      args: [account.address]
    });
    
    const newHealth = Number(formatUnits(newAccountData[5], 18)).toFixed(2);
    
    output({
      success: true,
      market: market.name,
      asset: token.symbol,
      amount: amountStr,
      healthFactor: newHealth,
      txHash,
      explorer: `${CHAIN.explorer}/tx/${txHash}`
    });
    
  } catch (error) {
    output({ error: error.message });
    process.exit(1);
  }
}

main();
