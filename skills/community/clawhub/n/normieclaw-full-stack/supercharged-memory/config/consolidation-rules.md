# Consolidation Rules

How the agent maintains MEMORY.md and the semantic memory files during periodic consolidation cycles.

---

## When Consolidation Runs

- Triggered during heartbeat checks when `last_consolidation` in `memory/heartbeat-state.json` is older than `consolidation.interval_hours` (default: 24 hours)
- Can also be triggered manually: user says "consolidate my memory" or "clean up your notes"
- Emergency trigger: MEMORY.md exceeds `memory_md.max_memory_md_chars` (default: 6000 chars)

---

## What Gets Promoted to MEMORY.md

### Promote If:
- A **preference** was expressed clearly ("I prefer X over Y") — promote as a bullet under `## Preferences`
- A **decision** was made that affects future work ("We're going with React for the frontend") — promote under `## Key Decisions`
- A **new person** was introduced who will be referenced again ("My manager Sarah handles approvals") — promote under `## About My Human` or `## People`
- A **project** started or changed status — promote under `## Active Projects`
- A **lesson was learned** from a mistake or discovery — promote under `## Lessons Learned`
- The same fact appears in **3+ daily notes** — it's clearly important, promote it

### Do NOT Promote:
- Routine work logs ("Fixed the CSS on the button") — these stay in daily notes
- One-off conversations that won't be referenced again
- Temporary states ("Waiting for Bob's reply") — unless still relevant
- Anything already in MEMORY.md (check for duplicates before adding)

---

## What Gets Moved to Semantic Files

### Move to `memory/semantic/<topic>.md` If:
- A topic has accumulated **5+ entries** across daily notes and MEMORY.md
- The topic is deep enough to warrant its own file (project details, infrastructure notes, a person's full context)
- MEMORY.md is over the size target and needs trimming — move detail to semantic files, keep a one-liner reference in MEMORY.md

### Semantic File Naming
- Use lowercase, hyphenated names: `memory/semantic/kitchen-renovation.md`, `memory/semantic/sarah-manager.md`
- One file per major topic. Don't create a file for something mentioned once.
- Include a header with the topic name and last-updated date

### Semantic File Format
```markdown
# [Topic Name]
_Last updated: YYYY-MM-DD_

## Summary
- One paragraph overview

## Key Details
- Specific facts, decisions, context

## History
- Chronological notes (date-stamped)
```

---

## What Gets Pruned from MEMORY.md

### Prune If:
- The information is **outdated** — a decision was reversed, a project was completed, a person left
- The entry has been **fully migrated** to a semantic file — replace with a one-liner reference: "See `memory/semantic/kitchen-renovation.md`"
- **Duplicate entries** exist — merge into one clean entry
- The entry is **too detailed** for MEMORY.md — move detail to semantic file, keep summary
- A "temporary" entry (waiting for X, trying Y) has been resolved

### Never Prune:
- Active preferences (unless the user explicitly changes them)
- Security-relevant information
- Contact details or relationships that are still active
- Lessons learned (these compound over time)

---

## Consolidation Output

After each consolidation cycle, the agent should:
1. Update `memory/heartbeat-state.json` with the new `last_consolidation` timestamp
2. **Not** announce consolidation to the user unless they asked for it
3. If significant changes were made (>5 entries added/removed), log a brief summary in today's daily notes:
   ```
   ## Memory Consolidation — HH:MM
   - Promoted 3 entries to MEMORY.md
   - Moved infrastructure details to memory/semantic/infrastructure.md
   - Pruned 2 outdated entries
   - MEMORY.md size: 4,200 chars (target: 6,000)
   ```

---

## Size Management

### MEMORY.md Target: Under 6,000 Characters
- At 5,000 chars (`warn_at_chars`): start being more selective about new promotions
- At 6,000 chars (`max_memory_md_chars`): trigger pruning pass before adding anything new
- Strategy: move detail → semantic files, keep one-liner references in MEMORY.md

### Daily Notes: No Size Limit
- Daily notes can grow freely — they're append-only during the day
- Old daily notes (30+ days) can optionally be archived but should NOT be deleted — they're the source of truth

### Semantic Files: Moderate Size
- Target: under 3,000 chars each
- If a semantic file gets too large, consider splitting into sub-topics
