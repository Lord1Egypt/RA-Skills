---
name: monarch
description: "Access Monarch Money financial data: accounts, transactions, budgets, and cashflow. Use when the user asks about their finances, spending, account balances, budget status, cashflow summaries, or wants to refresh linked bank accounts. Triggers on: 'how much did I spend', 'what's my balance', 'show my budget', 'cashflow this month', 'refresh my accounts', or any personal finance query."
metadata:
  {
    "openclaw":
      {
        "emoji": "💰",
        "requires": { "bins": ["python3"] },
        "install":
          [
            {
              "id": "pip",
              "kind": "pip",
              "package": "monarchmoney",
              "label": "Install monarchmoney Python library",
            },
          ],
      },
  }
---

# Monarch Money Skill

Query Monarch Money for financial data via CLI wrapper scripts.

## Prerequisites

1. Install the library:
   ```bash
   pip install monarchmoney
   ```

2. First-time authentication (interactive, run once):
   ```bash
   python3 scripts/login_setup.py
   ```
   Prompts for email, password, and MFA code if enabled. Saves session to `~/.monarchmoney/mm_session.pickle`. Sessions last months.

## Commands

All commands output JSON. Pipe through `jq` for filtering.

### Accounts
```bash
python3 scripts/monarch.py accounts
```
Returns: id, displayName, type, subtype, currentBalance, institution, isHidden, includeInNetWorth.

### Transactions
```bash
# Last 30 days (default)
python3 scripts/monarch.py transactions

# Custom date range
python3 scripts/monarch.py transactions --start 2026-01-01 --end 2026-01-31

# Limit results
python3 scripts/monarch.py transactions --limit 50
```
Returns: id, date, amount, merchant, category, account, notes, isPending, isRecurring.

### Budgets
```bash
python3 scripts/monarch.py budgets
```
Returns: monthlyBudget, totalSpent, per-category breakdown (budgetAmount, spentAmount, remainingAmount).

### Cashflow
```bash
# Current month
python3 scripts/monarch.py cashflow

# Specific month
python3 scripts/monarch.py cashflow --month 2026-01
```
Returns: income, expenses, savings, savingsRate for the specified month.

### Refresh Accounts
```bash
python3 scripts/monarch.py refresh
```
Triggers a sync with all linked financial institutions.

## Troubleshooting

- **"Not authenticated" or "Session expired"**: Delete `~/.monarchmoney/mm_session.pickle` and re-run `scripts/login_setup.py`.
- **Rate limiting**: Monarch Money may throttle rapid requests. Space out queries.
- **Import errors**: Ensure `monarchmoney` is installed in the Python environment being used.
