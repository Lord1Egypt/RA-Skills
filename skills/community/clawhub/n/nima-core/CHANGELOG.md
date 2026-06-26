# Changelog

All notable changes to NIMA Core will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.1.0] - 2026-03-20

### Added
- **LadybugDB column migrations** (`init_ladybug.py`) — `MEMORYNODE_COLUMN_MIGRATIONS` list with idempotent `ALTER TABLE MemoryNode ADD IF NOT EXISTS` loop. Schema drift can no longer silently recur after install. Wired into `upgrade.sh` (Step 5) and `doctor.sh` (schema drift check).
- **`scripts/migrate_sqlite_to_ladybug.py`** — Idempotent one-shot SQLite → LadybugDB migration. Supports `--dry-run`, `--force`, `--verbose`. Batch size 100; skips by `id` (safe to re-run).
- **Canonical LLM env vars** (`nima_core/llm_config.py`) — `NIMA_LLM_PROVIDER`, `NIMA_LLM_API_KEY`, `NIMA_LLM_MODEL`, `NIMA_LLM_BASE_URL` as the single source of truth for all LLM config. Provider inferred from base URL when not set. Old provider-specific vars (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`) preserved as silent-only fallbacks.
- **Readiness thresholds for cron jobs** — Lucid moments and precognition are now silent no-ops until sufficient data exists. Configurable via CLI flags:
  - Lucid moments: `--min-total-memories` (default 25), `--min-candidate-count` (default 3)
  - Precognition: `--min-memory-count` (default 25), `--min-pattern-count` (default 2), `--min-pattern-confidence` (default 0.35), `--min-prediction-confidence` (default 0.6)
  - Precog actions: `MIN_PRECOG_COUNT` (default 1), `MIN_PRECOG_CONFIDENCE` (default 0.6)
- **`allowSubagentRecall`** feature in `nima-recall-live` — sub-agents can read NIMA memories when flag is set; writes are always blocked for sub-agents.
- **Updated `.env.example`** — fully documents all current env vars with inline defaults and grouped sections.

### Fixed
- `ProtocolNode` schema: `INTEGER` → `INT64` (Kùzu does not accept `INTEGER` type).
- `INSTALL.md`: venv path corrected from `~/.nima/.venv` → `~/.nima/venv`.
- `before_response_send` hook removed from `nima-affect` (hook does not exist in OpenClaw); tone hint injection moved to `before_agent_start` via `formatAffectContext()`.
- Shell quoting bug in safe `.env` parser — replaced `source`/`.` with `grep | cut` to prevent arbitrary shell execution.
- `python3 -m pip` used throughout scripts instead of bare `pip`.
- Bare `except` blocks replaced with specific exception types; `print()` debug calls replaced with proper `logging` calls.
- Ghost export, recall dict, connection leak, and composite index issues.
- N+1 queries in `hebbian_updater` — `executemany` UPSERT + batch `IN` query.

### Changed
- `NIMA_DB_BACKEND` is now the canonical backend selector (`sqlite` | `ladybug`). Legacy vars `NIMA_STORE` and `NIMA_LADYBUG_ENABLED=true` map via fallback chain.
- `upgrade.sh` — `init_ladybug.py` gated on `NIMA_DB_BACKEND=ladybug`; decoupled from `HAS_SQLITE` gate.
- `doctor.sh` — schema drift now increments `ISSUES` counter; `NIMA_STORE` refs replaced with `NIMA_DB_BACKEND`.
- `install.sh` — added `--sqlite` / `--ladybug` / `--no-interactive` flags + interactive LadybugDB prompt (skipped when stdin is not a TTY).
- All LLM-using modules refactored to use `resolve_llm_config()` from `nima_core/llm_config.py`: `llm_client.py`, `lucid_moments.py`, `precognition.py`, `memory_pruner.py`, `dream/*`, `darwinism.py`, `config.py`.

## [3.0.4] - 2026-02-23

### Fixed
- Darwinian memory — ghost verification LLM call stability under high load
- nima-query CLI — correct handling of empty result sets
- install.sh — idempotent directory creation on fresh installs
- Various README and documentation alignment fixes

### Changed
- Version bump: 3.0.0 → 3.0.4
- All versions in README and SKILL.md aligned to 3.0.4

## [3.0.0] - 2026-02-23

### Added
- **Darwinian Memory** (`nima_core/darwinism.py`) — Clusters similar memories via cosine similarity, marks duplicates as ghosts via LLM verification. Survival-of-the-fittest approach: semantically redundant memories fade out over time.
- **Installer** (`install.sh`) — One-command setup: LadybugDB, hooks, directories, embedder config.
- **OpenClaw hooks bundled** — All three hooks (`nima-memory`, `nima-recall-live`, `nima-affect`) ship with `index.js` entry points in `openclaw_hooks/`.
- **nima-query CLI** — Unified database query interface across SQLite and LadybugDB backends.

### Changed
- All cognitive modules unified under single package import surface.
- README rewritten with full architecture diagram and configuration reference.
- Version bump: 2.5.0 → 3.0.0 (major — signals stable cognitive stack)

## [2.5.0] - 2026-02-21

### Added
- **Hive Mind** (`nima_core/hive_mind.py`) — Multi-agent memory sharing via shared DB + optional Redis pub/sub. `build_agent_context()` aggregates memories across agents; `capture_agent_result()` stores agent outputs.
- **Precognition** (`nima_core/precognition.py`) — Temporal pattern mining → predictive memory pre-loading. Mines recurring patterns from episodic memory; generates predictions for upcoming contexts.
- **Lucid Moments** (`nima_core/lucid_moments.py`) — Spontaneous surfacing of emotionally-resonant memories. Safety features: trauma filtering, quiet hours, daily caps.

### Changed
- Version bump: 2.4.0 → 2.5.0

## [2.4.0] - 2026-02-20

### Added
- **Dream Consolidation** (`nima_core/dream_consolidation.py`) — Nightly synthesis engine. Extracts insights and patterns from episodic memory via LLM; writes structured dream logs to `~/.nima/dreams/`.

### Changed
- Version bump: 2.3.0 → 2.4.0

## [2.3.0] - 2026-02-19

### Added
- **Memory Pruner** (`nima_core/memory_pruner.py`) — Episodic distillation engine. Distills old conversation turns into semantic gists via LLM, suppresses raw noise in 30-day limbo. Configurable: `NIMA_DISTILL_MODEL`, `NIMA_DB_PATH`, `NIMA_DATA_DIR`, `NIMA_CAPTURE_CLI`. Pure stdlib (no `anthropic` package needed).
- **Logging** (`nima_core/logging_config.py`) — Singleton logger with file + console handlers. `NIMA_LOG_LEVEL` env var.
- **Metrics** (`nima_core/metrics.py`) — Thread-safe counters, timings, gauges. `Timer` context manager. Tagged metric support.
- **Connection Pool** (`nima_core/connection_pool.py`) — SQLite connection pool with WAL mode, max 5 connections, thread-safe.
- **Ollama embedding support** — `NIMA_EMBEDDER=ollama` with `NIMA_OLLAMA_MODEL` configuration.

### Fixed
- `__init__.py` — `__all__` NameError (used before definition)
- Memory pruner — Cypher injection prevention via layer whitelist
- Connection pool — Thread-safe `_waiters` counter, no double-decrement
- Logging — Correct log directory path (`NIMA_DATA_DIR/logs`, not parent)
- Metrics — Tagged metrics no longer overwrite each other in `get_summary()`

### Changed
- Version bump: 2.2.0 → 2.3.0
- Python requirement: 3.8+ (was 3.11+)
- All hardcoded paths replaced with env vars for portability

## [2.2.0] - 2026-02-19

### Added
- **VADER Affect Analyzer** — Contextual sentiment replacing lexicon-based detection
- **4-Phase Noise Remediation** — Empty validation → heartbeat filter → dedup → metrics
- **Resilient hook wrappers** — Auto-retry with exponential backoff and jitter
- **Ecology scoring** — Memory strength, decay, recency, surprise, dismissal in recall
- **Suppression registry** — File-based memory suppression with 30-day limbo

### Fixed
- Null contemplation layer crash
- Duplicate VADER/emotion lexicon keys
- Negation logic (proper 2-word window)
- Hardcoded venv paths → dynamic `os.homedir()`
- `--who` CLI filter (was a no-op)
- `maxRetries` clamped ≥ 1 in resilient wrapper
- Debug logging gated behind `NIMA_DEBUG_RECALL`
- Division by zero in cleanup script
- Ruff E701 lint issues

### Changed
- Recall token budget: 500 → 3000
- Shebang: hardcoded path → `#!/usr/bin/env python3`
- Turn IDs: full millisecond timestamps

## [2.1.0] - 2026-02-17

### Added
- Pre-release of VADER and noise remediation (shipped in v2.2.0)

## [2.0.3] - 2026-02-15

### Security
- Fixed path traversal vulnerability in affect_history.py (CRITICAL)
- Fixed temp file resource leaks in 3 files (HIGH)

### Fixed
- Corrected non-existent `json.JSONEncodeError` → `TypeError`/`ValueError`
- Improved exception handling — replaced 5 generic catches with specific types

### Improved
- Better error visibility and debugging throughout

## [2.0.1] - 2026-02-14

### Fixed
- Thread-safe singleton with double-checked locking

### Security
- Clarified metadata requirements (Node.js, env vars)
- Added security disclosure for API key usage

## [2.0.0] - 2026-02-13

### Added
- **LadybugDB backend** with HNSW vector search (18ms query time)
- **Native graph traversal** with Cypher queries
- **nima-query CLI** for unified database queries
- SQL/FTS5 injection prevention
- Path traversal protection
- Temp file cleanup
- API timeouts (Voyage 30s, LadybugDB 10s)
- 348 unit tests with full coverage

### Performance
- 3.4x faster text search (9ms vs 31ms)
- 44% smaller database (50MB vs 91MB)
- 6x smaller context tokens (~30 vs ~180)

### Fixed
- Thread-safe singleton initialization

## [1.2.1] - 2026-02-10

### Added
- 8 consciousness systems (Φ, Global Workspace, self-awareness)
- Sparse Block VSA memory
- ConsciousnessCore unified interface

## [1.2.0] - 2026-02-08

### Added
- 4 Layer-2 composite affect engines
- Async affective processing
- Voyage AI embedding support

## [1.1.9] - 2026-02-05

### Fixed
- nima-recall hook spawning new Python process every bootstrap
- Performance: ~50-250x faster hook recall

---

## Release Notes Format

Each release includes:
- **Added** — New features
- **Changed** — Changes to existing functionality
- **Deprecated** — Soon-to-be removed features
- **Removed** — Removed features
- **Fixed** — Bug fixes
- **Security** — Security improvements
