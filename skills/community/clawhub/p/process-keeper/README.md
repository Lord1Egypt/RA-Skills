# Process Keeper

`process-keeper` is a lightweight skill for turning development work into a reusable process log.

It helps you:

- backfill what happened so far in a project
- record important decisions, fixes, and turning points
- keep a compact history for future review
- extract article-ready notes from development work

## When to use

Use this skill when the work is about:

- project history
- key decisions
- bug fix records
- retrospective notes
- narrative material for posts or articles

## Install

Clone this repository and place it in your local skills directory, or point your agent to the folder if your setup supports custom skill paths.

There is no build step.

## When not to use

Do not use it for:

- feature implementation
- task management
- daily chat logs
- tiny edits that do not change the direction
- private project details in public output

## How to trigger

Use a short instruction like:

- "Backfill the process so far"
- "Record this decision"
- "Turn this into a retrospective"
- "Keep a process log for this project"
- "Extract reusable notes from this iteration"

## What it outputs

The default output should be compact and structured.

Preferred fields:

- time
- context
- problem
- decision
- change
- result
- lesson
- article angle

Short version:

- what happened
- why it changed
- what changed after
- how to move faster next time

## Minimal workflow

1. Find the active project root.
2. Reconstruct the timeline from commits, files, and context.
3. Keep only meaningful nodes.
4. Write the process note in a compact format.
5. Extract reusable material only when asked.

If the repo has no process notes yet, create `docs/process/`.

The supporting files in this repository are:

- `SKILL.md`
- `PROCESS_GUIDE.md`
- `references/process-template.md`
- `references/examples.md`
- `agents/openai.yaml`

## Example

**User:** "We changed the result page structure. Record why."

**Expected output:** one compact process entry with the problem, decision, change, result, and lesson.

## Compatibility

This skill is designed to work with local coding agents and repo-aware assistants.

It should be usable with:

- Codex-style local agents
- Claude-style local agents
- editor-integrated agents
- other repo-aware coding assistants

## Boundary

This skill keeps process notes lightweight.

It is not meant to:

- flood the repo with transcripts
- mix process notes with product code
- record every tiny edit
- expose private paths or internal-only notes in public output
