---
name: market-news-brief
description: "Run a local script to fetch broad market news and tone. Use when: user asks about market conditions, macro news, what's happening in markets, or market sentiment for any region. Invoke by reading this SKILL.md then running: uv run /root/.openclaw/workspace/skills/market-news-brief/src/main.py <SCOPE>"
homepage: https://finance.yahoo.com
metadata: {"clawdbot":{"emoji":"📰","requires":{"bins":["uv"]}}}
---

# Skill: Market News Brief

## When to use
- The user wants to understand current market sentiment and news trends.
- The user wants broad market news and macro tone for a region or country.
- The user asks "what's happening in the market?" or "any market news today?"
- The user asks about US markets, European markets, Asian markets, or global markets.
- The user wants a news digest before making a trading or investment decision.

## When NOT to use
- The user wants the current price of a specific stock → use `stock-price-checker-pro`
- The user wants fundamentals (P/E, EPS, margins) for a company → use `stock-fundamentals`
- The user wants a full equity research report → use `equity-research`

## ⚠️ Critical: Scope Words Only

This skill takes a **market scope word** as its argument — NOT a company ticker.
Passing `AAPL`, `TSLA`, or any bare ticker symbol will cause an error.
Always map the user's intent to a scope word from the table below.

### Valid Scopes

| Scope         | Coverage                                            |
|---------------|-----------------------------------------------------|
| `GLOBAL`      | All regions combined (default if nothing specified) |
| `US`          | S&P 500, Nasdaq 100, Dow Jones, Russell 2000, VIX   |
| `EUROPE`      | UK + Germany + Netherlands combined                 |
| `UK`          | FTSE 100                                            |
| `GERMANY`     | DAX                                                 |
| `NETHERLANDS` | AEX / Euronext                                      |
| `ASIA`        | Japan + South Korea combined                        |
| `JAPAN`       | Nikkei 225                                          |
| `SOUTH_KOREA` | KOSPI                                               |

## Commands

### Get broad market news

```bash
uv run /root/.openclaw/workspace/skills/market-news-brief/src/main.py <SCOPE>
```

### Examples

```bash
# Global overview (default — use when no region is specified)
uv run /root/.openclaw/workspace/skills/market-news-brief/src/main.py GLOBAL

# US markets
uv run /root/.openclaw/workspace/skills/market-news-brief/src/main.py US

# European markets (covers UK, Germany, Netherlands)
uv run /root/.openclaw/workspace/skills/market-news-brief/src/main.py EUROPE

# Specific countries
uv run /root/.openclaw/workspace/skills/market-news-brief/src/main.py GERMANY
uv run /root/.openclaw/workspace/skills/market-news-brief/src/main.py UK
uv run /root/.openclaw/workspace/skills/market-news-brief/src/main.py JAPAN

# Asian markets
uv run /root/.openclaw/workspace/skills/market-news-brief/src/main.py ASIA
```

## Output

The command returns a formatted summary including:
- Index / ETF snapshot for the selected scope (price, change, % change)
- Market tone assessment (risk-on / risk-off / neutral)
- Dominant news themes (e.g. Central banks, Inflation, Tech, Energy, Geopolitics)
- Top headlines with source, publish timestamp, and link

## Notes

- Uses `uv run` internally — no manual pip install or venv setup needed.
- Do NOT pass a bare company ticker (e.g. `AAPL`) — it will error. Use scope words only.
- For a user asking about a German stock like `RHM.DE`, use `EUROPE` or `GERMANY` for market context.
- Do NOT use web search or curl to fetch market news — always use this script.
- Do NOT use the `market-news.sh` wrapper — call `uv run src/main.py` directly as shown above.