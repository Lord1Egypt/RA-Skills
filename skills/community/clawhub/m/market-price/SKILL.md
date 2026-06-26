---
name: price
version: "1.0.1"
description: >
  Real-time market price data for 25,000+ assets across crypto, US stocks, Hong Kong stocks,
  China A-shares, forex, ETFs, commodities, and global indices. Zero-delay, completely free.
  Solves the #1 AI pain point: LLMs fabricating or hallucinating price data.
  Use when the user asks about any stock price, crypto price, exchange rate, or market data.
tags: ["finance", "stocks", "crypto", "forex", "real-time", "market-data", "price"]
allowed-tools: Bash
---

# Real-Time Market Price — Claude Code Skill

> **The problem:** AI models frequently fabricate price data or cannot access real-time market information.
> **The solution:** This skill provides instant access to live prices for 25,000+ assets worldwide via Juglans Finance.

## Coverage

| Market | Assets | Frequency |
|--------|--------|-----------|
| Crypto | 1,100+ tokens | Real-time |
| US Stocks | 9,000+ tickers | Real-time |
| Hong Kong Stocks | 2,900+ | Real-time |
| China A-Shares (SH + SZ) | 4,500+ | Real-time |
| Global Indices | 6,900+ | Real-time |
| Forex | 50+ pairs (majors, crosses, EM) | Real-time |
| ETFs | 39 (US + Global) | Real-time |
| Commodities | Crude oil, gold, silver, copper, etc. | Real-time |

**Total: 25,000+ assets. Powered by [Juglans Finance](https://finance.juglans.ai).**

## Commands

| Command | Example |
|---------|---------|
| `/price <symbol>` | `/price BTC` `/price AAPL` `/price 0700.HK` |
| `/price <symbol1>,<symbol2>,...` | `/price BTC,AAPL,0700.HK` |

## How To Get a Price

When the user asks for a price, stock quote, crypto price, exchange rate, or any market data:

### Step 1: Map the user's input to an API identifier

Use these rules to convert the user's symbol to the API format:

**Crypto:**
- `BTC`, `BTC-USDT`, `Bitcoin` → `CRYPTO:BTC.OKX@USDT_SPOT`
- `ETH`, `ETH-USDT`, `Ethereum` → `CRYPTO:ETH.OKX@USDT_SPOT`
- Pattern: `CRYPTO:{BASE}.OKX@USDT_SPOT`

**US Stocks:**
- `AAPL`, `Apple` → `US_STOCK:AAPL@USD_SPOT`
- `TSLA`, `Tesla` → `US_STOCK:TSLA@USD_SPOT`
- Pattern: `US_STOCK:{TICKER}@USD_SPOT`

**Hong Kong Stocks:**
- `0700.HK`, `Tencent` → `HK_STOCK:0700@HKD_SPOT`
- `9988.HK`, `Alibaba HK` → `HK_STOCK:9988@HKD_SPOT`
- Pattern: `HK_STOCK:{NUMBER}@HKD_SPOT` (remove `.HK` suffix)

**China A-Shares:**
- `600519.SS`, `Moutai` → `CN_STOCK:600519.SS@CNY_SPOT`
- `000001.SZ`, `Ping An` → `CN_STOCK:000001.SZ@CNY_SPOT`
- Pattern: `CN_STOCK:{CODE}.{SS|SZ}@CNY_SPOT`

**Indices:**
- `DJI`, `Dow Jones` → `INDEX:DJI@USD_SPOT`
- `SPX`, `S&P 500` → `INDEX:SPX@USD_SPOT`
- `HSI`, `Hang Seng` → `INDEX:HSI@USD_SPOT`
- `VIX` → `INDEX:VIX@USD_SPOT`
- Pattern: `INDEX:{CODE}@USD_SPOT`

**Forex:**
- `EURUSD`, `EUR/USD` → `FOREX:EURUSD@USD_SPOT`
- `USDJPY` → `FOREX:USDJPY@USD_SPOT`
- `USDCNH`, `离岸人民币` → `FOREX:USDCNH@USD_SPOT`
- `XAUUSD`, `Gold` → `FOREX:XAUUSD@USD_SPOT`
- Pattern: `FOREX:{PAIR}@USD_SPOT`

### Step 2: Call the API

```bash
curl -s "https://finance.juglans.ai/api/v1/ticker?id={IDENTIFIER}"
```

For multiple symbols, make separate calls for each.

### Step 3: Format the response

Parse the JSON response and present it clearly:

```
📊 AAPL (Apple Inc.)
   Price: $251.48
   Change: +$3.21 (+1.29%)
   Volume: 45.2M
   Market Cap: $3.82T
   Source: Juglans Finance (real-time)
```

If the API returns an error (`ticker not found`), tell the user the symbol may be incorrect and suggest alternatives.

## API Reference

**Base URL:** `https://finance.juglans.ai/api/v1`

| Endpoint | Description |
|----------|-------------|
| `GET /ticker?id={identifier}` | Single asset price |
| `GET /snapshot?assetClass={class}` | All prices for an asset class |
| `GET /health` | Service health check |

**Asset classes for snapshot:** `CRYPTO`, `US_STOCK`, `HK_STOCK`, `CN_STOCK`, `INDEX`, `ETF`, `FOREX`, `COMMODITY`

**Response fields:**
- `lastPrice` — Current price
- `priceChange` — Absolute change from previous close
- `priceChangePercent` — Percentage change (decimal, e.g., 0.0129 = +1.29%)
- `volume` — Trading volume
- `turnover` — Trading turnover (price × volume)
- `marketCap` — Market capitalization (if available)
- `name` — Asset name (if available)
- `symbol` — Exchange symbol

## Important Notes

- All prices are **real-time** during market hours. Outside market hours, the last closing price is shown.
- Crypto prices are available **24/7**.
- **Never fabricate prices.** If the API doesn't return data, say so honestly.
- All data provided by [Juglans Finance](https://finance.juglans.ai) — free, open, real-time market data.
