---
name: polymarket-catastrophe-trader
description: Trades Polymarket prediction markets on hurricane seasons, earthquake probabilities, wildfire forecasts, and extreme weather records. Exploits two structural edges — availability bias correction (retail anchors to vivid recent disasters rather than 40+ years of NOAA base rates) and seasonal data quality timing (signal is only actionable when models are actively running in real time).
metadata:
  author: snetripp
  version: "1.0"
  displayName: Catastrophe & Extreme Risk Trader
  difficulty: advanced
---

# Catastrophe & Extreme Risk Trader

> **This is a template.**
> The default signal is keyword-based market discovery combined with conviction-based sizing and `catastrophe_bias()` — two structural edges that work without any external API.
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Catastrophe prediction markets are uniquely mispriced because retail traders anchor on the most recent vivid disaster rather than historical base rates. The availability heuristic is the dominant pricing force: the first named storm of the season spikes subsequent storm markets 20–40%, even when NOAA's seasonal forecast hasn't changed by a single storm. After a major wildfire, every "will X state break a fire record?" market overshoots. After a quiet start to a season, markets underprice the base rate. Two structural edges compound:

1. **Availability bias correction** — NOAA, NHC, NIFC, and USGS publish decades of calibrated base rates. Named Atlantic storm counts have 40+ years of forecasting data. Global temperature records are measured to ±0.01°C simultaneously by three independent agencies. The edge is in knowing these numbers when retail is trading on vibes and recent memory.

2. **Seasonal data quality timing** — The signal is only actionable when models are actively running. During hurricane peak season (Aug–Oct), NHC issues advisories every 6 hours and model ensembles update in real time. A named-storm-count market in February is priced on stale pre-season data; the same market in September is priced against daily NHC output. The edge doubles when real-time data is flowing.

## Signal Logic

### Default Signal: Conviction-Based Sizing with Catastrophe Bias

1. Discover active catastrophe and extreme weather markets on Polymarket
2. Compute base conviction from distance to threshold (0% at boundary → 100% at p=0/p=1)
3. Apply `catastrophe_bias()` — hazard type data quality × seasonal calendar timing
4. Size = `max(MIN_TRADE, conviction × bias × MAX_POSITION)` — capped at MAX_POSITION
5. Skip markets with spread > MAX_SPREAD or fewer than MIN_DAYS to resolution

### Catastrophe Bias (built-in, no API required)

**Factor 1 — Hazard Type / Data Quality**

| Hazard type | Multiplier | The structural reality |
|---|---|---|
| Named storm count / above-normal Atlantic season | **1.25x** | NOAA seasonal outlooks calibrated over 40+ years; above/below-normal ~70% accurate at 90-day lead; retail over-reacts after first storm (20–40% spike) |
| Global temperature record (hottest year/month) | **1.20x** | Measured to ±0.01°C by NOAA, Berkeley Earth, NASA GISS simultaneously; trajectory clear months before year-end; retail doesn't check |
| Billion-dollar disaster count | **1.20x** | NOAA tracks since 1980; trend clearly upward from climate change + expanding insured assets; retail anchors to average-year intuition |
| Wildfire season severity (acres burned, state records) | **1.20x** | NIFC YTD acres vs 10-year average: strong 2–4 week leading indicator; Palmer drought index leads fires by weeks; data public, updated daily |
| Major hurricane (Cat 3+) landfall | **1.10x** | NHC 2–5 day track cone probabilities annually verified; retail overprices landfall from visual cone; actual landfall-specific probability far lower |
| Tornado season record / violent outbreak | **1.10x** | SPC seasonal outlook reliable at 3-month scale; specific outbreak timing within season harder to predict |
| FEMA disaster declaration | **0.85x** | Political and bureaucratic discretion adds real noise beyond meteorological signal |
| Earthquake (M7+, specific region/window) | **0.80x** | Fundamentally unpredictable on quarterly timescales; USGS hazard models are long-run annual rates |
| Tsunami / volcanic eruption | **0.75x** | Triggered by underlying seismic/geologic events that cannot themselves be predicted; lowest edge in catastrophe markets |

**The Availability Bias Rule** — The first major event of a season creates a retail pricing spike that is almost always an overreaction. The NOAA seasonal forecast before and after that first storm is essentially unchanged, but the market price jumps 20–40%. Fading these spikes — or, better, entering *before* them — is the core mechanism of the named storm edge. The base rate, not the headline, is the signal.

**The Earthquake Exemption** — Unlike weather hazards, earthquakes have no seasonal signal and no meaningful short-term forecasting capability. USGS can give you a 1-in-500 annual probability for a M7+ event in a specific fault system. They cannot tell you if it will happen in Q3. Trade earthquake markets at maximum caution (0.80x), and tsunami/volcanic markets at the floor (0.75x).

**Factor 2 — Seasonal Calendar Timing**

| Condition | Multiplier | Why |
|---|---|---|
| Atlantic hurricane + Aug–Oct | **1.25x** | NHC issuing daily advisories; GFS/ECMWF updating every 6h; data richest |
| Atlantic hurricane + Jun–Jul/Nov | **1.10x** | Active season; storms possible; below peak frequency |
| Atlantic hurricane + Dec–May | **0.85x** | Off-season; no active systems; base rate near zero |
| Western wildfire + Jul–Sep | **1.20x** | NIFC daily updates; drought indices current; red flag warnings active |
| Western wildfire + May–Jun/Oct | **1.10x** | Fire weather building or receding |
| Western wildfire + Nov–Apr | **0.90x** | Most fires absent; markets on stale winter-season data |
| Tornado alley + Mar–Jun | **1.15x** | SPC issuing daily outlooks; storm reports accumulating |
| Tornado + Jul–Feb | **0.90x** | Off-season; tornado markets thinly priced |
| Winter storm + Dec–Feb | **1.10x** | GFS/ECMWF ensemble agreement highest in peak months |
| Temperature record + Oct–Feb | **1.15x** | Oct–Dec trajectory clear; Jan–Feb prior-year data finalised |

### Combined Examples

| Market | Type mult | Season mult | Final bias |
|---|---|---|---|
| "Will there be 20+ named Atlantic storms?" — September | 1.25x | 1.25x (hurricane peak) | **1.35x cap** |
| "Will 2026 be the hottest year on record?" — November | 1.20x | 1.15x (temp record) | **1.35x cap** |
| "Will Western US wildfire season exceed 10M acres?" — August | 1.20x | 1.20x (wildfire peak) | **1.35x cap** |
| "Will there be a Cat 5 hurricane landfall by Oct?" — March | 1.10x | 0.85x (off-season) | **0.94x** |
| "Will FEMA declare a major disaster in Florida?" | 0.85x | 1.0x | **0.85x** — always cautious |
| "Will there be a M8.0+ earthquake in Pacific NW by Dec?" | 0.80x | 1.0x | **0.80x** — floor territory |
| "Will there be a Pacific tsunami in 2026?" | 0.75x | 1.0x | **0.75x** — near MIN_TRADE |

### Keywords Monitored

```
hurricane, tropical storm, category 5, Atlantic season, named storm,
tornado, wildfire, acres burned, fire season, earthquake, magnitude,
tsunami, volcanic eruption, 100-year flood, FEMA, disaster declaration,
billion-dollar disaster, polar vortex, bomb cyclone, derecho, heat dome,
hottest year, warmest year, temperature record, blizzard, ice storm,
above-normal season, NOAA, NHC, Category 4, major hurricane
```

### Remix Signal Ideas

- **NOAA National Hurricane Center**: Named-storm seasonal forecast gives a directly tradeable probability for storm-count markets — compare NOAA's official probability to Polymarket price; the lag after a quiet start to the season can be 15–25%
- **NIFC Wildfire Statistics**: Year-to-date acres burned vs 10-year average — when YTD is tracking 40% above average by July, "above-normal fire season" markets are structurally underpriced
- **USGS Earthquake Hazards API**: Real-time seismic data M2.5+ globally — for post-earthquake aftershock markets, the USGS Omori decay law gives probability estimates of M6+ aftershocks within days of a major event
- **Berkeley Earth / NASA GISS**: Annual global temperature anomaly updated monthly — when October anomaly is already 0.2°C above the prior record, "will 2026 be hottest year?" is a near-certainty the market underprices


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
| `SIMMER_MAX_SPREAD` | `0.10` | Max bid-ask spread (10%) — catastrophe markets are thinner |
| `SIMMER_MIN_DAYS` | `7` | Min days until resolution — seasonal markets need time to develop |
| `SIMMER_MAX_POSITIONS` | `7` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES if market price ≤ this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO if market price ≥ this value |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |

## Dependency

`simmer-sdk` by Simmer Markets (SpartanLabsXyz)
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
