---
name: polymarket-micro-weather-sniper-trader
description: Trades Polymarket weather temperature markets using NOAA and Open-Meteo forecasts as an information edge. Buys YES on bins matching the forecast at discount prices, sells NO on bins the forecast disagrees with. Micro-sized positions ($2-$5).
metadata:
  author: Diagnostikon
  owner: Diagnostikon
  version: "1.0.0"
  displayName: Micro Weather Sniper Trader
  difficulty: advanced
  homepage: "https://simmer.markets/skills"
  repository: "https://github.com/SpartanLabsXyz/simmer-sdk"
  requires_env: "SIMMER_API_KEY"
  requires_pip: "simmer-sdk"
  default_mode: "paper"
  live_flag: "--live"
---

# Micro Weather Sniper Trader

> **This is a template.**
> The default signal uses NOAA (US) and Open-Meteo (global) weather forecasts to find mispriced temperature bins on Polymarket -- remix it with additional weather sources, ensemble model averaging, or multi-day position building.
> The skill handles all the plumbing (market discovery, forecast fetching, bin matching, trade execution, safeguards). Your agent provides the alpha.

## Strategy Overview

Polymarket lists "highest temperature" bin markets for cities worldwide (e.g. "Will the highest temperature in Warsaw be 10°C on April 10?"). These bins are priced by market participants who often lack access to professional weather forecast data.

This skill fetches actual weather forecasts from NOAA (US cities, ~85% accuracy for 1-2 day predictions) and Open-Meteo (global cities, free API, similar accuracy). It then compares the forecast temperature against each market bin:

- If the forecast **matches** the bin and the market price is low (p <= 20%): **BUY YES** -- the market is underpricing a likely outcome.
- If the forecast **disagrees** with the bin and the market price is high (p >= 80%): **SELL NO** -- the market is overpricing an unlikely outcome.

Example: Open-Meteo forecasts Warsaw high = 10°C on April 10. The bin "Warsaw 10°C" is priced at p=20%. Edge = 0.85 - 0.20 = 0.65. Conviction = 0.65 / 0.85 = 0.76. Size = max($2, 0.76 * $5) = $3.82. The skill buys YES at $3.82.

## Edge

Weather forecasts from NOAA and Open-Meteo are publicly available but not widely used by Polymarket participants. NOAA 1-2 day high temperature forecasts have documented accuracy of approximately 85%. This creates a structural information edge:

- The forecast provides a probability estimate (~85%) that the temperature will fall in a specific range
- Polymarket bins are priced by retail participants without systematic forecast data
- When the forecast-implied probability (85%) diverges from market price (e.g. 20%), the difference is pure edge
- Weather markets resolve daily, providing rapid feedback and capital recycling
- Micro-sizing ($2-$5) means each trade has minimal risk while maintaining consistent exposure

## Signal Logic

1. Discover active weather markets via keyword search across all supported cities plus `get_fast_markets()` and `get_markets(limit=200)` bulk scan
2. Parse each market question: extract city name, temperature range (bin), and resolution date
3. Fetch NOAA forecast (US cities) or Open-Meteo forecast (global cities) for each relevant city
4. For each market: check if the forecast temperature falls within the bin
5. If forecast **matches** bin AND `p <= YES_THRESHOLD` (0.40): buy YES -- conviction = `(0.85 - p) / 0.85`, size = `max($2, conviction * $5)`
6. If forecast **disagrees** with bin AND `p >= NO_THRESHOLD` (0.80): sell NO -- conviction = `(p - 0.15) / 0.85`, size = `max($2, conviction * $5)`
7. Spread gate: skip if spread > `MAX_SPREAD` (15%)
8. Place up to `MAX_POSITIONS` (10) micro trades per run
9. All trades include `signal_data` with forecast temperature, city, and edge for backtest support

### Remix Signal Ideas

- **Ensemble averaging**: Combine NOAA + Open-Meteo + AccuWeather forecasts and weight by historical accuracy per city
- **Confidence scaling**: NOAA is more accurate for D+1 than D+3 -- scale conviction by forecast horizon
- **Multi-bin strategy**: When forecast is between two bins (e.g. 9.9°C between 9°C and 10°C bins), buy YES on both at half size
- **Exit management**: Monitor positions and sell when price reaches `EXIT_THRESHOLD` (take profit) or forecast changes
- **Historical calibration**: Track forecast accuracy per city per season to dynamically adjust NOAA_ACCURACY

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
| `SIMMER_MAX_POSITION` | `5` | Max USDC per micro trade (ceiling at 100% conviction) |
| `SIMMER_MIN_TRADE` | `2` | Floor for any trade (min USDC regardless of conviction) |
| `SIMMER_MAX_SPREAD` | `0.15` | Max bid-ask spread (15%) |
| `SIMMER_MIN_DAYS` | `0` | Min days until resolution (0 = allow same-day weather) |
| `SIMMER_MAX_POSITIONS` | `10` | Max concurrent micro positions |
| `SIMMER_YES_THRESHOLD` | `0.40` | Buy YES when forecast matches bin and p <= this |
| `SIMMER_NO_THRESHOLD` | `0.80` | Sell NO when forecast disagrees with bin and p >= this |

## Dependency

`simmer-sdk` is published on PyPI by Simmer Markets.
- PyPI: https://pypi.org/project/simmer-sdk/
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk
