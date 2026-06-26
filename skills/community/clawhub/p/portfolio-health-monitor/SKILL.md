---
name: Portfolio Health Check
description: "Full portfolio monitoring across crypto, US stocks, and Chinese A-shares. P&L tracking, drawdown alerts, rebalancing signals. Supports OKX, Yahoo Finance, Sina."
emoji: 📊
color: blue
---

# Portfolio Health Check

Monitors your entire trading portfolio across multiple asset classes with automatic P&L calculation, risk alerts, and rebalancing recommendations.

## Features

- **Multi-Asset Coverage**: Crypto (OKX), US stocks (Yahoo), A-shares (Sina)
- **P&L Tracking**: Realized + unrealized per position and total
- **Stop-Loss Monitor**: Triggers when loss >25%
- **Take-Profit Alert**: Triggers when profit >30% + RSI >75
- **Rebalancing Signals**: Position size drift detection

## Alert Triggers

| Condition | Action |
|-----------|--------|
| Profit >30% + RSI >75 + pullback >5% | Take-profit alert |
| Loss >25% | Stop-loss alert |
| RSI >80 + profit >20% | Reduce position |
| Pullback >10% + RSI <35 | Add position |
| Any position >30% of portfolio | Rebalance warning |

## Exchange Support

- OKX (crypto perpetuals)
- Yahoo Finance (US stocks)
- Sina Finance (Chinese A-shares)

## Premium Version (Coming Soon)
- Real-time push notifications (Telegram/WeChat)
- Weekly performance report
- Custom alert thresholds
- Multi-portfolio management

---

*Know your positions. Control your risk.*
