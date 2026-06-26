---
name: local-agent-memory-v1
description: Build, maintain, or improve a layered local memory system for OpenClaw-style agents using markdown files instead of database-backed memory. Use when creating or refining `MEMORY.md`, `memory/YYYY-MM-DD.md`, `memory/semantic/`, `memory/procedural/`, heartbeat-based memory consolidation, skeptical memory rules, strict write discipline, long-term memory governance, or file-based agent memory workflows in local/Termux/workspace-based setups.
---

# Local Agent Memory v1

Build or refine a reliable file-based memory system for an agent.

## Core workflow

1. Create or inspect these layers:
   - `memory/YYYY-MM-DD.md`
   - `memory/semantic/`
   - `memory/procedural/`
   - `MEMORY.md`
2. Keep `MEMORY.md` lightweight and routing-oriented.
3. Put stable facts in semantic files.
4. Put repeatable methods in procedural files.
5. Treat memory as a hint/index layer, not unquestionable truth.
6. Re-verify current facts before taking real actions based on remembered information.
7. Write destination files first, then update `MEMORY.md` only if the change deserves long-term indexing.

## Decision rules

### Use daily memory for
- new events
- one-off attempts
- temporary troubleshooting detail
- anything not yet proven reusable

### Use semantic memory for
- stable user preferences
- durable environment facts
- platform constraints
- lasting architecture or governance decisions

### Use procedural memory for
- repeatable workflows
- checklists
- maintenance routines
- methods likely to be reused across sessions

## Maintenance pattern

Run a lightweight dream/consolidation pass when memory starts to sprawl:
- read `MEMORY.md`
- read recent daily logs
- identify repeated facts or workflows
- extract stable facts into semantic memory
- extract repeatable methods into procedural memory
- prune low-value or duplicated summary lines from `MEMORY.md`

Run a deeper pass for large daily logs or when the topic tree needs restructuring.

## Guardrails

- Do not let `MEMORY.md` become a diary.
- Do not promote everything that looks interesting.
- Do not rely on stale remembered facts for real actions.
- Do not mix memory maintenance with unrelated code changes unless the user asked for both.
- Prefer a few clear topic files over many overlapping files.

## References

Read these only as needed:
- `references/architecture.md` for the memory model and core disciplines
- `references/setup.md` for minimum structure and topic layout
- `references/maintenance.md` for governance and consolidation rules
