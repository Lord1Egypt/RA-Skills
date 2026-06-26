---
name: polymarket-sports-live-trader
description: Trades Polymarket prediction markets on sports championships, tournament outcomes, MVP awards, transfer windows, and season milestones. Use when you want to capture alpha on sports markets using league table data, injury reports, and Elo rating signals.
metadata:
  author: Diagnostikon
  version: "1.0"
  displayName: Sports & Championships Trader
  difficulty: intermediate
---

# Sports & Championships Trader

> **This is a template.**
> The default signal is keyword-based market discovery combined with probability-extreme detection — remix it with the data sources listed in the Edge Thesis below.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Sports prediction markets are dominated by passionate fans who bet emotionally. This creates two structural edges this skill exploits without any external API:

1. **Fan loyalty dampening** — Popular clubs (Real Madrid, Man City, Lakers) are systematically overpriced by emotional retail traders
2. **Sports calendar timing** — Each sport has a defined peak season; trading in-season means better signal density

## Signal Logic

### Default Signal: Conviction-Based Sizing with Fan Bias + Calendar

1. Discover active sports markets on Polymarket
2. Compute base conviction from distance to threshold (0% at boundary → 100% at p=0/p=1)
3. Apply `sport_bias()` — combines fan loyalty adjustment with sports calendar timing
4. Size = `max(MIN_TRADE, conviction × bias × MAX_POSITION)` — capped at MAX_POSITION
5. Skip markets with spread > MAX_SPREAD or fewer than MIN_DAYS to resolution

### Sport Bias (built-in, no API required)

**Factor 1 — Fan Loyalty Adjustment**

| Market type | Multiplier | Why |
|---|---|---|
| Fan-favorite clubs (Real Madrid, Man City, Lakers) | **0.75x** | Fan loyalty inflates YES — high noise, trade cautiously |
| Peak fan events (Super Bowl, UCL final, World Cup final) | **0.80x** | Maximum emotional retail attention = maximum mispricing |
| Individual sports (tennis, F1, golf) | **1.15x** | Individual performance is more data-driven than team sports |
| Transfer / contract markets | **1.20x** | Journalist sources trackable before market reprices |
| Award markets (MVP, Ballon d'Or, Golden Boot) | **1.10x** | Stats-driven — quantifiable advantage |

**Factor 2 — Sports Calendar Timing**

| Sport / Event | Active season | In-season multiplier |
|---|---|---|
| Football title run-in (UCL, PL, Liga) | Mar–May | **1.15x** |
| Transfer windows | Jan + Jun–Sep | **1.20x** |
| NBA playoffs | Apr–Jun | **1.15x** |
| NFL season | Sep–Feb | **1.10x** |
| Tennis / Wimbledon | Jun–Sep | **1.15x** |

Combined and capped at **1.35x**. Example: Transfer market in July → 1.20 × 1.20 = 1.35x (capped).

### Remix Signal Ideas

- **Club Elo**: Replace `market.current_probability` with Elo-implied win probability — trade divergence vs market
- **FiveThirtyEight NBA/NFL models**: Same divergence approach for American sports
- **Transfermarkt API**: Player valuations and injury status as signal inputs
- **ESPN hidden API**: `https://site.api.espn.com/apis/site/v2/sports/{sport}/{league}/scoreboard` for live scores/injury data


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
| `SIMMER_MAX_POSITION` | `25` | Max USDC per trade (reached at 100% conviction) |
| `SIMMER_MIN_VOLUME` | `5000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.08` | Max bid-ask spread (8%) |
| `SIMMER_MIN_DAYS` | `2` | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | `8` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES if market price ≤ this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO if market price ≥ this value |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
