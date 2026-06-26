# Session Continuity Protocol

This file defines the **hot-effective** long-task workflow for this workspace. It is designed to improve continuity **without** requiring hooks, plugins, gateway restarts, or source-code changes.

## When this protocol activates

Activate this protocol for any task that is multi-step, long-running, likely to touch multiple files/systems, or likely to stretch context.

Typical triggers:
- more than one real phase
- more than one independent workstream
- likely to take more than ~10 minutes
- likely to require multiple tool calls or validation loops
- anything the user may want resumed later without guesswork

## Immediate actions on task intake

For an activated task, do these immediately:

1. Append a task-intake note to `memory/YYYY-MM-DD.md`
2. Create or update `plans/YYYY-MM-DD-<task-slug>.md`
3. Create or update `status/YYYY-MM-DD-<task-slug>.md`

The daily memory note is for **durable intake + decisions**.
The plan file is for **intended structure**.
The status file is for **current truth**.

## Session isolation

Treat each session as isolated by default.

Rules:
- Do **not** assume unstated work from older sessions.
- Do **not** “fill in” missing context from vibes or partial recollection.
- Only carry forward facts that appear in one of these places:
  - the current conversation
  - `memory/YYYY-MM-DD.md`
  - `MEMORY.md` when appropriate
  - `plans/`, `status/`, or `handoff/` files
  - an explicitly supplied transcript or tool result
- If continuity is uncertain, say so and recover from written artifacts instead of inventing continuity.

## Parallel-first execution

When safe, prefer independent steps in parallel over serial progress theater.

Do this:
- parallelize independent reads, inspections, searches, and low-risk edits
- keep true dependencies serial
- converge results back into the status file after each phase

Do not do this:
- stretch a task by serializing obviously independent checks
- hide lack of progress behind repetitive micro-updates

## Required files and naming

Use a stable task slug in kebab-case.

Recommended naming:
- `plans/YYYY-MM-DD-<task-slug>.md`
- `status/YYYY-MM-DD-<task-slug>.md`
- `handoff/YYYY-MM-DD-<task-slug>.md`

If the same root task continues on the same day, keep the same slug and update the files instead of creating fragmented duplicates.

## Plan file rules

The plan file must exist before major execution for any activated task.

A good plan should contain:
- root task
- scope / non-goals
- critical constraints
- success criteria
- phased execution plan
- explicitly parallelizable workstreams
- validation plan

Update the plan only when the plan meaningfully changes.

## Status / checkpoint rules

The status file is the operational source of truth.

Update it:
- after each completed phase
- after each important decision
- when a blocker appears or clears
- before sending a substantial final report on a long task
- before pausing work that might need later resumption

The status file should stay short, factual, and current.

## Handoff rules

Create or update a handoff when:
- the user asks to pause or continue later
- context pressure reaches the handoff zone
- the task is blocked on external approval/login/payment
- the session may need to be resumed elsewhere

A handoff must contain at least:
- Root task
- Current status
- Completed
- Remaining
- Critical constraints
- Files / paths
- Commands / outputs worth preserving
- Key decisions
- Known blockers
- Next best action

## Context-pressure policy

Use `session_status` when you need a more reliable context reading than UI footer estimates.

### 80%+ — silent durability refresh
- refresh the relevant `status/` file when durable task state changes
- keep user-facing answer quality normal
- do not shorten prose or simplify reasoning just to save context

### 85%+ — successor preparation
- prepare continuity metadata for a clean successor handoff
- create or refresh the relevant `handoff/` file in the background when needed
- preserve commands, outputs, and decisions without degrading the visible reply

### 88%+ — predictive switch preparation
- if the next turn is likely to cross 90% context usage, prepare rollover before visible quality drops
- prefer background continuity preparation over visible compression tactics

### 90%+ — successor takeover
- roll over to a successor session for the next formal answer
- the current session should preserve durable state and hand off cleanly
- do not rely on visibly shorter or lower-quality answers as the primary control strategy

## Memory logging conventions

When a task is activated, add a concise intake note to the daily memory file including:
- root task
- scope boundaries
- unusual constraints
- the task slug / related files when useful

Also log:
- important decisions
- unexpected blockers
- conclusions that matter beyond the current turn

Do **not** use `temp/` as the only source of truth for anything important.

## temp/

Use `temp/` only for scratch notes, rough dumps, or transient working material.
Anything needed for continuity must be promoted to `memory/`, `plans/`, `status/`, or `handoff/`.
