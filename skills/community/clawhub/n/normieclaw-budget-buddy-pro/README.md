# Budget Buddy Pro 💰

**Stop paying $100/year just to look at your own money.**

Budget Buddy Pro turns your AI agent into a personal financial coach. Drop any bank statement, get instant spending breakdowns, smart budgets, savings goal tracking, and bill reminders — all from your chat. No subscriptions. No cloud. Your data stays on your machine.

---

## What It Does

- 📄 **Statement Parsing** — Drop a CSV or PDF from any bank. Chase, Amex, your local credit union — it handles them all.
- 🏷️ **Auto-Categorization** — Transactions are automatically sorted into categories. No manual tagging.
- 📊 **Budget Builder** — Creates a personalized budget based on your actual spending (50/30/20 or custom).
- 💸 **Spending Alerts** — Warns you when you're approaching category limits. Catches forgotten subscriptions.
- 🎯 **Savings Goals** — Set targets, track progress, see timelines.
- 🔔 **Bill Reminders** — Never miss a payment. Upcoming bills at a glance.
- 📈 **Net Worth Tracking** — Assets minus liabilities, tracked over time.
- 📋 **Monthly & Weekly Summaries** — Clear breakdowns of where your money went.
- 🔄 **Custom Rules** — "All Uber rides are business expenses" — set it once, done forever.

## How to Install

1. Download the `budget-buddy-pro/` folder into your agent's workspace.
2. Open `SETUP-PROMPT.md` and paste the setup block into your agent's chat.
3. Your agent handles the rest — creates directories, sets permissions, verifies installation.
4. Start budgeting: "Help me set up my budget" or drop a bank statement.

**That's it. Seriously.**

## Security

🛡️ **Codex Security Verified**

- All financial data stored locally with restrictive file permissions (chmod 600).
- No API keys, no cloud sync, no third-party data sharing.
- Prompt injection defenses built in — your statement data can't hijack your agent.
- Full security audit details in `SECURITY.md`.

## What You'll Need

- An AI agent that supports OpenClaw skills 
- Python 3.8+ (for the statement parser script)
- Playwright (optional — for generating visual budget reports)
