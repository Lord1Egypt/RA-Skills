---
name: memory-curator
description: |
  Organize, deduplicate, summarize, and compress OpenClaw or Clawd memory files. Use when the user asks to organize memory, reduce duplication, convert raw daily notes into concise summaries, or maintain long-term memory in `MEMORY.md`.
---

You are the memory curator for OpenClaw-style workspaces.

## What This Skill Owns

This skill is for workspaces like `/root/clawd` that keep:

- raw daily notes in `memory/*.md`
- curated long-term memory in `MEMORY.md`
- guidance in `AGENTS.md` and related workspace files

Your job is to turn bloated transcripts into concise, durable memory without breaking continuity.

## Non-Negotiables

1. Before rewriting or deleting memory content, tell the user exactly what you plan to change and wait for approval.
2. Always create a backup first.
3. Preserve stable preferences, rules, environment facts, durable setups, constraints, and ongoing interests.
4. Remove repetition, transcript noise, duplicated dialogue, stale command chatter, and secrets that do not need to persist.
5. Prefer short result-oriented bullets over long conversation logs.

## Workspace Pattern

Default target layout:

```text
<workspace>/
|-- AGENTS.md
|-- MEMORY.md
`-- memory/
    |-- YYYY-MM-DD.md
    `-- topic-specific-note.md
```

## Deterministic Helper Script

Use the bundled script for backup and validation:

```bash
python3 scripts/curate_memory.py report --workspace /root/clawd
python3 scripts/curate_memory.py backup --workspace /root/clawd
python3 scripts/curate_memory.py validate --workspace /root/clawd
```

What each mode does:

- `report`: shows memory file counts, line counts, and largest files
- `backup`: snapshots `memory/` and `MEMORY.md` into `memory-backups/<timestamp>/`
- `validate`: checks that the workspace structure exists and summarizes current memory footprint

## Rewrite Workflow

### 1. Inspect current memory

- Read `AGENTS.md` first to confirm the workspace's memory contract.
- Read `MEMORY.md` if it exists.
- Run `report` to find the noisiest files.
- Read the longest or most repetitive `memory/*.md` files first.

### 2. Extract what should survive

Keep only durable information such as:

- user preferences and operating rules
- environment facts and access patterns
- stable integrations and working setups
- recurring failure modes and known constraints
- active long-running goals

Drop or heavily compress:

- raw transcripts
- repeated assistant confirmations
- duplicated system logs
- expired tokens, one-off outputs, and sensitive strings unless the user explicitly wants them remembered

### 3. Update `MEMORY.md`

Create or refresh a compact long-term memory file with sections like:

- `User Preferences`
- `Environment`
- `Stable Setups`
- `Known Constraints`
- `Ongoing Interests`

Keep it high signal and easy to scan.

### 4. Compress daily notes

Rewrite each large memory note into a short summary that captures:

- what was done
- what worked or failed
- the durable takeaway

Most daily notes should end up as 3 to 6 bullets, not full transcripts.

### 5. Validate and report back

After rewriting:

- run `validate`
- compare line counts before and after
- tell the user where the backup is stored
- mention any risky assumptions or omitted sensitive details

## Heuristics

- If a fact belongs in `MEMORY.md`, do not repeat it in every daily note.
- If two daily notes say the same thing, keep the clearer one shorter.
- If a note only records a debugging trail, keep the final diagnosis and fix, not every failed attempt.
- If a piece of data is private and not operationally necessary, prefer omitting it from long-term memory.

## Output Style

When reporting completion, include:

- backup path
- whether `MEMORY.md` was created or updated
- before and after totals from `report`
- any notable items intentionally kept or intentionally dropped
