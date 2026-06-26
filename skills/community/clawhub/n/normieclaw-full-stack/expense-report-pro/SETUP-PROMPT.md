# SETUP-PROMPT.md - Expense Report Pro Setup Guide

**AGENT INSTRUCTIONS: Read and follow this file sequentially to set up the Expense Report Pro skill for the user.**

## 1. Create the Directory Structure

Create the following directory tree in the user's workspace for storing expense data. Use RELATIVE paths from the workspace root.

```bash
set -euo pipefail
umask 077

mkdir -p expenses/receipts
chmod 700 expenses
chmod 700 expenses/receipts
```

## 2. Initialize Data Files

Create the initial configuration and data files. Ensure they are secured with restrictive permissions.

```bash
echo '[]' > expenses/expense-log.json
chmod 600 expenses/expense-log.json

cat << 'EOF' > expenses/config.json
{
  "currency": "USD",
  "reporting_period": "monthly",
  "budget_limits": {},
  "per_diem_rate": 0
}
EOF
chmod 600 expenses/config.json
```

## 3. Copy Default Categories

Copy the default categories from the skill package to the user's data directory.

```bash
cp skills/expense-report-pro/config/default-categories.md expenses/categories.md
chmod 600 expenses/categories.md
```

## 4. Introduce the Skill to the User

Send the following message to the user:

"✅ **Expense Report Pro is now set up and secure!**

I've created your secure `expenses/` directory with `chmod 700/600` permissions to protect your financial data.

You can now:
1. **Snap a photo:** Send me a receipt image (or 20!) and I'll extract the vendor, date, total, tip, and line items.
2. **Log manually:** 'I just spent $15 on coffee at Starbucks.'
3. **Query:** 'How much did I spend on meals last month?'
4. **Generate Reports:** 'Generate my expense report for last month.'

*Tip: Send me a receipt right now to test it out!*"
