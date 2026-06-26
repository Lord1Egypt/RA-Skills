#!/usr/bin/env node
/**
 * Existing API key: GET /credits/plans → pick plan → pay on-chain → POST /credits/topup
 * (same verification as bds-agenthub-billing-metering `POST /credits/topup`).
 *
 * Required env (POWERLOOM_* only):
 *   POWERLOOM_API_KEY — Bearer sk_live_…
 *   POWERLOOM_EVM_PRIVATE_KEY — hex; must fund the transfer
 *   POWERLOOM_PLAN_ID — must match a row in GET /credits/plans
 *   POWERLOOM_EVM_CHAIN_ID — must match that plan's chain_id
 *   POWERLOOM_TOKEN_SYMBOL — must match plan.token_symbol for that row
 *
 * Optional:
 *   POWERLOOM_METERING_BASE_URL — default https://bds-metering.powerloom.io
 *   POWERLOOM_EVM_RPC_URL — if unset, uses plan.rpc_url or chains[].rpc_url (public hints from
 *                        GET /credits/plans; either may be empty — then you must set this)
 *
 * Confirmation (broadcast protection):
 *   Interactive TTY: prints summary; type CONFIRM before signing.
 *   Non-interactive: --yes / -y OR POWERLOOM_CREDITS_TOPUP_CONFIRM=yes after verifying details.
 *   --dry-run: resolve plan + print summary only; exits 0 without broadcasting.
 *
 * Usage:
 *   node scripts/credits-topup.mjs --dry-run
 *   node scripts/credits-topup.mjs
 *   POWERLOOM_CREDITS_TOPUP_CONFIRM=yes node scripts/credits-topup.mjs
 *   node scripts/credits-topup.mjs --yes
 */

import { ethers } from "ethers";
import {
  meteringBaseUrl,
  powerloomApiKey,
  evmPrivateKey,
  evmRpcUrl,
  planId,
  chainIdParsed,
  tokenSymbol,
} from "./lib/powerloom-env.mjs";
import { confirmSpendBeforeBroadcast } from "./lib/confirm-spend.mjs";

const ERC20_ABI = ["function transfer(address to, uint256 amount) returns (bool)"];

function fail(msg) {
  console.error(`[credits-topup] ${msg}`);
  process.exit(1);
}

function chainMeta(chains, chainId) {
  return (chains || []).find((c) => Number(c.chain_id) === Number(chainId));
}

function resolveRpc(plan, chains, envRpc) {
  const e = (envRpc || "").trim();
  if (e) return e;
  if (plan.rpc_url && String(plan.rpc_url).trim()) return String(plan.rpc_url).trim();
  const m = chainMeta(chains, plan.chain_id);
  if (m && m.rpc_url && String(m.rpc_url).trim()) return String(m.rpc_url).trim();
  return "";
}

function resolveRecipient(plan, chains) {
  if (plan.recipient && String(plan.recipient).trim()) return String(plan.recipient).trim();
  const m = chainMeta(chains, plan.chain_id);
  if (m && m.recipient && String(m.recipient).trim()) return String(m.recipient).trim();
  return "";
}

async function main() {
  const base = meteringBaseUrl();
  const apiKey = powerloomApiKey();
  const pk = evmPrivateKey();
  const pid = planId();
  const chainId = chainIdParsed();
  const symRaw = tokenSymbol();
  const rpcOverride = evmRpcUrl();

  if (!apiKey) fail("Set POWERLOOM_API_KEY");
  if (!pk) fail("Set POWERLOOM_EVM_PRIVATE_KEY");
  if (!pid || !Number.isFinite(chainId) || !symRaw) {
    fail("Set POWERLOOM_PLAN_ID, POWERLOOM_EVM_CHAIN_ID, and POWERLOOM_TOKEN_SYMBOL");
  }

  const pr = await fetch(`${base}/credits/plans`);
  if (!pr.ok) {
    console.error(await pr.text());
    fail(`GET /credits/plans failed (${pr.status})`);
  }
  const bundle = await pr.json();
  const plans = bundle.plans || [];
  const chains = bundle.chains || [];
  const sym = symRaw.toLowerCase();
  const plan = plans.find(
    (p) =>
      p.id === pid &&
      Number(p.chain_id) === chainId &&
      p.active !== false &&
      (p.token_symbol || "").toLowerCase() === sym,
  );
  if (!plan) {
    fail(
      `No matching active plan for id=${pid} chain_id=${chainId} token_symbol=${symRaw}. Run GET /credits/plans.`,
    );
  }

  const rpcUrl = resolveRpc(plan, chains, rpcOverride);
  if (!rpcUrl) {
    fail(
      "No RPC: set POWERLOOM_EVM_RPC_URL (metering may leave chains[].rpc_url empty when no public_rpc_url is configured)",
    );
  }

  const recipient = resolveRecipient(plan, chains);
  if (!recipient) fail("No recipient: plan.recipient and chains[].recipient are empty");

  const paymentKind = plan.payment_kind === "native_value" ? "native_value" : "erc20";
  const amount = ethers.parseUnits(String(plan.token_amount), Number(plan.token_decimals));

  const provider = new ethers.JsonRpcProvider(rpcUrl);
  const net = await provider.getNetwork();
  if (Number(net.chainId) !== chainId) {
    fail(`RPC chainId ${net.chainId} does not match POWERLOOM_EVM_CHAIN_ID ${chainId}. Fix POWERLOOM_EVM_RPC_URL.`);
  }

  const wallet = new ethers.Wallet(pk.startsWith("0x") ? pk : `0x${pk}`);
  const signer = wallet.connect(provider);

  const summaryLines = [
    "[credits-topup] Top-up summary — verify before broadcasting:",
    `  plan_id       ${pid}`,
    `  chain_id      ${chainId}`,
    `  token_symbol  ${symRaw}`,
    `  payment_kind  ${paymentKind}`,
    `  recipient     ${recipient}`,
    `  amount        ${amount.toString()} (atomic units, decimals=${plan.token_decimals})`,
    `  payer         ${wallet.address}`,
  ];

  if (process.argv.includes("--dry-run")) {
    for (const line of summaryLines) {
      console.error(line);
    }
    console.error("[credits-topup] --dry-run: no transaction broadcast. Re-run without --dry-run after confirming.");
    process.exit(0);
  }

  await confirmSpendBeforeBroadcast({
    scriptTag: "credits-topup",
    envConfirmVar: "POWERLOOM_CREDITS_TOPUP_CONFIRM",
    summaryLines,
  });

  let tx;
  if (paymentKind === "native_value") {
    tx = await signer.sendTransaction({
      to: recipient,
      value: amount,
    });
  } else {
    const token = new ethers.Contract(plan.token_contract, ERC20_ABI, signer);
    tx = await token.transfer(recipient, amount);
  }

  console.error("Submitted tx", tx.hash);
  const receipt = await tx.wait();
  if (!receipt || receipt.status !== 1) {
    fail("Transaction failed or reverted");
  }

  const reg = await fetch(`${base}/credits/topup`, {
    method: "POST",
    headers: {
      "content-type": "application/json",
      authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      plan_id: pid,
      chain_id: chainId,
      tx_hash: receipt.hash,
    }),
  });
  const text = await reg.text();
  let data;
  try {
    data = JSON.parse(text);
  } catch {
    fail(`Top-up response not JSON: ${text.slice(0, 400)}`);
  }
  if (!reg.ok) {
    console.error(JSON.stringify(data, null, 2));
    process.exit(1);
  }

  console.log(JSON.stringify({ ...data, notice: "Credits added for this API key." }, null, 2));
}

main().catch((e) => {
  console.error(e.message || e);
  process.exit(1);
});
