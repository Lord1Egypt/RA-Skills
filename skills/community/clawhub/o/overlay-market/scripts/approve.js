#!/usr/bin/env node

// Overlay Protocol — Approve USDT
// Encodes a USDT approve transaction for the LBSC contract.
// Outputs an unsigned transaction object (JSON) to stdout.
//
// Usage: node approve.js [amount]
//   amount — USDT to approve (default: unlimited)

import { encodeFunctionData, parseUnits, formatUnits, maxUint256 } from "viem";
import { CONTRACTS, CHAIN_ID, USDT_TOKEN, ERC20_APPROVE, ERC20_ALLOWANCE, publicClient, getAccount } from "./common.js";

const amountArg = process.argv[2];
const amount = amountArg ? parseUnits(amountArg, 18) : maxUint256;
const isUnlimited = amount === maxUint256;

console.error(`Approving USDT for LBSC (${CONTRACTS.LBSC})`);
console.error(`Amount: ${isUnlimited ? "unlimited" : formatUnits(amount, 18) + " USDT"}`);

// Show current allowance if we have an account
const account = getAccount();
if (account) {
  const current = await publicClient.readContract({
    address: USDT_TOKEN,
    abi: ERC20_ALLOWANCE,
    functionName: "allowance",
    args: [account.address, CONTRACTS.LBSC],
  });
  const currentNum = parseFloat(formatUnits(current, 18));
  console.error(`Current allowance: ${currentNum >= 1e15 ? "unlimited" : currentNum.toFixed(2) + " USDT"}`);
}

const data = encodeFunctionData({
  abi: ERC20_APPROVE,
  functionName: "approve",
  args: [CONTRACTS.LBSC, amount],
});

console.log(JSON.stringify({
  to: USDT_TOKEN,
  data,
  value: "0x0",
  chainId: CHAIN_ID,
}, null, 2));
