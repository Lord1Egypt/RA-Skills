# Budget Buddy Pro — Setup Prompt

Copy and paste the following block into your AI agent's chat to install Budget Buddy Pro automatically.

---

## Setup Instructions

Paste this entire block to your agent:

```
I need you to install the Budget Buddy Pro skill. Run these commands exactly:

# 1. Skill files (installed automatically by clawhub install)
# Files are installed by clawhub install — no manual copy needed

# 2. Create the data directories
mkdir -p skills/budget-buddy-pro/data/transactions
mkdir -p skills/budget-buddy-pro/data/statements

# 3. Initialize empty data files
echo '[]' > skills/budget-buddy-pro/data/recurring.json
echo '[]' > skills/budget-buddy-pro/data/rules.json
echo '[]' > skills/budget-buddy-pro/data/savings-goals.json
echo '[]' > skills/budget-buddy-pro/data/net-worth.json

# 4. Copy default categories to data directory
cp skills/budget-buddy-pro/config/budget-config.json skills/budget-buddy-pro/data/categories.json

# 5. Set secure permissions (directories: 700, sensitive files: 600)
chmod 700 skills/budget-buddy-pro/data
chmod 700 skills/budget-buddy-pro/data/transactions
chmod 700 skills/budget-buddy-pro/data/statements
chmod 700 skills/budget-buddy-pro/scripts
chmod 600 skills/budget-buddy-pro/data/*.json
chmod 600 skills/budget-buddy-pro/config/budget-config.json
chmod 700 skills/budget-buddy-pro/scripts/*.sh
chmod 700 skills/budget-buddy-pro/scripts/*.py

# 6. Verify the installation
echo "--- Budget Buddy Pro Installation Verification ---"
echo "Checking SKILL.md..."
test -f skills/budget-buddy-pro/SKILL.md && echo "✅ SKILL.md" || echo "❌ SKILL.md MISSING"
echo "Checking config..."
test -f skills/budget-buddy-pro/config/budget-config.json && echo "✅ budget-config.json" || echo "❌ budget-config.json MISSING"
echo "Checking data directory..."
test -d skills/budget-buddy-pro/data && echo "✅ data/" || echo "❌ data/ MISSING"
test -f skills/budget-buddy-pro/data/recurring.json && echo "✅ recurring.json" || echo "❌ recurring.json MISSING"
test -f skills/budget-buddy-pro/data/rules.json && echo "✅ rules.json" || echo "❌ rules.json MISSING"
test -f skills/budget-buddy-pro/data/savings-goals.json && echo "✅ savings-goals.json" || echo "❌ savings-goals.json MISSING"
test -f skills/budget-buddy-pro/data/net-worth.json && echo "✅ net-worth.json" || echo "❌ net-worth.json MISSING"
test -f skills/budget-buddy-pro/data/categories.json && echo "✅ categories.json" || echo "❌ categories.json MISSING"
echo "Checking scripts..."
test -f skills/budget-buddy-pro/scripts/generate-budget-report.sh && echo "✅ generate-budget-report.sh" || echo "❌ generate-budget-report.sh MISSING"
test -f skills/budget-buddy-pro/scripts/parse-statement.py && echo "✅ parse-statement.py" || echo "❌ parse-statement.py MISSING"
echo "Checking examples..."
test -d skills/budget-buddy-pro/examples && echo "✅ examples/" || echo "❌ examples/ MISSING"
echo "Checking dashboard kit..."
test -f skills/budget-buddy-pro/dashboard-kit/DASHBOARD-SPEC.md && echo "✅ DASHBOARD-SPEC.md" || echo "❌ DASHBOARD-SPEC.md MISSING"
echo "--- Installation complete! ---"
echo ""
echo "🎉 Budget Buddy Pro is ready! Try: 'Help me set up my budget' or drop a bank statement."
```

---

## What This Does

1. **Copies** all skill files from the downloaded package into your workspace's `skills/` directory.
2. **Creates** the `data/` directory structure for storing your financial data.
3. **Initializes** empty JSON arrays for recurring items, rules, savings goals, and net worth.
4. **Copies** default budget categories into your active data directory.
5. **Sets permissions** — directories at `700`, sensitive data files at `600`.
6. **Verifies** everything installed correctly with a checklist.

## After Setup

Just start talking to your agent about money! Try:
- "Help me set up a budget"
- Drop a CSV or PDF bank statement into the chat
- "I spent $45 on groceries today"
- "I want to save $5,000 for a vacation"

Your agent will read `skills/budget-buddy-pro/SKILL.md` and handle everything from there.
