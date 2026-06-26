# 支持的市场

## 美股 (US Stocks)

直接使用标准 ticker symbol。

| 示例 | 公司 |
|------|------|
| AAPL | Apple Inc. |
| TSLA | Tesla Inc. |
| NVDA | NVIDIA Corp. |
| META | Meta Platforms |
| MSFT | Microsoft Corp. |
| GOOGL | Alphabet Inc. |
| AMZN | Amazon.com |

**特点**：
- 支持 daily 和 intraday 两种模式
- 美东时间 9:30-16:00 盘中自动选 intraday，盘后选 daily
- 五个维度完整分析（技术面、基本面、情绪面、宏观面、期权面）

## 加密货币 (Crypto)

使用 `{COIN}USD` 格式。

| 示例 | 币种 |
|------|------|
| BTCUSD | Bitcoin |
| ETHUSD | Ethereum |
| SOLUSD | Solana |

**特点**：
- 24 小时交易，默认 intraday 模式
- 无期权面分析维度

## A 股 (China A-Shares)

直接传 6 位数字代码，系统自动识别交易所。

| 示例 | 公司 | 交易所 |
|------|------|--------|
| 600519 | 贵州茅台 | 上交所 (SH) |
| 000858 | 五粮液 | 深交所 (SZ) |
| 300750 | 宁德时代 | 创业板 (SZ) |

**特点**：
- 6 位数字代码，自动识别 SH/SZ 后缀
- 北京时间 9:30-15:00 盘中
- 无期权面分析维度

## Symbol 格式总结

| 市场 | 格式 | 示例 |
|------|------|------|
| 美股 | `TICKER` | `AAPL` |
| 加密货币 | `COINUSD` | `BTCUSD` |
| A 股 | `6位数字` | `600519` |
