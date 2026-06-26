---
name: newspulse
description: 📰 NewsPulse - 加密货币新闻聚合，重要事件实时推送
version: 0.1.0
author: gztanht
license: MIT
tags: [news, crypto, bitcoin, ethereum, media, alert]
pricing:
  free_tier: 5 queries/day
  sponsorship: 0.5 USDT or 0.5 USDC for unlimited
  note: "Feel free to sponsor more if you find it useful!"
wallet:
  usdt_erc20: "0x33f943e71c7b7c4e88802a68e62cca91dab65ad9"
  usdc_erc20: "0xcb5173e3f5c2e32265fbbcaec8d26d49bf290e44"
metadata:
  clawdbot:
    emoji: 📰
    requires:
      bins: [npm, node]
---

# 📰 NewsPulse - 加密货币新闻聚合

**Stay Ahead of the Market** - 不错过任何重要事件！

## Overview

NewsPulse 聚合全球主流加密货币新闻源（CoinDesk, Cointelegraph, TheBlock, Decrypt 等），提供实时新闻推送、重要事件提醒、社交媒体情绪分析等功能。

## Features

- 📰 **新闻聚合** - 10+ 主流加密媒体实时抓取
- 🔔 **重要事件** - 监管政策、交易所上线、黑客事件等即时推送
- 📊 **情绪分析** - 新闻情绪评分（正面/中性/负面）
- 🏷️ **分类筛选** - 按币种/主题/重要性筛选
- ⏰ **时间线** - 24h/7d/30d 新闻回顾
- 🌐 **多语言** - 英文/中文新闻支持

## Installation

```bash
npx @gztanht/newspulse
```

## Usage

### 查看最新新闻

```bash
# 最新 10 条新闻
node scripts/news.mjs --limit 10

# 比特币相关新闻
node scripts/news.mjs --tag btc

# 重大事件（高重要性）
node scripts_news.mjs --importance high

# 负面新闻预警
node scripts/news.mjs --sentiment negative
```

### 设置新闻推送

```bash
# BTC 相关新闻推送
node scripts/subscribe.mjs --tag btc

# 监管政策新闻
node scripts/subscribe.mjs --tag regulation

# 查看已订阅
node scripts/subscribe.mjs --list
```

### 情绪分析

```bash
# 查看 24h 新闻情绪
node scripts/sentiment.mjs --period 24h

# 特定币种情绪
node scripts/sentiment.mjs --tag eth
```

## News Sources

- CoinDesk
- Cointelegraph
- The Block
- Decrypt
- Bitcoin Magazine
- Ethereum World News
- CryptoSlate
- U.Today
- NewsBTC
- AMBCrypto

## Configuration

编辑 `config/sources.json` 自定义新闻源：

```json
{
  "sources": [
    {"name": "CoinDesk", "url": "https://coindesk.com/feed", "enabled": true},
    {"name": "Cointelegraph", "url": "https://cointelegraph.com/rss", "enabled": true}
  ]
}
```

## API Reference

- **RSS Feed 抓取** - 各新闻源官方 RSS
- **更新频率** - 每 5-15 分钟
- **缓存** - 本地缓存 1 小时

## Support

- 📧 Email: Support@NewsPulse.shark
- 💬 Telegram: @NewsPulseBot
- 🦈 赞助：USDT (ERC20): `0x33f943e71c7b7c4e88802a68e62cca91dab65ad9`

## License

MIT © 2026 gztanht
