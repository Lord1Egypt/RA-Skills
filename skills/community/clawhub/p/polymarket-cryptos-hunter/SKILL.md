---
name: polymarket-cryptos-hunter
description: HFT Market Making bot for Polymarket. Live execution via Web3 and CLOB API.
---

# Hunter Ultimate - Live Trading

This is a continuous, high-frequency Python bot that executes market-making strategies on Polymarket using real money. It reads the portfolio balance directly from the Polygon blockchain.

## Role of the AI Agent

You are the Portfolio Manager. Your only job is to start the bot. The bot runs indefinitely in the background and has a built-in 15% Stop Loss.

## Commands

Run this script to start the continuous trading bot. You MUST use `cd` to enter the skill directory first, and then use `nohup` and `&` to run the virtual environment's Python executable in the background. This ensures you do not block the terminal.

```bash
# Navigate to the skill folder and start the live trading bot in the background
cd polymarket-cryptos-hunter && nohup .venv/bin/python main.py start > bot_log.txt 2>&1 &
```
