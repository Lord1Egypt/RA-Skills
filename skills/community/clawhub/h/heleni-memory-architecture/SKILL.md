---
name: memory-architecture
version: "1.0.0"
description: "Honcho-inspired memory architecture for PA agents. Use when writing to MEMORY.md, ending a significant conversation, or deciding what to remember long-term. Implements two key patterns: deductive memory (not just facts, but logical conclusions) and session summaries (capture context before it disappears)."
---

## Load Local Context
```bash
CONTEXT_FILE="/opt/ocana/openclaw/workspace/skills/memory-architecture/.context"
[ -f "$CONTEXT_FILE" ] && source "$CONTEXT_FILE"
# Then use: $WORKSPACE, $MEMORY_FILE, $WHATSAPP_MEMORY_DIR, $OWNER_TIMEZONE, etc.
```

# Memory Architecture Skill (Honcho-inspired)

## Core Principle

Two types of memory, three tiers. Inspired by Honcho/Hermes Agent memory system.

---

## Memory Types

### [FACT] — Explicitly stated
Something the owner said directly.
> "Netanel works until 20:00" → [FACT]

### [DEDUCED] — Logical conclusion from behavior
Something inferred from patterns, corrections, or repeated behavior.
> "Netanel prefers execution over explanation" → [DEDUCED] (inferred from repeated feedback pattern)

**Rule:** After any interaction where a pattern becomes clear — write a [DEDUCED] entry. Don't wait for the owner to say it explicitly.

---

## Memory Tiers

| Tier | Where | When to write |
|---|---|---------|
| **Working** | In-session context | Available automatically |
| **Daily** | `memory/daily/YYYY-MM-DD.md` | End of every significant conversation (5+ exchanges) |
| **Projects** | `memory/projects/<name>.md` | Ongoing context per topic/project — open loops, status, decisions |
| **Long-term** | `MEMORY.md` | When pattern repeats 2+ times, or explicitly asked |

### Project Files
For active, multi-session work (rollouts, ongoing tasks, recurring topics), maintain a project file:

```
memory/projects/pa-rollout.md
memory/projects/crons-health.md
memory/projects/my-project.md
```

Each project file should contain:
- **Status** — current state
- **Open loops** — unresolved items that carry across days
- **Key decisions** — what was decided and why

**Load on demand:** Read the relevant project file when that topic comes up — not every session.
**Daily files are raw log.** Project files are living context.

**Rule:** If a task or decision needs to be remembered tomorrow — put it in the project file, not just the daily log.

---

## Session Summary Rule

At the end of any conversation with 5+ meaningful exchanges, append to `memory/YYYY-MM-DD.md`:

```markdown
## Session Summary — HH:MM

**Decisions made:**
- [list]

**Tasks completed:**
- [list]

**Deduced patterns:**
- [DEDUCED] [observation]

**Promote to MEMORY.md?**
- [ ] Yes: [what]
- [x] No
```

**When to promote to MEMORY.md:**
- Pattern has appeared 2+ times across different sessions
- Owner explicitly corrected something → update MEMORY.md immediately
- Important preference discovered → add as [DEDUCED]

---

## Writing Deduced Memories

After a correction or repeated behavior, write:

```markdown
- [DEDUCED] <conclusion> — evidence: <what happened>
```

Examples:
- `[DEDUCED] Prefers English for work docs — corrected me when I created Hebrew doc (2026-04-03)`
- `[DEDUCED] Expects autonomous execution without asking permission for reversible tasks — never asks why I acted autonomously`
- `[DEDUCED] Reads messages outside work hours but won't always respond`

---

## What NOT to remember

- One-time events with no pattern value
- Transient task state (use monday.com for that)
- Secrets or credentials (never in memory files)
- Conversation noise

---

## Memory Quality Checklist

Before writing to MEMORY.md, ask:
- [ ] Is this a fact OR a deduced pattern (not just noise)?
- [ ] Will this be useful in a future session?
- [ ] Is this tagged [FACT] or [DEDUCED]?
- [ ] Does it contradict an existing entry? (If yes, update the old one)

---

## Self-Review Cron Loop

For continuous self-improvement, set up two daily crons:

**Midday (13:00 local):**
```bash
openclaw cron add \
  --name "heleni-midday-self-review" \
  --cron "0 13 * * *" \
  --tz "Asia/Jerusalem" \
  --session isolated \
  --message "Run midday self-review: read today's memory file, find mistakes or corrections from this morning, update MEMORY.md with [DEDUCED] lessons if needed, commit to git. Silent if nothing to fix." \
  --timeout-seconds 180
```

**Nightly (23:00 local):**
```bash
openclaw cron add \
  --name "heleni-internal-self-review" \
  --cron "0 23 * * *" \
  --tz "Asia/Jerusalem" \
  --session isolated \
  --message "Run nightly self-review: read today's full memory file + last 3 MEMORY.md entries. Find: repeated mistakes, patterns to promote to long-term memory, rules to tighten. Update MEMORY.md and/or relevant SKILL.md files. Commit to git with message 'Self-review YYYY-MM-DD: [what changed]'. Silent if nothing to improve." \
  --timeout-seconds 180
```

**Why twice a day:**
- Midday catches morning mistakes early — fixes them before they repeat in the afternoon
- Nightly does the full consolidation of the day
- Once a day (evening only) is too slow for fast-moving days

---

## Memory Compaction (Prevent Bloat)

Left unchecked, MEMORY.md and AGENTS.md grow unbounded — causing context window bloat and degraded performance.

**Targets:**
- `MEMORY.md` → max 175 lines
- `AGENTS.md` → max 60 lines

**When to compact:**
- Weekly — set up a cron (see below)
- When MEMORY.md exceeds 200 lines
- When loading files already consumes >5% of context window

**How to compact:**
1. Read MEMORY.md fully
2. Merge duplicates, remove outdated entries, trim examples
3. Keep: active rules, key contacts, deduced patterns still valid
4. Remove: removed crons, resolved issues, one-time events
5. Commit to git after

**Weekly compaction cron:**
```bash
openclaw cron add \
  --name "weekly-memory-compaction" \
  --cron "0 7 * * 0" \
  --session isolated \
  --model "anthropic/claude-haiku-4-5" \
  --message "Weekly memory compaction: Read MEMORY.md and AGENTS.md. Remove outdated entries, merge duplicates. Target: MEMORY.md <175 lines, AGENTS.md <60 lines. Git push after. NO_REPLY." \
  --announce \
  --timeout-seconds 120
```

**Signal you need compaction:**
- MEMORY.md > 200 lines
- Session startup feels slow
- You notice you're repeating old rules that are no longer relevant

---

## Production Notes

- Workspace path: `/opt/ocana/openclaw/workspace` (not `~/.openclaw/workspace`)
- WhatsApp memory path: `memory/whatsapp/groups/<JID-sanitized>/context.md` or `memory/whatsapp/dms/<PHONE-sanitized>/context.md`
- Sanitize rule: replace `@`, `.`, `+` with `-`
- After writing memory — push to git (git-backup skill)
- **"sure thing" is a behavior rule** (not a memory item) — it lives in SOUL.md, do not re-derive from memory

## Cost Tips

- **Cheap:** File writes are free — don't hesitate to log
- **Session summaries:** Write once at the end, not after each message
- **MEMORY.md promotions:** Batch once per session, not per interaction
