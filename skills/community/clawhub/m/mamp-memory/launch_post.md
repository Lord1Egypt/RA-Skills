# MAMP: Mark AI Memory Protocol

**Every AI conversation starts from scratch. MAMP fixes that.**

MAMP is a lightweight, self-contained session memory protocol for AI agents — giving AI persistent, searchable memory using nothing but SQLite and the Python standard library.

## What Problem Does It Solve?

AI assistants forget. Every new conversation is a blank slate. MAMP solves this with:

- **Persistent sessions** — conversations survive restarts, context carries across sessions
- **Full-text search** — find any past topic across all conversations instantly (FTS5)
- **Cross-session recall** — ask "what did I say about finance last week?"
- **Priority tagging** — mark important memories, filter by importance
- **Zero dependencies** — stdlib + sqlite3 only, runs anywhere Python runs

## Why SQLite?

No external services. No vector DB. No API keys. No cloud lock-in. Just a `.db` file that works.

## Quick Start

```bash
git clone https://github.com/rokkiezeng/MAMP.git
cd MAMP
python3 demo.py
```

## The Core Idea

Memory should be **simple to query, reliable to store, and easy to extend**. MAMP treats memory as structured data — sessions, turns, tags, priorities — and gives you the primitives to build persistent, context-aware AI applications.

Built by [LeoTseng](https://github.com/rokkiezeng) | MIT-0 License
