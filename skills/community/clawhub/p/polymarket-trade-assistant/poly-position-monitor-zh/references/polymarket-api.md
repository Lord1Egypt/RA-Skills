# Polymarket API 参考（持仓监控）

## 概述

使用四个 API 接口。持仓、活动和成交为公开接口（无需认证）。挂单查询需要 CLOB L2 认证。

## 1. Data API — 持仓与活动

**基础 URL：** `https://data-api.polymarket.com`

### GET /positions

获取钱包地址的当前持仓。

| 参数 | 类型 | 说明 |
|------|------|------|
| `user` | string | **必填。** 钱包地址（0x 前缀） |
| `market` | string | Condition ID 过滤（与 eventId 互斥） |
| `eventId` | string | 事件 ID 过滤 |
| `sizeThreshold` | number | 最小代币数量（默认 1） |
| `limit` | int | 0–500（默认 100） |
| `offset` | int | 分页偏移量 |
| `sortBy` | string | CURRENT, INITIAL, TOKENS, CASHPNL, PERCENTPNL, TITLE, PRICE, AVGPRICE |
| `sortDirection` | string | ASC 或 DESC |

**响应字段：** conditionId, assetId, title, outcome, size, avgPrice, currentValue, initialValue, cashPnl, percentPnl, curPrice, eventSlug, endDate, redeemable, mergeable。

### GET /activity

用户的链上活动流。

| 参数 | 类型 | 说明 |
|------|------|------|
| `user` | string | **必填。** 钱包或代理地址 |
| `type` | string | TRADE, REDEEM, MERGE, SPLIT, REWARD, CONVERSION |
| `market` | string | Condition ID 过滤 |
| `eventId` | string | 事件 ID 过滤 |
| `start` | number | Unix 时间戳下限 |
| `end` | number | Unix 时间戳上限 |
| `side` | string | BUY 或 SELL |
| `limit` | int | 0–500（默认 100） |
| `offset` | int | 分页偏移量 |
| `sortBy` | string | TIMESTAMP, TOKENS, CASH |

### GET /trades

跨市场的历史成交记录。

| 参数 | 类型 | 说明 |
|------|------|------|
| `user` | string | 按参与者地址过滤 |
| `market` | string[] | Condition ID |
| `side` | string | BUY 或 SELL |
| `limit` | int | 0–10000（默认 100） |
| `offset` | int | 分页偏移量 |

### GET /holders

市场的主要持仓者。

| 参数 | 类型 | 说明 |
|------|------|------|
| `market` | string | Condition ID |

## 2. CLOB API — 价格与挂单

**基础 URL：** `https://clob.polymarket.com`

### GET /prices-history

历史价格数据。

| 参数 | 类型 | 说明 |
|------|------|------|
| `market` | string | **必填。** Token ID (asset_id) |
| `interval` | string | max, all, 1m, 1w, 1d, 6h, 1h |
| `fidelity` | int | 数据分辨率（分钟，默认 1） |
| `startTs` | number | Unix 时间戳下限 |
| `endTs` | number | Unix 时间戳上限 |

**响应：** `{"history": [{"t": unix_ts, "p": price_float}, ...]}`

### GET /orders（需认证）

获取认证用户的挂单。

| 参数 | 类型 | 说明 |
|------|------|------|
| `market` | string | Condition ID 过滤 |
| `asset_id` | string | Token ID 过滤 |
| `next_cursor` | string | 分页游标 |

**认证方式：** 通过 py-clob-client 的 L2 HMAC-SHA256。需要从钱包私钥派生的 apiKey、secret、passphrase。

### GET /book

代币的完整订单簿。

| 参数 | 类型 | 说明 |
|------|------|------|
| `token_id` | string | **必填。** CLOB token ID |

## 3. Gamma API — 市场发现

**基础 URL：** `https://gamma-api.polymarket.com`

### GET /public-profile

| 参数 | 类型 | 说明 |
|------|------|------|
| `address` | string | 钱包地址 |

返回：显示名、简介、X 用户名、代理钱包、头像。

## 认证

仅 `GET /orders` 需要认证。其他所有端点为公开接口。

获取 API 凭证：
```python
from py_clob_client.client import ClobClient
client = ClobClient("https://clob.polymarket.com", chain_id=137, key=PRIVATE_KEY)
creds = client.create_or_derive_api_creds()
# 返回: {"apiKey": "...", "secret": "...", "passphrase": "..."}
```

凭证通过确定性方式派生，仅需生成一次。
