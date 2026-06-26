---
name: polymarket-bot
description: Polymarket 5-minute crypto UP/DOWN market automated trading bot. AI-powered prediction using Binance technical analysis (Position, Momentum, RSI, Volume), automated betting via Polymarket CLOB API with gnosis-safe wallet mode. Use when setting up automated crypto trading on Polymarket, monitoring 5-minute BTC/ETH markets, or managing prediction market positions.
---

# Polymarket Trading Bot

Automated trading bot for Polymarket 5-minute crypto UP/DOWN markets.

## Architecture

```
auto_bot_v2.py (Main Loop)
  → Detects new 5-min markets (BTC/ETH)
  → Fetches Price-To-Beat via Playwright
  → Triggers AI analysis 80-100s before close

ai_analyze_v2.py (Decision Engine)
  → Binance technical analysis
  → Confidence scoring (Position 50%, Momentum 30%, RSI 10%, Volume 10%)
  → Executes bets via Polymarket CLI

monitor_bets.py (Notifications)
  → Monitors logs/bets.jsonl
  → Sends Telegram notifications on new bets

trading_state.py (Risk Management)
  → Tracks wins/losses
  → Enforces cooldown after consecutive losses
```

## Setup

1. Install Polymarket CLI and configure wallet (gnosis-safe mode)
2. Install dependencies: `pip install requests playwright`
3. Configure Telegram bot token and chat ID in `monitor_bets.py`
4. Run: `python3 -u auto_bot_v2.py > logs/bot.log 2>&1 &`

## Strategy Parameters

Edit in `scripts/ai_analyze_v2.py`:

- **Confidence threshold**: ≥85% (line 63)
- **EV threshold**: >0.6 (line 64)
- **Max odds**: <0.85 (line 65)
- **Bet size**: Fixed 5 shares (Polymarket minimum)

## Key Files

- `scripts/auto_bot_v2.py` - Main monitoring loop
- `scripts/ai_analyze_v2.py` - AI decision engine with bet execution
- `scripts/monitor_bets.py` - Telegram notification script
- `scripts/trading_state.py` - Win/loss tracking and cooldown logic

## Important Notes

- 5-minute markets cannot be exited early (orderbook disappears after close)
- Bot uses Binance data; Polymarket resolves via Chainlink (potential discrepancy)
- Minimum order: 5 shares (Polymarket hard limit)
- Uses `--signature-type gnosis-safe` for all CLI commands
