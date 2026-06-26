---
name: news-sentiment
version: 1.0.0
description: |
  Analyze crypto news sentiment (bullish/bearish).
  Scan Twitter, news sites, and social media.
  Get sentiment scores and trading signals.
metadata:
  openclaw:
    emoji: 📰
    requires:
      env:
        - DASHSCOPE_API_KEY
      bins:
        - python3
        - curl
  pricing:
    type: freemium
    free:
      description: "每日 10 次查询，基础情绪分析"
      limits:
        dailyQueries: 10
    pro:
      price: 1.99
      currency: USD
      period: monthly
      description: "无限查询，实时推送，API 访问"
      features:
        - "无限查询"
        - "实时推送告警"
        - "多币种对比"
        - "历史情绪图表"
        - "API 访问权限"
        - "定制阈值告警"
---

# 📰 News Sentiment Analyzer - 新闻情绪分析

Analyze crypto news and social media sentiment for trading signals.

## Features

- 📊 Sentiment scoring (bullish/bearish/neutral)
- 🔍 Multi-source analysis (Twitter, news, Reddit)
- 📈 Trading signal generation
- 🎯 Coin-specific sentiment
- ⚡ Real-time updates

## Usage

```bash
# Analyze sentiment for a coin
/news-sentiment analyze BTC

# Get market sentiment
/news-sentiment market

# Set alerts
/news-sentiment alert --threshold 0.7
```

## Sentiment Scale

- **0.7 - 1.0**: Very Bullish 🚀
- **0.3 - 0.7**: Neutral ➡️
- **0.0 - 0.3**: Very Bearish 📉

## API Sources

- Twitter API (6551.io)
- News APIs
- LLM analysis (Dashscope)

