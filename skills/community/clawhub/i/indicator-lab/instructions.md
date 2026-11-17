# Indicator Lab — Technical Analysis Backtesting

Backtest 13 technical indicators against SPY and QQQ on 5-year daily data.

## Quick Start
```bash
python scripts/indicator_backtest.py
```

## What It Tests
| Category | Indicators |
|---|---|
| Momentum | RSI(7), RSI(14), Stochastic, WilliamsR, CCI |
| Trend | MACD, SMA cross(20,50), SMA cross(50,200), ADX |
| Volatility | Bollinger(20,2), ATR trail |
| Volume | OBV, MFI |

## Output
- Single indicator performance (return, Sharpe, max DD, win rate)
- 2-indicator AND combinations
- 3-indicator triple combos
- Ranked by Sharpe + return - max DD score
- Compared vs Buy & Hold baseline

## Requirements
```
pip install pandas pandas-ta yfinance plotly
```

## Usage
```
"Backtest RSI against QQQ"
"Find the best 3-indicator combo for SPY"
"Compare MACD vs Bollinger on SPY last 5 years"
```