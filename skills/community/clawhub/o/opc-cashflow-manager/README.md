# opc-cashflow-manager

Cash flow decision system for solo founders. Probability-weighted forecasting, runway calculation, burn rate analysis, and survival alerts.

**It manages survival, not full accounting.**

## What It Does

### Cash Flow Forecasting
- Probability-weighted inflow projections (high/medium/low confidence → 0.95/0.60/0.20)
- 3-scenario modeling: base, conservative, aggressive
- Week-by-week breakdown for month 1, monthly for months 2–4
- Conservative scenario highlighted — plan for the worst, be pleasantly surprised

### Runway & Burn Rate
- Monthly burn rate broken down by essentiality (critical/important/optional)
- Net burn calculation (burn minus weighted income)
- Runway under three scenarios with survival threshold assessment
- What-if cut modeling (cut optional, cut optional+important, lose top client)

### Survival Alerts
- Runway warnings (< 6 months warning, < 3 months critical)
- Negative cash detection across all scenarios
- Collection urgency (overdue inflows)
- Large outflow warnings (> 30% of cash)
- Client concentration risk (> 50% of inflows from one source)

### Cost-Cut Analysis
- Ordered cut list: optional first, critical never
- Impact modeling per tier of cuts
- Monthly subscription audit framework
- Revenue-side alternatives before deeper cuts

### Collections Integration
- Auto-imports sent/overdue invoices from opc-invoice-manager
- Maps invoice status → inflow confidence levels
- Collection priority list sorted by urgency and amount
- AR health summary (outstanding, overdue, average days to pay)

### Scenario Modeling
- "What if I lose Client X?" — remove inflows, re-forecast
- "What if I hire at $5k/mo?" — add to recurring, re-forecast
- "What if payment delays 30 days?" — shift dates, re-forecast
- Side-by-side comparison: current vs modified forecast

## Installation

### Option 1: Clone with the full skill suite

```bash
git clone https://github.com/LeonFJR/opc-skills.git ~/.claude/skills/opc-skills
```

### Option 2: Copy just this skill

```bash
cp -r opc-skills/opc-cashflow-manager ~/.claude/skills/opc-cashflow-manager
```

### Option 3: Add as a project skill

```json
{
  "skills": ["path/to/opc-skills/opc-cashflow-manager"]
}
```

## Usage

### Create a forecast

```
/opc-cashflow-manager

I have $25,000 in the bank. Expected: $8,000 from Acme (invoice sent, due in 2 weeks),
$5,000 from Beta (verbal agreement, maybe next month), $3,000 pipeline lead.
Monthly expenses: $2,500 rent, $500 software, $2,000 contractor, $200 subscriptions.
```

### Check runway

```
How long can I survive at current burn rate?
```

### What-if scenario

```
What if I lose Acme as a client?
```

### Cut costs

```
What can I cut to extend runway by 3 months?
```

### Collections priority

```
Who owes me money and what should I chase first?
```

### Dashboard

```
What's my cash position?
```

## Data Model

Six core objects per monthly snapshot:

| Object | Purpose |
|--------|---------|
| Opening Cash | Cash on hand at period start |
| Expected Inflows | Probability-weighted income expectations |
| Committed Outflows | One-time expenses with essentiality classification |
| Recurring Commitments | Ongoing expenses (auto-expand into outflows) |
| Scenario Assumptions | 3-scenario factors (base/conservative/aggressive) |
| Alerts & Actions | System-generated warnings and recommended actions |

## Archive Structure

```
cashflow/
├── INDEX.json
└── snapshots/
    └── 2026-03/
        └── snapshot.json
```

## Cross-Skill Integration

| Skill | Integration |
|-------|-------------|
| opc-invoice-manager | Auto-import invoices as inflows, AR aging, collection stages |
| opc-contract-manager | Billing terms → recurring inflow expectations |
| opc-product-manager | Product costs → recurring commitment references |

All integrations are optional — the skill works standalone.

## Skill Architecture

- `SKILL.md` — Core workflow, loaded first. 6 modes: Forecast, Dashboard, Collections, Cost-Cut, Scenario, Runway
- `references/` — Loaded on-demand: forecasting rules, cost-cutting playbook, runway guide
- `templates/` — JSON schema + output templates for reports
- `scripts/` — Python 3.8+ (stdlib only) forecast engine and CLI

## Requirements

- Claude Code CLI
- Python 3.8+ (standard library only — no pip installs)

## What This Skill Is NOT

- Not an accounting system (no P&L, no balance sheet, no depreciation)
- Not a tax tool (escalates all tax questions to an accountant)
- Not a bookkeeping replacement (no transaction categorization)
- Not an investment advisor (escalates financing/investment decisions)
- Not a payroll system (no payroll tax calculation)

When in doubt, it tells you to talk to your accountant.

## License

MIT
