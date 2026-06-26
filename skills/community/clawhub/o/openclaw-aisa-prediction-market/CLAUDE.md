# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Prediction market data skill. Accesses Polymarket and Kalshi via the AIsa API — markets, prices, orderbooks, candlesticks, trade history, wallet positions, and P&L. Also supports cross-platform sports market matching.

## Common Commands

```bash
export AISA_API_KEY="your-key"

# Polymarket
python scripts/prediction_market_client.py polymarket markets --search "election" --status open
python scripts/prediction_market_client.py polymarket price <token_id>

# Kalshi
python scripts/prediction_market_client.py kalshi markets --search "fed rate"
python scripts/prediction_market_client.py kalshi price <market_ticker>

# Cross-platform sports
python scripts/prediction_market_client.py sports by-date nba --date 2025-03-01
```

## Architecture

Single-file client: `scripts/prediction_market_client.py`

`PredictionMarketClient` class wraps the AIsa API (`https://api.aisa.one/apis/v1`) with three method groups:
- **Polymarket**: markets, price, activity, orders, orderbooks, candlesticks, positions, wallet, pnl
- **Kalshi**: markets, price, trades, orderbooks
- **Cross-platform**: sports_matching, sports_by_date

CLI via `argparse` with subcommands.

## Key Patterns

**ID lookup is always required first** — most endpoints need IDs from `/markets` response:
- Polymarket `token_id` → `side_a.id` or `side_b.id`
- Polymarket `condition_id` → top-level field in markets response
- Kalshi `market_ticker` → top-level field in markets response

**Prices are decimals 0–1** (e.g., `0.65` = 65% probability).

No other files, no tests, no dependencies beyond stdlib.
