# Freelancer Toolkit — SKILL.md

> AI-powered time tracking, client management, and project profitability for freelancers.
> Replaces Toggl Track + Harvest. One-time $9.99 via NormieClaw.

---

## Overview

Freelancer Toolkit turns your OpenClaw agent into a personal freelance business manager. Track time by talking ("I worked 3 hours on the Acme redesign today"), manage clients and projects, monitor profitability, generate timesheets, and hand off invoices to InvoiceGen Pro — all through conversation.

No timers to click. No forms to fill. No apps to open. Just tell your agent what you did.

---

## Data Storage

All data lives in JSON files under `~/.freelancer-toolkit/`:

```
~/.freelancer-toolkit/
├── settings.json        # Global config (default rate, categories, preferences)
├── clients.json         # Client database
├── projects.json        # Project database
├── time-entries.json    # All time entries
├── timers.json          # Active timers (start/stop tracking)
└── exports/             # Generated timesheets and reports
```

### File Schemas

**settings.json**
```json
{
  "default_hourly_rate": 75,
  "currency": "USD",
  "currency_symbol": "$",
  "week_start": "monday",
  "billing_period": "monthly",
  "categories": ["design", "development", "consulting", "meetings", "admin", "writing", "research"],
  "non_billable_categories": ["admin", "internal"],
  "weekly_summary_day": "monday",
  "invoicegen_integration": true,
  "rounding": "nearest_quarter"
}
```

**clients.json** — Array of client objects:
```json
{
  "id": "client_uuid",
  "name": "Jane Smith",
  "company": "Acme Corp",
  "email": "jane@acmecorp.com",
  "phone": "555-0123",
  "default_rate": 85,
  "payment_terms": "net_30",
  "notes": "Prefers invoices on the 1st. Always pays on time.",
  "status": "active",
  "created_at": "2026-01-15T10:00:00Z",
  "total_billed": 12400,
  "total_paid": 9600,
  "tags": ["design", "retainer"]
}
```

**projects.json** — Array of project objects:
```json
{
  "id": "proj_uuid",
  "client_id": "client_uuid",
  "name": "Website Redesign",
  "description": "Full redesign of acmecorp.com",
  "status": "active",
  "billing_type": "fixed",
  "quoted_price": 5000,
  "hourly_rate": 85,
  "estimated_hours": 60,
  "hours_logged": 42.5,
  "effective_rate": 117.65,
  "budget_alert_threshold": 0.8,
  "milestones": [
    {"name": "Wireframes", "status": "completed", "due_date": "2026-02-01"},
    {"name": "Visual Design", "status": "in_progress", "due_date": "2026-03-01"},
    {"name": "Development", "status": "pending", "due_date": "2026-04-01"}
  ],
  "created_at": "2026-01-10T10:00:00Z",
  "completed_at": null,
  "tags": ["web", "design"]
}
```

**time-entries.json** — Array of time entry objects:
```json
{
  "id": "entry_uuid",
  "client_id": "client_uuid",
  "project_id": "proj_uuid",
  "date": "2026-03-10",
  "hours": 3.0,
  "description": "Logo concept exploration, 3 directions",
  "category": "design",
  "billable": true,
  "invoiced": false,
  "invoice_id": null,
  "created_at": "2026-03-10T17:30:00Z"
}
```

**timers.json** — Active timer state:
```json
{
  "active": true,
  "client_id": "client_uuid",
  "project_id": "proj_uuid",
  "description": "Working on homepage layout",
  "category": "design",
  "started_at": "2026-03-10T14:00:00Z",
  "paused_at": null,
  "accumulated_minutes": 0
}
```

---

## Initialization

On first use or when data files don't exist:

1. Create `~/.freelancer-toolkit/` directory
2. Copy default `settings.json` from the skill's `config/` directory
3. Initialize empty arrays in `clients.json`, `projects.json`, `time-entries.json`
4. Initialize `timers.json` with `{"active": false}`
5. Create `exports/` directory

```bash
mkdir -p ~/.freelancer-toolkit/exports
```

If `settings.json` already exists, never overwrite — the user may have customized it.

---

## Core Capabilities

### 1. Conversational Time Logging

This is the flagship feature. Parse natural language into structured time entries.

**Input patterns to recognize:**

| User says | Parsed result |
|-----------|--------------|
| "I worked 3 hours on the Acme redesign today" | client: Acme, project: redesign, hours: 3, date: today |
| "Just finished 2.5 hours of consulting with BrightPath" | client: BrightPath, hours: 2.5, category: consulting, date: today |
| "Yesterday I spent 45 minutes on admin for Johnson & Co" | client: Johnson & Co, hours: 0.75, category: admin, date: yesterday |
| "4 hrs Acme, homepage wireframes" | client: Acme, hours: 4, description: homepage wireframes |
| "Logged 1 hour meeting with Sarah at Nova Labs" | client: Nova Labs, hours: 1, category: meetings |
| "6 hours last Friday on the BrightPath app" | client: BrightPath, hours: 6, date: last Friday |

**Parsing rules:**

1. **Client matching**: Fuzzy match against `clients.json`. "Acme" matches "Acme Corp". If ambiguous, ask.
2. **Project matching**: Match against active projects for the identified client. If only one active project, auto-select. If multiple, ask.
3. **Hours**: Parse decimals (2.5), fractions (2 and a half), minutes (45 minutes → 0.75).
4. **Date**: Default to today. Parse "yesterday", "last Monday", "March 5th", specific dates.
5. **Category**: Infer from description keywords. "meeting" → meetings, "wireframe" → design.
6. **Billable**: Default true unless category is in `non_billable_categories`.
7. **Rounding**: Apply setting from `settings.json`.

**Always confirm before saving:**
```
✅ Logged: 3.00 hrs — Acme Corp → Website Redesign
   "Homepage wireframe revisions"
   Date: March 10, 2026 | Billable | Rate: $85/hr ($255.00)
```

**Unknown client/project:** Offer to create on the fly. Ask for rate at minimum.

### 2. Start/Stop Timers

For users who prefer real-time tracking:

**Starting a timer:**
- "Start tracking Acme" → Start timer for Acme Corp, prompt for project if multiple active
- "Start timer for BrightPath mobile app" → Start timer for specific project
- "Track time on Johnson consulting" → Start timer

**While running:** Store state in `timers.json`. If user starts a new timer, stop and log the current one first.

**Stopping:** "Stop tracking" / "Stop timer" → Calculate elapsed, round per settings, confirm and log. Prompt for description.

**Pausing:** "Pause timer" saves accumulated time. "Resume" continues.

### 3. Client Database

**Adding a client:**
- "Add a new client: Sarah Chen at Nova Labs, $95/hr, net 15"
- Parse and create the client record
- Ask for any missing required fields (name is minimum)

**Viewing clients:**
- "Show me my clients" → List all active clients with key stats
- "Tell me about Acme" → Full client detail view

**Client detail view:** Show contact info, rate, terms, active/completed project counts, total billed/paid/outstanding, and notes.

**Editing:** "Update Acme's rate to $95/hr", "Archive the Johnson account", etc.

**Client memory:** Proactively surface relevant context — last activity date, payment patterns ("BrightPath usually pays late"), average project size.

### 4. Project Management

**Creating a project:**
- "New project for Acme: Logo Refresh, quoted $2,000, estimated 25 hours"
- "Start a new project — BrightPath wants a landing page, hourly billing"

**Project fields:**
- `billing_type`: "fixed" (quoted price) or "hourly" (open-ended)
- `status`: "active", "paused", "completed"
- Fixed projects track `quoted_price` and `estimated_hours`
- All projects track `hours_logged` and calculate `effective_rate`

**Viewing projects:**
- "Show my active projects" → Summary list
- "How's the Acme redesign going?" → Detailed project view

**Project detail view:** Show status, billing type, hours vs estimate with percentage, effective rate, milestones with status, and recent time entries.

**Updating:** Support milestone completion, status changes (pause/complete), and scope adjustments. When marking complete, calculate final profitability and update client totals.

### 5. Profitability Analysis

**Per-project profitability (fixed-price projects):**

Calculate `effective_rate = quoted_price / hours_logged`.

**Budget alerts — proactive, triggered when logging time:**

- At `budget_alert_threshold` (default 80%): ⚠️ warning with remaining hours, effective rate, and pace estimate
- Over 100%: 🚨 alert with effective rate vs target rate and total "unpaid" dollar amount
- Always show these inline when logging time — don't wait for the user to ask

**Cross-project analysis:**
- "How am I doing on profitability?" → Summary across all active projects
- "Which clients are most profitable?" → Ranked by effective rate
- "Compare my design vs consulting rates" → Category analysis

**Summary format:** List each active project with effective rate, status indicator (✅/⚠️/🚨), and weighted average across all projects vs target rate.

### 6. Timesheet Generation

**Generate timesheets on demand:**
- "Show me last week's timesheet"
- "Generate March timesheet for Acme"
- "Weekly timesheet"
- "What did I work on this month?"

**Markdown format:** Table with Date, Client, Project, Hours, Description, Billable columns. Totals at bottom split by billable/non-billable with dollar amounts.

**CSV export:** Run `scripts/export-timesheet.sh --start YYYY-MM-DD --end YYYY-MM-DD [--client "Name"]`. Output to `~/.freelancer-toolkit/exports/`. Columns: `date,client,project,hours,description,category,billable,rate,amount`.

### 7. InvoiceGen Pro Integration

**Trigger invoice generation:**
- "Invoice Acme for March"
- "Generate invoice for BrightPath, February work"
- "Create invoices for all clients this month"

**Process:**

1. Pull all uninvoiced time entries for the specified client and period
2. Group by project
3. Calculate totals (hours × rate per project)
4. Build invoice data payload:

```json
{
  "client": {
    "name": "Acme Corp",
    "contact": "Jane Smith",
    "email": "jane@acmecorp.com"
  },
  "payment_terms": "net_30",
  "line_items": [
    {
      "description": "Website Redesign — Visual design concepts and revisions",
      "hours": 12.5,
      "rate": 85,
      "amount": 1062.50
    },
    {
      "description": "Website Redesign — Development and testing",
      "hours": 8.0,
      "rate": 85,
      "amount": 680.00
    }
  ],
  "subtotal": 1742.50,
  "total": 1742.50,
  "period": "March 2026"
}
```

5. Present summary with line items, subtotal, and payment terms for user approval
6. On confirmation, pass payload to InvoiceGen Pro skill (if installed)
7. Mark time entries as `invoiced: true` and store `invoice_id`
8. Update client's `total_billed`

**If InvoiceGen Pro is not installed:** Export as JSON to `~/.freelancer-toolkit/exports/invoice-{client}-{period}.json` and suggest installing it.

### 8. Weekly Summary

**Delivered every Monday (or configured day).** Contains:

1. **Total hours** — billable vs non-billable with dollar amounts
2. **By client** — hours and revenue per client
3. **Project status** — budget alerts for fixed-price projects
4. **Unbilled time** — clients with significant uninvoiced hours, with suggested actions
5. **Trend** — comparison to previous week

**Manual trigger:** "Give me my weekly summary" or "How did last week look?"

### 9. Dashboard Integration

The dashboard kit exposes these widgets via `dashboard-kit/manifest.json`:

1. **ft_hours_by_client** — Donut chart of hours logged per client (current month)
2. **ft_weekly_trend** — Bar chart of weekly hours over the past 8 weeks
3. **ft_profitability_table** — Table of active projects with effective rates, budget status
4. **ft_unbilled_alert** — Alert cards showing clients with significant unbilled hours
5. **ft_revenue_pipeline** — Stacked bar showing billed, paid, and outstanding amounts per client

Data sources: Read from `~/.freelancer-toolkit/*.json` files.

See `dashboard-kit/DASHBOARD-SPEC.md` for full widget specifications.

---

## Command Reference

These are conversational triggers, not slash commands. The agent recognizes intent.

### Time Tracking
| User intent | Example |
|-------------|---------|
| Log time | "I worked 3 hours on Acme today" |
| Log with details | "2.5 hrs BrightPath, API integration and testing" |
| Log past date | "Yesterday I did 4 hours on Nova Labs brand guide" |
| Start timer | "Start tracking Acme redesign" |
| Stop timer | "Stop tracking" |
| Pause timer | "Pause timer" |
| Resume timer | "Resume" |
| Check timer | "How long have I been tracking?" |
| Edit entry | "Change today's Acme entry to 3.5 hours" |
| Delete entry | "Delete the Nova Labs entry from yesterday" |

### Clients
| User intent | Example |
|-------------|---------|
| Add client | "New client: Sarah Chen, Nova Labs, $95/hr, net 15" |
| List clients | "Show my clients" |
| Client details | "Tell me about Acme" |
| Update client | "Update Acme's rate to $100/hr" |
| Archive client | "Archive Johnson & Co" |

### Projects
| User intent | Example |
|-------------|---------|
| Create project | "New project for Acme: Logo Refresh, $2,000 fixed, ~25 hours" |
| List projects | "Show active projects" |
| Project status | "How's the Acme redesign going?" |
| Update milestone | "Mark Acme wireframes as done" |
| Complete project | "The BrightPath app is finished" |
| Pause project | "Pause the Nova Labs project" |

### Reports & Invoicing
| User intent | Example |
|-------------|---------|
| Weekly timesheet | "Show me last week's timesheet" |
| Monthly timesheet | "March timesheet" |
| Client timesheet | "Timesheet for Acme, February" |
| Export CSV | "Export March timesheet as CSV" |
| Generate invoice | "Invoice Acme for March" |
| Profitability | "How am I doing on profitability?" |
| Weekly summary | "Give me my weekly summary" |
| Client report | "Billing summary for BrightPath" |

---

## Error Handling

- **Ambiguous client**: "I found 2 clients matching 'Nova' — Nova Labs or Nova Design Co. Which one?"
- **No matching client**: "I don't have a client called 'Zenith'. Want me to create them?"
- **No active timer**: "No timer is running right now. Want to start one?"
- **Timer already running**: "You're currently tracking BrightPath Mobile App (1h 23m). Stop that first, or I'll stop it and start the new one."
- **No time entries for period**: "No time logged for Acme in February. Check the date range?"
- **Over budget**: Always flag proactively. Never silently log time on an over-budget project.
- **Missing data files**: Re-initialize from defaults. Never crash on missing files.
- **Corrupted JSON**: Back up the corrupted file to `*.backup`, re-initialize, and alert the user.

---

## Integration Points

### InvoiceGen Pro (NormieClaw)
- Freelancer Toolkit generates structured invoice data
- InvoiceGen Pro handles formatting, PDF generation, and delivery
- Data passed via JSON export or direct skill-to-skill handoff
- If InvoiceGen Pro is not installed, Freelancer Toolkit exports raw data

### Legal Docs Pro (NormieClaw)
- Proposals and contracts are handled by Legal Docs Pro
- Freelancer Toolkit focuses on post-contract execution: time, billing, profitability
- Client data can be shared between tools via the common data directory

### Export Formats
- **CSV**: Via `export-timesheet.sh` script
- **JSON**: Native format for all data files
- **Markdown**: Timesheets and reports rendered in-chat

---

## Configuration

Edit `~/.freelancer-toolkit/settings.json` to customize:

- `default_hourly_rate`: Applied to new clients unless overridden (default: 75)
- `currency` / `currency_symbol`: Currency for display (default: "USD" / "$")
- `week_start`: "monday" or "sunday" (default: "monday")
- `billing_period`: "weekly", "biweekly", or "monthly" (default: "monthly")
- `categories`: List of time entry categories
- `non_billable_categories`: Categories that default to non-billable
- `weekly_summary_day`: Day of week for auto-summary (default: "monday")
- `invoicegen_integration`: Enable InvoiceGen Pro handoff (default: true)
- `rounding`: "none", "nearest_quarter", "nearest_tenth", "round_up_quarter" (default: "nearest_quarter")

---

## Best Practices for Agents

1. **Always confirm time entries** before saving. Show parsed data and let the user correct.
2. **Proactively flag budget issues.** Don't wait for the user to ask — if a project is approaching its budget, mention it when logging time.
3. **Remember client context.** When discussing a client, reference their payment history, preferences, and recent activity.
4. **Suggest invoicing.** If a client has 20+ uninvoiced hours, mention it.
5. **Keep summaries scannable.** Use emoji indicators (✅ ⚠️ 🚨) for quick visual parsing.
6. **Default to billable.** Unless the category is explicitly non-billable, assume time is billable.
7. **Handle edge cases gracefully.** Midnight crossovers, timezone considerations, partial hours — round and confirm.
8. **Back up before destructive operations.** Deleting entries or archiving clients should create backups.

---

## File Locations

| File | Path |
|------|------|
| Settings | `~/.freelancer-toolkit/settings.json` |
| Clients | `~/.freelancer-toolkit/clients.json` |
| Projects | `~/.freelancer-toolkit/projects.json` |
| Time entries | `~/.freelancer-toolkit/time-entries.json` |
| Active timer | `~/.freelancer-toolkit/timers.json` |
| Exports | `~/.freelancer-toolkit/exports/` |
| Setup script | `<skill_dir>/scripts/setup.sh` |
| Export script | `<skill_dir>/scripts/export-timesheet.sh` |
| Report script | `<skill_dir>/scripts/client-report.sh` |
