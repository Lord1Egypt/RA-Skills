---
name: harena-brief
description: 输入金融标的代码（BTC、GOOGL）或新闻事件关键词（美联储降息、美伊战争），实时拉取行情和新闻，用 Claude 生成结构化投资分析简报。
version: 1.0.0
metadata:
  openclaw:
    emoji: "📊"
    homepage: https://github.com/allenzhang79/harena-brief
    os: [macos, linux, windows]
---

# Harena Brief

个人投资者的实时分析简报工具。输入金融标的或新闻事件，自动拉取实时数据，生成有观点、有数字的结构化分析简报。

## MCP Server

```
https://web-production-cf0c41.up.railway.app/mcp
```

传输协议：Streamable HTTP（无需本地安装，直接远程调用）

## 工具

### `get_brief`

为指定金融标的或新闻事件生成结构化分析简报（中文）。

**输入参数**

| 参数      | 类型       | 必填 | 说明                                                                 |
|---------|----------|------|----------------------------------------------------------------------|
| symbols | string[] | ✅    | 金融标的代码或事件关键词列表，最多 6 项                                               |

`symbols` 支持两类输入，可混合使用：

- **金融标的代码**：1–6 位字母/数字，如 `"BTC"`、`"ETH"`、`"GOOGL"`、`"NVDA"`、`"TSLA"`
- **事件关键词**：自然语言短语，如 `"美联储降息"`、`"美伊战争"`、`"特朗普关税"`

**输出格式**

每个标的/事件输出四段式简报（事件类额外包含「对持仓的影响」）：

```
## [标的代码] · [全名]

### 发生了什么
### 为什么对你重要
### 现在怎么看
短期（1-2周）：偏多/偏空/震荡，支撑 $X，压力 $X
中期（1-3月）：偏多/偏空/震荡，目标 $X
### 接下来盯住什么
① 催化剂 — 时间节点
② 催化剂 — 时间节点
③ 催化剂 — 时间节点
```

## 数据来源

| 标的类型 | 行情 | 新闻 |
|--------|------|------|
| 加密货币（BTC、ETH） | CoinGecko 实时 | CoinDesk RSS 实时 |
| 美股（GOOGL、NVDA 等） | Alpha Vantage 实时 | — |
| 事件关键词 | — | Google News RSS 实时 |

## 使用示例

**纯金融标的**
```json
{ "symbols": ["BTC", "GOOGL"] }
```

**纯事件**
```json
{ "symbols": ["美联储降息", "特朗普关税"] }
```

**混合输入**
```json
{ "symbols": ["BTC", "美伊战争"] }
```

## Privacy & Data

- **不存储查询数据**：服务不记录、不持久化任何用户输入的标的代码或事件关键词。
- **数据仅用于生成简报**：所有拉取的行情和新闻数据只在当次请求中用于生成简报，请求结束后即丢弃，不传递给任何第三方。
- **第三方数据源**（均为公开数据，无需用户授权）：
  - [CoinGecko](https://www.coingecko.com) — 加密货币实时行情
  - [CoinDesk RSS](https://www.coindesk.com) — 加密货币新闻
  - [Alpha Vantage](https://www.alphavantage.co) — 美股历史行情
  - [Google News RSS](https://news.google.com) — 事件关键词新闻

## 接入方式

在 Claude Desktop 或支持 MCP 的客户端中添加以下配置：

```json
{
  "mcpServers": {
    "harena-brief": {
      "url": "https://web-production-cf0c41.up.railway.app/mcp"
    }
  }
}
```
