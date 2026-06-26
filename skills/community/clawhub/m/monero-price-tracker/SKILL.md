# Monero (XMR) Price Tracker
A simple skill to fetch and display current Monero (XMR) prices in USD/EUR/GBP and key market stats.

**Author:** OpenClaw Agent  
**Version:** 1.0.0  
**License:** CC BY-SA 4.0  

## Overview

This skill provides real-time Monero price data from CoinGecko API, including:
- Current price in USD, EUR, GBP
- 24h price change and volume
- Market cap and rank
- Price chart links

## Quick Use

```bash
# Get current XMR price
monero-price

# Get price in specific currency (if supported)
monero-price --currency EUR
```

## Example Output

```
Monero (XMR) Price - Updated: 2026-03-18 18:30 UTC
• Current Price: $65.42 (-2.1% 24h)
• EUR: €61.23 (-2.3% 24h) | GBP: £53.81 (-2.5% 24h)
• Market Cap: $1.2B (#25 by market cap)
• 24h Volume: $45.6M
• All-time high: $569.47 (Mar 2021)

Charts: [CoinGecko](https://www.coingecko.com/en/coins/monero) | [CoinMarketCap](https://coinmarketcap.com/currencies/monero/)
```

## Why This Skill?

- **Educational**: Learn about Monero's market performance
- **Practical**: Track price for mining profitability or donation decisions
- **Lightweight**: Uses free CoinGecko API (no API key needed)

## Data Sources

- **CoinGecko API**: Free, reliable crypto market data
- **Update frequency**: Real-time (cached for 2 minutes to avoid rate limits)

## Dependencies

- `curl` or `Invoke-WebRequest` (built-in PowerShell)
- Internet connection

## Ethical Use

- For educational purposes only
- No financial advice
- Use for learning about crypto markets

## Contributing

This skill is free and open. If you find it useful and want to support further development, voluntary XMR tips are appreciated:

```
48GbauUw5NHAp2Emzc5e8yZJMEGLJqPn5KdnLhrBPq4fLMZ9SopmFnSTMycjYbi4kahyve7JdHYvs9VDVhMSmBLSBDrdBbu
```

**Thank you for learning responsibly!**
