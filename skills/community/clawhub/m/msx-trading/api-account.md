# Module: Account & Portfolio

**When to load this file:** User asks about their account info, cash balance, holdings, or portfolio value.

Trigger phrases: "余额", "持仓", "账户", "组合", "资产", "balance", "portfolio", "positions"

---

## GET /account/profile

Returns basic account information.

**Request**
```
GET /account/profile
X-API-KEY: {MSX_API_KEY}
```

**Response**
```json
{
  "user_id": "U123456",
  "name": "Zhang San",
  "status": "active",
  "kyc_level": 2,
  "registered_at": "2024-01-15T08:00:00Z"
}
```

---

## GET /account/balance

Returns the user's current cash balance.

**Request**
```
GET /account/balance
X-API-KEY: {MSX_API_KEY}
```

**Response**
```json
{
  "currency": "USD",
  "available": 15000.00,
  "frozen": 2500.00,
  "total": 17500.00
}
```

Field notes:
- `available` — cash free to use for new orders
- `frozen` — cash locked in pending orders
- `total` — available + frozen

---

## GET /account/positions

Returns all currently held security tokens.

**Request**
```
GET /account/positions
X-API-KEY: {MSX_API_KEY}
```

**Response**
```json
{
  "positions": [
    {
      "symbol": "TOKEN-AAPL",
      "name": "Apple Inc. Token",
      "quantity": 50,
      "avg_cost": 182.30,
      "current_price": 195.00,
      "market_value": 9750.00,
      "unrealized_pnl": 635.00,
      "unrealized_pnl_pct": 6.97
    }
  ],
  "total_market_value": 9750.00,
  "total_unrealized_pnl": 635.00
}
```

**Display format:** Present as a table when multiple positions exist.

| Symbol | Qty | Avg Cost | Current Price | Market Value | P&L |
|--------|-----|----------|---------------|--------------|-----|
| TOKEN-AAPL | 50 | 182.30 | 195.00 | 9,750.00 | +635.00 (6.97%) |
