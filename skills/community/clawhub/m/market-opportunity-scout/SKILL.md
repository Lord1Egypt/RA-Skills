---
name: market-opportunity-scout
description: 市场机会侦察兵 - 自动监控 A/H 股市场异动、财经新闻、热点板块，生成投资机会简报。适合投资者、交易员、金融从业者。
version: 1.0.0
author: yoriko233
license: MIT
tags: [finance, stock, market, monitor, report, investment]
pricing:
  model: paid
  price: 9.9
  currency: CNY
  billing: monthly
---

# Market Opportunity Scout - 市场机会侦察兵

自动监控资本市场机会，生成结构化投资简报。

## 功能

- 📈 **异动监控**: 实时监控 A/H 股涨跌幅、成交量异常
- 📰 **新闻聚合**: 抓取财经新闻、公司公告、市场传闻
- 🔥 **热点追踪**: 识别热门板块、概念题材、资金流向
- 📊 **数据简报**: 生成结构化报告（Markdown/文本）
- ⏰ **定时推送**: 支持 cron 定时自动运行

## 安装

```bash
clawhub install market-opportunity-scout
```

## 使用

### 快速启动

```bash
# 生成今日市场简报
market-opportunity-scout --mode daily

# 监控特定股票
market-opportunity-scout --stocks 600519,00700,09988

# 监控特定板块
market-opportunity-scout --sectors 白酒，新能源，AI
```

### Cron 定时任务

```bash
# 每个交易日早上 8 点生成简报
0 8 * * 1-5 market-opportunity-scout --mode daily --output /path/to/report.md
```

### 输出格式

```markdown
# 市场机会简报 - 2026-03-25

## 📊 大盘概览
- 上证指数：XXXX (+X.XX%)
- 恒生指数：XXXX (+X.XX%)

## 🔥 热门板块
1. 白酒板块 (+3.2%)
2. 新能源 (+2.8%)

## ⚡ 异动个股
- 贵州茅台：+5.2% (放量突破)
- 腾讯控股：+3.8% (北向资金流入)

## 📰 重要新闻
1. [新闻标题 1] - 来源
2. [新闻标题 2] - 来源

## 💡 机会提示
- XXXX 板块连续 3 日资金净流入
- XXXX 个股突破 60 日均线
```

## 配置

可选配置文件 `~/.market-scout/config.json`:

```json
{
  "stocks": ["600519", "00700", "09988"],
  "sectors": ["白酒", "新能源", "科技"],
  "threshold": {
    "priceChange": 3.0,
    "volumeChange": 50.0
  },
  "output": {
    "format": "markdown",
    "path": "/tmp/market-report.md"
  }
}
```

## API 说明

本技能使用以下数据源（无需 API Key）：

- A 股/港股数据：akshare (开源财经数据接口)
- 财经新闻：公开 RSS/爬虫

## 注意事项

- ⚠️ 数据延迟约 15 分钟，不构成投资建议
- ⚠️ 仅供研究参考，投资需谨慎
- ⚠️ 首次运行需安装依赖：`pip install akshare pandas`

## 更新日志

### v1.0.0 (2026-03-25)
- 初始版本
- 支持 A/H 股监控
- 支持财经新闻聚合
- 支持定时任务

## 作者

yoriko233

## 支持

Issue: https://github.com/yoriko233/market-opportunity-scout/issues
