#!/usr/bin/env node

const ENDPOINT = "https://jarvis-orderflow-router.yl124915300.workers.dev/v1/route";
const ADDRESS = /^0x[0-9a-fA-F]{40}$/;
const DATA = /^0x[0-9a-fA-F]*$/;
const DECIMAL = /^(0|[1-9][0-9]*)(\.[0-9]+)?$/;
const UINT = /^(0|[1-9][0-9]*)$/;
const TOKENS = new Set(["USDC", "WETH", "DAI"]);
const TOKEN_ADDRESSES = new Set([
  "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
  "0x4200000000000000000000000000000000000006",
  "0x50c5725949a6f0c72e6c4a641f24049a917db0cb",
]);

function fail(message) {
  process.stderr.write(`${message}\n`);
  process.exit(1);
}

async function readIntent() {
  const inline = process.argv[2];
  const raw = inline ?? await new Promise((resolve, reject) => {
    let input = "";
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", (chunk) => { input += chunk; });
    process.stdin.on("end", () => resolve(input));
    process.stdin.on("error", reject);
  });
  try {
    return JSON.parse(raw);
  } catch {
    fail("Intent must be valid JSON.");
  }
}

const intent = await readIntent();
if (intent.chain !== "base") fail("Jarvis Smart Route supports Base only.");
for (const key of ["sellToken", "buyToken"]) {
  const value = String(intent[key] ?? "");
  if (!TOKENS.has(value.toUpperCase()) && !TOKEN_ADDRESSES.has(value.toLowerCase())) {
    fail(`${key} must be USDC, WETH, DAI, or its Base token address.`);
  }
}
if (!ADDRESS.test(intent.buyerWallet ?? "")) fail("buyerWallet must be a 20-byte EVM address.");
if (!DECIMAL.test(intent.amount ?? "") || Number(intent.amount) <= 0) {
  fail("amount must be a positive human decimal string.");
}
if (intent.slippageBps != null && (!Number.isInteger(intent.slippageBps) || intent.slippageBps < 1 || intent.slippageBps > 100)) {
  fail("slippageBps must be an integer from 1 to 100.");
}

let response;
try {
  response = await fetch(ENDPOINT, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      chain: intent.chain,
      sellToken: intent.sellToken,
      buyToken: intent.buyToken,
      amount: intent.amount,
      buyerWallet: intent.buyerWallet,
      ...(intent.slippageBps == null ? {} : { slippageBps: intent.slippageBps }),
    }),
  });
} catch (error) {
  fail(`Jarvis Router request failed: ${error?.message ?? "network error"}`);
}

const raw = await response.text();
let route;
try {
  route = JSON.parse(raw);
} catch {
  fail(`Jarvis Router returned non-JSON (HTTP ${response.status}).`);
}
if (!response.ok || route.ok !== true) fail(`Jarvis Router rejected the intent (HTTP ${response.status}).`);
if (route.safety?.JARVIS_CUSTODY !== 0 || route.safety?.JARVIS_CAPITAL_SPEND !== 0 || route.safety?.privateKeyAccessed !== false || route.safety?.signs !== false || route.safety?.sends !== false || route.safety?.broadcasts !== false) {
  fail("Jarvis safety invariants failed.");
}

if (route.decision === "NO_MONETIZABLE_ROUTE") {
  if (route.unsignedTransaction !== null || route.feeDisclosure?.feeBps !== 0) {
    fail("Inconsistent NO_MONETIZABLE_ROUTE response.");
  }
  process.stdout.write(`${JSON.stringify({
    ok: true,
    decision: "NO_MONETIZABLE_ROUTE",
    intentId: route.intentId,
    providerStatus: route.providerStatus,
    comparison: route.comparison,
    feeDisclosure: route.feeDisclosure,
    sendCallsInput: null,
    buyerApprovalRequired: true,
    signed: false,
    broadcast: false,
  }, null, 2)}\n`);
  process.exit(0);
}

const tx = route.unsignedTransaction;
if (!tx || tx.chainId !== 8453 || !ADDRESS.test(tx.to ?? "") || !DATA.test(tx.data ?? "") || !UINT.test(tx.value ?? "")) {
  fail("Jarvis Router returned malformed or non-Base unsigned calldata.");
}

process.stdout.write(`${JSON.stringify({
  ok: true,
  decision: "ROUTE_AVAILABLE",
  intentId: route.intentId,
  provider: route.provider,
  providerStatus: route.providerStatus,
  comparison: route.comparison,
  feeDisclosure: route.feeDisclosure,
  buyerExpectedNetOutput: route.buyerExpectedNetOutput ?? null,
  unsignedTransaction: tx,
  sendCallsInput: {
    chain: "base",
    calls: [{ to: tx.to, value: `0x${BigInt(tx.value).toString(16)}`, data: tx.data }],
  },
  buyerApprovalRequired: true,
  signed: false,
  broadcast: false,
}, null, 2)}\n`);
