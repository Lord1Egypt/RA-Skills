---
name: polymarket-real-estate-trader
description: Trades Polymarket prediction markets on housing prices, mortgage rates, Fed rate decisions, real estate crash scenarios, and regional property market milestones. Use when you want to capture alpha on macro housing markets using Fed minutes, Case-Shiller data, and mortgage rate signals.
metadata:
  author: Diagnostikon
  version: "1.0"
  displayName: Real Estate & Housing Trader
  difficulty: intermediate
---

# Real Estate & Housing Trader

> **This is a template.**
> The default signal is keyword-based market discovery combined with probability-extreme detection — remix it with the data sources listed in the Edge Thesis below.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Housing and Fed rate markets are priced by retail traders following mainstream media narratives. This skill exploits two structural edges without any external API:

1. **FOMC calendar timing** — Rate markets diverge most from CME FedWatch in the weeks *before* a meeting. Trading the pre-meeting window captures the professional vs retail pricing gap.
2. **Market type confidence** — Fed/rate decisions are professionally calibrated; crash/bubble markets are emotionally driven. Position sizing reflects this.

## Signal Logic

### Default Signal: Conviction-Based Sizing with Macro Cycle Bias

1. Discover active housing and rate markets on Polymarket
2. Compute base conviction from distance to threshold (0% at boundary → 100% at p=0/p=1)
3. Apply `macro_cycle_bias()` — combines FOMC month timing with market type confidence
4. Size = `max(MIN_TRADE, conviction × bias × MAX_POSITION)` — capped at MAX_POSITION
5. Skip markets with spread > MAX_SPREAD or fewer than MIN_DAYS to resolution

### Macro Cycle Bias (built-in, no API required)

**Factor 1 — FOMC Calendar Timing**

Fed rate decision markets have their highest edge in the 2–4 weeks BEFORE a meeting — when CME FedWatch (professional market) and Polymarket (retail) diverge most. After the decision, repricing happens within hours.

FOMC meets ~8x/year: **Jan, Mar, May, Jun, Jul, Sep, Nov, Dec**

| Condition | Multiplier |
|---|---|
| Rate question in FOMC-active month | **1.2x** — pre-meeting window, edge at its peak |
| Rate question in gap month (Apr, Aug, Oct) | **0.9x** — fewer catalysts |

**Factor 2 — Market Type Confidence**

| Market type | Multiplier | Why |
|---|---|---|
| Fed/FOMC rate decisions | **1.25x** | CME FedWatch = professional-grade calibration |
| Mortgage rate markets | **1.15x** | Mechanically tied to Fed funds — directionally predictable |
| Case-Shiller / price index | **1.10x** | Data-driven index releases — trackable trajectory |
| Housing crash / bubble / collapse | **0.75x** | Fear/narrative-driven — hard to time, high variance |
| Commercial RE / office vacancy | **0.80x** | WFH narrative distorts rational pricing |

Combined capped at **1.40x**. A Fed rate cut market in March → 1.2 × 1.25 = **1.40x** (cap) — maximum edge. A "housing bubble crash" question → 1.0 × 0.75 = **0.75x** — trade very conservatively.

### Remix Signal Ideas

- **CME FedWatch**: Replace `market.current_probability` with FedWatch implied probability — trade the divergence between professional futures and Polymarket retail pricing
- **FRED API**: Federal Reserve economic data releases as leading signal for rate trajectory
- **Case-Shiller releases**: Track monthly index trajectory to front-run known lagged data
- **Zillow / Redfin Research**: Regional data as leading indicator for national market questions


## Safety & Execution Mode

**The skill defaults to paper trading (`venue="sim"`). Real trades only with `--live` flag.**

| Scenario | Mode | Financial risk |
|---|---|---|
| `python trader.py` | Paper (sim) | None |
| Cron / automaton | Paper (sim) | None |
| `python trader.py --live` | Live (polymarket) | Real USDC |

`autostart: false` and `cron: null` — nothing runs automatically until you configure it in Simmer UI.

## Required Credentials

| Variable | Required | Notes |
|---|---|---|
| `SIMMER_API_KEY` | Yes | Trading authority. Treat as high-value credential. |

## Tunables (Risk Parameters)

All declared as `tunables` in `clawhub.json` and adjustable from the Simmer UI.

| Variable | Default | Purpose |
|---|---|---|
| `SIMMER_MAX_POSITION` | `30` | Max USDC per trade (reached at 100% conviction) |
| `SIMMER_MIN_VOLUME` | `8000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.08` | Max bid-ask spread (8%) |
| `SIMMER_MIN_DAYS` | `7` | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | `6` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES if market price ≤ this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO if market price ≥ this value |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
