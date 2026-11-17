# 量化、回放与快照

## 策略上下文

- 默认调用 `get_quant_strategy_context(view="compact")`。
- 综合持仓分析只调用一次 compact 策略上下文；它已包含持仓、市场、基金指标、执行窗口和数据质量，不再串行调用 `get_records`、`get_overview` 或逐基金量化工具重复取数。
- 先检查 `readyForAnalysis`、`readyForAction`、`blockingReasons` 和 `dataQuality`，再生成结论。
- `dataQuality.fundOfficialNavFreshness.retryAfterMs` 存在且仍不完整时，按该间隔有界重取，最多 3 次；重取后必须重新检查完整度。
- full view 只在 compact 缺少当前分析所需证据时使用。

## 历史与组合

- 交易账本使用分页和过滤条件。
- 组合净值、回撤与交易复盘必须使用后端统一 G 日口径。
- 批量基金净值是官方 D 日数据库快照；`freshnessMode=unchecked_db_snapshot` 表示未核验当前公布进度，`complete` 只说明请求区间边界覆盖，不能证明已更新到最新。当前量化分析使用基金量化工具的新鲜度契约。
- 当前区间的组合净值必须检查 `navFreshness`；存在 `retryAfterMs` 时按该间隔有界重取，最多 3 次。
- 长区间完整净值导出走 `huahua export nav-history`。

## 回测

- 回测信号只能使用当时已可获得的数据；不能同日使用未来公布净值成交。
- 检查完整度、覆盖率、基准和方法版本，不把零费率或非严格 point-in-time 结果描述成真实可实现收益。
- `client_run_id` 在同一次回测重试中保持稳定。

## 快照

- 快照只归档观察和证据，不直接交易，也不保存建议金额。
- 写入前确认 data cutoff、策略 ID/版本和 risk veto。
- 保存重试使用稳定 snapshot key；读取列表使用分页，详情按 ID 获取。
