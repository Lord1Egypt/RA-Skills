---
name: polymarket-multi-source-estimator
description: >
  Trade prediction markets using LLM probability estimation enriched with 10+
  real-time data sources (news, economic data, sports odds, political polling,
  and more). The skill fetches context from RSS feeds, FRED, GDELT, bookmaker
  odds, and other APIs, then asks an LLM to estimate the true probability.
  Trades when the estimate diverges significantly from the market price.
metadata:
  author: Mibayy
  version: 1.1.4
  displayName: Multi-Source LLM Estimator
  type: "automaton"
  difficulty: advanced
---

# Multi-Source LLM Estimator

A prediction market trading bot that enriches an LLM with real-time context
from 10+ data sources. It compares the LLM's estimated probability against
the current market price and trades when it detects significant mispricing.

## How It Works

```
10+ Data Sources --> Context String --> LLM Prompt --> Probability Estimate
                                                              |
                                                    Compare vs Market Price
                                                              |
                                              Trade if divergence > threshold
```

1. Fetches active markets from Polymarket (via Simmer SDK)
2. For each market, gathers real-time context from relevant data sources
3. Also checks cross-platform prices on Manifold and Kalshi
4. Sends the question + context to an LLM for probability estimation
5. If the LLM's estimate diverges from the market price by more than the
   threshold (default 15%), it places a trade

## Data Sources

| # | Source | What It Provides | API Key Required |
|---|--------|-------------------|------------------|
| 1 | **RSS News** | Headlines from 10 feeds (Reuters, BBC, Bloomberg, etc.) | No |
| 2 | **FRED** | Economic indicators (Fed rate, CPI, GDP, VIX, oil, gold) | Yes (free) |
| 3 | **GDELT** | Geopolitical event sentiment scores | No |
| 4 | **Odds API** | Sports bookmaker consensus probabilities | Yes (free tier) |
| 5 | **FiveThirtyEight** | US presidential approval polling averages | No |
| 6 | **Congress.gov** | Bill status and legislative tracking | Yes (free) |
| 7 | **OpenFDA** | Drug approval status and clinical trial data | No |
| 8 | **Open-Meteo** | Weather forecasts for major cities | No |
| 9 | **USGS** | Significant earthquake data | No |
| 10 | **Finnhub** | Earnings calendar and IPO data | Yes (free) |
| 11 | **Manifold** | Cross-platform prediction market prices | No |
| 12 | **Kalshi** | Cross-platform prediction market prices | No |

Sources are selected automatically based on category detection from the
question text. Only relevant sources are queried to minimize latency.

## Remixable Template

This skill is designed as a template you can customize:

- **Add your own data source**: Implement a `_get_X_context(question)` function
  that returns a `list[str]` of context lines. Add it to `_dispatch_sources()`.
- **Swap the LLM**: Set `LLM_API_URL` and `LLM_MODEL` env vars to point at
  any OpenAI-compatible API (OpenRouter, Ollama, vLLM, etc.).
- **Adjust the threshold**: Set `ESTIMATOR_THRESHOLD` higher for fewer but
  higher-conviction trades, or lower for more frequent trading.
- **Change the prompt**: Edit the `_build_prompt()` function to customize
  the LLM's reasoning style.

## Environment Variables

### Required

| Variable | Description |
|----------|-------------|
| `SIMMER_API_KEY` | Simmer SDK API key for trading |
| `LLM_API_KEY` | API key for your LLM provider (default: OpenRouter) |

### Optional

| Variable | Default | Description |
|----------|---------|-------------|
| `TRADING_VENUE` | `sim` | Trading venue (`sim` for paper, `polymarket` for real) |
| `TRADE_SIZE` | `10.0` | Trade size in USD per trade |
| `LLM_API_URL` | OpenRouter endpoint | OpenAI-compatible chat completions URL |
| `LLM_MODEL` | `xiaomi/mimo-v2-flash:free` | Model identifier |
| `ESTIMATOR_THRESHOLD` | `0.15` | Min divergence to trigger a trade (0.0-1.0) |
| `FRED_API_KEY` | — | FRED API key (free at api.stlouisfed.org) |
| `ODDS_API_KEY` | — | The Odds API key (free at the-odds-api.com) |
| `CONGRESS_API_KEY` | — | Congress.gov API key (free) |
| `FINNHUB_API_KEY` | — | Finnhub API key (free tier) |
| `LLM_CACHE_TTL` | `1800` | LLM response cache TTL in seconds |
| `LLM_MAX_CALLS` | `50` | Max LLM calls per run |

## Usage

Dry-run (no trades, just log estimates):
```bash
python multi_source_estimator.py
```

Live trading:
```bash
python multi_source_estimator.py --live
```

Quiet mode (errors only):
```bash
python multi_source_estimator.py --live --quiet
```

Limit markets scanned:
```bash
python multi_source_estimator.py --live --max-markets 20
```

## Scheduling

Runs every 5 minutes via cron (`*/5 * * * *`). Managed automaton (auto-executes on schedule).
Capped at 50 LLM calls per run (`LLM_MAX_CALLS`) to control costs.

## Security

- All trades go through `SimmerClient.trade()` only. No direct CLOB or wallet access.
- Dry-run by default. The `--live` flag must be explicitly passed to execute trades.
- No wallet private keys are required or read by this script.
- LLM receives only the market question text and publicly available context (news headlines, economic indicators, odds). No credentials or private data are sent to the LLM.
- `LLM_API_URL` defaults to OpenRouter. You control which LLM endpoint is used.
- All optional API keys (FRED, Odds, Congress, Finnhub) are for free public data APIs. If unset, those data sources are simply skipped.
