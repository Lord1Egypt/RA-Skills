---
name: ledgi
description: Interact with the user's Ledgi personal finance data. Use when the user asks about their accounts, balances, net worth, holdings, investments, ISA allowances, pensions, snapshots, or wants to add/update financial data.
allowed-tools: Bash(ledgi *), Bash(echo *), Write
---

# Ledgi CLI Skill

You can interact with the user's Ledgi personal finance tracker using the `ledgi` CLI. All financial data is accessed through the Ledgi Agent API.

## Prerequisites

- The `ledgi` CLI must be installed. If not, install with:
  ```bash
  curl -fsSL https://raw.githubusercontent.com/LedgiApp/ledgi-cli/main/install.sh | bash
  ```
- The `LEDGI_API_KEY` environment variable must be set, or the user must have run `ledgi login --api-key ledgi_sk_...`

If a command fails with an auth error, ask the user to set their API key.

## Core workflows

### Read financial data

```bash
ledgi accounts list                    # All accounts
ledgi accounts list --type isa_stocks  # Filter by type
ledgi holdings list                    # All investment holdings
ledgi holdings list --account-id ID    # Holdings in one account
ledgi networth summary                 # Net worth breakdown
ledgi snapshots list                   # Historical snapshots
ledgi isa summary                      # ISA allowance and usage
```

All commands return JSON by default. Use `--output table` for human-readable output when displaying to the user.

### Create or update accounts

For a single account:
```bash
ledgi accounts upsert --name "Monzo Current" --type current --balance 2500 --currency GBP --institution Monzo
```

For multiple accounts, write a JSON file then bulk-upsert:
```bash
ledgi accounts bulk-upsert --file /tmp/accounts.json
```

See [schemas.md](schemas.md) for JSON file formats.

### Create or update holdings

Write a JSON file then bulk-upsert:
```bash
ledgi holdings bulk-upsert --file /tmp/holdings.json
```

### Take a net worth snapshot

```bash
ledgi snapshots create
ledgi snapshots create --date 2026-01-31
```

### Log an ISA deposit

```bash
ledgi isa deposit --account-id ACCOUNT_ID --amount 5000 --date 2026-02-24
```

## Valid account types

Use these exact values for the `--type` flag:

- **Cash**: `cash`, `current`, `savings`, `premium_bonds`
- **ISA**: `isa_cash`, `isa_stocks`, `isa_lifetime`, `isa_innovative`
- **Pension**: `pension`, `pension_workplace`, `pension_sipp`, `pension_state`
- **Investment**: `investment`, `crypto_wallet`
- **Property**: `property`
- **Debt**: `credit_card`, `loan`, `mortgage`, `student_loan`
- **Other**: `other_asset`, `other_liability`

## Error handling

- **401 Unauthorized**: API key is missing or invalid. Ask the user to check their key.
- **403 Forbidden**: The API key doesn't have the required scope. Tell the user which scope is needed.
- **404 Not Found**: The referenced resource doesn't exist.
- **422 Validation Error**: Invalid input. Check the account type or required fields.

## Important notes

- Always use `--output table` when showing results to the user for readability.
- When creating accounts, include `--external-id` for idempotency so re-running won't create duplicates.
- Monetary values are in the account's currency (default GBP).
- The `--date` flag uses `YYYY-MM-DD` format.

For full command reference, see [commands.md](commands.md).
For JSON file schemas, see [schemas.md](schemas.md).
