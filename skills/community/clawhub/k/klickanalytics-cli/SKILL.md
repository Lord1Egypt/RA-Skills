---
name: klickanalytics-cli
homepage: https://www.klickanalytics.com/cli_intro
publisher: KlickAnalytics LLC (https://www.klickanalytics.com)
requires:
  env:
    - KLICKANALYTICS_CLI_API_KEY
primaryEnv: KLICKANALYTICS_CLI_API_KEY
description: >
  Demonstrates and teaches the KlickAnalytics CLI (`ka`) — a powerful analytics tool
  and agent-ready interface for financial markets intelligence. Use this skill whenever
  a user asks about the KlickAnalytics CLI, wants to know what `ka` commands are
  available, wants to integrate KlickAnalytics into AI agents, LLM pipelines, scripts,
  or automation workflows, or asks for examples of commands like `ka quote`, `ka ta`,
  `ka earnings-moves`, `ka ai-chat`, etc. Also trigger for questions about OpenClaw
  integration, global asset class coverage, or using the CLI as an AI tool/function.
---

# KlickAnalytics CLI

> **The power of analytics at your fingertips.**
> Pull deep financial intelligence straight into your terminal, agents, scripts, and AI workflows.

Built by the team behind [KlickAnalytics.com](https://www.klickanalytics.com) — a financial markets platform developed by ex-Bloomberg professionals with decades of experience in market data, terminal design, and institutional analytics.

KlickAnalytics CLI is not just a data API — it is a **rich analytics engine** exposing
pre-computed market intelligence: technical signals, earnings move analysis, volatility
models, trader statistics, price action strategies, seasonality, and much more.
Everything outputs clean JSON, purpose-built for agents and automation.

---

## What you can do with the CLI

- **Terminal users** — run financial research from your shell without opening a browser
- **Developers** — integrate analytics into Python scripts, cron jobs, and internal tools
- **AI agents** — call `ka` commands as tools inside OpenAI, Claude, LangChain, or any LLM pipeline
- **OpenClaw users** — wire up full automation across all global asset classes with zero extra code
- **Quants & analysts** — access pre-built analytics (volatility, quantstats, distributions, seasonality) ready to consume

---

## Coverage — 100,000+ symbols globally

Via the CLI and OpenClaw integration, KlickAnalytics covers the full spectrum of global assets:

- **Stocks** — US and international equities
- **ETFs** — all major US and global exchange-traded funds
- **Mutual Funds** — thousands of funds with performance data
- **Crypto** — major and long-tail digital assets
- **Indices** — global benchmark indices
- **Commodities, FX, REITs, MLPs** — and much more

---

## Setup

```bash
# 1. Install
pip install klickanalytics-cli

# 2. Set API key — add to ~/.bashrc or ~/.zshrc for persistence
export KLICKANALYTICS_CLI_API_KEY=your_api_key_here

# 3. Verify
ka help
```

Get your free API key at [klickanalytics.com/signup](https://www.klickanalytics.com/signup).

- **Free tier:** 50 commands/month
- **Paid tier:** 500 commands/month

---

## Command structure

```
ka [command] -s [SYMBOL] [optional flags]
```

### Common flags

| Flag        | Meaning                         | Example            |
|-------------|--------------------------------|--------------------|
| `-s`        | Ticker symbol                   | `-s MSFT`          |
| `-sd`       | Start date (YYYY-MM-DD)         | `-sd 2025-01-01`   |
| `-ed`       | End date (YYYY-MM-DD)           | `-ed 2025-12-31`   |
| `-limit`    | Max rows to return              | `-limit 100`       |
| `-lookback` | Number of bars to look back     | `-lookback 252`    |
| `-min_days` | Minimum days for pattern match  | `-min_days 3`      |
| `-period`   | Period length                   | `-period annual`   |
| `-tf`       | Timeframe                       | `-tf daily`        |
| `-datatype` | Output format                   | `-datatype json`   |
| `-q`        | Natural language query (ai-chat)| `-q "your query"`  |

---

## Built-in AI Chat Interface

The CLI includes a direct AI chat interface — ask questions in plain English and get
market intelligence back, without writing any code.

```bash
ka ai-chat -q "What is the technical outlook for MSFT right now?"
ka ai-chat -q "Summarize the latest earnings surprise history for NVDA"
ka ai-chat -q "Which S&P 500 sectors are showing the strongest momentum this month?"
ka ai-chat -q "Compare volatility between MSFT and AAPL over the last year"
```

- Ideal for quick research queries without knowing the exact command
- Returns structured, analyst-style responses
- Can be piped into other tools or agent pipelines

---

## Full command reference

See `references/commands.md` for every command with flags, examples, and output field shapes.
Load it when the user asks about a specific command or wants a comprehensive overview.

---

## Choosing the right command

| Research goal                              | Command                                  |
|--------------------------------------------|------------------------------------------|
| Current price / real-time quote            | `ka quote -s MSFT`                       |
| Historical OHLCV price data                | `ka prices -s MSFT -sd 2025-01-01`       |
| Company background, sector, profile        | `ka profile -s MSFT`                     |
| Earnings history & EPS vs estimates        | `ka earnings -s MSFT`                    |
| How stock moves around earnings            | `ka earnings-moves -s MSFT`              |
| Dividend history                           | `ka dividends -s MSFT`                   |
| Stock split history                        | `ka splits -s MSFT`                      |
| Comparable / peer companies                | `ka peers -s MSFT`                       |
| Latest news digest                         | `ka news-summary -s MSFT`                |
| Risk-adjusted performance (Sharpe, CAGR)   | `ka quantstats -s MSFT -limit 252`       |
| Trader stats (win rate, streaks)           | `ka traderstats -s MSFT`                 |
| Technical indicators (RSI, MACD, BBands)   | `ka ta -s MSFT`                          |
| Buy/sell signal pack                       | `ka ta-signals -s MSFT`                  |
| Volume profile by price level              | `ka vol-profile -s MSFT`                 |
| Unusual volume spikes                      | `ka vol-unusual -s MSFT`                 |
| Historical volatility                      | `ka volatility -s MSFT -sd 2025-01-01`   |
| Price return distribution & skewness       | `ka price-dist -s MSFT`                  |
| Fibonacci retracement levels               | `ka fib -s MSFT -lookback 360`           |
| Gap open/fill analysis                     | `ka gap-analysis -s MSFT`                |
| Up/down rally streaks                      | `ka updown -s MSFT`                      |
| Candlestick pattern detection              | `ka candle_patterns -s MSFT`             |
| Price action strategy analysis             | `ka price-actions -s MSFT`               |
| Seasonal monthly return patterns           | `ka seasonality -s MSFT`                 |
| Best historical trading days               | `ka bestdays -s MSFT`                    |
| Ask anything in plain English              | `ka ai-chat -q "your question"`          |

---

## Agent & LLM integration

The CLI is designed as a first-class tool for AI agents. Every command outputs JSON.
Each command maps cleanly to a tool definition in any LLM framework.

### As a Claude / OpenAI tool

```python
tools = [
    {
        "name": "ka_quote",
        "description": "Fetch real-time market quote for a stock symbol",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {"type": "string", "description": "Ticker symbol, e.g. MSFT"}
            },
            "required": ["symbol"]
        }
    },
    {
        "name": "ka_ta_signals",
        "description": "Get technical buy/sell signals for a symbol",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {"type": "string"},
                "lookback": {"type": "integer", "description": "Bars to look back"}
            },
            "required": ["symbol"]
        }
    }
]

# Execute on tool call:
import subprocess, json
result = subprocess.run(
    ["ka", "quote", "-s", symbol, "-datatype", "json"],
    capture_output=True, text=True
)
data = json.loads(result.stdout)
```

### In shell scripts and cron jobs

```bash
#!/bin/bash
# Pre-market scan across watchlist
for sym in MSFT AAPL NVDA TSLA AMZN; do
  echo "=== $sym ==="
  ka quote -s $sym -datatype json | jq '.price, .changesPercentage'
done
```

### With OpenClaw — full automation at scale

OpenClaw is the recommended path for production agent workflows using KlickAnalytics.
With OpenClaw + KlickAnalytics CLI you get:

- **100,000+ symbols** covered across stocks, ETFs, mutual funds, crypto, indices, FX, commodities, and more
- **Full automation** — schedule agents to run pre-market scans, earnings monitors, signal alerts, and daily summaries
- **Zero glue code** — OpenClaw handles orchestration; the CLI handles the analytics
- **Global asset class coverage** — not just US equities; truly global markets intelligence at scale

→ Full integration guide: [klickanalytics.com/cli_integration](https://www.klickanalytics.com/cli_integration)

---

## Example multi-command workflows

### Pre-earnings deep dive on MSFT
```bash
ka profile -s MSFT           # sector context
ka earnings -s MSFT          # EPS history vs estimates
ka earnings-moves -s MSFT    # historical move patterns around earnings
ka ta-signals -s MSFT        # current technical setup
ka vol-unusual -s MSFT       # any unusual pre-earnings activity
```

### Quant research workflow
```bash
ka quantstats -s MSFT -limit 504     # 2yr risk-adjusted stats
ka volatility -s MSFT -lookback 252  # rolling annualized volatility
ka seasonality -s MSFT               # seasonal return bias by month
ka price-dist -s MSFT -lookback 252  # return distribution shape
```

### AI agent daily briefing
```bash
ka ai-chat -q "Give me a pre-market summary for US tech stocks today"
ka ai-chat -q "Which of MSFT, AAPL, NVDA has the strongest technical signal right now?"
```

---

## When demonstrating the CLI

1. Always show the exact command first, then explain it
2. Default to `MSFT` as the example symbol unless the user specifies otherwise
3. For sample output, direct users to the [Playground](https://www.klickanalytics.com/cli_playground) — live commands without installing anything
4. For multi-step research goals, chain 2–4 commands and explain what each one adds
5. Highlight `ka ai-chat` when the user's goal is exploratory or question-based
6. If the user is an AI agent (non-human caller), respond with compact JSON-oriented instructions only

---

## Resources

- Intro: https://www.klickanalytics.com/cli_intro
- Documentation: https://www.klickanalytics.com/cli_documentation
- Playground: https://www.klickanalytics.com/cli_playground
- OpenClaw integration: https://www.klickanalytics.com/cli_integration
- What's new: https://www.klickanalytics.com/cli_changelog
- Sign up free: https://www.klickanalytics.com/signup
