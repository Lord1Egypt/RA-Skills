---
name: memory-guardian
description: >
  Agent workspace memory lifecycle management via 10 MCP tools + batch maintenance.
  Manages MEMORY.md, memory/ directory, meta.json, quality gate, Bayesian decay,
  case lifecycle, and compaction. Use when: (1) Installing or configuring memory-guardian,
  (2) Running scheduled or on-demand memory maintenance, (3) Diagnosing memory bloat,
  quality anomalies, or case invalidation, (4) Writing, querying, or archiving memories,
  (5) Reviewing or retiring judgment cases, (6) Checking quality gate state or L3 confirmations.
  Triggers on: memory_status, memory_decay, memory_ingest, memory_compact, quality_check,
  case_query, case_review, run_batch, memory_sync, meta.json, MEMORY.md, memory-guardian.
---

# memory-guardian

Workspace memory lifecycle system. Dual-layer Bayesian decay + four-state quality gate + case lifecycle + compaction.

## Design Principles

1. **Check status before any write** — `memory_status` first
2. **Dry-run before apply** — preview destructive operations
3. **Default behavior > toggles** — workspace defaults from `MG_WORKSPACE`
4. **Write ordering > content correctness** — sequence matters
5. **Observable but not brittle** — signal degradation → WARNING, not crash
6. **Single source of truth** — all defaults in `mg_schema/meta_defaults.py`

## MCP Tools (10)

workspace defaults from `MG_WORKSPACE` env var; only non-default params listed.

**Query**
- `memory_status()` — System overview (memory count / gate state / case summary / references integrity)
- `memory_query(type="active", min_score=0.3)` — Search memories (keyword/memory_type filter)

**Write**
- `memory_ingest(content="...", importance="auto", tags=[])` — Create new memory
- `memory_decay(lambda=0.01, dry_run=false)` — Run five-track Bayesian decay

**Audit**
- `quality_check(layer="all")` — Quality gate (retire_rate / similar_case_signal / stale_cases)
- `case_query(filter="frozen")` — Query cases (active/frozen/retired/stale/ignored)
- `case_review(case_id, action="retire", origin_type="agent_initiated")` — Case operations (active/frozen/retired/unfreeze/ignore)

**Batch**
- `run_batch(skip_compact=true, dry_run=false, timeout=300)` — Full maintenance (includes sync + signal merge)
- `memory_sync(dry_run=true)` — Sync file changes → meta.json (auto-run in run_batch)
- `memory_compact(dry_run=true, aggressive=false)` — Compact MEMORY.md

## Workflows

### New Installation

1. `memory_status` → confirm `references.complete: true`
2. If false, create missing files per the missing list, re-verify
3. Create cron task (see [signal-loop.md](references/signal-loop.md) for cron template)
4. Manually trigger once to verify

### Daily Maintenance (cron)

`run_batch(skip_compact=true)` runs automatically. Includes:
- memory_sync (incremental file scan)
- Signal merge (access_log + cron inference)
- Decay + quality gate check
- Compact triggers only when MEMORY.md > 15KB

### Diagnostics

**D1: Memory bloat** → `memory_compact(dry_run=true)` → apply if needed → see [compaction.md](references/compaction.md)

**D2: Quality anomaly** → `quality_check(layer="all")` → see [error_recovery.md](references/error_recovery.md)

**D3: Case invalidation** → `case_query(filter="stale")` → `case_review(action="retire"|"active"|"unfreeze")` → see [case-management.md](references/case-management.md)

### Signal Loop (v0.4.6)

Dual-layer access signals feed the decay engine:
- **Layer 1** (weight 1.0): `access_log.jsonl` — agent appends after `memory_get`
- **Layer 2** (weight 0.5): cron keyword inference from daily notes
- Health check auto-degrades to Layer 2 if access_log stale > 24h

Agent must append to `access_log.jsonl` after each `memory_get` call. See [signal-loop.md](references/signal-loop.md) for integration code.

## References

Load on demand per scenario:

- [signal-loop.md](references/signal-loop.md) — Signal loop setup, AGENTS.md integration code, cron template, config fields
- [triggers.md](references/triggers.md) — Trigger/anti-trigger rules
- [parameters.md](references/parameters.md) — Decay params, β scar, PID gains, TTL
- [compaction.md](references/compaction.md) — D1 diagnosis and compaction strategy
- [error_recovery.md](references/error_recovery.md) — D2 diagnosis, anomaly states, self-healing
- [case-management.md](references/case-management.md) — D3 diagnosis, case audit, L3 review
- [advanced-tools.md](references/advanced-tools.md) — Quiet degradation, topic lock, PID adaptive

## CLI Fallback

When MCP unavailable, CLI path relative to skill dir:
```bash
python3 scripts/memory_guardian.py <command> [--workspace <path>]
```
Commands: `status`, `ingest`, `bootstrap`, `snapshot`, `run`, `violations`, `migrate`
