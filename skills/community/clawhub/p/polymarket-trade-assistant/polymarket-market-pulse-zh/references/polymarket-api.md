# Polymarket API 参考

## 概述

三个公共 API 提供市场数据访问，只读操作无需认证。

## 1. Gamma API（市场发现）

**基础 URL：** `https://gamma-api.polymarket.com`

### GET /markets

获取市场列表，支持过滤和排序。

| 参数 | 类型 | 说明 |
|------|------|------|
| `active` | bool | 按活跃状态过滤（`true` = 可交易） |
| `closed` | bool | 按关闭状态过滤 |
| `order` | string | 排序字段：`volume_24hr`、`liquidity`、`start_date`、`end_date`、`competitive` |
| `ascending` | bool | 排序方向（默认：`false` 降序） |
| `limit` | int | 每页条数（最大 100） |
| `offset` | int | 分页偏移量 |

### GET /markets/{id}

按 ID 获取单个市场详情。

### 关键响应字段

```json
{
  "id": "string",
  "slug": "url-friendly-id",
  "question": "X 事件会在 Y 之前发生吗？",
  "description": "详细的结算标准...",
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

注意：`outcomes`、`outcomePrices`、`clobTokenIds` 可能是 JSON 编码的字符串，需要额外解析。

### GET /events

获取事件列表。每个事件包含嵌套的 `markets` 数组。**推荐使用此端点**进行市场发现，因为它同时提供事件级 slug（用于构造正确的市场链接）。

| 参数 | 类型 | 说明 |
|------|------|------|
| `active` | bool | 按活跃状态过滤（`true` = 可交易） |
| `closed` | bool | 按关闭状态过滤 |
| `order` | string | 排序字段：`volume24hr`、`liquidity`、`startDate`、`endDate` |
| `ascending` | bool | 排序方向（默认：`false` 降序） |
| `limit` | int | 每页条数（最大 **50**，注意比 /markets 的 100 更小） |
| `offset` | int | 分页偏移量 |

**响应结构：**

```json
[
  {
    "id": "event-id",
    "slug": "event-slug-for-url",
    "title": "事件标题",
    "description": "事件描述",
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

注意：一个事件可能包含 1 个或多个市场。嵌套的 markets 数组中的字段与 `/markets` 端点返回的字段相同。

### 事件 Slug vs 市场 Slug

Polymarket 的页面 URL 使用**事件级 slug**，而非市场级 slug：

- 正确：`https://polymarket.com/event/will-trump-win-2028`（事件 slug）
- 错误：`https://polymarket.com/event/will-trump-win-republican-primary-2028`（市场 slug，会 404）

通过 `/events` 端点获取数据时，事件 slug 在顶层对象的 `slug` 字段中，市场 slug 在嵌套 `markets[].slug` 中。构造链接时务必使用事件级 slug。

### GET /public-search

按关键词搜索事件和市场。参数：`query`（搜索关键词）。

### GET /comments

获取事件的用户评论。无需认证。

| 参数 | 类型 | 说明 |
|------|------|------|
| `parent_entity_type` | string | **必填**，固定值 `Event`（区分大小写） |
| `parent_entity_id` | int | **必填**，事件的数字 ID（来自 `/events` 端点的 `id` 字段） |
| `limit` | int | 每页条数（默认 20） |
| `order` | string | 排序字段，通常用 `createdAt` |
| `ascending` | bool | 排序方向（`false` = 最新在前） |

**注意：** `parent_entity_type` 仅支持 `Event`，其他值（如 `Market`、`market`）会返回 validation error。

**响应结构：**

```json
[
  {
    "id": "2478937",
    "body": "评论正文...",
    "parentEntityType": "Event",
    "parentEntityID": 90177,
    "parentCommentID": "2478065",
    "userAddress": "0x...",
    "createdAt": "2026-03-01T23:56:59.990224Z",
    "updatedAt": "2026-03-01T23:57:10.514602Z",
    "profile": {
      "name": "username",
      "pseudonym": "Fallback-Name",
      "displayUsernamePublic": true
    },
    "reportCount": 0,
    "reactionCount": 3,
    "reactions": [
      {"reactionType": "HEART", "userAddress": "0x..."}
    ]
  }
]
```

关键字段：
- `body`：评论正文
- `profile.name`：用户名（如未公开则用 `pseudonym`）
- `parentCommentID`：如非空，表示这是一条回复
- `reactionCount`：点赞/反应总数
- 部分事件可能没有评论，返回空数组 `[]`

## 2. CLOB API（价格与订单簿）

**基础 URL：** `https://clob.polymarket.com`

### GET /book?token_id={token_id}

获取某代币的完整订单簿。

```json
{
  "market": "condition_id",
  "asset_id": "token_id",
  "bids": [{"price": "0.34", "size": "1500.0"}, ...],
  "asks": [{"price": "0.36", "size": "2000.0"}, ...],
  "tick_size": "0.01",
  "min_order_size": "5"
}
```

买单（bids）按价格降序排列；卖单（asks）按价格升序排列。

### GET /price?token_id={token_id}&side={BUY|SELL}

获取特定方向的指示性价格。

### GET /midpoint?token_id={token_id}

获取中间价（最佳买卖价均值）。

### GET /spread?token_id={token_id}

获取当前买卖价差。

### GET /prices-history?token_id={token_id}&interval={interval}&fidelity={fidelity}

历史价格数据。interval：`1d`、`1w`、`1m`、`3m`、`all`。fidelity：数据点数量。

## 3. Data API（分析数据）

**基础 URL：** `https://data-api.polymarket.com`

### GET /trades

获取最近交易记录。

| 参数 | 类型 | 说明 |
|------|------|------|
| `market` | string[] | Condition ID 数组 |
| `limit` | int | 每页条数（最大 10000） |
| `side` | string | `BUY` 或 `SELL` |

### GET /oi?market={condition_id}

获取市场的未平仓合约量。

### GET /holders?market={condition_id}

获取市场的主要持仓者。

## 构造市场链接

市场页面：`https://polymarket.com/event/{event_slug}`

**必须使用事件级 slug**（来自 `/events` 端点的顶层 `slug` 字段），而非市场级 slug。使用市场 slug 会导致 404 错误。

如果只有市场数据（通过 `/markets` 端点获取），其 `slug` 字段是市场级别的，不适合直接用于 URL 构造。建议改用 `/events` 端点获取数据。
