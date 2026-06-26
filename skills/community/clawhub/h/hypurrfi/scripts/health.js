#!/usr/bin/env node

/**
 * Check health factor and liquidation risk
 * Usage: node scripts/health.js [--json]
 */

import { formatUnits, parseAbi } from 'viem';
import { getClients, walletExists } from '../lib/wallet.js';
import { MARKETS, AAVE_POOL_ABI } from '../lib/config.js';

const jsonFlag = process.argv.includes('--json');

function output(data) {
  if (jsonFlag) {
    console.log(JSON.stringify(data, null, 2));
  } else {
    if (data.error) {
      console.error('❌', data.error);
      return;
    }
    
    console.log('🏥 Health Check');
    console.log('');
    console.log('Health Factor:', data.healthFactor);
    console.log('Status:', data.status);
    console.log('');
    console.log('Collateral: $' + data.totalCollateralUSD);
    console.log('Debt: $' + data.totalDebtUSD);
    console.log('Can Borrow: $' + data.availableBorrowsUSD);
    
    if (data.warning) {
      console.log('');
      console.log('⚠️ ', data.warning);
    }
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
    const pooled = MARKETS.pooled;
    
    const accountData = await publicClient.readContract({
      address: pooled.pool,
      abi: poolAbi,
      functionName: 'getUserAccountData',
      args: [address]
    });
    
    const [totalCollateralBase, totalDebtBase, availableBorrowsBase, , , healthFactor] = accountData;
    
    const healthFactorNum = Number(formatUnits(healthFactor, 18));
    const totalCollateralUSD = Number(formatUnits(totalCollateralBase, 8)).toFixed(2);
    const totalDebtUSD = Number(formatUnits(totalDebtBase, 8)).toFixed(2);
    const availableBorrowsUSD = Number(formatUnits(availableBorrowsBase, 8)).toFixed(2);
    
    let status, warning;
    
    if (totalDebtBase === 0n) {
      status = '✅ No debt - no liquidation risk';
    } else if (healthFactorNum >= 2) {
      status = '✅ Healthy';
    } else if (healthFactorNum >= 1.5) {
      status = '🟡 Moderate';
      warning = 'Consider adding collateral or repaying some debt';
    } else if (healthFactorNum >= 1.1) {
      status = '🟠 Caution';
      warning = 'Liquidation risk increasing. Add collateral or repay debt soon.';
    } else {
      status = '🔴 DANGER';
      warning = 'HIGH LIQUIDATION RISK! Add collateral or repay debt immediately.';
    }
    
    const healthDisplay = healthFactorNum > 1000 ? '∞' : healthFactorNum.toFixed(2);
    
    output({
      healthFactor: healthDisplay,
      healthFactorRaw: healthFactorNum,
      status,
      totalCollateralUSD,
      totalDebtUSD,
      availableBorrowsUSD,
      warning
    });
    
  } catch (error) {
    output({ error: error.message });
    process.exit(1);
  }
}

main();
