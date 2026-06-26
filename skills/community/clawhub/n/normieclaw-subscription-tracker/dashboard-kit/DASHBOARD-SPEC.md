# Dashboard Spec — Subscription Tracker

> Widget specifications for the NormieClaw dashboard integration.

---

## Overview

The Subscription Tracker publishes 8 widgets to the NormieClaw dashboard. All widgets read from `~/.normieclaw/subscription-tracker/subscriptions.json` and use the `st_` prefix.

Refresh interval: daily (or on-demand after statement scans).

---

## Widget Specifications

### st_monthly_spend — Monthly Subscription Total

**Type:** Stat card
**Size:** Small (1x1)

Displays the total monthly cost of all active subscriptions. Annual subscriptions are divided by 12 and included in the total.

**Calculation:**
```
monthly = sum of all active subscriptions where frequency = "monthly"
annual_monthly = sum of all active subscriptions where frequency = "annual" / 12
weekly_monthly = sum of all active subscriptions where frequency = "weekly" * 4.33
total = monthly + annual_monthly + weekly_monthly
```

**Display:** `$187.43` with trend arrow comparing to previous month.
**Trend:** Lower is better (green arrow down, red arrow up).

---

### st_annual_spend — Annual Projected Spend

**Type:** Stat card
**Size:** Small (1x1)

Projects total annual subscription spend based on current active subscriptions.

**Calculation:**
```
annual = sum of all active monthly subscriptions * 12
       + sum of all active annual subscriptions
       + sum of all active weekly subscriptions * 52
```

**Display:** `$2,249.16`
**Trend:** Lower is better.

---

### st_sub_count — Active Subscription Count

**Type:** Stat card
**Size:** Small (1x1)

Count of all subscriptions with `status: "active"`.

**Display:** `12`
**Trend:** Neutral (no color coding).

---

### st_savings — Annual Savings from Cancellations

**Type:** Stat card
**Size:** Small (1x1)

Sum of `annual_savings` from all entries in the `cancelled` array.

**Calculation:**
```
savings = sum of cancelled[].annual_savings
```

**Display:** `$719.88` in green.
**Trend:** Higher is better (always green). Highlight color: `#22c55e`.

---

### st_category_breakdown — Spend by Category (Pie Chart)

**Type:** Pie chart
**Size:** Medium (2x1)

Groups active subscriptions by category and sums their monthly amounts. Each category gets a consistent color from the manifest.

**Segments:** One per category with at least one active subscription.
**Labels:** Category name + dollar amount + percentage.
**Sort:** Largest segment first (clockwise).

**Example segments:**
- 🎬 Streaming: $45.97 (25%)
- 💪 Fitness: free.99 (27%)
- 🤖 AI Tools: $20.00 (11%)
- 🔧 Productivity: $42.50 (23%)
- 🎵 Music: $11.99 (6%)
- ☁️ Cloud: $2.99 (2%)
- 📰 News: $13.99 (7%)

---

### st_upcoming_renewals — Upcoming Renewals List

**Type:** List/table
**Size:** Medium (2x1)

Shows all active subscriptions with `next_renewal` within the next 7 days, sorted by date.

**Columns:**
| Column | Source | Format |
|--------|--------|--------|
| Date | `next_renewal` | MMM DD |
| Service | `service` | Text |
| Amount | `amount` | $XX.XX |

**Max items:** 10
**Empty state:** "No renewals in the next 7 days ✅"
**Footer:** Total amount of upcoming renewals.

---

### st_price_changes — Recent Price Changes

**Type:** List/table
**Size:** Medium (2x1)

Shows subscriptions where the current amount differs from the previous charge (detected via `previous_amounts` array).

**Columns:**
| Column | Source | Format |
|--------|--------|--------|
| Service | `service` | Text |
| Was | `previous_amounts[-2]` | $XX.XX |
| Now | `amount` | $XX.XX |
| Change | calculated | +$X.XX (red) or -$X.XX (green) |

**Max items:** 5
**Empty state:** "No price changes detected"

---

### st_trend — Monthly Spend Trend (Line Chart)

**Type:** Line chart
**Size:** Large (2x2)

Shows total monthly subscription spend over the last 6 months. Requires the agent to maintain a `monthly_totals` history in the database (appended each month during the monthly summary).

**X-axis:** Month labels (Oct, Nov, Dec, Jan, Feb, Mar)
**Y-axis:** Dollar amount ($0 – auto-scaled max)
**Line color:** `#3b82f6` (blue)
**Data points:** Show value on hover.
**Annotations:** Mark months where subscriptions were added or cancelled.

**Data structure (stored in subscriptions.json):**
```json
{
  "monthly_totals": [
    { "month": "2025-10", "total": 156.43, "count": 10 },
    { "month": "2025-11", "total": 162.43, "count": 11 },
    { "month": "2025-12", "total": 162.43, "count": 11 },
    { "month": "2026-01", "total": 187.43, "count": 12 },
    { "month": "2026-02", "total": 187.43, "count": 12 },
    { "month": "2026-03", "total": 127.44, "count": 9 }
  ]
}
```

---

## Layout Recommendation

Dashboard grid layout (4 columns):

```
┌──────────────┬──────────────┬──────────────┬──────────────┐
│ st_monthly   │ st_annual    │ st_sub_count │ st_savings   │
│ $187.43      │ $2,249.16    │ 12           │ $719.88      │
├──────────────┴──────────────┼──────────────┴──────────────┤
│ st_category_breakdown       │ st_upcoming_renewals        │
│ [pie chart]                 │ Mar 27 Spotify    $11.99    │
│                             │ Mar 28 Adobe CC   $59.99    │
│                             │ Mar 30 NordVPN    $12.99    │
├──────────────┬──────────────┴──────────────────────────────┤
│ st_price     │ st_trend                                    │
│ changes      │ [line chart - 6 month trend]                │
│              │                                             │
└──────────────┴─────────────────────────────────────────────┘
```

---

## Data Refresh

Widgets refresh when:
1. **Daily cron:** `renewal-check.sh` runs and updates renewal dates
2. **Statement scan:** User uploads a new statement, triggering a full database update
3. **Manual action:** User adds, cancels, or modifies a subscription
4. **Monthly summary:** First of each month, monthly totals history is updated

The agent should update `subscriptions.json` → `last_updated` timestamp after any modification. Dashboard reads this field to determine if a refresh is needed.
