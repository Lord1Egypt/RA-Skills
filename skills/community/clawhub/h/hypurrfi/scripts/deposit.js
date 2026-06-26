#!/usr/bin/env node

/**
 * Deposit to HypurrFi markets
 * Usage: node scripts/deposit.js <market> <token> <amount> [--yes] [--json]
 * 
 * Markets: pooled, prime, yield, vault
 * Tokens: hype, usdt0, usdc, usdxl
 * 
 * Examples:
 *   node scripts/deposit.js pooled usdt0 100 --json
 *   node scripts/deposit.js prime hype 10 --yes --json
 */

import { formatUnits, parseUnits, parseAbi, encodeFunctionData } from 'viem';
import { getClients, walletExists } from '../lib/wallet.js';
import { CHAIN, MARKETS, TOKENS, ERC20_ABI, AAVE_POOL_ABI, WRAPPED_HYPE_GATEWAY_ABI, EULER_VAULT_ABI } from '../lib/config.js';

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
      console.log('✅ Deposit successful!');
      console.log('');
      console.log('Market:', data.market);
      console.log('Asset:', data.asset);
      console.log('Amount:', data.amount);
      console.log('TX:', `${CHAIN.explorer}/tx/${data.txHash}`);
    } else if (data.preview) {
      console.log('📋 Deposit Preview');
      console.log('');
      console.log('Market:', data.market);
      console.log('Asset:', data.token, `(${data.tokenAddress || 'native'})`);
      console.log('Amount:', data.amount);
      console.log('Your Balance:', data.balance);
      console.log('');
      console.log('Run with --yes to execute.');
    }
  }
}

function showUsage() {
  console.log('Usage: node scripts/deposit.js <market> <token> <amount> [--yes] [--json]');
  console.log('');
  console.log('Markets: pooled, prime, yield, vault');
  console.log('Tokens: hype, usdt0, usdc, usdxl');
  console.log('');
  console.log('Examples:');
  console.log('  node scripts/deposit.js pooled usdt0 100 --json');
  console.log('  node scripts/deposit.js prime hype 10 --yes --json');
  process.exit(1);
}

async function main() {
  try {
    if (!marketKey || !tokenKey || !amountStr) {
      showUsage();
    }
    
    if (!walletExists()) {
      output({ error: 'No wallet found. Run: node scripts/setup.js' });
      process.exit(1);
    }
    
    const market = MARKETS[marketKey];
    if (!market) {
      output({ error: `Unknown market: ${marketKey}. Options: ${Object.keys(MARKETS).join(', ')}` });
      process.exit(1);
    }
    
    const token = TOKENS[tokenKey];
    if (!token) {
      output({ error: `Unknown token: ${tokenKey}. Options: ${Object.keys(TOKENS).join(', ')}` });
      process.exit(1);
    }
    
    if (!token.markets.includes(marketKey)) {
      output({ error: `${token.symbol} not supported in ${market.name}. Supported markets: ${token.markets.join(', ')}` });
      process.exit(1);
    }
    
    const { public: publicClient, wallet: walletClient, account } = getClients();
    const amount = parseUnits(amountStr, token.decimals);
    const erc20Abi = parseAbi(ERC20_ABI);
    
    // Check balance
    let currentBalance;
    if (tokenKey === 'hype') {
      currentBalance = await publicClient.getBalance({ address: account.address });
    } else {
      currentBalance = await publicClient.readContract({
        address: token.address,
        abi: erc20Abi,
        functionName: 'balanceOf',
        args: [account.address]
      });
    }
    
    const balanceFormatted = formatUnits(currentBalance, token.decimals);
    
    if (currentBalance < amount) {
      output({ 
        error: `Insufficient balance. Have: ${balanceFormatted} ${token.symbol}, Need: ${amountStr}` 
      });
      process.exit(1);
    }
    
    // Preview mode (no --yes)
    if (!yesFlag) {
      output({
        preview: true,
        market: market.name,
        token: token.symbol,
        tokenAddress: token.address,
        amount: amountStr,
        balance: `${balanceFormatted} ${token.symbol}`
      });
      return;
    }
    
    // Execute deposit based on market type
    let txHash;
    
    if (market.type === 'aave') {
      // Pooled market (Aave v3 style)
      txHash = await depositAave(publicClient, walletClient, account, market, token, amount);
    } else if (market.type === 'euler') {
      // Prime/Yield markets (Euler style)
      txHash = await depositEuler(publicClient, walletClient, account, market, token, amount);
    } else if (market.type === 'curated') {
      // Vault market
      txHash = await depositVault(publicClient, walletClient, account, market, token, amount);
    }
    
    // Wait for confirmation
    const receipt = await publicClient.waitForTransactionReceipt({ hash: txHash });
    
    if (receipt.status !== 'success') {
      output({ error: 'Transaction failed', txHash });
      process.exit(1);
    }
    
    output({
      success: true,
      market: market.name,
      asset: token.symbol,
      amount: amountStr,
      txHash,
      explorer: `${CHAIN.explorer}/tx/${txHash}`
    });
    
  } catch (error) {
    output({ error: error.message });
    process.exit(1);
  }
}

async function depositAave(publicClient, walletClient, account, market, token, amount) {
  const poolAbi = parseAbi(AAVE_POOL_ABI);
  const gatewayAbi = parseAbi(WRAPPED_HYPE_GATEWAY_ABI);
  const erc20Abi = parseAbi(ERC20_ABI);
  
  if (token.symbol === 'HYPE') {
    // Native HYPE - use gateway
    return await walletClient.sendTransaction({
      to: market.wrappedHypeGateway,
      data: encodeFunctionData({
        abi: gatewayAbi,
        functionName: 'depositETH',
        args: [market.pool, account.address, 0]
      }),
      value: amount,
      chain: { id: CHAIN.id, name: CHAIN.name }
    });
  } else {
    // ERC20 - approve + supply
    const allowance = await publicClient.readContract({
      address: token.address,
      abi: erc20Abi,
      functionName: 'allowance',
      args: [account.address, market.pool]
    });
    
    if (allowance < amount) {
      const approveTx = await walletClient.sendTransaction({
        to: token.address,
        data: encodeFunctionData({
          abi: erc20Abi,
          functionName: 'approve',
          args: [market.pool, amount]
        }),
        chain: { id: CHAIN.id, name: CHAIN.name }
      });
      await publicClient.waitForTransactionReceipt({ hash: approveTx });
    }
    
    return await walletClient.sendTransaction({
      to: market.pool,
      data: encodeFunctionData({
        abi: poolAbi,
        functionName: 'supply',
        args: [token.address, amount, account.address, 0]
      }),
      chain: { id: CHAIN.id, name: CHAIN.name }
    });
  }
}

async function depositEuler(publicClient, walletClient, account, market, token, amount) {
  // TODO: Implement Euler vault deposit when addresses are available
  throw new Error(`${market.name} market coming soon. Use 'pooled' for now.`);
}

async function depositVault(publicClient, walletClient, account, market, token, amount) {
  // TODO: Implement Vault deposit when addresses are available
  throw new Error(`${market.name} market coming soon. Use 'pooled' for now.`);
}

main();
