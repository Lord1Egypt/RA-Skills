# error_recovery.md — Anomaly Mode Tri-State + 7-Day Self-Healing + State Machine

> Complete state machine reference for quality gate 4-state + anomaly mode 3-state.
> Source: `scripts/quality_gate.py` + `scripts/mg_state/transition_engine.py`

---

## Quality Gate Four-State Machine

```
NORMAL → WARNING → CRITICAL → RECOVERING → NORMAL
  ↑         ↑                         │
  └─────────┴─────────────────────────┘
```

### State Transition Rules

| Transition | Trigger Condition | Code |
|------------|------------------|------|
| NORMAL → WARNING | anomaly_count ≥ 3 | `transition_state("anomaly")` |
| WARNING → CRITICAL | Unresolved for 24h OR failure_rate > 0.2 | `_should_upgrade_to_critical()` |
| CRITICAL → RECOVERING | `force_normal` or manual fix | `transition_state("force_normal")` |
| RECOVERING → NORMAL | 8 consecutive clean checks | `consecutive_clean ≥ 8` |
| WARNING → NORMAL | anomaly_count drops to 0 | `transition_state("clean")` |
| RECOVERING → WARNING | Anomaly during recovery | `transition_state("anomaly")` |

### State Behaviors

| State | Security | Dedup | Ingest | Write Behavior |
|-------|----------|-------|--------|----------------|
| NORMAL | ✅ Full check | ✅ Full check | ✅ Full check | Normal execution |
| WARNING | ✅ Full check | ⚠️ Skip | ⚠️ Skip | Degraded write (L1 notification) |
| CRITICAL | ✅ Full check | ❌ Block | ❌ Block | Write queue (L2 paused) |
| RECOVERING | ✅ Full check | ⚠️ Relaxed | ✅ Check | Degraded write (L1 notification) |

---

## Intervention Levels (L0-L3)

| Level | Trigger Condition | Notify | Block | Timeout Handling |
|-------|------------------|--------|-------|------------------|
| L0_SILENT | NORMAL + safe action | ❌ | ❌ | - |
| L1_NOTIFY | WARNING/RECOVERING or anomaly≥3 | ✅ | ❌ | Auto-expires after 30min |
| L2_PAUSE | CRITICAL state | ✅ | ✅ | Auto-flush after 30min |
| L3_MANUAL | delete/modify + anomaly≥8 | ✅ | ✅ | Downgrades to L2 after 24h |

### L1 Parameters
- `L1_TIMEOUT_MINUTES_DEFAULT = 30`
- `L1_LOG_CAP = 30` (keep at most 30 audit records)
- After expiry, mark `audit_expired`, no manual action needed

### L2 Parameters (all configurable via `decay_config`)
- `l2_queue_cap = 20` (queue capacity)
- `l2_timeout_minutes = 30` (timeout auto-flush)
- `l2_early_recovery_m = 5` (consecutive clean checks needed for early recovery)
- Queue overflow → evict oldest entry, log `overflow_evictions`

### L3 Parameters
- `l3_anomaly_threshold = 8` (default, configurable via `decay_config`)
- `l3_sla_hours = 24` (downgrades to L2 after SLA timeout)
- `l3_max_pending = 10` (auto-downgrades oldest when exceeded)

---

## Anomaly Mode Tri-State

```
normal_decay → anomaly → error_recovery → normal_decay
```

### Transition Rules (`transition_engine.py`)

| Transition | Trigger Condition |
|------------|------------------|
| normal_decay → anomaly | failure_rate > 0.3 or failures ≥ 5 in last 10 checks |
| anomaly → error_recovery | gate_state enters CRITICAL |
| anomaly → normal_decay | 5 consecutive clean AND gate_state == NORMAL |
| error_recovery → normal_decay | 5 consecutive clean AND gate_state == NORMAL |

### Relationship with Gate State
- anomaly_mode is a **higher-level diagnostic dimension** of the gate state
- CRITICAL always comes with error_recovery
- But anomaly doesn't necessarily come with WARNING (may still be NORMAL)

---

## 7-Day Self-Healing Mechanism

```python
# auto_heal_anomaly_mode() in transition_engine.py
auto_heal_hours = 168  # 7 days
```

**Trigger conditions (all must be met):**
1. Current mode == `anomaly`
2. Been in anomaly for over 168 hours (7 days)
3. Last 5 checks all passed

**Effect:**
- Reset to `normal_decay`
- Clear `anomaly_mode_entered_at` and `anomaly_mode_reason`

**Note:** Only applies to `anomaly` mode, not `error_recovery`

---

## End Correction

- Detects active memories with `decay_score < 0.3`
- Marks `gate_mode: "anomaly_correction"` + bypass_reason
- Invocation: `end_correction(meta_path, meta)`
- Returns list of marked memory IDs

---

## Key Threshold Quick Reference

| Parameter | Value | Location |
|-----------|-------|----------|
| WARNING_ANOMALY_N | 3 | `quality_gate.py` |
| WARNING_CRITICAL_HOURS | 24 | `quality_gate.py` |
| WARNING_FAILURE_RATE | 0.2 | `quality_gate.py` |
| RECOVERY_SWITCH_M | 8 | `quality_gate.py` |
| END_CORRECTION_THRESHOLD | 0.3 | `quality_gate.py` |
| AUDIT_HISTORY_MAX | 200 | `quality_gate.py` |
| anomaly failure rate threshold | 0.3 | `transition_engine.py` |
| anomaly recovery consecutive count | 5 | `transition_engine.py` |
| auto_heal hours | 168 | `transition_engine.py` |
