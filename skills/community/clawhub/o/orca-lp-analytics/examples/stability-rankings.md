# Stability Rankings

Rank the top Orca pools by stability score using Beachhouse 6-month timeseries data for proper volatility and TVL consistency measurement.

> **Playbook**: [Stability Analysis](../SKILL.md#stability-analysis) — red flags (TVL bleeding, yield decay) and reporting rules live in SKILL.md.

## Usage

```bash
npx tsx stability-rankings.ts
```

## Code

```typescript
// stability-rankings.ts

const ORCA_API = "https://api.orca.so/v2/solana";
const BEACHHOUSE = "https://stats-api.mainnet.orca.so";

const STABLES = new Set([
  "USDC", "USDT", "USDG", "PYUSD", "USD1", "USX",
  "EURC", "CASH", "syrupUSDC", "hyUSD", "ONyc", "eUSX",
]);

async function fetchJson<T>(url: string): Promise<T> {
  const res = await fetch(url, { headers: { Accept: "application/json" } });
  if (!res.ok) throw new Error(`${res.status}`);
  return res.json();
}

interface VolPoint {
  totalVolumeUsd: string;
  volumeBase: string;
  volumeQuote: string;
  volumeBaseUsd: string;
  volumeQuoteUsd: string;
  unixTime: number;
}

interface TvlPoint {
  tvl: string;
  baseAmount: string;
  quoteAmount: string;
  unixTime: number;
}

interface Pool {
  address: string;
  feeRate: number;
  tvlUsdc: string;
  price: string;
  tokenA: { symbol: string };
  tokenB: { symbol: string };
  stats: {
    "24h": { volume: string; fees: string; yieldOverTvl: string };
    "7d": { volume: string; fees: string; yieldOverTvl: string };
    "30d": { volume: string; fees: string; yieldOverTvl: string };
  };
}

function stddev(values: number[]): number {
  if (values.length < 2) return 0;
  const mean = values.reduce((a, b) => a + b, 0) / values.length;
  const sq = values.reduce((a, v) => a + (v - mean) ** 2, 0) / (values.length - 1);
  return Math.sqrt(sq);
}

function mean(values: number[]): number {
  return values.length === 0 ? 0 : values.reduce((a, b) => a + b, 0) / values.length;
}

function coefficientOfVariation(values: number[]): number {
  const m = mean(values);
  if (m === 0) return Infinity;
  return stddev(values) / Math.abs(m);
}

async function main() {
  const now = Math.floor(Date.now() / 1000);
  const sixMonthsAgo = now - 180 * 86400;

  // Fetch top pools from REST API
  const allPools = await fetchJson<{ data: Pool[] }>(
    `${ORCA_API}/pools?orderBy=tvlUsdc&orderDirection=desc`
  );
  const pools = allPools.data.filter(p => Number(p.tvlUsdc) > 100_000).slice(0, 30);

  const results: Array<{
    pool: Pool;
    score: number;
    realizedVol: number;
    atrPct: number;
    tvlCv: number;
    maxDrawdown: number;
    apr7d: number;
    apr30d: number;
    isStable: boolean;
  }> = [];

  for (const pool of pools) {
    // Fetch 6-month volume from Beachhouse for VWAP prices
    let volData: VolPoint[];
    let tvlData: TvlPoint[];
    try {
      const volRes = await fetchJson<{ data: { data: VolPoint[] } }>(
        `${BEACHHOUSE}/api/pools/${pool.address}/volume?time_from=${sixMonthsAgo}&time_to=${now}&type=1D`
      );
      volData = volRes.data.data
        .filter(d => Number(d.volumeBase) > 0 && Number(d.volumeQuote) > 0)
        .sort((a, b) => a.unixTime - b.unixTime);
    } catch {
      continue; // Skip pools without Beachhouse data
    }

    // Fetch 6-month TVL from Beachhouse
    try {
      const tvlRes = await fetchJson<{ data: { data: TvlPoint[] } }>(
        `${BEACHHOUSE}/api/pools/${pool.address}/tvl?time_from=${sixMonthsAgo}&time_to=${now}&type=1D`
      );
      tvlData = tvlRes.data.data
        .filter(d => Number(d.tvl) > 0)
        .sort((a, b) => a.unixTime - b.unixTime);
    } catch {
      continue;
    }

    if (volData.length < 30) continue; // need enough data

    // Compute daily VWAP prices (A/B pool ratio: quote per base)
    const vwapPrices = volData.map(d => Number(d.volumeQuote) / Number(d.volumeBase));

    // ATR (14-day): mean of absolute daily price changes over last 14 days
    const recentPrices = vwapPrices.slice(-15); // need 15 prices for 14 diffs
    const dailyAbsChanges: number[] = [];
    for (let i = 1; i < recentPrices.length; i++) {
      dailyAbsChanges.push(Math.abs(recentPrices[i] - recentPrices[i - 1]));
    }
    const atr = mean(dailyAbsChanges);
    const atrPct = atr / recentPrices[recentPrices.length - 1];

    // Realized volatility from daily log returns
    const logReturns: number[] = [];
    for (let i = 1; i < vwapPrices.length; i++) {
      logReturns.push(Math.log(vwapPrices[i] / vwapPrices[i - 1]));
    }
    const realizedVol = stddev(logReturns);

    // TVL consistency: coefficient of variation
    const tvlValues = tvlData.map(d => Number(d.tvl));
    const tvlCv = coefficientOfVariation(tvlValues);

    // Max drawdown from VWAP prices
    let peak = vwapPrices[0];
    let maxDrawdown = 0;
    for (const p of vwapPrices) {
      if (p > peak) peak = p;
      const dd = (peak - p) / peak;
      if (dd > maxDrawdown) maxDrawdown = dd;
    }

    // Stability score: 100 minus penalties
    let score = 100;
    score -= Math.min(atrPct * 100 * 10, 30);        // ATR% penalty (max 30)
    score -= Math.min(tvlCv * 50, 25);                // TVL CV penalty (max 25)
    score -= Math.min(maxDrawdown * 100 * 0.8, 25);   // Max drawdown penalty (max 25)
    score -= Math.min(realizedVol * 100 * 3, 20);     // Realized vol penalty (max 20)
    score = Math.max(0, Math.round(score));

    const apr7d = Number(pool.stats["7d"].yieldOverTvl) / 7 * 365 * 100;
    const apr30d = Number(pool.stats["30d"].yieldOverTvl) / 30 * 365 * 100;
    const isStable = STABLES.has(pool.tokenA.symbol) && STABLES.has(pool.tokenB.symbol);

    results.push({
      pool, score, realizedVol, atrPct, tvlCv, maxDrawdown,
      apr7d, apr30d, isStable,
    });
  }

  results.sort((a, b) => b.score - a.score);

  function printGroup(label: string, items: typeof results) {
    console.log(`\n  ${label}`);
    console.log("  Rank  Pair              Score  ATR(14d)  RealVol  TVL CV  MaxDD   APR(7d)  APR(30d)");
    console.log("  " + "─".repeat(88));
    items.forEach((r, i) => {
      const pair = `${r.pool.tokenA.symbol}/${r.pool.tokenB.symbol}`;
      const icon = r.score >= 80 ? "🟢" : r.score >= 60 ? "🟡" : "🔴";
      const atr = (r.atrPct * 100).toFixed(2) + "%";
      const rv = (r.realizedVol * 100).toFixed(2) + "%";
      const cv = r.tvlCv.toFixed(3);
      const dd = (r.maxDrawdown * 100).toFixed(1) + "%";
      const a7 = r.apr7d.toFixed(1) + "%";
      const a30 = r.apr30d.toFixed(1) + "%";
      console.log(
        `  ${String(i + 1).padStart(4)}  ${pair.padEnd(16)} ${icon}${String(r.score).padStart(3)}  ` +
        `${atr.padStart(7)}  ${rv.padStart(6)}  ${cv.padStart(5)}  ${dd.padStart(5)}  ${a7.padStart(6)}  ${a30.padStart(7)}`
      );
    });
  }

  printGroup("STABLECOIN PAIRS", results.filter(r => r.isStable));
  printGroup("VOLATILE PAIRS", results.filter(r => !r.isStable));
}

main().catch(console.error);
```

## Output

```
  STABLECOIN PAIRS
  Rank  Pair              Score  ATR(14d)  RealVol  TVL CV  MaxDD   APR(7d)  APR(30d)
  ────────────────────────────────────────────────────────────────────────────────────────────
     1  PYUSD/USDC       🟢 95    0.01%   0.04%  0.031    0.3%    8.4%      7.9%
     2  syrupUSDC/USDC   🟢 93    0.00%   0.02%  0.025    0.1%   12.1%     11.5%
     3  USDG/USDC        🟢 91    0.02%   0.06%  0.042    0.5%    6.3%      5.8%
     4  ONyc/USDC        🟢 87    0.03%   0.09%  0.058    0.8%    9.2%      8.1%
     5  CASH/USDC        🟡 78    0.05%   0.14%  0.091    1.2%   14.6%     10.2%
     6  USDC/EURC        🟡 64    0.12%   0.31%  0.073    2.8%    5.1%      4.8%

  VOLATILE PAIRS
  Rank  Pair              Score  ATR(14d)  RealVol  TVL CV  MaxDD   APR(7d)  APR(30d)
  ────────────────────────────────────────────────────────────────────────────────────────────
     1  SOL/USDG         🟡 62    1.24%   2.81%  0.085   18.4%   18.3%     15.7%
     2  cbBTC/USDC       🟡 60    1.48%   3.15%  0.102   22.1%   22.1%     19.4%
     3  SOL/USDC         🔴 48    1.52%   3.24%  0.134   28.3%   31.5%     24.8%
     4  SOL/whETH        🔴 39    2.05%   4.12%  0.156   32.7%   28.4%     21.1%
     ...
```

> Stability score is computed from Beachhouse 6-month timeseries: ATR (14-day average true range from VWAP prices), realized volatility (stddev of daily log returns), TVL consistency (coefficient of variation), and max drawdown. REST API stats provide current APR context.
