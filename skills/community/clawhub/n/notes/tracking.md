# Action Item Tracking — Notes

## Central Tracker: `~/notes/actions.md`

Single source of truth for all action items across all notes.

```markdown
# Action Items Tracker

**Last updated:** YYYY-MM-DD HH:MM

## 🔴 Overdue

| # | Action | Owner | Due | Source | Days Late |
|---|--------|-------|-----|--------|-----------|
| 1 | [Task] | @name | YYYY-MM-DD | [[note-link]] | X days |

## 🟡 Due This Week

| # | Action | Owner | Due | Source |
|---|--------|-------|-----|--------|
| 1 | [Task] | @name | YYYY-MM-DD | [[note-link]] |

## 🟢 Upcoming

| # | Action | Owner | Due | Source |
|---|--------|-------|-----|--------|
| 1 | [Task] | @name | YYYY-MM-DD | [[note-link]] |

## ✅ Recently Completed

| # | Action | Owner | Completed | Source |
|---|--------|-------|-----------|--------|
| 1 | [Task] | @name | YYYY-MM-DD | [[note-link]] |

---
*Auto-generated from notes. Run "update actions" to refresh.*
```

---

## Tracking Rules

### 1. Sync on Every Note
After creating any note with action items:
1. Add new items to `actions.md`
2. Include source link `[[YYYY-MM-DD_note-name]]`
3. Set status based on due date

### 2. Status Definitions

| Status | Criteria | Action |
|--------|----------|--------|
| 🔴 OVERDUE | Due date passed | Escalate or reschedule |
| 🟡 DUE SOON | Within 3 days | Prioritize |
| 🟢 UPCOMING | More than 3 days | Track |
| ✅ DONE | Completed | Move to completed section |
| ⏸️ BLOCKED | Waiting on dependency | Note blocker |

### 3. Daily Review Prompt
When user starts day or asks for status:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 ACTION ITEMS — YYYY-MM-DD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 OVERDUE (X items)
1. [Task] — was due YYYY-MM-DD (X days ago)
   Source: [[note-link]]

🟡 DUE TODAY/THIS WEEK (X items)
1. [Task] — due YYYY-MM-DD
   Source: [[note-link]]

📊 Summary: X overdue | Y due soon | Z upcoming
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 4. Completing Items
When user marks item done:

```
✅ Marked complete: [Task]
   Originally from: [[YYYY-MM-DD_meeting-name]]
   Completed: YYYY-MM-DD

📋 Remaining: X overdue | Y due soon | Z upcoming
```

### 5. Rescheduling
When deadline needs to change:

```
📅 Rescheduled: [Task]
   Original due: YYYY-MM-DD
   New due: YYYY-MM-DD
   Reason: [brief note]
```

---

## Owner Tracking

### By Person View
Generate on request:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 @alice — 5 open items
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 Review proposal — was due Feb 15
🟡 Send feedback — due Feb 20
🟢 Schedule call — due Feb 25
🟢 Draft report — due Mar 1
🟢 Plan Q2 — due Mar 15
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### My Items Filter
For personal focus:

```
"Show my action items"
→ Filter actions.md for @me or user's name
→ Display grouped by status
```

---

## Escalation Rules

### Auto-Escalation Triggers

| Condition | Action |
|-----------|--------|
| 1 day overdue | Add ⚠️ flag |
| 3 days overdue | Add 🚨 flag, suggest follow-up |
| 7 days overdue | Suggest reschedule or cancel |

### Follow-Up Prompts

```
🚨 Item overdue by 3+ days:
   "[Task]" — @owner — was due YYYY-MM-DD

   Options:
   1. "done" — Mark complete
   2. "reschedule [date]" — New deadline
   3. "blocked [reason]" — Mark blocked
   4. "cancel" — Remove item
```

---

## Weekly Review

Generate on request or every Monday:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 WEEKLY ACTION REVIEW — Week of YYYY-MM-DD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ COMPLETED THIS WEEK: X items
   - [Task 1] — completed Mon
   - [Task 2] — completed Wed

📈 COMPLETION RATE: X%
   (X of Y items due this week)

🔴 CARRIED OVER: X items
   - [Task] — now X days overdue

🎯 DUE NEXT WEEK: X items
   - [Task 1] — Mon
   - [Task 2] — Wed
   - [Task 3] — Fri

👤 BY OWNER:
   @alice: 3 done, 2 pending
   @bob: 1 done, 4 pending
   @me: 5 done, 1 pending
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Integration Commands

| Command | Action |
|---------|--------|
| "show actions" | Display current action items |
| "my actions" | Filter to user's items |
| "overdue" | Show only overdue items |
| "due this week" | Show items due in 7 days |
| "@name actions" | Show items for specific person |
| "update actions" | Rescan all notes, rebuild tracker |
| "weekly review" | Generate weekly summary |
