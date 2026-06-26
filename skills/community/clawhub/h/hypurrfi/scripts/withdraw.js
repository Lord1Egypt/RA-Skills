#!/usr/bin/env node

/**
 * Withdraw from HypurrFi markets
 * Usage: node scripts/withdraw.js <market> <token> <amount|max> [--yes] [--json]
 */

import { formatUnits, parseUnits, parseAbi, encodeFunctionData, maxUint256 } from 'viem';
import { getClients, walletExists } from '../lib/wallet.js';
import { CHAIN, MARKETS, TOKENS, ERC20_ABI, AAVE_POOL_ABI, WRAPPED_HYPE_GATEWAY_ABI, DATA_PROVIDER_ABI } from '../lib/config.js';

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
      console.log('✅ Withdrawal successful!');
      console.log('');
      console.log('Market:', data.market);
      console.log('Asset:', data.asset);
      console.log('Amount:', data.amount);
      console.log('TX:', `${CHAIN.explorer}/tx/${data.txHash}`);
    } else if (data.preview) {
      console.log('📋 Withdraw Preview');
      console.log('');
      console.log('Market:', data.market);
      console.log('Asset:', data.token);
      console.log('Deposited:', data.deposited);
      console.log('Withdrawing:', data.amount);
      console.log('');
      console.log('Run with --yes to execute.');
    }
  }
}

function showUsage() {
  console.log('Usage: node scripts/withdraw.js <market> <token> <amount|max> [--yes] [--json]');
  console.log('');
  console.log('Examples:');
  console.log('  node scripts/withdraw.js pooled usdt0 50 --json');
  console.log('  node scripts/withdraw.js pooled usdt0 max --yes --json');
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
      output({ error: `${market.name} market coming soon. Use 'pooled' for now.` });
      process.exit(1);
    }
    
    const { public: publicClient, wallet: walletClient, account } = getClients();
    const poolAbi = parseAbi(AAVE_POOL_ABI);
    const dataProviderAbi = parseAbi(DATA_PROVIDER_ABI);
    const erc20Abi = parseAbi(ERC20_ABI);
    const gatewayAbi = parseAbi(WRAPPED_HYPE_GATEWAY_ABI);
    
    // Get current deposit balance
    let depositedBalance;
    
    if (tokenKey === 'hype') {
      // Check WHYPE aToken balance
      // TODO: Get proper WHYPE aToken address
      output({ error: 'HYPE withdrawal coming soon' });
      process.exit(1);
    } else {
      const userData = await publicClient.readContract({
        address: market.dataProvider,
        abi: dataProviderAbi,
        functionName: 'getUserReserveData',
        args: [token.address, account.address]
      });
      depositedBalance = userData[0]; // currentATokenBalance
    }
    
    const depositedFormatted = formatUnits(depositedBalance, token.decimals);
    
    // Determine withdrawal amount
    let withdrawAmount;
    if (amountStr.toLowerCase() === 'max') {
      withdrawAmount = depositedBalance;
    } else {
      withdrawAmount = parseUnits(amountStr, token.decimals);
    }
    
    if (withdrawAmount > depositedBalance) {
      output({ error: `Cannot withdraw ${amountStr}. Only ${depositedFormatted} ${token.symbol} deposited.` });
      process.exit(1);
    }
    
    const withdrawFormatted = formatUnits(withdrawAmount, token.decimals);
    
    // Preview mode
    if (!yesFlag) {
      output({
        preview: true,
        market: market.name,
        token: token.symbol,
        deposited: `${depositedFormatted} ${token.symbol}`,
        amount: `${withdrawFormatted} ${token.symbol}`
      });
      return;
    }
    
    // Execute withdrawal
    const txHash = await walletClient.sendTransaction({
      to: market.pool,
      data: encodeFunctionData({
        abi: poolAbi,
        functionName: 'withdraw',
        args: [token.address, withdrawAmount, account.address]
      }),
      chain: { id: CHAIN.id, name: CHAIN.name }
    });
    
    const receipt = await publicClient.waitForTransactionReceipt({ hash: txHash });
    
    if (receipt.status !== 'success') {
      output({ error: 'Transaction failed', txHash });
      process.exit(1);
    }
    
    output({
      success: true,
      market: market.name,
      asset: token.symbol,
      amount: withdrawFormatted,
      txHash,
      explorer: `${CHAIN.explorer}/tx/${txHash}`
    });
    
  } catch (error) {
    output({ error: error.message });
    process.exit(1);
  }
}

main();
