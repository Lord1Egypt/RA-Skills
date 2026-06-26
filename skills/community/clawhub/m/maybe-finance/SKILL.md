---
name: maybe-finance
description: Personal finance management skill using Maybe Finance OS. Use when users need to track expenses, analyze budgets, monitor net worth, or manage personal finances through the Maybe Finance self-hosted platform. Supports transaction tracking, account management, budget analysis, and financial reporting.
---

# Maybe Finance Skill

Personal finance management powered by [Maybe Finance](https://github.com/maybe-finance/maybe) - an open-source personal finance OS.

## Overview

Maybe Finance is a self-hosted personal finance platform for tracking:
- **Transactions** - Income and expenses
- **Accounts** - Bank accounts, investments, loans
- **Budgets** - Monthly spending targets
- **Net Worth** - Assets minus liabilities over time
- **Cash Flow** - Income vs expenses analysis

## Prerequisites

1. **Self-hosted Maybe instance** - Deploy via Docker:
   ```bash
   docker run -d -p 3000:3000 ghcr.io/maybe-finance/maybe:latest
   ```
2. **API Token** - Generate in Maybe UI: Settings → API Keys

## Configuration

Set environment variables:
```bash
export MAYBE_API_URL="http://localhost:3000"
export MAYBE_API_TOKEN="your-api-token"
```

## Usage

### Account Management
```bash
# List all accounts
maybe-finance accounts list

# Add a new account
maybe-finance accounts add --name "Alipay" --type checking --balance 5000

# Update account balance
maybe-finance accounts update <account-id> --balance 6000

# Delete account
maybe-finance accounts delete <account-id>
```

### Transaction Tracking
```bash
# List recent transactions
maybe-finance transactions list --limit 20

# Add income
maybe-finance transactions add --amount 10000 --type income --category "工资" --description "三月工资"

# Add expense
maybe-finance transactions add --amount -150 --type expense --category "餐饮" --description "午餐"

# Search transactions
maybe-finance transactions search --category "餐饮" --from 2024-01-01 --to 2024-03-31
```

### Budget Analysis
```bash
# View current month budget
maybe-finance budget current

# Analyze spending by category
maybe-finance budget analyze --month 2024-03

# Compare months
maybe-finance budget compare --from 2024-01 --to 2024-03
```

### Net Worth & Reports
```bash
# Current net worth snapshot
maybe-finance networth

# Cash flow report
maybe-finance cashflow --period monthly

# Generate financial summary
maybe-finance summary --year 2024
```

## Scripts

All functionality is available through `scripts/maybe-cli.py`:
- Handles API authentication
- Formats output for readability
- Supports JSON export for further processing

## Integration Ideas

- Connect with CSV import skill for bulk transaction entry
- Schedule daily/weekly financial reports via cron
- Export data for tax preparation
- Alert on budget overruns
