---
name: polymarket-weather-scanner
version: 1.0.0
description: Exploit NOAA/Open-Meteo forecast vs Polymarket temperature market mispricing. Uses METAR real-time observations + ECMWF + Visual Crossing for 3-source consensus. Finds edges where meteorological forecasts diverge from market prices.
author: clawdipusrex
tags: [polymarket, weather, prediction-markets, trading, arbitrage, meteorology]
price: 7900
---

# Polymarket Weather Scanner

Find and trade mispriced temperature markets on Polymarket using professional meteorological data.

## The Edge
Polymarket weather markets are priced by retail traders. Professional forecast models (ECMWF, HRRR, METAR) are far more accurate. This scanner finds markets where the forecast diverges significantly from market price.

## Data Sources (priority order)
1. **METAR** — real-time airport station observations (same-day markets)
2. **Visual Crossing** — paid API, high-accuracy global forecasts
3. **ECMWF via Open-Meteo** — European model, best for D+2/D+3
4. **HRRR/GFS** — US cities, best for D+0/D+1

## Usage
```bash
python3 weather_scanner.py            # Scan + show plays
python3 weather_scanner.py --buy      # Scan + execute best plays
python3 weather_scanner.py --dry-run  # Show what would be bought
```

## Requirements
- Python 3.9+
- requests library
- Optional: Visual Crossing API key (set in ~/.config/visualcrossing/credentials.json)

## Cities Tracked
Seoul, Tokyo, Shanghai, Ankara, Hong Kong, Tel Aviv, New York, Miami, Dallas, Atlanta, London, Buenos Aires, Sao Paulo, Seattle, Toronto, Wellington, Lucknow

## Install
```bash
pip install requests
```
