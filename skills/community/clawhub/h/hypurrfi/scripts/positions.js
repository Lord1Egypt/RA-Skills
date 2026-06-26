#!/usr/bin/env node

/**
 * Check HypurrFi positions across all markets
 * Usage: node scripts/positions.js [--json]
 */

import { formatUnits, parseAbi } from 'viem';
import { getClients, walletExists, getAddress } from '../lib/wallet.js';
import { CHAIN, MARKETS, TOKENS, ERC20_ABI, AAVE_POOL_ABI, DATA_PROVIDER_ABI } from '../lib/config.js';

const jsonFlag = process.argv.includes('--json');

function output(data) {
  if (jsonFlag) {
    console.log(JSON.stringify(data, null, 2));
  } else {
    if (data.error) {
      console.error('❌', data.error);
      return;
    }
    
    console.log('📊 HypurrFi Positions');
    console.log('');
    console.log('Address:', data.address);
    console.log('');
    
    if (data.pooled) {
      console.log('═══ POOLED MARKET ═══');
      console.log('Total Collateral: $' + data.pooled.totalCollateralUSD);
      console.log('Total Debt: $' + data.pooled.totalDebtUSD);
      console.log('Available to Borrow: $' + data.pooled.availableBorrowsUSD);
      console.log('Health Factor:', data.pooled.healthFactor);
      console.log('');
      
      if (data.pooled.supplies?.length > 0) {
        console.log('Supplies:');
        data.pooled.supplies.forEach(s => {
          console.log(`  ${s.symbol}: ${s.balance} (~$${s.valueUSD})`);
        });
      }
      
      if (data.pooled.borrows?.length > 0) {
        console.log('Borrows:');
        data.pooled.borrows.forEach(b => {
          console.log(`  ${b.symbol}: ${b.balance} (~$${b.valueUSD})`);
        });
      }
    }
    
    console.log('');
    console.log('Explorer:', `${CHAIN.explorer}/address/${data.address}`);
  }
}

async function main() {
  try {
    if (!walletExists()) {
      output({ error: 'No wallet found. Run: node scripts/setup.js' });
      process.exit(1);
    }
    
    const { public: publicClient, address } = getClients();
    const poolAbi = parseAbi(AAVE_POOL_ABI);
    const dataProviderAbi = parseAbi(DATA_PROVIDER_ABI);
    const erc20Abi = parseAbi(ERC20_ABI);
    
    // Get Pooled market data
    const pooled = MARKETS.pooled;
    
    const accountData = await publicClient.readContract({
      address: pooled.pool,
      abi: poolAbi,
      functionName: 'getUserAccountData',
      args: [address]
    });
    
    const [totalCollateralBase, totalDebtBase, availableBorrowsBase, currentLiquidationThreshold, ltv, healthFactor] = accountData;
    
    // Health factor is in wei (1e18 = 1.0)
    const healthFactorNum = Number(formatUnits(healthFactor, 18));
    const healthDisplay = healthFactorNum > 1000 ? '∞ (no debt)' : healthFactorNum.toFixed(2);
    
    // Collateral/debt are in USD with 8 decimals
    const totalCollateralUSD = Number(formatUnits(totalCollateralBase, 8)).toFixed(2);
    const totalDebtUSD = Number(formatUnits(totalDebtBase, 8)).toFixed(2);
    const availableBorrowsUSD = Number(formatUnits(availableBorrowsBase, 8)).toFixed(2);
    
    // Get individual token positions
    const supplies = [];
    const borrows = [];
    
    for (const [key, token] of Object.entries(TOKENS)) {
      if (!token.markets?.includes('pooled')) continue;
      if (key === 'hype') continue; // Skip native for now, handled separately
      
      try {
        const userData = await publicClient.readContract({
          address: pooled.dataProvider,
          abi: dataProviderAbi,
          functionName: 'getUserReserveData',
          args: [token.address, address]
        });
        
        const [aTokenBalance, , currentVariableDebt] = userData;
        
        if (aTokenBalance > 0n) {
          supplies.push({
            symbol: token.symbol,
            balance: formatUnits(aTokenBalance, token.decimals),
            valueUSD: '—' // Would need oracle for accurate USD
          });
        }
        
        if (currentVariableDebt > 0n) {
          borrows.push({
            symbol: token.symbol,
            balance: formatUnits(currentVariableDebt, token.decimals),
            valueUSD: '—'
          });
        }
      } catch (e) {
        // Token might not be in this market
      }
    }
    
    output({
      address,
      pooled: {
        totalCollateralUSD,
        totalDebtUSD,
        availableBorrowsUSD,
        healthFactor: healthDisplay,
        ltv: Number(ltv) / 100 + '%',
        supplies,
        borrows
      }
    });
    
  } catch (error) {
    output({ error: error.message });
    process.exit(1);
  }
}

main();
