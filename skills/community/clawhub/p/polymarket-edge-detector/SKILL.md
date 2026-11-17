---
name: polymarket-edge-detector
description: Polymarket prediction market edge detector. Compares Polymarket binary-option prices against external reference probabilities (polls, prediction APIs, market-implied odds) to find mispriced contracts. Scores markets by edge, liquidity, time-to-resolution, and historical accuracy. Surfaces +EV bets for political, sports, and crypto price markets. Built for prediction market traders, sports bettors crossing over to prediction markets, and DeFi quants looking for Sharpe outside pure trading.
compatibility: Created for Zo Computer
metadata:
  author: ssyopros.zo.computer
allowed-tools: Bash
---

# Polymarket Edge Detector

Find mispriced binary contracts on Polymarket. Compares market price to an external reference probability and surfaces +EV setups with liquidity, time-to-resolution, and confidence scoring.

## When to use

- User wants to find +EV Polymarket bets
- Comparing a market's price to a poll or external model
- Hunting low-liquidity markets where a thin order book misprices
- Tracking edge decay over time as resolution approaches
- Screening markets by category (politics, sports, crypto)

## Commands

```bash
python3 scripts/edge_detector.py scan            # All open markets, ranked by edge
python3 scripts/edge_detector.py scan --category politics
python3 scripts/edge_detector.py market <slug>   # Single market deep-dive
python3 scripts/edge_detector.py watch           # Stream prices, alert on edge>5%
python3 scripts/edge_detector.py resolve <id>    # Mark resolution, track accuracy
```

## Output

JSON with: market_id, question, category, yes_price, no_price, reference_prob, edge_pct, implied_odds, liquidity_usd, days_to_resolution, edge_decay_pct, signal (BUY_YES, BUY_NO, PASS), and a confidence score 0-100.

## Environment

- `POLY_API_URL` - Polymarket CLOB endpoint (default: https://clob.polymarket.com)
- `EDGE_THRESHOLD_PCT` - Minimum edge to surface (default: 3.0)
- `REFERENCE_SOURCE` - which external probability to use: `poll`, `model`, `market_implied` (default: market_implied)
- Works with mock data offline; production uses Polymarket's public CLOB API
