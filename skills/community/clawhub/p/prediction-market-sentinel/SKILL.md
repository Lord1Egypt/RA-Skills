---
name: polymarket-monitor
description: Monitor Polymarket prediction market wallets and detect new trades in real-time. Use when tracking whale wallets, detecting new positions, or monitoring prediction market activity. Supports CLOB API queries, wallet tracking, and trade alerts.
---

# Polymarket Monitor

Monitor Polymarket whale wallets and detect trading activity.

## Quick Start

Run the monitor script to track a wallet:

```bash
bash scripts/monitor.sh <wallet_address>
```

## Features

1. Track any Polymarket wallet by address
2. Detect new orders via CLOB API
3. Alert on new positions or large trades
4. Support multiple wallets simultaneously

## Usage

### Single wallet monitoring
```bash
bash scripts/monitor.sh 0x17db3fcd93ba12d38382a0cade24b200185c5f6d
```

### Configuration
Set environment variables:
- `POLL_INTERVAL` - Seconds between checks (default: 600)
- `ALERT_THRESHOLD` - Minimum trade size to alert (default: 100 USDC)

## How It Works

1. Queries Polymarket CLOB API for wallet orders
2. Compares with previous state
3. Alerts on new or changed positions
4. Logs all activity for analysis
