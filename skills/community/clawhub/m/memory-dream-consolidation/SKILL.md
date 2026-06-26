---
name: memory-dream
description: Structured memory classification and periodic consolidation (Dream) for OpenClaw agents. Activate when setting up a new agent's memory system, when MEMORY.md is getting too long (over 200 lines), when doing periodic memory maintenance during heartbeats, or when the user says "整理记忆" "记忆维护" "dream" "memory cleanup". NOT for daily note writing (just write normally) or conversation recall (use memory_search).
---

# Memory Dream — 记忆分类与整合系统

Inspired by Claude Code's Dream memory consolidation system. Adapted for OpenClaw's file-based memory architecture.

## Memory Classification — 四类记忆

Every memory entry belongs to one of four types. Tag each entry when writing.

| Type | What to Store | Where | Example |
|------|--------------|-------|---------|
| **user** | User's role, preferences, knowledge, communication style | USER.md / MEMORY.md | "Jim prefers casual Chinese, works at Amazon, timezone UTC+8" |
| **feedback** | Corrections **AND** confirmations — what works and what doesn't | AGENTS.md / MEMORY.md | "append over write for Feishu docs. Why: write overwrites history. How: always use feishu_doc append" |
| **project** | Ongoing work, goals, deadlines, decisions | daily notes / MEMORY.md | "France trip Jun 19-27, 4 people, budget TBD — optimized for museum closure days" |
| **reference** | Pointers to where information lives | TOOLS.md / MEMORY.md | "Brave API ~1000/mo free, usage tracked in memory/brave-search-usage.json" |

### Writing Format

Every feedback/project memory entry should follow:

```
**Rule/Fact:** [the thing itself]
**Why:** [reason — past incident, user preference, or constraint]
**How to apply:** [when/where this kicks in]
```

### Key Principles

1. **Record success too** — Only recording failures makes the agent overly cautious. "This approach worked well + why" is as valuable as "this broke + why"
2. **Include Why** — Without Why, the agent can't judge edge cases and blindly follows rules
3. **Absolute dates only** — Write "2026-03-31" not "today" or "yesterday". Memories must be interpretable after time passes
4. **Verify before trusting** — "Memory says X exists" ≠ "X exists now". Check current state before acting on recalled memories

### What NOT to Store

- Code patterns, architecture, file structure (derivable from code)
- Git history (git log is authoritative)
- Debugging solutions (the fix is in the code, commit message has context)
- Ephemeral task details or current conversation context
- Content already in CLAUDE.md / AGENTS.md

Even if the user asks to save something from the exclusion list, ask what was *surprising* or *non-obvious* — that's the part worth keeping.

## MEMORY.md Size Control

**Hard limit: 200 lines / 25KB.** When exceeded, run a Dream cycle.

Check with: `wc -l MEMORY.md && wc -c MEMORY.md`

## Dream Cycle — 记忆整合流程

A periodic consolidation pass over memory files. Run during heartbeats or when MEMORY.md exceeds limits.

### Trigger Gates (all three must pass)

1. **Time gate:** ≥ 3 days since last Dream
2. **Session gate:** ≥ 3 days of new daily notes since last Dream
3. **Lock gate:** No other Dream in progress

Track state in `memory/heartbeat-state.json`:
```json
{
  "lastDreamAt": "2026-03-31T15:40:00Z",
  "lastDreamResult": "pruned from 269 to 85 lines"
}
```

### Four Phases

#### Phase 1 — Orient

- Read MEMORY.md — understand current long-term memory landscape
- Scan recent `memory/YYYY-MM-DD.md` files since last Dream
- Note current MEMORY.md line count and byte size

#### Phase 2 — Gather

- Extract entries worth keeping long-term from daily notes
- Classify each as user / feedback / project / reference
- Priority: important decisions, then lessons learned, then discoveries, then people info
- **Collect successes too**, not just failures

#### Phase 3 — Consolidate

- Write or update MEMORY.md entries in appropriate sections
- Convert any relative dates to absolute dates
- **Delete contradicted facts** (new info overrides old)
- Merge near-duplicate entries
- For feedback type: ensure each has Why + How to apply

#### Phase 4 — Prune

- Enforce ≤ 200 lines / 25KB limit
- Remove: completed projects, resolved issues, stale preferences
- Replace verbose details with pointers: "详见 daily notes 2026-03-31"
- Check for and resolve contradictions between entries

### After Dream

- Update `lastDreamAt` in heartbeat-state.json
- Log what was done in today's daily notes: lines before → after, what was added/removed

## Setup Guide — First-Time Configuration

To add this system to a new OpenClaw agent:

1. Add the memory classification table and Dream procedure to AGENTS.md
2. Add size limit header to MEMORY.md:
   ```
   > 📏 限制：≤ 200 行 / 25KB | 上次整理：YYYY-MM-DD
   ```
3. Add `lastDreamAt` field to memory/heartbeat-state.json
4. Add Dream trigger check to HEARTBEAT.md:
   ```
   - [ ] **记忆整理（Dream）**：检查是否满足三重门控，满足则执行四阶段整理
   ```
5. Run an initial Dream cycle to establish baseline

## Memory Drift Warning

Before acting on a recalled memory:

- If memory names a **file path** → check the file exists
- If memory names a **function or config** → grep for it
- If memory is a **state snapshot** (activity log, architecture) → prefer git log or reading current code
- If memory conflicts with current reality → **trust what you see now, update the memory**
