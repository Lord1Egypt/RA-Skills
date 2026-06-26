# Polymarket API 参考

## 概述

三个公开 API 提供市场数据访问。只读操作无需认证。

## 1. Gamma API（市场发现）

**基础 URL：** `https://gamma-api.polymarket.com`

### GET /markets

列出市场，支持筛选和排序。

| 参数 | 类型 | 描述 |
|------|------|------|
| `active` | bool | 按活跃状态筛选（`true` = 可交易） |
| `closed` | bool | 按关闭状态筛选 |
| `order` | string | 排序方式：`volume_24hr`、`liquidity`、`start_date`、`end_date`、`competitive` |
| `ascending` | bool | 排序方向（默认：`false`） |
| `limit` | int | 每页结果数（最大 100） |
| `offset` | int | 分页偏移 |

### GET /markets/{id}

按 ID 获取单个市场。

### 关键响应字段

```json
{
  "id": "string",
  "slug": "url-friendly-id",
  "question": "X 会在 Y 之前发生吗？",
  "description": "详细结算条件...",
  "outcomes": "[\"Yes\",\"No\"]",
  "outcomePrices": "[\"0.35\",\"0.65\"]",
  "clobTokenIds": "[\"token_yes\",\"token_no\"]",
  "conditionId": "0x...",
  "active": true,
  "closed": false,
  "enableOrderBook": true,
  "liquidityNum": 50000.0,
  "volume24hr": 12000.0,
  "volumeNum": 500000.0,
  "bestBid": 0.34,
  "bestAsk": 0.36,
  "spread": 0.02,
  "lastTradePrice": 0.35,
  "oneDayPriceChange": -0.05,
  "oneWeekPriceChange": 0.10,
  "endDate": "2026-06-01T00:00:00Z"
}
```

注意：`outcomes`、`outcomePrices` 和 `clobTokenIds` 可能是 JSON 编码的字符串；需要相应解析。

### GET /events

列出事件。每个事件包含嵌套的 `markets` 数组。**推荐的市场发现端点**，因为它提供构建正确 URL 所需的事件级 slug。

| 参数 | 类型 | 描述 |
|------|------|------|
| `active` | bool | 按活跃状态筛选（`true` = 可交易） |
| `closed` | bool | 按关闭状态筛选 |
| `order` | string | 排序方式：`volume24hr`、`liquidity`、`startDate`、`endDate` |
| `ascending` | bool | 排序方向（默认：`false`） |
| `limit` | int | 每页结果数（最大 **50**，低于 /markets 的 100） |
| `offset` | int | 分页偏移 |
| `slug` | string | 按事件 slug 筛选（精确匹配） |

**响应结构：**

```json
[
  {
    "id": "event-id",
    "slug": "event-slug-for-url",
    "title": "事件标题",
    "description": "包含结算条件的事件描述",
    "markets": [
      {
        "id": "market-id",
        "slug": "market-slug",
        "question": "具体问题？",
        "outcomes": "[\"Yes\",\"No\"]",
        "outcomePrices": "[\"0.35\",\"0.65\"]",
        "clobTokenIds": "[\"token_yes\",\"token_no\"]",
        "liquidityNum": 50000.0,
        "volume24hr": 12000.0,
        "enableOrderBook": true,
        "endDate": "2026-06-01T00:00:00Z"
      }
    ]
  }
]
```

### 事件 Slug vs 市场 Slug

Polymarket 页面 URL 使用**事件级 slug**，而非市场级 slug：

- 正确：`https://polymarket.com/event/will-trump-win-2028`（事件 slug）
- 错误：`https://polymarket.com/event/will-trump-win-republican-primary-2028`（市场 slug — 返回 404）

### GET /public-search

按关键词搜索事件和市场。

| 参数 | 类型 | 描述 |
|------|------|------|
| `query` | string | 搜索关键词 |

## 2. CLOB API（价格和订单簿）

**基础 URL：** `https://clob.polymarket.com`

### GET /book?token_id={token_id}

获取某 token 的完整订单簿。

### GET /price?token_id={token_id}&side={BUY|SELL}

获取特定方向的参考价格。

### GET /midpoint?token_id={token_id}

获取中间价。

### GET /prices-history?token_id={token_id}&interval={interval}&fidelity={fidelity}

历史价格数据。间隔：`1d`、`1w`、`1m`、`3m`、`all`。

## 构建市场 URL

市场页面：`https://polymarket.com/event/{event_slug}`

**必须使用事件级 slug**（来自 `/events` 端点顶层 `slug` 字段），而非市场级 slug。使用市场 slug 会导致 404 错误。
