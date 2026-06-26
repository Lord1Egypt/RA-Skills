# Neko Futures Trader 🐱📈

Automated Binance Futures trading bot with professional risk management.

## Overview

This is a complete trading system for Binance Futures that:
- 🔍 **Auto Entry**: Scanner finds signals every 5 minutes
- 📊 **Dynamic ATR**: SL/TP adjusts based on volatility
- 🛡️ **Multi-TP**: 40% @ +10%, 30% @ +15%, 30% @ +20%
- 📈 **Auto Breakeven**: Moves SL to entry at +5%
- 🎯 **Auto Trailing**: TP trails at +10%
- 🔔 **Smart Notifications**: Telegram alerts
- ⏱️ **Auto TP/SL**: Price monitor checks every 1 second
- 🧹 **Auto Cache**: Cleans expired entries on startup
- 🚫 **Auto Delisting**: Blocks delisted tokens
- 🔄 **Auto Recovery**: Self-heals from errors

## What's New (v1.0.33)

- **14 Indicators**: RSI, MACD, VWAP, Bollinger, EMA, etc.
- **Dynamic ATR**: Volatility-based SL/TP
- **Multi-TP Strategy**: 1:2 Risk/Reward
- **Auto Features**: Cache cleanup, recovery, delisting
- **Self-Debugging**: Error handling, circuit breaker

---

## 🚀 Quick Start

```bash
# Terminal 1: Scanner (every 5 min)
cd /root/.openclaw/workspace/neko-futures-trader
nohup python3 scanner-v8.py > scanner.log 2>&1 &

# Terminal 2: Price Monitor (every 1 sec)
nohup python3 price-monitor.py > pm.log 2>&1 &

# Check status
python3 position_command.py
```

---

## ⚙️ Auto Features (All Active)

| Feature | Auto | Interval | Description |
|---------|------|----------|-------------|
| **Scanner** | ✅ | 5 min | Finds trading signals |
| **Price Monitor** | ✅ | 1 sec | Checks SL/TP/close |
| **Breakeven** | ✅ | On trigger | SL → Entry at +5% |
| **Trailing TP** | ✅ | On trigger | TP trails at +10% |
| **Cache Cleanup** | ✅ | On startup | Removes 24h+ old |
| **Delisting** | ✅ | On check | Blocks bad tokens |
| **Recovery** | ✅ | On error | Auto-restart |
| **Notify** | ✅ | On action | Telegram |

---

## 📊 Strategy Details

### Exit Plan (1:2 R/R)

| Level | Profit | Action |
|-------|--------|--------|
| STOP LOSS | -5% (LONG) / +5% (SHORT) | Auto close |
| TAKE PROFIT | +10% (LONG) / -10% (SHORT) | Auto close |

### Dynamic ATR System

| Volatility | ATR % | SL | TP |
|------------|-------|-----|-----|
| High | >3% | 2×ATR | 4×ATR |
| Normal | 1-3% | 1.5×ATR | 3×ATR |
| Low | <1% | 1×ATR | 2.5×ATR |

### Risk Protection

| Protection | Trigger | Action |
|------------|---------|--------|
| **Breakeven** | +5% profit | SL → Entry |
| **Trailing TP** | +10% profit | TP follows price |
| **Max Risk** | 1.5% per trade | Auto-reject |
| **Max Positions** | 7 open | Auto-skip |

---

## 📐 Signal Indicators (v1.0.33)

| # | Indicator | Condition | Score |
|---|-----------|-----------|-------|
| 1 | Volume Spike | >3x average | +2 |
| 2 | Price Change | >10% | +2 |
| 3 | Price Change | >5% | +1 |
| 4 | 1H Change | >3% | +1 |
| 5 | Breakout | HH/HL | +2 |
| 6 | Breakdown | LH/LL | +2 |
| 7 | OI Increase | >20% | +2 |
| 8 | Weekly Change | >20% | +3 |
| 9 | Pocket Pivot | Yes | +2 |
| 10 | RSI | <30 or >70 | +1 |
| 11 | Volume 5x+ | Extra spike | +2 |

**Signal Filters (v1.0.33):**
| Filter | Condition | Action |
|--------|-----------|--------|
| Whale Token | SHIB, DOGE, PEPE, WIF, etc. | REJECT |
| Volume | <2x average | REJECT |
| Price Change | <3% | REJECT |
| Timeframe | Divergence 1h vs 4h | REJECT |

**Minimum Score: 2 to trigger signal** (v1.0.33)

---

## ⚙️ Configuration (config.py)

```python
# === TRADING SETTINGS ===
MAX_POSITIONS = 7
AUTO_FILL_EMPTY_SLOTS = True
ENTRY_PERCENT = 6%
LEVERAGE = 10
MIN_GAIN = 0.5

# === RISK MANAGEMENT ===
MIN_PROFIT_BREAKEVEN = 5.0      # Move SL to entry at +5%
MIN_PROFIT_TRAILING_TP = 10.0  # Activate trailing at +10%
MAX_RISK_PERCENT = 1.5
MAX_MARGIN_PERCENT = 40

# === DYNAMIC ATR ===
ATR_HIGH_VOLATILITY = 3.0
ATR_MULTIPLIER_SL_HIGH = 2.0
ATR_MULTIPLIER_TP_HIGH = 4.0
ATR_MULTIPLIER_SL_NORMAL = 1.5
ATR_MULTIPLIER_TP_NORMAL = 3.0
ATR_MULTIPLIER_SL_LOW = 1.0
ATR_MULTIPLIER_TP_LOW = 2.5

# === MULTI-TP STRATEGY ===
TP1_PERCENT = 10.0  # Close 40% @ +10%
TP2_PERCENT = 15.0  # Close 30% @ +15%
TP3_PERCENT = 20.0  # Close 30% @ +20%

# === MONITOR ===
CHECK_INTERVAL = 1  # seconds
```

---

## 📁 File Structure

```
neko-futures-trader/
├── scanner-v8.py           # 🚀 Main scanner (auto entry)
├── price-monitor.py        # ⏱️ TP/SL executor (auto close)
├── config.py              # ⚙️ All settings
├── advanced_analysis.py    # 📊 Technical indicators
├── error_handling.py      # 🔄 Error recovery
├── delisting_monitor.py   # 🚫 Delisting safety
├── position_command.py    # 📋 /position command
├── .env                   # 🔑 API keys (SECRET)
├── .env.example           # 📝 Template
├── .positions_sl_tp.json  # 💾 Position cache
├── .recently_closed      # 🧹 Closed cache (24h)
├── .posted_signals       # 📤 Posted cache
├── README.md             # 📖 Documentation
└── SKILL.md              # 🤖 Agent skill
```

---

## 🔧 Commands

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

### Check Running Processes
```bash
pgrep -f scanner-v8 && echo "✅ Scanner OK"
pgrep -f price-monitor && echo "✅ Monitor OK"
```

---

## 🔑 Installation

### 1. Clone Repository
```bash
git clone https://github.com/lukmanc405/neko-futures-trader.git
cd neko-futures-trader
```

### 2. Install Dependencies
```bash
pip install requests hmac hashlib
```

### 3. Configure Environment
```bash
cp .env.example .env
nano .env
```

```env
BINANCE_API_KEY=your_key
BINANCE_SECRET=your_secret
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHANNEL=your_channel_id
BRAVE_API_KEY=your_brave_key
```

### 4. Get API Keys

**Binance:**
1. https://www.binance.com/en/futures
2. Account → API Management
3. Create API key (Enable Futures Trading)

**Telegram:**
1. @BotFather → /newbot
2. Get bot token

---

## 📱 Telegram Notifications

### 🚨 New Position
```
🟢 LONG SIGNAL 🟢

📈 BTCUSDT TECHNICAL ANALYSIS
📊 24h: +5.23%

🎯 RUNNER SCORE: 8/10 🚀

📈 TARGET:
• 
• 
• 
🛡 SL: $44,925 (-5%)

📊 DYNAMIC ATR:
• Volatility: 2.5%
• SL: 1.5×ATR | TP: 3×ATR

🛡 PROTECTION:
• Breakeven at: +5%
• Trailing TP: +10%
```

### 🔴 Position Closed
```
🔴 POSITION CLOSED

🔖 Symbol: ETHUSDT
📊 Type: TP2 HIT
💵 Entry: $2,500 → Exit: $2,625
💰 PnL: +$37.50 (+15%)
```

### 🛡 Breakeven
```
🛡 STOP LOSS MOVED TO BREAKEVEN

🔖 SOLUSDT
💵 Entry: $120.00
🛡 New SL: $120.00
💰 Profit: +5.2%
```

---

## 🎯 Trading Example

**Entry:** $100 at +10x leverage = $1,000 position

| Level | Price | Profit | Action |
|-------|-------|--------|--------|
| Entry | $100 | $0 | Open |
| SL | $95 | -$50 | Stop (-5%) |
| TP1 | $110 | +$100 | Close 40% |
| TP2 | $115 | +$75 | Close 30% |
| TP3 | $120 | +$50 | Close 30% |

**Risk/Reward: 1:2** ✅

---

## ⚠️ Safety Warning

1. Always use test account first
2. Never risk more than you can afford
3. Monitor positions regularly
4. Understand leveraged trading risks
5. Keep API keys secure - never commit to git

---

## 📊 Current Status (2026-03-19)

| Item | Value |
|------|-------|
| Balance | ~$392 |
| Positions | 2/7 |
| Scanner | ✅ Running |
| Monitor | ✅ Running |
| Version | v1.0.33 |

---

## 🆘 Troubleshooting

### Scanner not running?
```bash
ps aux | grep scanner-v8
nohup python3 scanner-v8.py &
```

### No signals?
- Check market conditions (need momentum)
- Signals require score ≥3

### API errors?
- Check Binance API permissions
- Verify Futures trading enabled

---

## 📞 Support

- GitHub: https://github.com/lukmanc405/neko-futures-trader

---

*Built by Neko Sentinel* 🐱🛡️

---


## 🌐 Live Dashboard

> **Replace `YOUR_VPS_IP` with your server IP.**

**URL:** `http://YOUR_VPS_IP:8080/neko-light.html`

### Design
- ⚫ Pure black background — bold minimalist
- 🔴 **SHORT** = red (#ff3b5c) | 🔵 **LONG** = blue (#3b8bff) | 🟡 **Accent** = yellow (#ffd23b)
- 🏆 Top 3 performers as ranked cards (gold/silver/bronze)
- 💰 Large balance display with live PnL
- 📊 Position table: Symbol, Dir, Entry, Now, SL, TP, ROI%
- ⬛ Left border accent on rows (blue/red per direction)
- 🙈 Eye button to show/hide balance
- 🔄 Refresh button with loading animation
- 👆 Hover effects + fade-up animations
- 📱 Responsive mobile layout

### Install for All Users
```bash
# Install the skill → dashboard auto-available
# Any OpenClaw user with this skill installed gets the dashboard
```

### Start Dashboard Server
```bash
cd /root/.openclaw/workspace
python3 dashboard_api.py &
# API + HTML server on port 8080
```

### Dashboard API
```
GET http://YOUR_VPS_IP:8080/api
Response: {"bal": float, "pnl": float, "pos": [{"s": symbol, "d": "LONG/SHORT", "e": entry, "m": mark, "u": unreal, "a": amount}]}
```

### SL/TP Strategy
**Primary:** ATR-based (adapts to token volatility, anti-fakeout)
**Fallback:** PRICE_TP/PRICE_SL when ATR% <1% or >10%

### ATR Config (config.py)
| Volatility | ATR% | SL Multiplier | TP Multiplier |
|------------|------|---------------|---------------|
| HIGH | >3% | 3.0× | 6.0× |
| NORMAL | 1-10% | 2.5× | 5.0× |
| LOW/EXTREME | <1% or >10% | Falls back to PRICE_TP/PRICE_SL |

### Key Config Values
```python
PRICE_TP = 10.0    # Fallback TP: +10%
PRICE_SL = 5.0      # Fallback SL: -5%
PRICE_FALLBACK_MAX_ATR = 10.0  # Use PRICE if ATR% > 10%
PRICE_FALLBACK_MIN_ATR = 1.0   # Use PRICE if ATR% < 1%
ATR_MULTIPLIER_SL_NORMAL = 2.5  # Wider for fakeout protection
ATR_MULTIPLIER_TP_NORMAL = 5.0
```
