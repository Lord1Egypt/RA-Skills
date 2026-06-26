# advanced-tools.md — PID Adaptive / Quiet Degradation / Scar β / Topic Lock

> Complete parameter reference for advanced mechanisms. Source: `scripts/pid_adaptive.py` + `scripts/memory_decay.py` + `scripts/mg_state/quality_gate_rules.py`

---

## PID Adaptive Controller

> `scripts/pid_adaptive.py` — Per-scene-group PID threshold adjustment

### Core Formula

```
threshold_adjust = Kp × error + Ki × integral + Kd × derivative
```

### Default Gains

| Parameter | Value | Description |
|-----------|-------|-------------|
| DEFAULT_KP | 0.1 | Proportional gain (conservative) |
| DEFAULT_KI | 0.02 | Integral gain (low, prevents windup) |
| DEFAULT_KD | 0.05 | Derivative gain (damping) |

### Safety Limits

| Parameter | Value | Description |
|-----------|-------|-------------|
| OUTPUT_LIMIT | 0.3 | Single-step adjustment cap (±0.3) |
| DEAD_ZONE | 0.01 | Ignore errors within this range |
| INTEGRAL_LIMIT | 1.0 | Integral anti-windup cap |
| MAX_HISTORY | 100 | Keep the most recent 100 error records |
| PID_UPDATE_INTERVAL_H | 1 | Minimum interval between PID updates (hours) |

### Error Signal

```
error = 0.85 - actual_L3_rate  # L3 coverage gap
```

Health score = `ln(correction_rate + 1) / ln(2)`, target < 0.3 (observational context, not part of error)
Gate state factor: WARNING=+0.1, CRITICAL=+0.3, RECOVERING=-0.05

### Per-Scene-Group

Each type (static/derive/absorb) has an independent controller, default thresholds 0.1/0.3/0.5, clamped [0.05, 0.95]
State persistence: `meta.json pid_state.controllers[]`
CLI: `status` / `compute` / `update` / `history` / `reset`

---

## Quiet Degradation

> `scripts/memory_decay.py` + `scripts/mg_state/quality_gate_rules.py`

### IQR Adaptive (within decay engine, effective when trigger_count ≥ min_sample)

```python
if beta_log_smooth > median_beta + iqr_multiplier × IQR:
    beta_log_smooth = beta_log_smooth × discount + median_beta × (1 - discount)
```

| Parameter | Default | Config Key | Description |
|-----------|---------|------------|-------------|
| min_sample | 5 | `quiet_degradation.min_sample` | Minimum trigger count |
| iqr_multiplier | 1.5 | `quiet_degradation.iqr_multiplier` | IQR multiplier |
| median_discount | 0.7 | `quiet_degradation.median_discount` | Outlier discount |
| trigger_exemption | 5 | `quiet_degradation.trigger_exemption` | Exemption threshold |

Uses `_precomputed_betas` to avoid O(N²). Effect: β outliers pulled back toward the median.

### Relative Baseline (within quality gate, `quality_gate_rules.py`)

```
degraded = sample_count ≥ min_sample AND baseline > 0 AND current < baseline / 1.5
```

| Parameter | Value | Description |
|-----------|-------|-------------|
| relative_baseline_factor | 1.5 | Current value below baseline/1.5 → degraded |
| baseline_window_days | 30 | Baseline window |
| seed_stale_days | 14 | Seed data staleness threshold |

---

## Scar β Calculation

> `scripts/memory_decay.py` → `compute_beta_recovery()`

### Complete Formula

```
β_log_smooth = max(1, 1 + α × ln(idle_days / base_days))
  × zombie_acceleration  (if zombie)
  → cap by type beta_cap

failure_boost = min(failure_count × 0.05, 2.0)
time_decay = max(0, 0.02 × days_since_creation / 30)

β_effective = β_log_smooth × (1 + failure_boost) - time_decay
β_effective = max(β_effective, 0.1)
```

### Wakeup Weights

| Wakeup Type | idle_days Effect | Code |
|-------------|-----------------|------|
| passive (external trigger) | +1.0 days effective idle | `WAKEUP_PASSIVE_BOOST` |
| active (cron/heartbeat) | +0.3 days effective idle | `WAKEUP_ACTIVE_BOOST` |

- Update `passive_wakeup_streak` on write
- streak resets on access
- zombie detection: `passive_wakeup_streak == 0 AND idle_days > 30`

### Per-Type Override

The `beta_cap` in the type profile is the **authoritative upper limit**, overriding the global BETA_CAP:
- static: 1.0 → almost no decay
- derive: 3.0 → moderate
- absorb: 3.5 → allows higher β

---

## Topic Lock

> Tag-based dedup for cases, preventing duplicate writes on the same topic

- Implemented in the dedup layer of `memory_ingest`
- Checks tag overlap between new memory and existing memories
- High overlap + high Jaccard similarity → reject write
- Not an independent tool, part of the ingest flow

### Related Parameters

| Parameter | Value | Location |
|-----------|-------|----------|
| dedup Jaccard threshold | 0.15 | `quality_gate.py check_layer("dedup")` |
| topic_similarity threshold | 0.6 | `similar_case_signal` calculation |

---

## File Sync

> `scripts/memory_sync.py` — File → meta.json auto-sync

### Trigger Timing
- Step 0 of `run_batch` (auto-executed before decay)
- Manual `memory_sync(dry_run=true)` to preview

### Scan Scope
- `MEMORY.md`: split by `##` headings, extract content containing action keywords
- `memory/*.md` (daily notes): split by `###` headings, extract action_lines

### Filtering Strategy
- **Keyword matching**: decision/confirm/complete/fix/release/update etc. → valuable
- **Skip headings**: index/file location/Git etc. → pure link lists
- **Minimum length**: skip content under 10 characters
- **Dedup check**: `quick_dedup_check(content, memories, threshold=0.85)`

### Cooldown Mechanism

| Parameter | Value | Description |
|-----------|-------|-------------|
| Cooldown interval | 30 minutes | Skip if `last_sync_at` < 30min ago |
| importance assignment | 0.4-0.9 | Matched by section heading (persona=0.9, tech=0.7, index=0.4) |

### New meta.json Fields
- `last_sync_at`: most recent sync time (ISO 8601)
