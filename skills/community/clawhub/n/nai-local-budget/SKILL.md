---
name: local-budget
description: Analyze exported bank/credit card CSV files locally to track spending, categorize transactions with LLM reasoning, compare against user-defined budgets, and generate markdown reports. Use when the user mentions budgeting, spending analysis, finance tracking, bank statements, credit card exports, CSV transactions, monthly spending, or wants to know where their money is going. Fully local — no third-party APIs, complete privacy. Triggers on words like budget, spending, transactions, bank CSV, credit card export, finance report, monthly expenses.
---

# Local Budget

Analyze bank/credit card CSV exports, categorize transactions, compare against budgets, and generate clean markdown reports for Obsidian.

## Workflow Overview

1. **Parse** — run `parse_csv.py` to normalize raw CSVs into a unified JSON format
2. **Categorize** — run `categorize.py` to get LLM-ready JSON with suggested categories; review/adjust
3. **Report** — run `report.py` to generate a markdown spending report

All scripts live in `scripts/`. Budget config and sample data in `assets/`. See `references/csv-formats.md` for supported formats and `references/categories.md` for category customization.

## Step 1: Parse CSV

```bash
python3 scripts/parse_csv.py <input.csv> [--format chase|boa|generic] [--output transactions.json]
```

- Auto-detects format if `--format` is omitted (checks header columns)
- Outputs a unified JSON array of transaction objects
- Each transaction: `{ "date": "YYYY-MM-DD", "description": str, "amount": float, "type": "debit"|"credit", "original_category": str|null }`
- Debits are positive amounts; credits (refunds/income) are negative
- Handles multiple date formats: `MM/DD/YYYY`, `YYYY-MM-DD`, `MM/DD/YY`
- Skips rows with missing date or amount; logs warnings to stderr

If the user's bank isn't auto-detected, check `references/csv-formats.md` for column mappings and use `--format generic` with the appropriate flag, or add a new format.

## Step 2: Categorize Transactions

```bash
python3 scripts/categorize.py transactions.json [--budget assets/sample-budget.json] [--output categorized.json]
```

- Outputs a JSON file with each transaction tagged with a suggested `category` based on description keyword matching
- The LLM (you) should review the output and adjust categories before generating the report
- Default categories: Housing, Food & Dining, Transportation, Utilities, Entertainment, Shopping, Health, Subscriptions, Income, Other
- To adjust: edit the JSON directly, or tell the user which transactions look miscategorized and confirm corrections
- See `references/categories.md` for the keyword-matching logic and how to customize

**LLM review step:** After running categorize.py, scan the output for anything in "Other" or with low-confidence keywords. Ask the user to confirm or correct those entries before proceeding.

## Step 3: Generate Report

```bash
python3 scripts/report.py categorized.json [--budget assets/sample-budget.json] [--output report.md]
```

- Generates a markdown report with:
  - Monthly summary (total in/out)
  - Spending by category with budget vs. actual comparison
  - Top 10 merchants by spend
  - Month-over-month trend if multiple months present in the data
  - Overage alerts for categories that exceed budget
- If `--budget` is omitted, report shows actuals only (no budget comparison)
- Output is Obsidian-compatible markdown with frontmatter

## Budget Config

Budget is defined in a JSON file. See `assets/sample-budget.json` for a realistic example.

```json
{
  "monthly_budgets": {
    "Housing": 1800,
    "Food & Dining": 600
  }
}
```

## Common Tasks

**"Analyze my Chase export"**
→ `parse_csv.py chase_export.csv --format chase --output tx.json`
→ `categorize.py tx.json --output cat.json`
→ Review categories, then `report.py cat.json --budget assets/sample-budget.json`

**"Show me my spending for March"**
→ Parse and categorize the CSV, then filter by month in `report.py` (it auto-groups by month)

**"I went over budget on dining"**
→ Run the full pipeline; report.py flags overage categories with ⚠️

**"Add a new bank format"**
→ See `references/csv-formats.md` for the column mapping spec

**"Customize categories"**
→ See `references/categories.md` to edit keyword lists or add new categories

## File Locations

Store CSVs and JSON outputs wherever the user prefers. Default working directory is wherever the command is run. Suggest keeping exports in a dedicated folder like `~/finances/exports/`.

Reports can be saved directly to the Obsidian vault:
```bash
python3 scripts/report.py categorized.json --output ~/path/to/vault/finance/2024-03-budget.md
```
