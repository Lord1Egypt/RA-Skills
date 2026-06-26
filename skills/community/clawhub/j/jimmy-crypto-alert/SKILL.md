---
name: crypto-alert
version: 1.0.0
description: Monitor cryptocurrency prices and send alerts when thresholds are crossed. No API key required — uses Binance public API. Supports BTC, ETH, SOL, and 10+ tokens.
---

# Crypto Alert Monitor

Monitor cryptocurrency prices and send alerts when thresholds are crossed. No API key required — uses Binance public API.

## Usage

```bash
# Check a single token
bash scripts/check-price.sh btc

# Check multiple tokens
bash scripts/check-price.sh btc eth sol

# Set an alert
bash scripts/set-alert.sh btc 100000 "BTC above 100K"

# Check alerts
bash scripts/check-alerts.sh
```

## Configuration

Edit `scripts/config.sh` to set your Telegram bot token and chat ID for alerts.

## How It Works

- Uses CoinGecko public API (rate limit: 10-30 calls/minute)
- Stores state in `~/.crypto-alert-state.json`
- Alerts trigger via Telegram bot (optional)
- Threshold format: `above:X` or `below:X`
