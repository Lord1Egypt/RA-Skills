# Monitor Pool in Real Time

Poll an Orca Whirlpool at a fixed interval and report price, TVL, and volume changes between each tick.

> **Related playbooks**: [Quick Ranking](../SKILL.md#quick-ranking) for the underlying pool fields, [Stability Analysis](../SKILL.md#stability-analysis) if you need longer-horizon stability instead of short-tick deltas.

## Usage

```bash
npx tsx monitor-pool.ts <pool_address> [interval_sec] [max_polls]
npx tsx monitor-pool.ts Czfq3xZZDmsdGdUyrNLtRhGc47cXcZtLG4crryfu44zE 15 40
```

## Code

```typescript
// monitor-pool.ts

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
  };
}

function pctChange(curr: number, prev: number): string {
  if (prev === 0) return "N/A";
  const delta = ((curr - prev) / prev) * 100;
  return `${delta >= 0 ? "+" : ""}${delta.toFixed(4)}%`;
}

async function monitorPool(
  address: string,
  intervalSec: number,
  maxPolls: number,
): Promise<void> {
  let prev: Pool | null = null;
  let polls = 0;
  let startPrice: number | null = null;

  console.log(`Monitoring pool ${address}`);
  console.log(`Interval: ${intervalSec}s | Max polls: ${maxPolls === Infinity ? "unlimited" : maxPolls}`);
  console.log("-".repeat(100));

  while (polls < maxPolls) {
    try {
      const pool = await orcaFetch<Pool>(`/pools/${address}`);
      const price = Number(pool.price);
      const tvl = Number(pool.tvlUsdc);
      const vol24h = Number(pool.stats["24h"].volume);
      const fees24h = Number(pool.stats["24h"].fees);
      const ts = new Date().toISOString();

      if (startPrice === null) startPrice = price;

      if (prev) {
        const prevPrice = Number(prev.price);
        const prevTvl = Number(prev.tvlUsdc);
        const totalPriceChange = ((price - startPrice) / startPrice) * 100;

        console.log(
          `[${ts}] ${pool.tokenA.symbol}/${pool.tokenB.symbol} | ` +
          `Price: ${pool.price} (${pctChange(price, prevPrice)}, session: ${totalPriceChange >= 0 ? "+" : ""}${totalPriceChange.toFixed(4)}%) | ` +
          `TVL: $${tvl.toLocaleString(undefined, { maximumFractionDigits: 0 })} (${pctChange(tvl, prevTvl)}) | ` +
          `Vol24h: $${vol24h.toLocaleString(undefined, { maximumFractionDigits: 0 })} | ` +
          `Fees24h: $${fees24h.toLocaleString(undefined, { maximumFractionDigits: 0 })}`
        );
      } else {
        console.log(
          `[${ts}] ${pool.tokenA.symbol}/${pool.tokenB.symbol} | ` +
          `Price: ${pool.price} | ` +
          `TVL: $${tvl.toLocaleString(undefined, { maximumFractionDigits: 0 })} | ` +
          `Vol24h: $${vol24h.toLocaleString(undefined, { maximumFractionDigits: 0 })} | ` +
          `Fees24h: $${fees24h.toLocaleString(undefined, { maximumFractionDigits: 0 })} (initial)`
        );
      }

      prev = pool;
      polls++;

      if (polls < maxPolls) {
        await new Promise((r) => setTimeout(r, intervalSec * 1000));
      }
    } catch (err) {
      console.error(`[${new Date().toISOString()}] Error: ${err}`);
      // Wait before retrying
      await new Promise((r) => setTimeout(r, intervalSec * 1000));
      polls++;
    }
  }

  console.log("-".repeat(100));
  console.log(`Monitoring complete. ${polls} polls over ${((polls * intervalSec) / 60).toFixed(1)} minutes.`);

  if (startPrice !== null && prev) {
    const finalPrice = Number(prev.price);
    const totalChange = ((finalPrice - startPrice) / startPrice) * 100;
    console.log(`Session price change: ${totalChange >= 0 ? "+" : ""}${totalChange.toFixed(4)}%`);
  }
}

// --- CLI entry point ---
const address = process.argv[2];
const intervalSec = Number(process.argv[3]) || 30;
// Default to a finite session (60 polls = 30 min at 30s interval). Pass an
// explicit max_polls to override; 0 / non-finite values are rejected so the
// script can't accidentally run forever.
const maxPolls = Number(process.argv[4]) || 60;
if (!Number.isFinite(maxPolls) || maxPolls <= 0) {
  console.error("max_polls must be a positive finite number — unbounded polling is not allowed.");
  process.exit(1);
}

if (!address) {
  console.error("Usage: npx tsx monitor-pool.ts <pool_address> [interval_sec] [max_polls]");
  process.exit(1);
}

// Handle Ctrl+C gracefully
process.on("SIGINT", () => {
  console.log("\nMonitoring stopped by user.");
  process.exit(0);
});

monitorPool(address, intervalSec, maxPolls).catch(console.error);
```

## Output

```
Monitoring pool Czfq3xZZDmsdGdUyrNLtRhGc47cXcZtLG4crryfu44zE
Interval: 30s | Max polls: 5
----------------------------------------------------------------------------------------------------
[2026-04-01T19:36:24Z] SOL/USDC | Price: 84.24 | TVL: $31,756,570 | Vol24h: $281,293,998 | Fees24h: $112,263 (initial)
[2026-04-01T19:36:54Z] SOL/USDC | Price: 84.25 (+0.01%) | TVL: $31,758,102 (+0.00%) | Vol24h: $281,295,000
[2026-04-01T19:37:24Z] SOL/USDC | Price: 84.22 (-0.04%) | TVL: $31,751,300 (-0.02%) | Vol24h: $281,298,000
```

> Output shows real-time price and TVL deltas between polls.

## Tips

- Keep the polling interval at 10 seconds or above to avoid rate limiting.
- `max_polls` defaults to 60 (≈30 min at 30s) and must be a positive finite number. Pass an explicit value to monitor for longer; press Ctrl+C to stop early.
- Session price change tracks the cumulative drift from the first poll -- useful for spotting trends during volatile periods.
