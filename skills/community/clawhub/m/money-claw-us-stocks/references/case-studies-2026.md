# 2026 极端行情案例口径

## 用途

在解释模型来源、验证规则或撰写项目文档时使用本文件。不要把历史事件研究描述为全部事前实盘信号，也不要把历史最高涨幅解释为可复制收益。

统一标签：

```text
R_high  = High(t) / Close(t-1) - 1
R_close = Close(t) / Close(t-1) - 1
```

`R_high >= 500%` 表示事件日最高价相对前收至少上涨五倍，不表示投资者能够在最低点买入并在最高点卖出。

## 样本内案例

以下事件来自一年期公开数据回测，价格为事件当时口径，金额和百分比保留两位小数：

| Symbol | Trade date | Prev close | Open | High | Close | R_high | R_close | Volume | Official gap |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ELPW | 2026-01-30 | $0.43 | $0.41 | $15.27 | $13.94 | 3,451.16% | 3,141.86% | 25.92m | -4.42% |
| SKK | 2026-05-04 | $1.75 | $1.76 | $17.95 | $12.19 | 925.71% | 596.57% | 22.20m | 0.86% |
| TDIC | 2026-05-13 | $2.36 | $2.99 | $30.00 | $23.05 | 1,171.19% | 876.69% | 109.26m | 26.48% |
| CPOP | 2026-06-10 | $0.36 | $0.51 | $2.55 | $1.52 | 608.33% | 322.22% | 287.96m | 41.67% |
| RGNT | 2026-06-15 | $1.50 | $1.70 | $15.50 | $9.40 | 933.33% | 526.67% | 186.53m | 13.33% |

这些案例说明极端行情不只有 `Gap >= 100%` 路径。SKK、RGNT 和 ELPW 等低 gap 事件必须依赖早盘周转、VWAP、预热量和供应结构确认，不能用收盘后数据冒充盘前因子。

## 样本外验证：CPHI

CPHI 的 2026-07-21 盘中截面发生在回测截止日之后，不进入训练样本：

```text
prev_close = $0.91
open ~= $0.86
high/snapshot_price = $11.55
R_high ~= 1,169.23%
official_gap ~= -5.49%
volume ~= 55.18m
turnover_total ~= 1.36x
turnover_vendor_float ~= 3.35x
```

该事件用于验证独立的 `CPHI_SUBTYPE`：低 official gap、事件前异常量预热、开盘后供应快速周转并保持在 VWAP 上方。它不是常规 gap squeeze，也不改变样本内命中率。

## 样本外执行研究：CYCU

CYCU 的 2026-07-30 事件进一步验证了 `CPHI_SUBTYPE` 的低 official gap、盘前预热和盘中周转扩张路径。该案例同时存在注册转售与 Nasdaq 合规风险，因此只用于 5 分钟阶段和退出逻辑研究，不记录为生产环境授权交易。

完整的 point-in-time 时间线、消息发酵、量价公式与供应冲突见 [cycu-2026-07-30.md](cycu-2026-07-30.md)。

## 数据来源与限制

- 样本内价格与成交量：Yahoo Finance Chart/Spark 的 point-in-time 日线，结合 split effective date 审计。
- 证券池与公司行动：Nasdaq Stock Screener、Nasdaq corporate actions。
- 股本和稀释：SEC EDGAR、公司公告。
- CPHI：用户盘中截图及公司公开披露，按截图时间戳计算。
- CYCU：用户分时截图、公司投资者关系公告及 SEC 文件；盘后数据与正则盘标签严格分离。
- 公开数据研究存在 survivorship bias、历史 ticker、奇异打印、LULD、slippage 和 float 时点误差。
