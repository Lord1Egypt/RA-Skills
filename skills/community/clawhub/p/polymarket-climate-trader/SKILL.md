---
name: polymarket-climate-trader
description: Trades Polymarket prediction markets on weather extremes, climate milestones, natural disasters, and agricultural outcomes. Use when you want to capture alpha on temperature records, hurricane seasons, flood events, and CO2 threshold markets using meteorological data signals.
metadata:
  author: Diagnostikon
  version: '1.0'
  displayName: Climate & Weather Trader
  difficulty: intermediate
---

# Climate & Weather Trader

> **This is a template.**  
> The default signal is keyword discovery + NOAA/weather API data alignment — remix it with ForecastEx climate oracle feeds, satellite NDVI data for agriculture, or ensemble weather model outputs.  
> The skill handles all the plumbing (market discovery, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Climate prediction markets are one of the fastest-growing underserved categories. Polymarket has 151+ active climate markets but most are basic. This skill captures alpha on:

- **Temperature extremes** — record highs, heatwaves, frost events
- **Natural catastrophes** — hurricane counts, earthquake magnitudes, wildfire acreage
- **Climate milestones** — CO2 ppm thresholds, Arctic sea ice minimums
- **Agricultural impacts** — wheat yields, drought-driven crop failures, water allocations

Climate markets are uniquely suited for quantitative trading: the data sources are public, verifiable, and highly structured (NOAA, ECMWF, NASA).

## Signal Logic

### Default Signal: Conviction-Based Sizing with Seasonal Bias

1. Discover active climate/weather markets on Polymarket
2. Compute base conviction from distance to threshold (0% at boundary → 100% at p=0/p=1)
3. Apply `season_bias()` multiplier based on current month and event type in the question
4. Size = `max(MIN_TRADE, conviction × bias × MAX_POSITION)` — capped at MAX_POSITION
5. Skip markets with spread > MAX_SPREAD or fewer than MIN_DAYS to resolution

### Seasonal Bias (built-in, no API required)

Climate events follow documented seasonal cycles. `season_bias()` boosts conviction when the current month aligns with peak season, and dampens it off-season:

| Event type | Peak season | In-season multiplier | Off-season multiplier |
|---|---|---|---|
| Hurricane / cyclone | June–November | **1.4x** | 0.6x |
| Sea ice / Arctic | July–September | **1.4x** | 0.7x |
| El Niño / La Niña / ENSO | December–February | **1.3x** | 0.9x |
| Wildfire / fire season | July–October | **1.3x** | 0.8x |
| Heatwave / drought | June–September | **1.3x** | 0.8x |
| Snowfall / blizzard | November–March | **1.3x** | 0.7x |

Example: a hurricane market at 25% in October → conviction 34% × 1.4x bias = 48% → $12 position. Same market in January → 34% × 0.6x = 20% → $5 (floor).

### Remix Ideas

- **ECMWF ensemble**: Replace `market.current_probability` with model consensus probability — trade the divergence between forecast and market
- **NOAA ENSO index**: Feed ONI values directly to boost/reduce `season_bias()` for El Niño markets
- **Insurance cat bond pricing**: Use ILS spreads as implied probability benchmarks for hurricane markets
- **Copernicus climate data**: Real-time European climate services for local/regional temperature markets

## Market Categories Tracked

```python
KEYWORDS = [
    'hurricane', 'tropical storm', 'cyclone', 'tornado', 'flood',
    'drought', 'wildfire', 'earthquake', 'CO2', 'sea ice', 'Arctic',
    'El Niño', 'La Niña', 'ENSO', 'snowfall', 'heatwave', 'heat wave',
    'temperature record', 'crop yield', 'wheat', 'harvest', 'glacier',
    'rainfall', 'water shortage', 'climate', 'emissions', 'carbon',
]
```

## Risk Parameters

| Parameter | Default | Notes |
|-----------|---------|-------|
| Max position size | $20 USDC | Per market |
| Min market volume | $3,000 | Climate markets are less liquid |
| Max bid-ask spread | 12% | Wider allowed for niche markets |
| Min days to resolution | 14 | Weather requires sufficient lead time |
| Max open positions | 8 | Diversify across events |

## Key Data Sources

- **NOAA Climate Data Online**: https://www.ncdc.noaa.gov/cdo-web/
- **Open-Meteo API**: https://open-meteo.com/ (free, no key required)
- **Copernicus C3S**: https://cds.climate.copernicus.eu/
- **ForecastEx**: https://forecastex.com/

## Installation & Setup

```bash
clawhub install polymarket-climate-trader
```

Requires: `SIMMER_API_KEY` environment variable. Optional: `OPENMETEO_API_KEY`.

## Cron Schedule

Runs every 30 minutes (`*/30 * * * *`). Weather data updates every 1–6 hours; no need to poll faster.

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
| `SIMMER_MIN_VOLUME` | `3000` | Min market volume filter (USD) |
| `SIMMER_MAX_SPREAD` | `0.12` | Max bid-ask spread (0.12 = 12%) |
| `SIMMER_MIN_DAYS` | `14` | Min days until market resolves |
| `SIMMER_MAX_POSITIONS` | `8` | Max concurrent open positions |
| `SIMMER_YES_THRESHOLD` | `0.38` | Buy YES if market price ≤ this value |
| `SIMMER_NO_THRESHOLD` | `0.62` | Sell NO if market price ≥ this value |
| `SIMMER_MIN_TRADE` | `5` | Floor for any trade (min USDC regardless of conviction) |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
- Publisher: hello@simmer.markets

Review the source before providing live credentials if you require full auditability.
