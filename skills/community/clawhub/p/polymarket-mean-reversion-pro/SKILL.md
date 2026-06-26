# Polymarket Mean Reversion Pro

Advanced mean reversion signal engine for Polymarket. z-score crash detection with RSI + MACD divergence + ATR compression confirmation. Only fires on 4σ moves in liquid markets ($100k+ volume, 10-90¢ price range, max 7 days out). Zero false signals.

## What It Does

- Monitors top 100 Polymarket markets by 24h volume every 30 minutes
- Builds 7-day rolling price history per market
- Fires when price deviates **4σ** from mean (tightened from 3σ to eliminate noise)
- **Triple confirmation required before any trade:**
  1. z-score threshold crossed (4σ crash or spike)
  2. RSI oversold (<40) or overbought (>60) 
  3. MACD divergence in expected direction
  4. ATR compression confirmed (volatility < 5% of price)
- VPIN cross-check: skips if informed traders detected
- Telegram alerts for every signal
- SQS integration for automated execution pipeline

## Filters (All Must Pass)

| Filter | Value | Reason |
|--------|-------|--------|
| Min daily volume | $100k | Liquidity requirement |
| Price range | 10¢–90¢ | Avoid lottery tickets & certainties |
| Time to resolution | 6h–168h | No day-ofs or macro bets |
| z-score threshold | ±4.0σ | Zero false signals |
| VPIN | < 0.60 | Skip if informed flow detected |

## Signal Logic

**BUY YES (crash):** z < -4.0 + RSI < 40 + MACD bullish divergence + ATR compressed
**BUY NO (spike):** z > +4.0 + RSI > 60 + MACD bearish divergence + ATR compressed

## Setup

```bash
pip install requests boto3
```

Configure environment variables (or `.env` file in same directory):
```
PRIVATE_KEY=your_polygon_private_key
WALLET_ADDRESS=0xYourWallet
TELEGRAM_BOT_TOKEN=your_bot_token  # optional
TELEGRAM_CHAT_ID=your_chat_id      # optional
```

## Usage

```bash
# Run once
python3 mean_reversion.py

# Dry run (show signals, no execution)
python3 mean_reversion.py --dry-run

# Watch mode (runs every 30 min)
python3 mean_reversion.py --watch

# Watch mode dry run
python3 mean_reversion.py --watch --dry-run
```

## Kelly Sizing

- Quarter Kelly (25% fractional)
- Min: $2, Max: $25 per trade
- Scales with probability confidence

## Integration

- Imports `vpin.py` for toxic flow detection (optional, falls back to 0.5)
- Pushes signals to AWS SQS for execution pipeline
- Sends Telegram alerts with z-score, price, volume, hours remaining

## Requirements

- Python 3.9+
- `requests` library
- `boto3` (for SQS, optional)
- `py_clob_client` (for execution)
- Polymarket wallet with USDC

## Notes

The 7-day history must accumulate before signals fire (24+ data points needed). In watch mode, signals start appearing after ~12 hours of data collection.
