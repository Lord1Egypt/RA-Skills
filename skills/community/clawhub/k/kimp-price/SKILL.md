---
name: kimchi-premium
version: 1.0.0
description: >
  Real-time Bitcoin Kimchi Premium calculator.
  Compares Bitcoin prices between a Korean exchange (Upbit, KRW) and a global exchange (Binance, USD)
  to calculate the premium percentage and price difference in KRW.
  Reflects live USD/KRW exchange rates and uses only Node.js built-in modules with zero dependencies.
author: seungdols
permissions:
  network:
    - open.er-api.com
    - api.upbit.com
    - api.binance.com
---

# Kimchi Premium 🌶️

A Claude Code skill that calculates the real-time Bitcoin **Kimchi Premium**.

## What is Kimchi Premium?

The Kimchi Premium is a metric that measures how much higher (or lower) Bitcoin prices are
on South Korean cryptocurrency exchanges (e.g. Upbit) compared to global exchanges (e.g. Binance).
The premium tends to rise when local demand is strong, influenced by investor sentiment
and capital flow regulations in South Korea.

## What This Skill Does

1. **Fetches live exchange rate** — Retrieves the current USD/KRW rate from ExchangeRate-API
2. **Fetches Upbit BTC price** — Gets the latest Bitcoin price in KRW from the Upbit API
3. **Fetches Binance BTC price** — Gets the latest Bitcoin price in USD from the Binance API
4. **Calculates the premium** — Converts the Binance price to KRW, then compares it with the Upbit price to produce the premium percentage and the absolute price difference in KRW

## Example Output

```json
{
  "timestamp": "2/1/2026, 2:20:00 PM",
  "exchange_rate": "1,380 KRW/USD",
  "upbit_btc": "145,000,000 KRW",
  "binance_btc": "105,000 USD",
  "kimchi_premium": "0.15%",
  "price_diff": "217,000 KRW"
}
```

## Usage

```bash
node index.mjs
```

## Technical Highlights

- Zero external dependencies — uses only the Node.js built-in `https` module
- Parallel API calls via `Promise.all` for fast response times
- 5-second timeout for reliable error handling
- Structured JSON output for easy parsing
