# Pair Discovery: Find All Pools for a Token

Find every Orca Whirlpool pool containing a given token, grouped by trading pair and sorted by TVL.

> **Playbook**: [Quick Ranking](../SKILL.md#quick-ranking) — token-centric variant (all pools for one mint).

## Usage

```bash
npx tsx pair-discovery.ts
```

To search for a different token, change the `TOKEN` constant or pass it as a CLI argument:

```bash
npx tsx pair-discovery.ts BONK
```

## Code

```typescript
// pair-discovery.ts

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
  stats: {
    "24h": { volume: string; fees: string };
    "7d": { volume: string; fees: string };
    "30d": { volume: string; fees: string };
  };
}

interface PairGroup {
  pair: string;
  otherToken: string;
  pools: Pool[];
  totalTvl: number;
  totalVol24h: number;
}

async function discoverPools(token: string): Promise<PairGroup[]> {
  // Search by token symbol -- use a high limit to catch all pools
  const pools = await orcaFetch<Pool[]>("/pools/search", {
    query: token,
    limit: "50",
  });

  // Filter to pools that actually contain the target token
  const matching = pools.filter(
    (p) =>
      p.tokenA.symbol.toUpperCase() === token.toUpperCase() ||
      p.tokenB.symbol.toUpperCase() === token.toUpperCase()
  );

  // Group by trading pair
  const pairMap = new Map<string, Pool[]>();
  for (const p of matching) {
    const isTokenA = p.tokenA.symbol.toUpperCase() === token.toUpperCase();
    const other = isTokenA ? p.tokenB.symbol : p.tokenA.symbol;
    const key = `${token.toUpperCase()}/${other}`;
    if (!pairMap.has(key)) pairMap.set(key, []);
    pairMap.get(key)!.push(p);
  }

  // Build pair groups with aggregates
  const groups: PairGroup[] = [...pairMap.entries()].map(([pair, pools]) => ({
    pair,
    otherToken: pair.split("/")[1],
    pools: pools.sort((a, b) => a.feeRate - b.feeRate),
    totalTvl: pools.reduce((s, p) => s + Number(p.tvlUsdc), 0),
    totalVol24h: pools.reduce((s, p) => s + Number(p.stats["24h"].volume), 0),
  }));

  // Sort by total TVL descending
  groups.sort((a, b) => b.totalTvl - a.totalTvl);

  return groups;
}

async function main() {
  const TOKEN = process.argv[2] || "SOL";

  console.log(`\n=== Discovering All ${TOKEN} Pools on Orca ===\n`);

  const groups = await discoverPools(TOKEN);

  if (groups.length === 0) {
    console.log(`No pools found containing ${TOKEN}`);
    return;
  }

  const totalPools = groups.reduce((s, g) => s + g.pools.length, 0);
  const totalTvl = groups.reduce((s, g) => s + g.totalTvl, 0);

  console.log(`Found ${totalPools} pools across ${groups.length} pairs`);
  console.log(`Combined TVL: $${totalTvl.toLocaleString()}\n`);

  // Summary table
  console.log("Pair              | Tiers | Combined TVL    | Vol 24h");
  console.log("-".repeat(70));

  for (const g of groups) {
    console.log(
      `${g.pair.padEnd(17)} | ` +
      `${String(g.pools.length).padStart(5)} | ` +
      `$${g.totalTvl.toLocaleString(undefined, { maximumFractionDigits: 0 }).padStart(14)} | ` +
      `$${g.totalVol24h.toLocaleString(undefined, { maximumFractionDigits: 0 })}`
    );
  }

  // Detailed breakdown for top pairs
  const topPairs = groups.slice(0, 5);

  for (const g of topPairs) {
    console.log(`\n--- ${g.pair} (${g.pools.length} fee tier(s)) ---\n`);
    console.log("  Fee Tier  | TVL            | Vol 24h         | Fees 24h    | Address");
    console.log("  " + "-".repeat(95));

    for (const p of g.pools) {
      const feePct = (p.feeRate / 10000).toFixed(2) + "%";
      const tvl = Number(p.tvlUsdc);
      const vol = Number(p.stats["24h"].volume);
      const fees = Number(p.stats["24h"].fees);

      console.log(
        `  ${feePct.padEnd(9)} | ` +
        `$${tvl.toLocaleString(undefined, { maximumFractionDigits: 0 }).padStart(13)} | ` +
        `$${vol.toLocaleString(undefined, { maximumFractionDigits: 0 }).padStart(14)} | ` +
        `$${fees.toLocaleString(undefined, { maximumFractionDigits: 0 }).padStart(10)} | ` +
        `${p.address}`
      );
    }
  }

  if (groups.length > 5) {
    console.log(`\n... and ${groups.length - 5} more pairs (use higher limit for full results)`);
  }
}

main().catch(console.error);
```

## Output

```
=== Discovering All SOL Pools on Orca ===

Found 23 pools across 20 pairs
Combined TVL: $68,407,032

Pair              | Tiers | Combined TVL    | Vol 24h
----------------------------------------------------------------------
SOL/USDC          |     2 | $    31,716,029 | $293,614,403
SOL/whETH         |     1 | $     7,698,075 | $32,748,066
SOL/JitoSOL       |     1 | $     7,129,850 | $7,019,441
SOL/cbBTC         |     2 | $     5,260,723 | $20,522,181
SOL/USDG          |     1 | $     4,630,774 | $2,938,793
SOL/JLP           |     1 | $     2,439,448 | $8,851,211
SOL/PUMP          |     2 | $     2,357,445 | $4,381,989
SOL/WBTC          |     1 | $     1,447,778 | $8,266,617
SOL/Fartcoin      |     1 | $     1,432,655 | $5,670,978
...

--- SOL/USDC (2 fee tier(s)) ---
  0.02%  | $220,400   | $606,587    | $121     | FpCMFDFG...
  0.04%  | $31,495,629 | $293,007,816 | $116,945 | Czfq3xZZ...
```

> Representative output.

## Searching by Mint Address

For tokens with common or ambiguous symbols, use the mint address directly:

```typescript
// Find all BONK pools by mint address
const BONK_MINT = "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263";

const pools = await orcaFetch<Pool[]>("/pools/search", {
  query: BONK_MINT,
  limit: "50",
});

// All results will contain BONK -- no symbol filtering needed
for (const p of pools) {
  const feePct = (p.feeRate / 10000).toFixed(2);
  console.log(
    `${p.tokenA.symbol}/${p.tokenB.symbol} (${feePct}%) | ` +
    `TVL: $${Number(p.tvlUsdc).toLocaleString()} | ${p.address}`
  );
}
```

## curl Fallback

```bash
curl -s "https://api.orca.so/v2/solana/pools/search?query=SOL&limit=50" | \
  npx tsx -e "
    import { readFileSync } from 'node:fs';
    const pools = JSON.parse(readFileSync(0, 'utf8'));
    const sol = pools.filter((p:any) => p.tokenA.symbol==='SOL' || p.tokenB.symbol==='SOL');
    const pairs = new Map<string, any[]>();
    for (const p of sol) {
      const other = p.tokenA.symbol === 'SOL' ? p.tokenB.symbol : p.tokenA.symbol;
      const key = \`SOL/\${other}\`;
      if (!pairs.has(key)) pairs.set(key, []);
      pairs.get(key)!.push(p);
    }
    for (const [pair, pools] of [...pairs.entries()].sort((a,b) =>
      b[1].reduce((s:number,p:any) => s+Number(p.tvlUsdc),0) -
      a[1].reduce((s:number,p:any) => s+Number(p.tvlUsdc),0)
    )) {
      const tvl = pools.reduce((s:number,p:any) => s+Number(p.tvlUsdc),0);
      console.log(\`\${pair} (\${pools.length} tiers) TVL: \$\${tvl.toLocaleString()}\`);
      for (const p of pools) {
        console.log(\`  \${(p.feeRate/10000).toFixed(2)}% | \${p.address}\`);
      }
    }
  "
```
