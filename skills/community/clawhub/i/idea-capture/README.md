# idea-capture

A lightweight OpenClaw skill for turning project discussions into durable idea records.

## What it does

`idea-capture` helps maintain a small idea archive inside your workspace. It can:

- create a new idea record
- update an existing idea
- append an update log entry
- write a session summary for later retrieval
- keep a simple human index and machine catalog in sync

## Storage model

The skill writes to a workspace-local idea system:

- `ideas/<idea-id>.md` — main idea doc
- `ideas/summaries/<idea-id>/<timestamp>.md` — session summaries
- `ideas/INDEX.md` — human-readable index
- `ideas/catalog.json` — machine-readable catalog

## Intended use

Use this when you want ideas to survive across sessions, branches, or future refinements.

Typical cases:

- capture a brand new project idea
- continue discussing an existing project and append updates
- preserve a concise session summary so later sessions can recover context quickly

## Modes

- `create` — always create a new idea
- `update` — require an existing matching idea
- `auto` — prefer `idea_id`, then title/slug matching, otherwise create

## Example

```bash
python3 skills/idea-capture/scripts/idea_capture.py \
  --title "Desktop Pet OpenClaw" \
  --summary "Turn OpenClaw into a desktop pet assistant" \
  --notes "Need create/update/session-summary support." \
  --tags ai,desktop,agent \
  --mode auto \
  --source qqbot
```

## Why this exists

OpenClaw conversations are great for ideation, but ideas can scatter across sessions. This skill creates a lightweight archive that is easy to read now and still flexible enough to evolve later toward richer indexing or a database-backed system.
