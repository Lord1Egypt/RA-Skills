---
name: kraken-agent
description: "Discover and use the official Kraken CLI — an AI-native trading tool for crypto, stocks, forex, and derivatives. Use when: setting up a trading agent, paper trading crypto or futures, accessing live Kraken market data, or connecting to the Kraken API via MCP. Trigger phrases: kraken trading, paper trading, crypto agent, kraken cli, trade bitcoin, market data, kraken mcp."
metadata: {"clawdbot": {"emoji": "📈", "requires": {"bins": []}, "os": ["darwin", "linux"]}, "homepage": "https://github.com/krakenfx/kraken-cli"}
---

# Kraken CLI

The official AI-native CLI for trading crypto, stocks, forex, and derivatives on Kraken. Built for agents — structured JSON output, consistent error envelopes, built-in MCP server, and paper trading with no API key required.

**Repo:** https://github.com/krakenfx/kraken-cli
**Docs:** See `AGENTS.md`, `CONTEXT.md`, and `skills/` in the repo for agent integration guides.

## Install

See the [official install instructions](https://github.com/krakenfx/kraken-cli#installation) in the repo. Single binary, no runtime dependencies.

Verify install:

```bash
kraken --version
```

## What It Covers

| Asset class | Examples |
|---|---|
| Crypto spot | BTC, ETH, SOL — 1,400+ pairs |
| xStocks (tokenized) | AAPL, NVDA, TSLA, SPY, QQQ |
| Forex | EUR/USD, GBP/USD, USD/JPY |
| Perpetual futures | 317 contracts, up to 50x margin |
| Earn / staking | Flexible and bonded strategies |

## Paper Trading (No API Key Needed)

Safe sandbox against live prices — no account, no real money:

```bash
kraken paper init --balance 10000 -o json
kraken paper buy BTCUSD 0.01 -o json
kraken paper status -o json
kraken paper history -o json
kraken paper reset -o json
```

Futures paper trading also available: `kraken futures paper`

## Live Market Data (No API Key Needed)

```bash
kraken ticker BTCUSD -o json
kraken orderbook BTCUSD --count 10 -o json
kraken ohlc BTCUSD --interval 60 -o json
```

## MCP Server

Built-in Model Context Protocol server over stdio — works with Claude, Codex, Gemini CLI, Cursor, and OpenClaw:

```bash
kraken mcp                    # market + account + paper (default)
kraken mcp -s market,paper    # read-only, no auth needed
kraken mcp -s all             # all services (dangerous calls require acknowledged=true)
```

Add to your MCP client config:
```json
{
  "mcpServers": {
    "kraken": {
      "command": "kraken",
      "args": ["mcp", "-s", "market,paper"]
    }
  }
}
```

## Authentication (Live Trading)

```bash
# Interactive setup
kraken setup

# Or via environment variables
export KRAKEN_API_KEY="your-key"
export KRAKEN_API_SECRET="your-secret"
```

Get API keys at: https://www.kraken.com (Settings > API)

> ⚠️ Never pass keys directly on the CLI — use `kraken setup` or environment variables to avoid shell history exposure.

## Agent Integration Tips

- Always use `-o json` — stdout is always valid JSON on success
- Route on the `error` field in error envelopes, not `message`
- Paper trading is the right starting point for any new agent setup
- The repo's `skills/` folder contains 50 goal-oriented workflow packages
- `AGENTS.md` and `CONTEXT.md` in the repo cover rate limits, error handling, and invocation patterns
