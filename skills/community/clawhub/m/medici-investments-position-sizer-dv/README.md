# Position Sizer

Calculate risk-based position sizes for stock trades using fixed fractional, ATR-based, or Kelly Criterion methods.

## Description

Position Sizer determines the optimal number of shares to buy for a stock trade based on risk management principles. It supports three calculation methods: Fixed Fractional (risk a fixed % per trade), ATR-Based (volatility-adjusted stops), and Kelly Criterion (mathematically optimal allocation from win/loss stats). The skill enforces portfolio constraints like maximum position size and sector concentration limits.

## Key Features

- **Three sizing methods** - Fixed fractional, ATR-based, Kelly Criterion
- **Risk-based calculation** - Never risk more than specified % of account per trade
- **Stop-loss integration** - Calculate position size from entry and stop prices
- **Volatility adjustment** - ATR-based sizing for different volatility regimes
- **Portfolio constraints** - Max position %, max sector % enforcement
- **Kelly Criterion** - Optimal sizing from win rate and payoff ratio statistics
- **Detailed breakdown** - Risk per share, dollar risk, position value, % of account

## Quick Start

```bash
# Fixed Fractional: Risk 1% of $100k account
python3 scripts/position_sizer.py \
  --account-size 100000 \
  --entry 155 \
  --stop 148.50 \
  --risk-pct 1.0

# ATR-Based: Use 2x ATR stop distance
python3 scripts/position_sizer.py \
  --account-size 100000 \
  --entry 155 \
  --atr 3.20 \
  --atr-multiplier 2.0 \
  --risk-pct 1.0

# Kelly Criterion: 55% win rate, 1.5:1 payoff
python3 scripts/position_sizer.py \
  --account-size 100000 \
  --kelly \
  --win-rate 0.55 \
  --avg-win 1500 \
  --avg-loss 1000 \
  --entry 155 \
  --stop 148.50
```

**Output:**
```
POSITION SIZING REPORT

Account Size: $100,000
Entry Price: $155.00
Stop Price: $148.50
Risk Per Share: $6.50
Risk Percentage: 1.0%
Max Dollar Risk: $1,000

Shares to Buy: 153
Position Value: $23,715
Position % of Account: 23.7%

Risk Management:
- Dollar Risk: $994.50
- R-Multiple on Entry: 1.0R
- If stopped out: Account becomes $99,005.50
```

## What It Does NOT Do

- Does NOT provide trade entry or exit signals
- Does NOT calculate optimal stop-loss levels (user must provide)
- Does NOT account for partial fills or slippage
- Does NOT manage multi-leg option positions (stocks only)
- Does NOT guarantee profitable trades (risk management tool only)

## Requirements

- Python 3.9+
- No external dependencies (standard library only)
- No API keys required

## License

MIT
