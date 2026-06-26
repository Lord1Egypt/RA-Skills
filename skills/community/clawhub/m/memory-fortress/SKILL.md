---
name: memory-fortress
version: 1.1.2
description: Complete memory management system for OpenClaw agents. Combines compaction-aware saving, a formal boot sequence, domain organization, memory scoring, structured learnings, and documentation-first project continuity.
---

# Memory Fortress 🏰

A unified memory system that prevents agents from forgetting what they did yesterday and ensures work survives session boundaries in written form.

**Built from five proven patterns:**
- Compaction-aware saving, disk is truth
- Boot sequence + state files, Dory-proof capture
- Domain organization, keeping `MEMORY.md` small and useful
- Memory types + priority, for durable recall
- Promote / demote lifecycle, so memory can evolve over time

---

## Mental model

```text
┌─────────────────────────────────────────────────────┐
│                   MEMORY FORTRESS                   │
├─────────────────────────────────────────────────────┤
│  🔴 SESSION RAM   → temporary, lost on compaction   │
│  🟡 STATE/        → active task, blockers, decisions│
│  🟢 DAILY LOG     → memory/YYYY-MM-DD.md            │
│  🔵 MEMORY.md     → curated durable knowledge       │
│  ⚪ DOMAINS/       → topic-specific detail           │
│  📦 ARCHIVE/      → older logs                      │
│  🧱 PROJECT FILES → task_plan.md + notes.md + output│
└─────────────────────────────────────────────────────┘
```

**Core principle:** session memory is temporary, files are truth.

---

## 1. Boot sequence — run at the start of every session

**Order matters.**

```text
1. state/HOLD.md        — what is blocked? do not do these
2. state/ACTIVE.md      — is there an active task?
3. state/DECISIONS.md   — recent decisions, last 48h
4. state/CLOSED.md      — durable closed decisions, not to be reopened casually
5. IDENTITY.md          — who the agent is
6. SOUL.md              — learned style and operating principles
7. USER.md              — who the agent serves
8. memory/YYYY-MM-DD.md — today + yesterday
9. MEMORY.md            — long-term knowledge, main session only
```

Post-boot status line:
```text
🏰 Boot: ACTIVE=[task|none] | HOLD=[n] | DECISIONS=[n last 48h]
```

### Not a boot step
- Domain files, load on demand with `memory_search`
- Archive, only when needed
- Other agents' memory, never by default

---

## 2. Dory-proof pattern — when a task arrives

When the user gives you a task:

1. **Immediately** write their **exact words** to `state/ACTIVE.md`
2. Then interpret the request
3. Then do the work
4. When done, update or clear ACTIVE

### `state/ACTIVE.md` format
```markdown
## Active task
**User said:** "[exact quote]"
**Interpretation:** [what you believe it means]
**Status:**
- [ ] Step 1
- [ ] Step 2
**Updated:** YYYY-MM-DD HH:MM
```

### `state/HOLD.md` format
```markdown
[YYYY-MM-DD HH:MM | session] Item — reason for blocking
```

### `state/DECISIONS.md` format
```markdown
[YYYY-MM-DD HH:MM | session] Decision — context / rationale
```

### `state/CLOSED.md` format
```markdown
[YYYY-MM-DD | decider] Topic keyword — short final decision
```

Use `CLOSED.md` for issues that were definitively settled and should not keep resurfacing as open questions.

---

## 3. Write Before Lose — compaction-aware saving

Session RAM can disappear. Save important things before that happens.

| Event | Where to write |
|------|----------------|
| Decision made | `state/DECISIONS.md` + daily log |
| Preference discovered | `MEMORY.md` or daily log |
| Task received | `state/ACTIVE.md` |
| Something blocked | `state/HOLD.md` |
| Error + lesson | daily log + `.learnings/` |
| Important fact discovered | daily log, later promote if durable |
| Work completed | `state/ACTIVE.md` + daily log |

**Rule:** if it matters, write it immediately.

---

## 4. Memory scoring — what belongs in `MEMORY.md`?

Score each candidate on 4 axes from 0 to 3.

| Axis | 0 | 1 | 2 | 3 |
|------|---|---|---|---|
| Durability | Gone tomorrow | Weeks | Months | Years+ |
| Reuse | One-time | Occasional | Frequent | Every session |
| Impact | Trivial | Helpful | Changes output | Changes decisions |
| Uniqueness | Obvious | Mildly useful | Hard to re-derive | Irreplaceable |

Put it in `MEMORY.md` if:
- total score ≥ 8, or
- any axis = 3 and total score ≥ 6

Everything else belongs in the daily log or a domain file.

---

## 5. Domain organization — keep `MEMORY.md` ≤10KB

```text
memory/
├── domains/
│   ├── projects.md
│   ├── infrastructure.md
│   ├── people.md
│   ├── skills-tools.md
│   ├── lessons.md
│   └── policies.md
├── .learnings/
├── archive/
└── YYYY-MM-DD.md
```

### Rules
- `MEMORY.md` stores summaries, references, and the most important durable knowledge
- `memory/domains/*.md` stores detailed topic-specific material
- `memory/archive/` stores old logs
- `memory/.learnings/` stores structured mistakes, corrections, and requests

---

## 6. Memory types and priority

| Prefix | Type |
|--------|------|
| `DEC` | Decision |
| `PREF` | Preference |
| `FACT` | Durable fact |
| `POLICY` | Rule |
| `LESSON` | Lesson learned |
| `ERR` | Known error |

Use priority 1 to 10. Reserve 9 to 10 for truly critical items.

---

## 7. Promote / Demote — memory lifecycle

### Promote when
- the memory becomes relevant again
- the user references it
- it supports an important decision

### Demote when
- it has not been used in 30+ days
- it is outdated
- a newer memory contradicts it

### Contradiction handling
1. Prefer the newer memory
2. Mark the older one `[STALE]`
3. Record why it changed in the daily log

---

## 8. Search strategy

Always use:
1. `memory_search`
2. `memory_get`

Search order:
1. `state/`
2. `MEMORY.md`
3. `memory/domains/*.md`
4. `memory/YYYY-MM-DD.md`
5. `memory/archive/`

Do not read entire memory trees "just in case."

---

## 9. Multi-agent rules

| Rule | Details |
|------|---------|
| Own workspace | Each agent writes in its own workspace |
| No cross-read | Do not read another agent's memory by default |
| Communication | Use direct agent messaging, not memory files |
| Shared state | Only explicitly shared folders |
| Private context | Keep private conversations private |

---

## 10. Anti-patterns

| Don't | Do instead |
|------|------------|
| "I'll remember this mentally" | Write it to a file immediately |
| Paste chat logs into `MEMORY.md` | Use daily log + summary |
| Let `MEMORY.md` bloat | Split into domain files |
| Answer past-context questions from memory alone | Search first |
| Keep many tasks in `ACTIVE.md` | One active task, rest in project files |
| Paraphrase the user's task | Keep the exact quote |
| Store secret values | Record only that they exist |

---

## 11. `.learnings/` — mistakes, corrections, and growth

Recommended files:
- `memory/.learnings/LEARNINGS.md`
- `memory/.learnings/ERRORS.md`
- `memory/.learnings/FEATURE_REQUESTS.md`

### Triggers
- User correction → `LEARNINGS.md` / `correction`
- Outdated knowledge → `LEARNINGS.md` / `knowledge_gap`
- Better method discovered → `LEARNINGS.md` / `best_practice`
- Command or tool failure → `ERRORS.md`
- Missing capability requested → `FEATURE_REQUESTS.md`

### ID format
```text
TYPE-YYYYMMDD-XXX
```

### Promotion logic
- behavioral pattern → persona / operating docs
- workflow improvement → operational manual
- tool gotcha → tool docs
- broadly reusable lesson → new skill

---

## 12. Documentation-first workflow — mandatory project continuity

Memory is not enough. The work itself must also exist in files.

### Core principle
**If it's not written down, it doesn't exist.**

### What to document, and where

| What | Where |
|------|-------|
| Incoming task | `state/ACTIVE.md`, exact user words |
| Decision | `state/DECISIONS.md` + daily log |
| Blocker | `state/HOLD.md` |
| Permanently closed decision | `state/CLOSED.md` |
| Reorientation snapshot | `state/ORIENT.md` |
| Research notes | `notes.md` |
| Project progress | `task_plan.md` |
| Final output | a dedicated deliverable file |
| General lesson | `.learnings/` or a domain file |

### Project detection
Treat work as a project immediately if any of these are true:
- it has 3 or more steps
- it has a name, slug, or concrete deliverable
- it may span multiple sessions
- it includes research, building, and review

### Required 3-file pattern
For any non-trivial task, create:

```text
projects/<project-slug>/
├── task_plan.md
├── notes.md
└── deliverable.md   or another suitable output file
```

### Minimum `task_plan.md`
```markdown
# Task Plan: [name]

## Goal
[one-sentence end state]

## Phases
- [ ] Phase 1: setup
- [ ] Phase 2: discovery / research
- [ ] Phase 3: execution
- [ ] Phase 4: review / deliver

## Decisions Made
- [decision]: [why]

## Errors Encountered
- [error]: [resolution]

## Status
**Currently in Phase X** - [current focus]
```

### Role of `notes.md`
Use it for sources, raw findings, analysis, and anything too large for the live context window.

### Documentation rules
1. Plan first
2. Read the plan before major decisions
3. Update the plan after each phase
4. Store large content in files, not in chat context
5. Log errors as they happen

### Cron and automation prompts
If you write a cron or automation prompt, include a dedicated section like this:

```markdown
### Documentation (MANDATORY)
- Append a short run summary to: [exact file path]
- Format: YYYY-MM-DD | type | slug | summary
- This must be the last step before finishing
```

### Why this belongs in Memory Fortress
Because project files are memory too. `task_plan.md`, `notes.md`, and `state/ORIENT.md` together form the operational memory of ongoing work.

---

## 13. Failsafe / reorientation layer

When an agent suddenly loses the thread, starts following the wrong branch of work, or needs to recover the real task from a long conversation, it should create a focused reorientation summary before doing more execution.

### Proven recovery prompt pattern
```text
Read back the full thread content and summarize what we have done so far, where the task is documented, and what the next step is. Do not go further, only produce this detailed summary.
```

### When to activate it
- the agent is unsure where the work actually stands
- too many side-tracks were followed
- after handoff or a long pause
- when thread state and file state must be reconciled
- before the context window becomes too noisy

### Reorientation protocol
1. Read back the relevant thread or documented context
2. Check `state/HOLD.md`, `state/ACTIVE.md`, `state/DECISIONS.md`, `state/CLOSED.md`
3. Open the canonical `task_plan.md` and `notes.md`
4. Produce a short factual summary
5. Write the compressed version to `state/ORIENT.md`
6. Only then resume execution

### Recommended `state/ORIENT.md` format
```markdown
## Reorientation snapshot
**Thread / Context:** [which thread or task this is]
**What we did so far:**
- ...
- ...

**Where it is documented:**
- `state/ACTIVE.md`
- `projects/<slug>/task_plan.md`
- `projects/<slug>/notes.md`

**Actual next step:**
- ...

**Do not do instead:**
- ...
- ...

**Closure criteria:**
- ...
- ...

**Last updated:** YYYY-MM-DD HH:MM
```

### Important rules
- a failsafe summary is not execution, it is reorientation
- do not jump into a new project or side-track first
- identify the real next step before acting
- send it to chat only for handoff, decision points, or explicit user request
- the canonical version should live in files, not only in chat

### Why not periodic Discord summaries?
Because they create noise, duplicate the file-based source of truth, and consume context themselves. The correct model is: **file-first summary, chat-only when useful**.

### When to make this a separate mini-skill
If the recurring task is thread readback + summary + documented next-step recovery, use a dedicated `context-rescue` mini-skill.

---

## 14. Maintenance schedule

| Frequency | Task |
|-----------|------|
| Every session | run boot sequence |
| Every task | update ACTIVE |
| Important event | write immediately |
| Daily | review daily log and clean state |
| Weekly | size-check MEMORY.md and update domains |
| Biweekly | archive old logs |
| Monthly | demote stale memories and resolve contradictions |
| On error | write to `.learnings/ERRORS.md` |
| On correction | write to `.learnings/LEARNINGS.md` |

---

## 15. Installation

### 1. Create state files
```bash
mkdir -p state
touch state/ACTIVE.md state/HOLD.md state/DECISIONS.md state/CLOSED.md
```

### 2. Create ORIENT file
```bash
touch state/ORIENT.md
```

### 3. Create memory structure
```bash
mkdir -p memory/domains memory/archive memory/.learnings
```

### 4. Create projects convention
```bash
mkdir -p projects
```

### 5. Update your agent manual
Add the boot sequence, the write-before-lose rule, the documentation-first project pattern, and the failsafe `ORIENT.md` reorientation layer.

---

*"Memory is what separates a tool from an ally."*
