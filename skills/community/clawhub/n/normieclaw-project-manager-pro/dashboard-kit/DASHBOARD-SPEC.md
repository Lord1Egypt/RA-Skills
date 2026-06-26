# Project Manager Pro — Dashboard Specification

## Overview

Project Manager Pro exposes 7 dashboard widgets for the NormieClaw dashboard system. All widgets use the `pm_` prefix and read from the local JSON data stores.

## Data Sources

| File | Path | Content |
|------|------|---------|
| `tasks.json` | `~/.openclaw/workspace/pm-pro/tasks.json` | All active tasks |
| `projects.json` | `~/.openclaw/workspace/pm-pro/projects.json` | All projects |
| `check-in-log.json` | `~/.openclaw/workspace/pm-pro/check-in-log.json` | Check-in history |

## Widget Specifications

### pm_today — Today's Tasks

**Type:** task-list
**Size:** 2×2
**Refresh:** Every 15 minutes

Displays all tasks due today plus any overdue tasks. Each task row shows:
- Priority badge (colored dot: 🔴 P1, 🟡 P2, 🟠 P3, ⚪ P4)
- Task title (truncated to 60 chars)
- Status icon (🔲 todo, 🔄 in-progress, 🚫 blocked)
- Time estimate if available
- "OVERDUE" badge in red for past-due tasks

**Sort order:** Priority (P1 first), then due date ascending.

**Empty state:** "Nothing due today — enjoy it or add something."

### pm_overdue — Overdue Alerts

**Type:** alert-list
**Size:** 1×1
**Refresh:** Every 30 minutes

Red-themed alert widget showing tasks past their due date. Each row:
- Task title
- Days overdue (e.g., "3 days late")
- Priority badge

**Sort order:** Days overdue descending (oldest first).

**Empty state:** Green checkmark with "All caught up."

**Behavior:** Widget border pulses red when items exist. Static green border when empty.

### pm_progress — Weekly Progress

**Type:** progress-bar
**Size:** 2×1
**Refresh:** Every 30 minutes

Horizontal progress bar showing completed tasks vs total tasks due this week (Monday–Sunday).

**Display:**
- Green fill bar proportional to completion percentage
- Text overlay: "8/14 done (57%)"
- Below bar: "Week of March 8–14"

**Color thresholds:**
- 0-33%: Red (#e53e3e)
- 34-66%: Yellow (#ecc94b)
- 67-100%: Green (#38a169)

### pm_project_status — Project Status

**Type:** multi-bar
**Size:** 2×2
**Refresh:** Every 60 minutes

Shows completion bars for each active project. Each row:
- Project name (truncated to 40 chars)
- Horizontal bar showing completed/total tasks
- Fraction text: "8/23 tasks"
- Target date badge if set

**Sort order:** Lowest completion percentage first (most attention needed).

**Max display:** 6 projects. If more exist, show "and N more..." link.

**Empty state:** "No active projects. Tell your agent to create one."

### pm_trends — Completion Trends

**Type:** line-chart
**Size:** 2×2
**Refresh:** Every 60 minutes

Line chart showing tasks completed per day. Toggle between 7-day and 30-day views.

**Chart elements:**
- X-axis: Dates (abbreviated: "Mar 5", "Mar 6", etc.)
- Y-axis: Task count (integer, starts at 0)
- Primary line: Tasks completed (purple, #805ad5)
- Dashed line: 7-day rolling average
- Hover tooltip: "Mar 11: 5 tasks completed"

**Empty state (< 3 days of data):** "Complete a few more tasks to see your trend."

### pm_priority_dist — Priority Distribution

**Type:** donut-chart
**Size:** 1×1
**Refresh:** Every 60 minutes

Donut chart showing active (non-done) task count by priority.

**Segments:**
- P1 Critical: Red (#e53e3e)
- P2 High: Yellow (#ecc94b)
- P3 Medium: Orange (#ed8936)
- P4 Low: Gray (#a0aec0)

**Center text:** Total active task count.

**Legend:** Below chart, compact format: "P1: 3 · P2: 7 · P3: 12 · P4: 4"

### pm_upcoming — Upcoming Timeline

**Type:** timeline
**Size:** 3×1
**Refresh:** Every 30 minutes

Horizontal 7-day timeline showing upcoming tasks grouped by date.

**Display:**
- 7 columns (today through +6 days)
- Column headers: Day name + date ("Wed 11", "Thu 12", etc.)
- Task pills within each column showing title (truncated) and priority dot
- Today's column highlighted with subtle background

**Interaction:** Hovering a task pill shows full title, project, and time estimate.

**Empty state:** "Clear week ahead."

## Integration Notes

- Widgets read directly from the JSON files — no API layer required
- The agent updates JSON files during conversation, so widgets reflect near-real-time state
- Archive files are NOT read by dashboard widgets — only active tasks/projects
- All timestamps are in the user's configured timezone
- Widget refresh intervals are suggestions — the dashboard system may adjust based on visibility

## Color Palette

| Usage | Hex | Name |
|-------|-----|------|
| P1 / Critical / Overdue | #e53e3e | Red |
| P2 / High | #ecc94b | Yellow |
| P3 / Medium | #ed8936 | Orange |
| P4 / Low / Inactive | #a0aec0 | Gray |
| Completed / On-track | #38a169 | Green |
| Projects / Info | #4299e1 | Blue |
| Trends / Charts | #805ad5 | Purple |
| Background | #1a202c | Dark |
| Card surface | #2d3748 | Dark Gray |
| Text primary | #e2e8f0 | Light |
| Text secondary | #a0aec0 | Muted |
