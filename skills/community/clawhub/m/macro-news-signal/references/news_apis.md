# 新闻API参考

## 1. RSS订阅源

### 1.1 主要金融新闻RSS

| 来源           | URL                                                     | 覆盖范围       | 说明               |
| -------------- | ------------------------------------------------------- | -------------- | ------------------ |
| 彭博社最新报道 | https://bbg.buzzing.cc/feed.json                        | 最新新闻       | Folo订阅地址       |
| 彭博社         | https://feeds.bloomberg.com/markets/news.rss            | 市场           | 无                 |
| CNBC           | https://www.cnbc.com/id/100003114/device/rss/rss.html   | 商业           | 无                 |
| 金融时报       | https://www.ft.com/rss/home                             | 全球金融       | 无                 |
| 华尔街日报市场 | https://feeds.a.dj.com/rss/RSSMarketsMain.xml           | 市场           | 无                 |
| 经济学人       | https://www.economist.com/finance-and-economics/rss.xml | 宏观/金融      | 无                 |
| 联合早报       | http://rss.spriple.org/zaobao/realtime/world            | 国际-即时      | RSSHub公共实例地址 |
| 同花顺         | https://rss.spriple.org/10jqka/realtimenews             | 24小时全球财经 | RSSHub公共实例地址 |

#### 来源说明：

1. 彭博社最新报道Folo订阅查询：https://app.folo.is/share/feeds/70844804758158336
2. RSSHub公共实例查询：https://docs.rsshub.app/zh/guide/instances

以上来源均可查，属于Folo和RSSHub官方提供，可做为可信来源。

### 1.2 央行RSS

| 来源     | URL                                                | 覆盖范围   |
| -------- | -------------------------------------------------- | ---------- |
| 美联储   | https://www.federalreserve.gov/feeds/press_all.xml | 美联储声明 |
| 英国央行 | https://www.bankofengland.co.uk/rss                | 英央行声明 |

## 2. 指数接口

| 来源                  | URL                                                                                                                                                                   | 数据位置                                   |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| US10YTIP              | https://quote.cnbc.com/quote-html-webservice/restQuote/symbolType/symbol?symbols=US10YTIP&requestMethod=itv&noform=1&partnerId=2&fund=1&exthrs=1&output=json&events=1 | FormattedQuoteResult.FormattedQuote[].last |
| ICE U.S. Dollar Index | https://quote.cnbc.com/quote-html-webservice/restQuote/symbolType/symbol?symbols=.DXY&requestMethod=itv&noform=1&partnerId=2&fund=1&exthrs=1&output=json&events=1     | FormattedQuoteResult.FormattedQuote[].last |
| Gold COMEX            | https://quote.cnbc.com/quote-html-webservice/restQuote/symbolType/symbol?symbols=%40GC.1&requestMethod=itv&noform=1&partnerId=2&fund=1&exthrs=1&output=json&events=1  | FormattedQuoteResult.FormattedQuote[].last |
| ICE Brent Crude  | https://quote.cnbc.com/quote-html-webservice/restQuote/symbolType/symbol?symbols=%40LCO.1&requestMethod=itv&noform=1&partnerId=2&fund=1&exthrs=1&output=json&events=1  | FormattedQuoteResult.FormattedQuote[].last |




## 3. 股票接口

### 3.1 全球主要指数（Yahoo Finance API）
Yahoo Finance API 调用方式请参考 **3.2 Yahoo Finance API调用方式及数据说明**
该接口会响应最近五个交易日的指数数据。

#### 3.1.1 🇺🇸 美国
| 指数 | Symbol | API | 时区 | 开盘 | 收盘 | 市场类型 | ETF |
|------|--------|-----|------|------|------|----------|-----|
| 标普500 | ^GSPC | https://query1.finance.yahoo.com/v8/finance/chart/^GSPC?range=5d&interval=1d | America/New_York | 09:30 | 16:00 | developed | SPY |
| 纳斯达克综合 | ^IXIC | https://query1.finance.yahoo.com/v8/finance/chart/^IXIC?range=5d&interval=1d | America/New_York | 09:30 | 16:00 | developed | QQQ |
| 道琼斯工业 | ^DJI | https://query1.finance.yahoo.com/v8/finance/chart/^DJI?range=5d&interval=1d | America/New_York | 09:30 | 16:00 | developed | DIA |
| 罗素2000 | ^RUT | https://query1.finance.yahoo.com/v8/finance/chart/^RUT?range=5d&interval=1d | America/New_York | 09:30 | 16:00 | developed | IWM |

---

#### 3.1.2 🇨🇳 中国
| 指数 | Symbol | API | 时区 | 开盘 | 收盘 | 市场类型 | ETF |
|------|--------|-----|------|------|------|----------|-----|
| 上证指数 | 000001.SS | https://query1.finance.yahoo.com/v8/finance/chart/000001.SS?range=5d&interval=1d | Asia/Shanghai | 09:30 | 15:00 | emerging | - |
| 深证成指 | 399001.SZ | https://query1.finance.yahoo.com/v8/finance/chart/399001.SZ?range=5d&interval=1d | Asia/Shanghai | 09:30 | 15:00 | emerging | - |
| 创业板指 | 399006.SZ | https://query1.finance.yahoo.com/v8/finance/chart/399006.SZ?range=5d&interval=1d | Asia/Shanghai | 09:30 | 15:00 | emerging | - |
| 沪深300 | 000300.SS | https://query1.finance.yahoo.com/v8/finance/chart/000300.SS?range=5d&interval=1d | Asia/Shanghai | 09:30 | 15:00 | emerging | 510300.SS |

---

#### 3.1.3 🇭🇰 中国香港
| 指数 | Symbol | API | 时区 | 开盘 | 收盘 | 市场类型 | ETF |
|------|--------|-----|------|------|------|----------|-----|
| 恒生指数 | ^HSI | https://query1.finance.yahoo.com/v8/finance/chart/^HSI?range=5d&interval=1d | Asia/Hong_Kong | 09:30 | 16:00 | developed | 2800.HK |

---

#### 3.1.4 🇪🇺 欧洲
| 指数 | Symbol | API | 时区 | 开盘 | 收盘 | 市场类型 | ETF |
|------|--------|-----|------|------|------|----------|-----|
| 德国DAX | ^GDAXI | https://query1.finance.yahoo.com/v8/finance/chart/^GDAXI?range=5d&interval=1d | Europe/Berlin | 09:00 | 17:30 | developed | EWG |
| 英国富时100 | ^FTSE | https://query1.finance.yahoo.com/v8/finance/chart/^FTSE?range=5d&interval=1d | Europe/London | 08:00 | 16:30 | developed | EWU |
| 法国CAC40 | ^FCHI | https://query1.finance.yahoo.com/v8/finance/chart/^FCHI?range=5d&interval=1d | Europe/Paris | 09:00 | 17:30 | developed | EWQ |
| 欧洲Stoxx50 | ^STOXX50E | https://query1.finance.yahoo.com/v8/finance/chart/^STOXX50E?range=5d&interval=1d | Europe/Brussels | 09:00 | 17:30 | developed | FEZ |

---

#### 3.1.5 🇯🇵 日本
| 指数 | Symbol | API | 时区 | 开盘 | 收盘 | 市场类型 | ETF |
|------|--------|-----|------|------|------|----------|-----|
| 日经225 | ^N225 | https://query1.finance.yahoo.com/v8/finance/chart/^N225?range=5d&interval=1d | Asia/Tokyo | 09:00 | 15:00 | developed | 1321.T |

---

#### 3.1.6 🌏 其他市场
| 国家 | 指数 | Symbol | API | 时区 | 开盘 | 收盘 | 市场类型 | ETF |
|------|------|--------|-----|------|------|------|----------|-----|
| 🇮🇳 印度 | NIFTY 50 | ^NSEI | https://query1.finance.yahoo.com/v8/finance/chart/^NSEI?range=5d&interval=1d | Asia/Kolkata | 09:15 | 15:30 | emerging | INDA |
| 🇮🇳 印度 | SENSEX | ^BSESN | https://query1.finance.yahoo.com/v8/finance/chart/^BSESN?range=5d&interval=1d | Asia/Kolkata | 09:15 | 15:30 | emerging | - |
| 🇰🇷 韩国 | KOSPI | ^KS11 | https://query1.finance.yahoo.com/v8/finance/chart/^KS11?range=5d&interval=1d | Asia/Seoul | 09:00 | 15:30 | developed | EWY |
| 🇦🇺 澳大利亚 | ASX 200 | ^AXJO | https://query1.finance.yahoo.com/v8/finance/chart/^AXJO?range=5d&interval=1d | Australia/Sydney | 10:00 | 16:00 | developed | EWA |
| 🇨🇦 加拿大 | S&P/TSX | ^GSPTSE | https://query1.finance.yahoo.com/v8/finance/chart/^GSPTSE?range=5d&interval=1d | America/Toronto | 09:30 | 16:00 | developed | EWC |

### 3.2 Yahoo Finance API调用方式

调用 Yahoo Finance 接口必须使用 `scripts/format.py` 他会将原始复杂的嵌套 JSON 响应转化为**线性、扁平化且具备上下文语义**的数据结构。

#### 3.2.1 Metadata (资产背景)
| 字段名 | 类型 | 说明 | 示例 |
| :--- | :--- | :--- | :--- |
| `symbol` | String | 证券/指数代码 | "000001.SS" |
| `name` | String | 证券全称 | "SSE Composite Index" |
| `currency` | String | 交易货币单位 | "CNY" |
| `exchange` | String | 交易所全称 | "Shanghai" |
| `current_price`| Float | 最近一个交易日的成交价 | 3880.1 |
| `52_week_high` | Float | 过去 52 周的最高点 | 4197.23 |
| `52_week_low`  | Float | 过去 52 周的最低点 | 3040.69 |

#### 3.2.2 Data Points (时间序列)
`data_points` 是一个包含历史交易数据的数组。

| 字段名 | 类型 | 说明 | 优化处理 |
| :--- | :--- | :--- | :--- |
| `date` | String | 交易日期 (YYYY-MM-DD) | 已从时间戳转换 |
| `open` | Float | 当日开盘价 | 保留 2 位小数 |
| `high` | Float | 当日最高价 | 保留 2 位小数 |
| `low` | Float | 当日最低价 | 保留 2 位小数 |
| `close` | Float | 当日收盘价 | 保留 2 位小数 |
| `volume` | Integer| 当日成交量 | 原始数值 |

---

#### 3.2.3 示例 JSON 响应

```json
{
  "metadata": {
    "symbol": "000001.SS",
    "name": "SSE Composite Index",
    "currency": "CNY",
    "exchange": "Shanghai",
    "current_price": 3880.1,
    "52_week_high": 4197.23,
    "52_week_low": 3040.69
  },
  "data_points": [
    {
      "date": "2026-03-30",
      "open": 3884.28,
      "high": 3924.29,
      "low": 3872.78,
      "close": 3923.29,
      "volume": 595600
    },
    {
      "date": "2026-03-31",
      "open": 3924.07,
      "high": 3948.81,
      "low": 3891.86,
      "close": 3891.86,
      "volume": 606700
    }
  ]
}
```

## 4. 扩展数据
除了上述固定的一些接口，你也可以访问 https://tradingeconomics.com/ 获取到所有指数和商品价格