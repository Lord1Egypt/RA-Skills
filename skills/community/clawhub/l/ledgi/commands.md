# Ledgi CLI Command Reference

## Global flags

| Flag | Description |
|------|-------------|
| `--api-key` | Override API key for this request |
| `--api-url` | Override API URL |
| `--output` | Output format: `json` (default) or `table` |

## accounts list

List all active accounts.

**Scope**: `accounts:read`

```bash
ledgi accounts list
ledgi accounts list --type current
ledgi accounts list --type isa_stocks
ledgi --output table accounts list
```

| Flag | Description |
|------|-------------|
| `--type` | Filter by account type (e.g. `cash`, `isa_stocks`, `current`) |

**Example JSON output:**
```json
{
  "accounts": [
    {
      "id": "abc123",
      "name": "Monzo Current",
      "type": "current",
      "balance": 2500.00,
      "currency": "GBP",
      "institution": "Monzo",
      "external_id": "monzo-1",
      "is_liability": false,
      "include_in_net_worth": true
    }
  ]
}
```

## accounts upsert

Create or update a single account.

**Scope**: `accounts:write`

```bash
ledgi accounts upsert --name "Main Current" --type current --balance 2500
ledgi accounts upsert --name "Vanguard ISA" --type isa_stocks --balance 15000 --institution Vanguard --external-id vanguard-isa
ledgi accounts upsert --name "Amex" --type credit_card --balance 500 --institution "American Express"
```

| Flag | Required | Description |
|------|----------|-------------|
| `--name` | Yes | Account name |
| `--type` | Yes | Account type (see valid types in SKILL.md) |
| `--balance` | No | Account balance (default: 0) |
| `--currency` | No | Currency code (default: GBP) |
| `--institution` | No | Institution name |
| `--external-id` | No | External ID for idempotent upserts. Auto-generated if omitted. |

## accounts bulk-upsert

Create or update multiple accounts from a JSON file.

**Scope**: `accounts:write`

```bash
ledgi accounts bulk-upsert --file /tmp/accounts.json
```

| Flag | Required | Description |
|------|----------|-------------|
| `--file` | Yes | Path to JSON file |

**Example output:**
```json
{
  "created": 2,
  "updated": 1
}
```

## holdings list

List all investment holdings.

**Scope**: `holdings:read`

```bash
ledgi holdings list
ledgi holdings list --account-id abc123
ledgi --output table holdings list
```

| Flag | Description |
|------|-------------|
| `--account-id` | Filter holdings by account ID |

**Example JSON output:**
```json
{
  "holdings": [
    {
      "id": "h123",
      "account_id": "abc123",
      "symbol": "VUSA",
      "name": "Vanguard S&P 500 ETF",
      "type": "etf",
      "quantity": 50.0,
      "average_cost": 65.00,
      "current_price": 72.50,
      "current_value": 3625.00,
      "currency": "GBP",
      "external_id": "vusa-holding"
    }
  ]
}
```

## holdings bulk-upsert

Create or update multiple holdings from a JSON file.

**Scope**: `holdings:write`

```bash
ledgi holdings bulk-upsert --file /tmp/holdings.json
```

| Flag | Required | Description |
|------|----------|-------------|
| `--file` | Yes | Path to JSON file |

## networth summary

Get net worth breakdown by asset category.

**Scope**: `networth:read`

```bash
ledgi networth summary
ledgi --output table networth summary
```

**Example JSON output:**
```json
{
  "total_net_worth": 125000.00,
  "total_assets": 150000.00,
  "total_liabilities": 25000.00,
  "breakdown": {
    "current": 5000.00,
    "isa_stocks": 20000.00,
    "pension_workplace": 45000.00,
    "investment": 30000.00,
    "property": 50000.00
  }
}
```

## snapshots list

List historical net worth snapshots.

**Scope**: `snapshots:read`

```bash
ledgi snapshots list
ledgi snapshots list --limit 5
```

| Flag | Description |
|------|-------------|
| `--limit` | Number of snapshots to return |

## snapshots create

Take a new net worth snapshot.

**Scope**: `snapshots:write`

```bash
ledgi snapshots create
ledgi snapshots create --date 2026-01-31
```

| Flag | Description |
|------|-------------|
| `--date` | Snapshot date in YYYY-MM-DD format (default: today) |

## isa summary

View ISA allowance usage for a tax year.

**Scope**: `isa:read`

```bash
ledgi isa summary
ledgi isa summary --tax-year 2025
```

| Flag | Description |
|------|-------------|
| `--tax-year` | Tax year (e.g. 2025 for 2025/26). Default: current tax year. |

## isa deposit

Log an ISA deposit.

**Scope**: `isa:write`

```bash
ledgi isa deposit --account-id abc123 --amount 5000 --date 2026-02-24
```

| Flag | Required | Description |
|------|----------|-------------|
| `--account-id` | Yes | ISA account ID |
| `--amount` | Yes | Deposit amount |
| `--date` | Yes | Deposit date (YYYY-MM-DD) |
