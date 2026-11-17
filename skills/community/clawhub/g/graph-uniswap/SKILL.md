---
name: graph-uniswap
description: "Simulate a Uniswap swap before making it — amount out, effective price, price impact — computed offline from The Graph with the protocol's own concentrated-liquidity math. Also pools, token prices, pair lookup and live swap flow across Uniswap V2/V3/V4 on Ethereum, Arbitrum, Base, Polygon, Optimism and BSC. Trigger keywords: uniswap, swap, quote, price impact, slippage, how much would I get, pool, liquidity, fee tier, LP, DEX, token price, V3, V4."
version: 0.3.3
homepage: https://github.com/PaulieB14/graph-uniswap-mcp
metadata:
  clawdbot:
    emoji: "🦄"
---

# Graph Uniswap

Answer Uniswap questions with live subgraph data — and, uniquely, answer *"what would this
trade actually cost me?"* without an RPC, a node, or a private key.

## Setup

Needs a free Graph API key (<https://thegraph.com/studio>, 100k queries/month free) in
`GRAPH_API_KEY`. The server runs over stdio via `npx -y graph-uniswap-mcp`.

## Picking a tool

| The user is asking… | Use |
|---|---|
| "how much would I get for X", "what's the slippage/price impact", "is this pool deep enough" | `quote_swap` |
| "what's WETH worth", "price of X" | `get_token_price` |
| "best pools on <chain>", "most active pools" | `top_pools` |
| "the USDC/WETH pool", "which fee tier" | `find_pool` |
| "stats for this pool" | `pool_info` |
| "recent trades", "who is trading" | `recent_swaps` |
| "what chains/versions are supported" | `list_markets` |
| anything the above cannot express | `raw_query` |

Typical flow for a trade question: `find_pool` → pick the pool → `quote_swap`.

## quote_swap — the one to reach for

Simulates an exact-input swap against the pool's real tick liquidity.

```
quote_swap  pool=0x8ad5…e6d8  tokenIn=WETH  amountIn=100  chain=ethereum  version=v3
→ amount_out 223661.14 USDC · effective_price 2236.61 · price_impact_pct 0.6291 · ticks_crossed 2
```

`price_impact_pct` is measured against the fee-adjusted spot, so it isolates depth rather than
restating the fee. `fee_pct` is reported separately.

**Always check `quotable`.** When it is `false`, report the `reason` — do not substitute a guess
or fall back to a TVL figure. It refuses on:

- **V4 pools with a hook** — hooks can override fee and curve, so vanilla math would be wrong.
  On Base the top V4 pools by volume are hook-driven.
- **Trades bigger than the visible liquidity** — you get `lower_bound_amount_out`, not a quote.
  Suggest splitting the trade, or quoting on-chain.
- **Zero in-range liquidity**, or a deployment exposing no `ticks` (V3 on Base).

The number simulates the most recently indexed block. Real execution depends on state at
inclusion — say so when the amount is material. It is single-pool: not a router, no multi-hop,
no splitting.

## TVL is null on purpose — do not work around it

`tvl_usd` is `null` for V3/V4. Uniswap's native subgraphs accumulate `totalValueLockedUSD` from
per-event deltas and it drifts: on the canonical USDC/WETH 0.3% pool it read 138.9M USDC against
6.1M actually held on chain (22.7x high, on a blue-chip pool). V2 `reserve0`/`reserve1` are real
balances and are still returned.

If a user asks how deep a pool is, **run `quote_swap` at their size** — that is the truthful
answer. Never reconstruct a TVL estimate from `raw_query` and present it as fact.

## Other things worth knowing

- Rank pools by **volume, never TVL** — one spam-token pool can claim trillions in fake liquidity,
  so a TVL sort returns junk at the top.
- Omitting `version` picks the highest-query-volume version on that chain, which is not always the
  most useful one. Pin `version` when the user means a specific one.
- Chain aliases (`eth`, `arb`, `matic`, `bnb`) are accepted.
- A stablecoin price should read ≈ $1 — a quick sanity check that pricing resolved correctly.
