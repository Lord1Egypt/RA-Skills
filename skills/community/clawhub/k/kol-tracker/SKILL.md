---
name: kol-tracker
version: 1.0.0
description: |
  Track crypto KOL and smart money wallets.
  Get alerts when they buy/sell tokens.
  Follow the smart money!
metadata:
  openclaw:
    emoji: 🐋
    requires:
      env:
        - TELEGRAM_BOT_TOKEN
        - ETHERSCAN_API_KEY
      bins:
        - python3
        - curl
  pricing:
    type: freemium
    free:
      description: "追踪 3 个 KOL，延迟 1 小时"
      limits:
        wallets: 3
        delay: "1 hour"
    pro:
      price: 1.99
      currency: USD
      period: monthly
      description: "追踪 20 个 KOL，实时推送"
      features:
        - "追踪 20 个 KOL 钱包"
        - "实时交易推送"
        - "持仓分析"
        - 盈亏统计"
        - "复制交易提醒"
        - "历史表现回顾"
---

# 🐋 KOL Tracker - KOL 钱包追踪

Track crypto influencers and smart money wallets.

## Features

- 🔍 Track KOL wallet activities
- 📊 Portfolio analysis
- 💰 P&L tracking
- ⚡ Real-time alerts
- 📈 Performance history

## Usage

```bash
# Add KOL wallet
/kol-tracker add <address> --name "Vitalik"

# View recent trades
/kol-tracker trades <address>

# Check portfolio
/kol-tracker portfolio <address>
```

## Pre-loaded KOLs

- Vitalik Buterin (Ethereum founder)
- CZ (Binance founder)
- SBF (FTX - caution!)
- And more smart money wallets...

