# Options Wheel Strategy Screener

A Python tool that screens tickers for cash-secured put candidates suited
to the options wheel strategy, using free Yahoo Finance data (`yfinance`).

## What it does

- Pulls the live option chain for each ticker
- Picks the expiration closest to your target DTE
- Picks the put strike closest to your target OTM%
- Estimates premium income, period yield, and annualized yield
- Reports implied volatility, volume, and open interest for liquidity checks

## Quick start

```bash
python3 scripts/wheel_screener.py AAPL MSFT KO PEP --dte 30 --otm-pct 5
```

## Dependencies

```
pip install yfinance
```

## Disclaimer

This is an idea-generation and screening tool only. It does not place
trades, connect to a brokerage, or account for assignment risk, taxes, or
portfolio margin requirements. Verify all quotes live before trading. Not
financial advice.
