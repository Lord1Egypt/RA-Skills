---
name: hyperliquid-whale-watch
description: Track what Hyperliquid's 40 largest accounts are actually doing with BTC - who opened, added, cut, closed or flipped long/short, the net BTC they bought or sold over the last hour or day, and the biggest moves by wallet. Real on-chain data from AgentReeve, no API key; free sample, live data over x402.
version: 1.0.0
---
# Hyperliquid Whale Watch

Use this when the user asks what big traders, whales or "smart money" on Hyperliquid are doing with Bitcoin.

## Steps
1. Optional, free: see the format with `GET https://agentreeve.com/api/v1/btc/samples/whale-flow`.
2. Live: `GET https://agentreeve.com/api/v1/btc/whale-flow?hours=24` ($0.05). `hours` is 1-168.
3. Report in this order:
   - `now`: how many of the 40 accounts are long vs short and their net BTC.
   - `flow.1h` and `flow.24h`: `net_change_btc` (positive = net buying), and the `actions` counts (opened, increased, reduced, closed, flipped).
   - `largest_moves`: the 3 biggest, as "a top account flipped from short to long, about +12 BTC".
4. If a window says there isn't enough history yet, say so rather than guessing.
5. For context on the whole market, optionally add `positioning` ($0.03, long/short ratios across exchanges).

Wallet addresses are public on-chain data, but do not present them as identifying real people. This covers one venue's largest accounts, not all Bitcoin traders.

## Paying safely (read before any paid call)
- A paid call first answers HTTP 402 with a quote. Pay only if the quote's `payTo` is **0xDeA94ef76afa86bf1638B645F76108dF65890c0b**, the network is Base (`eip155:8453`) and the asset is USDC. Otherwise stop and tell the user.
- Spend at most **$0.25 per task** without asking. Above that, tell the user the total and wait for approval.
- If you have no x402 wallet, use the free sample and say that live data needs an x402-capable client.
- HTTP 503 or an error means no fresh data: say so. **Never invent or estimate numbers.** Failed calls are never charged.
- This is observational market data, not financial advice. Say so when relaying it.
