# Module: Trade History & Reports

**When to load this file:** User asks about past trades, historical orders, or fund deposit/withdrawal records.

Trigger phrases: "history", "report", "transactions", "past trades", "历史", "记录", "报表", "成交", "流水"

---

## GET /trades/history — Executed trade history

Returns a list of all completed fills (actual executions).

**Request**
```
GET /trades/history
X-API-KEY: {MSX_API_KEY}
```

**Query params**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| symbol | string | No | Filter by token symbol |
| from | string | No | Start date, ISO 8601 format: `2025-01-01T00:00:00Z` |
| to | string | No | End date, ISO 8601 format |
| limit | integer | No | Max records to return. Default: `50`, max: `500` |

**Response**
```json
{
  "trades": [
    {
      "trade_id": "TRD-20250324-001",
      "order_id": "ORD-20250324-005",
      "symbol": "TOKEN-AAPL",
      "side": "buy",
      "quantity": 60,
      "price": 194.45,
      "fee": 1.17,
      "fee_currency": "USD",
      "executed_at": "2025-03-24T09:36:00Z"
    }
  ],
  "total": 1
}
```

---

## GET /orders/history — Historical orders

Returns all past orders regardless of status (filled, cancelled, rejected).

**Request**
```
GET /orders/history
X-API-KEY: {MSX_API_KEY}
```

**Query params**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| status | string | No | `filled`, `cancelled`, `rejected`, or `all`. Default: `all` |
| symbol | string | No | Filter by token symbol |
| from | string | No | Start date, ISO 8601 |
| to | string | No | End date, ISO 8601 |
| limit | integer | No | Default: `50`, max: `500` |

**Response**
```json
{
  "orders": [
    {
      "order_id": "ORD-20250324-005",
      "symbol": "TOKEN-AAPL",
      "side": "buy",
      "type": "limit",
      "quantity": 100,
      "filled_quantity": 100,
      "avg_fill_price": 194.48,
      "status": "filled",
      "created_at": "2025-03-24T09:35:00Z",
      "updated_at": "2025-03-24T09:37:00Z"
    }
  ],
  "total": 1
}
```

---

## GET /account/transactions — Fund transaction history

Returns cash flow records: deposits, withdrawals, trade settlements, and fees.

**Request**
```
GET /account/transactions
X-API-KEY: {MSX_API_KEY}
```

**Query params**

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| type | string | No | `deposit`, `withdrawal`, `trade`, `fee`, or `all`. Default: `all` |
| from | string | No | Start date, ISO 8601 |
| to | string | No | End date, ISO 8601 |
| limit | integer | No | Default: `50`, max: `500` |

**Response**
```json
{
  "transactions": [
    {
      "tx_id": "TX-20250320-001",
      "type": "deposit",
      "amount": 10000.00,
      "currency": "USD",
      "balance_after": 25000.00,
      "description": "Bank wire deposit",
      "created_at": "2025-03-20T08:00:00Z"
    },
    {
      "tx_id": "TX-20250324-010",
      "type": "trade",
      "amount": -11668.80,
      "currency": "USD",
      "balance_after": 13331.20,
      "description": "Buy 60 TOKEN-AAPL @ 194.45 + fee 1.17",
      "created_at": "2025-03-24T09:36:00Z"
    }
  ],
  "total": 2
}
```

**Display guidance:**
- Default to last 30 days if user doesn't specify a date range.
- Positive `amount` = money in (deposit, sell proceeds).
- Negative `amount` = money out (withdrawal, buy payment, fee).
- Present as a table sorted by `created_at` descending.
