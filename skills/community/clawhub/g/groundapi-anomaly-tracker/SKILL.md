---
name: groundapi-anomaly-tracker
description: Track A-share market anomalies — limit-up streaks, unusual volume, large capital flows — and drill into individual stocks for detailed analysis. Powered by GroundAPI MCP tools.
metadata:
  openclaw:
    requires:
      env: ["GROUNDAPI_KEY"]
    emoji: "🚨"
    homepage: "https://groundapi.net"
    primaryEnv: "GROUNDAPI_KEY"
---

# A 股异动追踪助手

当用户询问市场异动、放量股、连板股、资金异动，或类似以下表达时自动触发：
- "今天有什么异动"、"什么股票放量了"
- "连板股有哪些"、"涨停的是什么概念"
- "今天主力买了什么"

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

### Step 1 — 获取异动信号

`finance_market(scope="signals")` 获取：
- 连续涨停股（2板以上）
- 当日涨幅超 15% 的股票

### Step 2 — 获取涨停/炸板详情

`finance_market(scope="hot", limit=30)` 获取：
- 涨停池（含连板数、封板时间、封板资金、行业）
- 炸板池（曾涨停后打开）
- 连板梯队分层统计

### Step 3 — 对异动股深度挖掘

对用户感兴趣的或最显眼的异动股，获取资金和技术数据：
`finance_stock(symbol="XXXXXX", aspects="flow,technical,quote")`

关键看：
- `flow.cumulative_main_net` — 主力净流入金额
- `flow.consecutive_inflow_days` — 连续净流入天数
- `technical.signals` — 技术信号列表
- `quote.volume_ratio` — 量比

### Step 4 — 概念关联分析

对异动股查看所属概念：
`finance_stock(symbol="XXXXXX", aspects="profile")`

看 `profile.concepts` 和 `profile.concept_tags` 字段，找出共同概念。

如果多只异动股属于同一概念，说明该概念正在发酵，可以查成分股：
`finance_market(scope="sectors", sector="概念名")`

### Step 5 — 输出异动报告

```
## 市场异动追踪 — {YYYY-MM-DD}

### 异动概览
- 连续涨停：XX 只（最高 X 板）
- 涨幅超15%：XX 只
- 炸板：XX 只

### 连板梯队
| 板数 | 数量 | 股票 | 行业 |
|------|------|------|------|
| 5板 | 1 | XXX | AI |
| 3板 | 3 | XXX, XXX, XXX | 混合 |
| 2板 | 8 | ... | ... |

### 热点概念追踪
今日异动股主要集中在以下概念：
1. **AI 概念**（涨停 X 只）：XXX, XXX
2. **半导体**（涨停 X 只）：XXX

### 重点异动股分析

**XXX（代码）— 连续X板**
- 今日涨幅：+XX%
- 量比：X.X（放量/缩量）
- 封板资金：XX亿
- 近5日主力净流入：XX亿
- 技术信号：（列出 signals）
- 所属概念：XXX, XXX

以上数据基于公开信息，不构成投资建议。
```

## 注意事项

- 异动信号基于纯数学定义（涨幅/量比阈值），不含主观判断
- 概念关联分析是事实描述（"该股属于AI概念"），不是归因推测
- 某步数据获取失败时跳过并说明
- 输出语言跟随用户
