---
name: kamino-positions-monitor
description: Monitor Solana wallets with Kamino Lend positions for liquidation risk. Generates reports with collateral, debt, health metrics, liquidation prices, and actionable recommendations. Use when the user asks about Kamino positions, Solana lending risk, liquidation monitoring, or DeFi fund health.
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "homepage": "https://github.com/csacanam/kamino-positions-monitor",
        "requires": { "bins": ["node"] },
      },
  }
---

# Kamino Positions Monitor

Monitors Solana wallets with Kamino Lend positions. Outputs a liquidation-focused report with health metrics, SOL liquidation price, and how much to deposit or repay to reach 60% margin.

## When to Use

- User asks about Kamino positions, Solana lending, or liquidation risk
- User wants to check fund health or get actionable recommendations
- User mentions "Kamino", "Solana funds", "liquidation", or "DeFi monitoring"

## Prerequisites

The [kamino-positions-monitor](https://github.com/csacanam/kamino-positions-monitor) project must be installed and configured. **User must provide**: Solana wallet addresses in `wallets.json`. RPC is optional—if `SOLANA_RPC_URL` is not set, the public Solana mainnet RPC is used (rate-limited; for heavy use, set a dedicated RPC in `.env`).

1. Clone and install:
   ```bash
   git clone https://github.com/csacanam/kamino-positions-monitor
   cd kamino-positions-monitor && npm install
   ```
2. Configure: copy `wallets.json.example` → `wallets.json`, add wallet addresses. Optional in `.env`: `SOLANA_RPC_URL`. When run via OpenClaw, the report is delivered to the user's chat automatically. For direct runs (cron, terminal), optional `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` send the report to a Telegram chat.
3. Project path: directory containing `kamino_monitor.js`. Set `KAMINO_MONITOR_PATH` or use `.` if the workspace is the project.

## Run the Monitor

```bash
cd "${KAMINO_MONITOR_PATH:-.}" && node kamino_monitor.js wallets.json
```

## Output

Stdout gets the full report. Via OpenClaw, the agent delivers it to the user's chat. When run directly, optional `TELEGRAM_*` in `.env` also pushes to a Telegram chat (HTML formatting, Jupiter links).

Example (abbreviated):

```
📊 Funds Report | 02/22/26, 11:57 PM

📋 GLOBAL SUMMARY
   SOL price: $77.33
   Kamino: Coll $30881 | Debt $10521 | Net $20360
   To bring all to Health 60%: deposit ~$4583 or repay ~$1375
   P_liq of fund most at risk: $46.39 · SOL must drop 40% to reach
   If SOL drops:
     10% (SOL ~$70): deposit $7646 total (+$3047) or repay $2294 total (+$914)
     ...

👛 Fund 1 (Ab12…xyZ9)
   Spot: SOL 0.32 | USDC 0 | USDT 0 → $24.85
   Kamino: Coll $421 | Debt $189 | Net $232 🟢
   LTV 45% | Health 40% | Liq SOL: $46.39 (now $77.33)
   📌 For Health 60%: deposit ~$210 (~2.7 SOL) or repay ~$63
   🔗 https://jup.ag/portfolio/[wallet_address]
```

## Interpreting Results

- **🟢🟡🟠🔴**: Risk level (green = healthy, red = near liquidation)
- **⚪**: No debt or no Kamino position
- **Health ratio** 1.0 = at liquidation edge; >1 = safe
- **Health %** 0% = liquidation; 100% = max margin

See [reference.md](reference.md) for formula details.
