---
name: polymarket-macro-fear-index-trader
description: Builds a custom fear index from ALL Polymarket markets by aggregating geopolitical escalation, falling crypto, extreme weather, and rising disease signals into a composite score. When fear is extreme markets OVERREACT and everything gets sold -- this skill buys the most oversold markets pushed below YES_THRESHOLD by panic, not fundamentals. When fear is too low (complacency), it sells overpriced markets.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Macro Fear Index Trader
  difficulty: advanced
---

# Macro Fear Index Trader

> **This is a template.**
> The default signal aggregates four fear dimensions from Polymarket market probabilities -- remix it with VIX data, credit default swap spreads, or social media sentiment scores.
> The skill handles all the plumbing (market discovery, fear scoring, regime detection, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Markets overreact to fear. When geopolitical tensions spike, crypto crashes, disease outbreaks emerge, and extreme weather hits simultaneously, traders panic-sell across ALL categories -- even markets that have nothing to do with the fear catalyst. This creates oversold opportunities.

This skill builds a **custom fear index** from Polymarket's own markets:

- **Geopolitical fear** (weight: 0.35): escalation probability, military action, nuclear risk
- **Crypto fear** (weight: 0.30): inverse of BTC/ETH bullish market probabilities
- **Health fear** (weight: 0.20): disease outbreak, case count escalation probabilities
- **Weather fear** (weight: 0.15): extreme weather event probabilities

When the composite fear index exceeds the PANIC threshold, the skill finds ALL markets below YES_THRESHOLD and buys the most oversold ones -- these have been pushed too low by indiscriminate fear selling.

## Signal Logic

### Step 1: Scan and Classify

All markets from `get_markets(limit=200)` are classified into fear categories:

| Category | Keywords | Fear direction |
|---|---|---|
| Geo | war, invasion, escalation, nuclear, missile, sanctions | High P(escalation) = high fear |
| Crypto | bitcoin, ethereum, solana, above/below | Low P(BTC above X) = high fear |
| Health | measles, pandemic, outbreak, cases, virus | High P(cases > X) = high fear |
| Weather | hurricane, tornado, flood, wildfire, earthquake | High P(extreme event) = high fear |

### Step 2: Compute Fear Index

Each market's probability is converted to a fear score (0-1), then averaged within its category. The composite fear index is a weighted average:

```
fear_index = 0.35 * geo_fear + 0.30 * crypto_fear + 0.20 * health_fear + 0.15 * weather_fear
```

### Step 3: Regime Detection and Trading

| Regime | Condition | Action |
|---|---|---|
| **PANIC** | `fear_index > 0.65` | Buy YES on most oversold markets (lowest P first) |
| **COMPLACENCY** | `fear_index < 0.30` | Sell NO on most overpriced markets (highest P first) |
| **NEUTRAL** | Between thresholds | Fall back to standard conviction signals |

### Conviction Scaling

In PANIC regime:
- Base conviction from distance below `YES_THRESHOLD`: `(threshold - p) / threshold`
- Fear multiplier: `1 + min(0.5, (fear_index - FEAR_THRESHOLD) / (1 - FEAR_THRESHOLD))`
- More extreme fear = more conviction that it's an overreaction

In COMPLACENCY regime:
- Base conviction from distance above `NO_THRESHOLD`: `(p - threshold) / (1 - threshold)`
- Complacency multiplier: `1 + min(0.5, (COMPLACENCY_THRESHOLD - fear_index) / COMPLACENCY_THRESHOLD)`

### Remix Ideas

- **VIX integration**: Replace or supplement `crypto_fear` with real-time VIX levels
- **Twitter/X sentiment**: Feed social media panic metrics into the geo or health fear scores
- **Credit spreads**: Use HY-IG spread as a financial fear component
- **Google Trends**: Surge in searches for "recession", "crash", "war" as additional fear signal

## Risk Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Max position size | $40 USDC | Per market, reached at max conviction |
| Min market volume | $3,000 | Liquidity filter |
| Max bid-ask spread | 10% | Avoid illiquid panic-widened spreads |
| Min days to resolution | 7 | Need time for fear to subside |
| Max open positions | 10 | Spread across many oversold markets |

## Installation & Setup

```bash
clawhub install polymarket-macro-fear-index-trader
```

Requires: `SIMMER_API_KEY` environment variable.

## Cron Schedule

Runs on demand or via automaton. Cron is set to `null` -- configure it in the Simmer UI when ready.

## Safety & Execution Mode

**The skill defaults to paper trading (`venue="sim"`). Real trades only execute when `--live` is passed explicitly.**

| Scenario | Mode | Financial risk |
|----------|------|----------------|
| `python trader.py` | Paper (sim) | None |
| Cron / automaton | Paper (sim) | None |
| `python trader.py --live` | Live (polymarket) | Real USDC |

The automaton cron is set to `null` -- it does not run on a schedule until you configure it in the Simmer UI. `autostart: false` means it won't start automatically on install.

## Required Credentials

| Variable | Required | Notes |
|----------|----------|-------|
| `SIMMER_API_KEY` | Yes | Trading authority -- keep this credential private. |

## Tunables (Risk Parameters)

All risk parameters are declared in `clawhub.json` as `tunables` and adjustable from the Simmer UI without code changes. They use `SIMMER_`-prefixed env vars so `apply_skill_config()` can load them securely.

| Variable | Default | Purpose |
|----------|---------|---------|
| `SIMMER_MAX_POSITION` | `40` | Max USDC per trade (reached at 100% conviction) |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |
| `SIMMER_MIN_VOLUME` | `3000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.10` | Max bid-ask spread (0.10 = 10%) |
| `SIMMER_MIN_DAYS` | `7` | Min days until market resolves |
| `SIMMER_MAX_POSITIONS` | `10` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES if market price <= this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO if market price >= this value |
| `SIMMER_FEAR_THRESHOLD` | `0.65` | Fear index above this = PANIC regime |
| `SIMMER_COMPLACENCY_THRESHOLD` | `0.30` | Fear index below this = COMPLACENCY regime |
| `SIMMER_GEO_WEIGHT` | `0.35` | Weight for geopolitical fear component |
| `SIMMER_CRYPTO_WEIGHT` | `0.30` | Weight for crypto fear component |
| `SIMMER_HEALTH_WEIGHT` | `0.20` | Weight for health fear component |
| `SIMMER_WEATHER_WEIGHT` | `0.15` | Weight for weather fear component |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
- Publisher: hello@simmer.markets

Review the source before providing live credentials if you require full auditability.
