# JSON Schemas for Bulk Operations

## Accounts bulk-upsert

File format for `ledgi accounts bulk-upsert --file <path>`:

```json
{
  "accounts": [
    {
      "external_id": "monzo-current",
      "name": "Monzo Current Account",
      "type": "current",
      "balance": 2500.00,
      "currency": "GBP",
      "institution": "Monzo"
    },
    {
      "external_id": "vanguard-isa",
      "name": "Vanguard S&S ISA",
      "type": "isa_stocks",
      "balance": 20000.00,
      "currency": "GBP",
      "institution": "Vanguard"
    },
    {
      "external_id": "workplace-pension",
      "name": "Workplace Pension",
      "type": "pension_workplace",
      "balance": 45000.00,
      "currency": "GBP",
      "institution": "Aviva"
    }
  ]
}
```

### Account fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `external_id` | Yes | string | Unique identifier for idempotent upserts. Same external_id = update, new = create. |
| `name` | Yes | string | Display name for the account |
| `type` | Yes | string | Account type (see valid types below) |
| `balance` | No | number | Account balance (default: 0) |
| `currency` | No | string | ISO currency code (default: "GBP") |
| `institution` | No | string | Financial institution name |

### Valid account types

```
cash, current, savings, premium_bonds,
isa_cash, isa_stocks, isa_lifetime, isa_innovative,
pension, pension_workplace, pension_sipp, pension_state,
investment, crypto_wallet,
property,
credit_card, loan, mortgage, student_loan,
other_asset, other_liability
```

## Holdings bulk-upsert

File format for `ledgi holdings bulk-upsert --file <path>`:

```json
{
  "holdings": [
    {
      "external_id": "vusa-holding",
      "account_external_id": "vanguard-isa",
      "symbol": "VUSA",
      "name": "Vanguard S&P 500 ETF",
      "type": "etf",
      "quantity": 50.0,
      "average_cost": 65.00,
      "currency": "GBP"
    },
    {
      "external_id": "btc-holding",
      "account_external_id": "crypto-wallet-1",
      "symbol": "BTC",
      "name": "Bitcoin",
      "type": "crypto",
      "quantity": 0.5,
      "average_cost": 25000.00,
      "currency": "GBP"
    }
  ]
}
```

### Holding fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `external_id` | Yes | string | Unique identifier for idempotent upserts |
| `account_external_id` | Yes | string | The `external_id` of the parent account. The account must already exist. |
| `symbol` | Yes | string | Ticker symbol (e.g. VUSA, AAPL, BTC) |
| `name` | Yes | string | Display name |
| `type` | Yes | string | Holding type: `stock`, `etf`, `crypto`, `fund`, `bond`, `other` |
| `quantity` | Yes | number | Number of units held |
| `average_cost` | No | number | Average cost per unit (default: 0) |
| `currency` | No | string | ISO currency code (default: "GBP") |

### Important notes

- `account_external_id` references the parent account by its `external_id`, not its Ledgi internal ID. The account must be created first.
- Maximum 100 items per request.
- If an item with the same `external_id` exists, it will be updated. Otherwise, a new one is created.
