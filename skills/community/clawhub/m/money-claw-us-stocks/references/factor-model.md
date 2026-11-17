# 美股极端暴涨因子模型

精确案例口径与样本内/样本外边界见 [case-studies-2026.md](case-studies-2026.md)。

## 1. 回测定义

回测窗口：2025-07-21 至 2026-07-20，约 252 个完成交易日。

证券池：当前 Nasdaq screener 中的全美交易所普通股、Ordinary Shares、ADR/ADS，加显式历史 ticker aliases；排除 ETF、优先股、权证、Rights、Units 和债券。

```text
R_close(t) = Close(t) / Close(t-1) - 1
R_high(t)  = High(t)  / Close(t-1) - 1
```

- 主标签：`R_high >= 500%`
- 严格标签：`R_close >= 500%`
- IPO 首日无前收，不计入事件。
- split effective date 与事件日重合时剔除。

覆盖 5,544 只证券，识别 58 个真实 `R_high >= 500%` 事件，其中 25 个收盘仍 `>=500%`。加入上市至少 20 日、事件前价格不超过 $5.00、当日成交量至少 10.00m 股、当日成交额至少 $10.00m 后，得到 38 个 CPHI-like 样本。

```text
event rate per stock-year = 38 / 5,544 = 0.69%
event rate per stock-day  = 38 / (5,544 * 252) = 0.00272%
```

约每 36,765 个 stock-days 出现一次。

## 2. 样本分布

| 因子 | Q25 | 中位数 | Q75 |
|---|---:|---:|---:|
| 事件前股价 | $0.70 | $1.53 | $2.47 |
| 日内最高涨幅 | 553.71% | 652.87% | 925.71% |
| 收盘涨幅 | 271.61% | 361.47% | 532.77% |
| 当日成交量 | 77.43m | 137.66m | 224.21m |
| 当日成交额 | $437.71m | $843.73m | $1,759.48m |
| Relative Volume 20D | 55.58x | 439.52x | 2,615.85x |
| 事件前20日收益 | -26.95% | -12.63% | -2.03% |
| 事件前20日波动率 | 5.40% | 7.72% | 11.30% |
| 正式开盘 Gap | 26.48% | 161.95% | 349.57% |
| 收盘距日内高点 | -53.00% | -41.42% | -30.11% |

附加频率：

- 收盘仍 `>=500%`：31.58%
- 事件前20日收益为负：78.95%
- 收盘从高点回落至少30%：78.95%
- 中国、香港、新加坡发行人：50.00%

发行人地域没有匹配控制组，不得单独解释为预测 odds。

## 3. 条件因子检验

控制组为同一数据集内“收盘涨幅至少50%、非split、上市至少20日”的1,119个事件。目标是判断成为大涨股后，哪些条件增加触发 `R_high >= 500%` 的概率。

| 因子 | 可用时点 | 有因子命中率 | 无因子命中率 | OR | 95% CI | 解释 |
|---|---|---:|---:|---:|---:|---|
| 前收 ≤$5 | 事件前 | 5.29% | 4.93% | 1.04 | 0.54–2.02 | 单独无效 |
| 20D中位成交额 ≤$1.00m | 事件前 | 5.96% | 2.50% | **2.31** | **1.01–5.28** | 有效 |
| 20D收益 <0 | 事件前 | 6.27% | 3.71% | 1.71 | 0.96–3.02 | 有方向，未过95% CI |
| 20D波动率 ≥7.50% | 事件前 | 4.69% | 5.99% | 0.77 | 0.46–1.31 | 无效 |
| 正式开盘 Gap ≥100% | 开盘后 | **18.55%** | 1.91% | **11.49** | **6.43–20.54** | 最强确认 |
| RV20 ≥10x | 收盘后 | 5.36% | 4.68% | 1.12 | 0.58–2.16 | 区分度低 |

命中率是条件样本统计，不是任意盘前个股的直接上涨概率。

## 4. 两种路径

### 常规 gap squeeze

```text
official_gap >= 100%
```

这是最强事件日确认，但必须使用正式开盘价。盘前价格达到 `+100%` 只能标记为“等待开盘”。

### CPHI subtype

```text
official_gap < 20%
AND early_regular_volume / verified_float >= 1.00
AND price remains above VWAP
AND supply turnover continues expanding
AND prior abnormal-volume warm-up exists
AND spread <= 2.50%
AND first_5m_structure == confirmed
AND dilution_overhang == false
```

CPHI 截图事件的估算特征：

```text
Gap = -5.49%
R_high = 1,169.23%
volume = 55.18m
turnover_total ~= 1.36x
turnover_vendor_float ~= 3.35x
```

该子类在 `Gap<20%` 的433个控制事件中仅有12个触发 `+500%` 高点，命中率2.77%。必须独立建模。

## 5. 供应结构

候选池硬门槛：

```text
0.30 <= prev_close <= 5.00
AND median_dollar_volume_20 <= 1,000,000
AND (verified_float <= 15,000,000 OR total_shares <= 10,000,000)
```

没有稳定的全市场 point-in-time free float 免费源。若用：

```text
implied_total_shares = market_cap / price
```

只可作为总股数代理。必须进一步检查 SEC 文件中的 outstanding shares、ADS ratio、registered resale、convertible securities、ATM 和 warrants。

Post-split 低流通盘是常见结构，但 split effective date 当日价格与成交量易被复权污染。当日 split 直接排除；近期 split 则单独标记。

## 6. 执行指标

输入CSV/JSON支持以下字段；只有 `symbol` 必填，其他缺失字段输出 `UNKNOWN`。

| 字段 | 单位/类型 | 说明 |
|---|---|---|
| symbol | string | ticker |
| timestamp | string | 数据时间戳 |
| market_status | string | Pre-Market/Open/Closed |
| security_type | string | 证券类型 |
| listed_days | int | 已上市交易日 |
| prev_close | USD | 前收盘价 |
| pre_price | USD | 当前盘前价 |
| pre_high | USD | 盘前最高价 |
| pre_volume | shares | 盘前成交量 |
| bid, ask | USD | 买卖报价 |
| market_cap | USD | 当前市值 |
| total_shares | shares | 总股本 |
| float_shares | shares | 可流通股本 |
| median_dollar_volume_20 | USD | 20日中位成交额 |
| avg_volume_20 | shares | 20日平均成交量 |
| pre_return_20d_pct | percent | 事件前20日收益 |
| split_today | bool | 当日是否生效拆股 |
| post_split | bool | 是否属于近期反向拆股结构；只标记风险，不自动排除 |
| last_split_date | date | 最近拆股日期 |
| dilution_overhang | bool/string | 潜在稀释风险 |
| premarket_supply_risk | bool/string | 盘前消息与最新正式文件是否确认存在当前事件窗口的新增/可售股份风险 |
| supply_risk_type | string | `ACTIVE_ATM`、`OFFERING`、`REGISTERED_RESALE`、`PIPE_EQUITY_LINE`、`WARRANT`、`CONVERTIBLE`、`UNLOCK` 或 `OTHER` |
| supply_risk_source | string | SEC filing、交易所公告或发行人正式公告的链接/编号 |
| supply_risk_checked_at | datetime | 供给风险核验时间，需带时区 |
| halted | bool | 当前是否停牌；为真时禁止输出 `EXECUTE` |
| open_price | USD | 正式开盘价 |
| last_price | USD | 当前常规时段价格 |
| regular_volume | shares | 常规时段累计量 |
| vwap | USD | 常规时段 VWAP |
| first_5m_structure | string | `confirmed`/`failed`，第一根5分钟结构 |
| prior_abnormal_volume_warmup | bool | CPHI路径是否存在事件前异常量预热 |
| turnover_expanding | bool | 开盘后供应周转是否持续扩张 |
| catalyst | string | 催化说明 |

布尔值支持 `true/false`, `yes/no`, `1/0`, `是/否`。

评分脚本只输出 `EXECUTE`、`WAIT_OPEN`、`WAIT_DATA`、`WATCH`、`EXCLUDE`。JSON额外返回 `path_type` 和 `risk_flags`；`evidence_score` 只表示证据完整度与强度，不是概率。

供给风险是硬门控：`premarket_supply_risk=true` 或旧字段 `dilution_overhang=true`
时直接 `EXCLUDE`；核验结果为 `UNKNOWN` 时输出 `WAIT_DATA`。单独存在 shelf registration
但无法确认 takedown 时保持 `UNKNOWN`，不得把融资容量等同于已经发行，也不得据此判定
风险已经解除。

## 7. 局限

- 当前上市证券池存在 survivorship bias，历史退市股票可能漏样。
- 发现事件要求收盘涨幅至少50%，盘中上涨500%后完全回落的事件可能漏样。
- 这是 public-source event study，不是 CRSP/TAQ 级研究。
- 盘前成交、奇异打印、halt、LULD、borrow availability 和 slippage 不在日线回测中。
- 所有阈值用于筛选与执行纪律，不构成收益保证。

## 8. 基础数据来源

- Nasdaq Stock Screener API：https://api.nasdaq.com/api/screener/stocks
- Nasdaq company actions：https://www.nasdaqtrader.com/Trader.aspx?id=CorpActions
- SEC EDGAR：https://www.sec.gov/edgar/search/
- Yahoo Finance Chart/Spark：https://finance.yahoo.com/
