# External State Machine

Use this file as the operational contract for long-form novel projects.

## Goal
Keep project state outside chat so the orchestrator can resume, review, and continue long projects without carrying the whole book in context.

## State sources
Treat these as the source of truth:
- `project.json`
- `worldbuilding.md`
- `characters.md`
- `outline.md`
- `style.md`
- `memory.md`
- `chapters/*.md`
- `state/current.json` when present

`state/current.json` is the concise runtime snapshot. Prefer it for quick recovery and chapter-boundary checks, then fall back to the longer files for detail.

## Canonical flow
1. Discover project(s) if the request is resume/continue.
2. Read the smallest relevant canon slice.
3. Confirm execution mode and model mapping.
4. Lock premise, hard canon, and style before prose.
5. Draft one 10-chapter batch outline at a time.
6. If the full outline changes, invalidate any derived batch outline and regenerate it before drafting chapters.
7. Run writer → reviewer → orchestrator for the chapters inside the locked batch outline.
8. Sync chapter, memory, and state after acceptance.

## State machine
Recommended runtime steps:
- `idle`
- `project_discovered`
- `project_locked`
- `batch_outline_planned`
- `chapter_planned`
- `writer_running`
- `writer_done`
- `reviewer_running`
- `reviewer_done`
- `revision_needed`
- `chapter_accepted`
- `state_synced`

## What must live in files
- title, genre, audience, target length
- taboo list and hard canon
- model assignments
- latest chapter index and checkpoint
- character states and open loops
- style rules and forbidden phrasing
- chapter summaries and resume recovery notes

## What must not live only in chat
- whole-book memory
- authoritatively fixed canon
- model assignments
- recovery checkpoints
- style lock rules
- accepted chapter history

## Orchestrator rule
The main session should only assemble context, route work, verify outputs, and write state back. It should not silently author prose or invent missing canon.

## Failure handling
If a required fact is missing, pause and ask. If reviewer output arrives without writer prose, treat the workflow as incomplete, not as a valid review.
If the full outline changes, clear any derived batch-outline state before continuing.
