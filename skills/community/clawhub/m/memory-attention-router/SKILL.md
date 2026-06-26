---
name: memory-attention-router
description: Deterministic long-term memory routing for OpenClaw. Route, write, reflect on, and refresh reusable memory for multi-step agent work. Use when the task depends on prior sessions, durable user preferences, reusable procedures, past failures, project summaries, or stale memories that need replacement. Trigger on explicit memory phrases like "from now on", "remember this", "always", "prefer", "avoid", "my rule is", "replace my previous rule", and "going forward", and whenever an agent step needs a compact working-memory packet instead of raw history or plain RAG.
---

# Memory Attention Router Skill

Turn long-term memory into a small, role-aware working-memory packet.

Do not use this skill as plain document RAG.
Do not dump raw memory lists into model context.
Route to the right memory blocks, compose a compact packet, write back new learnings, and retire stale memory when better evidence appears.

## Trigger cues

Trigger immediately when the user states a durable rule or asks to preserve or replace memory, especially with phrases like:

- from now on
- remember this
- always
- prefer
- avoid
- my rule is
- replace my previous rule
- going forward

Also trigger when a planning, execution, critique, or response step needs compact memory state rather than raw history.

## Step roles

Choose the current step role before reading memory:

- `planner`
- `executor`
- `critic`
- `responder`

Current type preferences:

- `planner` -> `preference`, `procedure`, `summary`
- `executor` -> `preference`, `procedure`, `episode`, `reflection`
- `critic` -> `reflection`, `preference`, `summary`
- `responder` -> `preference`, `summary`, `procedure`

Important implication:

- `executor` should preserve durable hard constraints as well as reusable procedures

## Read flow

1. Build a route request with:
   - `goal`
   - `step_role`
   - `session_id` if known
   - `task_id` if known
   - `user_constraints`
   - `recent_failures`
   - `unresolved_questions`
2. Run:
   `python3 {baseDir}/scripts/memory_router.py route --input-json '<JSON>'`
3. Read the `packet`.
4. Use the packet in downstream reasoning.
5. Inspect `debug.selected_blocks` and `debug.selected_memories` when you need to understand why a memory was selected.

The router uses a deterministic two-stage flow:

1. select the best blocks from `task_scoped`, `session_scoped`, `durable_global`, and `recent_fallback`
2. score memories only inside the selected blocks

## Write flow

Store memory after important outcomes:

`python3 {baseDir}/scripts/memory_router.py add --input-json '<JSON>'`

Write memory when:

- a durable user preference or rule is learned
- a reusable procedure becomes clear
- a tool result will matter later
- a failure pattern should influence future behavior
- a stable summary is worth keeping

If a new memory replaces an older one, include `replaces_memory_id`. The router will retire the old memory, link it forward to the replacement, and persist a retirement reason.

## Reflect flow

At the end of meaningful work or after a failure cluster, create reflection and optionally procedure memory:

`python3 {baseDir}/scripts/memory_router.py reflect --input-json '<JSON>'`

Use reflection for:

- lessons
- warnings
- failure patterns
- reusable procedures derived from successful work

## Refresh flow

When new evidence invalidates or replaces older memory:

`python3 {baseDir}/scripts/memory_router.py refresh --input-json '<JSON>'`

Use refresh to:

- deactivate stale memories
- mark replacements with `replacement_memory_id`
- persist why the memory was retired with `refresh_reason`
- create contradiction links when a replacement exists

## Packet rules

A good packet contains:

- `hard_constraints`
- `relevant_facts`
- `procedures_to_follow`
- `pitfalls_to_avoid`
- `open_questions`
- `selected_memory_ids`

Current compactness targets:

- `selected_memory_ids` -> cap at 5
- `hard_constraints` -> cap at 4
- `relevant_facts` -> cap at 3
- `procedures_to_follow` -> cap at 3
- `pitfalls_to_avoid` -> cap at 3
- `open_questions` -> cap at 5

Prefer small, high-signal packets over broad recall.

## Routing rules

- Prefer durable, reusable memory over noisy transient notes.
- Preserve hard constraints for execution steps, not only planning steps.
- Use `support` edges to help validated memories win borderline ranking decisions.
- Treat `contradicts` edges directionally: penalize the stale target, not the newer memory asserting the contradiction.
- Use `summary` instead of verbose raw history when both carry the same signal.
- Retire stale memory when replacement is clear; do not allow conflicting active memories to accumulate indefinitely.

## Bootstrap

Initialize the database:

`python3 {baseDir}/scripts/memory_router.py init`

Default DB path behavior:

- if `MAR_DB_PATH` is set, that path is used
- otherwise, when installed at `<workspace>/skills/memory-attention-router`, the default is `<workspace>/.openclaw-memory-router.sqlite3`

Inspect stored memories:

`python3 {baseDir}/scripts/memory_router.py list --limit 20`

Inspect one memory:

`python3 {baseDir}/scripts/memory_router.py inspect --memory-id <ID>`

## File guide

See:

- [reference guide](references/REFERENCE.md)
- [memory schema](references/MEMORY_SCHEMA.md)
- [prompt templates](references/PROMPTS.md)
- [testing guide](references/TESTING.md)
