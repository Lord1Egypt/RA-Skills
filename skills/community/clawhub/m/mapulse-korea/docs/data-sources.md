# Data Sources API Reference

## 1. Daum Finance API

**Base URL**: `https://finance.daum.net/api`

**Required Headers** (all endpoints):
```
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
Referer: https://finance.daum.net
```

### 1.1 Stock Quote — `GET /api/quotes/A{ticker}`

Single stock with 50+ fields. The richest single-request endpoint.

**Key fields**:
```json
{
  "name": "삼성전자",
  "market": "KOSPI",
  "tradePrice": 196800.0,
  "changeRate": 0.0429,
  "marketCap": 1164984743049600,
  "marketCapRank": 1,
  "foreignRatio": 0.4956,
  "per": 38.12,
  "pbr": 3.26,
  "eps": 4950.0,
  "bps": 57951.0,
  "dps": 1446.0,
  "debtRatio": 0.29937,
  "high52wPrice": 223000.0,
  "low52wPrice": 52900.0,
  "wicsSectorName": "반도체와반도체장비",
  "wicsSectorChangeRate": 0.0349,
  "sales": 93837371000000.0,
  "operatingProfit": 20073660000000.0,
  "netIncome": 19641745000000.0,
  "companySummary": "동사는 1969년 설립...",
  "accTradeVolume": 9527843,
  "accTradePrice": 1873730430550.0,
  "openingPrice": 198000.0,
  "highPrice": 198000.0,
  "lowPrice": 195500.0,
  "prevClosingPrice": 188700.0,
  "marketStatus": "REGULAR_HOURS"
}
```

### 1.2 Batch Quote — `GET /api/quotesv4?codes=A005930,A000660,...`

Up to 20 tickers per request.

**Response**: `{ "today": {...}, "yesterday": {...}, "quotes": [...] }`

### 1.3 Daily Chart — `GET /api/charts/A{ticker}/days?limit={N}&adjusted=true`

**Header override**: `Referer: https://finance.daum.net/quotes/A{ticker}`

**Response**: `{ "code": 200, "data": [{date, tradePrice, openingPrice, highPrice, lowPrice, change, changePrice, changeRate, candleAccTradeVolume}] }`

### 1.4 Market Indexes — `GET /api/domestic/trend/market/indexes`

**Header override**: `Referer: https://finance.daum.net/domestic`

**Response**:
```json
{
  "KOSPI": [
    {
      "date": "2026-03-17 00:00:00",
      "tradePrice": 5699.81,
      "change": "RISE",
      "changePrice": 149.96,
      "accTradeVolume": 742087,
      "individualStraightPurchasePrice": -292572593184.0,
      "foreignStraightPurchasePrice": 7915489161.0,
      "institutionStraightPurchasePrice": 282601853085.0
    }
  ],
  "KOSDAQ": [...]
}
```

### 1.5 Market Investors — `GET /api/domestic/trend/market/investors`

**Header override**: `Referer: https://finance.daum.net/domestic`

Per-market daily net purchase by investor type (individual, foreign, institution, program).

### 1.6 WICS Sectors — `GET /api/sector/wics`

**Header override**: `Referer: https://finance.daum.net/domestic`

**Response**: `{ "code": 200, "data": [{sectorCode, sectorName, changeRate, stockCount, includedStocks: [{name, symbolCode, change, changeRate, tradePrice, marketCap, foreignRatio}]}] }`

### 1.7 Search Ranks — `GET /api/search/ranks`

**Response**: `{ "data": [{rank, rankChange, name, symbolCode, tradePrice, change, changeRate, accTradeVolume, isNew}] }`

### Known Non-Working Endpoints

| Endpoint | Status |
|----------|--------|
| `GET /api/investor/A{ticker}` | 500 Internal Server Error |
| `GET /api/trend/rise` | 500 Internal Server Error |
| `GET /api/domestic/trend/price_performance` | 500 Internal Server Error |

---

## 2. Naver Finance Mobile API

**Base URL**: `https://m.stock.naver.com/api`

No special headers required (default User-Agent works).

### 2.1 Stock Basic — `GET /api/stock/{ticker}/basic`

Real-time price, name, market status.

### 2.2 Stock Integration — `GET /api/stock/{ticker}/integration`

**Key fields in `totalInfos` array**:
```
전일: 188,700          시가: 194,400
고가: 198,700          저가: 194,400
거래량: 21,209,942      대금: 4,175,929백만
시총: 1,163조 8,008억   외인소진율: 49.56%
52주 최고: 228,500      52주 최저: 52,000
PER: 29.95배           EPS: 6,564원
추정PER: 8.08배        추정EPS: 24,341원
PBR: 3.07배            BPS: 63,997원
배당수익률: 0.85%       주당배당금: 1,668원
```

### 2.3 Annual Financials — `GET /api/stock/{ticker}/finance/annual`

Revenue, operating profit, net income, ROE, debt ratio, EPS by year.

### 2.4 Disclosures — `GET /api/stock/{ticker}/disclosure?page=1&size={N}`

Recent corporate filings with title, datetime, author.

### 2.5 Price History — `GET /api/stock/{ticker}/price?page=1&pageSize={N}`

Daily OHLCV with change percentage.

### 2.6 Investor Trend — `GET /api/stock/{ticker}/trend?page=1&pageSize={N}`

Foreign/institution/individual net purchase per day with foreign holding ratio.

### 2.7 SSR Discuss Page — `GET m.stock.naver.com/domestic/stock/{ticker}/discuss`

Scraped via `__NEXT_DATA__` JSON. Contains:
- OpenTalk real-time chat messages
- Broker research reports with target prices
- Investor trading trends (foreign/institution/individual)
- Industry peer comparison

---

## 3. pykrx (Python Library)

```python
from pykrx import stock

# Daily OHLCV
df = stock.get_market_ohlcv("20260310", "20260314", "005930")
# Columns: 시가, 고가, 저가, 종가, 거래량, 등락률

# Business days
stock.get_business_days("20260301", "20260314")

# Ticker list
stock.get_market_ticker_list("20260314", market="KOSPI")
```

---

## 4. Other Sources

### Exchange Rates
```
GET https://api.exchangerate-api.com/v4/latest/USD
→ { "rates": { "KRW": 1491.16, "CNY": 6.90, "JPY": 159.17 } }
```

### VIX (Google Finance Scrape)
```
GET https://www.google.com/finance/quote/VIX:INDEXCBOE
→ Parse data-last-price from HTML
```

### Fear & Greed
```
GET https://api.alternative.me/fng/?limit=7
→ { "data": [{ "value": "28", "value_classification": "Fear" }] }
```

### S&P 500 (Yahoo Finance)
```
GET https://query2.finance.yahoo.com/v8/finance/chart/^GSPC?range=1d&interval=1d
```

### Crypto (Binance)
```
GET https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT
```

### 6551.io OpenNews
```
POST https://ai.6551.io/open/news_latest
Authorization: Bearer $OPENNEWS_TOKEN
→ 72+ sources, AI-rated with trading signals
```

### 6551.io OpenTwitter
```
POST https://ai.6551.io/open/twitter_search
Authorization: Bearer $TWITTER_TOKEN
→ Tweet search, KOL tracking, deleted tweets
```
