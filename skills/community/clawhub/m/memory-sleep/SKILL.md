---
name: memory-sleep
description: "Lightweight memory consolidation for OpenClaw agents. Reviews recent daily memory files (`memory/*.md`), extracts durable knowledge, and merges it into `MEMORY.md` without imposing a new file architecture. Triggers: dream, consolidate memory, memory consolidation. Works well with manual runs or a simple nightly cron."
---

# Sleep — Lightweight Memory Consolidation for OpenClaw

`memory-sleep` is a small, conservative skill for agents that keep:
- daily notes in `memory/YYYY-MM-DD.md`
- long-term knowledge in `MEMORY.md`

It does **not** introduce extra indexes, dashboards, archives, or custom memory schemas.
Its job is simple: keep `MEMORY.md` fresh while daily files remain raw journals.

## Use When

- User says `dream`
- User asks to consolidate memory
- A nightly cron runs the skill
- Daily memory files are piling up and `MEMORY.md` is getting stale

## Goals

- Keep the existing OpenClaw-style memory structure
- Distill durable facts from recent journals
- Correct stale information in `MEMORY.md`
- Avoid over-editing or inventing new structure

## Inputs

- `MEMORY.md`
- `memory/YYYY-MM-DD.md` files

## Outputs

- Updated `MEMORY.md`
- Optional short run note appended to today's daily file

## Consolidation Flow

### 1. Orient

1. Read `MEMORY.md`
2. List files in `memory/`
3. Focus on recent daily files first

### 2. Scan Recent Daily Files

Default window: last **7 days**.

Extract only durable items such as:
- preferences
- decisions
- recurring facts
- important project context
- corrections to stale memory

Ignore or down-rank:
- routine acknowledgements
- temporary chatter
- one-off noise with no lasting value

### 3. Merge Conservatively into `MEMORY.md`

Use surgical edits only.

Allowed operations:
- **Add** new durable facts
- **Correct** stale facts with newer confirmed info
- **Deduplicate** overlapping entries
- **Prune** clearly obsolete items when confidence is high
- **Absolutize** relative dates where useful

Do **not**:
- rewrite the whole file unnecessarily
- create a new memory system
- add bureaucratic structure unless the file already uses it

### 4. Optional Journal Marking

For older files already consolidated, optionally prepend a short HTML comment such as:

```html
<!-- consolidated to MEMORY.md on YYYY-MM-DD -->
```

Never delete journal files.

### 5. Report Briefly

Return a short summary like:

```text
🌙 Dream complete
- Scanned N daily files
- MEMORY.md: +N added / ~N corrected / -N pruned
```

## Rules

- Prefer the existing workspace memory architecture
- `MEMORY.md` is the primary long-term memory output
- Daily files remain journals, not databases
- Be conservative when removing information
- Avoid leaking secrets into reports or memory summaries
- If logging the run, keep it short

## Recommended Cron

Nightly example:

```text
0 3 * * *
```

Example job message:

```text
Execute dream skill: consolidate memory
```

## Design Principle

This skill is intentionally minimal.

It is for users who want:
- lightweight consolidation
- compatibility with default OpenClaw memory habits
- no imposed sidecar files unless they choose to add them later

Think of it as a careful editor, not a memory framework.