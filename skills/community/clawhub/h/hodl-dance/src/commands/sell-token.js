#!/usr/bin/env node
/**
 * Sell tokens on HODL.DANCE Bonding Curve.
 *
 * Usage:
 *   sell-token <bondingCurveAddress> <tokenAmount>
 *
 * Arguments:
 *   bondingCurveAddress  Bonding Curve contract address — bonding_curve_address field from get-token/get-tokens
 *   tokenAmount          Amount of tokens to sell in full tokens (not wei), e.g. 1000000
 *
 * Requires: HODL_PRIVATE_KEY env variable
 *
 * NOTE — selling requires two steps handled automatically by this skill:
 *   Step 1: approve() — grant the Bonding Curve permission to transfer tokens from your wallet
 *   Step 2: sellTokens() — execute the actual sell
 * If allowance is already sufficient, approve is skipped (saves gas).
 */
const { ethers }                                      = require('ethers');
const { getWallet, getCurve, getToken, simulateSell } = require('../lib/chain');
const { ok, err }                                     = require('../lib/output');
const { requireValidAddress }                         = require('../lib/validators');

const [,, curveAddress, tokenAmount] = process.argv;
if (!curveAddress || !tokenAmount) {
  err('Usage: sell-token <bondingCurveAddress> <tokenAmount>', 'MISSING_ARG');
}

requireValidAddress(curveAddress, 'bondingCurveAddress');

(async () => {
  const wallet = getWallet();
  const curve  = getCurve(curveAddress, wallet);

  const finalized = await curve.finalized();
  if (finalized) err('Token migrated to PancakeSwap V3 — bonding curve trading is closed', 'TOKEN_FINALIZED');

  const tokenAddress  = await curve.token();
  const amountWei     = ethers.parseUnits(String(tokenAmount), 18);
  const tokenContract = getToken(tokenAddress, wallet);

  // Check balance before proceeding
  const balance = await tokenContract.balanceOf(wallet.address);
  if (balance < amountWei) {
    err(
      `Insufficient balance. Have: ${ethers.formatUnits(balance, 18)}, need: ${tokenAmount}`,
      'INSUFFICIENT_BALANCE'
    );
  }

  // Simulate output before sending
  const { bnbOut, fee } = await simulateSell(curveAddress, tokenAmount);

  // Step 1: Approve (only if current allowance is insufficient)
  let approveTxHash = null;
  const allowance = await tokenContract.allowance(wallet.address, curveAddress);
  if (allowance < amountWei) {
    const approveTx     = await tokenContract.approve(curveAddress, amountWei, { gasLimit: 100_000 });
    const approveReceipt = await approveTx.wait();
    approveTxHash = approveReceipt.hash;
  }

  // Step 2: Sell
  const tx      = await curve.sellTokens(amountWei, { gasLimit: 300_000 });
  const receipt = await tx.wait();

  let actualTokensIn = null, actualBnbOut = null;
  for (const log of receipt.logs) {
    try {
      const parsed = curve.interface.parseLog(log);
      if (parsed?.name === 'TokensSold') {
        actualTokensIn = ethers.formatUnits(parsed.args.tokensIn, 18);
        actualBnbOut   = ethers.formatEther(parsed.args.bnbOut);
        break;
      }
    } catch {}
  }

  ok({
    status:             'confirmed',
    tx_hash:            receipt.hash,
    block_number:       receipt.blockNumber,
    tokens_sold:        actualTokensIn ?? tokenAmount,
    bnb_received:       actualBnbOut   ?? ethers.formatEther(bnbOut),
    bnb_estimated:      ethers.formatEther(bnbOut),
    fee_bnb:            ethers.formatEther(fee),
    token_address:      tokenAddress,
    bonding_curve:      curveAddress,
    approve_tx_hash:    approveTxHash,
    approve_was_needed: approveTxHash !== null,
    gas_used:           receipt.gasUsed.toString(),
    note: approveTxHash
      ? 'ERC20 approve was sent automatically before sell (2 transactions total)'
      : 'Existing allowance was sufficient — only sell transaction sent (1 transaction)',
  });
})().catch(e => err(e.message));