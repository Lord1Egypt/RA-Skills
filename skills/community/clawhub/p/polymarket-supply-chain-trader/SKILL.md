---
name: polymarket-supply-chain-trader
description: Trades Polymarket prediction markets focused on supply chain disruptions, port congestion, shipping delays, commodity prices, and logistics outcomes. Use when you want to capture alpha on global trade flow events, raw material price markets, and demand spike predictions.
metadata:
  author: Diagnostikon
  version: '1.0'
  displayName: Supply Chain & Logistics Trader
  difficulty: intermediate
---

# Supply Chain & Logistics Trader

> **This is a template.**  
> The default signal is keyword-based market discovery (shipping, port, logistics, commodity, supply chain) — remix it with freight index APIs (Baltic Dry Index), satellite AIS vessel tracking data, or real-time port authority feeds.  
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Supply chain prediction markets are among the most underserved categories on Polymarket. This skill identifies and trades markets related to:

- **Port congestion** — Rotterdam, Suez Canal, LA/Long Beach delays
- **Commodity prices** — Brent crude, steel, lithium thresholds
- **Demand spikes** — GPU/chip shortages, EV battery supply
- **Company logistics** — Tesla delivery delays, Maersk shipping times, Amazon Prime SLAs

Research shows prediction markets can reduce supply chain forecasting errors by 20–50% vs traditional methods (CFTC data). This makes these markets both tradable AND informative.

## Signal Logic

### Default Signal: Conviction-Based Sizing with Disruption Bias

1. Discover active supply chain markets on Polymarket
2. Compute base conviction from distance to threshold (0% at boundary → 100% at p=0/p=1)
3. Apply `disruption_bias()` — combines seasonal shipping cycles with commodity predictability
4. Size = `max(MIN_TRADE, conviction × bias × MAX_POSITION)` — capped at MAX_POSITION
5. Skip markets with spread > MAX_SPREAD or fewer than MIN_DAYS to resolution

### Disruption Bias (built-in, no API required)

`disruption_bias()` multiplies conviction using two independent factors simultaneously:

**Factor 1 — Seasonal Shipping Cycle**

Container shipping has a well-documented Q4 crunch (Oct–Dec) driven by pre-holiday inventory builds. Congestion and delay markets are structurally more likely to resolve YES in peak season.

| Period | Multiplier | Why |
|---|---|---|
| Q4: Oct–Dec | **1.25x** | Peak season — pre-holiday crunch, port congestion likely |
| Q1: Jan–Mar | **0.85x** | Off-season — lower disruption probability |
| Apr–Sep | **1.05x** | Mild mid-year activity |

*Only applied when the question contains shipping/port/freight/cargo keywords.*

**Factor 2 — Commodity Predictability**

| Commodity type | Multiplier | Why |
|---|---|---|
| Crude oil / energy / LNG | **1.20x** | Most liquid commodity — highly modeled, information-rich |
| Semiconductors / chips / GPU | **1.15x** | Documented cycles, policy-driven — trackable |
| Lithium / cobalt / EV battery | **1.15x** | China-concentrated supply — export data publicly trackable |
| Chokepoints (Suez, Red Sea, Panama) | **1.10x** | Geopolitical risk well-documented and persistent |
| Agricultural / grain / harvest | **0.85x** | Weather-dependent, high variance — hard to model |

Combined multiplier capped at **1.40x**. A Q4 container shipping market mentioning Suez would score 1.25 × 1.10 = 1.375x.

### Remix Ideas

- **Baltic Dry Index**: BDI weekly change as direct conviction input — rising BDI = lean into shipping disruption YES
- **AIS vessel tracking (MarineTraffic)**: Real vessel queue counts at LA/Long Beach as direct oracle for port congestion markets
- **USDA crop reports**: Trade agricultural supply markets in the 48h window before/after report release
- **Port authority RSS feeds**: Rotterdam, Singapore, Shanghai real-time congestion data as entry trigger

## Market Categories Tracked

```python
KEYWORDS = [
    'shipping', 'port', 'container', 'supply chain', 'logistics',
    'commodity', 'crude oil', 'Brent', 'natural gas', 'LNG',
    'steel price', 'lithium', 'cobalt', 'critical mineral',
    'semiconductor', 'chip shortage', 'TSMC', 'GPU',
    'delivery delay', 'Maersk', 'Rotterdam', 'Suez', 'Panama Canal',
    'Red Sea', 'freight', 'Baltic Dry', 'EV battery',
]
```

## Risk Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Max position size | $25 USDC | Per market |
| Min market volume | $5,000 | Liquidity filter |
| Max bid-ask spread | 10% | Slippage guard |
| Min days to resolution | 7 | Avoid last-minute noise |
| Max open positions | 5 | Concentration limit |

## Installation & Setup

```bash
clawhub install polymarket-supply-chain-trader
```

Requires: `SIMMER_API_KEY` environment variable.

## Cron Schedule

Runs every 15 minutes (`*/15 * * * *`). Markets are slow-moving enough that high-frequency execution is unnecessary.

## Safety & Execution Mode

**The skill defaults to paper trading (`venue="sim"`). Real trades only execute when `--live` is passed explicitly.**

| Scenario | Mode | Financial risk |
|----------|------|----------------|
| `python trader.py` | Paper (sim) | None |
| Cron / automaton | Paper (sim) | None |
| `python trader.py --live` | Live (polymarket) | Real USDC |

The automaton cron is set to `null` — it does not run on a schedule until you configure it in the Simmer UI. `autostart: false` means it won't start automatically on install.

## Required Credentials

| Variable | Required | Notes |
|----------|----------|-------|
| `SIMMER_API_KEY` | Yes | Trading authority — keep this credential private. Do not place a live-capable key in any environment where automated code could call `--live`. |

## Tunables (Risk Parameters)

All risk parameters are declared in `clawhub.json` as `tunables` and adjustable from the Simmer UI without code changes. They use `SIMMER_`-prefixed env vars so `apply_skill_config()` can load them securely.

| Variable | Default | Purpose |
|----------|---------|---------|
| `SIMMER_MAX_POSITION` | `25` | Max USDC per trade (reached at 100% conviction) |
| `SIMMER_MIN_VOLUME` | `5000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.10` | Max bid-ask spread (0.10 = 10%) |
| `SIMMER_MIN_DAYS` | `7` | Min days until market resolves |
| `SIMMER_MAX_POSITIONS` | `5` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES if market price ≤ this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO if market price ≥ this value |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
- Publisher: hello@simmer.markets

Review the source before providing live credentials if you require full auditability.
