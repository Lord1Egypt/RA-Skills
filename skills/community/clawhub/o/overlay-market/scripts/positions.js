#!/usr/bin/env node

// Overlay Protocol — Position Monitor
// Fetches open positions for a given address with real-time PnL.
// Outputs JSON to stdout.
//
// Usage:
//   node positions.js [owner_address]
//   node positions.js                  (derives address from OVERLAY_PRIVATE_KEY)

import { CONTRACTS, SUBGRAPH_URL, STATE_ABI, fetchMarkets, fetchOvlPrice, fetchWithTimeout, publicClient, getAccount, bigIntToNumber } from "./common.js";

const POSITION_QUERY = `
  query GetPositions($account: String!) {
    positions(
      where: { owner: $account, isLiquidated: false, fractionUnwound_lt: "1000000000000000000", loan_not: null }
      orderBy: createdAtTimestamp
      orderDirection: desc
    ) {
      id
      positionId
      market { id }
      isLong
      leverage
      initialNotional
      entryPrice
      fractionUnwound
      createdAtTimestamp
      loan { stableAmount ovlAmount price }
    }
  }
`;

async function buildMarketNameMap() {
  const marketsRaw = await fetchMarkets();
  const map = {};
  for (const m of marketsRaw["56"] || []) {
    for (const c of m.chains || []) {
      if (String(c.chainId) === "56") {
        map[c.deploymentAddress.toLowerCase()] = m.marketName;
      }
    }
  }
  return map;
}

const arg = process.argv[2];
let ownerAddress;

if (arg) {
  ownerAddress = arg.toLowerCase();
} else {
  const account = getAccount();
  if (account) {
    ownerAddress = account.address.toLowerCase();
  }
}

if (!ownerAddress) {
  console.error("Usage: node positions.js [owner_address]");
  console.error("");
  console.error("  If no address is provided, derives it from OVERLAY_PRIVATE_KEY env var.");
  process.exit(1);
}

const [currentOvlPrice, marketNames] = await Promise.all([fetchOvlPrice(), buildMarketNameMap()]);
const ovlPriceNum = bigIntToNumber(currentOvlPrice);

console.error(`Owner: ${ownerAddress}`);
console.error(`OVL Price: $${ovlPriceNum.toFixed(6)}`);

const result = await fetchWithTimeout(SUBGRAPH_URL, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    query: POSITION_QUERY,
    variables: { account: ownerAddress },
  }),
}).then((r) => r.json());

if (result.errors) {
  console.error("GraphQL errors:", JSON.stringify(result.errors));
  process.exit(1);
}

const rawPositions = result.data?.positions || [];

if (rawPositions.length === 0) {
  console.log(JSON.stringify({ owner: ownerAddress, positions: [], errors: { count: 0 }, summary: { count: 0, totalValueUSDT: 0, totalPnlUSDT: 0 } }, null, 2));
  process.exit(0);
}

// Batch all RPC calls via multicall
const multicallContracts = rawPositions.flatMap((pos) => {
  const posId = BigInt(pos.positionId);
  return [
    { address: CONTRACTS.STATE, abi: STATE_ABI, functionName: "value", args: [pos.market.id, CONTRACTS.SHIVA, posId] },
    { address: CONTRACTS.STATE, abi: STATE_ABI, functionName: "tradingFee", args: [pos.market.id, CONTRACTS.SHIVA, posId] },
  ];
});

const multicallResults = await publicClient.multicall({ contracts: multicallContracts });

const positions = [];
const errorCounts = {};

for (let i = 0; i < rawPositions.length; i++) {
  const pos = rawPositions[i];
  const marketAddr = pos.market.id;
  const marketName = marketNames[marketAddr.toLowerCase()] || null;

  const valueResult = multicallResults[i * 2];
  const feeResult = multicallResults[i * 2 + 1];

  if (valueResult.status === "failure" || feeResult.status === "failure") {
    const err = valueResult.error || feeResult.error;
    const reason = err?.cause?.reason || err?.shortMessage || "RPC call failed";
    if (!errorCounts[reason]) errorCounts[reason] = [];
    errorCounts[reason].push(marketName || marketAddr);
    continue;
  }

  const ovlValue = valueResult.result;
  const tradingFee = feeResult.result;
  const loanCollateral = BigInt(pos.loan.stableAmount);
  const loanDebt = BigInt(pos.loan.ovlAmount);

  const netOvl = ovlValue - tradingFee - loanDebt;
  const netOvlInStable = (netOvl * currentOvlPrice) / BigInt(1e18);
  const stableValue = loanCollateral + netOvlInStable;

  const loanStableNum = bigIntToNumber(loanCollateral);
  const stableValueNum = Math.max(0, bigIntToNumber(stableValue));
  const pnlUSDT = stableValueNum - loanStableNum;
  const pnlPercent = loanStableNum > 0 ? (pnlUSDT / loanStableNum) * 100 : 0;
  const sizeUSDT = bigIntToNumber(BigInt(pos.initialNotional)) * ovlPriceNum;

  // Use enough decimal places to show meaningful digits (min 2, up to 6 for tiny values)
  const usdtDecimals = (v) => { const a = Math.abs(v); return a === 0 ? 2 : a < 0.01 ? 6 : a < 0.1 ? 4 : 2; };
  const fmt = (v) => parseFloat(v.toFixed(usdtDecimals(v)));

  positions.push({
    positionId: pos.positionId,
    market: marketName,
    marketAddress: marketAddr,
    isLong: pos.isLong,
    leverage: parseFloat(Number(pos.leverage).toFixed(2)),
    entryPrice: parseFloat(bigIntToNumber(BigInt(pos.entryPrice)).toFixed(6)),
    collateralUSDT: fmt(loanStableNum),
    sizeUSDT: fmt(sizeUSDT),
    valueUSDT: fmt(stableValueNum),
    pnlUSDT: fmt(pnlUSDT),
    pnlPercent: parseFloat(pnlPercent.toFixed(2)),
    createdAt: new Date(Number(pos.createdAtTimestamp) * 1000).toISOString(),
  });
}

const totalValue = positions.reduce((s, p) => s + p.valueUSDT, 0);
const totalPnl = positions.reduce((s, p) => s + p.pnlUSDT, 0);
const errorTotal = Object.values(errorCounts).reduce((s, arr) => s + arr.length, 0);

console.log(JSON.stringify({
  owner: ownerAddress,
  positions,
  errors: { count: errorTotal, reasons: errorCounts },
  summary: {
    count: positions.length,
    totalValueUSDT: parseFloat(totalValue.toFixed(2)),
    totalPnlUSDT: parseFloat(totalPnl.toFixed(2)),
  },
}, null, 2));
