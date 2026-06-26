# market-monitor 实现：Binance

> 本文件是 `SKILL.md` 的实现层，描述如何通过 Binance API 获取行情数据。
> 替换交易所时，参照本文件格式创建新的 `impl/{exchange}.md` 即可。

## 基础信息

| 字段             | 值                                    |
| ---------------- | ------------------------------------- |
| exchange id      | `binance`                             |
| 网络白名单       | `api.binance.com`, `fapi.binance.com` |
| 认证方式         | API Key Header（只读接口无需签名）    |
| API Key 环境变量 | `BINANCE_API_KEY`                     |

## 数据获取

### 24h 行情

```
GET https://api.binance.com/api/v3/ticker/24hr
参数: symbol={pair}（去掉 /，如 BTC/USDT → BTCUSDT）

响应字段映射:
  lastPrice   → price
  priceChangePercent → change24h
  volume      → volume24h（基础资产成交量）
  quoteVolume → volume24h_usd
```

### K 线数据

```
GET https://api.binance.com/api/v3/klines
参数:
  symbol   = {pair}（格式同上）
  interval = {interval}（1m/5m/15m/1h/4h/1d，与接口层一致）
  limit    = {limit}

响应为数组，每项结构:
  [0] openTime, [1] open, [2] high, [3] low, [4] close,
  [5] volume, [6] closeTime, ...
```

## 间隔参数映射

| 接口层 interval | Binance 参数 |
| --------------- | ------------ |
| 1m              | 1m           |
| 5m              | 5m           |
| 15m             | 15m          |
| 1h              | 1h           |
| 4h              | 4h           |
| 1d              | 1d           |

## 错误码对照

| HTTP 状态 | Binance 错误码 | 处理方式                              |
| --------- | -------------- | ------------------------------------- |
| 429       | —              | 检查 `Retry-After` 响应头，等待后重试 |
| 400       | -1121          | 交易对无效，提示用户检查 pair 格式    |
| 400       | -1100          | 参数非法，提示用户检查 interval       |
| 403       | —              | IP 被封，通知用户                     |
| 5xx       | —              | 服务故障，建议切换到 impl/okx.md      |
