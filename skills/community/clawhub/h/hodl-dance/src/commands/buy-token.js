#!/usr/bin/env node
/**
 * Buy tokens on HODL.DANCE Bonding Curve.
 *
 * Usage:
 *   buy-token <bondingCurveAddress> <bnbAmount> [--recipient=0x...]
 *
 * Arguments:
 *   bondingCurveAddress  Bonding Curve contract address — bonding_curve_address field from get-token/get-tokens
 *   bnbAmount            Amount of BNB to spend, e.g. 0.1
 *   --recipient          Optional: buy tokens for another address (uses buyTokensFor)
 *
 * Requires: HODL_PRIVATE_KEY env variable
 */
const { ethers }                           = require('ethers');
const { getWallet, getCurve, simulateBuy } = require('../lib/chain');
const { ok, err }                          = require('../lib/output');
const { requireValidAddress }              = require('../lib/validators');

const args         = process.argv.slice(2);
const curveAddress = args[0];
const bnbAmount    = args[1];
const flags        = Object.fromEntries(
  args.slice(2).filter(a => a.startsWith('--'))
    .map(a => { const [k, v] = a.slice(2).split('='); return [k, v ?? 'true']; })
);

if (!curveAddress || !bnbAmount) {
  err('Usage: buy-token <bondingCurveAddress> <bnbAmount> [--recipient=0x...]', 'MISSING_ARG');
}

requireValidAddress(curveAddress, 'bondingCurveAddress');

const recipient = flags.recipient || null;

(async () => {
  const wallet = getWallet();
  const curve  = getCurve(curveAddress, wallet);

  const finalized = await curve.finalized();
  if (finalized) err('Token migrated to PancakeSwap V3 — bonding curve trading is closed', 'TOKEN_FINALIZED');

  const { tokensOut, fee } = await simulateBuy(curveAddress, bnbAmount);
  const tokensEstimated    = ethers.formatUnits(tokensOut, 18);

  const value = ethers.parseEther(String(bnbAmount));
  let tx;
  if (recipient) {
    tx = await curve.buyTokensFor(recipient, { value, gasLimit: 300_000 });
  } else {
    tx = await curve.buyTokens({ value, gasLimit: 300_000 });
  }
  const receipt = await tx.wait();

  let actualBnbIn = null, actualTokensOut = null;
  for (const log of receipt.logs) {
    try {
      const parsed = curve.interface.parseLog(log);
      if (parsed?.name === 'TokensPurchased') {
        actualBnbIn     = ethers.formatEther(parsed.args.bnbIn);
        actualTokensOut = ethers.formatUnits(parsed.args.tokensOut, 18);
        break;
      }
    } catch {}
  }

  ok({
    status:           'confirmed',
    tx_hash:          receipt.hash,
    block_number:     receipt.blockNumber,
    bnb_spent:        actualBnbIn     ?? bnbAmount,
    tokens_received:  actualTokensOut ?? tokensEstimated,
    tokens_estimated: tokensEstimated,
    fee_bnb:          ethers.formatEther(fee),
    recipient:        recipient ?? wallet.address,
    bonding_curve:    curveAddress,
    gas_used:         receipt.gasUsed.toString(),
  });
})().catch(e => err(e.message));