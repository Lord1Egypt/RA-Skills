# Freelancer Toolkit

**AI-powered time tracking, client management, and project profitability for freelancers.**

Track time by talking. Invoice by clicking. Replace $240/yr in subscriptions with a one-time $9.99 tool.

## What It Does

- **Conversational time logging** — "I worked 3 hours on the Acme redesign today." No timers, no forms, no apps.
- **Client management** — Your agent remembers rates, payment terms, preferences, and project history for every client.
- **Project profitability** — Know your effective hourly rate on every project. Get alerted before you blow a budget.
- **Timesheet generation** — Weekly and monthly timesheets in markdown or CSV. Per-client or across all clients.
- **Auto-invoicing** — "Invoice Acme for March" pulls all tracked time, calculates totals, and generates an invoice via InvoiceGen Pro.
- **Weekly summaries** — Every Monday: hours breakdown, client split, budget warnings, unbilled time alerts.
- **Dashboard widgets** — Hours by client, weekly trends, profitability table, revenue pipeline.

## What It Replaces

| Tool | Annual Cost | What Freelancer Toolkit Covers |
|------|------------|-------------------------------|
| Toggl Track (Starter) | $108/yr | Time tracking, project estimates, billable rates |
| Harvest (Pro) | $132/yr | Time tracking, invoicing, project budgets |
| **Combined** | **$240/yr** | **All of the above + AI profitability insights** |

## Quick Start

1. Install from [normieclaw.ai](https://normieclaw.ai)
2. Run the setup prompt — takes about 2 minutes
3. Start logging: "I worked 2 hours on [client] today"

## How It Works

Tell your agent what you did. It handles the rest.

```
You: "Just finished 3 hours on the Acme redesign, homepage wireframes"

Agent: ✅ Logged: 3.00 hrs — Acme Corp → Website Redesign
       "Homepage wireframes"
       Date: March 10, 2026 | Billable | Rate: $85/hr ($255.00)
       
       ⚠️ Heads up: This project is at 87% of budget (52.5/60 hrs).
```

```
You: "Invoice Acme for March"

Agent: 📄 Invoice Draft: Acme Corp — March 2026
       • Visual design — 12.5 hrs × $85 = $1,062.50
       • Development — 8.0 hrs × $85 = $680.00
       Subtotal: $1,742.50 | Net 30
       
       Ready to generate with InvoiceGen Pro? (Y/n)
```

## File Structure

```
~/.freelancer-toolkit/
├── settings.json        # Your config (rates, categories, preferences)
├── clients.json         # Client database
├── projects.json        # Project database
├── time-entries.json    # All time entries
├── timers.json          # Active timer state
└── exports/             # Generated timesheets and reports
```

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/setup.sh` | Initialize data directory and default config |
| `scripts/export-timesheet.sh` | Export time entries as CSV |
| `scripts/client-report.sh` | Generate per-client billing summary |

## Requirements

- OpenClaw agent with file system access
- `jq` (for scripts — installed by setup.sh if missing)
- Bash 4+ (macOS/Linux)

## Support

Questions? Issues? Reach out at [normieclaw.ai](https://normieclaw.ai).

---

*Freelancer Toolkit is a NormieClaw product. $9.99 Free and open-source.*
