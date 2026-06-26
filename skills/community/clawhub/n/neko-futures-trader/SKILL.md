---
name: neko-futures-trader
description: |
  Professional Binance Futures automated trading system with AI-powered signal detection.
  
  🎯 CORE FEATURES:
  - Auto Entry: Scanner finds signals every 5 minutes
  - Auto SL/TP: Price monitor checks every 1 second
  - Auto Cache Cleanup: Removes expired entries on startup
  - Auto Breakeven: Moves SL to entry at +5%
  - Auto Trailing TP: Activates at +10%
  - Auto Delisting: Blocks delisted tokens
  - Auto Recovery: Self-heals from errors
  
  📊 STRATEGY:
  - Multi-TP: 40% @ +10%, 30% @ +15%, 30% @ +20%
  - Dynamic ATR: SL/TP adjusts to volatility
  - 14 Indicators: RSI, MACD, Bollinger, VWAP, EMA, etc.
  - 64 SAFE_COINS pre-filtered
  
  ⚙️ SETTINGS (in config.py):
  - MAX_POSITIONS = 7
  - ENTRY_PERCENT = 6%
  - MIN_PROFIT_BREAKEVEN = 5.0%
  - MIN_PROFIT_TRAILING_TP = 10.0%
  - CHECK_INTERVAL = 1 second
  
  📁 FILES:
  - scanner-v8.py (main scanner)
  - price-monitor.py (TP/SL executor)
  - config.py (all settings)
  - advanced_analysis.py (indicators)
  - error_handling.py (self-healing)
  - delisting_monitor.py (safety)
  - position_command.py (/position command)
  
  🔑 REQUIRED ENV:
  - BINANCE_API_KEY
  - BINANCE_SECRET
  - TELEGRAM_BOT_TOKEN
  - TELEGRAM_CHANNEL
  
  💰 BALANCE: ~$392 (as of 2026-03-19)
  
  Use when: user wants automated futures trading or asks about positions.
  
metadata:
  openclaw:
    emoji: 🐱📈
    requires:
      bins: ["python3"]
      env:
        - BINANCE_API_KEY
        - BINANCE_SECRET
        - TELEGRAM_BOT_TOKEN
        - TELEGRAM_CHANNEL
    startup:
      command: "cd /root/.openclaw/workspace/neko-futures-trader && nohup bash -c 'while true; do source .env && python3 scanner-v8.py; sleep 300; done' > scanner.log 2>&1 &"
      type: "background"
---

# Neko Futures Trader 🐱📈

## Quick Install (For New Agent)

```bash
# 1. Navigate to workspace
cd /root/.openclaw/workspace/neko-futures-trader

# 2. Check files exist
ls -la *.py *.md

# 3. Verify .env exists
cat .env | head -3

# 4. Start scanner
nohup python3 scanner-v8.py &

# 5. Start price monitor
nohup python3 price-monitor.py &

# 6. Check status
python3 position_command.py
```

## Auto Features (All Running)

| Feature | Status | Description |
|---------|--------|-------------|
| 🔍 Auto Entry | ✅ ON | Scanner runs every 5 min |
| ⏱️ Auto TP/SL | ✅ ON | Price monitor every 1 sec |
| 🧹 Auto Cache | ✅ ON | Cleans 24h old entries on startup |
| 🛡 Auto Breakeven | ✅ ON | SL → Entry at +5% |
| 🎯 Auto Trailing | ✅ ON | TP trails at +10% |
| 🚫 Auto Delisting | ✅ ON | Blocks bad tokens |
| 🔄 Auto Recovery | ✅ ON | Self-heals from errors |
| 📱 Auto Notify | ✅ ON | Telegram alerts |

## Configuration (config.py)

```python
# === TRADING ===
MAX_POSITIONS = 7
AUTO_FILL_EMPTY_SLOTS = True
ENTRY_PERCENT = 6%
LEVERAGE = 10

# === RISK ===
MIN_PROFIT_BREAKEVEN = 5.0      # SL → Entry at +5%
MIN_PROFIT_TRAILING_TP = 10.0   # Trail at +10%

# === MULTI-TP (1:2 R/R) ===
TP1_PERCENT = 10.0   # Close 40% @ +10%
TP2_PERCENT = 15.0   # Close 30% @ +15%
TP3_PERCENT = 20.0   # Close 30% @ +20%

# === DYNAMIC ATR ===
ATR_MULTIPLIER_SL_HIGH = 2.0    # High vol: SL 2×ATR
ATR_MULTIPLIER_TP_HIGH = 4.0    # High vol: TP 4×ATR
ATR_MULTIPLIER_SL_NORMAL = 1.5  # Normal: SL 1.5×ATR
ATR_MULTIPLIER_TP_NORMAL = 3.0  # Normal: TP 3×ATR
ATR_MULTIPLIER_SL_LOW = 1.0     # Low vol: SL 1×ATR
ATR_MULTIPLIER_TP_LOW = 2.5     # Low vol: TP 2.5×ATR

# === MONITOR ===
CHECK_INTERVAL = 1  # seconds
```

## Signal Indicators (v1.0.36)

| # | Indicator | Condition | Score |
|---|-----------|-----------|-------|
| 1 | Volume Spike | >3x avg | +2 |
| 2 | Price Change | >10% | +2 |
| 3 | 1H Change | >3% | +1 |
| 4 | Breakout | HH/HL broken | +2 |
| 5 | Breakdown | LH/LL broken | +2 |
| 6 | OI Increase | >20% | +2 |
| 7 | Weekly Change | >20% | +3 |
| 8 | Pocket Pivot | Yes | +2 |
| 9 | RSI | <30 or >70 | +1 |
| 10 | MACD Cross | Histogram | +1 |
| 11 | Bollinger | Band touch | +1 |
| 12 | VWAP Cross | Price cross | +1 |
| 13 | Volume 5x | Extra spike | +2 |
| 14 | DCR | >20% | +1 |

**Minimum Score: 3 to trigger signal**

## File Structure

```
neko-futures-trader/
├── scanner-v8.py          # Main scanner (auto entry)
├── price-monitor.py       # TP/SP executor (auto close)
├── config.py             # All settings
├── advanced_analysis.py   # RSI, MACD, etc.
├── error_handling.py     # Circuit breaker, rate limiter
├── delisting_monitor.py   # Auto block delisted
├── position_command.py    # /position command
├── .env                  # API keys (SECRET)
├── .positions_sl_tp.json # Position cache
├── .recently_closed      # Closed cache (24h)
├── .posted_signals       # Posted cache
├── README.md             # Documentation
└── SKILL.md              # This file
```

## Commands

### Start Scanner
```bash
cd /root/.openclaw/workspace/neko-futures-trader
nohup python3 scanner-v8.py > scanner.log 2>&1 &
```

### Start Price Monitor
```bash
cd /root/.openclaw/workspace/neko-futures-trader
nohup python3 price-monitor.py > pm.log 2>&1 &
```

### Check Positions
```bash
python3 position_command.py
```

### Check Running
```bash
pgrep -f scanner-v8 && echo "Scanner OK"
pgrep -f price-monitor && echo "Monitor OK"
```

## Current Status (2026-03-19)

- 💰 Balance: ~$392
- 📊 Positions: 2/7 (KAVA, ARB)
- 🔍 Scanner: Running
- ⏱️ Monitor: Running
- 📱 Telegram: Connected

## Safety Features

1. **Cache Auto-Cleanup**: Removes entries >24h old
2. **Recently Closed**: Skips re-entry for 24h
3. **Delisting Monitor**: Auto-blocks bad tokens
4. **Error Handling**: Circuit breaker, rate limiter
5. **Recovery**: Auto-restart on failure

---
*Built by Neko Sentinel* 🐱🛡️
