# Changelog

## 3.0.0 (2026-07-14)

### Breaking
- **Enforceable Skill Rules** — Skills can now define `enforce:` rules with `priority: critical`. Rules appear as structured directives above memory in every turn. Agents must follow them.
- **Loader ready** — `scripts/enforce_loader.py` parses SKILL.md frontmatter and outputs injectable YOU-MUST directives.
- **Kaskadierung** — Child skills inherit enforce rules from parent skills. Loader scans all loaded skills.

### Added
- **scripts/enforce_loader.py** — CLI tool to extract enforce rules from any installed skill
- **README enforce notice** — v3.0.0 führt enforce-Regeln ein. Alte Memory-Regeln entfernt. Enforce ist jetzt die Governance-Schicht.

### Fixed
- **Galaxy "loading" fix** — scope mapping now correctly matches unscoped items (`__unscoped__`), all items loaded (up to 20000), deadlock protection via lock_timeout
- **Favicon 401** — `/favicon.ico`, `/favicon.svg`, `/site.webmanifest` served at root, bypass auth
- **Unscoped in MV** — materialized view now includes empty/NULL scope_ids directly

## 2.9.0 (2026-07-13)

### Added
- **Unscoped galaxy tenant** — memories without scope_id now show as 📂 Unscoped tenant
- **Fire-and-forget update** — dashboard update no longer hangs (response completes before container restart)
- **Shared Brain documentation** — README + SKILL.md document Hermes+OpenClaw shared memory
- **OPENCLAW_SCOPE_PREFIX** — env var for separate OpenClaw scope tagging
- **Pre-rebuild backup + docker prune** — start scripts now run backup + cleanup before rebuild

### Fixed
- **Galaxy unscoped display on Linux** — all 3800+ memories now visible as planets
- **Galaxy tags column** — query now uses subquery from tags table (was crashing silently)

## 2.7.0 (2026-07-13)

### Added
- **Memory Galaxy real content** — hover shows actual stored text, importance, tags, date
- **Memory Galaxy all nodes** — up to 40 planets per scope, enriched with real data
- **Playwright dashboard test** — CI verifies dashboard renders without errors
- **BOM-safe .env writing** — setup.ps1 no longer writes UTF-8 BOM

### Fixed
- **Galaxy query timeout** — uses PK index (`id > MAX(id)-250`) instead of `ORDER BY created_at`
- **Non-existent `tags` column** — galaxy items query now uses subquery from `tags` table
- **Dashboard raw CSS** — fixed broken `</style>` tag that rendered CSS as text
- **`API_URL` warning** — silenced with empty default in docker-compose
- **PgBouncer `:latest` pin** — pinned by SHA256 digest (no version tags available)

### Changed
- **Type hints** added to auth, db, update, embedding_queue, scoring modules
- **Shared route helpers** extracted to `routes/_shared.py`
- **Docker builds** — `.dockerignore` reduces image size by ~237MB

## 2.5.1 (2026-07-13)

### Added
- **Multi-Replica API** — Redis + Caddy load balancer, 2 API instances (api1/api2)
- **PgBouncer custom Dockerfile** — edoburu/pgbouncer with password via build arg, port 5432
- **Materialized Views** — `pages_stats_mv` + `pages_scope_stats_mv` for dashboard (ms instead of COUNT*)
- **PITR Backup** — WAL archiving (wal_level=replica, archive_mode=on, pgwal volume)
- **Async Embedding Queue** — capture returns instantly, batch worker processes in background
- **HNSW Index Tuning** — m=16→32, ef_construction=400, ef_search×2 for 2M vectors
- **k6 Load Testing** — `tests/loadtest.js` (200 concurrent users, health/search/capture)

### Changed
- **Container naming** — `gbrain-*` → `hc-sidecar-*` (consistent with repo name)
- **API port** — internal 8100, Caddy on 8010 external
- **Dashboard** — COUNT(*) queries replaced by materialized views
- **Optimizer** — refreshes MV + auto-tier + dedup every cycle
- **macOS Setup** — Colima as primary Docker fallback

## 2.5.0 (2026-07-13)

## 2.4.0 (2026-07-13)

### Added
- **Data-loss prevention** — pgvector pinned to `pgvector/pgvector:0.8.0-pg17` (nicht `:latest`), verhindert DB Volume Re-Init bei Auto-Updates
- **Auto-Recovery** — bei `pages < 100` wird Hermes state.db automatisch im Hintergrund importiert
- **DB Backup** — `migrations/backup_db.sh`: täglicher pg_dump mit 14 Tagen Retention
- **15 Data-Loss Tests** — statische Analyse: pgvector-Pin, keine DROP TABLE pages, EMBEDDING_DIM portability, Recovery-Block in main.py
- **CI Gated Pipeline** — 3 Jobs (lint→test→docker) ohne `continue-on-error`, Integration-Tests mit Docker Healthcheck
- **Branch Protection** — main erfordert PR + 1 Review + CI-Checks
- **Pre-push Hook** — `.githooks/pre-push` läuft vor jedem Push auf main

### Fixed
- **EMBEDDING_DIM** portabel gemacht (`${EMBEDDING_DIM}` statt hardcodiertem 1536 → funktioniert wieder mit Ollama)
- **PGUSER/PGDATA** gesetzt → verhindert PostgreSQL Re-Init bei Container-Restart
- **ALLOW_EMBEDDING_SCHEMA_RESET** nur auf embeddings-Tabelle (nicht pages)

## 2.3.0 (2026-07-12)

### Added
- **Bi-temporal endpoints** — `/why/{id}` shows supersession chain + version history; `/timeline` shows all memory changes over time
- **Memory Galaxy v3** — search bar, memory type dropdown, confidence filter in the Galaxy overlay with real-time node filtering
- **MCP auto-discovery** — `mcp.json` manifest for Claude Desktop, VS Code, Cursor; 20 MCP tools total
- **GitHub Actions CI** — 3-job pipeline: lint (syntax+flake8+mypy), test (pytest+coverage), docker build
- **Expanded MCP tools** — `why_memory`, `bi_timeline` MCP tools for bi-temporal queries

### Changed
- AGENTS.md updated to v0.2.0 spec (32 lines, compact API table)
- llms.txt updated with all new features
- GitHub topics: +fastapi, +docker, +knowledge-graph, +ollama, +chat-memory, +semantic-search (19 total)

## 2.2.0 (2026-07-12)

### Added
- **DB backup prevention** — `content_hash` column for idempotent re-imports
- **Migration recovery** — `migrations/import_from_hermes_db.py` restores from Hermes state.db
- **content_hash** — SHA-256 per memory, auto-set on capture, index for fast dedup
- **Migration SQL** — `001_migrate_old_memories.sql` with full schema + indexes

### Changed
- Schema: `content_hash TEXT` + `idx_pages_content_hash` created on every API start
- Memory loss on DB reset is recoverable: run migration script, re-imports idempotently

## 2.1.0 (2026-07-12)

### Added
- **Ebbinghaus forgetting-curve decay** — `R=e^(-t/S)`, stability grows per spacing effect
- **Deterministic Conflict Resolver** — ADD/NOOP/INVALIDATE via token Jaccard + embedding cosine
- **Bi-temporal validity** — `valid_to`/`superseded_by`, superseded facts keep history
- **Interaction-aware reinforcement** — capture=1.0, retrieve=0.15, nudge=0.10
- **7-term hybrid score** — vector + lexical + retention + importance + recency + frequency - staleness
- **10K-scale PG tuning** — shared_buffers=1GB, work_mem=64MB, random_page_cost=1.1
- **Dynamic HNSW ef_search** — per query type (hybrid=80, vector=40, high_recall=400)
- **Dashboard keyset pagination** — cursor-based statt OFFSET
- **`/ask` Q&A endpoint** — natural language → vector + GraphRAG → LLM synthesis
- **`/export` endpoint** — JSON/Markdown backup with graph entities

### Changed
- Optimizer: Ebbinghaus decay archive at retention<0.05 statt flat confidence*0.995
- Search: SQL CTE hybrid score (kein Python merge/sort), 7-term weights
- Capture pipeline: Conflict Resolver ersetzt simple find_similar_page

## 1.6.0 (2026-07-11)

### Added
- **Dashboard UI integrations** — Tier badges (Hot/Warm/Cold), memory type filter, days back filter, Knowledge Graph link, Nudge link
- **Interactive buttons** — 👍/👎 feedback on each memory, ✏️ inline editor modal, 🔗 merge with checkboxes
- **Merge, Editor, Feedback, Nudge** — all new backend features now accessible from the Dashboard UI

## 2.0.0 (2026-07-11)

### Added
- **Knowledge Graph** — entities + relationships + entity_mentions tables, rule-based entity extraction, depth-traversal graph queries (`/graph/*` endpoints)
- **Memory Tiers** — Hot/Warm/Standard/Cold auto-assignment based on importance, recency, confidence
- **Memory Versioning** — `memory_versions` table tracks every change with reason
- **Memory Compression** — intelligent multi-line compression (keep first 40%, last 20%, compress middle)
- **Memory Consolidation** — embedding-similarity clustering groups related memories into summarized parents
- **Memory Merge** — `/memory/merge` endpoint merges multiple memories, reparents sources
- **Memory Editor** — `/memory/update/{id}` inline content + type editing
- **Memory Feedback** — `/feedback/{id}?helpful=true/false` adjusts importance + confidence
- **Memory Nudge** — `/nudge` returns top important recent facts (inspired by Hermes Built-In nudges)
- **Temporal Search** — `?days_back=N` filter on `GET /search`
- **Self-wiring Graph** — 15 relation patterns (built/leads/part_of/implements/located_at/communicates/preceded_by + original 6)
- **pgvector HNSW Index** — automatic HNSW index creation (falls back to IVFFlat)
- **Auto-Sync Daemon** — background thread imports new Hermes sessions every 5 minutes

### Changed
- Capture pipeline now extracts entities + relationships + compressed version on every `POST /capture`
- Optimizer loop runs tier assignment + consolidation every cycle
- Dashboard auto-refresh uses JS setTimeout (galaxy stays open)
- README comparison table expanded to 6 systems (Cognee, LangMem, Supermemory, gBrain, Mem0)

## 1.5.0 (2026-07-11)

### Added
- CONTRIBUTING.md with PR review structure, linting, commit conventions, merge strategy
- PR template (.github/PULL_REQUEST_TEMPLATE.md)
- "Contributions Welcome" section in README and SKILL.md

## 1.4.4 (2026-07-11)

### Added
- Document auto-import step in One-Click Install table

## 1.4.3 (2026-07-11)

### Added
- Subtle CTA at end of README and SKILL.md

## 1.4.2 (2026-07-11)

### Added
- Auto-Capture Cron section in SKILL.md (3 cron jobs for auto-install)

## 1.4.1 (2026-07-11)

### Added
- One-Click Install section in SKILL.md

## 1.4.0 (2026-07-11)

### Added
- Memory Galaxy Dashboard — interactive full-screen Canvas visualization

## 1.3.1 (2026-07-11)

_ClawHub auto-publish_

## 1.1.0 (2026-07-11)
- `secrets.yaml` — documented required environment secrets
- `scripts/install.ps1` — install verification script (checks Python, deps, Sidecar)
- `scripts/update.ps1` — update check script (compares with ClawHub)
- `scripts/smoke_test.ps1` — comprehensive integration tests (8 test cases)
- `README.md` — professional documentation with install steps and examples
- `CHANGELOG.md` — version history

### Changed
- `scripts/memory.py` — major optimization:
  - Structured `SidecarError` class with status/detail
  - Timeout handling (15s) with ConnectionError fallback
  - `ValueError` for empty text validation
  - Config resolution extracted to `_resolve_config()` for testability
  - `_show_result()` helper for clean output formatting
  - Logger integration (debug mode)
  - Input bounds clamping (`limit` capped 1–100)
  - Type annotations throughout
- `SKILL.md` — restructured with privacy disclosure and clearer sections

### Fixed
- All search results now return flat content strings (no raw JSON)
- Empty captures properly rejected before API call
- Connection errors handled gracefully instead of stack traces

## 1.0.1 (2026-07-11)

### Added
- `skill-card.md` — ClawHub marketplace card
- Privacy & consent disclosure in `SKILL.md`

### Fixed
- Security scan: privacy disclosure added to address SkillSpector findings

## 1.0.0 (2026-07-11)

### Added
- Initial publish to ClawHub
- `SKILL.md` with auto-capture/search/autosave instructions
- `scripts/memory.py` CLI tool
