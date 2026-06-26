---
name: market-monitor
version: "0.1.0"
description: Monitor cryptocurrency and financial markets via exchange APIs (Binance, OKX). Track prices, analyze trends, and generate market reports.
homepage: https://www.binance.com
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires": { "env": ["BINANCE_API_KEY"] },
        "primaryEnv": "BINANCE_API_KEY",
      },
  }
---

# Skill: market-monitor（接口定义）

> **接口层**：定义触发条件、分析框架、输出规范和错误策略，与具体交易所无关。
> 各交易所的 API 端点和请求格式见 `impl/` 目录：
>
> - `impl/binance.md` — Binance 实现
> - `impl/okx.md` — OKX 实现
>
> 新增交易所时，只需添加对应 `impl/{exchange}.md`，本文件无需修改。

## 概述

实时监控加密货币市场数据，计算技术指标，生成交易信号。

## 触发条件

- 用户询问行情或价格
- 定时轮询（可配置间隔）
- 价格触及预设警报线

## 输入参数

| 参数     | 类型   | 必填 | 说明                                                |
| -------- | ------ | ---- | --------------------------------------------------- |
| pair     | string | 是   | 交易对，格式 BASE/QUOTE（如 BTC/USDT）              |
| exchange | string | 否   | 目标交易所 id（见 impl/ 目录），默认 `binance`      |
| interval | string | 否   | K 线周期（1m / 5m / 15m / 1h / 4h / 1d），默认 `1h` |
| limit    | number | 否   | K 线数量，默认 `100`                                |

## 执行流程

```
1. 根据 exchange 参数加载对应 impl/{exchange}.md
2. 调用实现层获取 24h 行情和 K 线数据
3. 基于 K 线数据计算技术指标
4. 按信号规则生成交易信号
5. 返回标准输出格式
```

## 技术指标（与交易所无关）

- 移动平均线：MA7、MA25、MA99
- RSI（周期 14）
- MACD（12, 26, 9）
- 布林带（20, 2）
- 成交量分析

## 信号生成规则

| 信号          | 触发条件                                  |
| ------------- | ----------------------------------------- |
| `strong_buy`  | RSI < 30 且 MACD 金叉 且 价格触及布林下轨 |
| `buy`         | RSI < 40 且 MA7 上穿 MA25                 |
| `neutral`     | 30 ≤ RSI ≤ 70 且无明确趋势                |
| `sell`        | RSI > 60 且 MA7 下穿 MA25                 |
| `strong_sell` | RSI > 70 且 MACD 死叉 且 价格触及布林上轨 |

## 输出格式

```json
{
  "pair": "BTC/USDT",
  "exchange": "binance",
  "interval": "1h",
  "timestamp": "ISO8601",
  "price": 0.0,
  "change24h": 0.0,
  "volume24h": 0.0,
  "indicators": {
    "rsi14": 0.0,
    "macd": { "line": 0.0, "signal": 0.0, "histogram": 0.0 },
    "ma": { "ma7": 0.0, "ma25": 0.0, "ma99": 0.0 },
    "bollinger": { "upper": 0.0, "mid": 0.0, "lower": 0.0 }
  },
  "signal": "strong_buy | buy | neutral | sell | strong_sell",
  "confidence": 0.0,
  "keyLevels": { "support": [], "resistance": [] }
}
```

## 错误处理策略

| 错误类型          | 处理方式                   |
| ----------------- | -------------------------- |
| 限流（429）       | 等待 60s 后重试，最多 3 次 |
| 无效参数（400）   | 提示用户修正交易对或参数   |
| 服务不可用（5xx） | 告知用户稍后重试           |
| 网络超时          | 记录错误，告知用户         |

## 安全约束

- 只读操作，不触发任何下单
- 只访问 impl/ 中定义的白名单域名
- 所有 API 调用由网关记录到审计日志
