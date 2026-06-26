# Changelog

## v0.4.6 - 2026-04-15
- **Signal loop (Phase 1)**: Dual-layer access signal collection for the decay engine.
  - Layer 1 (real-time, low noise): `access_log.jsonl` — agent appends entries after `memory_get`, weight 1.0 (configurable).
  - Layer 2 (periodic inference, noisy): cron keyword matching against memory tags in daily notes, weight 0.5 (configurable).
  - Merge formula: `effective_access = log_count × w1 + infer_count × w2`.
  - Signal health check: monitors `access_log.jsonl` mtime, auto-degrades to Layer 2 only with WARNING when stale > threshold.
  - Dual-stage threshold: 2h during deployment period (first 7 days), 24h stable.
  - Access log auto-truncation: keeps last 30 days of entries.
  - `merge_signals()` integrates into `run_batch` start for seamless signal injection.
- **MCP integration**: `append_access_log` and `merge_signals` exposed via signal_loop module.
- **Phase 1 completion**: Signal loop provides real access data to decay engine, closing the "observable but not brittle" design goal.

### Code Quality
- Fixed `import json` placement in `scripts/mg_schema/__init__.py` (was after function definitions, moved to top).
- Resolved version inconsistency: `SCHEMA_VERSION` bumped from 0.4.5 → 0.4.6 to match `PRODUCT_VERSION`.
- Fixed variable shadowing in `scripts/signal_loop.py`: inner loop `for i` (bigram) shadowed outer loop `for i` (day range), renamed to `for bi`.
- Fixed circular import risk in `scripts/memory_sync.py`: replaced `from memory_guardian import workspace_path` with `from mg_utils import workspace_path`.
- Moved `workspace_path()` and `DEFAULT_WORKSPACE` from `memory_guardian.py` to `mg_utils.py` (single source of truth).
- Rewrote `SKILL.md` following skill-creator spec: removed version history, moved signal loop details to `references/signal-loop.md`, reduced from 300 → ~90 lines.

### Verification
- Full test suite: 600 tests all green.

## v0.4.5 - 2026-04-06
- **6-layer on-demand loading architecture**: storage / index / routing / signal / decay / migration — all implemented in one release.
- **Deep code review + 38 fixes** (17 critical / 16 medium / 5 optimization) across 35 source files / 13,703 lines.

### Security & Concurrency
- Fixed file lock TOCTOU: removed `os.unlink` in unlock, lock file now persists (prevents concurrent lock acquisition on new inode).
- Added file lock to `mutate_meta()`: entire load→mutate→save under single lock.
- Added file lock to `telemetry.record_module_run()`: prevents concurrent stat loss.
- Fixed violations log rotation TOCTOU: moved `load_events` inside lock context.
- Security layer high-severity rules now enforced in quality_gate path (was only checking `critical`, now `critical` + `high`).
- CRITICAL state now triggers L3 confirmation for destructive ops (delete/modify).
- Path traversal protection in MCP `resolve_workspace()` via `realpath` + `..` check.
- MCP protocol: handle `notifications/initialized` (silent ignore) and `shutdown` (exit cleanly).

### Data Integrity
- Fixed version constant downgrade: `DEFAULT_VERSION` 0.4.2→0.4.5 (normalize_meta was downgrading on-disk version).
- Fixed sync double-write: removed redundant tail `load_meta→save_meta` that overwrote IngestService writes.
- Ingest atomicity: cleanup written file if meta update fails.
- `case_rollback.create_version_entry()`: unconditional `failure_signals` reset (nested fields were leaking old values).
- `transition_engine.anomaly_count`: now incremented on anomaly detection, reset on recovery (was read-only → anomaly mode never triggered).
- `case_invalidate`: reset `consecutive_low_confidence` on freeze.
- `case_grow.merge`: `failure_signals` snapshot now uses `deepcopy`.

### Bug Fixes
- `quality_gate.enqueue_write()`: fixed `NameError` — `l2_cfg` was never loaded (guaranteed crash on any CRITICAL queue operation).
- `migrate_to_v042.save_meta()`: removed custom implementation (tmp unbound on mkstemp failure), replaced with `mg_utils.save_meta()` wrapper.
- `migrate_to_v042`: content truncation 500→2000 chars.
- `migrate_to_v042`: try/finally cleanup for temporary fields (`_path`, `_workspace`).
- `migrate_retag.step_verify`: each check now uses independent error list (shared list caused `if not errors` logic error).
- `compute_provenance_confidence`: added [0, 1] clamp.
- `generate_memory_id`: MD5 prefix 8→12 chars (48-bit, collision probability reduced from ~1/65K to ~1/28M).
- `pid_adaptive`: D-term now individually clamped to `[-OUTPUT_LIMIT, OUTPUT_LIMIT]`.
- `l3_confirm`: unified timestamp format with `datetime.now(CST)`.
- `memory_dedup`: skip non-active/observing memories (idempotent).
- `case_grow`: added 14 English negation pairs to conflict detection.

### Optimizations
- `normalize_meta`: `read_only=True` path skips deepcopy (significant for large meta.json).
- Removed duplicate `_merge_dict_defaults` (identical to `_deep_merge_defaults`).
- MCP stdout redirect: refactored to `@contextmanager`.
- `run_batch`: timeout protection (checks elapsed time before each step).
- `_fix_meta_types`: errors now logged to stderr instead of silently swallowed.
- `memory_diff`: snapshot cleanup (keeps latest 50).
- `case_review`: documented why some actions bypass script layer.

### New Architecture Components
- `scripts/memory_router.py`: tag-based routing with inverted index, content relevance scoring, routing log.
- `scripts/mg_app/ingest_service.py`: orchestrated ingest with `IngestService`, event logging, quality gate integration.
- `scripts/mg_repo/meta_json_repository.py`: `MetaJsonRepository` with `mutate_meta` (atomic write with hash detection).
- `scripts/mg_schema/`: centralized schema defaults, normalization, deep merge.
- `scripts/mg_state/`: transition engine, quality gate rules.
- `scripts/mg_events/telemetry.py`: module run telemetry with rotation.
- `scripts/migrate_retag.py`: tag-based directory migration with verification.
- Full test suite: 581 tests all green.

## v0.4.4 - 2026-04-04
- Added `scripts/memory_sync.py`: file → meta.json auto-sync engine. Scans MEMORY.md and daily notes for new/updated content, filters by action keywords, dedup checks (threshold=0.85), and ingests via IngestService. 30-minute cooldown to avoid redundant processing. Records `last_sync_at` in meta.json.
- Integrated sync into `cmd_run`: sync now runs as Step 0 before decay in the full maintenance cycle.
- Added `memory_sync` MCP tool (10th tool) to `mcp_server.py`: supports `dry_run` mode, integrated into `run_batch` before decay.
- Updated SKILL.md: added sync tool reference, scenario 4 (file sync), auto-sync note in scenario 2, cron setup guide, updated triggers.
- New test suite: `tests/test_memory_sync.py` — 14 tests covering empty workspace, no changes, new content, dedup skip, keyword filtering, dry-run, timestamp tracking, importance assignment, and combined sources.
- Full test suite: 1131 tests all green (1092 existing + 14 new + 25 test_all incremental).
- Updated README.md: 10 tools, 1131 tests, sync documentation, updated project structure.
- Updated cron job (b42af9ab): payload changed from CLI command to MCP tool invocation (memory_status + run_batch).

## v0.4.3 - 2026-04-04
- Added MCP Server (`mcp_server.py`) providing 9 structured tools (memory_status, memory_query, memory_decay, memory_ingest, memory_compact, quality_check, case_query, case_review, run_batch) with stdio transport and CLI fallback.
- Rewrote SKILL.md following OpenClaw AgentSkills spec: added YAML frontmatter with comprehensive trigger description, diagnostic paths D1/D2/D3, tool quick reference, and per-scenario references/ loading guide.
- Added 6 reference files under `references/` for progressive disclosure: triggers.md, parameters.md, compaction.md, error_recovery.md, case-management.md, advanced-tools.md.
- Passed OpenClaw `package_skill.py` structural validation (frontmatter, naming, file organization, no symlinks).
- Script layer: 19 scripts, zero changes from v0.4.2 code baseline.
- Test suite: 1092 tests all green (532 existing + 560 new across 16 test classes).

### Verification
- `python -m unittest discover -s tests -p "test_*.py" -v`
- `package_skill.py` → `[OK] Skill is valid!`
- neuro stress test: three paths (new user / D2 CRITICAL / degradation), P0+P1 all passed

## v0.4.2 - 2026-03-30
- Hardened the unified CLI bridge in `scripts/memory_guardian.py` with shared argument helpers, deferred result emission, and tighter child-script forwarding for violations, security, quality-gate, case-grow, migration, and invalidation commands.
- Fixed real CLI contract bugs: `migrate --no-backup` now forwards correctly, `migrate-042` rejects `--apply` + `--dry-run`, `security risk` preserves the child default listing mode, and `case-grow record-trigger` now forwards the case id.
- Reduced unnecessary write amplification in `scripts/case_invalidate.py` by batching `save_meta()` calls, and added targeted regression coverage for CLI bridging, ingest compatibility, and invalidation save behavior.
- Cleaned repository-local generated artifacts and tightened ignore rules for temporary workspace directories used by tests and local tooling.

### Verification
- `python -m pytest tests -q`
- `python scripts/memory_guardian.py status --workspace tests/.tmp_workspaces/cli_verification`
- `python scripts/memory_guardian.py run --dry-run --workspace tests/.tmp_workspaces/cli_verification`
- `python scripts/memory_guardian.py migrate --dry-run --no-backup --workspace tests/.tmp_workspaces/cli_verification`
- `python scripts/memory_guardian.py migrate-042 --apply --dry-run --workspace tests/.tmp_workspaces/cli_verification`

## v0.4.2 - 2026-03-29
- Completed deep refactor Task 1-9 on the existing `scripts/` entrypoints without switching the default storage backend.
- Added the `mg_schema`, `mg_repo`, `mg_events`, `mg_state`, and `mg_app` layers to centralize schema normalization, persistence, telemetry, state transitions, and ingest orchestration.
- Landed bootstrap-to-case migration, high-importance protection, typed decay, quiet degradation rules, provenance audit, snapshot support, and initial suite decomposition while keeping `tests/test_all.py` as a compatibility runner.
- Added dedicated regression suites for migration, protection, schema normalization, telemetry, compaction, ingest service, decay classification, quality gate state, snapshot/events, CLI coverage, and full quality gate coverage.
- Hardened the test suite for the current Windows sandbox by routing temporary workspaces through a repository-local helper instead of `tempfile.mkdtemp()`.

### Verification
- `python -m unittest discover -s tests -p "test_*.py" -v`
- `python tests/test_all.py`
- `python scripts/memory_guardian.py status --workspace <workspace>`
- `python scripts/memory_guardian.py run --dry-run --workspace <workspace>`
- `python scripts/dataflow_report.py --workspace <workspace>`
