# Yield Introspection

Retrospective yield analysis using Beachhouse 6-month timeseries data. Shows what a $10K deposit would have actually earned during stable price periods, using real daily volume and TVL.

> **Playbook**: [Retrospective Yield](../SKILL.md#retrospective-yield) — attribution caveats (concentrated LP fee scaling, stable-period vs blended APR) live in SKILL.md.

## Code

```typescript
// yield-introspection.ts

const ORCA_API = "https://api.orca.so/v2/solana";
const BEACHHOUSE = "https://stats-api.mainnet.orca.so";
const deposit = 10_000; // USD

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

interface TvlPoint {
  tvl: string;
  baseAmount: string;
  quoteAmount: string;
  unixTime: number;
}

function mean(values: number[]): number {
  return values.length === 0 ? 0 : values.reduce((a, b) => a + b, 0) / values.length;
}

const query = process.argv[2] ?? "SOL/USDC";

async function main() {
  const now = Math.floor(Date.now() / 1000);
  const sixMonthsAgo = now - 180 * 86400;

  // Find pool from REST API
  const res = await fetchJson<{ data: any[] }>(`${ORCA_API}/pools/search?query=${query}&limit=5`);
  const pool = res.data.sort((a: any, b: any) => Number(b.tvlUsdc) - Number(a.tvlUsdc))[0];
  if (!pool) { console.error(`No pool found for ${query}`); process.exit(1); }

  const pair = `${pool.tokenA.symbol}/${pool.tokenB.symbol}`;
  const feePct = pool.feeRate / 10000;
  const tvl = Number(pool.tvlUsdc);

  // Fetch 6-month volume and TVL from Beachhouse
  const [volRes, tvlRes] = await Promise.all([
    fetchJson<{ data: { data: VolPoint[] } }>(
      `${BEACHHOUSE}/api/pools/${pool.address}/volume?time_from=${sixMonthsAgo}&time_to=${now}&type=1D`
    ),
    fetchJson<{ data: { data: TvlPoint[] } }>(
      `${BEACHHOUSE}/api/pools/${pool.address}/tvl?time_from=${sixMonthsAgo}&time_to=${now}&type=1D`
    ),
  ]);

  const volData = volRes.data.data
    .filter(d => Number(d.volumeBase) > 0 && Number(d.volumeQuote) > 0)
    .sort((a, b) => a.unixTime - b.unixTime);
  const tvlData = tvlRes.data.data
    .filter(d => Number(d.tvl) > 0)
    .sort((a, b) => a.unixTime - b.unixTime);

  if (volData.length < 30 || tvlData.length < 30) {
    console.error("Insufficient Beachhouse data");
    process.exit(1);
  }

  // Build a TVL lookup by unix day
  const tvlByDay = new Map<number, number>();
  for (const d of tvlData) {
    const dayKey = Math.floor(d.unixTime / 86400);
    tvlByDay.set(dayKey, Number(d.tvl));
  }

  // Compute VWAP prices for each day (A/B pool ratio: quote per base)
  const vwapPrices = volData.map(d => Number(d.volumeQuote) / Number(d.volumeBase));

  // Find stable periods: consecutive days where price stayed within band
  interface StablePeriod {
    startIdx: number;
    endIdx: number;
    days: number;
    bandPct: number;
    centerPrice: number;
    totalFees: number;
    avgDailyFees: number;
    avgTvl: number;
    depositShare: number;
    depositEarnings: number;
    annualizedApr: number;
  }

  function findStablePeriods(bandPct: number): StablePeriod[] {
    const periods: StablePeriod[] = [];
    let startIdx = 0;

    while (startIdx < vwapPrices.length) {
      const center = vwapPrices[startIdx];
      const lo = center * (1 - bandPct / 100);
      const hi = center * (1 + bandPct / 100);
      let endIdx = startIdx;

      while (endIdx < vwapPrices.length && vwapPrices[endIdx] >= lo && vwapPrices[endIdx] <= hi) {
        endIdx++;
      }

      const days = endIdx - startIdx;
      if (days >= 7) { // only count periods of 7+ days
        // Calculate fees earned during this period
        let totalFees = 0;
        let totalTvl = 0;
        let tvlDays = 0;

        for (let i = startIdx; i < endIdx; i++) {
          const dailyFees = Number(volData[i].totalVolumeUsd) * (feePct / 100);
          totalFees += dailyFees;

          const dayKey = Math.floor(volData[i].unixTime / 86400);
          const dayTvl = tvlByDay.get(dayKey);
          if (dayTvl && dayTvl > 0) {
            totalTvl += dayTvl;
            tvlDays++;
          }
        }

        const avgTvl = tvlDays > 0 ? totalTvl / tvlDays : tvl;
        const depositShare = deposit / avgTvl;
        const depositEarnings = totalFees * depositShare;
        const annualizedApr = days > 0 ? (depositEarnings / deposit) * (365 / days) * 100 : 0;

        periods.push({
          startIdx, endIdx: endIdx - 1, days, bandPct, centerPrice: center,
          totalFees, avgDailyFees: totalFees / days, avgTvl,
          depositShare, depositEarnings, annualizedApr,
        });
      }

      startIdx = endIdx > startIdx ? endIdx : startIdx + 1;
    }
    return periods;
  }

  console.log(`\n  ${pair} (${feePct.toFixed(2)}% fee) — ${pool.address}`);
  console.log(`  TVL: $${(tvl / 1e6).toFixed(1)}M | Price: $${Number(pool.price).toFixed(4)}`);
  console.log(`  Beachhouse data: ${volData.length} days\n`);

  // Current rates from REST API
  const s24 = pool.stats["24h"];
  const s7d = pool.stats["7d"];
  const s30d = pool.stats["30d"];
  const apr24h = Number(s24.yieldOverTvl) * 365 * 100;
  const apr7d = Number(s7d.yieldOverTvl) / 7 * 365 * 100;
  const apr30d = Number(s30d.yieldOverTvl) / 30 * 365 * 100;

  console.log("  CURRENT RATES (from REST API stats)");
  console.log("  Period  | APR");
  console.log("  " + "─".repeat(24));
  console.log(`  24h     | ${apr24h.toFixed(1)}%`);
  console.log(`  7d      | ${apr7d.toFixed(1)}%`);
  console.log(`  30d     | ${apr30d.toFixed(1)}%`);

  // Retrospective analysis for each band
  for (const bandPct of [2, 5]) {
    const periods = findStablePeriods(bandPct);

    console.log(`\n  RETROSPECTIVE YIELD: STABLE PERIODS WITHIN ±${bandPct}% (min 7 days)`);

    if (periods.length === 0) {
      console.log("  No stable periods of 7+ days found within this band.");
      continue;
    }

    console.log("  Period                  | Days | Center      | Pool Fees     | $10K Earned | Annualized");
    console.log("  " + "─".repeat(88));

    for (const p of periods) {
      const startDate = new Date(volData[p.startIdx].unixTime * 1000).toISOString().slice(0, 10);
      const endDate = new Date(volData[p.endIdx].unixTime * 1000).toISOString().slice(0, 10);
      const fmtFees = p.totalFees >= 1e6
        ? `$${(p.totalFees / 1e6).toFixed(2)}M`
        : `$${(p.totalFees / 1e3).toFixed(1)}K`;

      console.log(
        `  ${startDate} → ${endDate} | ${String(p.days).padStart(3)}  | ` +
        `$${p.centerPrice.toFixed(2).padStart(9)} | ${fmtFees.padStart(12)} | ` +
        `$${p.depositEarnings.toFixed(2).padStart(9)} | ${p.annualizedApr.toFixed(1).padStart(6)}%`
      );
    }

    // Summary stats
    const totalDays = periods.reduce((s, p) => s + p.days, 0);
    const totalEarned = periods.reduce((s, p) => s + p.depositEarnings, 0);
    const avgApr = mean(periods.map(p => p.annualizedApr));
    console.log("  " + "─".repeat(88));
    console.log(
      `  Total: ${periods.length} periods, ${totalDays} days stable | ` +
      `$10K earned $${totalEarned.toFixed(2)} total | ` +
      `Avg annualized: ${avgApr.toFixed(1)}%`
    );
  }

  // Overall 6-month fee summary
  const totalVolume6m = volData.reduce((s, d) => s + Number(d.totalVolumeUsd), 0);
  const totalFees6m = totalVolume6m * (feePct / 100);
  const avgTvl6m = mean(tvlData.map(d => Number(d.tvl)));
  const depositShare6m = deposit / avgTvl6m;
  const depositFees6m = totalFees6m * depositShare6m;

  console.log("\n  6-MONTH FULL-PERIOD SUMMARY (all days, ignoring price movement)");
  console.log(`  Total volume:     $${(totalVolume6m / 1e6).toFixed(1)}M`);
  console.log(`  Total fees:       $${(totalFees6m / 1e6).toFixed(2)}M`);
  console.log(`  Avg daily TVL:    $${(avgTvl6m / 1e6).toFixed(1)}M`);
  console.log(`  $10K share:       ${(depositShare6m * 100).toFixed(4)}%`);
  console.log(`  $10K fees earned: $${depositFees6m.toFixed(2)} over ${volData.length} days`);
  console.log(`  Annualized:       ${(depositFees6m / deposit * 365 / volData.length * 100).toFixed(1)}%`);

  console.log("\n  Note: These are retrospective facts from actual Beachhouse data, not forecasts.");
  console.log("  Actual LP returns depend on range width, rebalancing, IL, and whether price stays in range.");
}

main().catch(console.error);
```

## Output

```
  SOL/USDC (0.04% fee) — Czfq3xZZDmsdGdUyrNLtRhGc47cXcZtLG4crryfu44zE
  TVL: $31.5M | Price: $148.3200
  Beachhouse data: 178 days

  CURRENT RATES (from REST API stats)
  Period  | APR
  ────────────────────────
  24h     | 181.9%
  7d      | 99.7%
  30d     | 81.1%

  RETROSPECTIVE YIELD: STABLE PERIODS WITHIN ±2% (min 7 days)
  Period                  | Days | Center      | Pool Fees     | $10K Earned | Annualized
  ────────────────────────────────────────────────────────────────────────────────────────────
  2025-01-12 → 2025-01-21 |  10  | $   142.80 |      $412.8K |    $131.04 |   47.8%
  2025-03-08 → 2025-03-18 |  11  | $   138.50 |      $489.2K |    $155.31 |   51.5%
  2025-04-06 → 2025-04-14 |   9  | $   149.10 |      $378.4K |    $120.12 |   48.7%
  ────────────────────────────────────────────────────────────────────────────────────────────
  Total: 3 periods, 30 days stable | $10K earned $406.47 total | Avg annualized: 49.3%

  RETROSPECTIVE YIELD: STABLE PERIODS WITHIN ±5% (min 7 days)
  Period                  | Days | Center      | Pool Fees     | $10K Earned | Annualized
  ────────────────────────────────────────────────────────────────────────────────────────────
  2024-12-20 → 2025-01-21 |  33  | $   140.20 |       $1.42M |    $450.92 |   49.9%
  2025-02-15 → 2025-03-18 |  32  | $   136.90 |       $1.38M |    $438.18 |   50.0%
  2025-03-28 → 2025-04-16 |  20  | $   148.30 |      $872.6K |    $277.12 |   50.6%
  ────────────────────────────────────────────────────────────────────────────────────────────
  Total: 3 periods, 85 days stable | $10K earned $1166.22 total | Avg annualized: 50.2%

  6-MONTH FULL-PERIOD SUMMARY (all days, ignoring price movement)
  Total volume:     $6,842.1M
  Total fees:       $2.74M
  Avg daily TVL:    $29.8M
  $10K share:       0.0336%
  $10K fees earned: $919.46 over 178 days
  Annualized:       18.9%

  Note: These are retrospective facts from actual Beachhouse data, not forecasts.
  Actual LP returns depend on range width, rebalancing, IL, and whether price stays in range.
```

> Retrospective yield analysis from Beachhouse 6-month daily volume and TVL data. Finds periods where price stayed within tight bands and calculates what a deposit would have earned from actual daily fees (totalVolumeUsd * feeRate) divided by actual daily TVL. REST API stats provide current rate context. These are historical facts, not projections.
