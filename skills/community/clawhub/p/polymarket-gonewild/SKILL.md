---
name: polymarket
description: Query Polymarket prediction markets - check odds, trending markets, search events, track prices and momentum. Includes watchlist alerts, resolution calendar, momentum scanner, and paper trading (simulated, no real money).
homepage: https://polymarket.com
user-invocable: true
disable-model-invocation: true
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins: [python3]
---

# Polymarket

Query [Polymarket](https://polymarket.com) prediction markets. Check odds, find trending markets, search events, track price movements.

## Quick Start

```bash
# Trending markets
python3 {baseDir}/scripts/polymarket.py trending

# Search
python3 {baseDir}/scripts/polymarket.py search "trump"

# Biggest movers
python3 {baseDir}/scripts/polymarket.py movers

# What's resolving soon
python3 {baseDir}/scripts/polymarket.py calendar
```

---

## After Install — Suggested Setup

### 1. Add to Morning Briefing
Add Polymarket to your daily cron:
```bash
python3 {baseDir}/scripts/polymarket.py featured
python3 {baseDir}/scripts/polymarket.py movers --timeframe 24h
```

### 2. Watch Markets You Care About
```bash
# Watch with price target alert
python3 {baseDir}/scripts/polymarket.py watch add trump-2028 --alert-at 60

# Watch with change alert (±10% from current)
python3 {baseDir}/scripts/polymarket.py watch add bitcoin-100k --alert-change 10
```

### 3. Set Up Hourly Alerts (Cron)
```bash
# Check watchlist every hour, only notify on alerts
python3 {baseDir}/scripts/polymarket.py alerts --quiet
```

### 4. Weekly Category Digests
```bash
# Every Sunday: politics digest
python3 {baseDir}/scripts/polymarket.py digest politics
```

### 5. Paper Trade to Track Predictions
```bash
python3 {baseDir}/scripts/polymarket.py buy trump-2028 100  # $100 on Trump
python3 {baseDir}/scripts/polymarket.py portfolio           # Check P&L
```

---

## Commands

### Core

```bash
# Trending markets (by 24h volume)
python3 {baseDir}/scripts/polymarket.py trending

# Featured/high-profile markets
python3 {baseDir}/scripts/polymarket.py featured

# Search markets
python3 {baseDir}/scripts/polymarket.py search "giannis"

# Get event by slug or URL
python3 {baseDir}/scripts/polymarket.py event trump-2028
python3 {baseDir}/scripts/polymarket.py event https://polymarket.com/event/trump-2028

# Show all outcomes in an event
python3 {baseDir}/scripts/polymarket.py event trump-2028 --all

# Browse by category
python3 {baseDir}/scripts/polymarket.py category politics

# Limit results
python3 {baseDir}/scripts/polymarket.py trending --limit 10
```

### Watchlist + Alerts

```bash
# Add to watchlist
python3 {baseDir}/scripts/polymarket.py watch add trump-2028
python3 {baseDir}/scripts/polymarket.py watch add bitcoin-100k --alert-at 70
python3 {baseDir}/scripts/polymarket.py watch add fed-rate-cut --alert-change 15

# Watch a specific outcome in a multi-market event
python3 {baseDir}/scripts/polymarket.py watch add giannis-trade --outcome warriors

# List watchlist with current prices
python3 {baseDir}/scripts/polymarket.py watch list

# Remove from watchlist
python3 {baseDir}/scripts/polymarket.py watch remove trump-2028

# Remove a specific outcome entry
python3 {baseDir}/scripts/polymarket.py watch remove giannis-trade --outcome warriors

# Check for alerts (for cron)
python3 {baseDir}/scripts/polymarket.py alerts
python3 {baseDir}/scripts/polymarket.py alerts --quiet  # Only output if triggered
```

### Resolution Calendar

```bash
# Markets resolving in next 7 days (default)
python3 {baseDir}/scripts/polymarket.py calendar

# Markets resolving in next 3 days
python3 {baseDir}/scripts/polymarket.py calendar --days 3

# More results over a longer window
python3 {baseDir}/scripts/polymarket.py calendar --days 14 --limit 20
```

### Momentum Scanner

```bash
# Biggest movers (24h, default)
python3 {baseDir}/scripts/polymarket.py movers

# Weekly movers
python3 {baseDir}/scripts/polymarket.py movers --timeframe 1w

# Monthly movers with volume filter ($50K+ 24h volume)
python3 {baseDir}/scripts/polymarket.py movers --timeframe 1m --min-volume 50
```

Timeframes: `24h` (default), `1w`, `1m`

### Category Digests

```bash
# Politics digest
python3 {baseDir}/scripts/polymarket.py digest politics

# Crypto digest
python3 {baseDir}/scripts/polymarket.py digest crypto

# Sports digest
python3 {baseDir}/scripts/polymarket.py digest sports
```

Categories: `politics`, `crypto`, `sports`, `tech`, `business`

### Paper Trading

Starts with $10,000 paper cash. Track your predictions without real money.

```bash
# Buy $100 of a market (Yes outcome)
python3 {baseDir}/scripts/polymarket.py buy trump-2028 100

# Buy a specific outcome in a multi-market event
python3 {baseDir}/scripts/polymarket.py buy giannis-trade 50 --outcome warriors

# View portfolio and P&L
python3 {baseDir}/scripts/polymarket.py portfolio

# Sell a position
python3 {baseDir}/scripts/polymarket.py sell trump-2028

# Sell a specific outcome
python3 {baseDir}/scripts/polymarket.py sell giannis-trade --outcome warriors

# Reset portfolio back to $10,000 (clears all positions)
python3 {baseDir}/scripts/polymarket.py reset
```

---

## Global Flags

| Flag | Short | Description |
|---|---|---|
| `--limit N` | `-l` | Number of results to show (default: 5) |
| `--all` | `-a` | Show all outcomes/markets in an event |

These flags work with: `trending`, `featured`, `search`, `category`, `calendar`, `movers`, `digest`, and `event`.

---

## Data Storage

Watchlist and portfolio are stored locally in `~/.polymarket/`:

| File | Contents |
|---|---|
| `watchlist.json` | Watched markets and alert thresholds |
| `portfolio.json` | Paper positions and trade history |

---

## Cron Examples

### Hourly Alert Check
```
0 * * * * python3 {baseDir}/scripts/polymarket.py alerts --quiet
```

### Daily Morning Brief
```
0 7 * * * python3 {baseDir}/scripts/polymarket.py movers && python3 {baseDir}/scripts/polymarket.py calendar --days 1
```

### Weekly Digests
```
0 10 * * 0 python3 {baseDir}/scripts/polymarket.py digest politics
0 10 * * 0 python3 {baseDir}/scripts/polymarket.py digest crypto
```

---

## Output Features

Markets display:
- **Current odds** — Yes/No prices as percentages
- **Price momentum** — 24h/1w/1m changes with directional arrows
- **Volume** — total and 24h activity
- **Time remaining** — until market resolution
- **Bid/ask spread** — where available

---

## API

Uses the public Gamma API (no authentication required):

- Base URL: `https://gamma-api.polymarket.com`
- Docs: https://docs.polymarket.com

Bulk commands (`watch list`, `alerts`, `portfolio`) are rate-limited to 1 request per 250ms to avoid hammering the API.

---

## Security & Permissions

**No API key or authentication required.** This skill uses Polymarket's public Gamma API.

**What this skill does:**
- Makes HTTPS GET requests to `gamma-api.polymarket.com` (public, unauthenticated)
- Reads market data: odds, volumes, event details, price history
- Paper trading is **local simulation only** — stored in `~/.polymarket/` as JSON files
- No real money, no wallet, no blockchain transactions

**What this skill does NOT do:**
- Does not connect to any wallet or financial account
- Does not execute real trades or transactions
- Does not require or handle any credentials or API keys
- Does not send any personal data externally
- Cannot be invoked autonomously by the agent (`disable-model-invocation: true`)

**Data stored locally:** `~/.polymarket/watchlist.json`, `~/.polymarket/portfolio.json`

Review `scripts/polymarket.py` before first use to verify behavior.

---

## Note

This is read-only market data + local paper trading only. Real trading on Polymarket requires wallet authentication, which is not implemented in this skill.
