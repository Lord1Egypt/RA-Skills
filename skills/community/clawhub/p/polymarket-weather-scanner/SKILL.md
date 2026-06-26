---
name: polymarket-weather-scanner
description: Weather forecast analysis for Polymarket prediction markets. Find edge in temperature betting markets using 9-model ensemble forecasts (GFS, ECMWF, GraphCast). Detect mispriced weather contracts and identify profitable trading opportunities.
license: MIT
user-invocable: true
metadata: {"openclaw":{"requires":{"env":[],"bins":["curl","jq"]},"primaryEnv":"POLYMARKET_SCANNER_API_KEY","files":["scripts/*"]}}
---

# Polymarket Weather Scanner

Find profitable opportunities in Polymarket temperature markets using multi-model ensemble weather forecasts.

Works out of the box -- no API key needed for free tier (3 cities, 5 scans/day). Just install and run `/scan`.

## What this skill does

- Aggregates forecasts from up to 9 weather models: GFS, ECMWF, JMA, GEM, MeteoFrance, UKMO, ICON, ARPEGE, GraphCast
- Cross-validates with NWS (National Weather Service) official forecasts
- Compares forecast probabilities against live Polymarket temperature market prices
- Detects markets where the forecast disagrees with the market price (positive edge)
- Reports confidence tiers based on model agreement: LOCK (all agree) / STRONG / SAFE / NEAR_SAFE
- Covers 16 cities worldwide: NYC, Chicago, Miami, Dallas, Atlanta, Seattle, Toronto, London, Paris, Munich, Seoul, Ankara, Wellington, Lucknow, Buenos Aires, Sao Paulo

## Quick Start

Install the skill, then:

```
/scan
```

That's it. No setup needed for free tier.

For full access (all 16 cities, 100 scans/day), get a free API key:

```
curl -X POST https://polymarket-scanner.fly.dev/keys/free
```

Then set: `export POLYMARKET_SCANNER_API_KEY="pm_your_key_here"`

## Commands

### `/scan` - Scan for mispriced markets
Scan all active weather temperature markets for profitable opportunities.

When the user asks to scan weather markets, find opportunities, check for edge, or look for Polymarket trades, run:

```bash
bash {baseDir}/scripts/scan.sh
```

Optional: pass number of days ahead to scan (default: 1). Example: `bash {baseDir}/scripts/scan.sh 3`

Display results as a table showing: city, date, forecast temp, confidence tier, edge %, and market cost.

### `/forecast <city>` - Get ensemble forecast
Get the multi-model ensemble weather forecast for a specific city.

When the user asks for a weather forecast, temperature prediction, or model comparison, run:

```bash
bash {baseDir}/scripts/forecast.sh "<city>" "<date>"
```

Where `<city>` is one of: nyc, chicago, miami, dallas, atlanta, seattle, toronto, london, paris, munich, seoul, ankara, wellington, lucknow, buenos-aires, sao-paulo.

And `<date>` is optional, in YYYY-MM-DD format (defaults to tomorrow).

Display the forecast showing: high temperature, standard deviation, number of models used, and individual model predictions.

### `/cities` - List available cities
Show which cities are available for scanning based on your tier.

```bash
bash {baseDir}/scripts/cities.sh
```

### `/tiers` - Show subscription plans
Display available subscription tiers and pricing.

```bash
bash {baseDir}/scripts/tiers.sh
```

## Tiers

| Tier | Price | Cities | Scans/day | Features |
|------|-------|--------|-----------|----------|
| Free | $0 | NYC, Chicago, Miami | 5 | Core scanning |
| Scanner | 5 USDC/mo | All 16 cities | 100 | Full coverage |
| Pro | 15 USDC/mo | All 16 cities | Unlimited | + Backtest |
| Trader | 30 USDC/mo | All 16 cities | Unlimited | + Auto-trade signals |

Payment: USDC on Base chain. Run `/tiers` for details.

## Use Cases

- **Prediction market traders**: Find temperature markets where the crowd is wrong
- **Weather enthusiasts**: Compare multiple global weather models side-by-side
- **Quantitative analysts**: Access ensemble forecast data with standard deviation and model agreement metrics
- **Arbitrage hunters**: Detect when forecast probability diverges from market price

## How It Works

1. Fetches forecasts from multiple independent weather models via Open-Meteo API
2. Calculates ensemble high temperature and standard deviation across models
3. Maps temperature to Polymarket range probabilities (e.g., "NYC high temp 60-69F")
4. Compares forecast probability vs market price for each range
5. Flags ranges where forecast probability exceeds market price (positive edge)
6. Rates confidence based on how many models agree

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| `https://polymarket-scanner.fly.dev/scan/weather` | API key (header) | Scan markets |
| `https://polymarket-scanner.fly.dev/forecast/{city}` | API key, city, date | Get forecast |
| `https://polymarket-scanner.fly.dev/cities` | API key | List cities |
| `https://polymarket-scanner.fly.dev/tiers` | None | Show pricing |
| `https://polymarket-scanner.fly.dev/keys/free` | Client IP | Create free key |

## Security & Privacy

- Works without an API key (anonymous free tier with IP-based rate limiting)
- Your API key is sent only to the scanner API server via HTTPS
- No wallet private keys or trading credentials are transmitted
- Market data comes from Polymarket's public Gamma API
- Weather data comes from Open-Meteo (open source, no API key required)
- All processing happens server-side; no data is stored from your queries

By using this skill, scan requests are sent to the Polymarket Weather Scanner API. Only install if you trust this service.
