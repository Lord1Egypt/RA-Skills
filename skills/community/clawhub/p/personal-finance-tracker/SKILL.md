---
name: Personal Finance Tracker
slug: personal-finance-tracker
version: 1.0.0
homepage: https://clawic.com/skills/personal-finance-tracker
description: Track personal finances with cashflow reviews, recurring bill detection, debt triage, CSV imports, and net worth snapshots.
changelog: "Initial release with cashflow review protocol, CSV analysis tools, recurring spend detection, and privacy-first local tracking."
metadata: {"clawdbot":{"emoji":"💸","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/personal-finance-tracker/"]}}
---

# Personal Finance Tracker

Personal finance tracker for cashflow control, recurring bills, debt pressure, and weekly money decisions.

## Setup

On first use, read `setup.md` for integration guidelines. Ask before creating `~/personal-finance-tracker/` or saving any financial context locally.

## When to Use

User needs personal finance tracking, finance tracker help, budgeting, expense tracking, cashflow visibility, debt prioritization, subscription cleanup, or recurring bill review. Agent handles fast money snapshots, pasted transaction cleanup, CSV imports, recurring spend detection, debt triage, runway checks, and weekly or monthly review workflows.

Use this when the job is making clearer money decisions, not just logging another transaction. The outcome should be an actionable view of what to protect, what to cut, and what needs attention before the next paycheck or billing cycle.

## Architecture

Local workspace is optional and only created with user consent.

```text
~/personal-finance-tracker/
├── memory.md        # High-signal money context and review cadence
├── accounts.md      # Balances, account roles, sync notes
├── recurring.md     # Bills, subscriptions, annual charges, due dates
├── plans.md         # Debt payoff, savings, cut list, next actions
└── reviews.md       # Weekly and monthly snapshots
```

## Quick Reference

Load only what improves the current answer. Prefer the scripts for deterministic summaries and the playbooks for judgment.

| Topic | File |
|-------|------|
| Setup and activation | `setup.md` |
| Optional continuity memory | `memory-template.md` |
| CSV schema and normalization | `csv-schema.md` |
| Review cadence and reporting | `review-rhythm.md` |
| Debt and subscription triage | `debt-triage.md` |
| Local command recipes | `commands.md` |
| CSV cashflow rollup script | `cashflow_rollup.py` |
| Recurring charge scanner | `recurring_scan.py` |

## Core Rules

### 1. Start with the Runway Review
- Answer three questions first: what cash is available now, what fixed obligations hit next, and what room is actually free to spend.
- A finance tracker that cannot tell the user whether they are safe this week is not useful.
- Use `review-rhythm.md` to frame the first snapshot in under 30 seconds.

### 2. Normalize inputs before making claims
- Clean dates, signs, merchants, categories, and duplicates before summarizing patterns, whether the input comes from CSV exports or pasted transaction lines.
- Messy exports create fake insights and broken budgets.
- Use `csv-schema.md` and `cashflow_rollup.py` before giving trend or category conclusions.

### 3. Separate recurring drag from one-off spend
- Distinguish rent, utilities, debt payments, subscriptions, and annual charges from irregular purchases.
- Users usually fail because fixed drag hides inside noisy transaction lists.
- Use `recurring_scan.py` and `debt-triage.md` to isolate what repeats and what can be cut.

### 4. Prioritize cashflow before optimization theater
- Protect essentials, taxes, minimum debt payments, and near-term obligations before discussing long-range goals.
- Fancy charts are useless if the account risks overdraft next week.
- Recommend protect, watch, cut, or defer actions instead of generic motivation.

### 5. Turn every review into a concrete next-action list
- End each session with a short list: pay, cancel, renegotiate, transfer, delay, or monitor.
- The skill should reduce decision fatigue, not create another dashboard the user ignores.
- Use `review-rhythm.md` to close weekly and monthly reviews with named actions.

### 6. Keep storage minimal, local, and opt-in
- Save only balances, recurring commitments, debt priorities, and review decisions the user wants remembered.
- Never create local files silently for sensitive finance data.
- Use `memory-template.md` only after the user agrees to continuity.

### 7. Never cross from guidance into account control
- This skill can analyze, classify, forecast, and prepare plans.
- It must not move money, cancel services, log into banks, or present itself as regulated financial advice.
- Keep recommendations transparent, reversible, and grounded in the user-provided data.

## Operating Rhythm

### Fast snapshot
- Cash on hand now
- Payments due in the next 7 to 14 days
- Largest recurring drains
- Free-to-spend amount after essentials

### Weekly review
- Compare actual outflow vs expected outflow
- Flag duplicate charges, subscription drift, and overspend categories
- Update the cut list and next bill dates

### Monthly reset
- Rebuild recurring obligations
- Re-rank debt pressure and savings targets
- Capture what changed in income, bills, and available runway

## Common Traps

- Tracking every coffee but ignoring annual charges -> false sense of control and surprise cash hits.
- Mixing personal, business, and tax money in one mental bucket -> bad decisions and missed obligations.
- Treating subscriptions as harmless small spend -> silent monthly drag compounds quickly.
- Looking only at category charts -> hides due dates, debt penalties, and account timing risk.
- Forecasting from raw exports without cleanup -> duplicates and sign errors corrupt the plan.
- Letting the agent store full statements by default -> unnecessary privacy exposure.

## Security & Privacy

**Data that stays local when the user opts in:**
- Balances, recurring bills, review notes, and debt priorities in `~/personal-finance-tracker/`
- CSV files and local script outputs run on the user's machine

**This skill does NOT:**
- Connect to banks or fintech APIs on its own
- Send transaction data to undeclared external services
- Create local storage without user consent
- Move money, cancel subscriptions, or change accounts automatically

**Guardrails:**
- Store only high-signal summaries, never full credentials or card numbers
- Ask before persisting any sensitive context
- Prefer local CSV analysis to cloud processing

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `money` — General money planning and financial conversations
- `subscriptions` — Subscription audits, trims, and renewal decisions
- `csv` — CSV cleanup, mapping, and transformation workflows
- `cfo` — Higher-level financial operating decisions and scenario planning

## Feedback

- If useful: `clawhub star personal-finance-tracker`
- Stay updated: `clawhub sync`
