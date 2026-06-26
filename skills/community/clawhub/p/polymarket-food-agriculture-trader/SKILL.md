---
name: polymarket-food-agriculture-trader
description: Trades Polymarket prediction markets on food commodity prices, crop yields, drought-driven supply shocks, alternative protein milestones, and agricultural policy events. Use when you want to capture alpha on food markets using USDA WASDE calendar timing, commodity concentration signals, and crop season windows.
metadata:
  author: Diagnostikon
  version: "1.0"
  displayName: Food & Agriculture Trader
  difficulty: intermediate
---

# Food & Agriculture Trader

> **This is a template.**
> The default signal is keyword-based market discovery combined with conviction-based sizing and `harvest_cycle_bias()` — remix it with the data sources listed below.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Agricultural markets are driven by hard data (USDA reports, satellite crop monitoring) but traded by retail participants who follow headlines. This skill exploits two structural edges without any external API:

1. **WASDE & crop calendar timing** — Information asymmetry between professional futures traders and Polymarket retail peaks around USDA WASDE release months and planting windows. Trading these windows captures the pro vs retail pricing gap before it closes.
2. **Commodity type confidence** — Cocoa and coffee (geographically concentrated supply) are dramatically more front-runnable than drought headlines (already crowded) or famine narratives (too complex to time).

## Signal Logic

### Default Signal: Conviction-Based Sizing with Harvest Cycle Bias

1. Discover active food and agriculture markets on Polymarket
2. Compute base conviction from distance to threshold (0% at boundary → 100% at p=0/p=1)
3. Apply `harvest_cycle_bias()` — combines WASDE calendar timing with commodity type confidence
4. Size = `max(MIN_TRADE, conviction × bias × MAX_POSITION)` — capped at MAX_POSITION
5. Skip markets with spread > MAX_SPREAD or fewer than MIN_DAYS to resolution

### Harvest Cycle Bias (built-in, no API required)

Two compounding structural edges:

**Factor 1 — Crop Calendar / WASDE Timing**

Agricultural markets have their highest information asymmetry at two points: (a) during the Northern hemisphere planting window (Mar–May) when yield uncertainty peaks, and (b) around USDA WASDE high-impact release months when professional traders have better reads than retail.

| Condition | Multiplier |
|---|---|
| Crop question + WASDE high-impact month (Jun, Aug, Nov, Jan) | **1.20x** — pro vs retail divergence peaks |
| Crop question + planting season (Mar–May) | **1.15x** — yield uncertainty at maximum |
| Crop question + S. hemisphere harvest (Jan–Apr) | **1.10x** — Brazil/Argentina soy/corn window |
| Crop question + off-season | **0.90x** — catalysts scarce, edge compresses |

**Factor 2 — Commodity Type Confidence**

| Commodity type | Multiplier | Why |
|---|---|---|
| Cocoa / coffee | **1.25x** | ~70% of supply from a few countries — W. Africa/Brazil weather is front-runnable |
| Wheat / corn / soy / grain / WASDE | **1.20x** | CME professional futures lead; Polymarket retail lags by days |
| Fertilizer / potash / nitrogen | **1.15x** | Upstream inputs move on Russia policy and energy — longer leads than retail prices |
| Alternative protein / lab-grown meat | **1.10x** | FDA/USDA FSIS approval milestones are public — regulatory calendar predictable |
| Food inflation / FAO index / CPI food | **1.05x** | Data-driven but lagged — moderate edge |
| Drought / wildfire crop damage | **0.85x** | Crowded media trade — edge mostly gone by the time a Polymarket question exists |
| Famine / food crisis / food security | **0.75x** | Humanitarian narratives — geopolitical complexity makes timing very hard |

Combined and capped at **1.40x**. A cocoa market in August (WASDE month) → 1.20 × 1.25 = **1.40x** cap — maximum conviction. A drought headline in October (off-season) → 0.90 × 0.85 = **0.77x** — trade very small.

### Keywords Monitored

```
wheat, corn, soybean, coffee, cocoa, sugar, food price, crop yield,
drought, harvest, USDA, FAO, food inflation, famine, supply shock,
alternative protein, Beyond Meat, Impossible Foods, lab-grown,
vertical farming, fertilizer, potash, nitrogen, El Niño crop,
La Niña harvest, WASDE, commodity, rice, palm oil, livestock,
cattle, food security, grain, oilseed
```

### Remix Signal Ideas

- **USDA NASS crop progress**: Free weekly API during growing season — monitor crop condition ratings as leading indicator before WASDE reflects them
- **FAO Food Price Index**: Monthly release — trade divergence between FAO trajectory and Polymarket food inflation question pricing
- **CME agricultural futures**: Replace `market.current_probability` with CME futures-implied probability to trade the pro vs retail gap directly
- **NOAA ENSO forecasts**: 3–6 month lead time on El Niño/La Niña impacts on major crop-growing regions — markets rarely incorporate this correctly


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
| `SIMMER_MIN_VOLUME` | `5000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.10` | Max bid-ask spread (10%) |
| `SIMMER_MIN_DAYS` | `7` | Min days until resolution |
| `SIMMER_MAX_POSITIONS` | `7` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES if market price ≤ this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO if market price ≥ this value |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
