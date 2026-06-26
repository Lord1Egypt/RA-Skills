# Scan Top Orca Pools by TVL

Fetch and display the top 20 Orca Whirlpool pools sorted by TVL.

> **Playbook**: [Quick Ranking](../SKILL.md#quick-ranking) — compute rules, reporting, and gotchas live in SKILL.md.

## Usage

```bash
npx tsx scan-pools.ts
```

## Code

```typescript
// scan-pools.ts

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

async function main() {
  const pools = await orcaFetch<Pool[]>("/pools", {
    orderBy: "tvlUsdc",
    orderDirection: "desc",
    limit: "20",
  });

  console.log("=== Top 20 Orca Whirlpool Pools by TVL ===\n");
  console.log(
    "Rank | Pair            | Fee    | TVL           | Vol 24h        | Fees 24h"
  );
  console.log("-".repeat(85));

  pools.forEach((p, i) => {
    const pair = `${p.tokenA.symbol}/${p.tokenB.symbol}`;
    const feePct = `${(p.feeRate / 10000).toFixed(2)}%`;
    const tvl = `$${Number(p.tvlUsdc).toLocaleString(undefined, { maximumFractionDigits: 0 })}`;
    const vol = `$${Number(p.stats["24h"].volume).toLocaleString(undefined, { maximumFractionDigits: 0 })}`;
    const fees = `$${Number(p.stats["24h"].fees).toLocaleString(undefined, { maximumFractionDigits: 0 })}`;

    console.log(
      `${String(i + 1).padStart(4)} | ${pair.padEnd(15)} | ${feePct.padEnd(6)} | ${tvl.padStart(13)} | ${vol.padStart(14)} | ${fees}`
    );
  });
}

main().catch(console.error);
```

## Output

```
=== Top 20 Orca Whirlpool Pools by TVL ===

Rank | Pair            | Fee    | TVL           | Vol 24h        | Fees 24h
-------------------------------------------------------------------------------------
   1 | SOL/USDC        | 0.04%  |   $31,495,629 |   $293,007,816 | $116,945
   2 | PYUSD/USDC      | 0.01%  |   $23,889,645 |    $46,670,988 | $4,666
   3 | syrupUSDC/USDC  | 0.01%  |   $25,224,434 |    $44,647,533 | $4,464
   4 | cbBTC/USDC      | 0.04%  |    $4,884,592 |    $42,120,072 | $16,826
   5 | SOL/whETH       | 0.05%  |    $7,698,075 |    $32,748,066 | $16,336
   6 | USDG/USDC       | 0.01%  |   $17,142,002 |    $23,772,761 | $2,377
   7 | SOL/cbBTC       | 0.16%  |    $5,191,752 |    $19,441,020 | $30,996
   8 | cbBTC/WBTC      | 0.01%  |    $1,491,065 |    $14,274,311 | $1,429
   9 | SOL/JLP         | 0.04%  |    $2,439,448 |     $8,851,211 | $3,535
  10 | SOL/WBTC        | 0.05%  |    $1,447,778 |     $8,266,617 | $4,126
```

> Representative output. Live values update from the Orca API at request time.

## curl Fallback

```bash
curl -s "https://api.orca.so/v2/solana/pools?orderBy=tvlUsdc&orderDirection=desc&limit=20" | \
  npx tsx -e "
    import { readFileSync } from 'node:fs';
    const pools = JSON.parse(readFileSync(0, 'utf8'));
    pools.forEach((p:any, i:number) => {
      const fee = (p.feeRate/10000).toFixed(2);
      console.log(\`\${i+1}. \${p.tokenA.symbol}/\${p.tokenB.symbol} (\${fee}%) TVL: \$\${Number(p.tvlUsdc).toLocaleString()}\`);
    });
  "
```
