# API 接口参考

## 认证

所有 API 请求需要在 Header 中携带 API Key：

```
X-API-Key: sk_live_xxx
```

## 响应格式

**成功响应**：
```json
{
  "code": 0,
  "msg": "success",
  "data": { ... }
}
```

**错误响应**：
```json
{
  "code": 40001,
  "msg": "错误信息",
  "data": { ... }
}
```

## 错误码

| 错误码 | HTTP 状态 | 说明 |
|--------|----------|------|
| 0 | 200 | 成功 |
| 40001 | 400 | 参数错误 |
| 40101 | 401 | API Key 无效，请前往金融界App获取最新API Key |
| 40102 | 401 | API Key 已过期，请前往金融界App获取最新API Key |
| 42901 | 429 | 超出每分钟请求限制，请稍后再试 |
| 42902 | 429 | 超出每日配额，请前往金融界App获取每日更多配额 |
| 50001 | 500 | 服务器内部错误 |
| 50201 | 502 | 上游服务错误 |

---

## 实时行情

获取股票、基金、指数的实时行情数据。

### 请求

```
POST /v1/quote/realtime
```

### 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| symbols | string[] | 是 | 证券代码列表，最多 100 个 |

### 请求示例

```json
{
  "symbols": ["600036.SH", "000001.SZ", "000001.SH"]
}
```

### 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| trade_date | int | 交易日 YYYYMMDD |
| quotes | Quote[] | 行情列表 |

**Quote 对象**：

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | string | 证券代码 |
| code | string | 原始代码 |
| name | string | 证券名称 |
| type | string | 类型：stock/fund/bond/index/sector |
| trade_date | int | 交易日 YYYYMMDD |
| time | int | 行情时间 HHMMSS |
| status | int | 交易状态：1=已收盘, 5=交易中, 7=停牌 |
| prev_close | float | 前收盘价 |
| open | float | 开盘价 |
| high | float | 最高价 |
| low | float | 最低价 |
| price | float | 最新价 |
| change | float | 涨跌额 |
| change_pct | float | 涨跌幅（小数） |
| volume | int | 成交量（股） |
| amount | float | 成交额（元） |
| bid_prices | float[] | 申买价（5档） |
| bid_volumes | int[] | 申买量（5档，手） |
| ask_prices | float[] | 申卖价（5档） |
| ask_volumes | int[] | 申卖量（5档，手） |
| bid_total_volume | int | 委买总量 |
| ask_total_volume | int | 委卖总量 |
| limit_up | float | 涨停价（仅股票/基金） |
| limit_down | float | 跌停价（仅股票/基金） |
| pe | float | 市盈率（仅股票） |
| iopv | float | IOPV（仅 ETF） |
| up_count | int | 上涨家数（仅指数/板块） |
| down_count | int | 下跌家数（仅指数/板块） |
| flat_count | int | 平盘家数（仅指数/板块） |

### 响应示例

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "trade_date": 20260320,
    "quotes": [
      {
        "symbol": "600036.SH",
        "code": "600036",
        "name": "招商银行",
        "type": "stock",
        "trade_date": 20260320,
        "time": 150000,
        "status": 1,
        "prev_close": 38.50,
        "open": 38.60,
        "high": 39.20,
        "low": 38.30,
        "price": 39.00,
        "change": 0.50,
        "change_pct": 0.013,
        "volume": 12345678,
        "amount": 480000000,
        "bid_prices": [38.99, 38.98, 38.97, 38.96, 38.95],
        "bid_volumes": [100, 200, 150, 300, 250],
        "ask_prices": [39.00, 39.01, 39.02, 39.03, 39.04],
        "ask_volumes": [150, 100, 200, 180, 120],
        "limit_up": 42.35,
        "limit_down": 34.65,
        "pe": 6.5
      }
    ]
  }
}
```

---

## K线数据

获取股票、基金、指数的历史日 K 线数据（只返回已收盘的历史数据）。

### 请求

```
POST /v1/quote/kline
```

### 参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| symbol | string | 是 | - | 证券代码 |
| period | string | 否 | daily | 周期：目前只支持 daily |
| adjust | string | 否 | none | 复权：none/qfq/hfq |
| limit | int | 否 | 100 | 返回数量 |
| start_date | int | 否 | - | 起始日期 YYYYMMDD，从该日期往最新方向取 |

### 使用模式

**模式1：获取最近N根K线（默认）**
- 只传 `limit`，从最新往历史取

```json
{"symbol": "600036.SH", "limit": 100}
```

**模式2：从指定日期往最新取**
- 传 `start_date` + `limit`，从起始日期往最新方向取

```json
{"symbol": "600036.SH", "start_date": 20260101, "limit": 100}
```

### 响应字段

| 字段 | 类型 | 说明 |
|------|------|------|
| symbol | string | 证券代码 |
| period | string | K线周期 |
| adjust | string | 复权类型 |
| count | int | 实际返回数量 |
| klines | Kline[] | K线数组 |
| truncated | bool | 是否被截断（可选，仅截断时出现） |

**Kline 对象**：

| 字段 | 类型 | 说明 |
|------|------|------|
| date | int | 日期 YYYYMMDD |
| open | float | 开盘价 |
| high | float | 最高价 |
| low | float | 最低价 |
| close | float | 收盘价 |
| volume | int | 成交量（股） |
| amount | float | 成交额（元） |

### 响应示例

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "symbol": "600036.SH",
    "period": "daily",
    "adjust": "qfq",
    "count": 100,
    "klines": [
      {
        "date": 20260101,
        "open": 36.50,
        "high": 37.00,
        "low": 36.30,
        "close": 36.80,
        "volume": 10000000,
        "amount": 368000000
      }
    ]
  }
}
```

> **注意**：当响应中包含 `truncated: true` 时，表示可能有更多数据未返回。建议调整 `limit` 或缩小查询范围。

---

## 证券代码格式

| 市场 | 后缀 | 示例 |
|------|------|------|
| 上海 | .SH | 600036.SH（招商银行） |
| 深圳 | .SZ | 000001.SZ（平安银行） |

### 常用代码

| 类型 | 示例 |
|------|------|
| 上证指数 | 000001.SH |
| 深证成指 | 399001.SZ |
| 沪深300 | 000300.SH |
| 创业板指 | 399006.SZ |
| 科创50 | 000688.SH |
