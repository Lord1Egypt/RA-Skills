---
id: 'medici-investments-position-sizer'
name: 'medici-investments-position-sizer'
description: 'Calculate risk-based position sizes for long stock trades. Use when user
  asks about position sizing, how many shares to buy, risk per trade, Kelly criterion,
  ATR-based sizing, or portfolio risk allocation. Supports stop-loss distance calculation,
  volatility scaling, and sector concentration checks.'
version: '1.0.0'
author: 'DaVinci'
last_amended_at: null
trigger_patterns: []
pre_conditions:
  git_repo_required: false
  tools_available: []
expected_output_format: 'natural_language'
---

# Position Sizing Calculator

## Overview

This skill calculates the optimal position size for a long stock trade based on a defined risk management framework. It ensures that no single trade can disproportionately impact the portfolio.

**Core Features:**
- **Risk-Based Sizing**: Position size is determined by risk per trade, not a fixed dollar amount.
- **Multiple Sizing Models**: Supports Percent Risk, ATR (Average True Range) Volatility, and Kelly Criterion models.
- **Stop-Loss Integration**: Calculates the number of shares to buy based on the distance to the stop-loss.
- **Portfolio Context**: Checks for sector concentration and total portfolio risk.

---

## When to Use This Skill

**Explicit Triggers:**
- "How many shares of AAPL should I buy?"
- "Calculate the position size for a trade in TSLA."
- "My stop-loss for GOOG is at $170, how much should I buy?"
- User asks about "position sizing," "risk per trade," "Kelly criterion," or "ATR sizing."

**Implicit Triggers:**
- User is planning a new stock purchase and mentions an entry and stop-loss price.
- User is asking about how to manage risk on a new trade.

---

## Workflow

### Step 1: Gather Inputs

The user must provide the following information:

```bash
position-sizer calculate \
  --portfolio-value 100000 \
  --risk-per-trade-pct 1 \
  --entry-price 175.00 \
  --stop-loss-price 170.00 \
  --ticker AAPL \
  # Optional sizing model:
  --model percent-risk # (default) or 'atr' or 'kelly'
  # Required for ATR model:
  --atr 2.5
  # Required for Kelly model:
  --win-probability 0.60 \
  --win-loss-ratio 2.0
```

**Required Parameters:**
- `--portfolio-value`: Total value of the trading portfolio.
- `--risk-per-trade-pct`: The maximum percentage of the portfolio to risk on this single trade (e.g., 1 for 1%).
- `--entry-price`: The intended purchase price of the stock.
- `--stop-loss-price`: The price at which the position will be sold for a loss.

**Optional Parameters:**
- `--ticker`: The stock ticker (used for sector concentration checks).
- `--model`: The sizing model to use. Defaults to `percent-risk`.
- `--atr`: The Average True Range of the stock (required for `atr` model).
- `--win-probability` and `--win-loss-ratio`: Required for `kelly` model.

### Step 2: Execute Calculation Script

Run the position sizing script with the provided inputs:

```bash
python3 skills/position-sizer/scripts/position_sizer.py --portfolio-value 100000 ...
```

The script performs the calculations based on the selected model.

### Calculation Models

**1. Percent Risk (Default)**
- **Risk per Trade ($)** = Portfolio Value * (Risk per Trade % / 100)
- **Risk per Share ($)** = Entry Price - Stop-Loss Price
- **Number of Shares** = Risk per Trade ($) / Risk per Share ($)

**2. ATR Volatility Sizing**
- **Risk per Share ($)** = ATR * Multiplier (default 2x)
- **Stop-Loss Price** = Entry Price - Risk per Share ($)
- **Number of Shares** = Risk per Trade ($) / Risk per Share ($)
- *This model is useful when a stop-loss price is not predetermined.*

**3. Kelly Criterion (Advanced)**
- **Kelly %** = Win Probability - [(1 - Win Probability) / Win-Loss Ratio]
- **Position Size ($)** = Portfolio Value * Kelly %
- **Number of Shares** = Position Size ($) / Entry Price
- *This model optimizes for long-term geometric growth but can be aggressive. Often used at half-Kelly.*

### Step 3: Sector Concentration Check

If a `--ticker` is provided, the script will:
1. Fetch the sector for the ticker.
2. Check the current portfolio's allocation to that sector.
3. Issue a warning if the new position would push the sector's weight above a defined threshold (e.g., 25%).

### Step 4: Present the Results

The script outputs a JSON object and a human-readable summary.

**JSON Output:**
```json
{
  "model": "Percent Risk",
  "inputs": { ... },
  "results": {
    "risk_per_trade_usd": 1000,
    "risk_per_share_usd": 5,
    "num_shares_to_buy": 200,
    "position_size_usd": 35000,
    "position_size_pct_of_portfolio": 35.0
  },
  "warnings": [
    "This position will represent 35.0% of your portfolio. This is a highly concentrated position."
  ]
}
```

**Human-Readable Summary:**
- **Model Used**: Percent Risk
- **Max Risk on this Trade**: $1,000.00 (1.0% of $100,000 portfolio)
- **Entry / Stop**: $175.00 / $170.00 (Risk per share: $5.00)
- **Calculated Position Size**:
  - **Shares to Buy**: 200
  - **Total Position Value**: $35,000.00
- **Portfolio Impact**: This position will be 35.0% of your total portfolio.
- **Warnings**:
  - ⚠️ This is a highly concentrated position.

---

## Important Considerations

- **Integer Shares**: Remind the user that they can only buy whole shares, so rounding down is the safest approach.
- **Liquidity**: For large position sizes, warn about potential slippage on entry.
- **Not Financial Advice**: Include a disclaimer that this is a risk management tool, not a recommendation to buy or sell.
