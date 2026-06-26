# Changelog

All notable changes to auto-evolve are documented here.

## [3.1.0] -- 2026-04-05

### New Features

- **EffectTracker:** `EffectTracker` class compares before/after snapshots of code quality metrics. Tracks: TODO/FIXME count, code lines, function count, duplicate lines, lint errors. Generates `effect.json` per iteration with verdict (positive/neutral/negative). Called automatically after each scan when changes are committed. `auto-evolve.py effects` command to inspect reports.

- **CostTracker:** `CostTracker` class records each LLM call with prompt/completion token counts and estimated USD cost using `LLM_PRICING` table (MiniMax-M2, GPT-4, GPT-4o, GPT-4o-mini, Claude 3.5 Sonnet, Claude 3 Opus). Calls saved to `llm_calls.jsonl` per iteration. Aggregated cost stored in `catalog.json` (`total_cost_usd`, `llm_calls`). `auto-evolve.py costs` command to view breakdowns.

- **IssueLinker:** `IssueLinker` class uses `gh issue list --json` to find open issues referencing changed files (by filename match in title/body). After each commit (auto or approved), `close_related_issues()` adds a comment and closes with reason `completed`. Integrated into `cmd_scan` (full-auto), `cmd_confirm`, and `cmd_approve`.

- **SmartScheduler:** `SmartScheduler` class assesses repo activity by counting commits in last 7 days. Thresholds: very_active (≥20, →24h), active (≥10, →72h), normal (≥3, →168h), idle (<3, →336h). `schedule --suggest` shows per-repo recommendations. `schedule --auto` applies them to config. Per-repo `scan_interval_hours` field added to `Repository` dataclass and config schema.

- **`effects` command:** `cmd_effects()` displays effect tracking reports for recent iterations. Shows verdict, summary, and delta values. `--iteration` flag for specific iteration.

- **`costs` command:** `cmd_costs()` displays LLM cost breakdown by iteration and model. Shows per-model call count, token count, and cost. `--iteration` flag for specific iteration.

- **Schedule `--suggest` and `--auto`:** New subcommands for smart scheduling. `--suggest` prints activity assessment and recommended intervals. `--auto` applies changes to config.

### Changed

- **Log output:** Shows 💰 cost and 🤖 LLM call count per iteration.
- **Repository config:** Added `scan_interval_hours` field per repository.
- **Iteration manifest:** Added `total_cost_usd` and `llm_calls` fields.
- **Catalog:** Added `total_cost_usd` and `llm_calls` per iteration entry.
- **`scan` output:** Shows effect verdict after scan completes.
- **`confirm` and `approve`:** Call IssueLinker to auto-close related issues after commit.

### Internal

- `LLM_PRICING` constant with per-model input/output pricing
- `EffectTracker` class with `snapshot()`, `track_iteration_effect()` methods
- `CostTracker` class with `track_llm_call()`, `get_iteration_cost()`, `load_calls()`, `flush_calls()` methods
- `IssueLinker` class with `find_related_issues()`, `close_issue()`, `close_related_issues()` methods
- `SmartScheduler` class with `assess_activity()`, `get_recommended_interval()`, `get_activity_stats()`, `suggest_schedule()`, `apply_schedule()` methods
- `run_llm_analysis_on_changes()` accepts optional `CostTracker` to track LLM costs
- `run_scan()` returns 4-tuple including `after_snapshots` for effect tracking
- `cmd_effects()`, `cmd_costs()` commands
- `Repository.scan_interval_hours` field added
- `IterationManifest.total_cost_usd` and `llm_calls` fields added

---

## [3.0.0] -- 2026-04-05

### New Features

- **LLM-driven code analysis:** `get_openclaw_llm_config()` reads OpenClaw LLM config. `analyze_with_llm()` sends top 5 pending items to LLM for optimization suggestions. `run_llm_analysis_on_changes()` orchestrates LLM calls and updates priority. Results stored in `pending-review.json`. No separate API key required.

- **Dependency awareness:** `analyze_dependencies()` scans import/require statements across Python, JavaScript, TypeScript, Go, and Java files. `build_dependency_map()` and `find_dependents()` build and query the dependency graph. Shown in scan output as `[!] Dependency Alert:` with list of affected files.

- **Test comparison:** `run_test_comparison()` runs pytest at two git refs and compares coverage. `run_tests_for_hash()` checks out a ref and runs pytest with coverage. Results stored in `metrics.json` as `test_coverage_delta`. Requires pytest and coverage plugin.

- **Cherry-pick rollback:** `rollback --to VERSION --item ID` reverts only the specific commit matching item ID. Implemented in `cmd_rollback()` with `item_id` argument. Shows `(cherry-pick: only item #N)` in output.

- **Multi-language support:** `TODO_PATTERNS` dict covers `.py`, `.js`, `.ts`, `.go`, `.sh`, `.java`, `.md`. `LANGUAGE_EXTENSIONS` maps extensions to language names. `scan_todos_multilang()` scans all supported file types with correct patterns. `_scan_code_file()` detects long functions in JS/TS/Go. Language detection shown in repo-list and scan output.

- **Release management:** `cmd_release()` / `release` command creates git tag + GitHub release. `create_release()` creates `v{version}` tag, pushes to origin, and calls `gh release create` with auto-generated release notes.

- **Contributor tracking:** `track_contributors()` parses git log, distinguishes `auto:` / `auto-evolve:` commits from manual commits. Returns total/auto/manual counts, auto percentage, last manual date. Shown in scan output and `log` command as `[C] {auto}A/{manual}M ({pct}% auto)`. Stored in iteration manifest.

### Changed

- **Scan output:** Shows detected languages per repository. Shows `[!deps(N)]` badge for items with dependency effects.
- **Approve prompt:** Shows dependency count and LLM badge for each item.
- **Repo-list:** Shows detected languages per repository.
- **Log command:** Shows `[C]` contributor stats and test coverage delta per iteration.
- **Iteration manifest:** Added `test_coverage_delta` and `contributors` fields.
- **Pending-review.json:** Added `affected_files`, `llm_suggestion`, `llm_implementation_hint` fields.
- **Metrics:** `test_coverage_delta` field added.

### Internal

- `get_openclaw_llm_config()`, `call_llm()`, `analyze_with_llm()` -- LLM integration
- `detect_language_from_path()`, `detect_repo_languages()`, `get_todo_patterns_for_file()` -- language detection
- `scan_todos_multilang()`, `_scan_code_file()` -- multi-language TODO scanning
- `extract_imports()`, `build_dependency_map()`, `find_dependents()`, `analyze_dependencies()` -- dependency analysis
- `run_tests_for_hash()`, `run_test_comparison()` -- test comparison
- `track_contributors()` -- contributor tracking
- `create_release()` -- release management
- `run_llm_analysis_on_changes()` -- orchestrates LLM analysis during scan
- `TODO_PATTERNS`, `LANGUAGE_EXTENSIONS` constants
- `llm_suggestion`, `llm_risk`, `llm_implementation_hint`, `affected_files` fields in ChangeItem
- `test_coverage_delta`, `contributors` fields in IterationManifest
- `release` subcommand added to CLI parser

---

## [2.2.0] -- 2026-04-05

### New Features

- **True OpenClaw cron integration:** `schedule --every` calls `openclaw cron add` directly when CLI is available. Falls back to printing manual commands otherwise. Cron ID tracked in config (`schedule_cron_id`). `schedule --remove` calls `openclaw cron remove`.

- **Value-based priority scoring:** Items scored on value/risk/cost (P = value*0.5 / risk*cost). Priority queue displayed in scan output. Pending items sorted by priority. Priority shown in approve prompt.

- **Iteration metrics tracking:** Every scan generates `.iterations/{id}/metrics.json` with todos_resolved, lint_errors_fixed, test_coverage_delta, files_changed, lines_added, lines_removed, quality_gate_passed.

- **PR batch merging:** `should_merge_prs()` detects 3+ similar changes across <=5 files to merge. `group_similar_changes()` groups by type and file scope. Applied before PR creation for high-risk changes.

- **Git conflict auto-resolution:** `handle_pr_conflict()` fetches origin/main, rebases, auto-resolves if conflicts affect <=2 files. Returns clean, auto_resolved, or manual_required.

- **Approval reasons:** `approve --reason "text"` records reason in `approvals.json`.

### Internal

- `PRIORITY_WEIGHTS`, `DEFAULT_VALUE_SCORES`, `DEFAULT_COST_SCORES` constants
- `calculate_priority()`, `infer_value_score()`, `infer_risk_score()`, `infer_cost_score()` functions
- `enrich_change_with_priority()`, `sort_by_priority()`, `priority_color()` functions
- `IterationMetrics` dataclass
- `save_metrics()`, `generate_metrics()`, `compute_todos_resolved()` functions
- `setup_cron()`, `remove_cron()` functions
- `should_merge_prs()`, `group_similar_changes()`, `build_merged_pr_body()` functions
- `get_conflict_files()`, `resolve_conflicts_simple()`, `handle_pr_conflict()` functions
- Config extended with `schedule_cron_id`
- ChangeItem extended with value/risk/cost/priority fields
- IterationManifest extended with metrics_id field

---

## [2.1.0] -- 2026-04-05

### New Features

- **Two operation modes:** `semi-auto` (default) and `full-auto`
- **`confirm` command:** Execute held changes in semi-auto mode
- **`reject` command:** Reject pending item with reason, recorded in learnings
- **`learnings` command:** View rejection and approval history
- **Learning history:** rejections.json and approvals.json in .learnings/
- **Closed-repo privacy sanitization:** pending-review.json redacts file paths
- **Execution preview:** Shows what will be executed before applying
- **`has_alert` flag** in catalog and manifest for quality gate failures

---

## [2.0.0] -- 2026-04-05

### Breaking Changes

- Config file restructured: `skills_to_monitor` replaced by `repositories[]`
- No Feishu integration
- Risk defaults changed for closed repos

### New Features

- Multi-type repositories: skill, norms, project, closed
- Branch + PR workflow for high-risk changes
- Proactive optimization scanner
- `approve` command with flexible approval
- Rollback with `git revert`
- Per-repository risk_override
- Pending-review.json

### Removed

- `--interact` flag
- Feishu notification mode
