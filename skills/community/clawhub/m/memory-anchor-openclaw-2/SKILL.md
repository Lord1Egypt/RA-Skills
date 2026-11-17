---
name: memory-anchor
description: >
  Long-term memory for OpenClaw agents — SQLite hybrid recall (FTS5 + keyword +
  associative expansion + optional LLM embeddings), raw/curated anchors, session
  briefings, and an explicit INDEX/REINDEX pipeline. Use when the user wants
  durable memory across sessions, Persistent Sage-style recall, or to remember/
  search facts, preferences, and past conversations.
version: 1.0.0
tags:
  - memory
  - sqlite
  - embeddings
  - fts5
  - long-term-memory
  - openclaw
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env:
        - OLLAMA_HOST
        - MEMORY_ANCHOR_DB
        - MEMORY_ANCHOR_EMBED_PROVIDER
        - MEMORY_ANCHOR_EMBED_MODEL
        - OPENAI_API_KEY
---

# Memory Anchor

Portable long-term memory used in Persistent Sage (originally Project Nova),
Snowball, and Linux Ultra. Agents store durable facts as **anchors**, then
recall them with hybrid search.

## Who runs what (important)

**End users do not run `remember` / `recall`.** They just chat normally
(“I have three cats”, “what pets do I have?”).

**You (the OpenClaw agent)** call those CLI commands behind the scenes — same
role as Persistent Sage’s `memory_search` tool and background ingest. The user
should never need to know the commands exist.

| Actor | Job |
| --- | --- |
| **User** | Talks naturally |
| **Agent** | `recall` before answering from memory; `remember` / `ingest` when they state a durable fact; `index` after writes; `briefing` at session start |
| **setup** | One-time (or rare) bootstrap — agent can run this; power users may too |

## When to use (agent)

- User states a durable fact / preference → store with `remember` or `ingest`
- User asks about past preferences, facts, projects, or earlier chats → `recall` first
- Start of a session → `briefing` before answering from memory
- After storing facts → `index` so semantic recall stays warm

## Architecture (full Persistent Sage design)

| Layer | What it does |
| --- | --- |
| **Raw anchors** | Auto-captured snippets from user messages (heuristic split) |
| **Curated anchors** | `fact` / `insight` / `curated` with importance 1–5 |
| **FTS5** | Porter + unicode61 full-text, ranked with bm25 |
| **Keyword LIKE** | Exact / substring match with escaped wildcards |
| **Associative expansion** | Rule-based synonyms (e.g. vision → colorblind) |
| **Embeddings** | Optional cosine similarity over stored vectors |
| **INDEX / REINDEX** | Explicit embedding pipeline (no always-on app) |

Embedding BLOB layout matches Persistent Sage Rust:
`little-endian u32 dimension` + `dim × f32 LE`.

Each vector also stores `embedding_model` so recall never mixes dimensions
from different embed models. If you switch models, run `reindex`.

## Setup (Install → Start Using)

Requires Python 3 with SQLite FTS5 (standard CPython builds include it).

**First run — one command** (detects Ollama, optionally installs it, pulls
`nomic-embed-text`, smoke-tests embeddings):

```bash
python3 scripts/memory_anchor_cli.py setup --yes
```

After setup, the **user** just chats. You (the agent) call remember/recall
internally — do not ask the user to type those commands.

What `setup --yes` automates:

1. Find Ollama CLI / API (`OLLAMA_HOST`, default `http://127.0.0.1:11434`)
2. If missing: install via `winget` (Windows), `brew` (macOS), or official script (Linux)
3. Start the daemon when needed
4. Pull `nomic-embed-text` (tiny open-source embedder; Pi 5 friendly)
5. Smoke-test `/api/embed`

`index` also auto-pulls the model if Ollama is already running but the model
is missing — so many users never need a manual `ollama pull`.

Lexical hybrid (FTS5 + keyword) works even before setup finishes.

Optional env:

```bash
export MEMORY_ANCHOR_DB="$HOME/.memory-anchor/memory_anchor.sqlite"
export MEMORY_ANCHOR_EMBED_PROVIDER=ollama   # alias: local (default)
export MEMORY_ANCHOR_EMBED_MODEL=nomic-embed-text
export OLLAMA_HOST=http://127.0.0.1:11434
# Opt-in cloud (not default): MEMORY_ANCHOR_EMBED_PROVIDER=openai + OPENAI_API_KEY
```

CLI entrypoint (from this skill folder):

```bash
python3 scripts/memory_anchor_cli.py --help
```

## Agent workflow (behind the scenes)

User says things in natural language. You translate that into tool calls:

| User says (example) | You run (silently) |
| --- | --- |
| “Remember I prefer dark mode” / states a lasting fact | `remember "…" --type fact --index` |
| Any substantive user turn worth keeping | `ingest "…" --conversation …` |
| “What pets do I have?” / “am I colorblind?” | `recall "…"` **before** answering |
| New session | `briefing` to load context |
| (periodic / after writes) | `index` |

### 0. First session — bootstrap local embedder

```bash
python3 scripts/memory_anchor_cli.py setup --yes
```

If setup is not ready, lexical `recall` still works; tell the user what
`next_steps` reported (usually “install/start Ollama”) — still without
asking them to run remember/recall.

### 1. Store (agent-only)

```bash
python3 scripts/memory_anchor_cli.py remember "User is colorblind and prefers high-contrast UI" \
  --type fact --importance 4 --json --index
```

```bash
python3 scripts/memory_anchor_cli.py ingest "I have three cats and a dog named Pixel." \
  --conversation default --json
```

### 2. Retrieve (agent-only)

```bash
python3 scripts/memory_anchor_cli.py recall "any pets?"
python3 scripts/memory_anchor_cli.py recall "Do you know anything about my vision?"
```

Lexical hybrid works even with zero embeddings. With local Ollama
(`nomic-embed-text`), cosine similarity is added automatically.

### 3. Index / briefing / status (agent-only)

```bash
python3 scripts/memory_anchor_cli.py index --json
python3 scripts/memory_anchor_cli.py briefing --conversation default --label Companion
python3 scripts/memory_anchor_cli.py status
```

## Tool policy for agents

1. Never ask the user to run `remember`, `recall`, `ingest`, or `index`.
2. Prefer `recall` before guessing about the user's past facts or preferences.
3. Prefer `remember` / `ingest` when the user states a durable fact.
4. After a batch of writes (or periodically), run `index` so semantic recall
   stays aligned with the configured embed model.
5. Never invent memories that `recall` did not return.
6. Do not echo API keys or preference values that look like secrets.

## Environment

| Variable | Purpose |
| --- | --- |
| `MEMORY_ANCHOR_DB` | SQLite file path (or directory) |
| `MEMORY_ANCHOR_EMBED_PROVIDER` | Default `ollama` (`local` alias). Also `ollama_cloud`, `openai` |
| `MEMORY_ANCHOR_EMBED_MODEL` | Default `nomic-embed-text` |
| `OLLAMA_HOST` | Local Ollama base (default `http://127.0.0.1:11434`) |
| `OLLAMA_API_KEY` | Ollama Cloud bearer token |
| `OPENAI_API_KEY` | Only if you opt into OpenAI embeddings |
| `OPENAI_BASE_URL` | Custom OpenAI-compatible base |

## Design notes

See `references/DESIGN.md` for schema, scoring, and parity with Persistent Sage.
