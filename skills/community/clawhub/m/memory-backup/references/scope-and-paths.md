# Scope and paths

Use this reference when deciding what counts as restorable OpenClaw memory.

## Core memory files

These are the primary human-authored or human-reviewed memory artifacts:
- `MEMORY.md`
- `memory/YYYY-MM-DD.md`
- other durable markdown files in `memory/`
- `DREAMS.md`
- `memory/dreaming/<phase>/YYYY-MM-DD.md`

These should normally be included when present.

## Dreaming machine state

Dreaming also writes machine state under `memory/.dreams/`.

Useful restore-oriented candidates include:
- `memory/.dreams/short-term-recall.json`
- `memory/.dreams/phase-signals.json`
- `memory/.dreams/daily-ingestion.json`
- `memory/.dreams/session-ingestion.json`
- other durable state files that represent staged memory evidence

Usually exclude:
- lock files
- temp files
- obviously rebuildable scratch files

Be cautious with `session-corpus/` content. It may be derived from transcripts. Exclude it by default unless the user explicitly wants transcript-derived dreaming corpus artifacts included.

## Memory wiki vault

When `memory-wiki` is enabled, the wiki vault may contain restorable durable knowledge.

Prefer including:
- top-level wiki markdown pages
- `entities/`
- `concepts/`
- `syntheses/`
- `sources/`
- `reports/`
- `_attachments/` only when it clearly contains durable wiki content the pages depend on
- minimal plugin metadata needed to preserve the vault state

Usually exclude:
- `.openclaw-wiki/cache/`
- `.openclaw-wiki/locks/`
- log files under `.openclaw-wiki/`
- other generated cache artifacts that can be rebuilt

If unsure whether a metadata file is rebuildable, prefer excluding it and note the omission.

## Active memory

Active memory is an interaction feature, not automatically a durable file set.

Only include active-memory artifacts when config and disk inspection show durable files or directories clearly owned by the memory feature and relevant to memory restoration.

Do not guess hidden paths.

## Extra indexed paths

If `agents.defaults.memorySearch.extraPaths` or similar config points to additional directories, include them only when all of these are true:
- they are clearly durable memory content
- they are not chats/logs/secrets
- the user wants them included or they are obviously part of the default memory layer

When ambiguous, ask.

## Exclusion policy

Exclude by default:
- session transcripts
- chat exports
- log files
- event streams
- caches and indexes
- lock files
- credentials or secrets
- unrelated project files
