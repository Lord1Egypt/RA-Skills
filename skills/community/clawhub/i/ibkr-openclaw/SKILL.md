---
name: ibkr-openclaw
description: Connect OpenClaw to Interactive Brokers via IB Gateway Docker. Live portfolio data, real-time quotes, historical K-lines, technical analysis, and Telegram alerts — all read-only safe. Use when users ask about IBKR integration, portfolio monitoring, stock analysis, or automated trading alerts.
---

# IBKR + OpenClaw Integration

Connect OpenClaw to your Interactive Brokers account for live portfolio monitoring, real-time quotes, technical analysis, and automated Telegram alerts.

## Features

- **Live account data** — NAV, cash, P&L, buying power
- **Positions** — all holdings with avg cost and exchange
- **Real-time quotes** — delayed or live market data
- **Historical K-lines** — daily OHLCV data for technical analysis
- **Technical indicators** — RSI, MACD, Bollinger Bands, ATR, MA (via ib_async)
- **Read-only safe** — API configured for read-only access

## Prerequisites

- Interactive Brokers account (live or paper)
- IBKR Mobile app (for 2FA approval)
- Docker & Docker Compose installed on your server
- Python 3.9+ with `ib_async` and `pandas`

## Setup Guide

### Step 1: Install Docker

```bash
curl -fsSL https://get.docker.com | sh
docker --version
docker compose version
```

### Step 2: Clone IB Gateway Docker

The IB Gateway runs in a Docker container based on [gnzsnz/ib-gateway-docker](https://github.com/gnzsnz/ib-gateway-docker).

```bash
cd ~/.openclaw/workspace
git clone https://github.com/gnzsnz/ib-gateway-docker.git
cd ib-gateway-docker
```

### Step 3: Configure Environment

Create a `.env` file in the `ib-gateway-docker` directory:

```env
# IBKR Account
TWS_USERID=your_username
TWS_PASSWORD=your_password

# Trading mode: live or paper
TRADING_MODE=live

# Read-only API (recommended for monitoring)
READ_ONLY_API=yes

# API settings
TWS_ACCEPT_INCOMING=auto
TWS_MASTER_CLIENT_ID=1

# 2FA device name (find in IBKR web portal → Settings → Security)
TWOFA_DEVICE=IB Key

# 2FA timeout
TWOFA_TIMEOUT_ACTION=exit

# Timezone
TIME_ZONE=Asia/Singapore
TZ=Asia/Singapore

# VNC password (optional, for remote desktop)
VNC_SERVER_PASSWORD=your_password

# Auto restart (daily maintenance)
AUTO_RESTART_TIME=23:45

# Save settings between restarts
SAVE_TWS_SETTINGS=yes
```

**Important:** Find your `TWOFA_DEVICE` name in your IBKR web portal under:
Settings → Security → Second Factor Authentication → Devices

### Step 4: Start the Container

```bash
docker compose up -d
```

Check logs:
```bash
docker logs algo-trader-ib-gateway-1 --tail 20
```

### Step 5: Approve 2FA

The Gateway will prompt for 2FA. Approve the notification on your **IBKR Mobile app**.

Once connected, the API is available on:
- **Port 4001** → Paper trading API
- **Port 4002** → Live trading API (read-only if configured)

### Step 6: Install Python Dependencies

```bash
pip install ib_async pandas
```

### Step 7: Test the Connection

```bash
python3 ~/.openclaw/workspace/skills/ibkr-openclaw/scripts/ibkr_client.py summary --port 4001
```

Expected output:
```
Account: ['DU1234567']
----------------------------------------
BuyingPower..............      500,000.00
NetLiquidation...........      125,000.00
TotalCashValue...........       25,000.00
StockMarketValue.........      100,000.00
FuturesPNL...............        -500.00
UnrealizedPnL............        3,200.00
```

## CLI Usage

### ibkr_client.py — Account, Positions & Quotes

```bash
# Account summary
python3 scripts/ibkr_client.py summary --port 4001

# All positions
python3 scripts/ibkr_client.py positions --port 4001

# Quick NAV
python3 scripts/ibkr_client.py nav --port 4001

# Quote a stock
python3 scripts/ibkr_client.py quote 2800 --exchange SEHK --currency HKD --port 4001
```

### Getting Historical Data (Python)

```python
from ib_async import IB, Stock

ib = IB()
ib.connect('127.0.0.1', 4001, clientId=1, readonly=True)

contract = Stock('2800', 'SEHK', 'HKD', primaryExchange='SEHK')
qualified = ib.qualifyContracts(contract)

bars = ib.reqHistoricalData(
    qualified[0], '', '6 M', '1 day', 'TRADES', True, 1
)

for bar in bars[-5:]:
    print(f"{bar.date} O:{bar.open} H:{bar.high} L:{bar.low} C:{bar.close} V:{bar.volume}")

ib.disconnect()
```

## API Port Reference

| Port | Mode | Description |
|---|---|---|
| 4001 | Paper | Paper trading API |
| 4002 | Live | Live trading API |
| 5900 | VNC | Remote desktop (if VNC enabled) |

## Troubleshooting

### 2FA not arriving
- Check IBKR Mobile app is logged in with the correct username
- Verify `TWOFA_DEVICE` matches your device name in IBKR web portal
- Check phone notification settings for IBKR app

### Connection timeout
- Ensure the container is running: `docker ps`
- Check logs: `docker logs algo-trader-ib-gateway-1 --tail 20`
- The Gateway restarts daily at 23:45 SGT (configured via `AUTO_RESTART_TIME`)

### Read-only errors
- `READ_ONLY_API=yes` prevents trading but allows all read queries
- Some ib_async features auto-request write access — ignore those errors
- Account summary and positions work fine in read-only mode

### Container won't start
- Check `.env` file has correct credentials
- Ensure ports 4001, 4002, 5900 are not in use: `netstat -tlnp | grep 400`
- Try recreating: `docker compose up -d --force-recreate`

## Security Notes

- `.env` contains your IBKR password in plain text — keep it secure
- `READ_ONLY_API=yes` prevents accidental trades
- VNC is bound to `127.0.0.1` (localhost only) by default
- The container auto-restarts daily to maintain connection

## Architecture

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────┐
│  OpenClaw   │────►│  ibkr_client.py  │────►│ IB Gateway  │
│  Agent      │     │  (ib_async)      │     │  (Docker)   │
└─────────────┘     └──────────────────┘     └──────┬──────┘
                                                     │
                                              ┌──────▼──────┐
                                              │ IBKR Servers│
                                              │ (live data) │
                                              └─────────────┘
```

## Credits

- [gnzsnz/ib-gateway-docker](https://github.com/gnzsnz/ib-gateway-docker) — IB Gateway Docker image
- [ib_async](https://github.com/ib-api-reloaded/ib_async) — Python IBKR API wrapper (maintained fork of ib_insync)
