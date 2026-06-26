# Meeting Scheduler Pro — Dashboard Specification

## Overview

Meeting Scheduler Pro provides dashboard visualizations for meeting patterns, prep habits, and follow-up tracking. All metrics use the `ms_` prefix.

---

## Visualizations

### 1. Weekly Meeting Heatmap

**Type:** Grid heatmap
**Axes:** X = hour of day (8 AM – 6 PM), Y = day of week (Mon – Fri)
**Color scale:** White (0 meetings) → Light blue (1) → Dark blue (3+)
**Data source:** Rolling 30-day meeting frequency by day/hour
**Purpose:** Identify your busiest time slots at a glance. Reveals patterns like "Tuesdays at 10 AM always have meetings" or "Friday afternoons are consistently free."

### 2. Meeting Frequency Trend

**Type:** Line chart
**X-axis:** Week (last 12 weeks)
**Y-axis:** Total meetings per week
**Reference line:** Your max_meetings_per_day × 5 (weekly capacity)
**Purpose:** Track whether meeting load is increasing, stable, or decreasing. Weeks above the reference line indicate overload.

### 3. Prep Completion Tracker

**Type:** Stacked bar chart
**X-axis:** Week (last 8 weeks)
**Y-axis:** Meeting count
**Segments:** Prepped (green) vs. Not prepped (gray)
**Annotation:** Prep rate percentage above each bar
**Purpose:** Track how consistently you're reviewing prep briefs before meetings. Declining rates may indicate the agent isn't generating useful briefs or you're too busy to review.

### 4. Follow-Up Pipeline

**Type:** Horizontal bar chart (kanban-inspired)
**Categories:**
- Pending (yellow) — action items created, not yet done
- Completed (green) — action items marked done
- Overdue (red) — past due date, still open
**Data:** Rolling 30-day action items from meeting follow-ups
**Purpose:** Track follow-through on meeting commitments. High overdue counts signal a capacity problem or dropped balls.

### 5. Calendar Health Score

**Type:** Single number + radial gauge
**Score:** 0–100, composite of:
- Buffer compliance (25% weight) — meetings with proper buffer time
- Daily limit compliance (25% weight) — days under max_meetings_per_day
- Focus time protection (25% weight) — no-meeting blocks respected
- Follow-up completion (25% weight) — action items completed on time
**Color:** Green (80+), Yellow (60–79), Red (below 60)
**Purpose:** At-a-glance calendar health. One number to answer "am I managing my meeting load well?"

### 6. Top Contacts by Meeting Frequency

**Type:** Horizontal bar chart
**Data:** Top 10 people you meet with most frequently (last 90 days)
**Bars:** Meeting count per contact
**Annotation:** Last meeting date for each
**Purpose:** See who dominates your calendar. Useful for auditing whether your meeting time aligns with priorities.

### 7. Meeting Duration Distribution

**Type:** Pie chart or donut chart
**Segments:** 15 min, 30 min, 45 min, 60 min, 60+ min
**Data:** Last 30 days of meetings by duration
**Purpose:** Understand your meeting length patterns. If 80% of meetings are 60 min, consider whether 30-min defaults would reclaim time.

---

## Metric Collection

Metrics are collected by the agent during normal operation:

| Metric | Collection Trigger |
|--------|--------------------|
| `ms_meetings_today` / `ms_meetings_week` | Calendar query during morning brief or on-demand |
| `ms_prep_rate` | Tracked when prep briefs are generated vs meetings held |
| `ms_followups_pending` / `ms_followups_done` | Updated when tasks are created/completed |
| `ms_avg_daily` | Calculated from 30-day meeting history |
| `ms_busiest_day` / `ms_busiest_hour` | Calculated from 30-day meeting history |
| `ms_noshow_rate` | Tracked when user reports a no-show or meeting cancellation |
| `ms_buffer_compliance` | Checked during calendar health audits |
| `ms_agent_booked` | Incremented when agent creates a calendar event |
| `ms_rescheduled` | Incremented when agent moves an existing event |

Metrics persist in the dashboard data store (managed by the NormieClaw dashboard framework). Historical data is retained for trending.

---

## Refresh Cadence

- **Real-time metrics** (meetings today, pending follow-ups): refreshed every 15 minutes or on interaction
- **Aggregated metrics** (trends, heatmap, health score): refreshed daily during morning brief
- **Historical metrics** (12-week trends): recalculated weekly
