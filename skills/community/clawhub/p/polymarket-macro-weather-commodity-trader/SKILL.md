---
name: polymarket-macro-weather-commodity-trader
description: Trades commodity markets based on extreme weather signals. When temperature markets show unusual readings (extreme heat or cold), it signals potential energy demand spikes or crop disruption that commodity markets have not yet priced in.
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Weather-Commodity Trader
  difficulty: advanced
---

# Weather-Commodity Trader

> **This is a template.**
> The default signal maps extreme weather readings to commodity market mispricings -- remix it with NOAA API data, satellite crop imagery, or energy grid load forecasts.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Extreme weather is a leading indicator for commodity disruption, but the transmission from weather prediction markets to commodity prediction markets is slow. Weather specialists trade temperature markets. Commodity traders watch OPEC and inventory reports. Few participants systematically connect the two.

This skill bridges that gap:

1. Scan Polymarket temperature/weather markets for stress signals
2. Compute weather stress: are temperatures showing extremes that imply energy or crop disruption?
3. Check commodity markets: have they already priced in the weather stress?
4. Trade commodity markets that are lagging behind the weather signal

## Edge Thesis

Weather-to-commodity transmission has a structural delay on prediction markets because:

- **Different participant pools:** Weather market traders are weather nerds; commodity traders watch financial news
- **Indirect causation:** "Dallas 84F+" does not directly say "oil up" -- it requires a mental model of AC demand, grid load, refinery stress
- **Temporal mismatch:** Weather markets resolve daily; commodity impacts play out over weeks

The edge is in connecting the dots faster than the market.

## Signal Logic

### 1. Weather Stress Computation

For each weather/temperature market, extract:
- **City** (Dallas, Chicago, Miami, New York, Houston, Phoenix)
- **Temperature threshold** (e.g., 84F)
- **Direction** (above/below)
- **Probability** of the extreme outcome

City-specific stress models:

| City | Hot Threshold | Cold Threshold | Stress Type |
|---|---|---|---|
| Dallas | 84F+ | 35F- | Energy demand |
| Chicago | 90F+ | 61F- | Crop risk + energy |
| Miami | 92F+ | 40F- | Hurricane indicator |
| New York | 88F+ | 30F- | Energy demand |
| Houston | 90F+ | 35F- | Energy demand |
| Phoenix | 100F+ | 40F- | Energy demand |

Stress score = probability that the extreme outcome occurs. Only signals above `WEATHER_STRESS_THRESHOLD` (default 50%) trigger cascade analysis.

### 2. Commodity Impact Mapping

| Weather Stress | Commodity Impact |
|---|---|
| Energy UP (extreme heat/cold) | Oil, gas, energy markets should rise |
| Crop risk (late spring cold) | Wheat, corn, soybean, agriculture markets should rise |
| Hurricane risk (Miami extreme heat) | Oil, energy, insurance/catastrophe markets should rise |

### 3. Lag Detection & Trading

For each commodity market matching the stress type, check if it has already repriced. If the commodity market probability is still low (below YES_THRESHOLD) despite high weather stress, it is underpriced -- buy YES.

### 4. Conviction-Based Sizing

All trades use the standard conviction formula:

- **YES**: `conviction = (YES_THRESHOLD - p) / YES_THRESHOLD`, boosted by weather stress
- **NO**: `conviction = (p - NO_THRESHOLD) / (1 - NO_THRESHOLD)`
- **Size**: `max(MIN_TRADE, conviction * MAX_POSITION)`

## Remix Ideas

- Add NOAA API for real-time temperature confirmation beyond prediction markets
- Incorporate energy grid load data (ERCOT for Texas, PJM for East Coast)
- Weight stress by city population and industrial activity
- Add crop calendar: spring cold in April is far worse than in February
- Cross-reference with commodity futures (CME) for additional price signals
- Add satellite-based crop health indices (NDVI) for agriculture stress

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
| `SIMMER_WEATHER_STRESS_THRESHOLD` | `0.50` | Min weather stress score to trigger commodity analysis |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
