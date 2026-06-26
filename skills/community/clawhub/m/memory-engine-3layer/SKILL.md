---
name: memory-engine
description: "Memory guardian for OpenClaw — three-layer anti-amnesia with capacity management. v6.0: MEMORY.md soft cap (5000 chars) + USER.md cap (1500 chars) prevent prompt explosion. Auto-snapshot before compaction/GC. Integrity monitoring restores from snapshot if MEMORY.md is wiped. Works alongside OpenClaw native memorySearch (vector+hybrid) when available, falls back to built-in FTS5 when not. Focuses on what native lacks: auto-write, session extraction, watcher daemon, GC, health checks, backup, capacity management. Layer 1 (system): cron every 1h + watcher detects resets <30s + integrity checks. Layer 2 (platform): memory-flush + session-memory hook. Layer 3 (agent): write/search/maintain/boot scripts. Use when: recalling past conversations, writing memory entries, checking memory health, maintaining search index. Triggers: 'remember', 'recall', 'what did we discuss', 'memory status', 'search memory', 'reindex'."
---

# Memory Engine 🧠⚡

**Persistent memory that survives session restarts — with three layers of protection against amnesia.**

## The Problem

AI agents wake up blank every session. Existing solutions either:
- Need embedding APIs (cost money, need keys)
- Only search (useless if nothing was written)
- Rely on the AI "remembering" to save (it won't)

Memory Engine solves all three.

## v5.0 — Memory Guardian Architecture

**v5.0 redefines Memory Engine's role**: instead of a "full-stack memory system", it's now a **memory guardian** — handling everything OpenClaw native memory *doesn't* do.

| Feature | Native memorySearch | Memory Engine |
|---------|-------------------|---------------|
| Semantic vector search | ✅ (embedding API) | ❌ (deferred to native) |
| BM25 keyword search | ✅ (hybrid mode) | ✅ (FTS5 fallback) |
| Auto-write daily logs | ❌ | ✅ `memory-write.js` |
| Session reset detection | ❌ | ✅ `memory-watcher.sh` (<30s) |
| Active session extraction | ❌ | ✅ `--active` mode |
| Health check + GC | ❌ | ✅ `memory-maintain.js` |
| Session resume context | ❌ | ✅ `memory-resume.js` |
| GitHub backup/restore | ❌ | ✅ `memory-backup.sh` |
| Zero-dep writing | ❌ (needs embedding API) | ✅ (pure Node.js) |

### Upgrade from v3/v4 (zero data loss)
```bash
node scripts/memory-migrate.js              # preview changes
node scripts/memory-migrate.js --apply      # apply (backs up config first)
node scripts/memory-migrate.js --rollback --apply   # revert if needed
```

The migrate tool:
1. Enables native `memorySearch` with hybrid search + temporal decay
2. Enables `session-memory` hook (saves session on /new and /reset)
3. Updates cron to 1h if still at 6h
4. Preserves ALL existing data — your memory files, index, daily logs untouched
5. FTS5 search remains as fallback if native isn't configured

**No breaking changes**: all v3/v4 commands still work. `memory-search.js` auto-detects native mode and adapts. `memory-boot.js` skips FTS5 indexing when native is active (saves time).

## Three-Layer Anti-Amnesia Architecture

```
Layer 1: SYSTEM (runs without AI)     Layer 2: PLATFORM (OpenClaw built-in)
┌─────────────────────────┐           ┌──────────────────────────┐
│ cron job (every 1h)     │           │ memory-flush             │
│ • rebuild search index  │           │ • auto-triggers before   │
│ • health check          │           │   context compaction     │
│ • auto-create daily log │           │ • forces AI to write     │
│   if missing            │           │   memory/YYYY-MM-DD.md   │
│ • active session extract│           │ • user-invisible         │
│ • ensure watcher alive  │           │                          │
│                         │           │ ⚙️ Built into OpenClaw,  │
│ 🔴 watcher daemon       │           │   just needs config      │
│ • polls every 30s       │           └──────────────────────────┘
│ • detects session reset │
│ • extracts memory <30s  │
│ • auto-started by cron  │
│                         │
│ ⚙️ Pure shell/node,     │
│   no AI involvement     │
└─────────────────────────┘
Layer 3: AGENT (AI calls these)
┌──────────────────────────────────────────────────┐
│ memory-write.js    → append daily log / MEMORY.md│
│ memory-search.js   → FTS5 search (native fallback)│
│ memory-index.js    → build/update FTS5 index     │
│ memory-maintain.js → stats / rebuild / prune     │
│ memory-migrate.js  → upgrade/rollback helper  NEW│
│                                                  │
│ 📋 Governed by AGENTS.md rules:                  │
│   Session start → health check + read MEMORY.md  │
│   During conversation → log key events           │
│   Session end → summarize + promote to MEMORY.md │
└──────────────────────────────────────────────────┘
```

**Why three layers?** Any single layer can fail:
- AI forgets to write → cron + memory-flush still capture data
- Cron stops → AI + memory-flush still work
- Memory-flush doesn't trigger (short session) → AI + cron still work

All three failing simultaneously = near zero probability.

## Setup (2 minutes)

### Quick Setup (v5.0 — recommended for OpenClaw ≥ 2026.4)
```bash
# 1. Install cron (watcher + maintenance)
(crontab -l 2>/dev/null; echo "0 * * * * $(pwd)/scripts/memory-cron.sh") | crontab -

# 2. Auto-configure native search + hooks
node scripts/memory-migrate.js --apply

# 3. Restart gateway
openclaw gateway restart
```
That's it! Native memorySearch handles search, we handle everything else.

### Classic Setup (FTS5 mode — for OpenClaw < 2026.4 or no embedding API)
```bash
# 1. Install FTS5 dependency
npm install -g better-sqlite3

# 2. Install cron job
(crontab -l 2>/dev/null; echo "0 * * * * $(pwd)/scripts/memory-cron.sh") | crontab -
```

### Step 3: Enable memory-flush (add to openclaw.json)
```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "memoryFlush": {
          "enabled": true,
          "softThresholdTokens": 4000,
          "prompt": "Pre-compaction memory flush. Store durable memories in memory/YYYY-MM-DD.md (create memory/ if needed). APPEND only, do not overwrite. Include: key decisions, task outcomes, user preferences, project status changes. Format each entry as: - HH:MM [tag] description. If nothing worth storing, reply with NO_REPLY."
        },
        "reserveTokensFloor": 20000,
        "postIndexSync": "async"
      },
      "heartbeat": {
        "every": "30m"
      }
    }
  }
}
```

> **⚠️ Important**: Do NOT instruct memory-flush to write MEMORY.md or run exec commands.
> During flush, OpenClaw restricts writes to `memory/YYYY-MM-DD.md` only — MEMORY.md, SOUL.md, AGENTS.md are read-only.
> Exec/shell commands may also be restricted. The cron job handles index rebuilding independently.

### Step 4: Add rules to AGENTS.md
```markdown
## Session Startup (MANDATORY)
1. Run: node skills/memory-engine/scripts/memory-boot.js
   (single command: health check + index update + MEMORY.md content)
2. Use memory-search.js for specific recall (NOT full file reads)

## During Conversation (MANDATORY)
- Key decisions: node skills/memory-engine/scripts/memory-write.js --today "decision" --tag decision
- Task completion: node skills/memory-engine/scripts/memory-write.js --today "done" --tag done

## Session End (MANDATORY)
1. node skills/memory-engine/scripts/memory-write.js --today "Session summary"
2. node skills/memory-engine/scripts/memory-write.js --core "durable fact" --section category
3. node skills/memory-engine/scripts/memory-index.js
```

## Commands

### Migrate (upgrade/rollback) — NEW in v5.0
```bash
node scripts/memory-migrate.js              # preview: what would change
node scripts/memory-migrate.js --apply      # apply changes (backs up config)
node scripts/memory-migrate.js --rollback --apply   # revert to FTS5-only mode
node scripts/memory-migrate.js --status     # show current mode (JSON)
```
Enables native memorySearch, session-memory hook, optimal cron frequency.
Config backup created automatically before changes. Zero data loss guaranteed.

### Boot (session startup)
```bash
node scripts/memory-boot.js                     # health + index + MEMORY.md output
```
Replaces 3 separate calls (`--status` + `memory-index.js` + `read MEMORY.md`) with one command.
Auto-recovers from corrupted database. v5.0: auto-detects native mode, skips FTS5 when native active.

### Write (most important!)
```bash
# Daily log (auto-creates memory/YYYY-MM-DD.md)
node scripts/memory-write.js --today "Deployed v2.0 to production"
node scripts/memory-write.js --today "User prefers dark mode" --tag preference

# Long-term memory (appends to MEMORY.md, capacity-managed — 5000 char soft cap)
node scripts/memory-write.js --core "Stack: Next.js + PostgreSQL + Redis"
node scripts/memory-write.js --core "Deploy via Docker Compose" --section infrastructure

# User profile (appends to USER.md — 1500 char soft cap)
node scripts/memory-write.js --user "Prefers concise answers, dislikes verbose explanations"

# Snapshot MEMORY.md (before risky operations)
node scripts/memory-write.js --snapshot

# Health check (now includes capacity % for MEMORY.md and USER.md)
node scripts/memory-write.js --status
```

Health output:
```json
{
  "hasTodayLog": true,
  "hasCoreMemory": true,
  "coreMemory": { "chars": 2651, "cap": 5000, "usage": "53%" },
  "userProfile": { "chars": 380, "cap": 1500, "usage": "25%" },
  "snapshots": 3,
  "gapCount": 2,
  "healthScore": 71,
  "warnings": ["2 gaps in last 14 days"]
}
```

### Resume (zero-latency session recovery) — Enhanced in v4.0
```bash
node scripts/memory-resume.js                    # generate recovery summary (<2000 tokens)
node scripts/memory-resume.js --max-chars 1000   # shorter for tight budgets
```
Use in AGENTS.md as the first session startup step. Outputs:
- Last session's final topic & status
- Recent 3 days' key entries (priority-sorted by tag)
- Active MEMORY.md sections summary
- **NEW v4.0**: Auto-detects unextracted reset sessions and extracts them before resuming
  (eliminates the "resume misses recent work" gap)

### Search (0 tokens, ~300 token results)
```bash
node scripts/memory-search.js "deployment plan"          # top 3, 200 chars
node scripts/memory-search.js "API重构" --json --max 5   # CJK support
node scripts/memory-search.js "query" --max 1 --max-chars 100  # ultra-minimal

# Date filtering (auto-detects "4月2日" / "April 2" in queries)
node scripts/memory-search.js "4月2日完成了什么"          # auto date filter
node scripts/memory-search.js "tasks" --date 2026-04-02  # exact date
node scripts/memory-search.js "progress" --recent 7      # last 7 days
node scripts/memory-search.js "bugs" --after 2026-04-01 --before 2026-04-08

# Last N entries (no query needed, time-ordered) — NEW in v3.0
node scripts/memory-search.js --last 5                   # last 5 entries across all logs
node scripts/memory-search.js --last 10 --today          # today's last 10
node scripts/memory-search.js --last 3 --tag done        # last 3 [done] entries
node scripts/memory-search.js --last 5 --tag decision    # last 5 decisions
```

### Index
```bash
node scripts/memory-index.js          # incremental (skips unchanged)
node scripts/memory-index.js --force  # full rebuild
```

### Maintain
```bash
node scripts/memory-maintain.js              # show stats
node scripts/memory-maintain.js --reindex    # force rebuild
node scripts/memory-maintain.js --prune-days 90  # trim old entries

# GC: detect & remove stale MEMORY.md entries — NEW in v3.0
node scripts/memory-maintain.js --gc             # preview stale entries
node scripts/memory-maintain.js --gc --apply     # remove them
```
GC detects: old version references (>14d), completed TODOs, entries >60d old, duplicates.

### Consolidate (capacity management) — NEW in v6.0
```bash
node scripts/memory-maintain.js --consolidate          # analyze merge candidates
node scripts/memory-maintain.js --consolidate --apply  # remove duplicates (snapshots first)
```
When MEMORY.md exceeds 70% of the 5000-char soft cap, use this to find and merge duplicate entries.
Auto-snapshots MEMORY.md before any destructive operation.
For deeper consolidation (merging semantically similar entries), manually edit MEMORY.md.

### Auto-Extract (session transcript mining) — Enhanced in v4.0
```bash
node scripts/memory-auto-extract.js                # extract from active session (full scan)
node scripts/memory-auto-extract.js <path.jsonl>   # extract from specific file
node scripts/memory-auto-extract.js --scan          # scan all unprocessed reset sessions
node scripts/memory-auto-extract.js --active        # incremental extract from active sessions (NEW v4.0)
node scripts/memory-auto-extract.js --dry-run       # preview without writing
```
Extracts: git commits, file writes, deployments, PM2 restarts, user instructions,
test results, API responses, config changes, version releases, bug fixes (NEW v4.0).
`--active` mode reads only new bytes since last extraction (offset-based), safe for frequent runs.
Integrated into cron: auto-scans reset sessions + active sessions every 1h.

### Watcher (real-time session reset detection) — NEW in v4.0
```bash
bash scripts/memory-watcher.sh          # start daemon (polls every 30s)
bash scripts/memory-watcher.sh --once   # single check, no loop
```
- Detects new `.reset.` files within 30 seconds
- Immediately extracts memory + rebuilds index
- Auto-started by cron (ensures watcher is always running)
- PID managed via `.memory/watcher.pid`
- Solves the #1 failure mode: session reset → instant amnesia

### Compact (compress old logs)
```bash
node scripts/memory-compact.js --stats                  # show candidates
node scripts/memory-compact.js --older-than 30 --dry-run  # preview
node scripts/memory-compact.js --older-than 30          # execute (originals → memory/archive/)
```

Compaction extracts headings + key bullets (✅/🔴/重要), saves originals to `memory/archive/`. Typical savings: 60-70%.

## How Search Works

1. **Chunking**: ~300 chars per chunk, 60 char overlap, split at headings
2. **Indexing**: SQLite FTS5 full-text index + file metadata
3. **Search**: BM25 + phrase matching for English; TF-density bigram for CJK
4. **Date filtering**: Auto-detects dates in queries (4月2日, April 2, 2026-04-02)
5. **Ranking**: TF_density × coverage × core_boost(1.5×) × temporal_decay(30-day half-life)
5. **Output**: truncated snippets with `file#line` citations

## Token Budget

| Operation | Tokens |
|-----------|--------|
| Search (SQLite) | 0 |
| Results (3 × 200 chars) | ~300 |
| Read full daily file | ~2000 |
| Read 4 daily files | ~8000 |
| **Savings** | **~95%** |

## Backup & Disaster Recovery

### Auto-backup (recommended)
Memory-cron automatically pushes to GitHub every 6 hours (if git remote is configured):
```bash
# One-time setup:
cd ~/.openclaw/workspace
git init && git branch -M main
git remote add origin https://<token>@github.com/<user>/openclaw-workspace.git
bash skills/memory-engine/scripts/memory-backup.sh   # first push
# After this, cron handles it automatically every 6h
```

### Restore after reinstall
```bash
# After fresh OpenClaw install:
bash memory-restore.sh https://<token>@github.com/<user>/openclaw-workspace.git
# Restores: memories, config, skills, crontab, rebuilds search index
```

### What's backed up
- `MEMORY.md` + `memory/*.md` (all memories — irreplaceable)
- `SOUL.md`, `USER.md`, `IDENTITY.md` (personality)
- `AGENTS.md`, `TOOLS.md`, `HEARTBEAT.md` (behavior rules)
- `skills/` (all installed skills)
- `openclaw.json` → backup copy
- `crontab` → backup copy

### What's NOT backed up (rebuilt automatically)
- `.memory/index.sqlite` (rebuilt from md files by restore script)
- `.memory/cron.log` (transient)

## Requirements

### v5.0 Native mode (recommended)
- Node.js 18+
- OpenClaw ≥ 2026.4 (for native memorySearch + session-memory hook)
- `better-sqlite3` **optional** (only needed for FTS5 fallback)
- No API keys required (OpenClaw auto-detects embedding providers)

### Classic FTS5 mode
- Node.js 18+
- `better-sqlite3` (for search/index)
- Write + health check: zero dependencies
- No API keys, no cloud, no Docker
