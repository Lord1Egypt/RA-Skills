# memory-guardian

`memory-guardian` is a local memory maintenance toolkit for Agent workspaces, providing a unified CLI and MCP Server around `meta.json`, snapshots, quality gates, decay, case migration, and dataflow observability. Current version offers dual entry points:
- **MCP Server** (`mcp_server.py`): 10 structured tools, stdio transport, for MCP clients like OpenClaw
- **CLI** (`scripts/memory_guardian.py`): Unified command-line entry point, for manual ops and cron scheduling
- **File Sync** (`scripts/memory_sync.py`): Auto-detect MEMORY.md / daily notes changes and sync to meta.json

The script layer (`scripts/`) has layered schema, repo, telemetry, state, and ingest service without switching the default storage backend.v0.4.5 introduces the **6-layer lazy-loading architecture** (Storage / Index / Routing / Signal / Decay / Migration), implemented via `mg_schema` / `mg_repo` / `mg_app` / `mg_events` / `mg_state` layered modules with on-demand imports to reduce cold-start overhead.New `memory_router` (tag-based routing) and `migrate_retag` (migration script) modules.

## Use Cases

- Maintaining long-term memory or case libraries based on `memory/meta.json`
- Migrating legacy `mem_*` records to more stable `case_*` data
- Governing write quality, anomaly states, L3 human confirmations, and invalidated cases
- Providing repeatable dry-run / apply ops workflows for Agent sessions
- Tracking per-module hit/miss, I/O volumes, and pipeline breakage candidates
- Lazy-loading architecture: 6-layer modules (Storage/Index/Routing/Signal/Decay/Migration) with on-demand imports
- Tag-based routing: `memory_router` distributes memories to index partitions by tag for fast tag queries
- Migration scripts: `migrate_retag` supports batch retagging and migration operations

## Current Capabilities

- **MCP Server**: 10 structured tools (memory_status / memory_query / memory_decay / memory_ingest / memory_compact / quality_check / case_query / case_review / run_batch / memory_sync), supporting stdio and CLI dual modes
- **6-Layer Lazy-Loading Architecture**: `mg_schema` (Storage) / `mg_repo` (Index) / `mg_app` (Application) / `mg_events` (Signal) / `mg_state` (Decay) / migration scripts, on-demand imports
- Tag-based routing: `memory_router` distributes memories to index partitions by tag for fast tag queries
- Auto file sync: `memory_sync` scans MEMORY.md and daily notes, filters by keywords + dedup check, auto-ingests to meta.json as Step 0 of run_batch
- Unified CLI entry point: status check, write, bootstrap, snapshot, maintenance workflow
- Schema normalization: `mg_schema.normalize_meta()` handles legacy field compatibility and default value filling
- Repo / App layering: `mg_repo` and `mg_app` encapsulate `meta.json` persistence and ingest orchestration
- Telemetry: `mg_events.telemetry` records module hits, I/O volumes, and reports
- Quality gate: supports `NORMAL / WARNING / CRITICAL / RECOVERING` state transitions
- L3 human confirmation: supports pending, confirm, reject, timeout downgrade
- PID adaptive: adjusts thresholds by scene group
- Case invalidation: freezes after consecutive low-confidence triggers, enters human review queue
- Snapshots & audit: `run` triggers `snapshot` for cross-time workspace comparison
- Agent Skill: conforms to OpenClaw AgentSkills spec with YAML frontmatter + 6 references/ lazy-loaded files
- File sync: `memory_sync` auto-executes as Step 0 of `run_batch`, 30-minute cooldown, keyword filtering + dedup
- Migration scripts: `migrate_retag` supports batch retagging and migration operations

## Project Structure

```text
memory-guardian/
├─ mcp_server.py              # MCP Server entry point (10 tools)
├─ scripts/
│  ├─ memory_guardian.py      # Unified CLI entry point
│  ├─ mg_utils.py             # Shared utilities: meta I/O, time, tokenization, protection rules
│  ├─ mg_schema/              # Storage layer: schema normalization and defaults
│  ├─ mg_repo/                # Index layer: meta.json persistence abstraction
│  ├─ mg_app/                 # Application layer: ingest service
│  ├─ mg_events/              # Signal layer: telemetry / dataflow stats
│  ├─ mg_state/               # Decay layer: quality gate state and rules
│  ├─ memory_router.py        # tag-based routing (distributes to index partitions by tag)
│  ├─ migrate_retag.py        # Batch retagging migration script
│  ├─ quality_gate.py         # Quality gate module
│  ├─ memory_sync.py          # File→meta.json auto sync
│  ├─ l3_confirm.py           # L3 human confirmation
│  ├─ pid_adaptive.py         # PID adaptive control
│  ├─ case_invalidate.py      # Case invalidation & review queue
│  └─ ...                     # decay / compact / diff / migrate and other scripts
├─ references/                # Skill lazy-loaded reference docs (6 files)
├─ tests/                     # unittest regression suite (581 tests)
├─ docs/                      # Design document
├─ CHANGELOG.md
├─ LICENSE                    # Mulan PSL v2
└─ SKILL.md                   # Agent Skill definition (YAML frontmatter)
```

## Workspace Conventions

Tools rely on the following workspace structure by default:

```text
<workspace>/
├─ MEMORY.md
├─ memory/
│  ├─ meta.json
│  └─ YYYY-MM-DD.md
└─ .memory-guardian/
   └─ diff-snapshots/
```

- Specify default workspace via `OPENCLAW_WORKSPACE` environment variable
- Or explicitly pass `--workspace <path>` with each command
- Always specify `--workspace` explicitly in automated environments to avoid writing to the default directory

## Quick Start

### 1. Check Current Status

```bash
python scripts/memory_guardian.py status --workspace <workspace>
```

This outputs:

- `meta.json` version and total memory count
- Count distribution by `status`
- Linked results from `memory_compact.py`, `memory_dedup.py`, `memory_decay.py --dry-run`

### 2. Preview a Full Maintenance Run

Maintenance workflow auto-includes file sync (sync → decay → compact → quality gate):

```bash
python scripts/memory_guardian.py run --dry-run --workspace <workspace>
```

Recommended: run dry-run first, then decide whether to apply:

```bash
python scripts/memory_guardian.py run --apply --workspace <workspace>
```

### 3. Write a Memory

```bash
python scripts/memory_guardian.py ingest \
  --content "Record a new experience" \
  --importance 0.7 \
  --tags "project,decision" \
  --workspace <workspace>
```

Also supports case field mode:

```bash
python scripts/memory_guardian.py ingest \
  --situation "When user asks to modify docs directly" \
  --judgment "First update README and usage docs" \
  --consequence "Reduces onboarding cost" \
  --action-conclusion "Organize commands first, then add workflow" \
  --workspace <workspace>
```

## Common Commands

### Main Entry `memory_guardian.py`

```bash
python scripts/memory_guardian.py status --workspace <workspace>
python scripts/memory_guardian.py run --dry-run --workspace <workspace>
python scripts/memory_guardian.py run --apply --workspace <workspace>
python scripts/memory_guardian.py ingest --content "..." --importance 0.7 --tags "project" --workspace <workspace>
python scripts/memory_guardian.py bootstrap --workspace <workspace>
python scripts/memory_guardian.py snapshot --workspace <workspace>
python scripts/memory_guardian.py migrate --dry-run --workspace <workspace>
python scripts/memory_guardian.py migrate --dry-run --no-backup --workspace <workspace>
python scripts/memory_guardian.py migrate-bootstrap --dry-run --workspace <workspace>
python scripts/memory_guardian.py migrate-042 --dry-run --workspace <workspace>
python scripts/memory_guardian.py violations-health --workspace <workspace>
python scripts/memory_guardian.py security --sec-command risk --workspace <workspace>
python scripts/memory_guardian.py quality-gate --qg-command status --workspace <workspace>
python scripts/memory_guardian.py l3-confirm --l3-command pending --workspace <workspace>
python scripts/memory_guardian.py pid-adaptive --pid-command status --workspace <workspace>
python scripts/memory_guardian.py case-grow --grow-command record-trigger --grow-id <case_id> --workspace <workspace>
python scripts/memory_guardian.py case-invalidate --inv-command review --workspace <workspace>
```

### File Sync

```bash
python scripts/memory_sync.py --dry-run --workspace <workspace>
python scripts/memory_sync.py --workspace <workspace>
```

### Standalone Modules

```bash
python scripts/dataflow_report.py --workspace <workspace>
python scripts/quality_gate.py status --workspace <workspace>
python scripts/l3_confirm.py pending --workspace <workspace>
python scripts/pid_adaptive.py history --workspace <workspace>
python scripts/case_invalidate.py check --dry-run --workspace <workspace>
```

## Typical Ops Workflows

### Daily Health Check

1. Run `status`
2. Run `run --dry-run` (includes sync → decay → compact → gate)
3. Check `dataflow_report.py`
4. If pending items exist, check `quality-gate`, `l3-confirm`, `case-invalidate`

### First-time Setup with Existing Workspace

1. Backup workspace
2. Run `bootstrap`
3. Run `migrate --dry-run`; pass `--no-backup` to skip backup
4. Run `migrate-bootstrap --dry-run`
5. Run `status` and `run --dry-run`

### Schema / Version Upgrade

1. Run `migrate-042 --dry-run` first
2. After confirming clean output, run `--apply` (mutually exclusive with `--dry-run`)
3. After upgrade, re-run `status`, `run --dry-run`, `dataflow_report.py`

## Unified CLI Notes

- `violations-health` View violation rule health summary directly without switching to sub-scripts.
- `security --sec-command risk` Without `--action`, lists risk levels for all known actions; with `--action <name>`, evaluates a single action.
- `case-grow --grow-command record-trigger` Requires `--grow-id <case_id>`.
- `migrate --no-backup` Explicitly disables v0.3 → v0.4 migration backup; `migrate-042` `--apply` and `--dry-run` are mutually exclusive.

## Testing & Verification

The repo primarily uses `unittest`. Core commands:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
python tests/test_all.py
python scripts/memory_guardian.py status --workspace <workspace>
python scripts/memory_guardian.py run --dry-run --workspace <workspace>
python scripts/dataflow_report.py --workspace <workspace>
```

Current regression coverage includes:

- bootstrap case migration
- high-importance protection
- schema normalization
- telemetry / dataflow reports
- compaction / log rotation
- ingest service
- typed decay
- quality gate state
- snapshot / audit events
- CLI behavior
- File sync (memory_sync): extraction, dedup, ingest, timestamp

## Design Philosophy

- Keep `scripts/` as compatible entry points, no one-shot rewrite
- Fix data flow first, then abstract modules
- `meta.json` remains the default source of truth
- Prefer dry-run before all dangerous operations
- Verify modules actually process data via telemetry, not just code path existence

## Notes

- Do not commit real sensitive memory data, keys, or tokens
- Before `--apply`, confirm `OPENCLAW_WORKSPACE` matches `--workspace`
- This repo is designed around local file workspaces; most capabilities run without external services
- Even when only modifying docs, run `status` and related dry-runs to ensure example commands haven't drifted

## Related Documents

- [`CHANGELOG.md`](CHANGELOG.md)
- [`AGENTS.md`](AGENTS.md)
- [`docs/design-proposal.md` — Design proposal (v0.4.6)
