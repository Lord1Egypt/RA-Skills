# LP Range Analysis

Recommend LP ranges for a pool based on ATR-derived price movement from Beachhouse 6-month timeseries data.

> **Playbook**: [Range Sizing](../SKILL.md#range-sizing) — backtest-vs-forward caveat and containment reporting live in SKILL.md.

## Usage

```bash
npx tsx lp-range-analysis.ts SOL/USDC
npx tsx lp-range-analysis.ts Czfq3xZZDmsdGdUyrNLtRhGc47cXcZtLG4crryfu44zE
```

## Code

```typescript
// lp-range-analysis.ts

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

const query = process.argv[2];
if (!query) {
  console.error("Usage: npx tsx lp-range-analysis.ts <PAIR or POOL_ADDRESS>");
  process.exit(1);
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

async function main() {
  const now = Math.floor(Date.now() / 1000);
  const sixMonthsAgo = now - 180 * 86400;

  // Find pool from REST API
  const res = await fetchJson<{ data: any[] }>(`${ORCA_API}/pools/search?query=${query}&limit=5`);
  const pools = res.data.sort((a: any, b: any) => Number(b.tvlUsdc) - Number(a.tvlUsdc));
  if (pools.length === 0) { console.error("No pools found"); process.exit(1); }

  const pool = pools[0];
  const pair = `${pool.tokenA.symbol}/${pool.tokenB.symbol}`;
  const feePct = pool.feeRate / 10000;
  const tickSpacing = pool.tickSpacing;
  const currentPrice = Number(pool.price);
  const isStable = STABLES.has(pool.tokenA.symbol) && STABLES.has(pool.tokenB.symbol);

  // Fetch 6-month volume from Beachhouse for VWAP prices
  const volRes = await fetchJson<{ data: { data: VolPoint[] } }>(
    `${BEACHHOUSE}/api/pools/${pool.address}/volume?time_from=${sixMonthsAgo}&time_to=${now}&type=1D`
  );
  const volData = volRes.data.data
    .filter(d => Number(d.volumeBase) > 0 && Number(d.volumeQuote) > 0)
    .sort((a, b) => a.unixTime - b.unixTime);

  if (volData.length < 15) {
    console.error("Insufficient Beachhouse data for ATR computation");
    process.exit(1);
  }

  // Compute daily VWAP prices (A/B pool ratio: quote per base)
  const vwapPrices = volData.map(d => Number(d.volumeQuote) / Number(d.volumeBase));

  // ATR (14-day): mean of absolute daily price changes over last 14 days
  const recentPrices = vwapPrices.slice(-15);
  const dailyAbsChanges: number[] = [];
  for (let i = 1; i < recentPrices.length; i++) {
    dailyAbsChanges.push(Math.abs(recentPrices[i] - recentPrices[i - 1]));
  }
  const atr = mean(dailyAbsChanges);
  const atrPct = atr / recentPrices[recentPrices.length - 1];

  // Realized volatility from daily log returns (full 6-month window)
  const logReturns: number[] = [];
  for (let i = 1; i < vwapPrices.length; i++) {
    logReturns.push(Math.log(vwapPrices[i] / vwapPrices[i - 1]));
  }
  const realizedVol = stddev(logReturns);

  // REST API stats for current context
  const s7d = pool.stats["7d"];
  const s30d = pool.stats["30d"];
  const apr7d = Number(s7d.yieldOverTvl) / 7 * 365 * 100;
  const apr30d = Number(s30d.yieldOverTvl) / 30 * 365 * 100;
  const volTvl = Number(pool.stats["24h"].volume) / Number(pool.tvlUsdc);

  console.log(`\nAnalyzing ${pair} (${feePct.toFixed(2)}% fee, tickSpacing=${tickSpacing}) — ${pool.address}\n`);

  console.log("  CURRENT STATE");
  console.log(`  Price:          $${currentPrice.toFixed(4)}`);
  console.log(`  TVL:            $${Number(pool.tvlUsdc).toLocaleString(undefined, { maximumFractionDigits: 0 })}`);
  console.log(`  Vol/TVL:        ${volTvl.toFixed(2)}x`);
  console.log(`  APR (7d):       ${apr7d.toFixed(1)}%`);
  console.log(`  APR (30d):      ${apr30d.toFixed(1)}%`);

  console.log("\n  VOLATILITY (from Beachhouse VWAP prices)");
  console.log(`  ATR (14d):      $${atr.toFixed(4)} (${(atrPct * 100).toFixed(2)}% of price)`);
  console.log(`  Realized vol:   ${(realizedVol * 100).toFixed(2)}% daily`);
  console.log(`  Data points:    ${volData.length} days`);

  // Range recommendations based on ATR multiples
  const strategies = [
    { name: "Tight",  mult: 2, desc: "Max capital efficiency, frequent rebalance" },
    { name: "Medium", mult: 4, desc: "Balanced efficiency and durability" },
    { name: "Wide",   mult: 8, desc: "Set-and-forget, lower IL risk" },
  ];

  console.log("\n  LP RANGE RECOMMENDATIONS (ATR-based)");
  console.log("  Strategy | Range                           | Width    | ATR mult | Note");
  console.log("  " + "─".repeat(90));

  for (const s of strategies) {
    const halfWidth = atr * s.mult;
    const low = currentPrice - halfWidth;
    const high = currentPrice + halfWidth;
    const widthPct = (halfWidth / currentPrice * 100).toFixed(1);

    console.log(
      `  ${s.name.padEnd(8)} | $${low.toFixed(4).padStart(10)} — $${high.toFixed(4).padEnd(10)} | ` +
      `±${widthPct.padStart(5)}% | ${s.mult}× ATR   | ${s.desc}`
    );
  }

  // Historical range containment: how often did price stay within these ranges?
  console.log("\n  HISTORICAL RANGE CONTAINMENT (6-month backtest)");
  console.log("  Range Width | Days In Range | % of Days | Avg Consecutive Days");
  console.log("  " + "─".repeat(65));

  for (const mult of [2, 4, 8]) {
    const halfWidth = atr * mult;
    const lo = currentPrice - halfWidth;
    const hi = currentPrice + halfWidth;
    let inRange = 0;
    let maxStreak = 0;
    let streak = 0;
    const streaks: number[] = [];

    for (const price of vwapPrices) {
      if (price >= lo && price <= hi) {
        inRange++;
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
      `  ±${(halfWidth / currentPrice * 100).toFixed(1).padStart(5)}% (${mult}×ATR) | ` +
      `${String(inRange).padStart(12)} | ${(inRange / vwapPrices.length * 100).toFixed(1).padStart(7)}%  | ` +
      `${avgStreak.toFixed(1).padStart(8)} days`
    );
  }

  // Recommendation
  console.log("");
  if (isStable) {
    console.log("  → Stablecoin pair. TIGHT range (2× ATR) recommended for maximum fee capture.");
    console.log("    Rebalance if price drifts beyond the tight range boundary.");
  } else if (atrPct < 0.02) {
    console.log("  → Low ATR. MEDIUM range (4× ATR) recommended. Check weekly.");
  } else if (atrPct < 0.04) {
    console.log("  → Moderate ATR. MEDIUM or WIDE range. Monitor bi-weekly.");
  } else {
    console.log("  → High ATR. WIDE range (8× ATR) recommended, or consider waiting for stabilization.");
  }
}

main().catch(console.error);
```

## Output

```
Analyzing SOL/USDC (0.04% fee, tickSpacing=4) — Czfq3xZZDmsdGdUyrNLtRhGc47cXcZtLG4crryfu44zE

  CURRENT STATE
  Price:          $148.3200
  TVL:            $31,487,806
  Vol/TVL:        12.47x
  APR (7d):       31.5%
  APR (30d):      24.8%

  VOLATILITY (from Beachhouse VWAP prices)
  ATR (14d):      $2.8400 (1.91% of price)
  Realized vol:   3.24% daily
  Data points:    178 days

  LP RANGE RECOMMENDATIONS (ATR-based)
  Strategy | Range                           | Width    | ATR mult | Note
  ──────────────────────────────────────────────────────────────────────────────────────────
  Tight    | $  142.6400 — $  154.0000       | ± 3.8%  | 2× ATR   | Max capital efficiency, frequent rebalance
  Medium   | $  136.9600 — $  159.6800       | ± 7.7%  | 4× ATR   | Balanced efficiency and durability
  Wide     | $  125.6000 — $  171.0400       | ±15.3%  | 8× ATR   | Set-and-forget, lower IL risk

  HISTORICAL RANGE CONTAINMENT (6-month backtest)
  Range Width | Days In Range | % of Days | Avg Consecutive Days
  ─────────────────────────────────────────────────────────────────
  ± 3.8% (2×ATR) |           42 |   23.6%  |      4.2 days
  ± 7.7% (4×ATR) |           89 |   50.0%  |      8.9 days
  ±15.3% (8×ATR) |          148 |   83.1%  |     18.5 days

  → Moderate ATR. MEDIUM or WIDE range. Monitor bi-weekly.
```

> Range widths are derived from ATR (14-day average true range) computed from Beachhouse VWAP prices. The backtest shows how often historical prices stayed within each range centered on the current price. Tick conversion (`PriceMath.priceToTickIndex` + tickSpacing alignment) happens at position-open time — see [Open Position](../SKILL.md#open-position).
