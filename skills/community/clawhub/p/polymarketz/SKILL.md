---
name: polymarket-council
version: "1.0.0"
description: >
  Comprehensive Polymarket prediction market skill — browse trending markets, search events,
  check real-time odds & prices, view order books, analyze price history, track positions,
  and execute trades. Read-only commands work instantly with zero setup. Supports all
  Polymarket categories: politics, crypto, sports, geopolitics, entertainment, and more.
author: openclaw
license: MIT
homepage: https://polymarket.com
metadata:
  openclaw:
    emoji: "🔮"
    tags:
      - prediction-markets
      - polymarket
      - trading
      - odds
      - analysis
      - betting
      - politics
      - crypto
      - sports
    requires:
      bins:
        - python3
      env: []
---

# Polymarket Council

Query, analyze, and trade on [Polymarket](https://polymarket.com) — the world's largest prediction market.

**Read-only commands work immediately** — no API keys, no install, no setup.

## Quick Start

```bash
# What's hot right now?
python3 {baseDir}/scripts/polymarket.py trending

# Search any topic
python3 {baseDir}/scripts/polymarket.py search "bitcoin"

# Get detailed odds for a specific market
python3 {baseDir}/scripts/polymarket.py market CONDITION_ID

# Price history
python3 {baseDir}/scripts/polymarket.py history TOKEN_ID --interval 1d --fidelity 60
```

## Commands

### Market Discovery (no setup needed)

```bash
# Trending markets by volume
python3 {baseDir}/scripts/polymarket.py trending [--limit 20]

# Search markets by keyword
python3 {baseDir}/scripts/polymarket.py search "QUERY" [--limit 10]

# Browse by category/tag
python3 {baseDir}/scripts/polymarket.py category TAG [--limit 20]
# Tags: politics, crypto, sports, pop-culture, business, science, world, ai, elections

# Get full event details (all markets in an event)
python3 {baseDir}/scripts/polymarket.py event SLUG_OR_ID

# Get a single market's details + current prices
python3 {baseDir}/scripts/polymarket.py market CONDITION_ID

# List active events
python3 {baseDir}/scripts/polymarket.py events [--limit 20] [--tag TAG]
```

### Prices & Order Books (no setup needed)

```bash
# Current price / odds for a token
python3 {baseDir}/scripts/polymarket.py price TOKEN_ID

# Batch prices for multiple tokens
python3 {baseDir}/scripts/polymarket.py prices TOKEN_ID1 TOKEN_ID2 ...

# Spread (best ask - best bid)
python3 {baseDir}/scripts/polymarket.py spread TOKEN_ID

# Full order book (bids + asks)
python3 {baseDir}/scripts/polymarket.py book TOKEN_ID

# Price history over time
python3 {baseDir}/scripts/polymarket.py history TOKEN_ID [--interval 1d] [--fidelity 60]
# intervals: 1m, 5m, 1h, 1d, 1w  |  fidelity: minutes between data points

# Last trade price
python3 {baseDir}/scripts/polymarket.py last-trade TOKEN_ID
```

### Analytics (no setup needed)

```bash
# Open interest for a market
python3 {baseDir}/scripts/polymarket.py open-interest CONDITION_ID

# Top holders of a token
python3 {baseDir}/scripts/polymarket.py holders TOKEN_ID [--limit 10]

# Live volume for an event
python3 {baseDir}/scripts/polymarket.py volume EVENT_ID

# Leaderboard
python3 {baseDir}/scripts/polymarket.py leaderboard [--limit 20]

# Public profile of a trader
python3 {baseDir}/scripts/polymarket.py profile ADDRESS

# Trader's activity / trade history
python3 {baseDir}/scripts/polymarket.py activity ADDRESS [--limit 20]
```

### Trading (requires wallet setup)

First-time setup:
```bash
python3 {baseDir}/scripts/polymarket.py wallet-setup
```

This creates `~/.config/polymarket/wallet.json` with your private key (Polygon).

```bash
# Check wallet balance
python3 {baseDir}/scripts/polymarket.py balance

# Buy limit order — preview only (no --confirm)
python3 {baseDir}/scripts/polymarket.py trade buy --token TOKEN_ID --price 0.50 --size 10

# Buy limit order — EXECUTE (with --confirm)
python3 {baseDir}/scripts/polymarket.py trade buy --token TOKEN_ID --price 0.50 --size 10 --confirm

# Sell limit order
python3 {baseDir}/scripts/polymarket.py trade sell --token TOKEN_ID --price 0.70 --size 10 --confirm

# Market order — buy $5 worth at best available price
python3 {baseDir}/scripts/polymarket.py trade buy --token TOKEN_ID --amount 5 --market-order --confirm

# View open orders
python3 {baseDir}/scripts/polymarket.py orders [--address ADDRESS]

# Cancel an order
python3 {baseDir}/scripts/polymarket.py cancel ORDER_ID --confirm

# Cancel all orders
python3 {baseDir}/scripts/polymarket.py cancel-all --confirm

# View positions
python3 {baseDir}/scripts/polymarket.py positions [--address ADDRESS]
```

## Example Chat Usage

- "What are the odds Trump wins the 2028 election?"
- "Show me trending markets on Polymarket"
- "Search Polymarket for Bitcoin price predictions"
- "What are the current crypto markets on Polymarket?"
- "Show the order book for [token]"
- "What's the price history for this market over the last week?"
- "Who are the top traders on Polymarket?"
- "Show me open interest for [market]"
- "Buy 10 shares of YES at $0.45 on [market]"
- "What are my positions?"

## API Reference

Read-only commands use **public** APIs (no auth required):

| API | Base URL | Purpose |
|-----|----------|---------|
| Gamma | `https://gamma-api.polymarket.com` | Markets, events, tags, search, profiles |
| Data | `https://data-api.polymarket.com` | Positions, trades, activity, leaderboards |
| CLOB | `https://clob.polymarket.com` | Order books, prices, spreads, price history |

Trading commands use authenticated CLOB API endpoints.

## Safety Notes

- **Real money.** Polymarket trades use real USDC on Polygon. Double-check before confirming.
- **All trades require `--confirm`.** Without it, you only see a preview.
- **Private key security.** Your key is stored in `~/.config/polymarket/wallet.json`. Protect it.
- **Gas fees.** On-chain operations require MATIC/POL for gas on Polygon.
- **Not financial advice.** This tool provides market data. Make your own decisions.
