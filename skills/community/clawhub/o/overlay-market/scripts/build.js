#!/usr/bin/env node

// Overlay Protocol — Build Position
// Encodes a buildStable transaction for opening a leveraged position.
// Outputs an unsigned transaction object (JSON) to stdout.
//
// Usage: node build.js <market> <long|short> <collateral> <leverage> [--slippage <pct>] [--dry-run]

import { encodeFunctionData, parseEther, formatUnits } from "viem";
import { CONTRACTS, CHAIN_ID, USDT_TOKEN, SHIVA_ABI, ERC20_BALANCE, ERC20_ALLOWANCE, resolveMarket, fetchMidPrice, fetchOvlPrice, calcPriceLimit, publicClient, getAccount, bigIntToNumber } from "./common.js";

const positional = [];
let slippage;
let dryRun = false;
const rawArgs = process.argv.slice(2);

for (let i = 0; i < rawArgs.length; i++) {
  if (rawArgs[i] === "--slippage" && i + 1 < rawArgs.length) {
    slippage = parseFloat(rawArgs[++i]);
  } else if (rawArgs[i] === "--dry-run") {
    dryRun = true;
  } else {
    positional.push(rawArgs[i]);
  }
}

if (positional.length < 4) {
  console.error("Usage: node build.js <market> <long|short> <collateral> <leverage> [--slippage <pct>] [--dry-run]");
  console.error("");
  console.error("  market      Market name (BTC/USD, SOL, GOLD/SILVER) or address");
  console.error("  long|short  Position direction");
  console.error("  collateral  USDT amount (e.g. 10)");
  console.error("  leverage    Multiplier (e.g. 5 for 5x)");
  console.error("  --slippage  Max slippage in % (default: 1)");
  console.error("  --dry-run   Simulate without outputting transaction");
  console.error("");
  console.error("Examples:");
  console.error("  node build.js BTC/USD long 10 5");
  console.error('  node build.js "GOLD/SILVER" short 1 3 --slippage 2');
  console.error("  node build.js BTC/USD long 10 5 --dry-run");
  process.exit(1);
}

const [marketQuery, direction, collateral, leverage] = positional;

if (direction !== "long" && direction !== "short") {
  console.error(`Error: direction must be 'long' or 'short'. Received: '${direction}'`);
  process.exit(1);
}

const col = parseFloat(collateral);
if (isNaN(col) || col <= 0) {
  console.error(`Error: collateral must be > 0. Received: '${collateral}'`);
  process.exit(1);
}

const lev = parseFloat(leverage);
if (isNaN(lev) || lev < 1) {
  console.error(`Error: leverage must be >= 1. Received: '${leverage}'`);
  process.exit(1);
}

const isLong = direction === "long";
const market = await resolveMarket(marketQuery);

const slippagePct = slippage != null ? slippage / 100 : undefined;
const slippageFrac = slippagePct ?? 0.01;
const [midPrice, ovlPrice] = await Promise.all([fetchMidPrice(market.address), fetchOvlPrice()]);
const priceLimit = calcPriceLimit(midPrice, isLong, true, slippagePct);
const midNum = bigIntToNumber(midPrice);
const limitNum = bigIntToNumber(priceLimit);

// minOvl: minimum OVL expected from USDT→OVL swap (protects against sandwich attacks)
const collateralWei = parseEther(collateral);
const expectedOvl = (collateralWei * BigInt(1e18)) / ovlPrice;
const minOvl = expectedOvl - (expectedOvl * BigInt(Math.round(slippageFrac * 10000))) / 10000n;
const notional = col * lev;

console.error(`Market: ${market.name} (${market.address})`);
console.error(`Direction: ${isLong ? "LONG" : "SHORT"}`);
console.error(`Collateral: ${collateral} USDT`);
console.error(`Leverage: ${leverage}x`);
console.error(`Notional: ${notional} USDT`);
console.error(`Mid price: ${midNum}`);
console.error(`Price limit: ${limitNum} (${slippage != null ? slippage : 1}% slippage)`);

const data = encodeFunctionData({
  abi: SHIVA_ABI,
  functionName: "buildStable",
  args: [{
    ovlMarket: market.address,
    brokerId: 0,
    isLong,
    stableCollateral: parseEther(collateral),
    leverage: parseEther(leverage),
    priceLimit,
    minOvl,
  }],
});

if (dryRun) {
  const account = getAccount();
  if (!account) {
    console.error("Dry run requires OVERLAY_PRIVATE_KEY to simulate.");
    process.exit(1);
  }

  const [usdtBalance, usdtAllowance, bnbBalance] = await Promise.all([
    publicClient.readContract({ address: USDT_TOKEN, abi: ERC20_BALANCE, functionName: "balanceOf", args: [account.address] }),
    publicClient.readContract({ address: USDT_TOKEN, abi: ERC20_ALLOWANCE, functionName: "allowance", args: [account.address, CONTRACTS.LBSC] }),
    publicClient.getBalance({ address: account.address }),
  ]);

  const usdtNum = parseFloat(formatUnits(usdtBalance, 18));
  const allowanceNum = parseFloat(formatUnits(usdtAllowance, 18));

  console.error(`\nWallet: ${account.address}`);
  console.error(`USDT balance: ${usdtNum.toFixed(2)}`);
  console.error(`USDT allowance for LBSC: ${allowanceNum >= 1e15 ? "unlimited" : allowanceNum.toFixed(2)}`);
  console.error(`BNB (gas): ${formatUnits(bnbBalance, 18)}`);

  if (usdtNum < col) {
    console.error(`\n✗ Insufficient USDT: need ${collateral}, have ${usdtNum.toFixed(2)}`);
    process.exit(1);
  }
  if (allowanceNum < col) {
    console.error(`\n✗ Insufficient USDT allowance: need ${collateral}, approved ${allowanceNum.toFixed(2)}`);
    console.error(`Run: node scripts/approve.js | node scripts/send.js`);
    process.exit(1);
  }

  try {
    await publicClient.simulateContract({
      address: CONTRACTS.SHIVA,
      abi: SHIVA_ABI,
      functionName: "buildStable",
      args: [{
        ovlMarket: market.address,
        brokerId: 0,
        isLong,
        stableCollateral: parseEther(collateral),
        leverage: parseEther(leverage),
        priceLimit,
        minOvl,
      }],
      account: account.address,
    });
    console.error(`\n✓ Simulation passed`);
  } catch (e) {
    const reason = e.cause?.reason || e.shortMessage || e.message;
    console.error(`\n✗ Simulation failed: ${reason}`);
    process.exit(1);
  }
} else {
  console.log(JSON.stringify({
    to: CONTRACTS.SHIVA,
    data,
    value: "0x0",
    chainId: CHAIN_ID,
  }, null, 2));
}
