# 🏛 Metals Desk OS v1.0.0

**Institutional Desk-Level Fully Automated Trading OS for XAU/USD and XAG/USD**

Architecture: Event-Driven, Risk-First, Multi-Engine AI Trading Desk

---

## 📁 File Structure

```
metals-desk-os/
├── index.js                    # Main entry point & orchestrator
├── package.json                # Dependencies
├── skill.json                  # OpenClaw skill manifest
├── manifest.json               # Runtime configuration
├── .env.example                # Environment template
│
├── core/                       # Trading engines
│   ├── bias-engine.js          # HTF/Intraday bias with conviction scoring
│   ├── structure-engine.js     # HH/HL/LH/LL, BOS, CHoCH, FVG, OB detection
│   ├── liquidity-engine.js     # Equal highs/lows, sweeps, pools
│   ├── execution-engine.js     # Trade signal generation & entry logic
│   ├── risk-engine.js          # Position sizing, drawdown, halts
│   ├── volatility-engine.js    # ATR, spike detection, regime classification
│   ├── macro-engine.js         # DXY, yields, risk sentiment
│   └── performance-engine.js   # Win rate, expectancy, Sharpe, drawdown
│
├── automation/                 # System automation
│   ├── event-bus.js            # Central nervous system (EventEmitter)
│   ├── price-feed.js           # Real-time price data from MT5/MetaAPI
│   ├── session-engine.js       # London/NY/Asian session tracking
│   ├── scheduler.js            # Cron-based daily tasks & reports
│   └── news-monitor.js         # Economic calendar & news blocking
│
├── broker/                     # Broker integration
│   ├── mt5-connector.js        # MetaAPI order execution
│   ├── risk-guard.js           # Active position monitoring & TP/SL management
│   └── order-manager.js        # High-level order lifecycle orchestration
│
├── dashboard/                  # Real-time dashboard
│   ├── websocket-feed.js       # WebSocket data broadcaster
│   ├── desk-dashboard.json     # Widget layout config
│   └── metrics.json            # Metrics template
│
├── alerts/                     # Notification system
│   ├── whatsapp-alert.js       # WhatsApp Business API alerts
│   ├── telegram-alert.js       # Telegram Bot alerts
│   └── risk-alert.js           # Centralized risk alert dispatcher
│
├── data/                       # Persistent state
│   ├── state.json              # System mode & connections
│   ├── trade-log.json          # Trade history
│   ├── performance.json        # Performance metrics
│   └── bias-memory.json        # Bias state persistence
│
└── prompts/                    # AI agent prompts
    ├── system.txt              # Main system prompt
    ├── intraday.txt            # Intraday protocol
    ├── swing.txt               # Swing protocol
    └── execution.txt           # Execution protocol
```

---

## 🚀 Step-by-Step Installation

### Step 1: Copy to OpenClaw

```bash
# From your local machine, copy to the claw1 server:
scp -r metals-desk-os/ root@claw1:~/.openclaw/agents/trader/agent/metals-desk-os/

# Or if building directly on claw1:
cd ~/.openclaw/agents/trader/agent/
mkdir -p metals-desk-os
# (paste files into the directory)
```

### Step 2: Install Dependencies

```bash
cd ~/.openclaw/agents/trader/agent/metals-desk-os
npm install
```

### Step 3: Configure Environment

Create a `.env` file in the skill root:

```bash
nano .env
```

Add the following (fill in your values):

```
# MetaAPI / MT5 Connection
METAAPI_TOKEN=your_metaapi_token_here
MT5_ACCOUNT_ID=your_mt5_account_id_here

# WhatsApp Business API (optional)
WHATSAPP_API_URL=https://graph.facebook.com/v18.0/YOUR_PHONE_NUMBER_ID/messages
WHATSAPP_TOKEN=your_whatsapp_token_here
WHATSAPP_PHONE=your_phone_number_with_country_code

# Telegram Bot (optional)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here

# News API (optional)
NEWS_API_KEY=

# AI Keys (optional)
OPENROUTER_API_KEY=
ANTHROPIC_API_KEY=
```

Where to get credentials:
- **METAAPI_TOKEN**: Sign up at https://metaapi.cloud, connect your Fusion Markets MT5
- **MT5_ACCOUNT_ID**: Your MetaAPI provisioned account ID
- **TELEGRAM_BOT_TOKEN**: Create via @BotFather on Telegram
- **TELEGRAM_CHAT_ID**: Get from @userinfobot
- **WHATSAPP_***: Configure via Meta Business API dashboard

### Step 4: Set System Mode

Edit `data/state.json`:
```json
{
  "mode": 1
}
```

Modes:
| Mode | Name | Behavior |
|------|------|----------|
| 1 | Advisory | Analysis & signals only (recommended to start) |
| 2 | Semi-Automated | Signals + auto TP/SL management |
| 3 | Fully-Automated | Full autonomous execution |
| 4 | Risk-Off | Monitoring only, no signals |

### Step 5: Start the System

```bash
# Advisory mode (start here)
npm run advisory

# Or with PM2 for persistent running:
pm2 start index.js --name metals-desk-os
pm2 save
```

---

## ⚙️ Pipeline Flow

```
PRICE FEED → SESSION ENGINE → STRUCTURE ENGINE → LIQUIDITY ENGINE →
MACRO ENGINE → BIAS ENGINE → VOLATILITY ENGINE → RISK ENGINE →
EXECUTION ENGINE → BROKER → PERFORMANCE ENGINE → DASHBOARD → ALERTS
```

Every component communicates through the **Event Bus**. All events are logged and can be monitored in real-time via the WebSocket dashboard.

---

## 🛡 Safety Rules (Non-Negotiable)

| Rule | Value |
|------|-------|
| Max risk per trade | 2% |
| Max daily exposure | 5% |
| Consecutive loss halt | 3 losses |
| Volatility spike | Reduce size 50% |
| Extreme volatility | Reduce size 75% |
| Spread anomaly | Block entry |
| News < 20 min | Block entry |
| Equity drawdown > 8% | Halt trading |
| API error | Cancel, do NOT retry |
| Broker disconnect | Close all positions |

---

## 📊 Dashboard

Connect any WebSocket client to `ws://localhost:3078` to receive real-time data.

Data includes:
- Live prices and spread
- HTF and intraday bias with conviction
- Active positions with live P&L
- Liquidity map (equal highs/lows, sweeps)
- Macro panel (DXY, yields, news countdown)
- Performance metrics (win rate, expectancy, drawdown, Sharpe)
- Risk status (halt state, daily P&L, exposure)
- Event log

---

## 🔔 Alert Format

### Trade Opened:
```
🔔 TRADE OPENED
Pair: XAUUSD
Direction: Long
Entry: 5024.50
SL: 5010.00
TP1: 5046.25
Risk: 1.5%
Session: London
Conviction: 82/100
```

### Risk Halt:
```
🛑 RISK HALT ACTIVATED
Reason: 3 consecutive losses
Trading paused for session
```

---

## 🧪 Testing

Start in **Mode 1 (Advisory)** first. The system will run the full analysis pipeline with simulated prices and emit signals without executing trades. Monitor the console output and WebSocket feed to verify:

1. Price feed is running
2. Structure detection is working
3. Liquidity pools are being identified
4. Bias engine produces reasonable conviction scores
5. Execution engine generates valid signals
6. Risk engine properly validates/rejects

Once confident, move to **Mode 2 (Semi-Auto)** to test TP/SL management, then **Mode 3 (Full-Auto)** for live execution.

---

## 🔧 PM2 Production Setup

```bash
# Install PM2 if not already
npm install -g pm2

# Start with PM2
pm2 start index.js --name metals-desk-os --cwd ~/.openclaw/agents/trader/agent/metals-desk-os

# Auto-restart on crash
pm2 save
pm2 startup

# View logs
pm2 logs metals-desk-os

# Monitor
pm2 monit
```

---

*Built for Carlos's OpenClaw Metals Trading Desk*
*Risk-First • Session-Aware • Macro-Aware • Institutional-Grade*
