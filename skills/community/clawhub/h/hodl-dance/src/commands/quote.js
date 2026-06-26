#!/usr/bin/env node
/**
 * Simulate buy/sell output without sending a transaction.
 *
 * Usage:
 *   quote <bondingCurveAddress> buy  <bnbAmount>     — how many tokens for X BNB
 *   quote <bondingCurveAddress> sell <tokenAmount>   — how much BNB for X tokens
 *
 * bondingCurveAddress = bonding_curve_address field from get-token or get-tokens
 */
const { ethers }                    = require('ethers');
const { simulateBuy, simulateSell } = require('../lib/chain');
const { ok, err }                   = require('../lib/output');
const { requireValidAddress }       = require('../lib/validators');

const [,, curveAddress, side, amount] = process.argv;
if (!curveAddress || !side || !amount) {
  err('Usage: quote <bondingCurveAddress> buy|sell <amount>', 'MISSING_ARG');
}

requireValidAddress(curveAddress, 'bondingCurveAddress');
if (!['buy', 'sell'].includes(side)) err('side must be: buy | sell', 'INVALID_ARG');

(async () => {
  if (side === 'buy') {
    const { tokensOut, fee, bnbNet } = await simulateBuy(curveAddress, amount);
    ok({
      side:         'buy',
      bnb_in:       amount,
      bnb_fee:      ethers.formatEther(fee),
      bnb_to_curve: ethers.formatEther(bnbNet),
      tokens_out:   ethers.formatUnits(tokensOut, 18),
      note:         '1% fee deducted from BNB input before price calculation',
    });
  } else {
    const { bnbOut, fee } = await simulateSell(curveAddress, amount);
    ok({
      side:      'sell',
      tokens_in: amount,
      bnb_gross: ethers.formatEther(bnbOut + fee),
      bnb_fee:   ethers.formatEther(fee),
      bnb_out:   ethers.formatEther(bnbOut),
      note:      '1% fee deducted from BNB output',
    });
  }
})().catch(e => err(e.message));