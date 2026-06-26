# Signal Loop — Dual-Layer Access Signal Collection (v0.4.6)

## Why

The decay engine (five-track Bayesian) needs real `access_count` / `trigger_count` to compute meaningful `decay_score`. Without real access data, the engine runs in a vacuum with near-zero discrimination.

## Architecture

### Layer 1: access_log.jsonl (real-time, low noise, weight 1.0)

- Agent appends a JSON line after every `memory_get` call
- Writer: agent itself (normal workflow, not heartbeat)
- Location: workspace root (`access_log.jsonl`)

Format:
```json
{"file": "memory/2026-04-12.md", "ts": "2026-04-15T10:00:00+08:00", "context": "checking yesterday's events", "tags": ["daily-note", "instreet"]}
```

### Layer 2: Cron Inference (periodic, noisy, weight 0.5)

- `run_batch` scans recent daily notes for keyword matches + file mtime changes
- Fully internal to memory-guardian, no external dependency
- Idempotent: same-day re-runs don't double-count

### Merge Formula

```
effective_access = log_count × w1 + infer_count × w2
```

Weights configurable in `decay_config.signal_weights`:
- `access_log_weight`: 1.0 (default)
- `infer_weight`: 0.5 (default)
- `implicit_access_weight`: 0.3 (reserved)

## Signal Health Check

`run_batch` checks `access_log.jsonl` mtime at start:
- Stale > threshold → auto-degrade to Layer 2 only + WARNING log
- Does NOT block run_batch, decay continues
- Next fresh entry auto-restores dual mode

Dual-stage thresholds:
- **Deploy period** (first 7 days): 2 hours
- **Stable**: 24 hours

## New meta.json Fields

```json
{
  "signal_source": "dual",
  "signal_health": {
    "layer1_active": true,
    "layer2_active": true,
    "stale_hours": 0.0,
    "threshold_hours": 24,
    "degraded": false
  },
  "last_signal_merge": "2026-04-12T00:00:00+08:00"
}
```

`signal_source` values: `dual` | `proxy_only` | `access_log_only` (reserved)

## New decay_config Fields

```json
{
  "signal_weights": {
    "access_log_weight": 1.0,
    "infer_weight": 0.5,
    "implicit_access_weight": 0.3
  },
  "signal_stale_threshold_hours": 24,
  "signal_stale_threshold_deploy_hours": 2
}
```

## Per-memory source_file Field

Each memory gets a `source_file` field (auto-populated by memory_sync), e.g. `memory/2026-04-12.md`, used for access_log signal matching.

## Automatic Maintenance

- **access_log truncation**: merge_signals auto-cleans entries older than 30 days
- **Layer 2 idempotent**: same-day run_batch calls don't double-infer
- **Deploy adaptation**: 2h threshold for first 7 days, then 24h

## Standalone Health Check

```bash
python3 scripts/signal_loop.py --workspace <path> --health-only
```

## Cron Task Template

Create via OpenClaw cron tool (3h interval, isolated session):

```json
{
  "name": "memory-guardian maintenance (3h)",
  "schedule": { "kind": "every", "everyMs": 10800000 },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "⏰ Memory maintenance cron trigger\n\nPlease execute in order:\n1. memory_status() — check system status\n2. run_batch(skip_compact=true) — execute signal merge + decay + gate maintenance\n\nNote: run_batch automatically executes signal merge (access_log + keyword inference), no manual call needed.\nIf signal health check reports WARNING (Layer 1 stale), remind the owner in the reply.\n\nReport requirements:\n- Total memory count (active/archived)\n- Gate state (NORMAL/WARNING/CRITICAL)\n- Signal source status (dual/proxy_only)\n- Archive/delete count this run\n- MEMORY.md size\n- One-line summary if all normal, detailed list if anomalies exist",
    "timeoutSeconds": 120
  },
  "delivery": { "mode": "announce" }
}
```

- Interval 3h (10800000ms), adjustable 1–6h based on write frequency
- `delivery.mode="announce"` pushes results to user
- Manually trigger once after creation to verify

## Agent Integration

The agent must append access_log entries. This code block should be in the agent's AGENTS.md:

```bash
echo '{"file":"memory/YYYY-MM-DD.md","ts":"'$(date -Iseconds)'","context":"brief reason","tags":["tag1"]}' >> access_log.jsonl
```

Rules:
- `file` must match meta.json relative path (e.g. `memory/2026-04-12.md`)
- `context` ≤ 200 chars
- Append after every `memory_get` call that reads a memory/ file
