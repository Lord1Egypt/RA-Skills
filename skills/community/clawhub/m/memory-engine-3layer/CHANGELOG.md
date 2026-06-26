# Changelog

## v6.0.0 (2026-04-17)
- **NEW**: MEMORY.md capacity management — 5000 char soft cap with usage% tracking, warns at 80%, blocks writes at 100%
- **NEW**: USER.md auto-update — `--user "preference"` writes to USER.md with 1500 char cap
- **NEW**: Auto-snapshot before compaction/GC — stored in `memory/snapshots/`, keeps last 10
- **NEW**: MEMORY.md integrity monitoring — cron detects accidental wipe (<100 bytes) and auto-restores from latest snapshot
- **NEW**: Periodic snapshots every 6h via cron
- **NEW**: `--consolidate` command — analyze and deduplicate MEMORY.md entries with snapshot safety
- **NEW**: `--snapshot` command — manual MEMORY.md snapshot
- **NEW**: Boot shows capacity% (`📊 MEMORY XX%`)
- **NEW**: Health check includes capacity info for both MEMORY.md and USER.md + snapshot count
- **NEW**: Gap alerting in cron (>2 consecutive days missing)
- **IMPROVE**: GC now snapshots before applying destructive changes
- **IMPROVE**: Health score includes capacity-based warnings at 80%/90% thresholds
- **INSPIRED BY**: Hermes Agent bounded memory design + OpenClaw Dreaming separation

## v5.0.0 (2026-04-12)
- **MAJOR**: Memory Guardian architecture — redefines role as complement to OpenClaw native memorySearch
- **NEW**: `memory-migrate.js` — lossless upgrade/rollback between FTS5 and native modes
- **NEW**: Auto-detect native memorySearch and adapt behavior (boot skips FTS5 when native active)
- **NEW**: `memory-watcher.sh` — real-time session reset detection (<30s), auto-started by cron
- **NEW**: `memory-auto-extract.js --active` — incremental extraction from live sessions (offset-based)
- **NEW**: `memory-resume.js` — zero-latency session recovery context
- **NEW**: `memory-maintain.js --gc` — detect and remove stale MEMORY.md entries (old versions, completed TODOs, duplicates)
- **IMPROVE**: Cron upgraded to 1h interval with watcher supervision
- **IMPROVE**: Session size warning (>4MB yellow, >8MB red)
- **IMPROVE**: memory-flush prompt hardened (no MEMORY.md writes, no exec during flush)

## v4.0.0 (2026-04-12)
- **NEW**: `memory-watcher.sh` — polls every 30s for session resets, extracts immediately
- **NEW**: `memory-auto-extract.js --active` — incremental extraction from active sessions
- **NEW**: `memory-resume.js` — auto-detects unextracted reset sessions
- **IMPROVE**: Cron ensures watcher is always running
- **IMPROVE**: Extended extraction patterns: git commits, file writes, deployments, bug fixes

## v3.0.0 (2026-04-10)
- **NEW**: `--last N` mode — retrieve recent entries without search query
- **NEW**: `--tag` filter for last-N queries
- **NEW**: `--today` flag for today-only queries
- **NEW**: `memory-maintain.js --gc` — MEMORY.md garbage collection
- **IMPROVE**: Published to ClawHub and GitHub

## v2.9.0 (2026-04-09)
- **OPTIMIZE**: Boot smart truncation — 1500 chars default, prevents token explosion
- **OPTIMIZE**: Search keyword-context extraction for better snippets

## v2.8.0 (2026-04-09)
- **NEW**: `memory-backup.sh` — auto-backup to GitHub (every 6h via cron)
- **NEW**: `memory-restore.sh` — one-command disaster recovery

## v2.7.0 (2026-04-09)
- **FIX**: Unified timezone resolution — reads from openclaw.json, matches memory-flush dates
- **NEW**: `_timezone.js` shared module

## v2.6.0 (2026-04-09)
- **FIX**: Corrupted database auto-recovery
- **FIX**: Date-only queries now return correct results

## v2.5.0 (2026-04-09)
- **NEW**: `memory-boot.js` — single-command session startup
- **FIX**: memory-flush prompt restrictions

## v2.0.0 (2026-04-09)
- **Initial release**: Three-layer anti-amnesia architecture
- SQLite FTS5 + BM25 + CJK bigram search + temporal decay
