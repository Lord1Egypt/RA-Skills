# Portfolio JSON 格式定义

文件路径：`~/polymarket-reports/portfolio.json`

## 顶层结构

```json
{
  "created_at": "ISO 8601 时间戳",
  "updated_at": "ISO 8601 时间戳",
  "mode": "paper | live",
  "initial_capital": 10000,
  "cash_balance": 9500.00,
  "positions": [],
  "pending_orders": [],
  "settled_trades": [],
  "trade_history": []
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| created_at | string | 组合创建时间 (UTC ISO 8601) |
| updated_at | string | 最后更新时间 |
| mode | string | `paper` 或 `live` |
| initial_capital | number | 初始资金 (USD) |
| cash_balance | number | 当前可用现金 |
| positions | array | 活跃持仓 |
| pending_orders | array | 未成交限价单 |
| settled_trades | array | 已结算交易 |
| trade_history | array | 所有交易操作日志 |

## positions 条目

```json
{
  "id": "pos_001",
  "market_id": "Gamma API market ID",
  "question": "市场问题文本",
  "event_slug": "event-slug-for-url",
  "direction": "Yes | No",
  "entry_price": 0.068,
  "shares": 735,
  "cost_basis": 49.98,
  "entry_date": "2026-02-24",
  "source_report": "market-pulse-2026-02-24-040000.md",
  "order_type": "market | limit",
  "clob_token_id": "CLOB token ID for this direction",
  "edge_at_entry": 0.284,
  "confidence": "高 | 中高 | 中 | 低",
  "end_date": "2026-02-28T00:00:00Z"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 唯一标识 `pos_NNN` |
| market_id | string | Gamma API 市场 ID |
| question | string | 市场问题 |
| event_slug | string | 事件 slug（用于构造 URL） |
| direction | string | 买入方向 Yes 或 No |
| entry_price | number | 成交价格（每份） |
| shares | number | 持有份数 |
| cost_basis | number | 总成本 = entry_price × shares |
| entry_date | string | 建仓日期 |
| source_report | string | 来源 pulse 报告文件名 |
| order_type | string | 下单方式 |
| clob_token_id | string | CLOB 代币 ID |
| edge_at_entry | number | 建仓时的 Edge 值（小数） |
| confidence | string | 建仓时的置信度 |
| end_date | string | 市场结算日期（用于判断结算） |

## pending_orders 条目

```json
{
  "id": "ord_001",
  "market_id": "Gamma API market ID",
  "question": "市场问题文本",
  "event_slug": "event-slug-for-url",
  "direction": "Yes | No",
  "limit_price": 0.14,
  "shares": 1428,
  "cost_reserved": 199.92,
  "created_at": "2026-02-24T04:10:00Z",
  "source_report": "market-pulse-2026-02-24-040000.md",
  "clob_token_id": "CLOB token ID",
  "edge_at_entry": 0.14,
  "confidence": "中",
  "end_date": "2026-11-03T00:00:00Z",
  "real_order_id": null
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 唯一标识 `ord_NNN` |
| limit_price | number | 限价价格 |
| cost_reserved | number | 冻结资金 = limit_price × shares |
| real_order_id | string/null | 实盘模式的 CLOB 订单 ID |

其余字段同 positions。

## settled_trades 条目

```json
{
  "id": "pos_001",
  "question": "市场问题文本",
  "event_slug": "event-slug-for-url",
  "direction": "No",
  "entry_price": 0.068,
  "exit_price": 1.0,
  "shares": 735,
  "cost_basis": 49.98,
  "revenue": 735.00,
  "pnl": 685.02,
  "pnl_pct": 1370.8,
  "settled_at": "2026-02-28T00:00:00Z",
  "outcome": "win | loss",
  "edge_at_entry": 0.284,
  "actual_result": "No",
  "holding_days": 4
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| exit_price | number | 结算价格（1.0 赢 / 0.0 输） |
| revenue | number | 收回金额 = shares × exit_price |
| pnl | number | 净损益 = revenue - cost_basis |
| pnl_pct | number | 百分比收益 = pnl / cost_basis × 100 |
| outcome | string | `win` 或 `loss` |
| actual_result | string | 市场实际结果（Yes/No） |
| holding_days | number | 持有天数 |

## trade_history 条目

每次操作的完整日志：

```json
{
  "timestamp": "2026-02-24T04:10:00Z",
  "action": "open_position | close_position | place_order | fill_order | cancel_order",
  "position_id": "pos_001",
  "details": {
    "market": "...",
    "direction": "No",
    "price": 0.068,
    "shares": 735,
    "amount": 49.98
  }
}
```

## ID 生成规则

- 持仓 ID：`pos_NNN`，NNN 为从 001 开始的自增序号（基于已有最大 ID）
- 订单 ID：`ord_NNN`，同上
- 查找当前最大 ID：遍历 positions + settled_trades（或 pending_orders），取最大序号 + 1
