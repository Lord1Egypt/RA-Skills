---
name: graph-advocate
description: "Route any blockchain data question to the right Graph Protocol service. Returns live data from 15,500+ subgraphs, Token API (EVM/Solana/TON + Polymarket + Hyperliquid), x402 payment analytics, cross-venue prediction-market spreads (Polymarket ↔ Limitless, Polymarket ↔ Kalshi), and protocol-specific MCP packages. Trigger keywords: subgraph, token, balance, holder, swap, pool, TVL, DeFi, NFT, Aave, Uniswap, Polymarket, Limitless, Kalshi, prediction market spread, arbitrage, Hyperliquid, perps, ENS, governance, x402, onchain data, blockchain."
version: 2.9.0
homepage: https://github.com/PaulieB14/graph-advocate
metadata:
  clawdbot:
    emoji: "⛓️"
---

# Graph Advocate

Ask any blockchain data question in plain English. Get back **live data** — not just a recommendation.

## Routing

Match the user's intent to the right service. Load only the reference you need.

| Intent | Service | Reference | Use for |
|--------|---------|-----------|---------|
| **Token balances, holders, swaps, NFTs** | token-api | [token-api.md](references/token-api.md) | Wallet data across EVM, Solana, TON |
| **Polymarket markets, OHLCV, P&L, positions** | token-api | [token-api.md](references/token-api.md) | REST endpoints under `/v1/polymarket/*` — no npm install |
| **Find a subgraph for a protocol** | subgraph-registry | [subgraph-registry.md](references/subgraph-registry.md) | Search 15,500+ subgraphs by protocol/chain |
| **Aave lending data** | graph-aave-mcp | [aave.md](references/aave.md) | 40 tools — V2/V3/V4, liquidations, rates |
| **Polymarket advanced (orderbook, disputes, trader winrate/drawdown)** | graph-polymarket-mcp | [polymarket.md](references/polymarket.md) | 31 tools — live CLOB, UMA resolution, subgraph-specific P&L stats |
| **Hyperliquid perps — trader skill, vaults, liquidations** | token-api + `/hyperliquid/*` | [hyperliquid.md](references/hyperliquid.md) | Raw markets/users/vaults via token-api; derived skill scores via GA's paid `/hyperliquid/*` endpoints |
| **Cross-protocol lending** | graph-lending-mcp | — | Messari standardized — 40+ protocols on 15 chains |
| **Limitless prediction markets** | graph-limitless-mcp | — | Markets on Base |
| **Cross-venue prediction-market spread (Polymarket ↔ Limitless)** | `/predmarket/spread` (paid) | — | Same-topic markets paired across venues, per-pair yes-mid spread (bps), arbitrage direction. JOIN single-venue passthroughs can't return. $0.05 USDC. |
| **Cross-source prediction-market spread (Kalshi ↔ Polymarket)** | `/kalshi-polymarket/spread` (paid) | — | Same-topic markets across Kalshi + Polymarket with mid-spread and arbitrage direction. $0.05 USDC. |
| **Agent reputation score (0-100)** | `/agent/score` (paid) | — | Composite from ERC-8004 registration + USDC settlement velocity + on-chain feedback registry, aggregated across all of owner's agents. Hard 8004 gate filters burns/CEX. Buyer-agent's "should I trust this peer" call. Response includes counterparty-ref-v1 conformant SHA-256 + preimage + canonical JCS string so a verifier can re-derive byte-exact without callback. $0.02 USDC. |
| **Kalshi consensus trend** | `/kalshi/consensus-trend` (paid) | — | Slope/acceleration/volatility band from Kalshi forecast_history. $0.05 USDC. |
| **Kalshi sports live-edge** | `/kalshi/sports-live-edge` (paid) | — | Play-by-play momentum vs market candlesticks; flags latency-arb windows. $0.05 USDC. |
| **Predict.fun prediction markets** | predictfun-mcp | — | BNB Chain prediction markets |
| **x402 payment analytics — NL question** | `/ask` (paid) | — | Natural-language Q&A over 132M settlements + daily_stats (May 2025 → Jun 2026). Sonnet + DuckDB. $0.05 USDC. |
| **x402 address lookup — onchain receipts** | `/onchain-x402/address` (paid) | — | Decentralized lookup via x402 Base subgraph: lifetime stats by role (payer/recipient), recent payments, facilitator, indexed_through_block. $0.01 USDC. |
| **x402 payment analytics (legacy reference)** | x402-analytics | [x402.md](references/x402.md) | Payment volume, facilitators, daily stats on Base |
| **Raw block data, streaming** | substreams | — | Traces, logs, custom transformations |
| **Agent discovery (ERC-8004)** | 8004scan | — | Find AI agents by capability |
| **MCP server auth** | mcp8004 | — | ERC-8004 identity verification |

**Polymarket routing rule:** Prefer `token-api` for common queries (markets, OHLCV, activity, user positions, P&L, platform stats). Only route to `graph-polymarket-mcp` for advanced queries: live orderbook depth, live spreads, disputed markets, UMA resolution, trader winrate/drawdown/profit factor, CTF splits/merges/redemptions.

If the request spans two services, use both and combine results.

## Quick Examples

```
"Top 10 USDC holders on Ethereum"           → token-api
"Best subgraph for Uniswap V3 on Arbitrum?" → subgraph-registry
"Aave V3 liquidations above $50K"           → graph-aave-mcp
"Hottest Polymarket markets"                → token-api (/v1/polymarket/markets)
"Polymarket OHLCV for Bitcoin market"       → token-api (/v1/polymarket/markets/ohlc)
"Polymarket trader P&L for 0x..."           → token-api (/v1/polymarket/users/positions)
"Polymarket live orderbook depth"           → graph-polymarket-mcp (advanced)
"Polymarket trader winrate/drawdown"        → graph-polymarket-mcp (subgraph P&L stats)
"Score Hyperliquid trader 0x..."            → /hyperliquid/score (paid)
"Hyperliquid top traders for HYPE"          → /hyperliquid/screen (paid)
"Evaluate Hyperliquid vault 0x..."          → /hyperliquid/vault (paid)
"Compare Aave vs Compound TVL"              → graph-lending-mcp
"x402 payment volume on Base today"         → x402-analytics
"Top 10 x402 recipients in the last 30 days" → /ask (paid, NL→SQL)
"When did x402 volume on Base inflect?"     → /ask (paid, NL→SQL)
"Has 0x0FF5A6… ever been paid via x402?"     → /onchain-x402/address (paid, decentralized)
"Polymarket vs Limitless spread on 'trump'"  → /predmarket/spread (paid, cross-venue JOIN)
"Kalshi vs Polymarket fed-rate arbitrage"    → /kalshi-polymarket/spread (paid)
"Find agents that do trading"               → 8004scan
```

## How It Works

1. Agent sends plain-English question
2. Graph Advocate identifies the best service
3. Searches the subgraph registry (15,500+ subgraphs with query hints)
4. Executes the query and returns **live data** in the response
5. Includes `get_started` link for agents to get their own free API key

## Response Format

```json
{
  "recommendation": "subgraph-registry",
  "reason": "why this service fits",
  "confidence": "high",
  "query_ready": { "tool": "...", "args": {...} },
  "execution_result": { "source": "subgraph-gateway", "data": {...} },
  "get_started": "Free API key: https://thegraph.com/studio/",
  "cache_for_seconds": 86400
}
```

## Endpoints

| Method | URL | Purpose |
|--------|-----|---------|
| POST | `https://graphadvocate.com/` | A2A JSON-RPC 2.0 |
| POST | `https://graphadvocate.com/chat` | Simple HTTP chat |
| GET | `https://graphadvocate.com/.well-known/agent-card.json` | Agent card |
| GET | `https://graphadvocate.com/agents/capabilities.json` | Machine-readable capability list |
| GET | `https://graphadvocate.com/mcp/catalog` | List of installable MCP servers |
| GET | `https://graphadvocate.com/llms.txt` | LLM-friendly discovery file |
| GET | `https://graphadvocate.com/quota?sender=0x...` | Free-tier quota remaining today (no charge) |
| GET | `https://graphadvocate.com/dashboard` | Live monitoring |
| POST | `https://graphadvocate.com/feedback` | Agent feedback |

## Default mode: no wallet, free tier

This skill is **fully functional with no wallet attached**. The default routing —
plain-English question in, JSON recommendation + live data out — runs against the
free tier and never asks for funds. Agents that don't expose an x402-enabled
runtime simply never see a payment challenge.

If you're evaluating Graph Advocate for the first time, start without a wallet,
use the free tier, and decide later whether the paid endpoints are worth opting
into.

## Optional paid mode (opt-in)

Some endpoints settle in USDC on Base via the x402 protocol. Paid mode is
**opt-in**: it only activates when your agent runtime is configured to accept
x402 payment challenges. Without that configuration, paid endpoints return
`402 Payment Required` and the call stops there — no funds move.

### Pricing
- `/route` — 3 free queries/sender/day, then **$0.01 USDC** per call (Base mainnet)
- `/polymarket/*` — paid from call 1 ($0.01 - $0.05 per call)
- `/hyperliquid/*` — paid from call 1 ($0.02 - $0.10 per call)
- `/predmarket/spread` — paid from call 1 (**$0.05 USDC**) — Polymarket ↔ Limitless cross-venue spread on a topic. POST `{topic, limit?}` returns per-pair yes-mid spread (bps) and arbitrage direction. JOIN that single-venue passthroughs structurally can't return.
- `/kalshi-polymarket/spread` — paid from call 1 (**$0.05 USDC**) — Kalshi ↔ Polymarket cross-source spread on a topic.
- `/kalshi/consensus-trend`, `/kalshi/sports-live-edge` — paid from call 1 (**$0.05 USDC** each).
- `/ask` — paid from call 1 (**$0.05 USDC**) — natural-language Q&A over the x402 Base settlements warehouse. 132M+ payments + pre-aggregated `daily_stats` (388 days). Returns `{answer, sql_trace, model, upstream_ms}` so callers can verify the data path.
- `/onchain-x402/address` — paid from call 1 (**$0.01 USDC**) — decentralized address lookup against the x402 Base subgraph on The Graph Network. POST `{address}` returns lifetime stats (payer + recipient roles), recent 10 payments in each direction, facilitator metadata, and `indexed_through_block` for freshness.

### 402 challenge — preview before paying
Every paid endpoint's 402 response body includes an `output_example` field with a sample of the payload you'll receive after paying. Inspect this before signing — if the shape doesn't fit your use case, bail without spending.

### Per-call approval (recommended)

Every paid call is preceded by an HTTP 402 challenge that names the price,
the recipient address, and the settlement network:

```
HTTP/1.1 402 Payment Required
X-Payment: { "amount": "0.01", "currency": "USDC", "network": "base",
             "recipient": "0x0FF5A6ec…7C86", "challenge": "<nonce>" }
```

The 402 challenge is the per-call approval surface. **Configure your runtime
to surface 402 challenges to the user** before any payment is signed — most
x402 clients accept an interactive-approval flag (e.g. `confirmBeforePay`).
With per-call approval enabled, you see the exact price and recipient on every
paid request and decide yes/no per call. This is the recommended posture for
any wallet that holds more than a trivial amount.

If you instead configure your runtime to accept 402 challenges automatically,
paid calls settle without an interactive prompt. That is a runtime-level choice,
not a property of this skill — and if you choose it, the spend controls below
become load-bearing.

### Free-quota visibility (no-charge)

Before any paid call, check today's remaining free-tier quota:

```
GET https://graphadvocate.com/quota?sender=0x<your-agent-address>
```

Returns:

```json
{
  "sender": "0x…",
  "free_quota_daily": 3,
  "used_today": 1,
  "remaining_today": 2,
  "free_tier_exhausted": false,
  "next_call_paid": false,
  "price_usdc_per_paid_call": 0.01
}
```

`/quota` is a no-charge metadata route. Use it to:

1. Display "N free queries remaining today" in your UI before the agent runs.
2. Halt autonomous loops when `remaining_today` hits 0 instead of accepting
   the 402 challenge.
3. Audit per-sender spend by polling daily.

### Required spend controls before autonomous use

1. **Dedicated low-balance wallet.** Fund only what you're willing to spend
   in a session (e.g. $5 USDC). Never connect a wallet that holds your treasury.
2. **Spend caps in your agent runtime.** Most x402 clients accept
   `maxAmountPerCall` and `maxTotalSpend` parameters. If yours does not, wrap
   calls to this skill in a counter that breaks after N invocations.
3. **Stop conditions.** Add at least one of:
   - Hard cap on call count per task (e.g. `max_calls_per_run = 5`)
   - Time bound on the task (e.g. abort after 5 minutes)
   - Cost ceiling check before each call (read wallet USDC balance; halt if below threshold)
4. **First-run probe mode.** Treat the first execution as a probe — log every
   call, inspect spend, then enable autonomous mode only after confirming the
   per-task cost matches expectations.

### Receipts and no-charge surface

- Every paid call returns an `x-payment-response` header with the on-chain
  settlement reference. Log it. If a call doesn't return that header but charged
  your wallet, file an issue — the contract is "no settlement, no charge."
- **No-charge endpoints** never trigger payment: `/.well-known/agent-card.json`,
  `/agents/capabilities.json`, `/mcp/catalog`, `/llms.txt`, `/dashboard`,
  `/chat`, `/quota`, `GET /`.

Payments are received by Ampersend smart account `0x0FF5A6ecef783BBA35463ec2F8403B9B5e9e7C86`.

## External Endpoints

| Endpoint | Data sent | Purpose |
|----------|-----------|---------|
| `graphadvocate.com` | Your plain-English query | Routes to the right Graph service |
| `gateway.thegraph.com/api/` | GraphQL queries | Executes subgraph queries for live data |
| `token-api.thegraph.com/` | REST requests | Fetches token/NFT/swap data |
| `api.studio.thegraph.com` | GraphQL queries | x402 payment analytics |

## Security & Privacy

- **Instruction-only skill** — no code is downloaded or executed on your machine
- **No credentials required** — Graph Advocate does not need API keys from you
- **No local file access** — reads nothing from your filesystem
- **Stateless** — no session data persists between requests

## Identity

- **ERC-8004:** Agent #734 (Arbitrum), #41,034 (Base)
- **ENS:** graphadvocate.eth
- **Ampersend:** [app.ampersend.ai/discover/agent/8453:41034](https://app.ampersend.ai/discover/agent/8453:41034)

## Trust Statement

By using this skill, your plain-English data queries are sent to `graphadvocate.com` (hosted on Railway, operated by @paulieb14). The service returns structured JSON with live data. Queries may include wallet addresses and protocol/trading intent — do not send sensitive private context (private keys, seed phrases, internal strategy details) and only install if you trust this endpoint operator.

**Paid mode is opt-in.** This skill never requests credentials from you. Paid
endpoints only settle when your agent runtime is configured to accept x402
payment challenges. Configure interactive approval if you want a per-call
y/N prompt, and always use a low-balance wallet — see the "Optional paid mode"
section above for the recommended posture and spend controls.

## Links

- GitHub: https://github.com/PaulieB14/graph-advocate
- The Graph: https://thegraph.com
- Subgraph Studio: https://thegraph.com/studio
