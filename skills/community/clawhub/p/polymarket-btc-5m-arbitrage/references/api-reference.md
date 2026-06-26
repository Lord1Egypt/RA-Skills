# Polymarket API 参考文档

## Base URLs

```
Gamma API: https://gamma-api.polymarket.com
CLOB API:  https://clob.polymarket.com
```

## Gamma API (市场信息)

### 获取市场详情

```bash
GET /markets?slug={slug}
```

响应字段:
- `id`: 市场ID
- `question`: 市场问题
- `slug`: 市场slug
- `clobTokenIds`: CLOB代币ID数组 [Yes, No]
- `outcomePrices`: 当前价格 ["0.50", "0.50"]
- `liquidity`: 流动性
- `volume24hr`: 24小时成交量
- `bestBid`: 最佳买价
- `bestAsk`: 最佳卖价
- `endDate`: 结束时间

### 获取活跃市场

```bash
GET /markets?active=true&closed=false&limit=100
```

## CLOB API (订单簿)

### 获取订单簿

```bash
GET /book?tokenId={token_id}
```

响应:
```json
{
  "bids": [
    {"price": "0.50", "size": "100"}
  ],
  "asks": [
    {"price": "0.51", "size": "50"}
  ]
}
```

### 获取价格

```bash
GET /price?tokenId={token_id}
GET /midpoint?tokenId={token_id}
```

## 交易

### 限价单

```bash
POST /orders
{
  "tokenId": "...",
  "side": "BUY",  // or "SELL"
  "price": "0.50",
  "size": 10
}
```

### 市价单

```bash
POST /orders
{
  "tokenId": "...",
  "side": "BUY",
  "size": 10,
  "type": "MARKET"
}
```

## BTC 5分钟市场

- **系列Slug**: `btc-up-or-down-5m`
- **市场Slug格式**: `btc-updown-5m-{timestamp}`
- **代币**: Up (Yes) / Down (No)
- **分辨率**: Chainlink BTC/USD

### 获取当前市场

```bash
curl "https://gamma-api.polymarket.com/markets?slug=btc-up-or-down-5m"
```
