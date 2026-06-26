# Hyperliquid BTC Auto Trader

**Fully autonomous BTC-USDC trading bot for Hyperliquid mainnet**

This skill turns Claude/OpenClaw into a complete, production-grade autonomous trading system using the exact sophisticated multi-timeframe anchored VWAP strategy you requested.

### Core Strategy (exactly as specified)
- Market regime detection (trending_bull, trending_bear, ranging, volatile, transition) using ADX14 + ATR% + SMA50/200
- Volume profile analysis with 50-bin HVN/LVN anchors
- Swing point detection with 5-candle lookback + 1.5× volume confirmation
- Multi-timeframe anchors: daily (last 7 days), weekly (last 4 weeks), swing points, volume nodes, trend-start anchors
- Anchored VWAP with 0.95 exponential time decay + confidence scoring
- Confluence zone detection (VWAP clusters within 0.5%)
- Weighted signal score combining:
  - VWAP deviation (core)
  - Confluence adjustment (±30)
  - Regime adjustment (±10)
  - Order book imbalance (top 20 levels, 25% weight)
  - Trade flow (last 50 trades, 20% weight)
  - Candle patterns (hammer, engulfing, volume surge, 15% weight)
- Performance-based anchor learning (win-rate × normalized P&L, updates daily after 10 trades)

### Position Management & Execution
- Base size: $2,000 USD
- Signal multiplier: 1.5× (strong ≥80), 1.2× (moderate 60-79)
- Max position: $10,000 USD absolute
- Dynamic TP/SL based on signal strength (2:1 RR on strong signals)
- 40× maximum leverage (hard-capped)
- Real market orders + limit TP + stop-market SL via official Hyperliquid SDK

### Non-Negotiable Safety Limits (enforced at every cycle)
- Max position $10,000
- Max daily loss $500 → pause trading
- Max 5 trades per day
- Minimum USDC balance $20 (configurable)
- Pause after 3 consecutive losses
- 5-minute cooldown after every trade
- Circuit breaker on signal jumps >50 points in <60 seconds
- Manual kill switch available

### Quick Start
1. Set your environment variables:
   ```powershell
   $env:HYPERLIQUID_WALLET_ADDRESS = "0x..."
   $env:HYPERLIQUID_PRIVATE_KEY = "0x..."


   
#### 2. of `SKILL.md`

After the frontmatter, add this richer body (replace everything after the `---`):

```markdown
# Hyperliquid BTC Autonomous Trader

**This skill runs a complete autonomous BTC-USDC trading bot on Hyperliquid mainnet using the sophisticated multi-timeframe anchored VWAP strategy.**

The bot continuously:
- Pulls real 1-minute candles, L2 order book, and recent trades
- Detects market regime and selects the best anchors
- Calculates anchored VWAPs with exponential decay
- Identifies confluence zones
- Combines 6 different signal components into a final score
- Executes real trades when score ≥ ±60
- Enforces every safety limit you specified

All calculations use real Hyperliquid API data (no placeholders).

**How to use this skill**
- Say “Start hyperliquid-btc-auto-trader” to launch the live trading loop
- Say “Show current signal” to see live score, regime, and confluence zones
- Say “Pause the trader” or “Stop the trader” at any time

**Safety first**  
All 8 hard safety limits are coded and cannot be bypassed. The bot will never risk more than you allow.

**Ready to trade**  
Once started, the bot runs completely autonomously 24/7 until you tell it to stop.