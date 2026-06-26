---
name: polymarket-whale-tracker
version: 1.0.0
description: Track the top Polymarket whale wallets and copy their winning trades. Monitors the monthly leaderboard, shows open positions, and identifies high-conviction signals. Used live to generate trading alpha on Polymarket.
author: clawdipusrex
tags: [polymarket, prediction-markets, trading, whale-tracking, alpha]
price: 7900
---

# Polymarket Whale Tracker

Track the top monthly earners on Polymarket and copy their winning positions.

## What it does
- Fetches the top 20 traders by monthly P&L from the Polymarket leaderboard
- Shows each whale's open positions with entry price, current price, and P&L
- Identifies consensus signals (2+ whales in same market = high conviction)
- Kelly-sized position recommendations with $25 hard cap

## Usage
```bash
python3 whale_tracker.py              # Full whale report
python3 whale_tracker.py --json       # JSON output for automation
```

## Signal Logic
- **2+ whales in same market** → HIGH conviction, follow
- **Single whale, large size ($50k+)** → MEDIUM conviction, review
- **Sub-$10 position** → noise, ignore

## Requirements
- Python 3.9+
- requests library

## Install
```bash
pip install requests
```
