# Polymarket Portfolio Tracker

Real-time Polymarket position monitor with P&L tracking, profit alerts, and auto-reinvestment. Runs as a cron job every 30 minutes or as a standalone daemon. Sends Telegram alerts on resolved positions, big price moves, and reinvestment activity.

## What It Does

- Fetches all open positions from Polymarket Data API
- Detects resolved positions (WIN/LOSS) and calculates P&L
- Alerts on 20%+ price moves on open positions
- **Circuit breaker:** Pauses all new trades if daily loss > 15%
- **Auto-reinvest:** When cash ≥ $40, triggers reinvestment scripts
- Tracks cumulative P&L, ROI, and progress toward your goal
- Silent HEARTBEAT_OK when nothing notable (no notification spam)

## Features

| Feature | Detail |
|---------|--------|
| Position tracking | All open Polymarket positions |
| Resolved detection | WIN/LOSS with P&L calculation |
| Price move alerts | 20%+ moves on meaningful positions |
| Circuit breaker | 15% daily loss limit |
| Auto-reinvest | Triggers when cash ≥ $40 |
| Goal tracking | Progress toward $ target |
| Telegram alerts | Resolved positions + big moves |

## Setup

```bash
pip install requests
```

Edit constants at the top of `monitor.py`:
```python
WALLET = "0xYourPolymarketWallet"
```

Or set via environment:
```
PRIVATE_KEY=your_polygon_private_key
WALLET_ADDRESS=0xYourPolymarketWallet
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

## Usage

```bash
# Run once
python3 monitor.py

# Run via cron every 30 minutes
*/30 * * * * cd /path/to/scripts && python3 monitor.py >> logs/monitor.log 2>&1
```

## Output Example (Telegram Alert)

```
🦞 Polymarket Update — 2025-03-15 14:30 UTC

Resolved/Moved:
  ✅ WON +$18.40 — YES | Will Bitcoin exceed $90k by March?
  📈 MOVE +22% — YES now 73% | Will Fed pause in March?

Portfolio: $1,247.82 | 12 open positions
Total P&L: +$183.40 on $892.00 wagered (20.6% ROI)
Cash: $156.20
Goal: $5,000 (3.7% there) 🏁

Auto-reinvested: Deployed $80 into 2 plays
```

## Circuit Breaker

Automatically triggers if daily portfolio loss exceeds 15%:
- Pauses ALL new reinvestment
- Sends alert: "⛔ CIRCUIT BREAKER ACTIVE"
- Resets at midnight UTC

## State Files

- `.monitor_state.json` — position snapshots and cumulative P&L
- `.daily_pnl.json` — daily P&L tracking for circuit breaker

## Integration

Works alongside:
- `auto_reinvest.py` — sports plays reinvestment
- `weather_scanner.py` — weather market reinvestment  
- `exit_manager.py` — stop-loss/take-profit on Kalshi

## Requirements

- Python 3.9+
- `py_clob_client`: `pip install polymarket-clob-client`
- Polymarket wallet on Polygon
