---
name: polymarket-pmxt-trader
description: Trade Polymarket using PMXT cross-exchange predictions and orderbook data for entry/exit signals.
metadata:
  author: "FRIDAY"
  version: "1.0.0"
  displayName: "PMXT Cross-Exchange Trader"
  difficulty: "intermediate"
---

# PMXT Cross-Exchange Trader

> **This is a template.** Default signal: PMXT API price discovery across exchanges (Polymarket, Kalshi, Limitless, etc.).
> Remix it with custom probability models, different signal sources, or alternative confidence scoring.
> The skill handles all plumbing (market discovery, trade execution, safeguards). Your agent provides alpha.

## What it does

Queries [PMXT](https://pmxt.dev) for active prediction markets, identifies bargains (entry threshold ≤45¢), and routes trades through Simmer SDK to Polymarket. PMXT aggregates orderbook depth, volume, and pricing across multiple exchanges, giving better signal quality than single-source price feeds.

## Strategy

1. Fetch top trending markets from PMXT API
2. Filter by entry threshold (default ≤25¢ for strong buy, ≤45¢ for bargain)
3. Cross-check liquidity & volume (skip illiquid markets)
4. Check Simmer context for flip-flop warnings & slippage
5. Size position via Kelly with min EV threshold
6. Execute trade with reasoning tag

## Configuration

Set via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `PMXT_API_KEY` | — | PMXT API key (required) |
| `SIMMER_API_KEY` | — | Simmer SDK key (required) |
| `PMXT_ENTRY_THRESHOLD` | 0.25 | Max YES price to enter (cents) |
| `PMXT_EXIT_THRESHOLD` | 0.45 | Sell when price reaches this |
| `PMXT_MAX_POSITION_USD` | 2.00 | Max per-trade position |
| `PMXT_MIN_VOLUME` | 10000 | Min market volume USD |
| `PMXT_MAX_TRADES_PER_RUN` | 5 | Trade count cap |
| `PMXT_CATEGORIES` | (any) | Optional category filter (Bitcoin,Sports,Politics) |

## Usage

```bash
# Dry run (default)
python pmxt_trader.py

# Live trading
python pmxt_trader.py --live

# Show positions only
python pmxt_trader.py --positions

# Smart sizing (Kelly-based)
python pmxt_trader.py --live --smart-sizing
```

## Safeguards

- Volume floor (skip illiquid markets)
- Spread check via Polymarket CLOB
- Flip-flop detection via Simmer context
- Daily budget cap
- Max position per trade
- Resolution time check (skip markets resolving <2h)
