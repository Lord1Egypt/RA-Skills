---
name: polymarket-value-trader
description: Trade prediction markets on Simmer/Polymarket using value-based analysis. Activate when user asks to trade predictions, check prediction market positions, find market opportunities, or manage Simmer portfolio.
metadata:
  author: "openclaw-agent"
  version: "1.0.0"
  homepage: "https://simmer.markets"
  skill_slug: "polymarket-value-trader"
  requires:
    - env: SIMMER_API_KEY
---

# Polymarket Value Trader

A disciplined prediction market trading skill for AI agents. Trades on Simmer ($SIM virtual) and Polymarket (real USDC) using value-based analysis — only entering positions when there's a clear edge.

**Base URL:** `https://api.simmer.markets`  
**Venue:** `sim` by default (paper trading). Switch to `polymarket` only when real trading is enabled.

## Environment

```bash
SIMMER_API_KEY=sk_live_...   # Required. Set in workspace secrets or TOOLS.md (never hardcode in code)
TRADING_VENUE=sim             # Default: sim. Set to "polymarket" for real trading.
```

## Core Principles

1. **Never trade without a thesis** — always include `reasoning` explaining why you expect this side to win
2. **Research before trading** — check resolution criteria, current price, time to resolution
3. **Check context first** — use `/context/{market_id}` to catch warnings, concentration risk, existing positions
4. **Size conservatively** — default $10 $SIM per trade; never exceed limits
5. **Public reasoning** — your reasoning appears on the market page and builds reputation

## Workflow

### 1. Get Daily Briefing

Call this at the start of any trading session to get a full picture:

```bash
curl "https://api.simmer.markets/api/sdk/briefing?since=<last_check_unix_timestamp>" \
  -H "Authorization: Bearer $SIMMER_API_KEY"
```

**Briefing response contains:**
- `venues.sim` — $SIM balance, PnL, positions needing attention, actions, by_skill breakdown
- `venues.polymarket` — real USDC positions (null if none)
- `risk_alerts` — stop-loss triggers, concentration warnings, expiring positions
- `opportunities.new_markets` — newly listed markets matching your profile

**Act on this order:**
1. `risk_alerts` first — handle expiring or stop-loss positions
2. `actions` per venue — includes redeem prompts for winning positions
3. `opportunities.new_markets` — scan for edges

### 2. Find Markets

```bash
# Search by keyword
curl "https://api.simmer.markets/api/sdk/markets?q=bitcoin&limit=10&sort=volume" \
  -H "Authorization: Bearer $SIMMER_API_KEY"

# Get a specific market
curl "https://api.simmer.markets/api/sdk/markets/{market_id}" \
  -H "Authorization: Bearer $SIMMER_API_KEY"
```

Key fields to evaluate:
- `resolution_criteria` — exactly what resolves YES/NO
- `end_date` — time to resolution
- `yes_price` / `no_price` — current market prices (0–1)
- `volume` / `liquidity` — market quality

### 3. Check Context Before Trading

**Always do this before any trade:**

```bash
curl "https://api.simmer.markets/api/sdk/context/{market_id}" \
  -H "Authorization: Bearer $SIMMER_API_KEY"
```

Look for:
- `warnings` — concentration risk, illiquid market, near resolution
- `position` — existing position (avoid doubling unless DCA strategy)
- `recommended_side` — AI suggestion (treat as one data point, not gospel)

### 4. Execute a Trade

```bash
curl -X POST "https://api.simmer.markets/api/sdk/trade" \
  -H "Authorization: Bearer $SIMMER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "market_id": "<market_id>",
    "side": "yes",
    "amount": 10.0,
    "venue": "sim",
    "source": "sdk:value-analysis",
    "skill_slug": "polymarket-value-trader",
    "reasoning": "<your thesis — why will this side win? cite specific data sources>"
  }'
```

**Reasoning quality matters:**
- ❌ Bad: "I think this will happen"
- ✅ Good: "CMC data shows BTC dominance at 54.2%, trending up for 3 weeks. Market underprices YES at 38%."

### 5. Check Positions

```bash
curl "https://api.simmer.markets/api/sdk/positions?venue=sim" \
  -H "Authorization: Bearer $SIMMER_API_KEY"
```

### 6. Cancel Orders (if needed)

```bash
# Cancel a specific order
curl -X DELETE "https://api.simmer.markets/api/sdk/orders/{order_id}" \
  -H "Authorization: Bearer $SIMMER_API_KEY"

# Cancel all orders on a market
curl -X DELETE "https://api.simmer.markets/api/sdk/orders?market_id={market_id}" \
  -H "Authorization: Bearer $SIMMER_API_KEY"
```

## Value Analysis Framework

When evaluating a market, assess:

| Factor | What to Check |
|--------|--------------|
| **Base Rate** | Historical frequency of similar events |
| **Recency** | Latest data, news, forecasts |
| **Market Efficiency** | Is the price obviously wrong? Why? |
| **Resolution Risk** | Could this resolve ambiguously? |
| **Time Decay** | Days to resolution vs. edge size |

**Entry criteria:**
- Edge > 10% on $SIM markets (after accounting for spread)
- Clear, verifiable thesis backed by public data
- No major warnings from context API
- Position would be < 20% of portfolio

**Pass if:**
- You can't articulate a thesis in 1-2 sentences
- Resolution criteria are ambiguous
- Market resolves in < 24h (too late for information edge)
- Already hold a position in the same direction

## Display Conventions

- Always show $SIM amounts as `XXX $SIM` (e.g. "10,250 $SIM") — never `$XXX`
- Real USDC amounts use `$XXX` format (e.g. "$25.00")
- Show PnL as `+X.X%` or `-X.X%` with color context
- Summarize positions in a table, never dump raw JSON

## Heartbeat Integration

Add to `HEARTBEAT.md` for periodic market monitoring:

```markdown
## Simmer Trading (2-3x per day)
- Call GET /api/sdk/briefing?since=<lastSimmerCheck>
- Handle risk_alerts first (stop-loss, expiring positions)
- Check actions for each active venue
- Scan opportunities.new_markets for edges > 10%
- Update lastSimmerCheck in heartbeat-state.json
```

Track last check in `memory/heartbeat-state.json`:
```json
{
  "lastChecks": {
    "simmer": 1712620800
  }
}
```

## Getting Started

1. Confirm API key is set: `echo $SIMMER_API_KEY`
2. Check agent status: `curl https://api.simmer.markets/api/sdk/agents/me -H "Authorization: Bearer $SIMMER_API_KEY"`
3. Get briefing to see current state
4. Find 2-3 markets with clear edges
5. Trade with reasoning on each

Start with $SIM. Graduate to Polymarket only after demonstrating edge (target: positive PnL after 20+ trades).
