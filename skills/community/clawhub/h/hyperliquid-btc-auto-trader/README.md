# Hyperliquid BTC Auto Trader

**Fully autonomous BTC-USDC trading bot on Hyperliquid mainnet**  
Implements the exact sophisticated multi-timeframe anchored VWAP strategy you requested.

**Features**
- Real-time regime detection (ADX + ATR + SMAs)
- Volume profile + HVN anchors
- Swing detection with volume filter
- Multi-timeframe anchors (daily + weekly)
- Anchored VWAP with 0.95 exponential decay
- Confluence zones
- Order book imbalance, trade flow, candle patterns
- Performance-based anchor learning
- Full safety limits (max $10k, $500 daily loss, 5 trades/day, etc.)
- 40x max leverage

Run with: `python trader.py`

Set env vars first:
```bash
export HYPERLIQUID_WALLET_ADDRESS="0x..."
export HYPERLIQUID_PRIVATE_KEY="0x..."