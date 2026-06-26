---
name: Polymarket AutoTrader
description: Auto-trade BTC, ETH, SOL, XRP on Polymarket price prediction markets at 5-minute and 15-minute intervals using RSI, MACD, and EMA signals.
version: 1.0.0
metadata:
  openclaw:
    emoji: 📈
    homepage: https://polymarket.com
    primaryEnv: POLYMARKET_PRIVATE_KEY
    requires:
      env:
        - POLYMARKET_PRIVATE_KEY
        - SKILLPAY_USER_ID
      bins:
        - node
    install:
      - kind: node
        package: "@polymarket/clob-client"
        bins: []
      - kind: node
        package: ethers
        bins: []
---

# Polymarket AutoTrader

Automatically trades BTC, ETH, SOL, and XRP price prediction markets on [Polymarket](https://polymarket.com) using short-term technical analysis signals.

## How It Works

1. **Signal Generation** — Fetches OHLCV candles from Binance (public API, no key required) for each asset on the selected timeframe (5m or 15m). Computes RSI(14), MACD(12/26), and EMA(9/21) crossover.

2. **Market Discovery** — Queries the Polymarket Gamma API to find active, unclosed price prediction markets for the relevant asset expiring soon.

3. **Order Placement** — If signal confidence ≥ `MIN_CONFIDENCE` (default 60%), places a limit order on the soonest-expiring market:
   - **BUY signal** → buy YES tokens
   - **SELL signal** → buy NO tokens

4. **Billing** — Each cycle deducts 0.001 USDT via SkillPay before executing. If balance is insufficient, a top-up link is returned.

5. **Scheduler** — Runs automatically every 5 or 15 minutes (set via `TRADE_TIMEFRAME`).

## Required Environment Variables

| Variable | Description |
|---|---|
| `POLYMARKET_PRIVATE_KEY` | Ethereum wallet private key (Polygon/MATIC network). Used to sign orders. |
| `SKILLPAY_API_KEY` | SkillPay API key for billing (from your SkillPay dashboard). |
| `SKILLPAY_USER_ID` | Your SkillPay user ID for billing. |
| `POLYMARKET_API_KEY` | _(Optional)_ Polymarket CLOB API key for higher rate limits. |
| `POLYMARKET_API_SECRET` | _(Optional)_ Polymarket CLOB API secret. |
| `POLYMARKET_API_PASSPHRASE` | _(Optional)_ Polymarket CLOB API passphrase. |

## Optional Environment Variables

| Variable | Default | Description |
|---|---|---|
| `TRADE_TIMEFRAME` | `5m` | `5m` or `15m` |
| `TRADE_ASSETS` | `BTC,ETH,SOL,XRP` | Comma-separated list of assets to trade |
| `MAX_TRADE_USDC` | `10` | Maximum USDC to spend per trade |
| `MIN_CONFIDENCE` | `60` | Minimum signal confidence % required to place a trade |
| `DRY_RUN` | `false` | Set `true` to simulate without placing real orders |

## Quickstart

### 1. Install dependencies
```bash
npm install
```

### 2. Set environment variables
```bash
export POLYMARKET_PRIVATE_KEY="0xYOUR_WALLET_PRIVATE_KEY"
export SKILLPAY_USER_ID="your_skillpay_user_id"
export TRADE_TIMEFRAME="5m"
export DRY_RUN="true"   # Start with dry run!
```

### 3. Get Polymarket API credentials (optional but recommended)
Visit https://clob.polymarket.com and follow the authentication guide to generate API keys for higher order limits.

### 4. Run
```bash
node trader.js
```

### 5. Run as a persistent service (Linux/Mac)
```bash
# Using pm2
npm install -g pm2
pm2 start trader.js --name polymarket-autotrader
pm2 save
```

## Strategy Details

### 5-Minute Timeframe
Optimized for scalping short-duration markets. Uses tighter RSI thresholds (35/65) and requires volume confirmation.

### 15-Minute Timeframe
Captures medium-term momentum. Suitable for markets expiring same-day or next day.

### Signal Scoring
| Indicator | Bullish | Bearish |
|---|---|---|
| RSI < 35 | +2 | — |
| RSI > 65 | — | +2 |
| MACD > 0 | +1 | — |
| EMA9 > EMA21 | +2 | — |
| Volume spike (bullish) | +1 | — |

Signal is `BUY` or `SELL` only when the winning side scores ≥ 4.

## Risk Warning

⚠️ Polymarket prediction markets are binary (YES/NO) and highly volatile. Past signal performance does not guarantee future results. Always start with `DRY_RUN=true` and small position sizes. Never risk capital you cannot afford to lose.

## Usage (via Claude Code)

When this skill is active, you can ask Claude to:

- `"Run the Polymarket AutoTrader for BTC and ETH on the 15m timeframe"`
- `"Show me the current signals for all assets"`
- `"Start the trader in dry-run mode"`
- `"Check what Polymarket markets are available for SOL"`

Claude will run `trader.js` with the appropriate environment variables set.
