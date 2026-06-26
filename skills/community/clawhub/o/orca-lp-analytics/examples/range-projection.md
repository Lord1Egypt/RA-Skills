# Range Projection

Monte Carlo price projection using Beachhouse-derived realized volatility from 6-month VWAP prices.

> **Playbook**: [Monte Carlo Projection](../SKILL.md#monte-carlo-projection) — critical reporting rules (percentile framing, GBM caveat, never combine with fee projection) live in SKILL.md.

## Usage

```bash
npx tsx range-projection.ts SOL/USDC
npx tsx range-projection.ts USDG/USDC
```

## Code

```typescript
// range-projection.ts

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
  const isStableStable = STABLES.has(pool.tokenA.symbol) && STABLES.has(pool.tokenB.symbol);
  const cur = Number(pool.price);

  // Fetch 6-month volume from Beachhouse
  const volRes = await fetchJson<{ data: { data: VolPoint[] } }>(
    `${BEACHHOUSE}/api/pools/${pool.address}/volume?time_from=${sixMonthsAgo}&time_to=${now}&type=1D`
  );
  const volData = volRes.data.data
    .filter(d => Number(d.volumeBase) > 0 && Number(d.volumeQuote) > 0)
    .sort((a, b) => a.unixTime - b.unixTime);

  if (volData.length < 30) {
    console.error("Insufficient Beachhouse data for volatility computation");
    process.exit(1);
  }

  // Compute daily VWAP prices (A/B pool ratio: quote per base)
  const vwapPrices = volData.map(d => Number(d.volumeQuote) / Number(d.volumeBase));

  // Compute daily log returns
  const logReturns: number[] = [];
  for (let i = 1; i < vwapPrices.length; i++) {
    logReturns.push(Math.log(vwapPrices[i] / vwapPrices[i - 1]));
  }

  // Realized volatility and drift from actual daily returns
  const dailyVol = stddev(logReturns);
  const dailyDrift = mean(logReturns);

  console.log(`\n  ${pair} (${(pool.feeRate / 10000).toFixed(2)}% fee)`);
  console.log(`  Address: ${pool.address}`);
  console.log(`  Current: $${cur.toFixed(4)} | TVL: $${(Number(pool.tvlUsdc) / 1e6).toFixed(1)}M`);
  console.log(`\n  VOLATILITY PARAMETERS (from ${volData.length}-day Beachhouse VWAP)`);
  console.log(`  Realized daily vol: ${(dailyVol * 100).toFixed(2)}%`);
  console.log(`  Daily drift:        ${(dailyDrift * 100).toFixed(3)}%`);
  console.log(`  Annualized vol:     ${(dailyVol * Math.sqrt(365) * 100).toFixed(1)}%`);

  // --- Monte Carlo Projection using geometric Brownian motion ---
  const SIMS = 5000;
  console.log(`\n  ┌─ MONTE CARLO PROJECTION (${SIMS} sims, Beachhouse-derived vol) ─────┐`);

  for (const days of [7, 14, 30, 90]) {
    const finals: number[] = [];
    for (let sim = 0; sim < SIMS; sim++) {
      let p = cur;
      for (let d = 0; d < days; d++) {
        // Box-Muller for normal random
        const u1 = Math.random(), u2 = Math.random();
        const z = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
        // Geometric Brownian motion: S(t+1) = S(t) * exp((mu - sigma^2/2) + sigma*z)
        p *= Math.exp((dailyDrift - 0.5 * dailyVol * dailyVol) + dailyVol * z);
      }
      finals.push(p);
    }
    finals.sort((a, b) => a - b);
    const p5 = finals[Math.floor(SIMS * 0.05)];
    const p25 = finals[Math.floor(SIMS * 0.25)];
    const p50 = finals[Math.floor(SIMS * 0.50)];
    const p75 = finals[Math.floor(SIMS * 0.75)];
    const p95 = finals[Math.floor(SIMS * 0.95)];
    const width90 = ((p95 - p5) / cur) * 100;

    console.log(
      `  │  ${String(days).padStart(2)}d:  5th $${p5.toFixed(2).padStart(10)} | ` +
      `25th $${p25.toFixed(2).padStart(10)} | ` +
      `50th $${p50.toFixed(2).padStart(10)} | ` +
      `75th $${p75.toFixed(2).padStart(10)} | ` +
      `95th $${p95.toFixed(2).padStart(10)}  │`
    );
    console.log(
      `  │       90% range: $${p5.toFixed(2).padStart(10)} — $${p95.toFixed(2).padEnd(10)}  ` +
      `(±${(width90 / 2).toFixed(1)}%)` +
      `${" ".repeat(Math.max(0, 24 - (width90 / 2).toFixed(1).length))}│`
    );
  }
  console.log("  └──────────────────────────────────────────────────────────────────┘");

  // --- Volatility regime ---
  const regime = dailyVol < 0.01 ? "LOW" : dailyVol < 0.03 ? "MEDIUM" : "HIGH";
  console.log(`\n  Volatility regime: ${regime} (${(dailyVol * 100).toFixed(2)}% realized daily vol)`);

  // --- Summary recommendation ---
  console.log("\n  RECOMMENDATION:");
  if (isStableStable && dailyVol < 0.005) {
    console.log("  → Stablecoin pair with minimal vol. Use ±2% range, rebalance if depeg > 1%.");
  } else if (dailyVol < 0.02) {
    console.log("  → Moderate volatility. Use 14d 90% range for LP positioning. Rebalance bi-weekly.");
  } else {
    console.log("  → High volatility. Use 30d 90% range with buffer. Consider wider range or active management.");
  }
}

main().catch(console.error);
```

## Output

```
  SOL/USDC (0.04% fee)
  Address: Czfq3xZZDmsdGdUyrNLtRhGc47cXcZtLG4crryfu44zE
  Current: $148.3200 | TVL: $31.5M

  VOLATILITY PARAMETERS (from 178-day Beachhouse VWAP)
  Realized daily vol: 3.24%
  Daily drift:        -0.082%
  Annualized vol:     61.9%

  ┌─ MONTE CARLO PROJECTION (5000 sims, Beachhouse-derived vol) ─────┐
  │   7d:  5th $    131.42 | 25th $    140.85 | 50th $    147.18 | 75th $    154.62 | 95th $    166.81  │
  │       90% range: $    131.42 — $166.81      (±11.9%)                        │
  │  14d:  5th $    122.10 | 25th $    135.84 | 50th $    146.04 | 75th $    157.95 | 95th $    178.52  │
  │       90% range: $    122.10 — $178.52      (±19.0%)                        │
  │  30d:  5th $    107.38 | 25th $    128.42 | 50th $    144.20 | 75th $    163.71 | 95th $    199.14  │
  │       90% range: $    107.38 — $199.14      (±30.9%)                        │
  │  90d:  5th $     72.84 | 25th $    108.64 | 50th $    138.52 | 75th $    179.41 | 95th $    268.20  │
  │       90% range: $     72.84 — $268.20      (±65.9%)                        │
  └──────────────────────────────────────────────────────────────────┘

  Volatility regime: HIGH (3.24% realized daily vol)

  RECOMMENDATION:
  → High volatility. Use 30d 90% range with buffer. Consider wider range or active management.
```

> Monte Carlo projections use geometric Brownian motion with drift and volatility derived from Beachhouse 6-month daily VWAP prices. Realized volatility (stddev of daily log returns) captures actual price movement including choppy periods that net priceDelta would miss. Outputs are stochastic and vary between runs.
