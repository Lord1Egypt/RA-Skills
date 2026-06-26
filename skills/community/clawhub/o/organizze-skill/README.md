# Organizze Skill

![Node.js](https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen)
[![The Claw is The law](https://img.shields.io/badge/%F0%9F%A6%9E-The%20Claw%20is%20The%20law-2ea44f?style=flat-square)](https://clawhub.ai/leaofelipe/organizze-skill)

[ClawHub — organizze-skill](https://clawhub.ai/leaofelipe/organizze-skill)

Node.js scripts to interact with the [Organizze API](https://github.com/organizze/api-doc). Each resource has its own script executable directly from the terminal.

## Requirements

- Node.js >= 18.0.0
- An [Organizze](https://app.organizze.com.br) account with an API token

## Configuration

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
ORGANIZZE_EMAIL=your@email.com
ORGANIZZE_TOKEN=your_access_token
ORGANIZZE_USER_AGENT=organizze-skill (your@email.com)
```

Your API token is available at [app.organizze.com.br/configuracoes/api-keys](https://app.organizze.com.br/configuracoes/api-keys).

## Usage

### Accounts

```bash
node src/routes/accounts.js list
node src/routes/accounts.js get <id>
node src/routes/accounts.js create '{"name":"Itau CC","type":"checking"}'
node src/routes/accounts.js update <id> '{"name":"Itau Savings"}'
node src/routes/accounts.js delete <id>
```

### Categories

```bash
node src/routes/categories.js list
node src/routes/categories.js get <id>
node src/routes/categories.js create '{"name":"Groceries"}'
node src/routes/categories.js update <id> '{"name":"Supermarket"}'
node src/routes/categories.js delete <id>
node src/routes/categories.js delete <id> '{"replacement_id":5}'
```

### Transactions

```bash
node src/routes/transactions.js list
node src/routes/transactions.js list --start-date=2026-04-01 --end-date=2026-04-30
node src/routes/transactions.js list --account-id=<id>
node src/routes/transactions.js get <id>
node src/routes/transactions.js create '{"description":"Supermarket","amount_cents":-5000,"date":"2026-04-03","paid":true}'
node src/routes/transactions.js update <id> '{"description":"Updated description"}'
node src/routes/transactions.js delete <id>
node src/routes/transactions.js delete <id> '{"update_future":true}'
# extra: not a native Organizze API feature
node src/routes/transactions.js list --group-by-tag
node src/routes/transactions.js list --start-date=2026-04-01 --end-date=2026-04-30 --group-by-tag
# a transaction with multiple tags appears in each matching group
```

### Credit Cards

```bash
node src/routes/credit-cards.js list
node src/routes/credit-cards.js get <id>
node src/routes/credit-cards.js create '{"name":"Nubank","due_day":10,"closing_day":3,"limit_cents":500000}'
node src/routes/credit-cards.js update <id> '{"name":"Nubank Black"}'
node src/routes/credit-cards.js delete <id>
node src/routes/credit-cards.js list-invoices <credit_card_id>
node src/routes/credit-cards.js list-invoices <credit_card_id> --start-date=2026-01-01 --end-date=2026-12-31
node src/routes/credit-cards.js get-invoice <credit_card_id> <invoice_id>
node src/routes/credit-cards.js get-payments <credit_card_id> <invoice_id>
```

### Transfers

> `list` returns both sides of each transfer as separate transaction objects (debit and credit).

```bash
node src/routes/transfers.js list
node src/routes/transfers.js list --start-date=2026-04-01 --end-date=2026-04-30
node src/routes/transfers.js get <id>
node src/routes/transfers.js create '{"credit_account_id":3,"debit_account_id":4,"amount_cents":10000,"date":"2026-04-03","paid":true}'
node src/routes/transfers.js update <id> '{"description":"Adjusted transfer"}'
node src/routes/transfers.js delete <id>
```

## Structure

```
src/
├── client.js          # HTTP client (auth, headers, error handling)
└── routes/
    ├── accounts.js
    ├── categories.js
    ├── transactions.js
    ├── credit-cards.js
    └── transfers.js
```

Each module in `src/routes/` works in two modes:

- **CLI** — run directly with `node src/routes/<resource>.js <action> [args]`
- **Module** — imported in other scripts via `import { listAccounts } from './src/routes/accounts.js'`

Output is always JSON on stdout. Errors go to stderr with exit code 1.
