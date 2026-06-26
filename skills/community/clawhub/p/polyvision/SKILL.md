---
name: polyvision
description: Analyze Polymarket prediction market wallets — get copy trading scores (1-10), P&L, win rate, risk metrics (Sharpe ratio, Sortino ratio, max drawdown), red flags, position sizing, market category performance, recent performance (7d/30d/90d), streak analysis, individual open positions with entry/current prices, and recent trade history. Also discover elite traders via daily leaderboard, hot bets from top traders, and random wallet discovery. Connects via MCP server or REST API. Use when evaluating whether to copy trade a Polymarket trader, comparing multiple wallets side-by-side, screening for elite prediction market performers, checking if a wallet has bot-like trading patterns or hidden losses, researching a trader's risk profile, viewing recent trade activity, finding today's best open bets, or discovering new traders to follow. Free API key, no daily limits, 6-hour result caching.
homepage: https://polyvisionx.com
license: MIT
disable-model-invocation: true
metadata: {"clawdis":{"emoji":"📊","primaryEnv":"POLYVISION_API_KEY","requires":{"env":["POLYVISION_API_KEY"]}}}
---

# PolyVision — Polymarket Wallet Analyzer

PolyVision analyzes Polymarket prediction market wallets and returns a comprehensive trading profile: copy trading score (1-10), P&L breakdown, win rate, risk metrics (Sharpe ratio, Sortino ratio, max drawdown), position sizing consistency, market category performance, recent performance windows (7d/30d/90d), streak analysis, red flags, and individual open positions with entry/current prices. It also provides a daily leaderboard of top-ranked traders, hot bets (most profitable open positions from top traders), and random elite wallet discovery. Use it to evaluate whether a trader is worth copy trading, compare multiple wallets, screen for elite performers, find today's best bets, or discover new traders to follow.

## When to Use
- User mentions a Polymarket wallet address (0x...)
- User asks about copy trading, trader evaluation, or wallet scoring
- User wants to compare prediction market traders or screen for elite performers
- User asks about a trader's risk profile, red flags, or trading patterns
- User asks what bets top traders are making, or wants today's best open positions
- User wants to discover or find new Polymarket traders to follow
- User asks about a daily leaderboard or top traders ranking
- User wants to see a trader's individual open positions with P&L details
- User asks about a trader's recent trades, trade history, or latest activity
- User asks for copy trading strategy recommendations or optimal settings
- User wants to know what risk profile or parameters to use for copy trading

## When NOT to Use
- General crypto price queries (not Polymarket-specific)
- Placing trades or executing orders — PolyVision never trades on-chain, executes orders, or moves funds
- Non-Polymarket wallet lookups (Ethereum DeFi, NFTs, etc.)

> **What PolyVision can and cannot change:** Every analysis, scoring, leaderboard, hot-bets, strategy, trades, and discovery tool is **read-only** — PolyVision never places trades, executes orders, or touches the blockchain or your funds. The *only* state it can modify is **your own** PolyVision tracked-wallet portfolio (a saved watch-list scoped to your API key), via the `add_to_portfolio` and `remove_from_portfolio` tools and their REST equivalents (`POST` / `DELETE /v1/portfolio`). Those two tools are flagged below with a ⚠️ mutation warning; treat them as state-changing and only call them when the user explicitly asks.

## Setup: MCP Server (Recommended)

Add to your MCP client configuration (e.g. `claude_desktop_config.json`, Cursor, Windsurf):

```json
{
  "mcpServers": {
    "polyvision": {
      "type": "streamable-http",
      "url": "https://api.polyvisionx.com/mcp",
      "headers": {
        "Authorization": "Bearer ${POLYVISION_API_KEY}"
      }
    }
  }
}
```

## Setup: Get an API Key

Get a free API key (no daily limits) from the Telegram bot:

1. Open the [PolyVision bot](https://t.me/PolyVisionBot) on Telegram
2. Run `/apikey` to generate your key
3. Copy the `pv_live_...` key (shown only once, store it securely)

Set it as an environment variable:

```bash
export POLYVISION_API_KEY="pv_live_abc123..."
```

Full API docs: https://polyvisionx.com/docs

## Access & Tiers

The API key itself is free and there are no daily request limits, but most data tools require **Premium or an active trial**. New accounts start in a trial that is effectively Premium; once it ends, gated tools return **403** (a valid key that simply lacks Premium — not an auth failure).

- **Premium / active trial:** `analyze_wallet`, `get_score`, `get_hot_bets`, `get_leaderboard`, `get_wallet_pool`, `get_strategy`, `discover_wallet`, `get_recent_trades` (plus REST `/v1/trades/batch`). Over REST, the portfolio endpoints (`/v1/portfolio`) also require Premium/trial.
- **Any valid key (free):** `check_quota`, `calculate`, `get_knowledge`, `health`, `regenerate_key`, `deactivate_key`, and — over MCP — the portfolio tools (`get_portfolio`, `add_to_portfolio`, `remove_from_portfolio`).

On a 403, point the user to the Telegram bot `/premium` or https://polyvisionx.com/pricing.

## MCP Tools Reference

### `analyze_wallet`

Run a comprehensive Polymarket wallet analysis.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `wallet_address` | string | Yes | — | Ethereum address (42 chars, starts with `0x`) |
| `mode` | string | No | `"quick"` | `"quick"` (~5s) or `"full"` (~30-60s with timing data) |

**Returns:** Full analysis dict with P&L, win rate, risk metrics, categories, copy trading score (1-10), red flags, and usage info. Results are cached for 6 hours — cache hits are instant. See `references/response-schemas.md` for the complete field reference.

**Timing:** Quick mode ~5s, full mode ~30-60s. Cached responses are instant.

### `get_score`

Get a compact copy-trading score for a wallet. Shares the same cache as `analyze_wallet`.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `wallet_address` | string | Yes | Ethereum address (42 chars, starts with `0x`) |

**Returns:** Score (1-10), recommendation, tier (green/yellow/orange/red), total P&L, win rate, trade count, Sharpe ratio, red flags, cache status, and usage info.

**Timing:** ~5s fresh, instant if cached.

### `get_hot_bets`

Get today's hot bets from top traders. Returns the most profitable open positions from top-ranked Polymarket traders, sourced from the daily strategy report.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `limit` | integer | No | `20` | Maximum number of bets to return |
| `sort_by` | string | No | `"rank"` | `"rank"` (default) or `"pnl"` |

**Returns:** Scan date, total count, and list of hot bets — each with trader info (wallet, username, score, win rate), market details (title, slug, outcome), pricing (entry price, current price, current value), P&L (unrealized P&L, percent), resolution info (end date, days until resolution), entry timing (entry date, days since entry, hold hours), and Polymarket URL. See `references/response-schemas.md` for the complete field reference.

### `get_leaderboard`

Get the daily top-10 leaderboard of ranked Polymarket traders. Synced daily from the scan pipeline.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `sort_by` | string | No | `"rank"` | `"rank"` (default), `"score"`, or `"pnl"` |

**Returns:** Scan date, total count, and list of leaderboard entries — each with wallet address, username, total P&L, volume, ROI%, win rate, risk metrics (Sharpe ratio, max drawdown, profit factor), copy score (1-10), recommendation, tier (green/yellow/orange/red), red flags, track record days, last trade date, and category percentages (politics, crypto, sports). See `references/response-schemas.md` for the complete field reference.

### `get_wallet_pool`

Get consistently high-performing traders from the historical wallet pool — traders who appeared across many daily leaderboard scans. Higher `consistency_pct` means they ranked in the top tier more often. Unlike the daily top-10 leaderboard, this is the persistent pool of repeat performers.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `sort_by` | string | No | `"score"` | `"score"` (default), `"pnl"`, or `"winrate"` |
| `category` | string | No | — | Filter to traders with ≥40% of trades in `sports`, `crypto`, or `politics` |
| `page` | integer | No | `0` | Page number (0-indexed) |
| `limit` | integer | No | `20` | Results per page (1-100) |

**Returns:** Dict with `total_count`, `page`, `limit`, `sort_by`, `category`, and an `entries` list — each with the leaderboard fields plus `consistency_pct`, `appearances`, `avg_score`, `avg_rank`, `first_seen`, and `last_seen`. See `references/response-schemas.md` for the complete field reference.

### `get_strategy`

Get pre-computed copy trading strategy profiles. Returns 3 risk profiles (conservative, moderate, aggressive) with backtested parameters and expected metrics, updated daily.

**Parameters:** None

**Returns:** Scan date, total count, and list of strategy profiles — each with parameters (price range, min score, max trades/day, min trade size, position sizing method), backtest results (win rate, ROI, Sharpe ratio, max drawdown, profit factor, EV/trade, total P&L), cost-adjusted results, and a plain-English description. See `references/response-schemas.md` for the complete field reference.

### `get_recent_trades`

Get recent trades for a Polymarket wallet. Returns trade history with side, size, price, market title, and timestamps.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `wallet_address` | string | Yes | — | Ethereum address (42 chars, starts with `0x`) |
| `since` | integer | No | — | Unix timestamp — only return trades after this time |
| `limit` | integer | No | `50` | Max trades to return (1-100) |

**Returns:** Dict with `wallet_address`, `since`, `count`, and `trades` list — each trade with side (BUY/SELL), size, price, timestamp, market title, outcome, slug, and transaction hash. See `references/response-schemas.md` for the complete field reference.

### `discover_wallet`

Discover a random elite trader from the curated wallet pool (250+). Returns a random wallet address each call — use `analyze_wallet` or `get_score` to investigate it.

**Parameters:** None

**Returns:** `{ "wallet_address": "0x...", "pool_size": 250, "message": "..." }`

### `check_quota`

Check your usage statistics. Does not consume quota.

**Parameters:** None

**Returns:** `{ "used_today": <int>, "tier": "api" }`

API/MCP access has no daily limits — usage is tracked for analytics only.

### `get_portfolio`

Get the user's tracked wallet portfolio with scores and nicknames.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `page` | integer | No | `0` | Page number (0-indexed) |
| `limit` | integer | No | `10` | Results per page (1-50) |

**Returns:** Dict with `total_count`, `page`, `limit`, and `wallets` list — each with wallet address, nickname, score, last analyzed date, and notifications status. See `references/response-schemas.md` for the complete field reference.

### `add_to_portfolio`

Add a wallet to the user's portfolio for tracking.

> ⚠️ **Mutates state.** This writes a new entry to your PolyVision tracked-wallet portfolio (scoped to your API key). It does not place trades or move funds, but it does persist account state. Only call when the user explicitly asks to track, save, or add a wallet.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `wallet_address` | string | Yes | — | Ethereum address (42 chars, starts with `0x`) |
| `nickname` | string | No | — | Display name (defaults to first 10 chars of address) |

**Returns:** Dict with `wallet_address`, `nickname`, and `message` on success, or dict with `error` key on failure (duplicate, limit reached).

**Limits:** Free users: 3 wallets. Premium users: 20 wallets.

### `remove_from_portfolio`

Remove a wallet from the user's portfolio.

> ⚠️ **Mutates state.** This permanently deletes an entry from your PolyVision tracked-wallet portfolio (scoped to your API key). It does not place trades or move funds, but the deletion cannot be undone. Only call when the user explicitly asks to remove, untrack, or delete a wallet.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `wallet_address` | string | Yes | Ethereum address to remove |

**Returns:** Dict with `wallet_address` and `message` on success, or dict with `error` key if wallet not found.

### `health`

Check system health.

**Parameters:** None

**Returns:** `{ "status": "ok" }` or `{ "status": "degraded" }`

### `calculate`

Evaluate a numeric expression deterministically. Use this for **any** arithmetic — ROI math, position sizing, cross-trader comparisons — instead of computing by hand. MCP-only (no REST endpoint).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `expression` | string | Yes | Arithmetic expression (max 200 chars). Supports `+ - * / // % **`, parentheses, and `abs, min, max, round, sqrt, log, log10, exp, ceil, floor`; constants `pi`, `e`. No variables, attribute access, or imports. |

**Returns:** `{ "expression", "result", "formatted" }` on success, or `{ "expression", "error" }` on invalid input.

### `get_knowledge`

Look up curated PolyVision knowledge instead of guessing how the product works or what a report column means. Covers reading the daily reports (`daily_leaderboard`, `strategy_report`, `ev_proof`), copy-trading methodology (`copy_trading_basics`, `scoring_system`, `position_sizing`, `red_flags`, `getting_started`), and features (`polyvision_features`). Use it for "what does X mean / how do I use Y"; for live numbers, use the data tools. MCP-only (no REST endpoint).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `topic` | string | Yes | The knowledge topic to retrieve (one of the keys listed above) |

**Returns:** `{ "topic", "content" }` (markdown) on a hit, or `{ "error", "available_topics" }` for an unknown topic.

### `regenerate_key`

> ⚠️ **Destructive — requires `confirm=true`.** Generates a new API key and **immediately invalidates the old one**. The new key is returned once; the user must update their MCP/REST configuration with it. Only call after the user explicitly confirms.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `confirm` | boolean | Yes | Must be `true` to execute. Without it the tool refuses and asks for confirmation. |

**Returns:** Dict with the new `api_key` and `key_prefix` on success.

### `deactivate_key`

> ⚠️ **Irreversible — requires `confirm=true`.** Deactivates the current API key; all future requests with it are rejected. There is no self-serve undo — use `regenerate_key` instead if a replacement is needed. Only call after the user explicitly confirms.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `confirm` | boolean | Yes | Must be `true` to execute. Without it the tool refuses and asks for confirmation. |

**Returns:** Confirmation that the key was deactivated.

## Score Tiers

| Tier | Score Range | Recommendation | Meaning |
|------|------------|----------------|---------|
| Green | 8.0 – 10.0 | Strong Copy | Consistently profitable, good risk management, strong track record |
| Yellow | 6.0 – 7.9 | Moderate Copy | Decent performance with some concerns, proceed with caution |
| Orange | 4.0 – 5.9 | Risky Copy | Mixed results, significant red flags, high risk |
| Red | 0.0 – 3.9 | Don't Copy | Poor performance, major red flags, likely to lose money |

## Decision Table

| User Intent | Tool | Mode | Why |
|-------------|------|------|-----|
| "Should I copy this trader?" | `get_score` | — | Quick yes/no with score + red flags |
| "Deep dive on this wallet" | `analyze_wallet` | `full` | Complete analysis with timing data |
| "Quick check on a wallet" | `analyze_wallet` | `quick` | Full analysis without activity timing |
| "What are this trader's open positions?" | `analyze_wallet` | `quick` | `open_positions_detail` in analysis response |
| "Compare two traders" | `get_score` x2 | — | Side-by-side scores for fast comparison |
| "What categories does this trader focus on?" | `analyze_wallet` | `quick` | Category breakdown in analysis |
| "What are the best bets right now?" | `get_hot_bets` | — | Today's most profitable open positions from top traders |
| "What bets are top traders making?" | `get_hot_bets` | sort=`pnl` | Hot bets sorted by P&L |
| "Who are the top traders today?" | `get_leaderboard` | — | Daily top-10 ranked traders |
| "Which traders are consistently good?" | `get_wallet_pool` | — | Persistent top performers across many scans |
| "Find me a good trader to follow" | `discover_wallet` | — | Random elite wallet, then `get_score` or `analyze_wallet` |
| "What trades has this wallet made recently?" | `get_recent_trades` | — | Recent trade history for a wallet |
| "What strategy should I use for copy trading?" | `get_strategy` | — | 3 risk profiles with backtested parameters |
| "What's the safest way to copy trade?" | `get_strategy` | — | Conservative profile with low drawdown |
| "Discover new traders" | `discover_wallet` x3 | — | Multiple random picks to explore |
| "Show my tracked wallets" | `get_portfolio` | — | View portfolio with scores and nicknames |
| "Add this wallet to my portfolio" | `add_to_portfolio` | — | Track a wallet with optional nickname |
| "Remove wallet from portfolio" | `remove_from_portfolio` | — | Stop tracking a wallet |
| "What does this score / red flag / report mean?" | `get_knowledge` | — | Curated explanations of PolyVision concepts (MCP-only) |
| "Compute this ROI / position size" | `calculate` | — | Deterministic arithmetic (MCP-only) |
| "Rotate / regenerate my API key" | `regenerate_key` | — | ⚠️ Destructive — invalidates old key (needs `confirm=true`) |
| "Disable my API key" | `deactivate_key` | — | ⚠️ Irreversible (needs `confirm=true`) |
| "Is the system up?" | `health` | — | System status check |
| "How many analyses have I run?" | `check_quota` | — | Usage stats (no limits enforced) |

## Red Flag Reference

Red flags are returned as a list of strings. Here's what each one means:

| Red Flag | Trigger | Severity |
|----------|---------|----------|
| Low win rate | Win rate below 40% | High |
| Large single loss | Single worst trade exceeds 50% of total P&L | Medium |
| Overall unprofitable | Net P&L is negative | High |
| Limited track record | Fewer than 10 closed positions | Medium |
| Inactive | No trades in 30+ days | Low |
| BOT ALERT | Median trade duration under 5 minutes | High |
| Very fast trading | Median trade duration under 30 minutes | Medium |
| LOSS HIDING | 70%+ of open positions underwater (5+ open) | High |
| Open positions losing | 50%+ of open positions underwater (3+ open) | Medium |
| No major red flags detected | No concerning patterns found | None |

## REST API (Alternative)

For agents that cannot use MCP, the data and account tools are available as REST endpoints at `https://api.polyvisionx.com`. (`calculate` and `get_knowledge` are MCP-only — there is no REST equivalent.) All endpoints require Bearer token authentication except `GET /health`. Analysis and market-data endpoints additionally require Premium or an active trial (see **Access & Tiers**) and return **403** without it.

Interactive docs and the OpenAPI spec are available at:
- **Swagger UI:** `https://api.polyvisionx.com/docs`
- **OpenAPI JSON:** `https://api.polyvisionx.com/openapi.json`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `GET /v1/auth/me` | GET | Current user info, tier, premium status, usage (any valid key) |
| `POST /v1/auth/regenerate` | POST | ⚠️ Regenerate your API key — invalidates the old key, returns the new one once |
| `POST /v1/auth/deactivate` | POST | ⚠️ Deactivate your API key — irreversible, rejects all future requests |
| `GET /v1/analyze/{wallet_address}?mode=quick` | GET | Full wallet analysis (includes `open_positions_detail`) |
| `GET /v1/score/{wallet_address}` | GET | Compact copy-trading score |
| `GET /v1/hot-bets?page=0&limit=20&sort_by=rank` | GET | Today's hot bets from top traders |
| `GET /v1/leaderboard?sort_by=rank` | GET | Daily top-10 leaderboard |
| `GET /v1/wallet-pool?sort_by=score&category=&page=0&limit=20` | GET | Consistently high-performing traders from the historical pool |
| `GET /v1/strategy` | GET | Pre-computed copy trading strategy profiles (3 risk levels) |
| `GET /v1/trades/{wallet_address}?since=&limit=50` | GET | Recent trades for a wallet |
| `POST /v1/trades/batch` | POST | Recent trades for up to 5 wallets (JSON body: `wallets`, optional `since`/`since_per_wallet`, `limit`) |
| `GET /v1/discover` | GET | Discover a random elite trader |
| `GET /v1/portfolio?page=0&limit=10` | GET | Get your tracked wallet portfolio |
| `POST /v1/portfolio` | POST | Add a wallet to your portfolio (JSON body: `wallet_address`, `nickname`) |
| `DELETE /v1/portfolio/{wallet_address}` | DELETE | ⚠️ Remove a wallet from your portfolio |
| `GET /health` | GET | Health check (no auth required) |

### Example: Analyze a wallet

```bash
curl -s https://api.polyvisionx.com/v1/analyze/0x1234...abcd?mode=quick \
  -H "Authorization: Bearer $POLYVISION_API_KEY" | jq .
```

### Example: Get a score

```bash
curl -s https://api.polyvisionx.com/v1/score/0x1234...abcd \
  -H "Authorization: Bearer $POLYVISION_API_KEY" | jq .
```

### Example: Get hot bets

```bash
curl -s https://api.polyvisionx.com/v1/hot-bets?sort_by=pnl \
  -H "Authorization: Bearer $POLYVISION_API_KEY" | jq .
```

### Example: Get leaderboard

```bash
curl -s https://api.polyvisionx.com/v1/leaderboard \
  -H "Authorization: Bearer $POLYVISION_API_KEY" | jq .
```

### Example: Get strategy profiles

```bash
curl -s https://api.polyvisionx.com/v1/strategy \
  -H "Authorization: Bearer $POLYVISION_API_KEY" | jq .
```

### Example: Discover a random trader

```bash
curl -s https://api.polyvisionx.com/v1/discover \
  -H "Authorization: Bearer $POLYVISION_API_KEY" | jq .
```

## Error Codes

| Code | Meaning | Recovery |
|------|---------|----------|
| 400 | Invalid wallet address (must be 42-char hex starting with `0x`) | Fix the address format |
| 401 | Invalid or inactive API key | Get a key from the [PolyVision Telegram bot](https://t.me/PolyVisionBot) via `/apikey` |
| 429 | Rate limited | Wait and retry — Polymarket API has upstream limits |
| 503 | System at capacity (all analysis slots in use) | Retry in 30-60 seconds |
| 502 | Upstream Polymarket API error | Retry — the upstream data API may be temporarily unavailable |
| 504 | Analysis timed out | Retry — the wallet may have extensive history |
