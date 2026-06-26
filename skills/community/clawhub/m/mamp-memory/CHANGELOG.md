# MAMP Changelog

## v1.2.1 (current)

### Security Fixes (to clear clawhub warnings)

- **DEFAULT_DB_PATH reverted to cwd-only** — `./mark_memory.db` in current working directory, matching SKILL.md "local-only" description. No more platform-aware system paths.
- **MARK_MEMORY_DB env var still respected** — users can override with `export MARK_MEMORY_DB=/your/path.db`
- **platform_info persistence removed** — `_PLATFORM_INFO` (hostname, python_executable, arch, container) is no longer written to the SQLite DB
- **LOCK/LOG/AUDIT paths changed to relative** — `./session_gc.lock`, `./session_gc.log`, `./session_gc_audit.log`
- **DB_VERSION 15 → 16** (migration 15 reversed; platform_info table no longer created)

## v1.1.5

### New Features

- **priority_levels persisted to DB** — add_priority_level() and remove_priority_level() survive restarts
- **merge_sessions duplicate O(n log n)** — bisect optimization, conflicts resolved without losing either turn
- **vacuum() enhanced** — batch_size, compress_level (default 6, was 1), max_memory_mb parameters
- **FTS rebuild thread lock** — concurrent rebuilds blocked, no race conditions
- **search_batch daemon threads** — clean shutdown, no zombie threads
- **busy_timeout=5000** — all write connections, prevents lock contention

### Bug Fixes

- **search() FTS path — mixed tags type** — r.get("tags") returns list from FTS, string from DB rows. Added dual-type detection.
- **_fts_lock undefined** — threading import was at line 1726, lock used at line 377. Fixed with lazy init.
- **SessionManager.search_count — tag_filter list→string** — normalized at wrapper layer for caller convenience.

---

## v1.1.4

- merge_sessions() 'duplicate' conflict strategy
- vacuum() squash_spaces option
- SessionManager.search_count() exposed
- SessionManager.get_session_extended() exposed
- WAL mode on all connections

## v1.1.3

- _fts_search() zero-result corruption detection fixed
- get_all_sessions() alias added
- is_stale() threshold calculation fixed

## v1.1.2

- _rebuild_fts() uses DROP+RECREATE instead of DELETE
- _fts_search() detects empty FTS vs corrupted
- get_session(max_turns=N) cursor isolation fixed
- get_session_extended() returns full turns list
- truncation flags exposed at top level

## v1.1.1

- get_session(max_turns=N) — head+tail loading for large sessions
- search_count() — fast count-only search
- get_session_extended() — full session with stats

## v1.1.0

- FTS5 full-text search (10-100x faster than LIKE)
- Pagination (offset support)
- search_with_snippets()
- Jaccard similarity in find_duplicates()
- FTS auto-rebuild after bulk operations
