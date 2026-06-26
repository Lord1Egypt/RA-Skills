# Memory Engine 🧠⚡

**Persistent memory for [OpenClaw](https://github.com/openclaw/openclaw) agents — with three layers of protection against amnesia and capacity-managed long-term memory.**

[![ClawHub](https://img.shields.io/badge/ClawHub-memory--engine--3layer-blue)](https://clawhub.com)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Version](https://img.shields.io/badge/version-6.0.0-orange)](https://github.com/ZackO2o/memory-engine/releases)

## The Problem

AI agents wake up blank every session. Existing solutions either:
- 💸 Need embedding APIs (cost money, need keys)
- 🔍 Only search (useless if nothing was written)
- 🧠 Rely on the AI "remembering" to save (it won't)
- 💥 Let memory grow unbounded until context explodes

**Memory Engine solves all four.**

## What's New in v6.0

- **Capacity Management** — MEMORY.md soft cap (5000 chars) + USER.md cap (1500 chars). Warns at 80%, blocks at 100%. No more context explosion from unbounded memory growth.
- **Auto-Snapshot** — MEMORY.md snapshots before compaction/GC + periodic every 6h. Keeps last 10.
- **Integrity Monitoring** — Cron detects accidental MEMORY.md wipe and auto-restores from snapshot.
- **Consolidation** — `--consolidate` command to deduplicate entries when approaching capacity.
- **User Profile** — `--user` flag to manage USER.md with capacity tracking.

## Three-Layer Anti-Amnesia Architecture

```
Layer 1: SYSTEM (no AI needed)         Layer 2: PLATFORM (OpenClaw built-in)
┌─────────────────────────┐           ┌──────────────────────────┐
│ cron job (every 1h)     │           │ memory-flush             │
│ • rebuild search index  │           │ • auto-triggers before   │
│ • health check          │           │   context compaction     │
│ • MEMORY.md integrity   │           │ • forces AI to write     │
│ • auto-snapshot (6h)    │           │   memory/YYYY-MM-DD.md   │
│ • session extraction    │           │                          │
│ • gap alerting          │           │ session-memory hook      │
│                         │           │ • saves on /new + /reset │
│ watcher daemon (30s)    │           └──────────────────────────┘
│ • detects session reset │
│ • extracts memory <30s  │
└─────────────────────────┘

Layer 3: AGENT (AI calls these)
┌──────────────────────────────────────────────────┐
│ memory-write.js    → daily log + MEMORY.md       │
│                      + USER.md (capacity-managed)│
│ memory-search.js   → FTS5/native hybrid search   │
│ memory-boot.js     → single-command startup      │
│ memory-resume.js   → session recovery context    │
│ memory-maintain.js → GC / consolidate / stats    │
│ memory-compact.js  → compress old logs           │
└──────────────────────────────────────────────────┘
```

## Capacity Management (v6.0)

| Store | Soft Cap | Typical Entries | Behavior at Limit |
|-------|----------|-----------------|-------------------|
| MEMORY.md | 5,000 chars | 30-50 entries | Blocks new writes, suggests consolidation |
| USER.md | 1,500 chars | 5-15 entries | Blocks new writes |

Boot shows live capacity: `📊 MEMORY 53%`

Health check warns at 80% and 90%.

## Quick Start

### Install via ClawHub
```bash
clawhub install memory-engine-3layer
```

### Or clone
```bash
git clone https://github.com/ZackO2o/memory-engine.git
cp -r memory-engine ~/.openclaw/workspace/skills/
```

### Setup
```bash
# Dependencies
npm install -g better-sqlite3

# Cron (Layer 1)
cd ~/.openclaw/workspace/skills/memory-engine
(crontab -l 2>/dev/null; echo "0 * * * * $(pwd)/scripts/memory-cron.sh") | crontab -

# Native search upgrade (recommended for OpenClaw ≥ 2026.4)
node scripts/memory-migrate.js --apply
```

### Enable memory-flush (Layer 2)
Add to `~/.openclaw/openclaw.json`:
```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "memoryFlush": { "enabled": true, "softThresholdTokens": 4000 }
      },
      "heartbeat": { "every": "30m" }
    }
  }
}
```

## Usage

```bash
# Daily log
node scripts/memory-write.js --today "Deployed v2.0" --tag done

# Long-term memory (capacity-managed)
node scripts/memory-write.js --core "Stack: Next.js + PostgreSQL" --section infrastructure

# User profile (capacity-managed)
node scripts/memory-write.js --user "Prefers concise answers"

# Snapshot
node scripts/memory-write.js --snapshot

# Health check (includes capacity %)
node scripts/memory-write.js --status

# Search
node scripts/memory-search.js "deployment plan"
node scripts/memory-search.js "API重构" --json --max 5
node scripts/memory-search.js --last 5 --tag done

# Boot (session startup)
node scripts/memory-boot.js

# GC + Consolidate
node scripts/memory-maintain.js --gc --apply
node scripts/memory-maintain.js --consolidate --apply
```

## Token Budget

| Operation | Tokens |
|-----------|--------|
| Search (SQLite, local) | **0** |
| Results (3 snippets) | **~300** |
| Read full daily file | ~2,000 |
| **Savings vs raw files** | **~95%** |

## Requirements

- Node.js 18+
- `better-sqlite3` (for search/index)
- OpenClaw (any version; ≥ 2026.4 recommended for native search)
- No API keys, no cloud, no Docker

## Links

- [Full documentation (SKILL.md)](SKILL.md)
- [Changelog](CHANGELOG.md)
- [ClawHub](https://clawhub.com)
- [OpenClaw](https://github.com/openclaw/openclaw)

## License

MIT
