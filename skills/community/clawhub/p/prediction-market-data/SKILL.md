---
name: prediction-market-data
description: "Cross-platform prediction market data via AIsa API. Query Polymarket and Kalshi markets, prices, orderbooks, candlesticks, positions, and trades. Use when user asks about: prediction market odds, election betting, event probabilities, market sentiment, Polymarket prices, Kalshi prices, sports betting odds, wallet PnL, or cross-platform market comparison."
license: MIT
metadata:
  openclaw:
    emoji: "📈"
    requires:
      bins: [python3]
      env: [AISA_API_KEY]
    primaryEnv: AISA_API_KEY
---

# Prediction Market Data

Query [Polymarket](https://polymarket.com) and [Kalshi](https://kalshi.com) prediction markets via [AIsa API](https://aisa.one).

## Setup

```bash
export AISA_API_KEY="your-key"
```

Get a key at [aisa.one](https://aisa.one) ($0.01/query, pay-as-you-go).

## Workflow

Querying prediction market data involves these steps:

1. **Search markets** to find IDs (always start here)
2. **Extract the ID** from the response (`token_id`, `condition_id`, or `market_ticker`)
3. **Query details** using the extracted ID (price, orderbook, candlesticks, etc.)

## Quick Examples

### Polymarket: search → get price

```bash
# Step 1: Search — find markets and extract token_id (side_a.id or side_b.id)
python3 {baseDir}/scripts/prediction_market_client.py polymarket markets --search "election" --status open --limit 5

# Step 2: Get price using token_id from Step 1
python3 {baseDir}/scripts/prediction_market_client.py polymarket price <token_id>
```

### Kalshi: search → get price

```bash
# Step 1: Search — find markets and extract market_ticker
python3 {baseDir}/scripts/prediction_market_client.py kalshi markets --search "fed rate" --status open --limit 5

# Step 2: Get price using market_ticker from Step 1
python3 {baseDir}/scripts/prediction_market_client.py kalshi price <market_ticker>
```

### Cross-platform sports

```bash
python3 {baseDir}/scripts/prediction_market_client.py sports by-date nba --date 2025-04-01
```

## ID Reference

Most commands need an ID from the `markets` response. Always search first.

| Platform | ID Field | Where to Find |
|----------|----------|---------------|
| Polymarket | `token_id` | `side_a.id` or `side_b.id` in markets output |
| Polymarket | `condition_id` | `condition_id` in markets output |
| Kalshi | `market_ticker` | `market_ticker` in markets output |

## Commands

### Polymarket

```bash
python3 {baseDir}/scripts/prediction_market_client.py polymarket markets [--search <kw>] [--status open|closed] [--min-volume <n>] [--limit <n>]
python3 {baseDir}/scripts/prediction_market_client.py polymarket price <token_id> [--at-time <unix_ts>]
python3 {baseDir}/scripts/prediction_market_client.py polymarket activity --user <wallet> [--market-slug <slug>] [--limit <n>]
python3 {baseDir}/scripts/prediction_market_client.py polymarket orders [--market-slug <slug>] [--token-id <id>] [--user <wallet>] [--limit <n>]
python3 {baseDir}/scripts/prediction_market_client.py polymarket orderbooks --token-id <id> [--start <ms>] [--end <ms>] [--limit <n>]
python3 {baseDir}/scripts/prediction_market_client.py polymarket candlesticks <condition_id> --start <unix_ts> --end <unix_ts> [--interval 1|60|1440]
python3 {baseDir}/scripts/prediction_market_client.py polymarket positions <wallet_address> [--limit <n>]
python3 {baseDir}/scripts/prediction_market_client.py polymarket wallet (--eoa <addr> | --proxy <addr>) [--with-metrics]
python3 {baseDir}/scripts/prediction_market_client.py polymarket pnl <wallet_address> --granularity <day|week|month>
```

### Kalshi

```bash
python3 {baseDir}/scripts/prediction_market_client.py kalshi markets [--search <kw>] [--status open|closed] [--min-volume <n>] [--limit <n>]
python3 {baseDir}/scripts/prediction_market_client.py kalshi price <market_ticker> [--at-time <unix_ts>]
python3 {baseDir}/scripts/prediction_market_client.py kalshi trades [--ticker <ticker>] [--start <unix_ts>] [--end <unix_ts>] [--limit <n>]
python3 {baseDir}/scripts/prediction_market_client.py kalshi orderbooks --ticker <ticker> [--start <ms>] [--end <ms>] [--limit <n>]
```

### Cross-Platform Sports

```bash
python3 {baseDir}/scripts/prediction_market_client.py sports matching (--polymarket-slug <slug> | --kalshi-ticker <ticker>)
python3 {baseDir}/scripts/prediction_market_client.py sports by-date <sport> --date <YYYY-MM-DD>
```

Sports: `nfl`, `mlb`, `cfb`, `nba`, `nhl`, `cbb`, `pga`, `tennis`.

## Understanding Odds

Prices are decimals: `0.65` = 65% implied probability. "Yes" price = probability the event happens. Higher volume = more liquidity.

## Security & Permissions

**Requires:** `AISA_API_KEY` environment variable.

All operations are **read-only** via HTTPS GET to `api.aisa.one`. No trades executed, no wallets connected, no personal data sent beyond the API key. Every response includes `usage.cost` and `usage.credits_remaining`.

Full docs: [AIsa API Reference](https://docs.aisa.one/reference/).
