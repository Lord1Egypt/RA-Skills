# Pool Detail and Fee APR

Fetch detailed info for a single Orca Whirlpool and compute annualized fee APR across 24h, 7d, and 30d windows.

> **Playbook**: [Quick Ranking](../SKILL.md#quick-ranking) — single-pool variant. See SKILL.md for APR formula and caveats.

## Usage

```bash
npx tsx pool-detail.ts <pool_address>
npx tsx pool-detail.ts Czfq3xZZDmsdGdUyrNLtRhGc47cXcZtLG4crryfu44zE
```

## Code

```typescript
// pool-detail.ts

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
  tickCurrentIndex: number;
  liquidity: string;
  tokenA: { symbol: string; name: string; decimals: number };
  tokenB: { symbol: string; name: string; decimals: number };
  tokenMintA: string;
  tokenMintB: string;
  tokenBalanceA: string;
  tokenBalanceB: string;
  price: string;
  tvlUsdc: string;
  yieldOverTvl: string;
  poolType: string;
  stats: {
    "24h": { volume: string; fees: string; rewards: string; yieldOverTvl: string };
    "7d": { volume: string; fees: string };
    "30d": { volume: string; fees: string };
  };
}

function computeFeeAPR(pool: Pool) {
  const tvl = Number(pool.tvlUsdc);
  if (tvl === 0) return { apr24h: 0, apr7d: 0, apr30d: 0 };

  const fees24h = Number(pool.stats["24h"].fees);
  const fees7d = Number(pool.stats["7d"].fees);
  const fees30d = Number(pool.stats["30d"].fees);

  return {
    apr24h: (fees24h / tvl) * 365 * 100,
    apr7d: (fees7d / 7 / tvl) * 365 * 100,
    apr30d: (fees30d / 30 / tvl) * 365 * 100,
  };
}

async function main() {
  const address = process.argv[2];
  if (!address) {
    console.error("Usage: npx tsx pool-detail.ts <pool_address>");
    process.exit(1);
  }

  const pool = await orcaFetch<Pool>(`/pools/${address}`);
  const feePct = pool.feeRate / 10000;
  const balA = Number(pool.tokenBalanceA) / 10 ** pool.tokenA.decimals;
  const balB = Number(pool.tokenBalanceB) / 10 ** pool.tokenB.decimals;
  const apr = computeFeeAPR(pool);

  console.log(`=== Pool Detail ===\n`);
  console.log(`Address:        ${pool.address}`);
  console.log(`Pair:           ${pool.tokenA.symbol}/${pool.tokenB.symbol}`);
  console.log(`Pool Type:      ${pool.poolType}`);
  console.log(`Fee:            ${feePct}% (feeRate: ${pool.feeRate})`);
  console.log(`Tick Spacing:   ${pool.tickSpacing}`);
  console.log(`Current Tick:   ${pool.tickCurrentIndex}`);
  console.log(`Price:          ${pool.price} ${pool.tokenB.symbol} per ${pool.tokenA.symbol}`);
  console.log(`TVL:            $${Number(pool.tvlUsdc).toLocaleString()}`);
  console.log(`Liquidity:      ${pool.liquidity}`);
  console.log();
  console.log(`--- Token Balances ---`);
  console.log(`${pool.tokenA.symbol}:  ${balA.toLocaleString()} (mint: ${pool.tokenMintA})`);
  console.log(`${pool.tokenB.symbol}:  ${balB.toLocaleString()} (mint: ${pool.tokenMintB})`);
  console.log();
  console.log(`--- Volume & Fees ---`);
  console.log(`24h Volume:     $${Number(pool.stats["24h"].volume).toLocaleString()}`);
  console.log(`24h Fees:       $${Number(pool.stats["24h"].fees).toLocaleString()}`);
  console.log(`7d Volume:      $${Number(pool.stats["7d"].volume).toLocaleString()}`);
  console.log(`7d Fees:        $${Number(pool.stats["7d"].fees).toLocaleString()}`);
  console.log(`30d Volume:     $${Number(pool.stats["30d"].volume).toLocaleString()}`);
  console.log(`30d Fees:       $${Number(pool.stats["30d"].fees).toLocaleString()}`);
  console.log();
  console.log(`--- Fee APR (annualized) ---`);
  console.log(`24h APR:        ${apr.apr24h.toFixed(2)}%`);
  console.log(`7d avg APR:     ${apr.apr7d.toFixed(2)}%`);
  console.log(`30d avg APR:    ${apr.apr30d.toFixed(2)}%`);

  // Sustainability check
  if (apr.apr24h > apr.apr30d * 3) {
    console.log(`\n[WARNING] 24h APR is ${(apr.apr24h / apr.apr30d).toFixed(1)}x the 30d average -- likely a transient volume spike.`);
  }
}

main().catch(console.error);
```

## Output

```
=== Pool Detail ===

Address:        Czfq3xZZDmsdGdUyrNLtRhGc47cXcZtLG4crryfu44zE
Pair:           SOL/USDC
Pool Type:      whirlpool
Fee:            0.04% (feeRate: 400)
Tick Spacing:   4
Current Tick:   -24870
Price:          83.18 USDC per SOL
TVL:            $31,495,629
Liquidity:      941888392134818

--- Token Balances ---
SOL:  290,602.472 (mint: So11...112)
USDC:  7,324,042.317 (mint: EPjF...t1v)

--- Volume & Fees ---
24h Volume:     $293,007,816
24h Fees:       $116,945
7d Volume:      $940,134,039
7d Fees:        $375,745
30d Volume:     $4,222,866,729
30d Fees:       $1,688,599

--- Fee APR (annualized) ---
24h APR:        135.53%
7d avg APR:     62.21%
30d avg APR:    65.23%
```

> Representative output.

## curl Fallback

```bash
curl -s "https://api.orca.so/v2/solana/pools/Czfq3xZZDmsdGdUyrNLtRhGc47cXcZtLG4crryfu44zE"
```
