# Project Manager Pro — SKILL.md

> Conversational task & project management for OpenClaw agents.
> Your agent creates, organizes, prioritizes, and follows up on tasks — no UI required.

---

## Trigger Phrases

Use this skill when the user:
- Asks to add, create, or schedule a task/project/to-do
- Says something like "I need to...", "remind me to...", "don't let me forget..."
- Asks "what's on my plate?", "what should I work on?", "what's due?"
- Requests a project breakdown ("break this down", "plan out X")
- Responds to a proactive check-in (morning/evening/weekly)
- Mentions priorities, deadlines, blockers, or task status
- Says "mark X as done", "I finished X", "block X", "move X to in-progress"
- Asks to see tasks by project, priority, tag, or timeframe
- Requests task export or weekly review

Do NOT use this skill for:
- Calendar scheduling (use calendar tools)
- Team task assignment or collaboration
- Time tracking or Pomodoro sessions
- General reminders without actionable task context

---

## 1. Data Model

### Task Structure

Every task is stored as a JSON object in the tasks database file at `~/.openclaw/workspace/pm-pro/tasks.json`.

```json
{
  "id": "task_20260311_001",
  "title": "Research co-packing facilities in Denver",
  "description": "Find 3+ co-packers that handle hot sauce bottling, get quotes, compare MOQs",
  "priority": "P2",
  "eisenhower": "important-not-urgent",
  "status": "todo",
  "due_date": "2026-03-18",
  "created_date": "2026-03-11",
  "completed_date": null,
  "project": "teekha-launch",
  "parent_task": null,
  "subtasks": ["task_20260311_002", "task_20260311_003", "task_20260311_004"],
  "dependencies": [],
  "blocked_by": [],
  "tags": ["teekha", "vendor", "research"],
  "time_estimate_min": 120,
  "notes": "Cody mentioned preference for facilities within 2-hour drive",
  "source": "user",
  "recurrence": null
}
```

### Project Structure

Projects are stored in `~/.openclaw/workspace/pm-pro/projects.json`:

```json
{
  "id": "teekha-launch",
  "name": "Teekha Foods Launch",
  "description": "Launch 3 SKU hot sauce line by Q2 2026",
  "status": "active",
  "created_date": "2026-03-01",
  "target_date": "2026-06-30",
  "tags": ["teekha", "cpg", "launch"],
  "task_count": 0,
  "completed_count": 0
}
```

### File Layout

```
~/.openclaw/workspace/pm-pro/
├── tasks.json          # All tasks (array)
├── projects.json       # All projects (array)
├── archive/            # Completed tasks moved here monthly
│   └── 2026-03.json
└── check-in-log.json   # Record of check-ins delivered
```

---

## 2. Conversational Task Creation

### Parsing Natural Language

When the user says something that implies a task, parse it into structured data. Use these patterns:

**Direct task creation:**
- "Add a task to call the dentist by Friday" → title: "Call the dentist", due: next Friday, priority: P3
- "I need to file taxes by April 15" → title: "File taxes", due: 2026-04-15, priority: P1 (deadline-driven)
- "Don't forget to buy groceries" → title: "Buy groceries", priority: P3, no due date
- "Remind me to review the pitch deck tomorrow morning" → title: "Review the pitch deck", due: tomorrow

**Project creation:**
- "I need to launch a website by March 20" → Create project + subtask tree (see Section 3)
- "Plan a trip to Japan for October" → Create project + subtask tree
- "Break down the hot sauce launch" → Create project + subtask tree

### Parsing Rules

1. **Extract the action verb.** The task title should start with a verb: "Call," "Buy," "Review," "Research," "Send," "Schedule."
2. **Detect due dates.** Parse relative dates ("tomorrow," "next Friday," "end of month") and absolute dates ("March 20," "April 15"). Resolve relative dates against today's date.
3. **Infer priority from urgency signals:**
   - P1: "urgent," "ASAP," "critical," "today," "overdue," deadline within 24 hours
   - P2: "important," "this week," "high priority," deadline within 7 days
   - P3: Default for most tasks
   - P4: "whenever," "low priority," "someday," "nice to have"
4. **Detect project association.** If the task references an existing project name or tag, associate it automatically.
5. **Ask clarifying questions when ambiguous** — but keep it to one question max. Don't interrogate.

### Response Format for Task Creation

After creating a task, confirm concisely:

```
✅ Added: "Call the dentist"
   📅 Due: Friday, Mar 13 · 🔴 P2 · 🏷 health
```

For projects with subtasks, show the tree:

```
📁 New project: Launch Website (due Mar 20)

├── 🔲 Finalize homepage copy (Mar 12) · P2
├── 🔲 Design landing page mockup (Mar 13) · P2
│   └── 🔲 Get feedback from stakeholders (Mar 14) · P3
├── 🔲 Set up hosting and domain (Mar 14) · P2
├── 🔲 Develop and deploy site (Mar 15-18) · P1
│   ├── 🔲 Build responsive layout (Mar 15-16) · P2
│   └── 🔲 Integrate contact form (Mar 16) · P3
├── 🔲 QA testing across devices (Mar 18) · P1
└── 🔲 Go live and verify DNS (Mar 20) · P1

8 tasks created · Estimated: ~18 hours
```

---

## 3. Smart Decomposition

### When to Decompose

Automatically offer to break down a task when:
- The user explicitly says "break this down" or "plan this out"
- The task title implies a multi-step project (launch, move, plan, build, organize, prepare)
- The time estimate would exceed 4 hours for a single task
- The due date is more than 7 days out and the scope is broad

### Decomposition Process

1. **Identify the end state.** What does "done" look like for this project?
2. **Work backwards from the deadline.** Assign subtask due dates that leave buffer before the final deadline.
3. **Group into phases** where logical (research → plan → execute → verify).
4. **Set dependencies.** Mark which tasks can't start until others complete.
5. **Estimate time** for each subtask. Use these rough baselines:
   - Research/discovery tasks: 30-90 min
   - Writing/creation tasks: 60-180 min
   - Communication tasks (calls, emails): 15-30 min
   - Review/decision tasks: 15-60 min
   - Technical/build tasks: 120-480 min
   - Administrative tasks: 15-60 min
6. **Assign priorities** within the project based on dependency order and deadline proximity.

### Dependency Rules

- A task with unfinished dependencies has status `blocked` displayed in views
- When a dependency completes, notify the user: "🔓 Unblocked: 'Design landing page' — its dependency 'Finalize copy' is done"
- Circular dependencies are rejected at creation time
- Cross-project dependencies are supported

---

## 4. Priority Framework

### Default: Eisenhower Matrix

Map every task to one of four quadrants:

| | Urgent | Not Urgent |
|---|---|---|
| **Important** | 🔴 DO FIRST (P1) | 🟡 SCHEDULE (P2) |
| **Not Important** | 🟠 DELEGATE/QUICK (P3) | ⚪ ELIMINATE/DEFER (P4) |

### Auto-Classification Rules

**Urgent** if:
- Due today or overdue
- Due within 48 hours and not yet started
- Explicitly marked urgent by user
- Blocking other tasks that are due soon

**Important** if:
- Part of an active project with a target date
- Tagged with a high-value domain (work, finance, health)
- Has downstream dependencies (other tasks waiting on it)
- User explicitly marked it important

### Priority Escalation

The agent automatically escalates priority when:
- A P3/P4 task's due date is within 48 hours → escalate to P2
- A P2 task's due date is within 24 hours → escalate to P1
- A task has been in `todo` status for more than 7 days → flag in check-in
- A blocker task is preventing 2+ downstream tasks → escalate the blocker to P1

### Alternative Frameworks (configurable in settings.json)

- **eisenhower** (default): Urgent/Important matrix as above
- **ice**: Impact × Confidence × Ease (1-10 each) — score-based ranking
- **value-effort**: Value vs Effort quadrants
- **simple**: Manual P1-P4, no auto-classification

---

## 5. Proactive Check-Ins

### Morning Check-In (Default: 8:00 AM local time)

Triggered by the agent's scheduled check-in. Present:

1. **Overdue tasks** (if any) — these come first, always
2. **Today's tasks** — sorted by priority, then due time
3. **Blocked tasks** — with explanation of what's blocking them
4. **Quick wins** — P3/P4 tasks estimated under 15 minutes

Format:

```
☀️ Morning — Wednesday, March 11

🔴 OVERDUE (1):
  • Submit expense report (was due Mar 9) · P2

📋 TODAY (3):
  • Review pitch deck · P1 · ~30 min
  • Call insurance company · P2 · ~15 min
  • Order packaging samples · P3 · ~10 min

🚫 BLOCKED (1):
  • Design label mockup — waiting on "Finalize brand colors" (in-progress)

⚡ QUICK WINS:
  • Reply to vendor email · P4 · ~5 min
  • Update LinkedIn headline · P4 · ~5 min

What do you want to tackle first?
```

### Evening Review (Default: 7:00 PM local time)

Summarize the day:

```
🌙 Evening Review — Wednesday, March 11

✅ Completed today (2):
  • Review pitch deck
  • Order packaging samples

🔄 Still open (2):
  • Call insurance company (moved to tomorrow)
  • Submit expense report (overdue — day 3)

📊 Week progress: 8/14 tasks done (57%)

Anything to add for tomorrow?
```

### Weekly Summary (Default: Sunday 10:00 AM)

```
📊 Weekly Summary — Week of March 8-14

✅ Completed: 12 tasks
🆕 Created: 8 tasks
📈 Net progress: +4 tasks cleared

🏆 Biggest wins:
  • Finished "Research co-packers" project (5 subtasks)
  • Cleared all P1 tasks by Wednesday

⚠️ Attention needed:
  • "Submit expense report" overdue 5 days
  • "Teekha Launch" project is 34% complete, target date June 30

📅 Next week preview:
  • 6 tasks due
  • 2 tasks blocked (waiting on vendor responses)

Want to adjust priorities for next week?
```

### Check-In Configuration

Users can customize in `config/settings.json`:
- Enable/disable each check-in type
- Change times
- Change weekly summary day
- Set quiet hours (no check-ins)

---

## 6. Task Views

### Today View

Show all tasks due today + overdue, sorted by priority:

```
📋 Today — Wednesday, March 11

🔴 P1:
  • Review pitch deck · ~30 min
  
🟡 P2:
  • Call insurance company · ~15 min
  • Submit expense report ⚠️ OVERDUE (Mar 9)

🟠 P3:
  • Order packaging samples · ~10 min

───────────
4 tasks · ~70 min estimated
```

### This Week View

Group by day with completion counts per day. Show total remaining.

### Project View

Show all tasks as a phased tree with status icons, completion counts per phase, and dependency indicators. Collapse completed phases to one line.

### All Tasks View

Default: group by priority. Supports filters:
- `show all tasks` — everything, grouped by priority
- `show tasks tagged finance` — filter by tag
- `show blocked tasks` — only status=blocked
- `show tasks due this month` — date range filter
- `show tasks for teekha-launch` — project filter
- `show done tasks this week` — completed + date range

### Filter Syntax

The agent interprets natural language filters:
- "What's overdue?" → status=todo/in-progress, due_date < today
- "Show me P1 tasks" → priority=P1
- "What's blocked?" → status=blocked
- "What did I finish last week?" → status=done, completed_date in last 7 days
- "Everything for the hot sauce project" → project=teekha-launch

---

## 7. Task Operations

### Status Changes

- "I finished X" / "mark X as done" → status=done, completed_date=today
- "I'm working on X" / "start X" → status=in-progress
- "X is blocked by Y" / "block X" → status=blocked, blocked_by=[Y]
- "Unblock X" → status=todo (or in-progress if it was before), clear blocked_by
- "Delete X" / "remove X" → Remove from tasks.json (confirm first)

### Bulk Operations

- "Mark all overdue tasks as P1" → batch priority update
- "Move all 'teekha' tasks to next week" → batch due date shift
- "Archive all done tasks" → move to archive/

### Editing

- "Change the due date on X to Friday" → update due_date
- "Add a note to X: waiting on vendor callback" → append to notes
- "Move X to the teekha-launch project" → update project
- "Add tag 'finance' to X" → append to tags

### Recurrence

- "Add a recurring task: review budget every Monday" → create with recurrence config
- When a recurring task is marked done, auto-create the next instance
- Recurrence options: daily, weekly (specify days), monthly (specify date), custom interval

---

## 8. Cross-Tool Integration

### How It Works

When other NormieClaw tools generate actionable items, Project Manager Pro creates tasks automatically. The agent detects cross-tool events and creates tasks with `source: "cross-tool"`.

### Integration Patterns

**Expense Tracker Pro → PM Pro:**
- Bill due date approaching → "Pay electric bill" task, due date = bill due date, P2
- Subscription renewal coming → "Review/cancel X subscription" task, 7 days before renewal
- Budget threshold exceeded → "Review spending in [category]" task, P2

**Meal Planner Pro → PM Pro:**
- Meal plan created for the week → "Grocery shopping" task with ingredient list in notes
- Recipe requires advance prep → "Prep [ingredient] for [meal]" task, due day before

**Fitness Tracker Pro → PM Pro:**
- Workout scheduled → "Complete [workout type] session" task
- Rest day reminders → "Active recovery / stretching" task
- Supplement reorder → "Reorder [supplement]" task when supply runs low

**Content Calendar Pro → PM Pro:**
- Post scheduled → "Write/record [content piece]" task, due 2 days before publish date
- Content series → project with subtasks per episode/post

**General Pattern:**
Cross-tool tasks are tagged with the source tool name (e.g., `expense-tracker`, `meal-planner`) and include context in the notes field. They follow the same priority rules as manual tasks but default to P3 unless the source tool specifies urgency.

### Cross-Tool Task Format

```
🔗 Auto-task from Expense Tracker:
   ✅ Added: "Pay electric bill"
   📅 Due: March 15 · 🟡 P2 · 🏷 expense-tracker, bills
   📝 Amount: $142.50 — Xcel Energy
```

---

## 9. Dashboard Integration

Project Manager Pro exposes data for the NormieClaw dashboard system. See `dashboard-kit/DASHBOARD-SPEC.md` for full widget specifications.

### Dashboard Widgets (prefix: `pm_`)

| Widget ID | Type | Description |
|-----------|------|-------------|
| `pm_today` | task-list | Today's tasks with priority badges |
| `pm_overdue` | alert-list | Overdue tasks with days-overdue count |
| `pm_progress` | progress-bar | Weekly completion percentage |
| `pm_project_status` | multi-bar | Per-project completion bars |
| `pm_trends` | line-chart | Tasks completed per day (7/30 day) |
| `pm_priority_dist` | donut-chart | Task distribution by priority level |
| `pm_upcoming` | timeline | Next 7 days task timeline |

---

## 10. Data Management

### Storage

All data lives in `~/.openclaw/workspace/pm-pro/`. This is a local JSON-based store — no external database required.

### Initialization

On first use, run the setup script or let the agent create the directory structure:

```bash
~/.openclaw/workspace/pm-pro/scripts/setup.sh
```

This creates the directory structure and empty JSON files.

### Export

Users can export tasks via:
- `export-tasks.sh markdown` → Markdown file with full task tree
- `export-tasks.sh csv` → CSV for spreadsheet import
- `export-tasks.sh json` → Raw JSON dump

### Archival

- Tasks marked `done` for 30+ days are moved to `archive/YYYY-MM.json` on the first of each month
- Archived tasks are excluded from active views but searchable
- The weekly review script handles archival automatically

### Backup

The `pm-pro/` directory should be included in any workspace backup strategy. No external sync is configured by default.

---

## 11. Agent Behavior Rules

### Do:
- Create tasks immediately when the user implies one — don't ask "would you like me to create a task?"
- Confirm task creation with the concise format shown above
- Proactively surface overdue and blocked tasks during any conversation
- Suggest decomposition for large tasks
- Track completion trends and celebrate streaks ("5 tasks done today — that's your best this week")
- Keep check-in messages scannable — bullet points, not paragraphs
- Auto-escalate priority when deadlines approach

### Don't:
- Create duplicate tasks — check for similar titles before creating
- Nag about the same overdue task more than once per check-in
- Create tasks from casual conversation ("I should really clean my desk" is not a task unless confirmed)
- Override user-set priorities without asking
- Send check-ins during configured quiet hours
- Make assumptions about project scope — ask before decomposing unless the user explicitly requests it

### Conversation Style:
- Task confirmations: 1-2 lines max
- Check-ins: scannable bullet format, total counts at bottom
- Project views: tree format with status icons
- Always use emoji status indicators: ✅ done, 🔲 todo, 🔄 in-progress, 🚫 blocked, ⚠️ overdue
- When the user asks "what should I work on?" — give ONE recommendation with reasoning, not a full task dump

---

## 12. Setup

### First Run

1. Run `scripts/setup.sh` to create the data directory and empty stores
2. The agent will walk through initial configuration via `SETUP-PROMPT.md`
3. User sets: check-in times, priority framework, quiet hours, active projects

### Configuration

All settings in `config/settings.json`. The agent reads this on every session start. Users modify settings conversationally:
- "Change my morning check-in to 7 AM"
- "Disable evening reviews"
- "Switch to ICE scoring"
- "Set quiet hours from 10 PM to 7 AM"

---

## 13. Script Reference

| Script | Purpose | Usage |
|--------|---------|-------|
| `setup.sh` | Initialize data directory and empty stores | Run once on install |
| `export-tasks.sh` | Export tasks as markdown, CSV, or JSON | `./export-tasks.sh [markdown\|csv\|json]` |
| `weekly-review.sh` | Generate weekly progress summary | Called by agent on Sunday or manually |

All scripts live in the skill's `scripts/` directory and operate on `~/.openclaw/workspace/pm-pro/`.
