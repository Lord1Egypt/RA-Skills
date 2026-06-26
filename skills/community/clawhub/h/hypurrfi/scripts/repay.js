#!/usr/bin/env node

/**
 * Repay debt on HypurrFi markets
 * Usage: node scripts/repay.js <market> <token> <amount|max> [--yes] [--json]
 * 
 * Examples:
 *   node scripts/repay.js pooled usdt0 500 --json
 *   node scripts/repay.js pooled usdt0 max --yes --json
 */

import { formatUnits, parseUnits, parseAbi, encodeFunctionData, maxUint256 } from 'viem';
import { getClients, walletExists } from '../lib/wallet.js';
import { CHAIN, MARKETS, TOKENS, ERC20_ABI, AAVE_POOL_ABI, DATA_PROVIDER_ABI, WRAPPED_HYPE_GATEWAY_ABI } from '../lib/config.js';

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
      console.log('✅ Repayment successful!');
      console.log('');
      console.log('Market:', data.market);
      console.log('Asset:', data.asset);
      console.log('Amount Repaid:', data.amount);
      console.log('Remaining Debt:', data.remainingDebt);
      console.log('TX:', `${CHAIN.explorer}/tx/${data.txHash}`);
    } else if (data.preview) {
      console.log('📋 Repay Preview');
      console.log('');
      console.log('Market:', data.market);
      console.log('Asset:', data.token);
      console.log('Current Debt:', data.currentDebt);
      console.log('Repay Amount:', data.amount);
      console.log('Your Balance:', data.balance);
      console.log('');
      console.log('Run with --yes to execute.');
    }
  }
}

async function main() {
  try {
    if (!marketKey || !tokenKey || !amountStr) {
      console.log('Usage: node scripts/repay.js <market> <token> <amount|max> [--yes] [--json]');
      process.exit(1);
    }
    
    if (!walletExists()) {
      output({ error: 'No wallet found. Run: node scripts/setup.js' });
      process.exit(1);
    }
    
    const market = MARKETS[marketKey];
    const token = TOKENS[tokenKey];
    
    if (!market || market.type !== 'aave') {
      output({ error: 'Repay only supported in Pooled market currently' });
      process.exit(1);
    }
    
    if (!token) {
      output({ error: `Unknown token: ${tokenKey}` });
      process.exit(1);
    }
    
    const { public: publicClient, wallet: walletClient, account } = getClients();
    const erc20Abi = parseAbi(ERC20_ABI);
    const poolAbi = parseAbi(AAVE_POOL_ABI);
    const dataProviderAbi = parseAbi(DATA_PROVIDER_ABI);
    
    // Get current debt
    let currentDebt = 0n;
    if (tokenKey !== 'hype' && token.address) {
      const userData = await publicClient.readContract({
        address: market.dataProvider,
        abi: dataProviderAbi,
        functionName: 'getUserReserveData',
        args: [token.address, account.address]
      });
      currentDebt = userData[2]; // currentVariableDebt
    }
    
    const debtFormatted = formatUnits(currentDebt, token.decimals);
    
    // Get wallet balance
    let balance;
    if (tokenKey === 'hype') {
      balance = await publicClient.getBalance({ address: account.address });
    } else {
      balance = await publicClient.readContract({
        address: token.address,
        abi: erc20Abi,
        functionName: 'balanceOf',
        args: [account.address]
      });
    }
    
    const balanceFormatted = formatUnits(balance, token.decimals);
    
    // Determine repay amount
    const isMax = amountStr.toLowerCase() === 'max';
    let amount = isMax ? currentDebt : parseUnits(amountStr, token.decimals);
    let amountDisplay = isMax ? debtFormatted : amountStr;
    
    if (currentDebt === 0n) {
      output({ error: `No ${token.symbol} debt to repay` });
      process.exit(1);
    }
    
    // Preview mode
    if (!yesFlag) {
      output({
        preview: true,
        market: market.name,
        token: token.symbol,
        currentDebt: debtFormatted,
        amount: amountDisplay,
        balance: balanceFormatted
      });
      return;
    }
    
    // Execute repay
    let txHash;
    
    if (tokenKey === 'hype') {
      // Repay native HYPE via gateway
      const gatewayAbi = parseAbi(WRAPPED_HYPE_GATEWAY_ABI);
      txHash = await walletClient.sendTransaction({
        to: market.wrappedHypeGateway,
        data: encodeFunctionData({
          abi: gatewayAbi,
          functionName: 'repayETH',
          args: [market.pool, isMax ? maxUint256 : amount, 2, account.address]
        }),
        value: amount,
        chain: { id: CHAIN.id, name: CHAIN.name }
      });
    } else {
      // Approve if needed
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
            args: [market.pool, maxUint256]
          }),
          chain: { id: CHAIN.id, name: CHAIN.name }
        });
        await publicClient.waitForTransactionReceipt({ hash: approveTx });
      }
      
      // Repay
      txHash = await walletClient.sendTransaction({
        to: market.pool,
        data: encodeFunctionData({
          abi: poolAbi,
          functionName: 'repay',
          args: [token.address, isMax ? maxUint256 : amount, 2, account.address]
        }),
        chain: { id: CHAIN.id, name: CHAIN.name }
      });
    }
    
    const receipt = await publicClient.waitForTransactionReceipt({ hash: txHash });
    
    if (receipt.status !== 'success') {
      output({ error: 'Transaction failed', txHash });
      process.exit(1);
    }
    
    // Get remaining debt
    let remainingDebt = '0';
    if (tokenKey !== 'hype' && token.address) {
      const newUserData = await publicClient.readContract({
        address: market.dataProvider,
        abi: dataProviderAbi,
        functionName: 'getUserReserveData',
        args: [token.address, account.address]
      });
      remainingDebt = formatUnits(newUserData[2], token.decimals);
    }
    
    output({
      success: true,
      market: market.name,
      asset: token.symbol,
      amount: amountDisplay,
      remainingDebt,
      txHash,
      explorer: `${CHAIN.explorer}/tx/${txHash}`
    });
    
  } catch (error) {
    output({ error: error.message });
    process.exit(1);
  }
}

main();
