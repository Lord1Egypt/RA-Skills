# Architecture — Memory Dreaming

## The Biological Analogy

During waking hours, the brain absorbs raw sensory input as short-term memories. During REM sleep, it replays the day's events, strengthens important connections, discards noise, and organizes everything into long-term memory.

OpenClaw agents have the "waking" part:
- `memory/YYYY-MM-DD.md` daily logs (auto-flushed before compaction)
- `.learnings/` structured error/correction capture
- Session transcripts (30-day retention)
- QMD indexes everything for search

But without consolidation, daily notes accumulate noise — contradictions, stale references, duplicate entries. The signal-to-noise ratio degrades over time, exactly like a sleep-deprived brain.

**Memory dreaming is the REM sleep cycle.** It replays recent sessions, strengthens what matters, discards what's stale, and organizes the rest.

## The 4-Phase Cycle

### Phase 1: Orient
**Input:** Current memory state
**Output:** Mental map of what exists

Read:
- `MEMORY.md` — current long-term memory
- `memory/YYYY-MM-DD.md` — recent daily logs (since last dream)
- `.learnings/*.md` — pending corrections, errors, best practices
- `memory/dreaming-log.md` — when was the last dream, what changed
- Obsidian vault state (if configured) — what's already synced

This phase answers: "What do I already know, and what's new since last time?"

### Phase 2: Gather Signal
**Input:** Session transcripts, daily logs, learnings
**Output:** List of high-value new information

The key insight from Claude Code's AutoDream: **grep narrowly, don't read full transcripts.** Exhaustively reading hundreds of session files burns tokens for diminishing returns. Instead, search for specific high-signal patterns:

**Correction patterns** (highest value — the human told us we were wrong):
- "no, that's wrong", "actually...", "I meant...", "not X, Y"
- "that's outdated", "you're wrong about"

**Decision patterns** (durable facts):
- "let's do X", "go with Y", "use Z instead"
- "we decided", "the plan is"

**Save patterns** (explicit memory requests):
- "remember this", "save to memory", "don't forget"

**Entity patterns** (proper nouns worth tracking):
- Names, project names, URLs, API keys mentioned
- New tools, services, repos discovered

**Plan patterns** (scan for task_plan.md files):
- New plans that need Obsidian tracking
- Plan status changes (phases completed)

### Phase 3: Consolidate
**Input:** Gathered signal + current MEMORY.md
**Output:** Updated MEMORY.md

Operations:
1. **Merge duplicates** — same fact noted in 3 sessions → one clean entry
2. **Absolute dates** — "yesterday we decided X" → "On 2026-03-25 we decided X"
3. **Delete contradictions** — if user corrected a fact, remove the old version
4. **Remove stale** — references to deleted files, completed tasks, resolved issues
5. **Promote learnings** — high-priority pending items from `.learnings/` → MEMORY.md sections
6. **Size management** — keep MEMORY.md focused; archive very old sections if needed

### Phase 4: Sync
**Input:** Consolidated MEMORY.md + gathered signal
**Output:** Updated Obsidian vault + dreaming log

Obsidian sync (if enabled):
1. Compare MEMORY.md sections against vault notes
2. Create new notes for topics not yet in vault (with tags, wikilinks)
3. Update existing notes with new information
4. Track plans: `task_plan.md` files → `Plans/<name>.md` notes
5. Update plans dashboard

Dreaming log:
- Write entry with: timestamp, duration, tokens, cost, what changed

## Comparison: AutoDream vs Memory Dreaming

| Aspect | Claude Code AutoDream | Memory Dreaming |
|---|---|---|
| **Runtime** | Claude Code (project-scoped) | OpenClaw (agent-scoped) |
| **Trigger** | 24h + 5 sessions | Time-only (≥6h) |
| **Memory format** | MEMORY.md + topic files | MEMORY.md + daily logs + learnings |
| **External sync** | None | Obsidian vault (opt-in) |
| **Plan tracking** | None | Scans for task_plan.md → Obsidian |
| **Execution** | Background sub-agent | Isolated cron agentTurn |
| **Index management** | Keeps MEMORY.md < 200 lines | Configurable size limit |

## Design Decisions

1. **Time-only gate** — OpenClaw generates sessions constantly via heartbeats/crons/subagents. Session count is not a meaningful signal. Time since last dream is.

2. **Grep not read** — Session transcripts can be huge. Targeted grep for correction/decision/save patterns extracts 90% of the value at 10% of the token cost.

3. **Obsidian is opt-in** — Not everyone uses Obsidian. The core consolidation (MEMORY.md) works without it. Obsidian sync is a bonus.

4. **Never delete source files** — Daily logs and learnings are append-only source material. Dreaming reads from them and writes to MEMORY.md + Obsidian. Source files are never modified or deleted.

5. **Idempotent** — Running the dream cycle twice in a row produces the same result. The second run sees nothing new and writes nothing.
