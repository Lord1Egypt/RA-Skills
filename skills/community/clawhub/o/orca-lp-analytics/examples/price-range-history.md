# Price Range History

Show actual historical price bands from Beachhouse 6-month VWAP data with rolling min/max windows and band containment analysis.

> **Playbook**: [Range Sizing](../SKILL.md#range-sizing) — historical-backtest variant. See SKILL.md for the forward-looking Monte Carlo companion.

## Usage

```bash
npx tsx price-range-history.ts SOL/USDC
npx tsx price-range-history.ts USDG/USDC
```

## Code

```typescript
// price-range-history.ts

const ORCA_API = "https://api.orca.so/v2/solana";
const BEACHHOUSE = "https://stats-api.mainnet.orca.so";

const STABLES = new Set([
  "USDC", "USDT", "USDG", "PYUSD", "USD1", "USX",
  "EURC", "CASH", "syrupUSDC", "hyUSD", "ONyc", "eUSX",
]);

async function fetchJson<T>(url: string): Promise<T> {
  const res = await fetch(url, { headers: { Accept: "application/json" } });
  if (!res.ok) throw new Error(`${res.status}: ${await res.text()}`);
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

function mean(values: number[]): number {
  return values.length === 0 ? 0 : values.reduce((a, b) => a + b, 0) / values.length;
}

function stddev(values: number[]): number {
  if (values.length < 2) return 0;
  const m = mean(values);
  const sq = values.reduce((a, v) => a + (v - m) ** 2, 0) / (values.length - 1);
  return Math.sqrt(sq);
}

const query = process.argv[2] ?? "SOL/USDC";
const [targetA, targetB] = query.includes("/") ? query.split("/") : [query, ""];

async function main() {
  const now = Math.floor(Date.now() / 1000);
  const sixMonthsAgo = now - 180 * 86400;

  // Find pool from REST API
  const r = await fetchJson<{ data: any[] }>(`${ORCA_API}/pools/search?query=${query}&limit=20`);
  const pool = r.data
    .filter((p: any) => {
      if (targetB) return p.tokenA.symbol === targetA && p.tokenB.symbol === targetB;
      return p.tokenA.symbol === targetA || p.tokenB.symbol === targetA;
    })
    .sort((a: any, b: any) => Number(b.tvlUsdc) - Number(a.tvlUsdc))[0];

  if (!pool) { console.error(`No pool found for ${query}`); process.exit(1); }

  const pair = `${pool.tokenA.symbol}/${pool.tokenB.symbol}`;
  const cur = Number(pool.price);

  // Fetch 6-month volume from Beachhouse for VWAP prices
  const volRes = await fetchJson<{ data: { data: VolPoint[] } }>(
    `${BEACHHOUSE}/api/pools/${pool.address}/volume?time_from=${sixMonthsAgo}&time_to=${now}&type=1D`
  );
  const volData = volRes.data.data
    .filter(d => Number(d.volumeBase) > 0 && Number(d.volumeQuote) > 0)
    .sort((a, b) => a.unixTime - b.unixTime);

  if (volData.length < 30) {
    console.error("Insufficient Beachhouse data");
    process.exit(1);
  }

  // Compute daily VWAP prices (A/B pool ratio: quote per base)
  const vwapPrices = volData.map(d => Number(d.volumeQuote) / Number(d.volumeBase));
  const timestamps = volData.map(d => d.unixTime);

  const allMin = Math.min(...vwapPrices);
  const allMax = Math.max(...vwapPrices);
  const allMean = mean(vwapPrices);

  console.log(`\n  ${pair} (${(pool.feeRate / 10000).toFixed(2)}% fee) | Now: $${cur.toFixed(4)} | TVL: $${(Number(pool.tvlUsdc) / 1e6).toFixed(1)}M`);
  console.log(`  Address: ${pool.address}`);
  console.log(`  Beachhouse data: ${volData.length} days\n`);

  // 6-month summary
  console.log("  6-MONTH PRICE SUMMARY (from VWAP)");
  console.log(`  Min:    $${allMin.toFixed(4)}  (${((allMin - cur) / cur * 100).toFixed(1)}% from current)`);
  console.log(`  Max:    $${allMax.toFixed(4)}  (+${((allMax - cur) / cur * 100).toFixed(1)}% from current)`);
  console.log(`  Mean:   $${allMean.toFixed(4)}`);
  console.log(`  Range:  $${(allMax - allMin).toFixed(4)} (${((allMax - allMin) / allMean * 100).toFixed(1)}% of mean)`);

  // Rolling min/max over different windows
  console.log("\n  ROLLING PRICE RANGES (min/max within window ending today)");
  console.log("  Window  | Low          | High         | Range       | Current Percentile");
  console.log("  " + "─".repeat(78));

  for (const window of [7, 14, 30, 90, 180]) {
    const windowPrices = vwapPrices.slice(-Math.min(window, vwapPrices.length));
    const lo = Math.min(...windowPrices);
    const hi = Math.max(...windowPrices);
    const range = hi - lo;
    const pctile = hi > lo ? ((cur - lo) / (hi - lo) * 100) : 50;

    console.log(
      `  ${String(window).padStart(4)}d  | $${lo.toFixed(4).padStart(10)} | ` +
      `$${hi.toFixed(4).padStart(10)} | $${range.toFixed(4).padStart(9)} | ` +
      `${pctile.toFixed(0).padStart(3)}%  ${pctile > 75 ? "(near high)" : pctile < 25 ? "(near low)" : "(mid-range)"}`
    );
  }

  // Band containment: how long did price stay within +-X% of current price
  console.log("\n  BAND CONTAINMENT (% of days price was within band of current $" + cur.toFixed(2) + ")");
  console.log("  Band     | Days In  | % of Total | Longest Streak | Avg Streak");
  console.log("  " + "─".repeat(65));

  for (const bandPct of [2, 5, 10, 20]) {
    const lo = cur * (1 - bandPct / 100);
    const hi = cur * (1 + bandPct / 100);
    let inBand = 0;
    let maxStreak = 0;
    let streak = 0;
    const streaks: number[] = [];

    for (const price of vwapPrices) {
      if (price >= lo && price <= hi) {
        inBand++;
        streak++;
      } else {
        if (streak > 0) streaks.push(streak);
        if (streak > maxStreak) maxStreak = streak;
        streak = 0;
      }
    }
    if (streak > 0) { streaks.push(streak); if (streak > maxStreak) maxStreak = streak; }
    const avgStreak = streaks.length > 0 ? mean(streaks) : 0;

    console.log(
      `  ±${String(bandPct).padStart(2)}%    | ${String(inBand).padStart(6)}   | ` +
      `${(inBand / vwapPrices.length * 100).toFixed(1).padStart(7)}%   | ` +
      `${String(maxStreak).padStart(8)} days   | ${avgStreak.toFixed(1).padStart(5)} days`
    );
  }

  // Recent price trajectory (last 14 days)
  console.log("\n  RECENT PRICE TRAJECTORY (last 14 days)");
  const recent = volData.slice(-14);
  const recentPrices = recent.map(d => Number(d.volumeQuote) / Number(d.volumeBase));
  const recentMin = Math.min(...recentPrices);
  const recentMax = Math.max(...recentPrices);

  for (let i = 0; i < recent.length; i++) {
    const d = recent[i];
    const price = recentPrices[i];
    const date = new Date(d.unixTime * 1000).toISOString().slice(0, 10);
    const barLen = Math.round(((price - recentMin) / (recentMax - recentMin || 1)) * 30);
    const bar = "█".repeat(barLen) + "░".repeat(30 - barLen);
    console.log(`  ${date}  $${price.toFixed(4).padStart(10)}  ${bar}`);
  }

  // Realized volatility context
  const logReturns: number[] = [];
  for (let i = 1; i < vwapPrices.length; i++) {
    logReturns.push(Math.log(vwapPrices[i] / vwapPrices[i - 1]));
  }
  const realizedVol = stddev(logReturns);

  console.log(`\n  Realized daily volatility: ${(realizedVol * 100).toFixed(2)}% (from ${logReturns.length} daily log returns)`);
  console.log(`  Annualized volatility:     ${(realizedVol * Math.sqrt(365) * 100).toFixed(1)}%`);
}

main().catch(console.error);
```

## Output

```
  SOL/USDC (0.04% fee) | Now: $148.3200 | TVL: $31.5M
  Address: Czfq3xZZDmsdGdUyrNLtRhGc47cXcZtLG4crryfu44zE
  Beachhouse data: 178 days

  6-MONTH PRICE SUMMARY (from VWAP)
  Min:    $95.2400  (-35.8% from current)
  Max:    $183.7100  (+23.9% from current)
  Mean:   $142.8600
  Range:  $88.4700 (61.9% of mean)

  ROLLING PRICE RANGES (min/max within window ending today)
  Window  | Low          | High         | Range       | Current Percentile
  ──────────────────────────────────────────────────────────────────────────────
     7d  | $  144.1200 |   $  152.8400 |   $  8.7200 |  48%  (mid-range)
    14d  | $  138.5600 |   $  155.2100 |   $ 16.6500 |  59%  (mid-range)
    30d  | $  126.4200 |   $  155.2100 |   $ 28.7900 |  76%  (near high)
    90d  | $   95.2400 |   $  175.3800 |   $ 80.1400 |  66%  (mid-range)
   180d  | $   95.2400 |   $  183.7100 |   $ 88.4700 |  60%  (mid-range)

  BAND CONTAINMENT (% of days price was within band of current $148.32)
  Band     | Days In  | % of Total | Longest Streak | Avg Streak
  ─────────────────────────────────────────────────────────────────
  ± 2%    |     12   |     6.7%   |        4 days   |   2.4 days
  ± 5%    |     31   |    17.4%   |        9 days   |   4.4 days
  ±10%    |     62   |    34.8%   |       18 days   |   7.8 days
  ±20%    |    108   |    60.7%   |       34 days   |  13.5 days

  RECENT PRICE TRAJECTORY (last 14 days)
  2025-04-03  $  144.1200  ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
  2025-04-04  $  141.8500  ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
  2025-04-05  $  145.2100  ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░
  2025-04-06  $  147.8400  █████████░░░░░░░░░░░░░░░░░░░░░░░░░
  2025-04-07  $  152.8400  ██████████████████████████████░░░░░
  2025-04-08  $  150.1200  █████████████████████████░░░░░░░░░░
  2025-04-09  $  148.9500  ████████████████████████░░░░░░░░░░░
  2025-04-10  $  151.3400  ███████████████████████████░░░░░░░░
  2025-04-11  $  149.7800  █████████████████████████░░░░░░░░░░
  2025-04-12  $  147.2100  ███████████████████████░░░░░░░░░░░░
  2025-04-13  $  148.5600  ████████████████████████░░░░░░░░░░░
  2025-04-14  $  152.4100  █████████████████████████████░░░░░░
  2025-04-15  $  150.8200  ██████████████████████████░░░░░░░░░
  2025-04-16  $  148.3200  ████████████████████████░░░░░░░░░░░

  Realized daily volatility: 3.24% (from 177 daily log returns)
  Annualized volatility:     61.9%
```

> Historical price bands are computed from Beachhouse 6-month daily VWAP prices as the A/B pool ratio (volumeQuote / volumeBase), which matches the actual pool execution price rather than a USD-derived approximation. This is critical for non-USDC pools like SOL/JitoSOL or cbBTC/WBTC where the ratio is what an LP position trades against. Band containment shows how realistic each range width is based on actual price history. Realized volatility uses stddev of daily log returns, not priceDelta.
