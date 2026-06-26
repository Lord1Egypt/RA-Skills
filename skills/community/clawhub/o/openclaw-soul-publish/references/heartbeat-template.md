# HEARTBEAT.md — Structured Heartbeat Protocol

> Every heartbeat is an opportunity to do useful work. Follow this protocol step by step.

---

## Step 0: Determine Wake Context

Check why you were woken:

| Wake Reason | Action |
|-------------|--------|
| **Timer** (scheduled interval) | Run full protocol below |
| **Message** (new user/group message) | Prioritize message handling, then resume protocol |
| **Task assignment** (new task delegated to you) | Jump to Step 3 with assigned task |
| **Approval resolution** (user approved/rejected a proposal) | Handle approval outcome, then resume protocol |

If wake reason is unclear, treat as Timer.

---

## Step 1: Quick Scan (~30 seconds)

- Scan connected messaging channels for missed messages
- Check `working-memory.md` for active tasks
- Read `GOALS.md` for current priorities
- **If nothing needs attention and last check was <30min ago** → reply HEARTBEAT_OK and stop

---

## Step 2: Goal Alignment Check

Before doing any work, verify it serves current goals:

1. Read `GOALS.md` → what are the active goals?
2. Check active tasks in working-memory.md → do they still align with goals?
3. If a task has no goal connection → flag it for review, deprioritize

---

## Step 3: Task Triage

For each active task in working-memory.md:

### 3a. Is this task blocked?

- **YES, and I already reported the blocker with no new context since** → **SKIP** (do not repeat "still blocked")
- **YES, but new context has arrived** → re-evaluate, update status
- **YES, blocked >24h** → escalate to user with proposed alternatives
- **NO** → proceed to Step 4

### 3b. Priority ranking

If multiple tasks are unblocked, pick by:
1. User explicitly requested (highest)
2. Goal-aligned and time-sensitive
3. Goal-aligned and not time-sensitive
4. Housekeeping (memory maintenance, reflection)

---

## Step 4: Execute

Do the work. Update `working-memory.md` as you go:
- Task started: mark `in_progress`
- Task completed: mark `done`, record outcome
- Task blocked: mark `blocked`, record blocker and timestamp

---

## Step 5: Memory Maintenance

After executing primary work (or if no primary work exists):

### Every heartbeat:
- Extract durable facts from recent conversations → write to `memory/entities/` (Layer 1)
- Update `memory/daily/YYYY-MM-DD.md` with today's events (Layer 2)

### Every 3rd heartbeat (Deep Reflection):
- Review interactions since last reflection
- Update `long-term-memory.md` with new user patterns or lessons (Layer 3)
- Check capability tree — anything to strengthen or prune?
- If insights found, append to Evolution Log in SOUL.md
- Run memory decay: review entity summaries, demote cold facts

### Daily Morning Brief (first heartbeat after 08:00 user local time):
- Summarize yesterday's key events and outcomes
- Suggest today's priorities based on GOALS.md context
- Flag any pending or overdue items

### Post-Major-Session:
- After substantive conversations (not quick Q&A), propose 1-3 SOUL.md improvements
- Core Identity changes: present proposal and wait for approval
- Working Style / User Understanding: update autonomously and notify

### Weekly (every ~7 days):
- Full entity summary rewrite: regenerate each entity's `summary.md` from active facts
- Archive completed goals from GOALS.md
- Review `soul-revisions/` — any drift patterns worth noting?

---

## Step 6: Budget Awareness

If you have visibility into token usage:
- **<80% budget**: normal operation
- **80-99% budget**: focus only on user-requested and critical tasks. Skip housekeeping.
- **100% budget**: stop proactive work entirely. Only respond to direct user messages.

---

## Heartbeat State

Track in `memory/heartbeat-state.json`:
```json
{
  "last_check": "ISO timestamp",
  "last_reflection": "ISO timestamp",
  "last_morning_brief": "ISO date",
  "last_weekly_review": "ISO date",
  "heartbeat_count": 0,
  "blocked_tasks_reported": {
    "task_id": "last_reported_timestamp"
  }
}
```
