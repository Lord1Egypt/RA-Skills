---
name: mamp-memory
description: Mark AI Memory Protocol — persistent, searchable session memory for AI agents. SQLite-only, zero external dependencies.
author: LeoTseng
version: 1.2.1
license: MIT-0
security:
  credential_access: false  # Local SQLite only, no external services or credentials
  data_persistence: true   # Writes to a local .db file on disk
---

# MAMP — Mark AI Memory Protocol

Gives AI agents persistent, searchable memory using SQLite.

## When to Use

- User says "remember what I told you last time"
- Agent needs to recall facts across conversations
- User asks about past topics, preferences, or decisions
- Context window is filling up and older info needs to be summarized

## Core Concepts

- **Session** — a conversation, has an ID, survives restarts
- **Turn** — one message in a session (role: user/assistant)
- **Tag** — labels for a turn, e.g. ["finance", "important"]
- **Priority** — importance level: critical, normal, trivial

## Key Methods

```python
from importlib.util import spec_from_file_location, module_from_spec
spec = spec_from_file_location("mamp", "ai_memory_protocol_v1.2.0.py")
mod = module_from_spec(spec)
spec.loader.exec_module(mod)

# Manual mode — explicit add_turn() calls
sm = mod.SessionManager()
sm.start_conversation()
sm.add_turn("user", "I prefer dark mode")
sm.add_turn("assistant", "Noted")

# Auto mode (v1.1.8+) — auto-captures turns without manual add_turn()
sm = mod.SessionManager(auto_record=True)
sm.start_conversation()
# ... conversations are recorded automatically ...
sm.stop()  # flushes buffer and disables auto_record

# Heartbeat (v1.1.9+) — called externally every ~5 min via Hermes cron
# sm.heartbeat()  # flushes buffer + closes idle sessions (>30 min)

# Explicit db_path (recommended)
sm = mod.SessionManager(db_path="./memory.db", auto_record=True)

# Environment variable override:
# export MARK_MEMORY_DB=/path/to/memory.db
```

## What It Solves

AI forgets everything each conversation. MAMP makes memory persistent, searchable, and structured — without any external service, API key, or dependency beyond SQLite.

## Security Notes

**Default behavior — local directory only:**

- DB file written to `./mark_memory.db` in the current working directory
- No system directories are touched
- No log files, audit files, or hidden state files are written
- No network access, no external services

**Pass an explicit path to isolate data:**

```python
sm = mod.SessionManager(db_path="/your/specific/path/memory.db")
```

**Environment variable override:**

```bash
export MARK_MEMORY_DB=/your/specific/path/memory.db
```

This takes precedence over both the default and any `db_path` argument.

**Permissions awareness:**

- The DB file contains your conversation history in plaintext
- Ensure the directory has appropriate access controls
- If multiple agents run on the same host with the same path, they share memory — use different paths per agent to isolate

**No credentials stored:**

MAMP uses no API keys, tokens, or secrets. It is a pure local SQLite store.
