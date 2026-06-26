# market-monitor 实现：OKX

> 本文件是 `SKILL.md` 的实现层，描述如何通过 OKX API 获取行情数据。

## 基础信息

| 字段             | 值                                                    |
| ---------------- | ----------------------------------------------------- |
| exchange id      | `okx`                                                 |
| 网络白名单       | `api.okx.com`, `www.okx.com`                          |
| 认证方式         | 公开行情接口无需签名；私有接口需 OK-ACCESS-KEY + 签名 |
| API Key 环境变量 | `OKX_API_KEY`, `OKX_API_SECRET`, `OKX_PASSPHRASE`     |

## 数据获取

### 24h 行情

```
GET https://api.okx.com/api/v5/market/ticker
参数: instId={pair}（格式保持 BTC-USDT，以 - 分隔）

响应字段映射（data[0]）:
  last     → price
  sodUtc8  → open（当日开盘，用于计算 change24h）
  vol24h   → volume24h（基础资产）
  volCcy24h→ volume24h_usd
```

### K 线数据

```
GET https://api.okx.com/api/v5/market/candles
参数:
  instId = {pair}（格式 BTC-USDT）
  bar    = {interval}（见下方映射）
  limit  = {limit}

响应为数组，每项结构:
  [0] ts, [1] open, [2] high, [3] low, [4] close,
  [5] vol（基础资产）, [6] volCcy（计价资产）, [7] confirm
```

## 间隔参数映射

| 接口层 interval | OKX bar 参数 |
| --------------- | ------------ |
| 1m              | 1m           |
| 5m              | 5m           |
| 15m             | 15m          |
| 1h              | 1H           |
| 4h              | 4H           |
| 1d              | 1D           |

## 交易对格式转换

| 接口层格式 | OKX 格式 |
| ---------- | -------- |
| BTC/USDT   | BTC-USDT |
| ETH/USDT   | ETH-USDT |
| SOL/USDT   | SOL-USDT |

## 错误码对照

| HTTP 状态 | OKX sCode | 处理方式                             |
| --------- | --------- | ------------------------------------ |
| 200       | 51001     | instId 无效，提示用户检查交易对格式  |
| 200       | 50011     | 请求频率超限，等待 60s 后重试        |
| 429       | —         | 降低请求频率                         |
| 5xx       | —         | 服务故障，建议切换到 impl/binance.md |
