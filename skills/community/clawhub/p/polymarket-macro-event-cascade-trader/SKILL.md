---
name: polymarket-macro-event-cascade-trader
description: Trades 2nd and 3rd order effects from nearly-resolved Polymarket events. When a major geopolitical, crypto, or weather event resolves, downstream markets (oil, equities, crypto) take hours to fully reprice. This skill identifies the cascade chain and trades the lagging targets before they catch up.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Macro Event Cascade Trader
  difficulty: advanced
---

# Macro Event Cascade Trader

> **This is a template.**
> The default signal trades cascade lag from nearly-resolved trigger events to downstream target markets -- remix it with real-time news feeds, order-flow data, or cross-venue latency analysis.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

When a major event resolves on Polymarket, the repricing does not happen all at once. First-order effects (the directly related markets) reprice within minutes. But second and third-order effects -- the markets connected through economic or geopolitical transmission channels -- take hours to fully adjust.

Example cascade: Iran ceasefire resolves YES ->
1. **1st order (immediate):** Geopolitics markets reprice
2. **2nd order (30min-2h):** Oil drops, BTC rises
3. **3rd order (2h-8h):** Equity/recession markets rise

This skill scans all markets, identifies triggers that are nearly resolved (p > 90% or p < 10%, or resolving within 24h), maps the expected cascade chain, and trades the downstream targets that have NOT yet repriced.

## Edge Thesis

Prediction market participants are specialists. The person trading Iran ceasefire markets is not the same person trading BTC or oil markets. Cross-asset repricing requires information to travel between siloed participant pools. This creates a structural lag that is largest for 3rd-order effects and during off-hours when fewer participants are active.

The edge is not in predicting the trigger event. The edge is in being faster than cross-asset information flow.

## Signal Logic

### 1. Trigger Detection

Scan all markets and identify nearly-resolved events:
- Probability > 90% or < 10% (market has effectively decided)
- Resolution within 24 hours and probability > 50% or < 50%

### 2. Event Classification

Classify each trigger into a category: geopolitics, crypto, commodity, health, weather, equity. For geopolitics, further classify as escalation or de-escalation.

### 3. Cascade Chain Mapping

Predefined cascade chains map trigger signals to expected target movements:

| Trigger | 2nd Order | 3rd Order |
|---|---|---|
| Geo escalation YES | Oil UP, Crypto DOWN | Equity DOWN |
| Geo de-escalation YES | Oil DOWN, Crypto UP | Equity UP |
| Crypto milestone UP | Equity UP | |
| Weather extreme YES | Commodity UP | |
| Health outbreak YES | Equity DOWN, Commodity UP | |

### 4. Lag Detection

For each cascade target, measure how much it has NOT moved in the expected direction. A target sitting at 35% when the cascade says it should go UP has a lag of 15% (from the 50% midpoint). Only trade targets where lag exceeds `CASCADE_LAG` threshold.

### 5. Conviction-Based Sizing

All trades use the standard conviction formula:

- **YES**: `conviction = (YES_THRESHOLD - p) / YES_THRESHOLD`, boosted by cascade lag
- **NO**: `conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)`, boosted by cascade lag
- **Size**: `max(MIN_TRADE, conviction * MAX_POSITION)`

## Remix Ideas

- Add real-time news API to confirm trigger events before trading cascade
- Weight cascade strength by trigger market volume (bigger trigger = stronger cascade)
- Add time-decay: cascade signal weakens as hours pass since trigger detection
- Cross-venue arbitrage: check Kalshi/Metaculus for cascade lag confirmation
- Add order-book depth analysis to estimate how much repricing is left

## Safety & Execution Mode

**The skill defaults to paper trading (`venue="sim"`). Real trades only with `--live` flag.**

| Scenario | Mode | Financial risk |
|---|---|---|
| `python trader.py` | Paper (sim) | None |
| Cron / automaton | Paper (sim) | None |
| `python trader.py --live` | Live (polymarket) | Real USDC |

`autostart: false` and `cron: null` mean nothing runs automatically until configured in Simmer UI.

## Required Credentials

| Variable | Required | Notes |
|---|---|---|
| `SIMMER_API_KEY` | Yes | Trading authority. Treat as a high-value credential. |

## Tunables (Risk Parameters)

All declared as `tunables` in `clawhub.json` and adjustable from the Simmer UI.

| Variable | Default | Purpose |
|---|---|---|
| `SIMMER_MAX_POSITION` | `40` | Max USDC per trade at full conviction |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade |
| `SIMMER_MIN_VOLUME` | `10000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.07` | Max bid-ask spread |
| `SIMMER_MIN_DAYS` | `3` | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | `6` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES only if market probability <= this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO only if market probability >= this value |
| `SIMMER_CASCADE_LAG` | `0.08` | Min lag (from 50% midpoint) before trading a cascade target |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
