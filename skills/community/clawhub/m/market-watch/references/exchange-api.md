# Exchange HTTP API Reference

## Binance — 现货价格 ticker

**Endpoint:** `https://api.binance.com/api/v3/ticker/price`  
**Protocol:** HTTP GET（polling 5s）  
**Auth:** 无需（公开接口）

**单个资产:**
```
GET /api/v3/ticker/price?symbol=BTCUSDT
```

**批量资产（推荐）:**
```
GET /api/v3/ticker/price?symbols=["BTCUSDT","ETHUSDT","SOLUSDT"]
```

**返回:**
```json
[
  {"symbol": "BTCUSDT", "price": "84000.00"},
  {"symbol": "ETHUSDT", "price": "2100.50"}
]
```

**支持资产:** BTC, ETH, SOL, BNB, HYPE (HYPEUSDT)  
**更新频率:** 约 100ms 延迟（polling 间隔 5s）  
**备注:** 免费公开接口，无需 API key，IP 限制 1200 req/min

---

## OKX — 现货 ticker

**Endpoint:** `https://www.okx.com/api/v5/market/ticker`  
**Protocol:** HTTP GET（polling 5s）  
**Auth:** 无需（公开频道）

**请求:**
```
GET /api/v5/market/ticker?instId=BTC-USDT
```

**返回:**
```json
{
  "code": "0",
  "data": [{
    "instId": "BTC-USDT",
    "last": "84000.1",
    "bidPx": "84000.0",
    "askPx": "84001.0",
    "ts": "1672926468073"
  }]
}
```

**支持资产:** BTC, ETH, SOL, XAUT (XAUT-USDT), HYPE  
**备注:** OKX 可能因地区限制（中国大陆）返回 403，CoinGecko 兜底

---

## Bitget — 现货 ticker (v2)

**Endpoint:** `https://api.bitget.com/api/v2/spot/market/tickers`  
**Protocol:** HTTP GET（polling 5s）  
**Auth:** 无需（公开频道）

**请求:**
```
GET /api/v2/spot/market/tickers?symbol=BTCUSDT
```

**返回:**
```json
{
  "code": "00000",
  "data": [{
    "symbol": "BTCUSDT",
    "lastPr": "84000.0",   // v2 字段名
    "bidPr": "83999.9",
    "askPr": "84001.1",
    "ts": "1695702438018"
  }]
}
```

**支持资产:** BTC, ETH, SOL, HYPE (HYPEUSDT)

---

## Hyperliquid — allMids (perp + spot)

**Endpoint:** `https://api.hyperliquid.xyz/info`  
**Protocol:** HTTP POST（polling 5s）  
**Auth:** 无需（公开接口）

**请求:**
```json
POST /info
{"type": "allMids"}
```

**返回:**
```json
{
  "BTC":  "84000.0",
  "ETH":  "2100.0",
  "SOL":  "120.0",
  "HYPE": "15.5",
  ...
}
```

**支持资产:** HYPE 和所有 Hyperliquid 上市资产（perp + spot mids）  
**备注:** allMids 是全市场 mid price 快照，每次 POST 返回当前状态

---

## CoinGecko — HTTP Fallback

**Endpoint:** `https://api.coingecko.com/api/v3/simple/price`  
**Protocol:** HTTP GET（polling 30s fallback）  
**Auth:** 无需（免费公开 API）

**请求:**
```
GET /api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd
```

**返回:**
```json
{"bitcoin": {"usd": 84000}, "ethereum": {"usd": 2100}}
```

**限制:** 免费 tier 约 30req/min，30s 轮询间隔安全  
**覆盖:** BTC, ETH, SOL, BNB, HYPE, XAUT 等（通过 coin ID）

---

## pytdx — A股行情 (TCP 请求-响应)

**协议:** TCP request-response（非 HTTP，非推送）  
**Python:** `from pytdx.hq import TdxHq_API`  
**API:**
```python
api = TdxHq_API()
with api.connect("115.238.90.165", 7709):
    data = api.get_security_quotes([(1, "600519"), (0, "000001")])
    # market: 1=沪A(6开头/5开头), 0=深A
    # data[i]["price"] = 当前价格
```

**轮询间隔:** 盘中 3-5 秒（可支持，pytdx 延迟约 50-200ms）  
**交易时段:** 周一-五 9:30-11:30, 13:00-15:00 (北京时间)  
**备用服务器列表:**
- `115.238.90.165:7709`
- `115.238.56.198:7709`
- `180.153.18.170:7709`
- `101.227.73.20:7709`

---

## Asset → Exchange Priority

| 资产 | 优先级 |
|------|--------|
| BTC  | Binance → Hyperliquid → OKX → Bitget → CoinGecko |
| ETH  | Binance → Hyperliquid → OKX → Bitget → CoinGecko |
| SOL  | Binance → Hyperliquid → OKX → Bitget → CoinGecko |
| BNB  | Binance → CoinGecko |
| HYPE | Hyperliquid → Binance → OKX → Bitget → CoinGecko |
| XAUT | OKX → CoinGecko |
| A股  | pytdx (盘中) |

---

## 新闻源 HTTP API

### 金十数据（非官方接口）

> ⚠️ **非官方接口**：URL 和响应格式随时可能变化。代码内置降级处理。

**Endpoint:** `https://www.jin10.com/flash_newest.js`  
**Protocol:** HTTP GET  
**Auth:** 无需，但需要 Referer/User-Agent 伪装

**请求头（必要）:**
```
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ...
Referer: https://www.jin10.com/
```

**响应（当前已知格式）:**
```javascript
var flash_newest={"code":0,"message":"","data":[
  {"id":"abc123","time":"10:30:00","content":"BTC突破9万美元","important":1},
  ...
]};
```

**降级处理:** 先尝试直接解析 JSON，失败则用正则提取 `{...}` 块

---

### 华尔街见闻（非官方接口）

> ⚠️ **非官方接口**：响应结构可能随版本迭代变化。代码内置多路径解析。

**Endpoint:** `https://api-one.wallstcn.com/apiv1/content/lives`  
**Protocol:** HTTP GET  
**Auth:** 无需，但需要 Referer/User-Agent 伪装

**请求:**
```
GET /apiv1/content/lives?channel=global-channel&limit=20
Referer: https://wallstreetcn.com/
```

**响应（已知结构）:**
```json
{
  "code": 20000,
  "data": {
    "items": [
      {
        "id": 12345,
        "title": "文章标题",
        "summary": "摘要内容...",
        "published_at": 1741234567
      }
    ]
  }
}
```

**降级处理:** 支持 `data.items`、`data.list`、`data`（直接列表）等多种结构

---

### CoinDesk RSS

**Endpoint:** `https://www.coindesk.com/arc/outboundfeeds/rss/`  
**Format:** RSS 2.0  
**Auth:** 无需

---

### CoinTelegraph RSS

**Endpoint:** `https://cointelegraph.com/rss`  
**Format:** RSS 2.0  
**Auth:** 无需

---

### The Block RSS

**Endpoint:** `https://www.theblock.co/rss.xml`  
**Format:** RSS 2.0  
**Auth:** 无需

---

### Decrypt RSS

**Endpoint:** `https://decrypt.co/feed`  
**Format:** RSS 2.0 / Atom  
**Auth:** 无需
