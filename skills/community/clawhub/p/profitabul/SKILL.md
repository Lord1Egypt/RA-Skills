---
name: profitabul-mcp
description: Real-time futures market intelligence, GEX/options flow analysis, trading signals, paper trading, backtesting, and live execution via MCP. Covers ES, NQ, SPX, NDX, QQQ, IWM, GC, SI, CL, and more.
version: 0.2.3
metadata:
  openclaw:
    requires:
      env:
        - PROFITABUL_API_KEY
    primaryEnv: PROFITABUL_API_KEY
    emoji: "\U0001F4C8"
    homepage: https://profitabul.ai
---

# Profitabul MCP

Real-time futures and options market intelligence for AI trading agents. Get live market context, GEX-derived support/resistance levels, trading signals, historical data, backtesting, and paper trading — all through a single MCP endpoint.

## Features

- **Market Context** — Live price, GEX regime, VIX state, and candle summaries for 13 symbols
- **Heatseeker Signals** — Directional trading signals combining gamma exposure, vanna exposure, and VIX trend
- **GEX Key Levels** — King node, gatekeeper, zero gamma, ceiling, and floor levels derived from real options flow
- **Historical Data** — Candle data across multiple timeframes (1m to 1d) with up to 200K bars
- **Statistics** — Realized volatility, average range, volume stats over any lookback period
- **Reports** — Opening Range Breakout (ORB) and Initial Balance (IB) analysis
- **Backtesting** — Server-side strategy backtests (ORB breakout/fade) with configurable parameters
- **Paper Trading** — Open, close, and track hypothetical positions with full P&L
- **Live Execution** — Execute real trades through ProjectX broker (when enabled)

## Supported Symbols

| Category | Symbols |
|----------|---------|
| Indices | SPX, NDX |
| ETFs | SPY, QQQ, IWM |
| Futures | ES, NQ, YM, RTY |
| Commodities | GC (Gold), SI (Silver), CL (Crude Oil), HG (Copper) |

## Setup

### 1. Get Your API Key

1. Sign up at [profitabul.com](https://profitabul.com)
2. Subscribe to a Pro plan (API access is included)
3. Go to **Settings > Integrations** and generate an Agent API key
4. Copy the key (shown once, starts with `pab_live_`)

### 2. Configure Environment

Add to `~/.clawdbot/.env`:
```bash
PROFITABUL_API_KEY=pab_live_YOUR_KEY_HERE
```

### 3. Configure mcporter

Add to `config/mcporter.json`:
```json
{
  "mcpServers": {
    "profitabul": {
      "baseUrl": "https://agents.profitabul.ai/mcp",
      "headers": {
        "Authorization": "Bearer ${PROFITABUL_API_KEY}"
      }
    }
  }
}
```

### 4. Verify

```bash
mcporter list profitabul
```

## Available Tools (16)

### Market Intelligence

| Tool | Description |
|------|-------------|
| `get_market_context` | Comprehensive market snapshot: price, GEX levels, VIX state, candle summary |
| `get_signal` | Heatseeker trading signal with directional bias, confidence, and entry/exit levels |
| `get_key_levels` | GEX-derived support/resistance: king node, gatekeeper, zero gamma, floor, ceiling |

### Historical Data & Analysis

| Tool | Description |
|------|-------------|
| `get_history` | Fetch historical candles for any symbol/timeframe/date range |
| `get_statistics` | Summary statistics: realized volatility, average range, volume |
| `run_report` | Opening Range Breakout (ORB) and Initial Balance (IB) analysis |
| `run_backtest` | Server-side strategy backtest with configurable parameters |

### Paper Trading

| Tool | Description |
|------|-------------|
| `paper_trade` | Open, close, or list paper positions with P&L tracking |

### Live Execution (When Enabled)

| Tool | Description |
|------|-------------|
| `live_open` | Open a live futures trade with stop/target |
| `live_close` | Close a tracked live trade |
| `live_reduce` | Partially reduce an open position |
| `live_add_risk` | Add stop-loss/take-profit to existing position |
| `live_cancel_orders` | Cancel open orders |
| `live_account` | Read account info (balance, margin) |
| `live_positions` | Read open positions |
| `live_orders` | Read working orders |

## Usage Examples

### Market Analysis Workflow

```bash
# 1. Get current market context
mcporter call 'profitabul.get_market_context(symbol: "SPX")'

# 2. Check key GEX levels
mcporter call 'profitabul.get_key_levels(symbol: "SPX")'

# 3. Get trading signal based on current conditions
mcporter call 'profitabul.get_signal(
  symbol: "SPX",
  gex_bias: "positive",
  vex_bias: "bullish",
  vix_trend: "falling"
)'
```

### Historical Analysis

```bash
# Get 30 days of 5-minute candles
mcporter call 'profitabul.get_history(symbol: "ES", timeframe: "5m", days: 30)'

# Run ORB analysis
mcporter call 'profitabul.run_report(reportType: "orb", symbol: "ES", days: 60)'

# Backtest ORB breakout strategy
mcporter call 'profitabul.run_backtest(
  symbol: "ES",
  days: 30,
  strategy: { type: "orb-breakout", params: { stopMult: 0.75, targetMult: 1.0 } }
)'
```

### Paper Trading

```bash
# Open a paper trade
mcporter call 'profitabul.paper_trade(
  action: "open",
  symbol: "ES",
  side: "long",
  entry: 5825,
  size: 2,
  reason: "GEX support bounce at zero gamma"
)'

# List open positions
mcporter call 'profitabul.paper_trade(action: "list")'

# Close a trade
mcporter call 'profitabul.paper_trade(
  action: "close",
  trade_id: "pt_1705312200_abc123",
  exit: 5850,
  close_reason: "Target reached at king node"
)'
```

## Recommended Workflow

1. **Start with context** — Call `get_market_context` to understand current conditions
2. **Check levels** — Use `get_key_levels` for precise support/resistance
3. **Get signal** — Feed GEX bias, VEX bias, and VIX trend into `get_signal`
4. **Validate with history** — Use `run_report` or `run_backtest` to check if the setup has edge
5. **Execute** — Open a `paper_trade` (or `live_open` if enabled) at signal levels
6. **Manage** — Track and close positions based on level targets

## Rate Limits

- 120 requests per minute per API key
- Sliding window rate limiting
- Returns `429 Too Many Requests` with `Retry-After` header when exceeded

## Resources

- [Profitabul Platform](https://profitabul.com)
- [API Documentation](https://profitabul.ai/docs)
- [Discord Community](https://discord.gg/profitabul)
