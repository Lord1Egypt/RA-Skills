# Freelancer Toolkit — Dashboard Specification

All widgets read from `~/.freelancer-toolkit/` JSON files. No external API calls.

---

## Widget: ft_hours_by_client

**Type:** Donut chart
**Size:** Medium (400×400)
**Data:** `time-entries.json` + `clients.json`

**Logic:**
1. Filter `time-entries.json` for current calendar month
2. Group by `client_id`, sum `hours`
3. Resolve client names from `clients.json`
4. Include a "Non-billable" segment for entries where `billable: false` and no client
5. Sort segments largest to smallest

**Display:**
- Center label: total hours for the month
- Segments colored by client (assign consistent colors based on client creation order)
- Legend below chart with client name and hours
- Hover/tooltip shows hours and percentage

---

## Widget: ft_weekly_trend

**Type:** Stacked bar chart
**Size:** Wide (800×300)
**Data:** `time-entries.json`

**Logic:**
1. Calculate the last 8 complete weeks (Monday–Sunday based on `settings.json` week_start)
2. For each week, sum billable and non-billable hours separately
3. X-axis: week labels ("Mar 3–9", "Feb 24–Mar 2", etc.)
4. Y-axis: hours

**Display:**
- Billable hours: primary color (blue)
- Non-billable hours: secondary color (gray)
- Stacked bars
- Horizontal reference line at user's target weekly hours (if set in settings, default 40)
- Labels on each bar showing total hours

---

## Widget: ft_profitability_table

**Type:** Table
**Size:** Wide (800×auto)
**Data:** `projects.json` + `time-entries.json` + `clients.json`

**Columns:**

| Column | Source | Format |
|--------|--------|--------|
| Project | `projects.json` → `name` | Text |
| Client | `clients.json` → `name` (via `client_id`) | Text |
| Type | `projects.json` → `billing_type` | "Fixed" or "Hourly" |
| Quoted | `projects.json` → `quoted_price` | Currency (blank for hourly) |
| Hours | Sum of `time-entries.json` where `project_id` matches | Decimal (1 place) |
| Budget | `hours_logged / estimated_hours × 100` | Percentage (blank for hourly) |
| Eff. Rate | Fixed: `quoted_price / hours_logged`. Hourly: `hourly_rate` | Currency |
| Status | Derived from budget percentage | Emoji indicator |

**Status indicators:**
- ✅ Under 80% of budget (or hourly project)
- ⚠️ 80–100% of budget
- 🚨 Over 100% of budget

**Sorting:** Active projects first, sorted by budget percentage descending (most urgent at top).

**Row styling:**
- Over budget rows: light red background
- At risk rows (80%+): light yellow background
- On track: no highlight

---

## Widget: ft_unbilled_alert

**Type:** Alert cards
**Size:** Medium (400×auto)
**Data:** `time-entries.json` + `clients.json`

**Logic:**
1. For each client, sum hours where `invoiced: false` and `billable: true`
2. Filter to clients exceeding `threshold_hours` (default: 20 from manifest)
3. Calculate estimated unbilled amount (hours × client default rate)
4. Calculate days since the client's last invoiced entry

**Card layout:**
```
┌──────────────────────────────┐
│ 🔔 Acme Corp                │
│ 29.0 unbilled hours         │
│ ~$2,465.00 estimated        │
│ Last invoiced: 34 days ago  │
│ [Generate Invoice →]        │
└──────────────────────────────┘
```

**Sorting:** Highest unbilled amount first.

**Empty state:** "All caught up — no clients with significant unbilled hours."

---

## Widget: ft_revenue_pipeline

**Type:** Stacked horizontal bar chart
**Size:** Wide (800×auto, scales with client count)
**Data:** `clients.json` + `time-entries.json` + `projects.json`

**Logic:**
Per client, calculate three segments:
1. **Paid** (green): `total_paid` from `clients.json`
2. **Billed, unpaid** (yellow): `total_billed - total_paid`
3. **Unbilled** (red): Sum of `hours × rate` for all entries where `invoiced: false` and `billable: true`

**Display:**
- One horizontal bar per active client
- Three color segments per bar
- Labels showing dollar amounts per segment
- Total at the end of each bar
- Y-axis: client names
- X-axis: dollar amounts

**Summary row at bottom:**
- Total paid | Total outstanding | Total unbilled
- Overall pipeline total

---

## Color Palette

| Element | Color | Hex |
|---------|-------|-----|
| Primary (billable/paid) | Blue | #3B82F6 |
| Secondary (non-billable) | Gray | #9CA3AF |
| Warning (at risk) | Amber | #F59E0B |
| Danger (over budget/unbilled) | Red | #EF4444 |
| Success (on track/paid) | Green | #10B981 |
| Billed unpaid | Yellow | #FBBF24 |
| Background | White | #FFFFFF |
| Text | Dark gray | #1F2937 |

---

## Refresh Behavior

- Widgets with `refresh_interval: "1h"` re-read data files hourly
- Widgets with `refresh_interval: "6h"` re-read every 6 hours
- All widgets should handle missing or empty data files gracefully
- If a data file is missing, show "Run setup to get started" in the widget area
