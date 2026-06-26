---
name: groundapi-stock-screener
description: Screen A-share stocks by PE, PB, market cap, dividend yield, industry, concept — with preset filters, macro context (gold/forex), and deep-dive into results — powered by GroundAPI MCP tools.
metadata:
  openclaw:
    requires:
      env: ["GROUNDAPI_KEY"]
    emoji: "🔍"
    homepage: "https://groundapi.net"
    primaryEnv: "GROUNDAPI_KEY"
---

# A 股选股助手

当用户要求选股、筛选、或类似以下表达时自动触发：
- "帮我找几只低估值的股票"、"高分红的有哪些"
- "PE 低于 10 的银行股"
- "市值 100 亿以下的科技股"
- "AI 概念里哪些股票不错"

## 前置条件

```json
{
  "mcpServers": {
    "groundapi": {
      "url": "https://mcp.groundapi.net/mcp",
      "headers": {
        "X-API-Key": "sk_gapi_xxxxx"
      }
    }
  }
}
```

## 执行流程

### Step 1 — 理解用户需求，映射为筛选参数

| 用户说 | 映射为 |
|-------|-------|
| "低估值" | `pe_max=15` |
| "高分红" | `min_dividend_yield=3, sort_by="dividend_yield"` |
| "银行股" | `industry="银行"` |
| "AI概念" | `concept="AI"` |
| "小盘股" | `max_market_cap=10000000000` |
| "大盘蓝筹" | `min_market_cap=50000000000, pe_max=20` |

也可以用**预置组合**快速筛选：
- `filter_preset="low_pe_high_div"` → PE<15 且 股息率>3%
- `filter_preset="small_cap_growth"` → 市值<100亿
- `filter_preset="large_cap_stable"` → 市值>500亿 且 PE<20

### Step 2 — 执行筛选

`finance_screen(industry="银行", pe_max=10, sort_by="pe", order="asc", limit=20)`

### Step 3 — 宏观环境参考

并行获取宏观数据，为选股提供大环境背景：
- `life_calendar()` → 确认是否交易日
- `finance_gold_price()` → 金价走势（避险情绪参考）
- `finance_exchange_rate(from_currency="USD", to_currency="CNY")` → 汇率（外贸/外资敏感行业参考）

### Step 4 — 对优选结果深度挖掘

从筛选结果中取 Top 3-5 只，调用 summary 获取多维度数据：
`finance_stock(symbol="601398,601939,600036", aspects="overview")`

或逐个深度分析：
`finance_stock(symbol="601398", aspects="summary")`

### Step 5 — 输出选股报告

```
## 选股结果 — {筛选条件描述}

### 宏观环境
- 日期：{YYYY-MM-DD}（{交易日/非交易日}）
- 黄金：¥XXX/克 | 美元兑人民币：X.XXXX

### 筛选条件
- 行业：银行
- PE 上限：10
- 排序：PE 从低到高

### 结果（共XX只）
| 排名 | 代码 | 名称 | PE | PB | 股息率 | 市值(亿) | 今日涨跌 |
|------|------|------|-----|-----|--------|---------|---------|
| 1 | 601398 | 工商银行 | 5.2 | 0.5 | 6.1% | 18000 | +0.3% |
| 2 | ... | ... | ... | ... | ... | ... | ... |

### Top 3 快速概览

**1. 工商银行（601398）**
- 主力资金：近5日净流入XX亿
- 技术面：均线多头排列，MACD金叉
- 股东：户数连续3期减少（筹码集中）

**2. ...**

以上数据基于公开信息，不构成投资建议。
```

## 注意事项

- `finance_screen` 依赖数据库快照数据，非实时交易数据
- 筛选条件可自由组合，所有参数均可选
- PE 为负的股票默认被过滤（亏损企业）
- 输出语言跟随用户
