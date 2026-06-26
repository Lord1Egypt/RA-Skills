/**
 * Normalize trades from all-pool snapshot (tradeData map) or pool snapshot (data.trades).
 */

export function flattenAllTradesFromSnapshot(snapshot) {
  if (!snapshot) return [];
  if (Array.isArray(snapshot.trades)) {
    return snapshot.trades.map((t) => ({ poolAddress: null, trade: t }));
  }
  const td = snapshot.tradeData;
  if (!td || typeof td !== "object") return [];
  const out = [];
  for (const [poolAddress, poolBlock] of Object.entries(td)) {
    const trades = poolBlock?.trades;
    if (!Array.isArray(trades)) continue;
    for (const t of trades) {
      out.push({ poolAddress, trade: t });
    }
  }
  return out;
}

export function tradeUsd(tradeWrapper) {
  const t = tradeWrapper.trade || tradeWrapper;
  const raw =
    t.data?.calculated_trade_amount_usd ??
    t.calculated_trade_amount_usd ??
    "0";
  const n = parseFloat(String(raw).replace(/,/g, ""));
  return Number.isFinite(n) ? n : 0;
}

export function tradeDirectionLabel(tradeWrapper) {
  const t = tradeWrapper.trade || tradeWrapper;
  const a0 = parseFloat(String(t.data?.amount0 ?? "0").replace(/,/g, ""));
  return a0 < 0 ? "SELL" : "BUY";
}

export function formatEtherscanTx(hash) {
  if (!hash) return "";
  return `https://etherscan.io/tx/${hash}`;
}

export function poolInAllowlist(poolAddress, allowSet) {
  if (!poolAddress) return false;
  return allowSet.has(String(poolAddress).toLowerCase());
}

/** Pools that list a token — keys are often pool addresses (UniswapTokenPoolsSnapshot). */
export function buildPoolAllowlistFromTokenPoolsResponse(resp) {
  const set = new Set();
  const data = resp?.data ?? resp;
  const pools = data?.pools;
  if (pools && typeof pools === "object" && !Array.isArray(pools)) {
    for (const k of Object.keys(pools)) {
      if (/^0x[a-fA-F]{40}$/.test(k)) set.add(k.toLowerCase());
    }
  }
  if (Array.isArray(pools)) {
    for (const p of pools) {
      if (typeof p === "string") set.add(p.toLowerCase());
      else if (p?.pool_address) set.add(String(p.pool_address).toLowerCase());
      else if (p?.address) set.add(String(p.address).toLowerCase());
    }
  }
  return set;
}
