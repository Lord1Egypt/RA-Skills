# case-management.md — Case State Machine + Confidence + Freeze + L3 Audit Specification

> Full lifecycle management reference for judgment cases. Source: `scripts/case_invalidate.py` + `scripts/l3_confirm.py`

---

## Case State Machine

```
observing → active → frozen → reviewing → active | retired
    ↑                       ↑
    └───────────────────────┘ (unfreeze)
any state → ignore (v3.1)
```

### State Transition Rules

| Transition | Trigger Condition | Action |
|------------|------------------|--------|
| observing → active | trigger ≥ 3 AND feedback ≥ 1 AND risk_tag ≥ 1 | Auto-promote |
| active → frozen | confidence < 0.2 for 3 consecutive times | Auto-freeze |
| active → frozen | failure_count ≥ 5 AND confidence < 0.4 | Auxiliary condition |
| active → stale | No confidence change for 6 consecutive heartbeats | stale_watchdog |
| frozen → reviewing | Added to review_queue | Manual review entry |
| stale → reviewing | L3 escalation | Automatic |
| reviewing → active | `case_review(action="active")` / `unfreeze()` | Restore |
| reviewing → retired | `case_review(action="retire")` / `archive_case()` | Retire (irreversible) |
| reviewing → ignore | `case_review(action="ignore")` | No longer remind, but preserve |

---

## Confidence Curve

### Freeze Thresholds
- **Primary condition**: `confidence < 0.2` for 3 consecutive evaluations (`INVALIDATION_CONSECUTIVE_N = 3`)
- **Auxiliary condition**: `failure_count ≥ 5 AND confidence < 0.4` (either condition triggers freeze)
- **Cooldown period**: ≥ 7 days between freeze checks for the same case (`INVALIDATION_COOLDOWN_DAYS`)

### Confidence Reset
- On unfreeze, reset to `new_confidence` (default 0.5), also clear consecutive low-confidence counter

---

## Freeze/Unfreeze Rules

### Freeze
```python
mem["status"] = "frozen"
mem["frozen_at"] = now
mem["frozen_reason"] = reason  # includes confidence and consecutive count
mem["frozen_consecutive_low"] = consec
```

### Unfreeze (`unfreeze()`)
```python
mem["status"] = "active"
mem["confidence"] = new_confidence  # default 0.5
mem["consecutive_low_confidence"] = 0
```

### Frozen Cap
- `MAX_FROZEN = 20`: automatically archives the oldest frozen case when exceeded (reason `"max_frozen_exceeded"`)
- Synchronously updates review_queue

---

## Ignore Semantics (v3.1)

- After `action="ignore"`, writes an `ignore_at` timestamp
- **No more proactive reminders** (respect user intent)
- **Tags preserved for audit** (audit value)
- `case_query(filter="ignored")` can query all ignored cases
- Ignore does not change status, only adds a timestamp marker

---

## L3 Audit Four-Item Diagnostic Information

1. **Confidence history curve**: smooth decline vs. violent oscillation
2. **Recent trigger scenario semantic summary**
3. **Original write context**: `origin_type` (agent_initiated / notification_callback / unknown)
4. **Top-3 similar cases**: status + confidence + topic_similarity (> 0.6 filter)

### L3 Confirmation Flow: pending → confirmed / rejected / degraded / expired

| State | Trigger | Effect |
|-------|---------|--------|
| pending | Created | Awaiting human review |
| confirmed | Approved | Execute immediately |
| rejected | Rejected | Permanently discarded |
| degraded | 24h SLA timeout or max_pending | Downgrade to L2 execution |

---

## similar_case_signal Three-Level Signal

Calculation method: aggregate Top-3 similar cases of the target case (`topic_similarity > 0.6`)

| Signal | Meaning | Action |
|--------|---------|--------|
| `has_active_ref: true` | ≥1 similar case is active | Normal reference, single anomaly |
| `all_retired: true` | All similar cases have retired | Rule-type systemic defect → system-level audit |
| `no_similar: true` | No similar cases found (topic_similarity ≤ 0.6) | Cognitive blind spot entry |

**Key judgment:** `all_retired` doesn't just affect a single case — multiple same-type cases with all_retired → triggers a system-level trend signal

---

## System-Level Audit Perspective

- **Single stagnation** = possibly noise, observe only
- **Broad stagnation across same type** = underlying assumption failure
- Judgment basis shifts from confidence to **scenario match quality**
- L3 escalates from "case-level approval" to "system-level audit"

---

## Review Queue Format

```python
meta.case_review_queue[]  # {case_id, frozen_at, reason, confidence_at_freeze, status}
# status: pending_review | unfrozen | archived | deleted
```

---

## stale_watchdog

- No confidence change AND no operations for 6 consecutive heartbeats (~18h)
- Automatically marks stale → triggers L3 escalation
- Check: `quality_check()` returns `stale_cases[]`

---

## Code References

- Freeze/Unfreeze: `case_invalidate.py` → `check_invalidations()`, `unfreeze()`, `archive_case()`
- L3 confirmation: `l3_confirm.py` → `create_confirmation()`, `confirm()`, `reject()`, `check_timeout()`
- Review queue: `case_invalidate.py` → `get_review_queue()`
