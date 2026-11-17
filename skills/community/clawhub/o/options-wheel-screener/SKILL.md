---
name: options-wheel-screener
description: Screen a watchlist of stock tickers for cash-secured put candidates suited to the options wheel strategy, using free Yahoo Finance data via yfinance with no API key required. Finds the expiration nearest a target days-to-expiration window, selects the put strike closest to a target out-of-the-money percentage, and estimates period and annualized premium yield alongside implied volatility, volume, and open interest. Built for options trading, income-generation, and passive income workflows where selling premium on quality tickers is the core strategy. Idea generation only — does not place trades or connect to a broker.
compatibility: Created for Zo Computer
metadata:
  author: ssyopros.zo.computer
---

# Options Wheel Strategy Screener

Scans a ticker watchlist for cash-secured put candidates that fit the
options "wheel" strategy — selling puts for premium income, with the
willingness to take assignment and sell covered calls if exercised.

## When to use this skill

- Building a weekly/monthly watchlist of wheel candidates across a basket
  of tickers
- Comparing annualized premium yield across tickers at a consistent
  DTE (days-to-expiration) and OTM% target
- Quickly checking liquidity (volume, open interest) before considering a
  strike

## How to use it

```
python3 scripts/wheel_screener.py AAPL MSFT KO PEP --dte 30 --otm-pct 5
python3 scripts/wheel_screener.py AAPL --dte 21 --otm-pct 8 --min-premium-yield 1.0
```

- `--dte`: target days to expiration (the script picks the closest
  available real expiration)
- `--otm-pct`: how far out-of-the-money to target the put strike
- `--min-premium-yield`: flags rows meeting an annualized-yield-implied
  minimum period yield with an asterisk

## Limitations

- Uses moneyness (strike distance from spot) as a delta proxy, not live
  option greeks — yfinance does not expose real-time delta
- Premium is estimated from bid/ask midpoint, which can be stale or wide
  for illiquid names — always check the live quote before trading
- Screening/idea-generation only; does not execute trades or connect to a
  brokerage. Not financial advice.
