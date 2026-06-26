---
name: openmem
description: "SQLite long-term memory compression system for extended memory life. Adds tools for agents to control their memory functions."
metadata:
  {
    "openclaw": {
      "emoji": "🧠",
      "requires": { "bins": ["python3"] },
      "optionalEnv": [
        "OPENMEM_DB",
        "OPENMEM_SESSIONS_DIR",
        "OPENMEM_BOOTSTRAP_LIMIT",
        "OPENMEM_COMPRESS_INACTIVITY"
      ],
      "reads": [
        "~/.openclaw/agents/main/sessions/*.jsonl"
      ],
      "writes": [
        "~/.openclaw/workspace/memory/openmem.db",
        "~/.openclaw/workspace/memory/openmem-cache.json",
        "~/.openclaw/workspace/memory/auto_compress_state.json",
        "~/.openclaw/logs/openmem-compress.log"
      ],
      "credentialAccess": "none — compression uses `openclaw capability model run` which handles provider auth internally"
    }
  }
---

# OpenMem v1.3.0

SQLite-backed long-term memory.

MIT License — free to use, modify, redistribute. No attribution required.

## Privacy & Scope

**Read this before installing.**

- **Full session transcripts are read during compression.** Both manual (`compress.py read`) and automated (`auto_compress.py`) compression read the complete raw JSONL session files. The full content is passed to the extractor — everything in that session is visible. Only 3–10 selected items are written to the DB; the raw content is never stored permanently. This is intentional but privacy-sensitive: sessions may contain passwords, keys, or personal data entered during a conversation.

- **Automated compression destroys original session files.** `auto_compress.py` replaces session JSONL files older than 24h with a one-line stub after memories are confirmed. This is irreversible. Run with `--no-wipe` to disable this behaviour, or skip auto-compression entirely.

- **Network calls are made during auto-compression.** `auto_compress.py` calls `openclaw capability model run` to extract memories using the user's configured model. OpenClaw handles all provider routing and auth — session excerpts are passed as a prompt through the local gateway. The MCP server itself makes no network calls.

- **Cache file is plaintext.** After every memory write, top memories are written to `openmem-cache.json` in the same directory as the DB, unencrypted. Trust level is identical to the DB file.

- **Persistent presence.** `setup.py` registers an MCP server and an hourly cron job with your OpenClaw gateway. OpenMem has ongoing read access to session files and write access to the local DB while enabled. Run `uninstall.py` to remove all registered components.

## Filesystem & Credential Access

What this skill reads and writes — declared up-front.

**Reads:**
- `~/.openclaw/agents/main/sessions/*.jsonl` — session transcripts, read in full during compression (see Privacy above).

**Writes:**
- `~/.openclaw/workspace/memory/openmem.db` — SQLite memory database
- `~/.openclaw/workspace/memory/openmem-cache.json` — plaintext top-memory cache, written after every memory write
- `~/.openclaw/workspace/memory/auto_compress_state.json` — last-run state for the daily guard
- `~/.openclaw/logs/openmem-compress.log` — compression log

All paths are overridable via env vars (see Environment Variables).

## MCP Tool Calls

When the OpenMem MCP server is registered, use these native tool calls directly:

| Tool | Purpose |
|---|---|
| `memory_add` | Store a new memory (content, category, importance, source) |
| `memory_search` | FTS search with relevance + importance + recency ranking |
| `memory_update` | Change content, category, or importance by ID |
| `memory_delete` | Remove a memory by ID |
| `memory_list` | List memories sorted by importance / recency / access |
| `memory_stats` | Total count, breakdown by category, date range |

## Installation

After `openclaw skills install openmem`, run setup once:

```bash
python3 ~/.openclaw/workspace/skills/openmem/scripts/setup.py
```

This creates the database, checks requirements, registers the MCP server, registers the auto-compression launchd job (macOS), and prints the next steps (hook enable).

## Uninstall

Removes the cron job, MCP server, and bootstrap hook. **Your database is not deleted** — its path is printed so you can export or remove it yourself.

```bash
python3 ~/.openclaw/workspace/skills/openmem/scripts/uninstall.py
```

## CLI Quick Reference

```bash
SCRIPTS=~/.openclaw/workspace/skills/openmem/scripts

# Add a memory
python3 $SCRIPTS/mem.py add "User prefers concise responses" --category preference

# Search
python3 $SCRIPTS/mem.py search "response style"

# List top memories
python3 $SCRIPTS/mem.py list --limit 20

# Stats
python3 $SCRIPTS/mem.py stats

# --- Session compression ---
# List uncompressed sessions
python3 $SCRIPTS/compress.py pending

# Read a session (then you summarize it into mem.py add calls)
python3 $SCRIPTS/compress.py read <session-id>

# Mark compressed after adding memories
python3 $SCRIPTS/compress.py mark-done <session-id> --memory-count 5
```

## Categories

`fact` · `insight` · `preference` · `correction` · `event` · `general`

## Compression Workflow

### Automatic (default)

After setup, an OpenClaw cron job runs `auto_compress.py` every hour (via `--tools exec`, so it can only run the script — no loops possible). The script itself handles all guards:
1. Checks it hasn't already run today
2. Checks the agent has been inactive for 2+ hours
3. Finds all uncompressed sessions (skipping the most recently active one)
4. Calls Ollama to extract 3–8 memories per session (falls back to heuristics if Ollama is unavailable)
5. Deduplicates each candidate against existing memories (word-overlap check)
6. Inserts and **confirms** each memory is in the DB before proceeding
7. Wipes sessions older than 24h to a stub after memories are confirmed
8. Logs everything to `~/.openclaw/logs/openmem-compress.log`

To run it manually:
```bash
python3 $SCRIPTS/auto_compress.py --force          # skip guards, compress now
python3 $SCRIPTS/auto_compress.py --dry-run        # preview without writing
python3 $SCRIPTS/auto_compress.py --no-wipe        # compress but keep session files
```

### On-demand (agent)

You can also trigger compression by saying:
- *"compress my sessions"*
- *"save this to long-term memory"*

**Step by step:**

1. `python3 $SCRIPTS/compress.py pending` — find sessions not yet compressed
2. `python3 $SCRIPTS/compress.py read <id>` — read the conversation
3. Extract 3–10 key facts, corrections, preferences, and insights
4. Use `memory_add` tool call (or `mem.py add`) for each memory
5. `python3 $SCRIPTS/compress.py mark-done <id> --memory-count <N>`

**What to extract:**
- Facts the user stated about their system, preferences, or projects
- Mistakes made and the correct approach
- Decisions reached and why
- Important events (deploys, incidents, milestones)

**What to skip:** Raw command output, transient errors, small talk.

### Deduplication

`memory_add` automatically checks for similar existing memories before inserting (word-overlap similarity ≥ 65%). If a near-duplicate is found, it returns the existing memory ID instead of inserting. Pass `"check_duplicate": false` to force an insert.

## Importance Guide

| Score | Meaning |
|---|---|
| 0.9–1.0 | Critical — always surface (key preferences, major corrections) |
| 0.7–0.8 | Important — surface often |
| 0.5–0.6 | Normal (default) |
| 0.3–0.4 | Low — background context |
| 0.0–0.2 | Archive only |

## OpenAuto Integration

If [OpenAuto](https://clawhub.ai/halthelobster/openauto) is installed alongside OpenMem, the two work together:

- **OpenAuto defers long-term writes to OpenMem** — when `memory_add` is available, OpenAuto uses it instead of writing directly to `MEMORY.md`
- **OpenMem replaces `MEMORY.md` searches** — `memory_search` handles ranked FTS lookup so OpenAuto doesn't need to grep flat files
- **Session compression feeds OpenMem** — OpenAuto's Working Buffer and daily notes are the source material; saying "compress my sessions" extracts durable memories into OpenMem
- **Bootstrap injection bridges both** — OpenMem injects top memories as `OPENMEM.md` at session start, which OpenAuto reads alongside its own workspace files

Both skills work independently. If both are installed and OpenMem's MCP server is registered, the integration activates automatically — no extra setup required.

## Bootstrap Hook

The bootstrap hook auto-injects your top memories at session start.

Enable once:
```bash
openclaw hooks enable openmem
```

Memories appear in `OPENMEM.md` at the start of every session.
Control injection count with `OPENMEM_BOOTSTRAP_LIMIT` (default: 12).

## Database Schema

See [references/schema.md](references/schema.md) for full schema details.

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `OPENMEM_DB` | `~/.openclaw/workspace/memory/openmem.db` | Database path |
| `OPENMEM_BOOTSTRAP_LIMIT` | `12` | Memories injected at bootstrap |
| `OPENMEM_SESSIONS_DIR` | `~/.openclaw/agents/main/sessions` | Session files location |
| `OPENMEM_COMPRESS_INACTIVITY` | `2` | Minimum inactivity hours before auto-compress runs |
