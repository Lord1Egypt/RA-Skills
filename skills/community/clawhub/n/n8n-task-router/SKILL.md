---
name: n8n-task-router
description: Decision framework for routing tasks between n8n and OpenClaw. Use when
  deciding whether a new task should be automated in n8n or handled by an OpenClaw
  agent. Owned by Liv.
version: 1.0.0
metadata:
  openclaw:
    emoji: 🔀
---

# n8n Task Router

## The Core Rule

**If the task is deterministic and scheduled, use n8n. If it requires reasoning, judgment, or workspace context, use OpenClaw.**

Every OpenClaw call injects ~44KB of context (AGENTS.md, SOUL.md, MEMORY.md, history, tool logs) whether it needs it or not. For tasks that don't need that context, it's pure waste. n8n runs the same pipeline for $0 overhead.

---

## Route to n8n when

- Task runs on a **fixed schedule** (cron, interval, webhook trigger)
- Task is **deterministic** — same input → same output, every time
- Task is a **pipeline with defined steps** — no branching decisions
- Task does **not** need to read workspace files (MEMORY.md, STATUS.md, project files)
- Task is one of: fetch URL, transform data, call API, send email/notification, generate report, forward receipt, watch for approval

**Examples:**
- Tweet scheduling (via Buffer or n8n HTTP node calling Buffer API)
- Receipt forwarding to nissan@reddi.tech
- Blog Drafts Approval Watcher (poll Notion, notify on status change)
- Weekly Competitive Intelligence fetch
- Spend reports
- Autoresearch pipeline trigger

---

## Route to OpenClaw when

- Task requires **judgment, reasoning, or autonomous decisions**
- Task needs to **read/write workspace files** (MEMORY.md, STATUS.md, project files)
- Task involves **multi-step tool use with unpredictable branching**
- Task needs to **synthesise information and make a recommendation**
- Task involves **spawning other agents**

**Examples:**
- Research briefs (Archie)
- Code review (Oli)
- Content drafting (Sara, Belle)
- Architecture decisions (Loki)
- Debugging (Kit)
- Anything requiring agent-to-agent coordination

---

## Decision Checklist

Before routing, answer these:

1. **Scheduled?** Fixed cron/interval → strong n8n signal
2. **Deterministic?** Same input always → same output → n8n
3. **Needs workspace files?** MEMORY.md / STATUS.md / project files → OpenClaw
4. **Needs branching?** Unpredictable decision trees → OpenClaw
5. **Needs agents?** Spawning / coordination → OpenClaw
6. **Just fetch-transform-send?** → n8n

| Signal | n8n | OpenClaw |
|---|---|---|
| Fixed schedule | ✅ | ❌ |
| Deterministic pipeline | ✅ | ❌ |
| No workspace context needed | ✅ | ❌ |
| Judgment / reasoning | ❌ | ✅ |
| Read/write workspace files | ❌ | ✅ |
| Multi-agent coordination | ❌ | ✅ |
| Unpredictable branching | ❌ | ✅ |

---

## Cost Context

- **OpenClaw call minimum:** ~44KB context injection + model tokens + tool call tokens
- **n8n HTTP node:** $0 (self-hosted) + only the actual API call tokens (if any LLM node involved)
- **Savings estimates:**
  - Scheduled heartbeat checks → **~$2–5/month saved per check moved to n8n**
  - Weekly competitive intel run → **~$10–20/month saved**
  - Recurring "check X, send Y" tasks → **97% cheaper in n8n**

> **Note:** Social publishing (LinkedIn, X) uses Buffer (`skills/buffer-publisher/SKILL.md`). Typefully cancelled 2026-03-25.

If a task runs daily and takes no reasoning, it should be in n8n. Full stop.

---

## Current n8n Workflows (reference)

- **Blog Drafts Approval Watcher** — polls Notion Content Pipeline DB, notifies on status change
- **Autoresearch Pipeline** — triggers periodic research runs
- **Competitive Intelligence Weekly Run** — fetches and compiles competitive intel on a schedule

**n8n setup:**
- Container: `n8n-n8n-1` at `localhost:5678`
- API key: `op://OpenClaw/mfi5ztglzek7mgh6wmj45aavlu/credential`
- Start script: `projects/n8n/start-n8n.sh`

---

## How to add a new n8n workflow

1. Confirm task passes the Decision Checklist above (n8n column)
2. Start n8n if not running: `bash projects/n8n/start-n8n.sh`
3. Open `localhost:5678` in browser
4. Create new workflow → use Cron or Webhook trigger node
5. Build pipeline: Trigger → Fetch/Transform → Action (HTTP, email, Notion, etc.)
6. Test with manual trigger before activating
7. Activate workflow
8. Add to "Current n8n Workflows" section above
9. Log in `memory/YYYY-MM-DD.md`

---

## Anti-patterns

- **Autonomous reasoning in n8n** — n8n has no tools, no context, no memory. Don't put tasks that need judgment in n8n and expect good results.
- **Cron tasks through OpenClaw heartbeats** — if the task is "check X every day", that's n8n. Don't burn 44KB of context injection on a deterministic fetch.
- **"Check X and send Y" in OpenClaw** — if there's no branching decision, it doesn't need an agent. Move it to n8n.
- **Forgetting to update this file** — when a new n8n workflow is added, update the "Current n8n Workflows" section. Stale reference = routing mistakes.
