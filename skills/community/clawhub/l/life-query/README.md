English | [中文](README.zh.md)

# Life Query — Everyday Info at Your Fingertips

A Claude Code skill that handles daily life queries: parcel tracking, currency exchange, gas prices, and weather forecasts — all through natural language.

## Capabilities

- **Parcel Tracking** — Track packages across major Chinese carriers (SF Express, YTO, ZTO, JD, etc.). Supports free tier or bring-your-own Kuaidi100 credentials for direct connection
- **Exchange Rate** — Real-time and historical rates for 30 currencies (CNY/USD/EUR/JPY/GBP/HKD/KRW...). Data from ECB, no API key needed
- **Gas Price** — Latest 92/95/diesel prices for all 31 provinces in China. Data from Eastmoney / NDRC
- **Weather Forecast** — Current conditions, multi-day forecasts, and hourly details for any city worldwide. Data from wttr.in

## Quick Start

```bash
# Track a package
bash scripts/run.sh call courier-track --trackingNumber SF1234567890

# Convert 100 CNY to USD, EUR, JPY
bash scripts/run.sh call exchange-rate --from CNY --to USD,EUR,JPY --amount 100

# Gas prices for all provinces (table format)
bash scripts/run.sh call oil-price --format table

# 3-day weather forecast for Shanghai
bash scripts/run.sh call weather --city Shanghai --days 3 --format table

# List all available APIs
bash scripts/run.sh list
```

## Install

```bash
npx clawhub@latest install life-query
```

## Changelog

- 2026-03-21: refactor — Merged `apis/` into `scripts/`, optimized SKILL.md structure
- 2026-03-17: feat — Added weather forecast (wttr.in)
- 2026-03-17: feat — Added exchange rate and gas price queries
- 2026-03-17: fix — Removed API Key verification, parcel tracking restored
- 2026-03-14: init — Initial release with parcel tracking
