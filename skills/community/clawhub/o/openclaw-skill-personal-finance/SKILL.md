---
name: personal-finance
description: Parse personal finance CSV exports, validate schema, categorize transactions via local rules, and summarize/report income, expenses, merchants, and categories.
---

# Personal Finance

## Scope & Safety
- Operate on exported bank or credit-card CSVs in a read-only manner by default; no automatic uploads, API calls, or write-backs occur unless an explicit `--output` path is provided.
- Mask account numbers in all CLI outputs by replacing digits except the final four to keep PII safe for every command.
- Work offline; all logic lives inside `personal-finance.sh`, `config/category-rules.json`, and the included sample CSV.

## Primary Operations
All commands live in `personal-finance.sh` at the skill root. Invoke with:

```sh
./personal-finance.sh <command> [--csv <path>] [--config <path>] [--output <path>] [--period <period>]
```

### 1. validate
Checks that the CSV contains the required fields (`date`, `description`, `amount`, `account_number`) and that every amount is numeric. Use this before processing new exports to avoid schema drift.

```
./personal-finance.sh validate --csv sample-data/sample-transactions.csv
```

### 2. summarize
Aggregates income (positive `amount`) and expenses (negative `amount`) by period. Supports `month`, `quarter`, or `year` (default `month`). Outputs totals and net flows.

```
./personal-finance.sh summarize --period month --csv sample-data/sample-transactions.csv
```

### 3. categorize
Uses the local rules file (`config/category-rules.json`) to map descriptions to categories through keyword matching. Prints each transaction with masked accounts and assigned categories. Pass `--output` to emit a new CSV; otherwise, it stays read-only.

```
./personal-finance.sh categorize --csv sample-data/sample-transactions.csv --output /tmp/categorized.csv
```

### 4. report
Builds insight summaries: top merchants and categories by spend, plus transaction counts. It reuses the same rules file so it can work offline and stay consistent with `categorize`.

```
./personal-finance.sh report --csv sample-data/sample-transactions.csv
```

## Configuration & Samples
- `config/category-rules.json`: keyword-to-category rules that `categorize` and `report` share.
- `sample-data/sample-transactions.csv`: minimal CSV (date, description, merchant, category, amount, account_number) for smoke tests and onboarding.

Keep both files in the skill folder. Adjust the JSON rules for your own merchant vocabulary; the script reloads them each run and never calls external services.
