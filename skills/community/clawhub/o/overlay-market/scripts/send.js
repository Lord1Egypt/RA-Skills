#!/usr/bin/env node

// Overlay Protocol — Transaction Sender
// Signs and broadcasts an unsigned transaction using a private key.
// Reads transaction JSON from stdin or as a CLI argument.
//
// Usage:
//   node build.js BTC/USD long 10 5 2>/dev/null | node send.js
//   node send.js '{"to":"0x...","data":"0x...","value":"0x0","chainId":56}'
//
// Requires: OVERLAY_PRIVATE_KEY environment variable (with or without 0x prefix)

import { CONTRACTS, CHAIN_ID, USDT_TOKEN, getAccount, getWalletClient, publicClient } from "./common.js";

const account = getAccount();
if (!account) {
  console.error("Error: OVERLAY_PRIVATE_KEY environment variable is required.");
  console.error("  export OVERLAY_PRIVATE_KEY=0xabc...");
  process.exit(1);
}

// Read tx from arg or stdin
let raw = process.argv[2];
if (!raw) {
  raw = "";
  for await (const chunk of process.stdin) raw += chunk;
}
raw = raw.trim();

if (!raw) {
  console.error("Error: no transaction provided. Pipe from build.js/unwind.js or pass as argument.");
  process.exit(1);
}

const tx = JSON.parse(raw);

if (tx.chainId && tx.chainId !== CHAIN_ID) {
  console.error(`Error: expected chainId ${CHAIN_ID}, got ${tx.chainId}`);
  process.exit(1);
}

const ALLOWED_TARGETS = new Set([CONTRACTS.SHIVA.toLowerCase(), USDT_TOKEN.toLowerCase()]);
if (!tx.to || !ALLOWED_TARGETS.has(tx.to.toLowerCase())) {
  console.error(`Error: unexpected target address ${tx.to}`);
  console.error(`Allowed: ${[...ALLOWED_TARGETS].join(", ")}`);
  process.exit(1);
}

// Only approve() is allowed on the USDT token — block transfer/transferFrom/etc.
if (tx.to.toLowerCase() === USDT_TOKEN.toLowerCase()) {
  const selector = tx.data?.slice(0, 10);
  if (selector !== "0x095ea7b3") { // approve(address,uint256)
    console.error(`Error: only approve() calls are allowed on USDT. Got selector: ${selector}`);
    process.exit(1);
  }
}

const client = getWalletClient();

console.error(`Sending from: ${account.address}`);
console.error(`To: ${tx.to}`);

const hash = await client.sendTransaction({
  to: tx.to,
  data: tx.data,
  value: BigInt(tx.value || "0x0"),
});

console.error(`Waiting for confirmation...`);
const receipt = await publicClient.waitForTransactionReceipt({ hash });

console.log(JSON.stringify({
  hash,
  status: receipt.status,
  blockNumber: Number(receipt.blockNumber),
  gasUsed: Number(receipt.gasUsed),
}));
