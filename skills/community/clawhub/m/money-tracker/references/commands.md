# money_tracker Commands

## Runtime

- Python: `3.9+`
- Dependencies: Python standard library only
- Default database path: `~/.money_tracker/bookkeeping.db`
- Runtime script: `{baseDir}/scripts/bookkeeping.py`
- Override order:
  1. `--db <path>`
  2. `MONEY_TRACKER_DB`
  3. `LOCAL_BOOKKEEPING_DB` (legacy compatibility)
  4. default home-directory path
- Day, week, month, and year reports do not perform FX conversion
- For extra prompt examples, see `{baseDir}/references/chat_reference.md`

## Command Summary

All commands print JSON with `ensure_ascii=False`.

### Initialize the database

Create the database file and schema at the resolved path:

```bash
python "{baseDir}/scripts/bookkeeping.py" init-db
python "{baseDir}/scripts/bookkeeping.py" --db ./my-bookkeeping.db init-db
```

### List categories

```bash
python "{baseDir}/scripts/bookkeeping.py" list-categories
python "{baseDir}/scripts/bookkeeping.py" list-categories --all
```

### List accounts

```bash
python "{baseDir}/scripts/bookkeeping.py" list-accounts
python "{baseDir}/scripts/bookkeeping.py" list-accounts --all
```

Default wallet accounts are seeded automatically when the database is initialized:

- `支付宝:CNY`
- `微信:CNY`
- `银行卡:CNY`
- `银行卡:USD`
- `银行卡:EUR`

### Show account balances

```bash
python "{baseDir}/scripts/bookkeeping.py" account-balances
python "{baseDir}/scripts/bookkeeping.py" account-balances --currency USD
python "{baseDir}/scripts/bookkeeping.py" account-balances --all
```

Key output fields:

- `accounts`
- `totals_by_currency`

Use this command for current holdings by wallet and by currency.

### Set categories

Replace the active set:

```bash
python "{baseDir}/scripts/bookkeeping.py" set-categories --replace 日常 学习 电器
```

Add new active categories without removing old ones:

```bash
python "{baseDir}/scripts/bookkeeping.py" set-categories 旅行
```

### Set accounts

Replace the active set:

```bash
python "{baseDir}/scripts/bookkeeping.py" set-accounts --replace 支付宝:CNY 微信:CNY 银行卡:CNY 银行卡:USD 银行卡:EUR
```

Re-enable or add wallet accounts without removing other active ones:

```bash
python "{baseDir}/scripts/bookkeeping.py" set-accounts Wise:USD Revolut:EUR
```

### Update one account

Rename a wallet or change its configured currency:

```bash
python "{baseDir}/scripts/bookkeeping.py" update-account --name Wise:USD --new-name TravelCard
python "{baseDir}/scripts/bookkeeping.py" update-account --name Wise:USD --new-name TravelCard --currency EUR
```

Notes:

- `--name` identifies the existing wallet; provide `wallet:currency` when the wallet name is ambiguous
- `--new-name` changes the wallet name
- `--currency` changes the wallet currency
- Linked entries and recurring schedules are rewritten to the updated wallet label and currency for consistency

### Record one transaction

Expense example:

```bash
python "{baseDir}/scripts/bookkeeping.py" record --amount 10 --category 日常 --account 支付宝 --description 奶茶 --date 2026-03-15 --source-text "我喝奶茶用了10元" --strict-category --strict-account
```

Income example:

```bash
python "{baseDir}/scripts/bookkeeping.py" record --type income --amount 5000 --category 工资 --account 银行卡 --description 工资到账 --date 2026-03-01 --source-text "这个月工资到账5000元" --strict-account
python "{baseDir}/scripts/bookkeeping.py" record --amount 12 --category 订阅 --account 银行卡:USD --description Claude --date 2026-03-15 --strict-account
```

Notes:

- `--type` defaults to `expense`
- `--date` defaults to today
- `--currency` defaults to the selected wallet currency or `CNY` when no wallet currency is available
- `--category` defaults to `未分类`
- `--account` defaults to `未指定账户`
- `--strict-category` fails if the category is not an active predefined category
- `--strict-account` fails if the account is not an active predefined account

### Recurring transactions

Add one recurring transaction schedule:

```bash
python "{baseDir}/scripts/bookkeeping.py" add-recurring --amount 3000 --category 日常 --account 银行卡:CNY --description 房租 --frequency monthly --next-date 2026-04-01 --strict-category --strict-account
python "{baseDir}/scripts/bookkeeping.py" add-recurring --type income --amount 5000 --category 工资 --account Wise:USD --description 工资到账 --frequency monthly --next-date 2026-04-01 --strict-account
```

List recurring schedules:

```bash
python "{baseDir}/scripts/bookkeeping.py" list-recurring
python "{baseDir}/scripts/bookkeeping.py" list-recurring --all
python "{baseDir}/scripts/bookkeeping.py" list-recurring --due-by 2026-04-30
python "{baseDir}/scripts/bookkeeping.py" list-recurring --account 支付宝 --frequency monthly
python "{baseDir}/scripts/bookkeeping.py" list-recurring --account 银行卡:USD --frequency monthly
```

Update one recurring schedule:

```bash
python "{baseDir}/scripts/bookkeeping.py" update-recurring --id 1 --account 银行卡:USD --next-date 2026-05-01 --strict-account
```

Additional activate or deactivate examples:

```bash
python "{baseDir}/scripts/bookkeeping.py" update-recurring --id 1 --deactivate
python "{baseDir}/scripts/bookkeeping.py" update-recurring --id 1 --activate
```

Deactivate one recurring schedule:

```bash
python "{baseDir}/scripts/bookkeeping.py" delete-recurring --id 1
```

### Daily report

```bash
python "{baseDir}/scripts/bookkeeping.py" day-report --date 2026-03-15
```

### Weekly report

```bash
python "{baseDir}/scripts/bookkeeping.py" week-report --week 2026-W11
python "{baseDir}/scripts/bookkeeping.py" week-report --date 2026-03-15
```

### Monthly report

```bash
python "{baseDir}/scripts/bookkeeping.py" month-report --month 2026-03
```

### Yearly report

```bash
python "{baseDir}/scripts/bookkeeping.py" year-report --year 2026
```

Key output fields:

- `expense_total`
- `income_total`
- `net_total`
- `expense_by_category`
- `income_by_category`
- `expense_by_account`
- `income_by_account`
- `top_expense_category`
- `top_income_category`
- `top_expense_account`
- `top_income_account`
- `entry_count`

These report commands return raw stored amounts. They do not add `totals_by_currency` and they do not convert between currencies.

### List transactions for one date, ISO week, month, or year

```bash
python "{baseDir}/scripts/bookkeeping.py" list-transactions --date 2026-03-15
python "{baseDir}/scripts/bookkeeping.py" list-transactions --week 2026-W11
python "{baseDir}/scripts/bookkeeping.py" list-transactions --month 2026-03
python "{baseDir}/scripts/bookkeeping.py" list-transactions --year 2026
python "{baseDir}/scripts/bookkeeping.py" list-transactions --month 2026-03 --type expense --limit 20
python "{baseDir}/scripts/bookkeeping.py" list-transactions --month 2026-03 --category 学习 --limit 20
python "{baseDir}/scripts/bookkeeping.py" list-transactions --month 2026-03 --account 支付宝 --limit 20
python "{baseDir}/scripts/bookkeeping.py" list-transactions --month 2026-03 --account 银行卡:USD --limit 20
```

### Recent transactions

```bash
python "{baseDir}/scripts/bookkeeping.py" recent-transactions
python "{baseDir}/scripts/bookkeeping.py" recent-transactions --limit 10
python "{baseDir}/scripts/bookkeeping.py" recent-transactions --limit 10 --category 学习
python "{baseDir}/scripts/bookkeeping.py" recent-transactions --limit 10 --account 微信
python "{baseDir}/scripts/bookkeeping.py" recent-transactions --limit 10 --account Wise:USD
```

### Show the latest transaction

```bash
python "{baseDir}/scripts/bookkeeping.py" latest-entry
```

### Update one transaction

```bash
python "{baseDir}/scripts/bookkeeping.py" update-entry --id 1 --amount 12 --category 学习 --account 微信 --description 奶茶教材 --strict-category --strict-account
python "{baseDir}/scripts/bookkeeping.py" update-entry --id 1 --account 银行卡:USD --strict-account
```

Use this when the user wants to fix amount, category, description, note, date, type, currency, or the original prompt text.

### Delete one transaction

```bash
python "{baseDir}/scripts/bookkeeping.py" delete-entry --id 3
```

### Delete the latest transaction

```bash
python "{baseDir}/scripts/bookkeeping.py" delete-latest-entry
```

### Delete one category

```bash
python "{baseDir}/scripts/bookkeeping.py" delete-category --name 旅行
```

### Delete one account

```bash
python "{baseDir}/scripts/bookkeeping.py" delete-account --name 银行卡:USD
```

## Classification Guidance

When a user says `记账 <prompt>`:

1. Extract the monetary amount.
2. Infer whether it is `expense` or `income`.
3. Resolve the date into `YYYY-MM-DD`.
4. Read active categories.
5. Read active accounts when the payment method matters.
6. Map the transaction to the closest active category.
7. Map the payment method to a wallet account such as `支付宝:CNY`, `微信:CNY`, `银行卡:CNY`, `银行卡:USD`, `银行卡:EUR`, or a custom wallet like `Wise:USD`.
8. If the mapping is weak, ask one question instead of inventing a category or account.
9. Use `未分类` or `未指定账户` only as intentional fallbacks.

## Data Semantics

- Amounts are stored internally as integer cents.
- Date storage uses ISO format `YYYY-MM-DD`.
- Weekly filtering uses ISO weeks in `YYYY-Www` format and Monday as the start of the week.
- Period filtering uses half-open ranges:
  - start: inclusive start date for the day, ISO week, month, or year
  - end: exclusive end date for the next day, next ISO week, next month, or next year
- Category reports group by the saved category snapshot so historical entries remain readable even if the active category list changes later.
- Account reports group by the saved wallet snapshot, including currency, so historical entries remain readable even if the active wallet list changes later.
- Period report totals are raw stored amounts. A mixed-currency month such as `10 CNY + 20 USD` is reported as `30.00`, not as a converted value.
- `update-account` rewrites the linked entry and recurring snapshots, plus their currencies, to match the updated wallet definition.
- Recurring transactions are stored as schedules; they do not auto-create normal entries unless the caller decides to record them separately.
