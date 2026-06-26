# Compare Fee Tiers for a Token Pair

Fetch all SOL/USDC pools on Orca and compare price, TVL, volume, and APR across fee tiers.

> **Playbook**: [Fee Tier Comparison](../SKILL.md#fee-tier-comparison) — compute rules, reporting, and gotchas live in SKILL.md.

## Usage

```bash
npx tsx compare-fee-tiers.ts
```

## Code

```typescript
// compare-fee-tiers.ts

const ORCA_BASE = "https://api.orca.so/v2/solana";

async function orcaFetch<T>(path: string, params?: Record<string, string>): Promise<T> {
  const url = new URL(`${ORCA_BASE}${path}`);
  if (params) {
    Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v));
  }
  const res = await fetch(url.toString(), {
    headers: { "Accept": "application/json" },
  });
  if (!res.ok) throw new Error(`Orca API ${res.status}: ${await res.text()}`);
  const json = await res.json();
  // Orca API wraps responses in { data: T } — unwrap automatically
  return (json.data ?? json) as T;
}

interface Pool {
  address: string;
  feeRate: number;
  tickSpacing: number;
  tokenA: { symbol: string; decimals: number };
  tokenB: { symbol: string; decimals: number };
  price: string;
  tvlUsdc: string;
  liquidity: string;
  tokenBalanceA: string;
  tokenBalanceB: string;
  yieldOverTvl: string;
  stats: {
    "24h": { volume: string; fees: string };
    "7d": { volume: string; fees: string };
    "30d": { volume: string; fees: string };
  };
}

function computeAPR(pool: Pool): { apr24h: number; apr7d: number; apr30d: number } {
  const tvl = Number(pool.tvlUsdc);
  if (tvl === 0) return { apr24h: 0, apr7d: 0, apr30d: 0 };
  return {
    apr24h: (Number(pool.stats["24h"].fees) / tvl) * 365 * 100,
    apr7d: (Number(pool.stats["7d"].fees) / 7 / tvl) * 365 * 100,
    apr30d: (Number(pool.stats["30d"].fees) / 30 / tvl) * 365 * 100,
  };
}

async function main() {
  const PAIR = "SOL/USDC";
  const [symbolA, symbolB] = PAIR.split("/");

  // 1. Fetch all pools for the pair
  const pools = await orcaFetch<Pool[]>("/pools/search", {
    query: PAIR,
    limit: "20",
  });

  // 2. Filter to exact pair match
  const matched = pools.filter(
    (p) =>
      (p.tokenA.symbol === symbolA && p.tokenB.symbol === symbolB) ||
      (p.tokenA.symbol === symbolB && p.tokenB.symbol === symbolA)
  );

  if (matched.length === 0) {
    console.log(`No pools found for ${PAIR}`);
    return;
  }

  // 3. Sort by fee rate
  matched.sort((a, b) => a.feeRate - b.feeRate);

  // 4. Compute totals
  const totalTvl = matched.reduce((s, p) => s + Number(p.tvlUsdc), 0);
  const totalVol24h = matched.reduce((s, p) => s + Number(p.stats["24h"].volume), 0);

  console.log(`\n=== ${PAIR} Fee Tier Comparison ===`);
  console.log(`Found ${matched.length} pools | Combined TVL: $${totalTvl.toLocaleString()}\n`);

  // 5. Print comparison table
  console.log(
    "Fee Tier  | Price       | TVL            | TVL %   | Vol 24h         | Vol %   | APR (7d)"
  );
  console.log("-".repeat(100));

  for (const p of matched) {
    const feePct = (p.feeRate / 10000).toFixed(2) + "%";
    const tvl = Number(p.tvlUsdc);
    const vol24h = Number(p.stats["24h"].volume);
    const tvlShare = totalTvl > 0 ? (tvl / totalTvl) * 100 : 0;
    const volShare = totalVol24h > 0 ? (vol24h / totalVol24h) * 100 : 0;
    const apr = computeAPR(p);

    // Normalize price direction
    const price = p.tokenA.symbol === symbolA ? Number(p.price) : 1 / Number(p.price);

    console.log(
      `${feePct.padEnd(9)} | ` +
      `$${price.toFixed(2).padStart(9)} | ` +
      `$${tvl.toLocaleString(undefined, { maximumFractionDigits: 0 }).padStart(13)} | ` +
      `${tvlShare.toFixed(1).padStart(5)}%  | ` +
      `$${vol24h.toLocaleString(undefined, { maximumFractionDigits: 0 }).padStart(14)} | ` +
      `${volShare.toFixed(1).padStart(5)}%  | ` +
      `${apr.apr7d.toFixed(2)}%`
    );
  }

  // 6. Price spread analysis
  const prices = matched
    .filter((p) => Number(p.tvlUsdc) > 1000)
    .map((p) => ({
      feeRate: p.feeRate,
      price: p.tokenA.symbol === symbolA ? Number(p.price) : 1 / Number(p.price),
    }));

  if (prices.length >= 2) {
    const minPrice = Math.min(...prices.map((x) => x.price));
    const maxPrice = Math.max(...prices.map((x) => x.price));
    const spreadBps = ((maxPrice - minPrice) / minPrice) * 10000;

    console.log(`\nPrice Spread: ${spreadBps.toFixed(2)} bps across ${prices.length} active tiers`);
  }

  // 7. Recommendations
  const viable = matched.filter((p) => Number(p.tvlUsdc) > 10_000);
  if (viable.length > 0) {
    const bestForLP = viable.reduce((best, p) => {
      const aprP = computeAPR(p).apr7d;
      const aprBest = computeAPR(best).apr7d;
      return aprP > aprBest ? p : best;
    });
    const bestForTrade = viable.reduce((best, p) =>
      p.feeRate < best.feeRate ? p : best
    );

    console.log(`\nRecommendations:`);
    console.log(
      `  Best for LP:      ${(bestForLP.feeRate / 10000).toFixed(2)}% tier ` +
      `(APR: ${computeAPR(bestForLP).apr7d.toFixed(2)}%, TVL: $${Number(bestForLP.tvlUsdc).toLocaleString()})`
    );
    console.log(
      `  Best for trading: ${(bestForTrade.feeRate / 10000).toFixed(2)}% tier ` +
      `(lowest fee with $${Number(bestForTrade.tvlUsdc).toLocaleString()} TVL)`
    );
  }
}

main().catch(console.error);
```

## Output

```
=== SOL/USDC Fee Tier Comparison ===
Found 2 pools | Combined TVL: $31,716,029

Fee Tier  | Price       | TVL            | TVL %   | Vol 24h         | Vol %   | APR (7d)
----------------------------------------------------------------------------------------------------
0.02%     | $    83.20 | $      220,400 |   0.7%  | $       606,587 |   0.2%  | 12.75%
0.04%     | $    83.18 | $   31,495,629 |  99.3%  | $   293,007,816 |  99.8%  | 62.21%

Price Spread: 2.48 bps across 2 active tiers

Recommendations:
  Best for LP:      0.04% tier (APR: 62.21%, TVL: $31,495,629)
  Best for trading: 0.02% tier (lowest fee with $220,400 TVL)
```

> Representative output.

## curl Fallback

```bash
curl -s "https://api.orca.so/v2/solana/pools/search?query=SOL/USDC&limit=20" | \
  npx tsx -e "
    import { readFileSync } from 'node:fs';
    const pools = JSON.parse(readFileSync(0, 'utf8'));
    const matched = pools.filter((p:any) =>
      (p.tokenA.symbol==='SOL' && p.tokenB.symbol==='USDC') ||
      (p.tokenA.symbol==='USDC' && p.tokenB.symbol==='SOL')
    );
    matched.sort((a:any,b:any) => a.feeRate - b.feeRate);
    for (const p of matched) {
      const fee = (p.feeRate/10000).toFixed(2);
      const tvl = Number(p.tvlUsdc).toLocaleString();
      const vol = Number(p.stats['24h'].volume).toLocaleString();
      console.log(\`\${fee}% | TVL: \$\${tvl} | Vol24h: \$\${vol} | Price: \${p.price}\`);
    }
  "
```
