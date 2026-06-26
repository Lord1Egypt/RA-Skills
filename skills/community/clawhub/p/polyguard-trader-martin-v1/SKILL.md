# PolyGuard Martin Pro

**Free and open-source** OpenClaw skill for automated trading on Polymarket. No hidden backdoors, no data collection.

## Overview

PolyGuard Martin Pro monitors Polymarket order books and places orders only when your configured price conditions are met. All logic runs locally; the skill does not call any third-party or analytics APIs.

## Key Features

- **Free and open-source:** No external APIs beyond Polymarket.
- **Auditable:** Logic is transparent; no hidden behavior.
- **Security-first:** No data collection, no telemetry, no external callbacks.
- **Robust handling:** Clear errors for API failures and insufficient balance.
- **Configurable:** Set market, side, size, price threshold, and poll interval in `config.yaml`.

## Installation

1. Add this skill to your OpenClaw workspace.
2. Edit `config.yaml` and set flat key-value pairs (no nesting):
   - `api_key` - your Polymarket API key
   - `market_id` - the market you want to trade
   - `side`, `size`, `max_price`, `poll_interval_seconds` as needed

## Configuration

All settings are in `config.yaml` as top-level keys only. No nested paths. Use placeholders until you paste your own credentials.

- `api_key` - Your Polymarket API key
- `market_id` - Target market ID
- `side` - "buy" or "sell"
- `size` - Order size in outcome shares
- `max_price` - Trigger level: buy when price <= this; sell when price >= this
- `poll_interval_seconds` - How often to check price (seconds)

This tool is free and open-source. No monetization or external charges.

## License and Safety

PolyGuard Martin Pro is provided as-is. You are responsible for your own trading capital and API keys. The skill does not transmit your keys or order data to any server other than Polymarket's official API.

---
**Author:** Martin | PolyGuard Labs  
**Powered by:** OpenClaw
