---
name: openclaw-dream
description: "Automatic memory consolidation for OpenClaw agents. Cleans, deduplicates, and organizes memory files (MEMORY.md + memory/*.md) like human REM sleep consolidates memories. Triggers: 'dream', 'consolidate memory', 'tidy memory', 'clean up memory', '整理记忆', '记忆整理', or automatically via cron/heartbeat. Use when memory files have accumulated noise, contradictions, stale dates, duplicates, or exceed manageable size."
---

# OpenClaw Dream

Automatic memory consolidation — turn scattered daily notes into clean, organized long-term memory.

## Overview

Memory files accumulate noise over time: relative dates lose meaning, contradictory entries confuse the agent, duplicates waste context, and stale information causes hallucinations. Dream fixes this by running a structured consolidation pass.

## When to Run

- **Manual**: User says "dream", "整理记忆", "consolidate memory"
- **Cron**: Schedule via `openclaw cron add` for daily execution (recommended: 3-4 AM)
- **Heartbeat**: Add to HEARTBEAT.md as a periodic task (every 3-5 days)
- **Condition check**: Only run if `memory/.last_dream` is older than 24h AND new daily notes exist since last dream

## Execution

**Always run as a sub-agent** to avoid blocking the main session:

```
sessions_spawn:
  task: "Run openclaw-dream consolidation. Read the skill at skills/openclaw-dream/SKILL.md first."
  mode: run
  model: sonnet  # use a cheaper model
```

For manual triggers in the main session, spawn the sub-agent, reply to user "开始整理记忆，稍后汇报结果", then yield.

## Four-Phase Consolidation

### Phase 1: Scan

1. Read `MEMORY.md` — note current line count, section headers, last-updated date
2. Read all `memory/YYYY-MM-DD.md` files from the last 14 days
3. Read `memory/self-improving/*.jsonl` if it exists (error/correction/best_practice/decision logs)
4. Read `.last_dream` timestamp to know what's already been processed
5. Build a mental map: what topics exist, what's fresh, what's stale

### Phase 2: Analyze

Scan all content for these problems:

**Relative dates** — Find phrases like "yesterday", "today", "last week", "recently", "刚才", "昨天", "上周". Cross-reference with the file's date to compute the absolute date.

**Contradictions** — Same topic with conflicting conclusions across different files. Examples:
- "API uses Express" in one file, "migrated to Fastify" in another
- Different pricing numbers for the same product on different dates

**Duplicates** — Same fact recorded in multiple daily notes. Example:
- Three different files all note the same build command or deployment step

**Stale entries** — Information about things that no longer exist:
- References to deleted files or deprecated APIs
- Completed tasks still marked as "in progress"
- Resolved issues still listed as open

**Unprocessed JSONL patterns** — High-frequency errors or corrections in self-improving logs that should become rules in MEMORY.md

**Important events not yet in MEMORY.md** — Significant decisions, lessons, or changes in daily notes that deserve long-term retention

### Phase 3: Consolidate

Execute fixes in this order:

1. **Date absolutization**: Replace relative dates with absolute dates
   - "Yesterday we decided X" (in 2026-03-15.md) → "2026-03-14: decided X"
   - Preserve the original meaning; only change the date reference

2. **Contradiction resolution**: Keep the most recent entry, remove or mark the old one
   - Add `[superseded by YYYY-MM-DD]` to the old entry if in a daily note
   - In MEMORY.md, simply update to the latest fact

3. **Duplicate merging**: Consolidate into one canonical entry
   - Keep the most complete/detailed version
   - Note the date range if relevant ("first noted YYYY-MM-DD")

4. **Stale cleanup**: Remove or archive entries about things that no longer exist
   - Mark completed projects as done with completion date
   - Remove references to deleted files/configs

5. **JSONL distillation**: Extract patterns from self-improving logs
   - Errors appearing ≥2 times → add rule to MEMORY.md "经验教训" section
   - Important decisions → add to appropriate MEMORY.md section
   - Update `memory/self-improving/.last_distill` timestamp

6. **Daily notes → MEMORY.md promotion**: Identify significant items worth keeping long-term
   - Major decisions, architectural changes, new integrations
   - People/relationships updates
   - Lessons learned
   - Do NOT promote routine operational logs

### Phase 4: Write

1. **Update MEMORY.md**:
   - Apply all changes from Phase 3
   - Keep total line count under 250 lines (warn if approaching)
   - Update the `*最后更新*` date at the bottom
   - Preserve existing section structure (don't reorganize unless necessary)

2. **Rebuild vector index**:
   ```bash
   openclaw memory index --force
   ```

3. **Generate dream log** at `memory/dream-log-YYYY-MM-DD.md`:
   ```markdown
   # Dream Log YYYY-MM-DD

   ## Changes Made
   - [date-fix] 3 relative dates converted to absolute
   - [contradiction] Removed stale Express reference (superseded by Fastify migration)
   - [duplicate] Merged 2 duplicate build command entries
   - [stale] Marked ChatClaw Phase 2 as completed
   - [promote] Added RhinoRank order tracking to MEMORY.md
   - [distill] Added 1 new rule from error logs

   ## MEMORY.md Stats
   - Lines: 119 → 128
   - Sections: 8 (unchanged)

   ## Skipped
   - 5 daily notes with only routine operational logs (no action needed)
   ```

4. **Update timestamp**:
   ```bash
   date -u +%Y-%m-%dT%H:%M:%SZ > memory/.last_dream
   ```

## Safety Rules

- **Never delete daily note files** — only modify MEMORY.md and generate dream-log
- **Never modify source code, configs, or non-memory files**
- **Preserve all 📌 pinned entries** in MEMORY.md (lines starting with 📌 are never removed)
- **When uncertain about a contradiction**, keep both entries and flag in dream-log as "needs human review"
- **Dream-log is append-only** — never modify past dream logs

## Configuration

Users can create `DREAM.md` in workspace root to customize behavior:

```markdown
# DREAM.md

## Settings
- max_memory_lines: 250
- lookback_days: 14
- min_hours_between_dreams: 24

## Protected Sections
<!-- These MEMORY.md sections are never auto-pruned -->
- 经验教训
- 关于 River
- Agent 网络

## Custom Rules
<!-- Additional consolidation rules -->
- Always keep pricing/billing related entries
- Merge duplicate API endpoint references
```

If `DREAM.md` doesn't exist, use defaults above.

## Cron Setup Example

```bash
openclaw cron add \
  --id dream-nightly \
  --schedule "0 3 * * *" \
  --task "Run openclaw-dream memory consolidation. Read skills/openclaw-dream/SKILL.md and follow Phase 1-4." \
  --model sonnet \
  --isolated
```
