#!/usr/bin/env node

// Overlay Protocol — Wallet Balance
// Shows USDT and BNB balances for the trading wallet on BSC.
//
// Usage:
//   node balance.js [address]
//   node balance.js              (derives address from OVERLAY_PRIVATE_KEY)

import { formatUnits, formatEther } from "viem";
import { USDT_TOKEN, ERC20_BALANCE, publicClient, getAccount } from "./common.js";

const arg = process.argv[2];
let address;

if (arg) {
  address = arg;
} else {
  const account = getAccount();
  if (account) {
    address = account.address;
  }
}

if (!address) {
  console.error("Usage: node balance.js [address]");
  console.error("");
  console.error("  If no address is provided, derives it from OVERLAY_PRIVATE_KEY env var.");
  process.exit(1);
}

const [bnbBalance, usdtBalance] = await Promise.all([
  publicClient.getBalance({ address }),
  publicClient.readContract({
    address: USDT_TOKEN,
    abi: ERC20_BALANCE,
    functionName: "balanceOf",
    args: [address],
  }),
]);

console.log(JSON.stringify({
  address,
  bnb: formatEther(bnbBalance),
  usdt: formatUnits(usdtBalance, 18),
}, null, 2));
