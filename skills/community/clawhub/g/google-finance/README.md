# google-finance

> OpenClaw skill — Track stock prices, company news, and buy/sell signals via Google Finance.

## What it does

- Monitors a watchlist of stocks on Google Finance (default: **NVDA, AAPL, META, GOOGL**)
- Fetches real-time price, volume, P/E ratio, and 52-week range
- Surfaces top company news headlines from the past 24 hours
- Generates a scored **BUY / HOLD / SELL** signal using a 4-factor model
- Alerts on price moves >3%, volume spikes, and high-impact news keywords
- Can run on a cron schedule (market open/close, or every N hours)

## Installation

```bash
clawhub install google-finance
```

Or search and install from within OpenClaw:

```bash
clawhub search google-finance
```

Once installed, use `/google-finance` in any OpenClaw session.

## Quick start

```
/google-finance check            — check all watched stocks
/google-finance add TSLA         — add a stock
/google-finance remove TSLA      — remove a stock
/google-finance list             — show watchlist
/google-finance schedule         — set up cron job
```

## Requirements

- `python3` on PATH
- No API keys needed — data is fetched from public Google Finance pages

## State file

Watchlist and snapshots are stored locally at:
```
~/.openclaw/workspace/stock-tracker-state.json
```

## Signal scoring

| Factor | Max points |
|--------|-----------|
| Price momentum + 52-week position | ±4 |
| Volume vs average | ±2 |
| P/E vs sector benchmark | ±2 |
| News sentiment | ±3 |
| **Total → BUY (≥+4) / HOLD / SELL (≤-4)** | ±10 |

## Disclaimer

This skill provides informational signals only and does not constitute financial advice. Data sourced from Google Finance (may be 15 min delayed for some exchanges).
