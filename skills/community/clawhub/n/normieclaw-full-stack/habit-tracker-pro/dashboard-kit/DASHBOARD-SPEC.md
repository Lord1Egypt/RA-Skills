# Habit Tracker Pro — Dashboard Specification

## Widget Prefix

All widget IDs use the `ht_` prefix.

---

## ht_habit_grid — Contribution Chart

**Type:** Grid / Heatmap
**Size:** Full width (12 cols) × 4 rows

A GitHub-style contribution grid. Each row is one habit. Each column is one day.
Cells are color-coded by completion status.

**Layout:**
- Y-axis: habit names (sorted by category, then alphabetical)
- X-axis: dates (most recent on the right)
- Default view: last 90 days (scrollable left for more history)

**Cell Colors:**
- ██ Completed: `#22c55e` (green-500) — opacity scales with streak length
- ░░ Missed (scheduled): `#94a3b8` (slate-400)
- ·· Not scheduled: transparent / `#1e293b` (slate-800)
- 🧊 Frozen: `#38bdf8` (sky-400) — streak freeze days

**Interactions:**
- Hover/tap: shows date, habit name, completion status, and any note
- Click habit name: jumps to that habit's detail view

**Data Source:** `completions.json` + `habits.json`

---

## ht_streak_board — Streak Leaderboard

**Type:** Ranked table
**Size:** Half width (6 cols) × 3 rows

Your habits competing against each other. Ranked by current streak.

**Columns:**
| Rank | Habit | Current Streak | Longest Streak | 30-Day Rate |
|------|-------|---------------|----------------|-------------|

**Special Indicators:**
- 🔥 Active streaks within 3 days of longest-ever → highlight row
- 🏆 New personal best streak → badge on the row
- ↗️ Trending up (last 7-day rate > last 30-day rate)
- ↘️ Trending down (last 7-day rate < last 30-day rate by 15%+)

**Data Source:** `habits.json` + `streaks.json`

---

## ht_weekly_trends — Trend Lines

**Type:** Multi-line chart
**Size:** Half width (6 cols) × 3 rows

Completion rate per habit, plotted weekly over the last 8 weeks.

**Axes:**
- X: Week (labeled "Mar 3–9", "Mar 10–16", etc.)
- Y: Completion rate 0–100%

**Lines:**
- One line per active habit, color-coded by category
- Dashed line for overall average across all habits
- Line thickness: thicker for habits with more scheduled days

**Reference Lines:**
- 80% threshold (subtle dashed green) — "strong" territory
- 50% threshold (subtle dashed yellow) — "needs attention"

**Interactions:**
- Hover line: shows exact rate and completion count for that week
- Click legend item: toggle habit visibility on/off

**Data Source:** `completions.json` + `habits.json`

---

## ht_pattern_insights — Insight Cards

**Type:** Card list
**Size:** Half width (6 cols) × 2 rows

Top 3-5 insights from the most recent pattern analysis. Each insight is a card.

**Card Structure:**
```
┌──────────────────────────────────────┐
│ 📊 Friday is your weakest day        │
│                                      │
│ 38% completion vs 74% average.       │
│ Reading: 1/5 Fridays. Gym: 2/5.     │
│                                      │
│ Detected: Mar 8 · Confidence: High   │
└──────────────────────────────────────┘
```

**Card Types:**
- **Day pattern:** Weak/strong days of the week
- **Correlation:** Two habits that move together
- **Skip cluster:** Recurring skip patterns with context
- **Recovery:** Streak recovery speed analysis
- **Trend shift:** Significant improvement or decline

**Refresh:** Weekly after pattern analysis runs, or on demand.

**Data Source:** `patterns.json`

---

## ht_daily_summary — Today's Status

**Type:** Status list
**Size:** Half width (6 cols) × 2 rows

What's done, what's pending, what's missed for today.

**Layout:**
```
Today — March 11, 2026

✅ Morning Meditation (8:14 AM)
✅ Supplements (8:20 AM)
✅ Gym Session (via Trainer Buddy)
⏳ Reading (30 min) — evening
⏳ Journaling — evening
```

**Status Icons:**
- ✅ Completed (with timestamp)
- ⏳ Pending (scheduled for later)
- ❌ Missed (past scheduled time, not completed)
- 🧊 Frozen (streak freeze active)
- 🔄 Auto-completed (via cross-tool sync, shows source)

**Progress Bar:** Visual bar at the top showing X/Y complete.

**Data Source:** `completions.json` + `habits.json` (filtered to today)

---

## ht_category_breakdown — Category Performance

**Type:** Horizontal bar chart
**Size:** Half width (6 cols) × 2 rows

Completion rates grouped by habit category. Quick read on which areas of life
are getting attention and which are falling behind.

**Layout:**
```
Fitness     ████████████████████░░░░  82%
Wellness    █████████████████░░░░░░░  74%
Learning    ██████████████░░░░░░░░░░  58%
Nutrition   ████████████░░░░░░░░░░░░  51%
```

**Colors:** Each category gets a distinct color from the theme.

**Time Range Toggle:** 7 days / 30 days / 90 days (default: 30 days)

**Data Source:** `completions.json` + `habits.json`

---

## Layout Grid

Default dashboard layout (12-column grid):

```
Row 1-4:  [ht_habit_grid ———————————————————————————]  (12 cols)
Row 5-7:  [ht_streak_board ————] [ht_weekly_trends ————]  (6+6 cols)
Row 8-9:  [ht_pattern_insights ] [ht_daily_summary ————]  (6+6 cols)
Row 10-11:[ht_category_breakdown] [empty / future widget]  (6+6 cols)
```

---

## Data Refresh

- Widgets refresh every 60 minutes by default (configurable in manifest).
- `ht_daily_summary` refreshes on every page load.
- `ht_pattern_insights` refreshes after weekly pattern analysis.
- Manual refresh available via dashboard controls.

---

*Habit Tracker Pro Dashboard Kit — NormieClaw · normieclaw.ai*
