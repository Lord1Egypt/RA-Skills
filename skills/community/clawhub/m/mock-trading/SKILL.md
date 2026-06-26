---
name: mock-trading-agent
description: Simulate cryptocurrency trading using algorithmic strategies (SMA Crossover, Mean Reversion) without risking real capital. Use when the user wants to start a paper trading simulation, test a trading bot, or monitor a mock portfolio.
---

# Mock Trading Agent Skill

This skill provides a fully functional mock (paper) trading environment. It allows OpenClaw to simulate algorithmic trading by fetching live market data, evaluating algorithmic strategies, and updating a virtual portfolio.

## Components

- **`assets/portfolio.json`**: A template virtual bank account containing $10,000 USD. 
- **`scripts/mock_bot.py`**: A python script that executes a single "tick" of the trading bot. It fetches the current price, evaluates the strategy based on price history, executes mock trades, and updates the portfolio file.

## Setup & Usage

When a user asks to start a mock trading session:

1. **Initialize the Portfolio**: 
   Copy the template portfolio to the user's working directory.
   ```bash
   cp {baseDir}/assets/portfolio.json ./my_portfolio.json
   ```

2. **Run a Trading Tick**:
   Run the bot script. This executes a single cycle (fetch data -> evaluate -> trade -> save).
   ```bash
   uv run {baseDir}/scripts/mock_bot.py --portfolio ./my_portfolio.json --asset bitcoin
   ```

3. **Automation (Heartbeat/Cron)**:
   To run the bot continuously, add the command from Step 2 into the user's `HEARTBEAT.md` file or schedule it via cron to run every 5-10 minutes.

4. **Reporting**:
   Read `./my_portfolio.json` to report the user's current PnL, cash balance, and trade history.

## Modifying Strategies
The script currently defaults to an **SMA Crossover** strategy. You can edit the python script locally to swap it with Mean Reversion, Momentum Breakout, or RSI strategies if the user requests different logic.