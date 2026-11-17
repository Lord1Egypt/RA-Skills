# 基金与市场

## 基金识别

- 用户提供 6 位代码：直接调用对应批量或单只工具。
- 用户只提供名称：先 `search_item`；多个候选时向用户轻确认。
- 多只基金优先批量工具，避免逐只循环。

## 常用能力

- 当前估值：`get_item_estimate`。
- 画像、费率、周期排名、量化指标：优先批量版本。
- 市场概览：`get_overview`；只需要交易状态时用 `get_status`。
- 指数/ETF：先 catalog，再 quotes；时间线和历史只在用户需要时读取。
- 资金流和板块：使用 fund flow、sector metrics 等有界工具，不把单一指标解释成确定交易信号。
- 交易日、确认日推导：使用 `calculate_trading_dates` / `get_next_trading_day`，不按自然日猜节假日。

## 数据表达

- 分时图可能追加同一交易会话的最新真实报价点，不保证等间隔。保留各点 time；latestQuote.stale / freshness=stale 表示旧帧，不能改成当前时间或当作实时行情。

- 明确区分官方净值、盘中估算和 QDII 夜盘参考。
- 夜盘只作执行参考，不是官方净值，也不是已确认收益。
- 技术指标数据不足、freshness 不可靠或 partial 时说明限制。
- 基金量化结果存在 `retryAfterMs` 且 complete=false、stale 或 computing 时，按该间隔有界重取，最多 3 次；仍不完整则披露补数状态。
- 用户问当前或刚刷新结果时，必须在当前轮重新调用工具，不复用早先上下文中的数据。
- 用户要完整长区间历史文件时使用 CLI export；普通分析使用 MCP 的范围参数。
