#!/usr/bin/env node
/**
 * Headless pay-signup: POST /signup/pay/quote → pay on-chain → POST /signup/pay/claim.
 * Uses quote.payment_kind: **erc20** = ERC-20 transfer; **native_value** = native/CGT value
 * send to recipient (e.g. POWER on chain 7869). Must match the plan (see GET /credits/plans).
 *
 * Required env (POWERLOOM_* only):
 *   POWERLOOM_EVM_PRIVATE_KEY — hex, optionally 0x-prefixed (funds the transfer)
 *   POWERLOOM_PLAN_ID — plan id from GET /credits/plans
 *   POWERLOOM_EVM_CHAIN_ID — EIP-155 chain id (must match the plan row)
 *   POWERLOOM_TOKEN_SYMBOL — must match plan.token_symbol for that chain
 *
 * Optional:
 *   POWERLOOM_METERING_BASE_URL — default https://bds-metering.powerloom.io
 *   POWERLOOM_EVM_RPC_URL — if unset, uses rpc_hint from the quote
 *   POWERLOOM_AGENT_NAME — default openclaw-pay-agent
 *   POWERLOOM_EMAIL — if set, must not already be registered
 *
 * Confirmation (broadcast protection — avoids silent spend after quote):
 *   Interactive TTY: prints quote summary; you must type CONFIRM before signing.
 *   Non-interactive (OpenClaw / CI): pass --yes OR set POWERLOOM_SIGNUP_PAY_CONFIRM=yes
 *   after manually verifying recipient, amount, chain, token, and plan on stderr output.
 *   --dry-run: fetch quote + print summary only; exits 0 without broadcasting (review step).
 *
 * On success, prints JSON with api_key — set POWERLOOM_API_KEY from the output.
 *
 * Usage:
 *   node scripts/signup-pay.mjs --dry-run
 *   node scripts/signup-pay.mjs
 *   POWERLOOM_SIGNUP_PAY_CONFIRM=yes node scripts/signup-pay.mjs
 *   node scripts/signup-pay.mjs --yes
 */

import { ethers } from "ethers";
import {
  meteringBaseUrl,
  evmPrivateKey,
  evmRpcUrl,
  planId,
  chainIdParsed,
  tokenSymbol,
  agentNameOr,
  signupEmail,
} from "./lib/powerloom-env.mjs";
import { confirmSpendBeforeBroadcast } from "./lib/confirm-spend.mjs";

const ERC20_ABI = ["function transfer(address to, uint256 amount) returns (bool)"];

async function main() {
  const base = meteringBaseUrl();
  const pk = evmPrivateKey();
  const pid = planId();
  const chainId = chainIdParsed();
  const sym = tokenSymbol();
  const agentName = agentNameOr("openclaw-pay-agent");
  const emailRaw = signupEmail();

  if (!pk) {
    console.error("Set POWERLOOM_EVM_PRIVATE_KEY");
    process.exit(1);
  }
  if (!pid || !Number.isFinite(chainId) || !sym) {
    console.error(
      "Set POWERLOOM_PLAN_ID, POWERLOOM_EVM_CHAIN_ID, and POWERLOOM_TOKEN_SYMBOL (see GET /credits/plans).",
    );
    process.exit(1);
  }

  const wallet = new ethers.Wallet(pk.startsWith("0x") ? pk : `0x${pk}`);
  const quoteBody = {
    agent_name: agentName,
    plan_id: pid,
    chain_id: chainId,
    token_symbol: sym,
    payer_address: wallet.address,
  };
  if (emailRaw) {
    quoteBody.email = emailRaw;
  }

  const qr = await fetch(`${base}/signup/pay/quote`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(quoteBody),
  });
  const quoteText = await qr.text();
  let quote;
  try {
    quote = JSON.parse(quoteText);
  } catch {
    console.error("Quote response not JSON:", quoteText.slice(0, 500));
    process.exit(1);
  }
  if (!qr.ok) {
    console.error(JSON.stringify(quote, null, 2));
    process.exit(1);
  }

  const rpcUrl = evmRpcUrl() || quote.rpc_hint;
  if (!rpcUrl) {
    console.error(
      "No RPC: set POWERLOOM_EVM_RPC_URL (quote.rpc_hint is null when metering has no public_rpc_url for that chain).",
    );
    process.exit(1);
  }

  const provider = new ethers.JsonRpcProvider(rpcUrl);
  const net = await provider.getNetwork();
  if (Number(net.chainId) !== Number(quote.chain_id)) {
    console.error(
      `RPC chainId ${net.chainId} does not match quote.chain_id ${quote.chain_id}. Fix POWERLOOM_EVM_RPC_URL.`,
    );
    process.exit(1);
  }

  const signer = wallet.connect(provider);
  const amount = BigInt(quote.amount_atomic);
  const isNative = quote.payment_kind === "native_value";

  const summaryLines = [
    "[signup-pay] Quote summary — verify before broadcasting:",
    `  plan_id       ${pid}`,
    `  chain_id      ${quote.chain_id}`,
    `  token_symbol  ${sym}`,
    `  payment_kind  ${quote.payment_kind}`,
    `  recipient     ${quote.recipient}`,
    `  amount_atomic ${quote.amount_atomic}`,
    `  payer         ${wallet.address}`,
    `  signup_nonce  ${quote.signup_nonce}`,
  ];

  if (process.argv.includes("--dry-run")) {
    for (const line of summaryLines) {
      console.error(line);
    }
    console.error("[signup-pay] --dry-run: no transaction broadcast. Re-run without --dry-run after confirming.");
    process.exit(0);
  }

  await confirmSpendBeforeBroadcast({
    scriptTag: "signup-pay",
    envConfirmVar: "POWERLOOM_SIGNUP_PAY_CONFIRM",
    summaryLines,
  });

  let tx;
  if (isNative) {
    console.error("[signup-pay] payment_kind=native_value → send native/CGT value to recipient");
    tx = await signer.sendTransaction({
      to: quote.recipient,
      value: amount,
    });
  } else {
    console.error("[signup-pay] payment_kind=erc20 → ERC-20 transfer to recipient");
    const token = new ethers.Contract(quote.token_contract, ERC20_ABI, signer);
    tx = await token.transfer(quote.recipient, amount);
  }
  console.error("Submitted tx", tx.hash);
  const receipt = await tx.wait();
  if (!receipt || receipt.status !== 1) {
    console.error("Transfer failed or reverted.");
    process.exit(1);
  }

  const cr = await fetch(`${base}/signup/pay/claim`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ signup_nonce: quote.signup_nonce, tx_hash: receipt.hash }),
  });
  const claimText = await cr.text();
  let claim;
  try {
    claim = JSON.parse(claimText);
  } catch {
    console.error("Claim response not JSON:", claimText.slice(0, 500));
    process.exit(1);
  }
  if (!cr.ok) {
    console.error(JSON.stringify(claim, null, 2));
    process.exit(1);
  }

  console.log(
    JSON.stringify(
      {
        api_key: claim.api_key,
        org_id: claim.org_id,
        credit_balance: claim.credit_balance,
        plan_id: claim.plan_id,
        tx_hash: claim.tx_hash,
        chain_id: claim.chain_id,
        notice: "Export: export POWERLOOM_API_KEY=<api_key> (do not commit keys).",
      },
      null,
      2,
    ),
  );
}

main().catch((e) => {
  console.error(e.message || e);
  process.exit(1);
});
