# Migration and repair

Use this guide when the workspace already has memory files but the pipeline is incomplete, unreliable, or flat.

## Typical upgrade cases

### Case 1: `MEMORY.md` exists, but no `memory/inbox.md`

Interpretation:
- long-term memory exists
- capture layer is missing

Repair:
- create `memory/inbox.md`
- define concise capture rules
- install the hourly archive job
- test inbox → raw before touching daily/weekly jobs

### Case 2: `memory/inbox.md` exists, but raw files stay empty

Interpretation:
- capture layer exists
- archive layer is broken or unchecked

Repair:
- verify the hourly job exists and is enabled
- add a seed item under `## pending`
- trigger the job manually
- wait for completion before checking results
- confirm raw gained content and pending was cleared

### Case 3: raw files exist, but no daily summaries

Interpretation:
- archive layer works
- summary layer is missing

Repair:
- install the daily summary job
- trigger it manually once
- confirm `memory/YYYY-MM-DD.md` is created and concise

### Case 4: daily summaries exist, but `MEMORY.md` never improves

Interpretation:
- long-term review layer is missing or too weak

Repair:
- install or tighten the weekly review job
- make the prompt stricter about durable information only
- confirm the weekly run updates `MEMORY.md` without copying transient noise

### Case 5: everything exists, but memory is messy

Interpretation:
- files were created, but placement rules are unclear

Repair:
- keep the main chain intact: inbox → raw → daily → MEMORY
- introduce `memory/projects/` for durable project-specific notes
- introduce `memory/system/` for stable operating rules
- move only high-value durable topic notes into those structured folders

## Migration rules

When adding structure to an existing setup:

- do not break the working main chain
- do not move every historical note into structured folders
- do not promote daily noise into `MEMORY.md`
- migrate only durable content that is easier to use by topic than by date

## Good first migrations

Move content into `memory/projects/` when:
- it belongs to a long-running initiative
- it will be resumed later
- future work depends on that context

Move content into `memory/system/` when:
- it describes a standing rule
- it affects how the agent should behave repeatedly
- it describes environment defaults or tool habits

## Anti-patterns

Avoid these during repair:

- creating a second memory system outside the existing workspace files
- replacing the main chain with only topic folders
- storing everything forever instead of curating
- trusting ‘cron says ok’ without checking file outcomes
