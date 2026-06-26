---
name: memory-pipeline
description: Install, repair, and validate a persistent memory workflow for OpenClaw-style agents using Markdown memory files plus recurring cron jobs. Use when setting up or fixing MEMORY.md / memory/ structures, adding inbox→raw→daily→weekly memory pipelines, creating or auditing memory-related cron jobs, defining how an agent should capture preferences, decisions, todos, project state, and long-term rules across sessions, or introducing structured memory folders such as memory/projects/ and memory/system/.
---

# Memory Pipeline

Install and maintain a Markdown-based personal memory system with four layers:

1. **Capture layer** — `memory/inbox.md` for newly learned, high-value context
2. **Archive layer** — hourly raw notes in `memory/YYYY-MM-DD-raw.md`
3. **Summary layer** — daily highlights in `memory/YYYY-MM-DD.md`
4. **Long-term layer** — `MEMORY.md` plus optional structured topic files under `memory/projects/`, `memory/system/`, and `memory/groups/`

Prefer a **curated memory** workflow, not full transcript dumping. Default to recording preferences, decisions, todos, project state, lessons learned, and other details that will matter later.

## Workflow decision tree

Use this skill in one of four modes:

### 1. Fresh install
Use when the workspace has no stable memory structure yet.

Do this:
- read `references/directory-layout.md`
- create the base files/directories
- install all three cron jobs
- run the acceptance checks from `references/verification.md`

### 2. Repair / audit
Use when memory files exist but the workflow is unreliable.

Do this:
- read `references/verification.md`
- identify whether the failure is in capture, hourly archive, daily summary, or weekly review
- repair only the broken layer
- rerun acceptance checks

### 3. Structured memory upgrade
Use when the user already has basic memory files but wants clearer separation of project rules, system rules, or group-specific context.

Do this:
- read `references/directory-layout.md`
- add `memory/projects/`, `memory/system/`, and `memory/groups/`
- keep the existing inbox/raw/daily/MEMORY chain as the primary backbone
- migrate only durable topic-specific material into the structured folders

### 4. Policy / behavior design
Use when the user wants to define what should be remembered, what should be ignored, or how dense memory capture should be.

Do this:
- read `references/memory-rules.md`
- set the default capture mode
- define user-controlled overrides such as “remember this” / “don’t remember this”

## Quick start

When asked to create or repair the memory system, read these references in order:

1. `references/directory-layout.md`
2. `references/memory-rules.md`
3. `references/cron-spec.md`
4. `references/verification.md`
5. `references/migration-and-repair.md` when upgrading or repairing an existing setup

If the user wants the full workflow, create or verify all of the following:

- `MEMORY.md`
- `memory/inbox.md`
- `memory/YYYY-MM-DD-raw.md` (created on demand)
- `memory/YYYY-MM-DD.md` (created by daily summary job)
- `memory/projects/`
- `memory/system/`
- `memory/groups/`
- three cron jobs:
  - hourly inbox → raw archive
  - daily raw/context → daily summary
  - weekly daily summaries → `MEMORY.md`

## Core operating model

Use this memory flow:

```text
conversation → memory/inbox.md → memory/YYYY-MM-DD-raw.md → memory/YYYY-MM-DD.md → MEMORY.md
```

Treat `memory/projects/`, `memory/system/`, and `memory/groups/` as **structured sidecars**, not replacements for the main flow.

## Capture policy

### What goes into `memory/inbox.md`

Write to `memory/inbox.md` when the conversation reveals:

- user preferences
- important decisions
- todos or reminders
- project status changes
- recurring workflow rules
- corrections, mistakes, or lessons learned
- context that will likely matter in a future session

Do **not** default to storing every message or full chat transcripts.

### Default memory mode

Use **concise / curated memory mode** unless the user explicitly asks for higher-fidelity logging.

In concise mode:

- summarize instead of quoting entire exchanges
- prefer concrete facts over vague summaries
- avoid duplicate entries
- skip transient chatter with no future value

If the user says things like **“remember this”**, **“记一下”**, or asks to retain a whole exchange, increase capture density for that segment.

If the user says **“don’t remember this”** or **“别记”**, exclude that content from memory.

See `references/memory-rules.md` for the compact ruleset.

## Structured memory directories

Use structured topic files when date-based notes are not enough.

### `memory/projects/`

Store long-running project context here:

- project background
- milestones
- confirmed approaches
- known blockers
- next-step context needed to resume work later

Examples:

- `memory/projects/159755-weekly-tracking.md`
- `memory/projects/openclaw-browser.md`

### `memory/system/`

Store durable operating rules and environment-specific conventions here:

- messaging preferences
- browser workflow defaults
- memory pipeline rules
- tool-specific operating rules that remain true over time

Examples:

- `memory/system/telegram-rules.md`
- `memory/system/browser-defaults.md`
- `memory/system/memory-pipeline.md`

### `memory/groups/`

Use for group-specific context when the same agent participates in multiple group chats and needs separate social or project memory.

## Recommended install order

When installing from scratch, use this order:

1. create or verify `MEMORY.md`
2. create `memory/` and `memory/inbox.md`
3. create `memory/projects/`, `memory/system/`, `memory/groups/`
4. define the memory policy (concise by default unless user requests otherwise)
5. install the hourly archive job
6. test hourly archive with a seed item in `memory/inbox.md`
7. install the daily summary job
8. install the weekly long-term review job
9. run the full acceptance checklist

Do not install only the daily/weekly jobs while leaving the capture layer undefined. The hourly job depends on reliable writes into `memory/inbox.md`.

## Cron workflow

Install or repair these three jobs together unless the user explicitly wants only part of the pipeline.

### 1. Hourly archive job

Suggested name:
- `context: compress chat history (hourly)`

Purpose:
- read `memory/inbox.md`
- process only `## pending`
- append the new content into `memory/YYYY-MM-DD-raw.md`
- group entries under `## YYYY-MM-DD HH:00 Asia/Macau`
- merge into an existing same-hour section if present
- deduplicate near-identical items
- clear processed pending items afterward
- stay silent (no user-visible message)

### 2. Daily summary job

Suggested name:
- `daily-memory-diary`

Purpose:
- create or update `memory/YYYY-MM-DD.md`
- write only the 1–2 most important items from the day
- keep the summary brief and specific
- stay silent

### 3. Weekly long-term review job

Suggested name:
- `weekly-memory-review`

Purpose:
- review recent `memory/YYYY-MM-DD.md` files
- extract durable preferences, decisions, recurring projects, and long-lived rules
- update `MEMORY.md`
- avoid copying one-off noise into long-term memory
- stay silent

See `references/cron-spec.md` for a recommended spec and guardrails.

## Verification and repair

When asked to verify or fix the system:

1. check required files and directories exist
2. check the three cron jobs exist and are enabled
3. check recent run status for each job
4. if the hourly job claims success, confirm that:
   - inbox pending items were cleared or marked processed
   - the raw file actually received a new section or merged content
5. if the daily job claims success, confirm the daily summary file exists and is non-empty
6. if the weekly job claims success, confirm `MEMORY.md` was updated only with durable information

Common failure modes:

- inbox exists but nothing is ever written into it
- cron run reports `ok` but raw file was checked before the run actually finished
- raw file is missing and the prompt forgot to require creating it
- same-hour sections duplicate because merge logic was too brittle
- daily or weekly jobs copy too much noise because memory rules were not explicit enough
- structured folders exist but nothing routes into them because placement rules were never defined

Use `references/verification.md` for the validation checklist.
Use `references/migration-and-repair.md` for upgrades and partial repairs.

## Resource map

### Scripts

- `scripts/init_memory_pipeline.py` — create the base directory structure and seed core templates without overwriting existing files
- `scripts/verify_memory_pipeline.py` — verify the workspace memory structure, inbox format, basic downstream artifacts, and best-effort cron health; checks expected cron names plus workspace-path fingerprints in cron payloads, and supports `--skip-cron` with configurable cron timeout for slower environments

### References

- `references/directory-layout.md` — file layout and what belongs where
- `references/memory-rules.md` — concise memory policy and capture rules
- `references/cron-spec.md` — three-job pipeline spec, naming, and recommended behavior
- `references/verification.md` — acceptance checks and troubleshooting
- `references/migration-and-repair.md` — how to upgrade an existing flat memory setup into this pipeline

## Scope boundary

This skill is for a **Markdown memory workflow backed by cron jobs**.

Do not expand it into a separate external database or cloud memory product unless the user explicitly asks. Prefer keeping memory:

- readable
- editable by hand
- stored in the workspace
- aligned with the user’s existing `MEMORY.md` and `memory/` workflow
