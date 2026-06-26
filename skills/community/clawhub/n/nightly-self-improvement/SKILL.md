---
name: nightly-build
description: Ship one small improvement while the user sleeps. Scans today's sessions for friction points, picks the highest-impact reversible fix, builds it, and sends a morning briefing. Runs nightly via cron.
---

# Nightly Build

Your agent scans the day's conversations while you sleep, finds one friction point worth fixing, ships it, and leaves a morning briefing. No scope creep, no manufactured busywork — just steady compounding improvement.

## Philosophy

> Proactive > reactive. Fix one friction point while you sleep. Ship small, reversible improvements. Leave a morning briefing.

The idea: every night, your agent reviews what happened today, spots something worth improving (a repeated manual step, an annoying workflow, a doc that's out of date), and quietly fixes it. You wake up to a brief message explaining what changed and how to undo it if you don't like it.

Over weeks, this compounds. The agent gets better at anticipating your needs before you have to ask.

## Setup

### 1. Create NIGHTLY_BUILD.md in your workspace

Save this file to your clawd workspace root (`~/clawd/NIGHTLY_BUILD.md`):

```markdown
# NIGHTLY_BUILD.md — The Nightly Build

## Philosophy
Proactive > reactive. Fix one friction point while you sleep. Ship small, reversible improvements. Leave a morning briefing.

## Schedule
Runs at 3:00 AM (your local time) via cron, after nightly memory extraction.

## Process

### 1. Scan for friction points (~2 min)
Review today's sessions for:
- Repeated manual steps or commands
- Things [user] asked about but didn't finish
- Complaints or annoyances mentioned in passing
- Patterns across recent days (check memory/YYYY-MM-DD.md)
- Stale workspace files or disorganized areas
- Missing documentation or notes
- Upcoming tasks that could use prep work

### 2. Pick ONE improvement
Choose the highest-impact, lowest-risk item. Prefer:
- Things that save [user] time tomorrow morning
- Things that are clearly reversible
- Things that compound (better memory, better tooling, better docs)

### 3. Tier Check — What's allowed?

**Tier 1 — Just do it** (no permission needed):
- Workspace/memory file organization
- Shell scripts or aliases (in ~/clawd/scripts/)
- Research and summaries saved to files
- Documentation improvements
- Memory cleanup (dedup, organize, update summaries)
- Prep work for known upcoming tasks
- New skills or cron job drafts (saved as files, not deployed)

**Tier 2 — Prep but don't deploy** (queue for morning review):
- Changes to code repos (create branch + PR draft, don't merge)
- New cron jobs or config changes
- Anything that changes how existing tools work

**Tier 3 — Never without permission**:
- External-facing actions (emails, messages, posts)
- Spending money
- Deleting data
- Production deployments

### 4. Build it
- Keep it small — if you can't explain it in one sentence, it's too big
- Make it reversible — git commits, not direct edits to important files
- Document what you did and why

### 5. Morning Briefing
Send [user] a message at completion with:
🌙 Nightly Build Report

**What I built:** [one sentence]
**Why:** [what friction I noticed]
**How to undo:** [one command or "delete X file"]
**Tier 2 queue:** [anything prepped but waiting for your OK]

If nothing worth building → skip silently. Don't manufacture busywork.

## Anti-patterns
- ❌ Scope creep ("while I'm here...")
- ❌ Building something cool but useless
- ❌ Touching things [user] intentionally left a certain way
- ❌ Manufacturing work to look industrious
- ❌ Breaking the chain of provenance (always explain WHY)
```

### 2. Add the cron job

Run this in your OpenClaw session:

```
Add a nightly cron job called "nightly-build" that runs at 3 AM every night.
It should fire a systemEvent on the main session with this text:

"🌙 Nightly Build: Time to ship one improvement while [user] sleeps.

Read ~/clawd/NIGHTLY_BUILD.md and follow the process:
1. Scan today's sessions for friction points (use sessions_list + sessions_history)
2. Check recent memory/YYYY-MM-DD.md files for patterns
3. Pick ONE small, reversible, high-impact improvement
4. Tier check: only Tier 1 work gets shipped. Tier 2 gets prepped.
5. Build it
6. Send morning briefing to [user] via your configured messaging channel

If nothing worth building tonight, skip silently."
```

Or configure it directly via `cron` tool:

```json
{
  "name": "nightly-build",
  "schedule": { "kind": "cron", "expr": "0 3 * * *", "tz": "America/Chicago" },
  "sessionTarget": "main",
  "payload": {
    "kind": "systemEvent",
    "text": "🌙 Nightly Build: Time to ship one improvement while you sleep.\n\nRead ~/clawd/NIGHTLY_BUILD.md and follow the process:\n1. Scan today's sessions for friction points (use sessions_list + sessions_history)\n2. Check recent memory/YYYY-MM-DD.md files for patterns\n3. Pick ONE small, reversible, high-impact improvement\n4. Tier check: only Tier 1 work gets shipped. Tier 2 gets prepped.\n5. Build it\n6. Send morning briefing via your configured messaging channel\n\nIf nothing worth building tonight, skip silently."
  }
}
```

## What It Does Each Night

The agent follows a fixed process:

1. **Scans sessions** — uses `sessions_list` + `sessions_history` to review the day's conversations
2. **Reads daily notes** — checks `memory/YYYY-MM-DD.md` for patterns across recent days
3. **Identifies friction** — repeated commands, unfinished requests, missing docs, stale files
4. **Picks ONE thing** — the highest-impact, most reversible improvement
5. **Checks the tier** — Tier 1 ships immediately, Tier 2 gets prepped as a draft/PR
6. **Builds it** — shell scripts, documentation, memory cleanup, prep work
7. **Sends a briefing** — one short message explaining what changed and how to undo it

## Customization

Edit `NIGHTLY_BUILD.md` to:

- **Adjust the tier rules** — tighten or loosen what the agent can do autonomously
- **Change the scan scope** — add specific friction areas to prioritize
- **Modify the briefing format** — add metrics, link to files, change tone
- **Add an anti-backlog** — list things you explicitly don't want touched

## Tips

- **Let it run for 2 weeks before judging it.** The first few nights may find small things; after a week of patterns the improvements get sharper.
- **Read the briefings.** Even when the improvement seems minor, the _why_ often reveals something useful about your workflow.
- **Expand Tier 1 as trust grows.** Start conservative. Once you've seen the agent make good calls consistently, loosen the tier rules.
- **Pair it with the Three-Tier Memory System** (also on ClawMart) for better pattern detection across days.
