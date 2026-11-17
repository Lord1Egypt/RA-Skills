# 持仓与同步

## 选路

- “今天收益、总资产、持有收益”：先用 `get_summary`。
- 需要逐只基金、观察列表或完整度：用 `get_records(include_transactions=false)`。
- 只有审计单只/少量交易时才用 `get_transactions(code=...)` 或分页 `get_transaction_ledger`。
- 判断 App 数据是否已同步：先用 `get_sync_meta`，不要为检查时间下载完整主数据。
- 完整主数据迁移或审计：使用 `huahua export portfolio`，不要把 `get_raw_sync_data(include_json_text=true)` 的大包放进模型上下文。
- 分组、标签和策略偏好使用对应读取工具；core 优先 `get_portfolio_preferences`。

## 新鲜度与完整度

- 组合新鲜度只看 `portfolioUpdatedAt`；payload 内的 `timestamp` 可能是客户端谱系或迁移元数据。
- `summary.estimateCompleteness.complete=false` 时，不把不可用帧产生的 0 元当成真实零涨跌。
- `timeoutCount`、`staleCount`、`partialCount` 或 unavailable codes 非空时披露不完整。
- `marketValue` 使用官方净值锚点；`estimatedMarketValue` 是独立估算，不能混为官方市值。
- 最新 QDII 收益没有可靠 G 日时保持未归属，不回退到 D 日。

## 数据最小化

- 默认不带原始 transactions；只有复盘、核账或用户明确要求时开启。
- 用户只问汇总时不要拉完整持仓和历史。
- 账本已有 cursor/limit，连续读取时遵循 `nextCursor`，不要一次请求最大值作为默认。
