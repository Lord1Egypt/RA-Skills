---
name: organizze
description: >-
  Runs Organizze personal finance API operations via Node.js CLI scripts:
  accounts, categories, transactions (filters, tag grouping), credit cards
  (invoices, payments), and transfers. Use when the user works with Organizze,
  budgets, expenses, income, categories, bank accounts, credit card bills,
  transfers, or asks to query or change their Organizze data through the terminal.
version: 1.3.4
metadata:
  openclaw:
    requires:
      env:
        - ORGANIZZE_TOKEN
        - ORGANIZZE_EMAIL
        - ORGANIZZE_USER_AGENT
      bins:
        - node
        - npm
    primaryEnv: ORGANIZZE_TOKEN
credentials:
  - name: ORGANIZZE_TOKEN
    description: API token for authenticating with the Organizze REST API (used as HTTP Basic Auth password)
    required: true
env:
  - name: ORGANIZZE_EMAIL
    description: Email address associated with the Organizze account (used as HTTP Basic Auth username)
    required: true
  - name: ORGANIZZE_USER_AGENT
    description: Short string identifying the integration, required by the Organizze API
    required: true
---

# Organizze API (CLI scripts)

Use the **organizze-skill** repository to read and write Organizze personal finance data through the official REST API. JSON is printed to stdout; errors go to stderr and the process exits non-zero on failure.

## Before running anything

Check whether the required credentials are available:

```bash
[[ -n "${ORGANIZZE_TOKEN:-}" && -n "${ORGANIZZE_EMAIL:-}" && -n "${ORGANIZZE_USER_AGENT:-}" ]] && echo "READY" || echo "MISSING"
```

- If the output is `MISSING`: stop and guide the user through setup below. Do NOT proceed until all variables are set.
- If the output is `READY`: proceed.

### Setup guidance (show this when MISSING)

Tell the user they have two options:

**Option 1 (recommended) — OpenClaw UI:**
Open the OpenClaw UI, go to **Skills → organizze**, enter the API token in the **API key** field, and click **Save key**. Then set `ORGANIZZE_EMAIL` and `ORGANIZZE_USER_AGENT` as environment variables in the skill's env section.

**Option 2 — Edit `~/.openclaw/openclaw.json` directly (for CLI users):**

```json
{
  "skills": {
    "entries": {
      "organizze": {
        "enabled": true,
        "apiKey": "<your-organizze-token>",
        "env": {
          "ORGANIZZE_EMAIL": "your@email.com",
          "ORGANIZZE_USER_AGENT": "my-organizze-skill"
        }
      }
    }
  }
}
```

The gateway picks up the change automatically — no restart needed.

The user can get their API token from the Organizze web app under **Configurações → Integrações → Token de API**.

## Working directory

**Before every `node` command, set the shell working directory to the repository root** — the directory that contains `package.json`.

## Prerequisites

- Node.js 18 or newer
- From the repository root: `npm install`
- A `.env` file (copy from `.env.example`) with:
  - `ORGANIZZE_EMAIL`
  - `ORGANIZZE_TOKEN`
  - `ORGANIZZE_USER_AGENT` (required by the API; any short string identifying your integration)

Do not print or log credential values. Mask PII when summarizing API output for the user.

## How to run

```bash
node src/routes/<resource>.js <action> [args]
```

`<resource>` is one of: `accounts`, `categories`, `transactions`, `credit-cards`, `transfers`.

Run a script with no arguments to see its full usage on stderr.

**Output:** pretty-printed JSON on stdout. **Errors:** message on stderr, exit `1`.

---

## Conventions

- **`amount_cents`:** integer cents. R$ 50.00 = `5000`. Expenses are negative.
- **Dates:** `YYYY-MM-DD`.
- **JSON arguments:** pass as a single quoted shell argument.
- **`transactions list --group-by-tag`:** local grouping after the API response (not a native API feature). Returns `[{ tag, total_cents, transactions }]`. Transactions with multiple tags appear in each group; untagged ones go into `"untagged"`.
- **`transfers list`:** returns two entries per transfer (debit and credit sides), not one merged object.

For field names and payloads not listed here, see: https://github.com/organizze/api-doc

---

## accounts

| Action   | Arguments |
|----------|-----------|
| `list`   | (none) |
| `get`    | `<id>` |
| `create` | `<json>` |
| `update` | `<id>` `<json>` |
| `delete` | `<id>` |

```bash
node src/routes/accounts.js list
node src/routes/accounts.js get 12345
```

---

## categories

| Action   | Arguments |
|----------|-----------|
| `list`   | (none) |
| `get`    | `<id>` |
| `create` | `<json>` |
| `update` | `<id>` `<json>` |
| `delete` | `<id>` `[json]` |

`delete` accepts optional JSON with `replacement_id` to migrate existing references before removal.

```bash
node src/routes/categories.js list
node src/routes/categories.js delete 42 '{"replacement_id":18}'
```

---

## transactions

| Action   | Arguments |
|----------|-----------|
| `list`   | Optional flags: `--start-date=YYYY-MM-DD`, `--end-date=YYYY-MM-DD`, `--account-id=<id>`, `--group-by-tag` |
| `get`    | `<id>` |
| `create` | `<json>` |
| `update` | `<id>` `<json>` |
| `delete` | `<id>` `[json]` |

`delete` accepts optional JSON for recurring/installment behavior: `'{"update_future":true}'` or `'{"update_all":true}'`.

```bash
node src/routes/transactions.js list --start-date=2025-04-01 --end-date=2025-04-30
node src/routes/transactions.js list --account-id=1 --group-by-tag
node src/routes/transactions.js delete 888 '{"update_future":true}'
```

---

## credit-cards

| Action           | Arguments |
|------------------|-----------|
| `list`           | (none) |
| `get`            | `<id>` |
| `create`         | `<json>` |
| `update`         | `<id>` `<json>` |
| `delete`         | `<id>` |
| `list-invoices`  | `<credit_card_id>` optional `--start-date=...` `--end-date=...` |
| `get-invoice`    | `<credit_card_id>` `<invoice_id>` |
| `get-payments`   | `<credit_card_id>` `<invoice_id>` |

```bash
node src/routes/credit-cards.js list
node src/routes/credit-cards.js list-invoices 3 --start-date=2025-01-01 --end-date=2025-12-31
node src/routes/credit-cards.js get-payments 3 1001
```

---

## transfers

| Action   | Arguments |
|----------|-----------|
| `list`   | Optional `--start-date=YYYY-MM-DD` `--end-date=YYYY-MM-DD` |
| `get`    | `<id>` |
| `create` | `<json>` |
| `update` | `<id>` `<json>` |
| `delete` | `<id>` |

Typical `create` fields: `credit_account_id`, `debit_account_id`, `amount_cents`, `date`, `paid`. Confirm exact shape via the API doc or by inspecting existing transfers.

```bash
node src/routes/transfers.js list --start-date=2025-04-01 --end-date=2025-04-30
node src/routes/transfers.js get 55
```

---

## End-to-end workflows

### Balances

```bash
node src/routes/accounts.js list
```

### Transactions for a period, filtered by account

```bash
# 1. get account id
node src/routes/accounts.js list

# 2. list transactions
node src/routes/transactions.js list --start-date=2025-04-01 --end-date=2025-04-30 --account-id=1
```

### Create an expense

```bash
node src/routes/transactions.js create \
  '{"description":"Coffee","amount_cents":-1500,"date":"2025-04-03","category_id":10,"account_id":1}'
```

Use negative `amount_cents`. Get `category_id` and `account_id` from prior `list` calls. Adjust fields to match the API.

### Spending by tag

```bash
node src/routes/transactions.js list --start-date=2025-04-01 --end-date=2025-04-30 --group-by-tag
```

Each group in the result has `tag` and `total_cents`.
