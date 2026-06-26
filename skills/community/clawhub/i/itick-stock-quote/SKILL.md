---
name: itick-stock-quote
description: 查询股票实时盘中行情、股票信息等功能。支持HK（港股）、SH（上证）、SZ（深证）、US（美股）、SG（新加坡）、JP（日本）、TW（中国台湾）、IN（印度）、TH（泰国）、DE（德国、MX（墨西哥）、MY（马来西亚）、TR（土耳其）、ES（西班牙）、NL（荷兰）、GB（英国）等，可获取实时报价和深度行情（买卖盘口）。使用itick.org API。
metadata:
  { "openclaw": { "emoji": "🗠", "primaryEnv":"ITICK_API_TOKEN", "requires": {"env":["ITICK_API_TOKEN"]} } }
---

# 股票实时行情查询

使用itick API查询股票实时行情。

## ⚠️ Token 与鉴权（必读）

API Token 通过环境变量 `ITICK_API_TOKEN` 自动注入（由 ClawHub 管理），**不需要用户在对话中手动提供或粘贴 Token**。

# 使用方法

## 1. 股票信息

```bash
curl -X GET "https://api.itick.org/stock/info?type=stock&region=<region>&code=<code>" \
  -H "accept: application/json" \
  -H "token: $ITICK_API_TOKEN"
```

响应参数示例：

```json
 {
  "code": 0, //响应code
  "msg": "ok", //响应描述
  "data": { //响应结果
    "c": "AAPL", //股票代码
    "n": "Apple Inc.", //股票名称
    "t": "stock", //类型
    "e": "NASDAQ", //交易所
    "s": "Electronic Technology", //所属板块
    "i": "Telecommunications Equipment", //所属行业
    "r": "USD", //区域/国家代码
    "bd": "Apple, Inc. engages in the design, manufacture, and sale of smartphones, personal computers, tablets, wearables and accessories, and other varieties of related services. It operates through the following geographical segments: Americas, Europe, Greater China, Japan, and Rest of Asia Pacific. The Americas segment includes North and South America. The Europe segment consists of European countries, as well as India, the Middle East, and Africa. The Greater China segment comprises China, Hong Kong, and Taiwan. The Rest of Asia Pacific segment includes Australia and Asian countries. Its products and services include iPhone, Mac, iPad, AirPods, Apple TV, Apple Watch, Beats products, AppleCare, iCloud, digital content stores, streaming, and licensing services. The company was founded by Steven Paul Jobs, Ronald Gerald Wayne, and Stephen G. Wozniak in April 1976 and is headquartered in Cupertino, CA.", //公司简介
    "wu": "http://www.apple.com", //公司网站URL
    "mcb": 3436885784335, //总市值
    "tso": 14840389413, //总股本
    "pet": 35.3865799154784, //市盈率
    "fcc": "USD" //货币代码
  }
}
```

## 2. 股票IPO

```bash
curl -X GET "https://api.itick.org/stock/ipo?type=<type>&region=<region>" \
  -H "accept: application/json" \
  -H "token: $ITICK_API_TOKEN"
```

响应参数示例：

```json
{
  "code": 0, //响应code
  "msg": "ok", //响应描述
  "data": { //响应结果
    "content": [
      {
        "dt": 1755820800000, //上市日期时间戳（单位：毫秒）
        "cn": "Picard Medical Inc", //股票公司名称
        "sc": "PMI", //股票代码
        "ex": "NYSE", //交易所名称
        "mc": "19.1M", //市值
        "pr": "3.50-4.50", //价格
        "ct": "US", //国家代码
        "bs": 1648403200, //开始申购时间（单位：秒）
        "es": 1648998400, //申购截止时间（单位：秒）
        "ro": 1649001600 //公布中签结果时间（单位：秒）
      },
      {
        "dt": 1755734400000,
        "cn": "Elite Express Holding Inc",
        "sc": "ETS",
        "ex": "NASDAQ",
        "mc": "16.0M",
        "pr": "4.00",
        "ct": "US",
        "bs": 1648403200,
        "es": 1648998400,
        "ro": 1649001600
      }
    ],
    "page": 0,
    "totalElements": 28,
    "totalPages": 14,
    "last": false,
    "size": 2
  }
}
```

### 3. 股票除权因子

```bash
curl -X GET "https://api.itick.org/stock/split?region=<region>" \
  -H "accept: application/json" \
  -H "token: $ITICK_API_TOKEN"
```

响应参数示例：

```json
{
  "code": 0, //响应code
  "msg": "ok", //响应描述
  "data": { //响应结果
    "content": [
      {
        "d": 1768521600000, //复权日期时间戳（单位：毫秒）
        "r": "HK", //国家/地区代码
        "n": "Polyfair Holdings", //股票名称
        "c": "8532", //股票代码
        "v": "1:10" //复权因子，拆股/合股的比例
      },
      {
        "d": 1768262400000,
        "r": "HK",
        "n": "China Supply Chain Holdings",
        "c": "3708",
        "v": "1:10"
      }
    ],
    "totalPages": 1,
    "totalElements": 3,
    "page": 0,
    "last": true,
    "size": 20
  }
}
```

### 4. 实时成交

```bash
curl -X GET "https://api.itick.org/stock/tick?region=<region>&code=<code>" \
  -H "accept: application/json" \
  -H "token: $ITICK_API_TOKEN"
```

响应参数示例：

```json
{
  "code": 0, //响应code
  "msg": null, //响应描述
  "data": {
    "s": "700", //产品代码
    "ld": 567, //最新价
    "t": 1754554087000, //最新成交的时间戳：2025-08-07 08:08:07 UTC
    "v": 1134500, //成交数量
    "te": 0 //交易时段 0:常规交易 1:盘前交易 2:盘后交易
  }
}
```

### 5. 实时报价

```bash
curl -X GET "https://api.itick.org/stock/quote?region=<region>&code=<code>" \
  -H "accept: application/json" \
  -H "token: $ITICK_API_TOKEN"
```

响应参数示例：

```json
{
  "code": 0, //响应code
  "msg": null, //响应描述
  "data": { //响应结果
    "s": "700", //产品代码
    "ld": 616, //最新价
    "o": 608, //开盘价
    "p": 608, //前日收盘价
    "h": 616, //最高价
    "l": 601.5, //最低价
    "t": 1765526889000, //最新成交的时间戳：2025-12-12 08:08:09 UTC
    "v": 17825495, //成交数量
    "tu": 10871536434.36, //成交额
    "ts": 0, //交易状态 0:正常交易 1:停牌 2:退市 3:熔断
    "ch": 8, //涨跌额
    "chp": 1.32 //涨跌幅百分比
  }
}
```

### 6. 实时盘口

```bash
curl -X GET "https://api.itick.org/stock/depth?region=<region>&code=<code>" \
  -H "accept: application/json" \
  -H "token: $ITICK_API_TOKEN"
```

响应参数示例：

```json
{
  "code": 0, //响应code
  "msg": null, //响应描述
  "data": { //响应结果
    "s": "700", //产品代码
    "a": [ //卖盘
      {
        "po": 1, //档位
        "p": 567, //价格
        "v": 13400, //挂单量
        "o": 3 //订单数量
      },
      {
        "po": 2,
        "p": 567.5,
        "v": 170200,
        "o": 52
      },
      {
        "po": 3,
        "p": 568,
        "v": 268400,
        "o": 217
      },
      {
        "po": 4,
        "p": 568.5,
        "v": 126000,
        "o": 72
      },
      {
        "po": 5,
        "p": 569,
        "v": 132200,
        "o": 133
      },
      {
        "po": 6,
        "p": 569.5,
        "v": 185800,
        "o": 108
      },
      {
        "po": 7,
        "p": 570,
        "v": 423200,
        "o": 706
      },
      {
        "po": 8,
        "p": 570.5,
        "v": 108500,
        "o": 58
      },
      {
        "po": 9,
        "p": 571,
        "v": 141400,
        "o": 221
      },
      {
        "po": 10,
        "p": 571.5,
        "v": 83600,
        "o": 90
      }
    ],
    "b": [ //买盘
      {
        "po": 1, //档位
        "p": 566.5, //价格
        "v": 24700, //挂单量
        "o": 5 //订单数量
      },
      {
        "po": 2,
        "p": 566,
        "v": 27500,
        "o": 7
      },
      {
        "po": 3,
        "p": 565.5,
        "v": 35000,
        "o": 17
      },
      {
        "po": 4,
        "p": 565,
        "v": 177200,
        "o": 80
      },
      {
        "po": 5,
        "p": 564.5,
        "v": 42800,
        "o": 30
      },
      {
        "po": 6,
        "p": 564,
        "v": 43000,
        "o": 53
      },
      {
        "po": 7,
        "p": 563.5,
        "v": 82600,
        "o": 34
      },
      {
        "po": 8,
        "p": 563,
        "v": 103900,
        "o": 78
      },
      {
        "po": 9,
        "p": 562.5,
        "v": 58700,
        "o": 31
      },
      {
        "po": 10,
        "p": 562,
        "v": 36900,
        "o": 92
      }
    ]
  }
}
```

### 7. K线查询

```bash
curl -X GET "https://api.itick.org/stock/kline?region=<region>&code=<code>&kType=<ktype>&limit=<limit>&et=<et>" \
  -H "accept: application/json" \
  -H "token: $ITICK_API_TOKEN"
```

响应参数示例：

```json
{
  "code": 0, //响应code
  "msg": null, //响应描述
  "data": [ //响应结果
    {
      "tu": 56119888070.5, //成交金额
      "c": 534.5, //该K线收盘价
      "t": 1741239000000, //时间戳：2025-03-06 05:30:00 UTC
      "v": 104799385, //成交数量
      "h": 536, //该K线最高价
      "l": 534.5, //该K线最低价
      "o": 535 //该K线开盘价
    }
  ]
}
```

### 查询参数说明

| 参数     | 说明                                                                                                                             |
| ------ | ------------------------------------------------------------------------------------------------------------------------------ |
| region | 市场代码，支持HK（港股）、SH（上证）、SZ（深证）、US（美股）、SG（新加坡）、JP（日本）、TW（中国台湾）、IN（印度）、TH（泰国）、DE（德国、MX（墨西哥）、MY（马来西亚）、TR（土耳其）、ES（西班牙）、NL（荷兰）、GB（英国）等 |
| type   | 类型（upcoming 即将上市、recent 近期上市的股票）                                                                                               |
| code   | 产品代码                                                                                                                           |
| ktype  | 周期 1分钟、2五分钟、3十五分钟、4三十分钟、5一小时、8一天、9一周、10一月                                                                                      |
| et     | 查询截止时间戳 如（1751328000000）为空时默认为当前时间戳                                                                                            |
| limit  | 查询条数                                                                                                                           |

## 示例

```bash
# 查询港股南方两倍做多恒生科技实时报价
curl -X GET "https://api.itick.org/stock/quote?region=HK&code=7226" \
  -H "accept: application/json" \
  -H "token: d267a8c7d18a4ba4b19c81225a2ffd3eae0e9ca3bd1a4bd9b969dfee99ee7acd"

# 查询沪A贵州茅台实时报价
curl -X GET "https://api.itick.org/stock/quote?region=SH&code=600519" \
  -H "accept: application/json" \
  -H "token: d267a8c7d18a4ba4b19c81225a2ffd3eae0e9ca3bd1a4bd9b969dfee99ee7acd"
```
