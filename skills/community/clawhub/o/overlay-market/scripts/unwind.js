#!/usr/bin/env node

// Overlay Protocol — Unwind Position
// Encodes an unwindStable transaction for closing a position (always 100%).
// Fetches 1inch swap data when excess OVL needs to be converted to USDT.
// Outputs an unsigned transaction object (JSON) to stdout.
//
// Usage: node unwind.js <market> <position_id> --direction <long|short> [--slippage <pct>] [--dry-run]

import { encodeFunctionData, parseEther, decodeFunctionData } from "viem";
import { CONTRACTS, CHAIN_ID, OVL_TOKEN, USDT_TOKEN, SHIVA_ABI, STATE_ABI, SUBGRAPH_URL, resolveMarket, fetchMidPrice, fetchOvlPrice, calcPriceLimit, fetchWithTimeout, publicClient, getAccount, bigIntToNumber } from "./common.js";

const ONEINCH_PROXY = "https://1inch-proxy.overlay-market-account.workers.dev";
const ONEINCH_API = "https://api.1inch.dev";
const SWAP_SLIPPAGE = 1; // 1% slippage for OVL→USDT swap

// 1inch v6 AggregationRouterV6.swap ABI (just enough to decode)
const ONEINCH_SWAP_ABI = [{
  inputs: [
    { name: "executor", type: "address" },
    { components: [
      { name: "srcToken", type: "address" },
      { name: "dstToken", type: "address" },
      { name: "srcReceiver", type: "address" },
      { name: "dstReceiver", type: "address" },
      { name: "amount", type: "uint256" },
      { name: "minReturnAmount", type: "uint256" },
      { name: "flags", type: "uint256" },
    ], name: "desc", type: "tuple" },
    { name: "data", type: "bytes" },
  ],
  name: "swap",
  outputs: [{ name: "returnAmount", type: "uint256" }, { name: "spentAmount", type: "uint256" }],
  stateMutability: "payable",
  type: "function",
}];

async function fetchSwapData(ovlAmount, swapSlippage = SWAP_SLIPPAGE) {
  const params = new URLSearchParams({
    src: OVL_TOKEN,
    dst: USDT_TOKEN,
    amount: ovlAmount.toString(),
    from: CONTRACTS.SHIVA,
    origin: CONTRACTS.SHIVA,
    receiver: CONTRACTS.SHIVA,
    disableEstimate: "true",
    usePatching: "true",
    slippage: String(swapSlippage),
  });

  const apiKey = process.env.ONEINCH_API_KEY;
  const base = apiKey ? ONEINCH_API : ONEINCH_PROXY;
  const url = `${base}/swap/v6.1/56/swap?${params}`;
  const headers = apiKey
    ? { Authorization: `Bearer ${apiKey}` }
    : { Origin: "https://app.overlay.market" };
  const res = await fetchWithTimeout(url, { headers });
  const json = await res.json();

  // Decode minReturnAmount from the swap calldata
  const decoded = decodeFunctionData({ abi: ONEINCH_SWAP_ABI, data: json.tx.data });
  const minReturnAmount = decoded.args[1].minReturnAmount;

  return { swapData: json.tx.data, dstAmount: BigInt(json.dstAmount), minReturnAmount };
}

// Parse args
const positional = [];
let direction = null;
let slippage;
let dryRun = false;
let ownerArg = null;
const raw = process.argv.slice(2);

for (let i = 0; i < raw.length; i++) {
  if (raw[i] === "--direction" && i + 1 < raw.length) {
    direction = raw[++i].toLowerCase();
  } else if (raw[i] === "--slippage" && i + 1 < raw.length) {
    slippage = parseFloat(raw[++i]);
  } else if (raw[i] === "--owner" && i + 1 < raw.length) {
    ownerArg = raw[++i];
  } else if (raw[i] === "--dry-run") {
    dryRun = true;
  } else {
    positional.push(raw[i]);
  }
}

if (positional.length < 2 || !direction) {
  console.error("Usage: node unwind.js <market> <position_id> --direction <long|short> [--slippage <pct>] [--dry-run]");
  console.error("");
  console.error("  market       Market name or address");
  console.error("  position_id  Position ID number");
  console.error("  --direction  Required. 'long' or 'short' (sets correct price limit)");
  console.error("  --owner      Owner address (default: derived from OVERLAY_PRIVATE_KEY)");
  console.error("  --slippage   Max slippage in % (default: 1)");
  console.error("  --dry-run    Show expected value without outputting transaction");
  console.error("");
  console.error("Examples:");
  console.error("  node unwind.js BTC/USD 42 --direction long");
  console.error('  node unwind.js "GOLD/SILVER" 7 --direction short --dry-run');
  process.exit(1);
}

if (direction !== "long" && direction !== "short") {
  console.error(`Error: --direction must be 'long' or 'short'. Received: '${direction}'`);
  process.exit(1);
}

let positionId;
try {
  positionId = BigInt(positional[1]);
} catch {
  console.error(`Error: position_id must be a valid integer. Received: '${positional[1]}'`);
  process.exit(1);
}

const isLong = direction === "long";
const market = await resolveMarket(positional[0]);

const slippagePct = slippage != null ? slippage / 100 : undefined;
const midPrice = await fetchMidPrice(market.address);
const priceLimit = calcPriceLimit(midPrice, isLong, false, slippagePct);
const midNum = bigIntToNumber(midPrice);
const limitNum = bigIntToNumber(priceLimit);

console.error(`Market: ${market.name} (${market.address})`);
console.error(`Position ID: ${positionId.toString()}`);
console.error(`Direction: ${isLong ? "LONG" : "SHORT"}`);
console.error(`Mid price: ${midNum}`);
console.error(`Price limit: ${limitNum} (${slippage != null ? slippage : 1}% slippage)`);

// Fetch position data to determine if swap is needed
const account = getAccount();
const ownerAddress = ownerArg || account?.address;
if (!ownerAddress) {
  console.error("Error: provide --owner <address> or set OVERLAY_PRIVATE_KEY.");
  process.exit(1);
}

const LOAN_QUERY = `
  query GetLoanData($market: String!, $positionId: String!, $owner: String!) {
    positions(where: { market: $market, positionId: $positionId, owner: $owner }) {
      loan { stableAmount ovlAmount }
      entryPrice
    }
  }
`;

const [ovlValue, tradingFee, currentOvlPrice, subgraphResult] = await Promise.all([
  publicClient.readContract({
    address: CONTRACTS.STATE, abi: STATE_ABI,
    functionName: "value", args: [market.address, CONTRACTS.SHIVA, positionId],
  }),
  publicClient.readContract({
    address: CONTRACTS.STATE, abi: STATE_ABI,
    functionName: "tradingFee", args: [market.address, CONTRACTS.SHIVA, positionId],
  }),
  fetchOvlPrice(),
  fetchWithTimeout(SUBGRAPH_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query: LOAN_QUERY,
      variables: {
        market: market.address,
        positionId: "0x" + positionId.toString(16),
        owner: ownerAddress.toLowerCase(),
      },
    }),
  }).then(r => r.json()),
]);

const ovlPriceNum = bigIntToNumber(currentOvlPrice);
const pos = subgraphResult.data?.positions?.[0];

if (!pos?.loan) {
  console.error("Error: Could not find loan data for this position.");
  process.exit(1);
}

const loanCollateral = BigInt(pos.loan.stableAmount);
const loanDebt = BigInt(pos.loan.ovlAmount);
const netOvl = ovlValue - tradingFee - loanDebt;
const netOvlInStable = (netOvl * currentOvlPrice) / BigInt(1e18);
const stableValue = loanCollateral + netOvlInStable;

const collateralNum = bigIntToNumber(loanCollateral);
const valueNum = Math.max(0, bigIntToNumber(stableValue));
const feeNum = bigIntToNumber(tradingFee) * ovlPriceNum;
const pnl = valueNum - collateralNum;
const pnlPct = collateralNum > 0 ? (pnl / collateralNum) * 100 : 0;
const entryPrice = bigIntToNumber(BigInt(pos.entryPrice));

console.error("");
console.error(`Entry price: ${entryPrice}`);
console.error(`Collateral: ${collateralNum.toFixed(2)} USDT`);
console.error(`Current value: ${valueNum.toFixed(2)} USDT`);
console.error(`Trading fee: ~${feeNum.toFixed(4)} USDT`);
console.error(`PnL: ${pnl >= 0 ? "+" : ""}${pnl.toFixed(2)} USDT (${pnlPct >= 0 ? "+" : ""}${pnlPct.toFixed(1)}%)`);
console.error(`Expected receive: ~${valueNum.toFixed(2)} USDT`);

// Fetch swap data if there's excess OVL to convert
let swapData = "0x";
let minOut = 0n;

if (netOvl > 0n) {
  const netOvlNum = bigIntToNumber(netOvl);
  console.error(`\nExcess OVL: ${netOvlNum.toFixed(4)} (~$${(netOvlNum * ovlPriceNum).toFixed(4)} USDT)`);
  console.error("Fetching 1inch swap quote (OVL → USDT)...");
  const swap = await fetchSwapData(netOvl);
  swapData = swap.swapData;
  minOut = swap.minReturnAmount;
  console.error(`Swap expected: ${bigIntToNumber(swap.dstAmount).toFixed(6)} USDT`);
  console.error(`Swap minOut: ${bigIntToNumber(minOut).toFixed(6)} USDT`);
} else {
  console.error("\nNo excess OVL — swap not needed.");
}

const data = encodeFunctionData({
  abi: SHIVA_ABI,
  functionName: "unwindStable",
  args: [
    {
      ovlMarket: market.address,
      brokerId: 0,
      positionId,
      fraction: parseEther("1"),
      priceLimit,
    },
    swapData,
    minOut,
  ],
});

if (dryRun) {
  // Simulate
  try {
    await publicClient.simulateContract({
      address: CONTRACTS.SHIVA,
      abi: SHIVA_ABI,
      functionName: "unwindStable",
      args: [
        {
          ovlMarket: market.address,
          brokerId: 0,
          positionId,
          fraction: parseEther("1"),
          priceLimit,
        },
        swapData,
        minOut,
      ],
      account: ownerAddress,
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
