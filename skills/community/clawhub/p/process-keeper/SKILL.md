---
name: process-keeper
description: Backfill project timelines, capture key decisions and fixes, and extract reusable process notes from development work.
---

# Process Keeper

Use this skill when you want to turn project activity into a lightweight, reusable process log.

## Best for

- backfilling what happened so far in a project
- recording important decisions, fixes, and turning points
- keeping a compact history for future review
- extracting article-ready notes from development work
- maintaining a simple process trail without flooding the repo

## Good triggers

- "Backfill the history so far"
- "Record this decision"
- "Turn this work into a retrospective"
- "Keep a process log for this project"
- "Extract reusable notes from this iteration"

## What it does

This skill helps you:

- reconstruct a project timeline from commits, files, and conversation context
- capture only meaningful nodes: problem, decision, change, result, lesson
- keep the process notes compact and readable
- turn process notes into reusable summaries, outlines, or narrative material

## What it is not

- not a task manager
- not a daily journal
- not a code review tool
- not a replacement for feature specs
- not a place to dump every tiny edit

## Core workflow

1. Find the project root.
   - Prefer the active repository.
   - If the repo has no process notes yet, create `docs/process/`.

2. Backfill first, then continue.
   - Reconstruct the timeline from commits, files, and available context.
   - Capture only the meaningful nodes.
   - Avoid transcript-style narration.

3. Keep three layers.
   - `HISTORY.md` for the timeline
   - `PROCESS_GUIDE.md` for recording rules
   - `TEMPLATE.md` for reusable entry structure

4. Record at key nodes.
   - major UI or UX changes
   - architecture or versioning changes
   - bug fixes with a clear cause
   - design disagreements that get resolved
   - successful or failed verification

5. Extract reusable material when asked.
   - retrospective
   - project narrative
   - article outline
   - "how we solved it" notes

## Output style

Prefer compact records over long narrative blocks.

### Default fields

- time
- context
- problem
- decision
- change
- result
- lesson
- article angle

### Short version

Use a short version when the user only needs a quick record.

- what happened
- why it changed
- what changed after
- how to move faster next time

## Public-use notes

- Keep public output free of private project names, private paths, and internal-only notes.
- Keep examples generic so they work in any repository.
- If a tiny edit did not change the direction, skip it.

## Compatible use

This skill is designed to work with local coding agents and project assistants that can read files and write process notes.

Examples:

- Codex-style local agents
- Claude-style local agents
- editor-integrated agents
- other repo-aware coding assistants

## Files

- `PROCESS_GUIDE.md`
- `references/process-template.md`
- `references/examples.md`
- `agents/openai.yaml`
