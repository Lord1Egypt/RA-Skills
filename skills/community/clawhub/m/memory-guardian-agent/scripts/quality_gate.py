#!/usr/bin/env python3
"""memory-guardian: Quality gate module (v0.4.1).

Four-state quality gate for the case pipeline:
  - NORMAL:      Full per-layer check (security → dedup → ingest → decay)
  - WARNING:     Degraded write (security only), async notification
  - CRITICAL:    Blocked write, human confirmation required
  - RECOVERING:  Gradual relaxation after CRITICAL, audit logging

State transitions:
  NORMAL → WARNING:    anomaly_count ≥ 3 OR single critical failure
  WARNING → CRITICAL:  24h unresolved OR failure_rate > 0.2
                       (Note: each anomaly increments total_failures, so
                        failure_rate is coupled with anomaly_count. With zero
                        successful writes, 4 anomalies → failure_rate=1.0
                        → immediate CRITICAL upgrade.)
  CRITICAL → RECOVERING: human --force-normal
  RECOVERING → NORMAL:  M=8 consecutive clean writes
  Any → NORMAL:        --force-normal

v0.4.1 additions:
  - 4-state machine replacing 2-state (maste/neuro)
  - Degraded write audit trail
  - Cross-session state persistence (bug fix)
  - --force-normal CLI for manual recovery
  - beta_correction on manual override (neuro)

Usage:
  python3 quality_gate.py check [--content "..."] [--workspace <path>]
  python3 quality_gate.py status [--workspace <path>]
  python3 quality_gate.py record [--pass-check | --fail-check] [--reason "..."]
  python3 quality_gate.py force-normal [--workspace <path>] [--reason "..."]
"""
import json, os, re, argparse, sys
from datetime import datetime, timedelta
from mg_utils import _now_iso, CST, tokenize, jaccard_distance, load_meta, save_meta, safe_print
from mg_events.telemetry import record_module_run
from mg_schema import normalize_meta
from mg_state.quality_gate_rules import evaluate_quiet_degradation
from mg_state.transition_engine import auto_heal_anomaly_mode, update_anomaly_mode_state

print = safe_print

# ─── Quality Gate Parameters ────────────────────────────────
WARNING_ANOMALY_N = 3          # anomalies to trigger WARNING
WARNING_CRITICAL_HOURS = 24    # hours in WARNING before CRITICAL upgrade
WARNING_FAILURE_RATE = 0.2     # failure rate to trigger CRITICAL
RECOVERY_SWITCH_M = 8          # clean writes to RECOVERING→NORMAL
END_CORRECTION_THRESHOLD = 0.3 # below this decay_score → force review
AUDIT_HISTORY_MAX = 200        # max audit log entries

# Gate layers (order matters)
LAYERS = ["security", "dedup", "ingest", "decay"]

# State constants
STATE_NORMAL = "NORMAL"
STATE_WARNING = "WARNING"
STATE_CRITICAL = "CRITICAL"
STATE_RECOVERING = "RECOVERING"
ALL_STATES = [STATE_NORMAL, STATE_WARNING, STATE_CRITICAL, STATE_RECOVERING]

# v0.4.1: Intervention levels
INTERVENTION_L0_SILENT = "L0_SILENT"      # 自动执行，不通知
INTERVENTION_L1_NOTIFY = "L1_NOTIFY"      # 异步通知（非阻塞），30min超时自动执行
INTERVENTION_L2_PAUSE = "L2_PAUSE"        # 暂停自动写入 → 写入队列（v0.4.1）
INTERVENTION_L3_MANUAL = "L3_MANUAL"      # 必须人工确认（v0.4.2）

# L3 threshold (configurable via decay_config.l3_anomaly_threshold, default 8)
L3_ANOMALY_THRESHOLD_DEFAULT = 8

# L1 Pending notification parameters
L1_TIMEOUT_MINUTES_DEFAULT = 30    # auto-execute after this many minutes
L1_LOG_CAP = 30                    # max L1 pending entries to retain

# L2 Write Queue parameters (neuro + azha0 design)
# All configurable via meta.json decay_config (defaults below)
L2_QUEUE_CAP_DEFAULT = 20          # max queued writes before forced flush
L2_TIMEOUT_MINUTES_DEFAULT = 30    # auto-recover after this many minutes
L2_EARLY_RECOVERY_M_DEFAULT = 5    # M clean writes to trigger early recovery

# v0.4.2 P2: Anomaly Mode three-state (maste)
# NORMAL_DECAY → ANOMALY → ERROR_RECOVERY
# Canonical definition in mg_state/transition_engine.py
from mg_state.transition_engine import (
    ANOMALY_MODE_NORMAL,
    ANOMALY_MODE_ANOMALY,
    ANOMALY_MODE_ERROR_RECOVERY,
)
ALL_ANOMALY_MODES = [ANOMALY_MODE_NORMAL, ANOMALY_MODE_ANOMALY, ANOMALY_MODE_ERROR_RECOVERY]



def get_l2_config(meta):
    """Read L2 config from meta.json decay_config, with defaults."""
    dc = meta.get("decay_config", {})
    return {
        "queue_cap": dc.get("l2_queue_cap", L2_QUEUE_CAP_DEFAULT),
        "timeout_minutes": dc.get("l2_timeout_minutes", L2_TIMEOUT_MINUTES_DEFAULT),
        "early_recovery_m": dc.get("l2_early_recovery_m", L2_EARLY_RECOVERY_M_DEFAULT),
    }


def load_normalized_meta(meta_path, persist=False):
    """Load meta.json and normalize schema aliases/defaults."""
    meta = load_meta(meta_path)
    normalized, changed = normalize_meta(meta)
    if persist and changed:
        save_meta(meta_path, normalized)
    return normalized


def get_gate_state(meta):
    """Get or initialize 4-state gate state from meta.json.

    Backward compatible: if v0.4 2-state exists, migrate to 4-state.
    """
    gate = meta.get("quality_gate_state", {})

    # v0.4 → v0.4.1 migration: only trigger if 'state' field is absent
    # (v0.4 used 'mode', v0.4.1 uses 'state')
    if "state" not in gate:
        old_mode = gate.get("mode", "normal")
        if old_mode == "anomaly":
            gate["state"] = STATE_WARNING
            gate["migrated_from_v04"] = True
        else:
            gate["state"] = STATE_NORMAL
            gate["migrated_from_v04"] = True
    # Ensure state is valid
    if gate.get("state") not in ALL_STATES:
        gate["state"] = STATE_NORMAL

    return {
        "state": gate.get("state", STATE_NORMAL),
        "anomaly_count": gate.get("anomaly_count", 0),
        "consecutive_clean": gate.get("consecutive_clean", 0),
        "total_writes": gate.get("total_writes", 0),
        "total_failures": gate.get("total_failures", 0),
        "failure_rate": gate.get("failure_rate", 0.0),
        "state_entered_at": gate.get("state_entered_at"),
        "last_anomaly_at": gate.get("last_anomaly_at"),
        "degraded_writes": gate.get("degraded_writes", []),
        "mode_switches": gate.get("mode_switches", 0),
        "history": gate.get("history", []),
        "migrated_from_v04": gate.get("migrated_from_v04", False),
        "total_checks": gate.get("total_checks", 0),
        "manual_overrides": gate.get("manual_overrides", []),
    }


def save_gate_state(meta_path, meta, state):
    """Persist gate state to meta.json (cross-session persistence).

    Merges state fields into existing quality_gate_state to preserve
    extra fields (check_history, l1_pending, overflow_evictions, etc.)
    that are not part of get_gate_state()'s return schema.
    """
    qgs = meta.setdefault("quality_gate_state", {})
    # Update known fields from state (skip None values to preserve existing)
    for k, v in state.items():
        if v is not None:
            qgs[k] = v
    # Bound lists
    qgs["history"] = qgs.get("history", [])[-AUDIT_HISTORY_MAX:]
    qgs["degraded_writes"] = qgs.get("degraded_writes", [])[-50:]
    save_meta(meta_path, meta)


def _hours_since(iso_str):
    """Parse ISO timestamp and return hours since then."""
    if not iso_str:
        return float('inf')
    try:
        dt = datetime.fromisoformat(iso_str)
        return (datetime.now(CST) - dt).total_seconds() / 3600
    except (ValueError, TypeError):
        return float('inf')


def _should_upgrade_to_critical(state):
    """Check if WARNING should upgrade to CRITICAL."""
    if state["state"] != STATE_WARNING:
        return False

    # Condition 1: 24h unresolved
    hours_in_warning = _hours_since(state.get("state_entered_at"))
    if hours_in_warning >= WARNING_CRITICAL_HOURS:
        return True

    # Condition 2: failure rate > threshold
    if state["failure_rate"] > WARNING_FAILURE_RATE:
        return True

    return False


def transition_state(state, trigger, reason="", now=None):
    """Execute state transitions and return (new_state, changed, transition_info).

    trigger: "anomaly" | "clean" | "force_normal" | "auto_check"
    """
    if now is None:
        now = _now_iso()

    prev = state["state"]
    changed = False
    info = ""

    if trigger == "force_normal":
        # Manual override from any state
        state["state"] = STATE_NORMAL
        state["anomaly_count"] = 0
        state["consecutive_clean"] = 0
        state["failure_rate"] = 0.0
        changed = True
        info = f"Manual force-normal: {prev} -> NORMAL"

    elif trigger == "anomaly":
        state["total_checks"] = state.get("total_checks", 0) + 1
        state["anomaly_count"] += 1
        state["total_failures"] += 1
        state["consecutive_clean"] = 0
        state["last_anomaly_at"] = now

        # Update failure rate
        total = state["total_writes"] + state["total_failures"]
        state["failure_rate"] = round(state["total_failures"] / max(total, 1), 4)

        if state["state"] == STATE_NORMAL:
            if state["anomaly_count"] >= WARNING_ANOMALY_N:
                state["state"] = STATE_WARNING
                state["state_entered_at"] = now
                changed = True
                info = f"Anomaly count {state['anomaly_count']} >= {WARNING_ANOMALY_N}: NORMAL -> WARNING"

        elif state["state"] == STATE_WARNING:
            if _should_upgrade_to_critical(state):
                state["state"] = STATE_CRITICAL
                state["state_entered_at"] = now
                changed = True
                info = f"24h unresolved / failure_rate {state['failure_rate']}: WARNING -> CRITICAL"

        elif state["state"] == STATE_RECOVERING:
            # Anomaly during recovery → back to WARNING
            state["state"] = STATE_WARNING
            state["state_entered_at"] = now
            state["anomaly_count"] = 1  # reset counter
            changed = True
            info = "Anomaly during recovery: RECOVERING -> WARNING"

    elif trigger == "clean":
        state["total_checks"] = state.get("total_checks", 0) + 1
        state["total_writes"] += 1
        state["consecutive_clean"] += 1
        state["anomaly_count"] = max(0, state["anomaly_count"] - 1)

        # Update failure rate
        total = state["total_writes"] + state["total_failures"]
        state["failure_rate"] = round(state["total_failures"] / max(total, 1), 4)

        if state["state"] == STATE_RECOVERING:
            if state["consecutive_clean"] >= RECOVERY_SWITCH_M:
                state["state"] = STATE_NORMAL
                state["state_entered_at"] = now
                changed = True
                info = f"Clean streak {state['consecutive_clean']} >= {RECOVERY_SWITCH_M}: RECOVERING -> NORMAL"

        elif state["state"] == STATE_WARNING:
            # If anomaly_count drops to 0, auto-recover
            if state["anomaly_count"] == 0:
                state["state"] = STATE_NORMAL
                state["state_entered_at"] = now
                changed = True
                info = "Anomaly count resolved: WARNING -> NORMAL"

    elif trigger == "auto_check":
        # Periodic check: upgrade WARNING→CRITICAL if conditions met (time/failure_rate)
        # This allows auto-upgrade even without new anomaly triggers
        if state["state"] == STATE_WARNING and _should_upgrade_to_critical(state):
            state["state"] = STATE_CRITICAL
            state["state_entered_at"] = now
            changed = True
            info = f"Auto-check: 24h/failure_rate threshold exceeded: WARNING -> CRITICAL"

    if changed:
        state["mode_switches"] = state.get("mode_switches", 0) + 1
        state["history"].append({
            "from": prev,
            "to": state["state"],
            "trigger": trigger,
            "reason": reason or info,
            "timestamp": now,
        })

    return state, changed, info


def check_layer(content, layer, meta, gate_state):
    """Check if content passes a specific gate layer.

    Layer behavior depends on gate state:
      NORMAL:      full check
      WARNING:     only security layer checked, others relaxed
      CRITICAL:    blocked entirely
      RECOVERING:  security + ingest, dedup relaxed
    """
    state = gate_state["state"]

    if state == STATE_CRITICAL:
        return False, "critical:blocked", False

    if layer == "security":
        # Security is ALWAYS checked (even in WARNING)
        rules = meta.get("security_rules", [])
        critical_rules = [r for r in rules if r.get("severity") in ("critical", "high")]
        content_lower = (content or "").lower()
        for rule in critical_rules:
            pattern = rule.get("pattern", "")
            if not pattern:
                continue
            try:
                if re.search(pattern, content_lower):
                    return False, f"security:{rule['id']}", False
            except re.error:
                # Skip malformed regex rules instead of falling back to literal match
                continue

    elif layer == "dedup":
        if state == STATE_WARNING:
            # Skip dedup in WARNING (degraded mode)
            return True, "dedup:skipped_warning", True
        elif state == STATE_RECOVERING:
            # Relaxed dedup in RECOVERING
            return True, "dedup:relaxed_recovering", True

        # Full dedup check
        try:
            # Dedup check using shared tokenization
            tokens_new = set(tokenize(content))
            for mem in meta.get("memories", []):
                if mem.get("status") not in ("active", "observing"):
                    continue
                tokens_old = set(tokenize(mem.get("content", "")))
                dist = jaccard_distance(tokens_new, tokens_old)
                if dist < 0.15:
                    return False, f"dedup:{mem.get('id')}", True
        except ImportError:
            pass

    elif layer == "ingest":
        if state == STATE_WARNING:
            return True, "ingest:skipped_warning", True
        if content and len(content) < 10:
            return False, "ingest:content_too_short", True

    elif layer == "decay":
        return True, "decay:passthrough", True

    return True, "pass", False


def check_all_layers(content, meta, gate_state=None):
    """Run all gate layers for content, respecting gate state.

    Returns: (all_passed, results_per_layer, is_degraded)
    """
    if gate_state is None:
        gate_state = get_gate_state(meta)

    results = {}
    all_passed = True
    is_degraded = gate_state["state"] in (STATE_WARNING, STATE_RECOVERING)

    for layer in LAYERS:
        passed, reason, bypass_allowed = check_layer(content, layer, meta, gate_state)
        results[layer] = {
            "passed": passed,
            "reason": reason,
            "bypass_allowed": bypass_allowed,
        }
        if not passed and not bypass_allowed:
            all_passed = False

    # v0.4.1: Add intervention level to results
    level, notify_needed, should_block = compute_intervention_level(gate_state, "ingest", meta)
    results["intervention_level"] = level
    results["notification_needed"] = notify_needed
    results["should_block"] = should_block

    return all_passed, results, is_degraded



def record_result(meta_path, meta, all_passed, gate_state=None):
    """Record a quality gate check result to the audit trail (check_history).

    Counters (total_checks/total_failures/total_writes) are handled by
    transition_state(), which should be called before this function.
    This function only maintains the check_history[] audit trail.
    """
    if gate_state is None:
        gate_state = get_gate_state(meta)

    # Write directly to meta to avoid save_gate_state overwriting unknown fields
    meta.setdefault("quality_gate_state", {})
    qgs = meta["quality_gate_state"]
    qgs.setdefault("check_history", [])
    qgs["check_history"].append({
        "timestamp": _now_iso(),
        "passed": all_passed,
        "state": gate_state["state"],
    })

    # Keep check_history bounded
    if len(qgs["check_history"]) > 100:
        qgs["check_history"] = qgs["check_history"][-50:]

    save_meta(meta_path, meta)


def record_degraded_write(meta_path, meta, content, gate_state, reason=""):
    """Record a degraded write to the audit trail."""
    now = _now_iso()
    entry = {
        "timestamp": now,
        "state": gate_state["state"],
        "reason": reason,
        "content_preview": (content or "")[:100],
        "layers_skipped": [],
    }

    # Record which layers were skipped
    if gate_state["state"] == STATE_WARNING:
        entry["layers_skipped"] = ["dedup", "ingest"]
    elif gate_state["state"] == STATE_RECOVERING:
        entry["layers_skipped"] = ["dedup"]

    gate_state["degraded_writes"].append(entry)
    save_gate_state(meta_path, meta, gate_state)


def end_correction(meta_path, meta):
    """Flag low-decay memories for review."""
    flagged = []
    for mem in meta.get("memories", []):
        if mem.get("status") == "active" and mem.get("decay_score", 1.0) < END_CORRECTION_THRESHOLD:
            mem.setdefault("quality_gate", {})
            mem["quality_gate"]["confidence"] = mem.get("confidence", 0.5)
            mem["quality_gate"]["gate_mode"] = "anomaly_correction"
            mem["quality_gate"]["bypass_reason"] = f"decay_score {mem['decay_score']:.3f} < {END_CORRECTION_THRESHOLD}"
            flagged.append(mem.get("id"))

    if flagged:
        save_meta(meta_path, meta)

    return flagged


def compute_intervention_level(gate_state, write_action, meta=None):
    """Compute intervention level for a write action.

    v0.4.1: L2 now actively queues writes (neuro: "visible braking point").

    Args:
        gate_state: dict from get_gate_state()
        write_action: str, e.g., "ingest", "delete", "modify", "record_trigger"
        meta: dict (optional), meta.json for reading configurable thresholds

    Returns:
        tuple: (level_str, notification_needed:bool, should_block:bool)
    """
    state = gate_state["state"]
    anomaly_count = gate_state["anomaly_count"]

    # Read configurable L3 threshold (default 8)
    l3_threshold = L3_ANOMALY_THRESHOLD_DEFAULT
    if meta:
        l3_threshold = meta.get("decay_config", {}).get(
            "l3_anomaly_threshold", L3_ANOMALY_THRESHOLD_DEFAULT
        )

    # L0: Normal state + safe actions
    if (state == STATE_NORMAL and
        write_action in ["ingest", "record_trigger"]):
        return INTERVENTION_L0_SILENT, False, False

    # L3: High-risk actions with very high anomaly count (v0.4.2 ready)
    # Must check BEFORE L1 so it takes priority for critical operations
    # Also triggers in CRITICAL state for destructive actions (delete/modify)
    if (write_action in ["delete", "modify"] and
        anomaly_count >= l3_threshold and
        state != STATE_WARNING):
        return INTERVENTION_L3_MANUAL, True, True

    # L1: Warning/Recovering states, or higher-risk actions in normal
    if ((state in (STATE_WARNING, STATE_RECOVERING) or anomaly_count >= 3) and
        state != STATE_CRITICAL):
        if write_action in ["delete", "modify"]:
            return INTERVENTION_L1_NOTIFY, True, False
        # In WARNING/RECOVERING, ingest is still L1 notify (not block)
        return INTERVENTION_L1_NOTIFY, True, False

    # L2: CRITICAL state — queue writes, block immediate execution
    if state == STATE_CRITICAL:
        return INTERVENTION_L2_PAUSE, True, True

    # Default fallback
    return INTERVENTION_L0_SILENT, False, False


def intervention_notify(level, gate_state, reason, meta_path):
    """Write intervention notification to meta.json's intervention_log[].

    Args:
        level: str, intervention level
        gate_state: dict from get_gate_state()
        reason: str, notification reason
        meta_path: str, path to meta.json

    Returns:
        dict: notification entry
    """
    now = _now_iso()
    notification = {
        "level": level,
        "timestamp": now,
        "reason": reason,
        "gate_state": gate_state["state"],
    }

    meta = load_normalized_meta(meta_path, persist=True)
    meta.setdefault("intervention_log", []).append(notification)

    # Keep last 50 notifications
    if len(meta["intervention_log"]) > 50:
        meta["intervention_log"] = meta["intervention_log"][-50:]

    save_meta(meta_path, meta)
    return notification


# ─── L2 Write Queue (v0.4.1) ───────────────────────────────

def enqueue_write(meta_path, write_data, queue_reason=""):
    """Add a write to the L2 pending queue.

    When quality gate is in CRITICAL state, writes are queued instead of
    immediately applied. Queue auto-flushes on recovery or timeout.

    Args:
        meta_path: str, path to meta.json
        write_data: dict, the write operation to queue
            e.g., {"action": "ingest", "content": "...", "fields": {...}}
        queue_reason: str, why this write was queued

    Returns:
        dict: queue entry with status
    """
    if not write_data or not isinstance(write_data, dict):
        return {"status": "rejected", "reason": "write_data must be a non-empty dict"}

    now = _now_iso()
    import uuid as _uuid

    # Fix: load meta and l2_config (previously undefined → NameError)
    meta = load_normalized_meta(meta_path, persist=True)
    l2_cfg = get_l2_config(meta)

    queue = meta.get("l2_write_queue", [])

    # Check queue overflow: if at capacity, evict oldest to make room for 1 new entry
    # After eviction: queue has cap-1 entries, then we append 1 → queue at cap
    if len(queue) >= l2_cfg["queue_cap"]:
        slots_needed = len(queue) - l2_cfg["queue_cap"] + 1
        evicted = queue[:slots_needed]
        for entry in evicted:
            entry["status"] = "force_flushed"
            entry["flushed_at"] = now
            entry["flush_reason"] = "queue_overflow"

        # Record overflow evictions (separate from degraded_writes list)
        meta.setdefault("quality_gate_state", {}).setdefault("overflow_evictions", 0)
        meta["quality_gate_state"]["overflow_evictions"] += len(evicted)

        # Move evicted entries to intervention log
        meta.setdefault("intervention_log", [])
        for entry in evicted:
            meta["intervention_log"].append({
                "level": INTERVENTION_L2_PAUSE,
                "timestamp": now,
                "reason": f"Queue overflow: force flushed {entry.get('action', '?')}",
                "gate_state": "CRITICAL",
                "queue_overflow": True,
            })

        queue = queue[slots_needed:]

    entry = {
        "id": f"q_{now.replace('-','').replace(':','').replace('.','')[:16]}_{len(queue)}_{_uuid.uuid4().hex[:4]}",
        "queued_at": now,
        "action": write_data.get("action", "ingest"),
        "fields": write_data.get("fields", {}),
        "queue_reason": queue_reason,
        "status": "pending",
    }

    queue.append(entry)
    meta["l2_write_queue"] = queue
    meta["quality_gate_state"]["queue_size"] = len(queue)
    meta["quality_gate_state"]["l2_entered_at"] = meta["quality_gate_state"].get(
        "l2_entered_at", now)

    save_meta(meta_path, meta)

    return {
        "status": "queued",
        "queue_size": len(queue),
        "queue_cap": l2_cfg["queue_cap"],
        "entry_id": entry["id"],
    }


def flush_queue(meta_path, flush_reason=""):
    """Flush the L2 pending queue — apply all pending writes.

    Called when:
    1. Gate state recovers to NORMAL or RECOVERING
    2. Timeout (L2_TIMEOUT_MINUTES) expires
    3. Manual flush via CLI

    v0.4.1 fix: Actually re-execute queued writes via memory_ingest instead
    of just marking them "flushed" (which silently dropped data).

    Args:
        meta_path: str, path to meta.json
        flush_reason: str, why the flush was triggered

    Returns:
        dict: flush summary
    """
    now = _now_iso()
    meta = load_normalized_meta(meta_path, persist=True)

    queue = meta.get("l2_write_queue", [])
    pending = [e for e in queue if e.get("status") == "pending"]

    if not pending:
        return {"flushed": 0, "skipped": 0, "failed": 0, "reason": flush_reason}

    flushed = 0
    skipped = 0
    failed = 0

    # Re-execute each queued write through memory_ingest
    for entry in pending:
        action = entry.get("action", "ingest")
        try:
            if action == "ingest":
                _replay_ingest(meta, entry)
            elif action == "delete":
                _replay_delete(meta, entry)
            elif action == "modify":
                _replay_modify(meta, entry)
            else:
                # Unknown action — skip but log
                skipped += 1
                continue

            entry["status"] = "flushed"
            entry["flushed_at"] = now
            entry["flush_reason"] = flush_reason
            flushed += 1

            # Advance gate state: each successful flush counts as a clean write
            # so RECOVERING can auto-recover via consecutive_clean ≥ M
            gate = meta.get("quality_gate_state", {})
            if gate.get("state") == STATE_RECOVERING:
                gate["consecutive_clean"] = gate.get("consecutive_clean", 0) + 1
                gate["total_writes"] = gate.get("total_writes", 0) + 1
                gate["total_checks"] = gate.get("total_checks", 0) + 1
        except Exception as exc:
            entry["status"] = "flush_failed"
            entry["flushed_at"] = now
            entry["flush_error"] = str(exc)
            failed += 1

    # Update gate state
    gate = meta.get("quality_gate_state", {})
    gate["queue_size"] = 0
    gate["l2_entered_at"] = None
    gate["last_queue_flush_at"] = now

    # Check if flush advanced RECOVERING → NORMAL (or early recovery)
    if gate.get("state") == STATE_RECOVERING:
        l2_cfg = get_l2_config(meta)
        early_m = l2_cfg.get("early_recovery_m", L2_EARLY_RECOVERY_M_DEFAULT)
        switch_m = RECOVERY_SWITCH_M
        threshold = min(early_m, switch_m)
        if gate.get("consecutive_clean", 0) >= threshold:
            gate["state"] = STATE_NORMAL
            gate["state_entered_at"] = now
            gate["anomaly_count"] = 0
            label = "early" if threshold < switch_m else "full"
            flush_reason += f" + RECOVERING->NORMAL ({label} recovery, clean streak {gate['consecutive_clean']}>={threshold})"

    # Log the flush
    meta.setdefault("intervention_log", []).append({
        "level": INTERVENTION_L2_PAUSE,
        "timestamp": now,
        "reason": f"Queue flushed: {flushed} writes ({flush_reason})",
        "gate_state": gate.get("state", "UNKNOWN"),
        "queue_flush_count": flushed,
        "queue_failed_count": failed,
        "queue_skipped_count": skipped,
    })

    save_meta(meta_path, meta)

    return {
        "flushed": flushed,
        "skipped": skipped,
        "failed": failed,
        "reason": flush_reason,
    }


def _replay_ingest(meta, entry):
    """Replay a queued ingest write into meta.json memories[].

    Mirrors memory_ingest.py field structure so flushed memories have the
    same schema as directly-ingested ones.  (v0.4.1 fix: previously
    missing ~15 fields including entities, beta, failure_*, cooldown, etc.)
    """
    fields = entry.get("fields", {})
    if not fields.get("content"):
        raise ValueError("Queued ingest has no content")

    now = _now_iso()
    import uuid

    # v0.4.5: derive memory_id and file_path from content + tags
    tags = fields.get("tags", [])
    content_text = fields["content"]
    memory_id = fields.get("memory_id")
    if not memory_id:
        from mg_utils import generate_memory_id, derive_file_path
        existing_ids = {m.get("memory_id") or m.get("id") for m in meta.get("memories", []) if m.get("memory_id") or m.get("id")}
        memory_id = generate_memory_id(content_text, existing_ids=existing_ids)
    file_path = fields.get("file_path")
    if not file_path:
        from mg_utils import derive_file_path
        file_path = derive_file_path(memory_id, tags, content_text)

    mem = {
        "id": fields.get("id", f"mem_{uuid.uuid4().hex[:8]}"),
        "memory_id": memory_id,
        "file_path": file_path,
        "content": content_text,
        "created_at": entry.get("queued_at", now),
        "updated_at": now,
        "importance": fields.get("importance", 0.5),
        "importance_f": fields.get("importance", 0.5),
        "entities": fields.get("entities", []),
        "tags": tags,
        "status": "active",
        "decay_score": fields.get("importance", 0.5),
        "access_count": 0,
        "trigger_count": 0,
        "confidence": fields.get("confidence", 0.5),
        "quality_gate": {
            "confidence": fields.get("confidence", 0.5),
            "gate_mode": fields.get("gate_mode", "normal"),
            "bypass_reason": fields.get("bypass_reason"),
            "intervention_level": "L2_REPLAY",
            "replayed_from_queue": True,
            "passed": True,
            "layers": {},
            "degraded": False,
        },
        # v0.4.5 classification
        "classification": fields.get("classification", {
            "primary_tag": "misc",
            "confidence": 0.5,
            "needs_review": False,
        }),
        "classification_confidence": fields.get("classification_confidence", 0.5),
        "signal_level": fields.get("signal_level", "none"),
        # v0.4 core fields
        "case_type": fields.get("case_type", "case"),
        "situation": fields.get("situation"),
        "judgment": fields.get("judgment"),
        "consequence": fields.get("consequence"),
        "action_conclusion": fields.get("action_conclusion"),
        "reversibility": fields.get("reversibility", 1),
        "beta": fields.get("beta", 1.0),
        "last_triggered": None,
        "cooling_threshold": fields.get("cooling_threshold", 5),
        "boundary_words": fields.get("boundary_words", []),
        "conflict_refs": [],
        "failure_conditions": [],
        "failure_count": 0,
        "last_failure_trigger": None,
        "last_failure_fix": None,
        "source_case_id": fields.get("source_case_id"),
        "alternatives_considered": fields.get("alternatives_considered", []),
        "cost_factors": fields.get("cost_factors", {
            "write_cost": 0, "verify_cost": 0, "human_cost": 0, "transfer_cost": 0,
        }),
        "importance_explain": fields.get("importance_explain"),
        "security_version": 1,
        "cooldown_active": False,
        "cooldown_until": None,
        "observing_since": None,
        "suspended_pending_count": 0,
        "memory_type": fields.get("memory_type", "derive"),
        "tags_locked": fields.get("tags_locked", False),
        # v0.4.1 provenance
        "provenance_level": fields.get("provenance_level"),
        "provenance_source": fields.get("provenance_source"),
        "citations": fields.get("citations", []),
        "last_accessed": entry.get("queued_at", now),
    }

    meta.setdefault("memories", []).append(mem)

    # v0.4.5 fix: write memory file to category directory
    fp = mem.get("file_path", "")
    if fp:
        try:
            from memory_ingest import _write_memory_file
            workspace = os.path.dirname(os.path.dirname(meta_path))  # meta.json → memory/ → workspace
            _write_memory_file(mem["memory_id"], mem.get("content", ""), fp, workspace=workspace)
        except Exception:
            import logging
            logging.warning("_replay_ingest: failed to write file %s", fp, exc_info=True)


def _replay_delete(meta, entry):
    """Replay a queued delete by marking target as archived."""
    target_id = entry.get("fields", {}).get("target_id")
    if not target_id:
        raise ValueError("Queued delete has no target_id")

    for mem in meta.get("memories", []):
        if mem.get("id") == target_id:
            mem["status"] = "archived"
            mem["archived_at"] = entry.get("queued_at", _now_iso())
            mem["archive_reason"] = f"L2_queue_replay:{entry.get('queue_reason', '')}"
            return

    raise ValueError(f"Queued delete target not found: {target_id}")


def _replay_modify(meta, entry):
    """Replay a queued modify by updating fields on target."""
    target_id = entry.get("fields", {}).get("target_id")
    update_fields = entry.get("fields", {}).get("update_fields", {})
    if not target_id or not update_fields:
        raise ValueError("Queued modify has no target_id or update_fields")

    for mem in meta.get("memories", []):
        if mem.get("id") == target_id:
            for k, v in update_fields.items():
                mem[k] = v  # Allow both updating existing and adding new fields
            mem["updated_at"] = _now_iso()
            return

    raise ValueError(f"Queued modify target not found: {target_id}")


def check_l2_timeout(meta_path):
    """Check if L2 queue has timed out and should auto-flush.

    Returns:
        dict: {"timed_out": bool, "elapsed_minutes": float, "flushed": int}
    """
    meta = load_normalized_meta(meta_path, persist=True)
    gate = meta.get("quality_gate_state", {})
    entered_at = gate.get("l2_entered_at")

    if not entered_at:
        return {"timed_out": False, "elapsed_minutes": 0, "flushed": 0}

    l2_cfg = get_l2_config(meta)

    try:
        entered_dt = datetime.fromisoformat(entered_at)
        elapsed = (datetime.now(CST) - entered_dt).total_seconds() / 60
    except (ValueError, TypeError):
        return {"timed_out": False, "elapsed_minutes": 0, "flushed": 0}

    if elapsed >= l2_cfg["timeout_minutes"]:
        result = flush_queue(meta_path, f"timeout ({elapsed:.0f}min > {l2_cfg['timeout_minutes']}min)")
        return {"timed_out": True, "elapsed_minutes": round(elapsed), "flushed": result.get("flushed", 0)}

    return {"timed_out": False, "elapsed_minutes": round(elapsed), "flushed": 0}


# ─── L1 Pending Queue ────────────────────────────────────────

def enqueue_l1_pending(meta_path, write_data, reason=""):
    """Queue a write as L1 pending (notified, auto-executes after timeout).

    L1 semantics: notify the human, proceed with write immediately BUT
    also log it in l1_pending[] so it can be audited. Unlike L2 which
    blocks execution, L1 writes go through right away.

    If the gate state is WARNING/RECOVERING, L1 writes for delete/modify
    are still executed but tracked for 30min audit window.

    Args:
        meta_path: str, path to meta.json
        write_data: dict, {"action": str, "fields": dict}
        reason: str, why this write was L1

    Returns:
        dict: queue entry
    """
    now = _now_iso()
    meta = load_normalized_meta(meta_path, persist=True)

    dc = meta.get("decay_config", {})
    timeout = dc.get("l1_timeout_minutes", L1_TIMEOUT_MINUTES_DEFAULT)

    entry = {
        "id": f"l1_{now.replace('-','').replace(':','').replace('.','')[:16]}",
        "queued_at": now,
        "action": write_data.get("action", "unknown"),
        "fields": write_data.get("fields", write_data),
        "reason": reason,
        "status": "executed",  # L1 always executes immediately
        "audit_until": None,    # set below
        "reviewed": False,
    }

    # Set audit window end time
    from datetime import datetime, timedelta
    try:
        queued_dt = datetime.fromisoformat(now)
        audit_end = queued_dt + timedelta(minutes=timeout)
        entry["audit_until"] = audit_end.isoformat()
    except (ValueError, TypeError):
        pass

    pending = meta.get("l1_pending", [])
    pending.append(entry)

    # Cap pending list
    if len(pending) > L1_LOG_CAP:
        pending = pending[-L1_LOG_CAP:]

    meta["l1_pending"] = pending
    save_meta(meta_path, meta)

    return entry


def check_l1_audit_expired(meta_path):
    """Check and resolve expired L1 audit entries.

    Expired entries that haven't been reviewed are auto-resolved
    (no action needed, just marked as audit_expired).

    Returns:
        dict: {"expired": int, "resolved": int}
    """
    now = _now_iso()
    meta = load_normalized_meta(meta_path, persist=True)
    pending = meta.get("l1_pending", [])

    if not pending:
        return {"expired": 0, "resolved": 0}

    from datetime import datetime
    expired = 0
    for entry in pending:
        if entry.get("status") != "executed":
            continue
        audit_until = entry.get("audit_until")
        if not audit_until:
            continue
        try:
            if datetime.fromisoformat(now) >= datetime.fromisoformat(audit_until):
                if not entry.get("reviewed"):
                    entry["status"] = "audit_expired"
                    entry["resolved_at"] = now
                    entry["resolution"] = "auto: audit window expired"
                    expired += 1
        except (ValueError, TypeError):
            continue

    meta["l1_pending"] = pending
    save_meta(meta_path, meta)

    return {"expired": expired, "resolved": expired}


def get_l1_pending_count(meta_path):
    """Return count of active (executed, within audit window) L1 entries."""
    meta = load_normalized_meta(meta_path, persist=True)
    pending = meta.get("l1_pending", [])
    active = [e for e in pending if e.get("status") == "executed"]
    return {"active": len(active), "total": len(pending)}


# ─── CLI Commands ────────────────────────────────────────────

def cmd_check(content, meta_path, workspace):
    """Check content against all gate layers."""
    meta = load_normalized_meta(meta_path, persist=True)
    gate_state = get_gate_state(meta)

    state_icons = {
        STATE_NORMAL: "🟢",
        STATE_WARNING: "🟡",
        STATE_CRITICAL: "🔴",
        STATE_RECOVERING: "🔵",
    }
    icon = state_icons.get(gate_state["state"], "❓")

    print(f"{icon} Quality Gate Check (state: {gate_state['state']})")
    print(f"  Anomaly count: {gate_state['anomaly_count']}/{WARNING_ANOMALY_N}")
    print(f"  Consecutive clean: {gate_state['consecutive_clean']}/{RECOVERY_SWITCH_M}")
    print(f"  Failure rate: {gate_state['failure_rate']:.2%}")
    print()

    if not content:
        print("No content to check.")
        return

    all_passed, results, is_degraded = check_all_layers(content, meta, gate_state)

    for layer, r in results.items():
        icon = "✅" if r["passed"] else ("⚠️" if r["bypass_allowed"] else "🚫")
        print(f"  {icon} {layer}: {r['reason']}")

    if is_degraded:
        print(f"\n  ⚠️ DEGRADED MODE — some layers skipped")

    print(f"\n  Overall: {'PASS' if all_passed else 'BLOCKED'}")

    # Record result
    trigger = "clean" if all_passed else "anomaly"
    prev = gate_state["state"]
    new_state, switched, info = transition_state(gate_state, trigger, reason=results)
    save_gate_state(meta_path, meta, new_state)

    if switched:
        print(f"\n  🔄 {info}")
        # Auto-flush L2 queue when leaving CRITICAL state
        if prev == STATE_CRITICAL and new_state["state"] != STATE_CRITICAL:
            flush_result = flush_queue(meta_path, f"auto_flush on state exit: {info}")
            if flush_result.get("flushed", 0) > 0:
                print(f"  🚰 Auto-flushed {flush_result['flushed']} queued writes")

    if is_degraded and all_passed:
        record_degraded_write(meta_path, meta, content, new_state, reason="degraded_write")

    # L1: Log to pending queue for audit tracking (30min window)
    intervention = results.get("intervention_level", "")
    if intervention == INTERVENTION_L1_NOTIFY:
        enqueue_l1_pending(
            meta_path,
            {"action": "ingest", "fields": {"content": content[:200]}},
            reason=f"L1_NOTIFY check: state={new_state['state']}",
        )
        print(f"  🟡 L1 audit window started (30min)")


def cmd_status(meta_path, workspace):
    """Show quality gate state."""
    meta = load_normalized_meta(meta_path, persist=True)
    gate_state = get_gate_state(meta)

    state_icons = {
        STATE_NORMAL: "🟢",
        STATE_WARNING: "🟡",
        STATE_CRITICAL: "🔴",
        STATE_RECOVERING: "🔵",
    }
    icon = state_icons.get(gate_state["state"], "❓")

    print(f"{icon} Quality Gate Status (v0.4.1 4-state)")
    print(f"  State: {gate_state['state']}")
    print(f"  Anomaly count: {gate_state['anomaly_count']}/{WARNING_ANOMALY_N}")
    print(f"  Consecutive clean: {gate_state['consecutive_clean']}/{RECOVERY_SWITCH_M}")
    print(f"  Failure rate: {gate_state['failure_rate']:.2%}")
    print(f"  Total writes: {gate_state['total_writes']}")
    print(f"  Total failures: {gate_state['total_failures']}")
    print(f"  State entered at: {gate_state.get('state_entered_at', 'N/A')}")
    print(f"  Last anomaly at: {gate_state.get('last_anomaly_at', 'N/A')}")
    print(f"  State transitions: {gate_state['mode_switches']}")
    print(f"  Degraded writes: {len(gate_state.get('degraded_writes', []))}")
    print(f"  History entries: {len(gate_state.get('history', []))}")

    if gate_state.get("migrated_from_v04"):
        print(f"  ⚠️ Migrated from v0.4 2-state")

    # L2 queue info (v0.4.1)
    queue = meta.get("l2_write_queue", [])
    pending = [e for e in queue if e.get("status") == "pending"]
    if pending or gate_state.get("l2_entered_at"):
        entered = gate_state.get("l2_entered_at")
        l2_cfg = get_l2_config(meta)
        if entered:
            try:
                elapsed = (datetime.now(CST) - datetime.fromisoformat(entered)).total_seconds() / 60
                remaining = max(0, l2_cfg["timeout_minutes"] - elapsed)
                print(f"\n  📦 L2 Queue: {len(pending)}/{l2_cfg['queue_cap']} pending (timeout in {remaining:.0f}min)")
            except (ValueError, TypeError):
                print(f"\n  📦 L2 Queue: {len(pending)}/{l2_cfg['queue_cap']} pending")

    # L1 pending audit info (v0.4.1)
    l1_result = check_l1_audit_expired(meta_path)
    l1_count = get_l1_pending_count(meta_path)
    if l1_count["active"] > 0 or l1_result["expired"] > 0:
        print(f"\n  🟡 L1 Audit: {l1_count['active']} active, {l1_result['expired']} expired this check")
    # Re-load meta after audit expiry may have written
    meta = load_normalized_meta(meta_path, persist=True)

    # State transition history
    history = gate_state.get("history", [])
    if history:
        print(f"\n  📋 State transitions:")
        for h in history[-10:]:
            # Backward compat: v0.4 entries have 'passed'/'mode' instead of 'from'/'to'
            if "from" not in h and "mode" in h:
                h_from = h["mode"]  # v0.4: single mode, no from/to
                h_to = h["mode"]
                h_reason = ("PASS" if h.get("passed") else "FAIL") + " (v0.4 check)"
            else:
                h_from = h.get("from", "?")
                h_to = h.get("to", "?")
                h_reason = h.get("reason", "")[:60]
            icon = "🟢" if h_to == STATE_NORMAL else ("🟡" if h_to == STATE_WARNING else ("🔴" if h_to == STATE_CRITICAL else "🔵"))
            ts = h.get("timestamp", "")[:16]
            print(f"    {icon} [{ts}] {h_from} → {h_to}: {h_reason}")

    # Degraded writes summary
    degraded = gate_state.get("degraded_writes", [])
    if degraded:
        print(f"\n  ⚠️ Recent degraded writes ({len(degraded)}):")
        for dw in degraded[-5:]:
            ts = dw.get("timestamp", "")[:16]
            skipped = ", ".join(dw.get("layers_skipped", []))
            print(f"    [{ts}] {dw.get('state', '?')}: skipped={skipped}")
            print(f"      {dw.get('content_preview', '')[:60]}")

    # CRITICAL: show end-correction
    if gate_state["state"] in (STATE_CRITICAL, STATE_WARNING):
        print(f"\n  💡 Use --force-normal to manually restore to NORMAL")

    # Check for WARNING → CRITICAL upgrade
    if gate_state["state"] == STATE_WARNING and _should_upgrade_to_critical(gate_state):
        print(f"\n  ⚠️ WARNING should upgrade to CRITICAL (24h exceeded or failure_rate > {WARNING_FAILURE_RATE})")
        print(f"     Run auto-check to trigger upgrade, or use --force-normal to reset")


def cmd_record(meta_path, workspace, passed, reason):
    """Manually record a pass/fail with anomaly mode tracking (v0.4.2 P2)."""
    meta = load_normalized_meta(meta_path, persist=True)
    gate_state = get_gate_state(meta)

    trigger = "clean" if passed else "anomaly"
    new_state, switched, info = transition_state(gate_state, trigger, reason=reason)

    # v0.4.2 P2: Update anomaly mode (maste three-state)
    _update_anomaly_mode(meta, new_state, passed, trigger)

    # Record result to check_history (modifies meta + saves)
    record_result(meta_path, meta, passed, gate_state=new_state)

    # Final save: anomaly_mode + gate_state in one write
    save_gate_state(meta_path, meta, new_state)

    mode = meta.get("anomaly_mode", ANOMALY_MODE_NORMAL)
    action = "PASS" if passed else "FAIL"
    print(f"Recorded: {action} — state={new_state['state']} | mode={mode}")
    if switched:
        print(f"  🔄 {info}")


# ─── v0.4.2 P2: Anomaly Mode Three-State (maste) ────────────

def _update_anomaly_mode(meta, gate_state, passed, trigger):
    """Update anomaly mode via the explicit transition engine."""
    state = update_anomaly_mode_state(meta, gate_state, passed, trigger)
    return state


def get_anomaly_mode(meta, meta_path=None):
    """Get current anomaly mode with metadata.

    If meta_path is provided, auto-heal changes are persisted to disk.
    """
    healed = auto_heal_anomaly_mode(meta)
    mode = meta.get("anomaly_mode", ANOMALY_MODE_NORMAL)
    entered = meta.get("anomaly_mode_entered_at")
    reason = meta.get("anomaly_mode_reason", "")
    if healed.get("healed") and meta_path:
        save_meta(meta_path, meta)

    return {
        "mode": mode,
        "entered_at": entered,
        "reason": reason,
        "config": {
            "failure_rate_threshold": 0.3,
            "failure_count_threshold": 5,
            "recovery_consecutive_clean": 5,
            "auto_heal_hours": 168,
        },
    }


def evaluate_quiet_degradation_state(meta, now=None):
    """Expose quiet degradation assessment from persisted quality gate telemetry."""
    qgs = meta.get("quality_gate_state", {})
    samples = qgs.get("archive_rate_history", [])
    decay_config = meta.get("decay_config", {})
    quiet_config = decay_config.get("quiet_degradation", {}) if isinstance(decay_config, dict) else {}
    baseline_factor = decay_config.get("relative_baseline_factor", 1.5) if isinstance(decay_config, dict) else 1.5
    if "relative_baseline_factor" not in quiet_config:
        quiet_config = dict(quiet_config)
        quiet_config["relative_baseline_factor"] = baseline_factor
    return evaluate_quiet_degradation(
        samples,
        config=quiet_config,
        now=now,
        seed_last_updated_ts=qgs.get("seed_last_updated_ts"),
    )


def cmd_force_normal(meta_path, workspace, reason):
    """Manually force gate back to NORMAL state."""
    meta = load_normalized_meta(meta_path, persist=True)
    gate_state = get_gate_state(meta)
    prev = gate_state["state"]

    if prev == STATE_NORMAL:
        print("Already in NORMAL state.")
        return

    new_state, switched, info = transition_state(gate_state, "force_normal", reason=reason)

    # Record manual override for beta correction (before save so it persists)
    new_state.setdefault("manual_overrides", []).append({
        "from": prev,
        "timestamp": _now_iso(),
        "reason": reason,
    })

    save_gate_state(meta_path, meta, new_state)

    print(f"🔄 Force-normal: {prev} → NORMAL")
    print(f"  Reason: {reason or 'manual'}")
    print(f"  Anomaly count reset: 0")
    print(f"  Failure rate reset: 0.0")

    # Auto-flush L2 queue when leaving CRITICAL state
    if prev == STATE_CRITICAL:
        flush_result = flush_queue(meta_path, "force_normal")
        if flush_result.get("flushed", 0) > 0:
            print(f"  🚰 Auto-flushed {flush_result['flushed']} queued writes")
        elif flush_result.get("failed", 0) > 0:
            print(f"  ⚠️ {flush_result['failed']} queued writes failed to replay")


def cmd_intervention(meta_path, workspace, action):
    """Simulate intervention level calculation for a given action."""
    meta = load_normalized_meta(meta_path, persist=True)
    gate_state = get_gate_state(meta)

    print(f"🎯 Intervention Level Simulation")
    print(f"  Gate state: {gate_state['state']}")
    print(f"  Anomaly count: {gate_state['anomaly_count']}")
    print(f"  Action: {action}")
    print()

    level, notify_needed, should_block = compute_intervention_level(gate_state, action, meta)

    icons = {
        INTERVENTION_L0_SILENT: "🟢",
        INTERVENTION_L1_NOTIFY: "🟡",
        INTERVENTION_L2_PAUSE: "🔴",
        INTERVENTION_L3_MANUAL: "🔴",
    }
    icon = icons.get(level, "❓")

    print(f"  {icon} Level: {level}")
    print(f"  Notification needed: {notify_needed}")
    print(f"  Should block: {should_block}")

    if level == INTERVENTION_L1_NOTIFY:
        # Simulate notification
        notification = intervention_notify(level, gate_state, f"Simulated: {action}", meta_path)
        print(f"  📝 Notification logged to intervention_log[]")


# ─── v0.4.5: Health Checks ──────────────────────────────────

# Thresholds for health check alerts
INBOX_BACKLOG_WARNING = 10      # _inbox entries above this → warning
INBOX_BACKLOG_CRITICAL = 30     # _inbox entries above this → critical
NEEDS_REVIEW_TIMEOUT_DAYS = 7    # default timeout for needs_review
ROUTING_CONCENTRATION_MAX = 0.8  # >80% same category → anomaly
CONFLICT_RATE_WARNING = 0.02     # >2% → L2 warning
CONFLICT_RATE_CRITICAL = 0.05    # >5% → L3 + pause auto-write


def check_inbox_backlog(meta):
    """Check _inbox and needs_review status.

    Returns:
        dict: {status, inbox_count, needs_review_count, overdue_count,
               resolution_rate, alerts}
    """
    now = datetime.now(CST)
    memories = meta.get("memories", [])

    inbox_count = 0
    needs_review_count = 0
    overdue_count = 0
    total_inbox_historical = 0
    resolved_count = 0

    for mem in memories:
        if mem.get("status") == "_inbox":
            inbox_count += 1
        if mem.get("needs_review"):
            needs_review_count += 1
            # Check timeout
            since = mem.get("needs_review_since")
            if since:
                try:
                    dt = datetime.fromisoformat(since)
                    timeout_days = mem.get("needs_review_timeout", NEEDS_REVIEW_TIMEOUT_DAYS)
                    timeout_str = str(timeout_days)
                    # Handle "7d" format
                    if timeout_str.endswith("d"):
                        timeout_val = int(timeout_str[:-1])
                    else:
                        timeout_val = int(float(timeout_str))
                    if (now - dt).total_seconds() / 86400 > timeout_val:
                        overdue_count += 1
                except (ValueError, TypeError):
                    pass

        # Track resolution rate from status history
        if mem.get("status") in ("active", "archived"):
            classification = mem.get("classification", {})
            if isinstance(classification, dict) and "reviewed" in classification:
                total_inbox_historical += 1
                if classification["reviewed"]:
                    resolved_count += 1

    resolution_rate = (resolved_count / total_inbox_historical) if total_inbox_historical > 0 else None

    alerts = []
    status = "healthy"

    if inbox_count >= INBOX_BACKLOG_CRITICAL:
        alerts.append(f"critical:inbox_backlog:{inbox_count} (≥{INBOX_BACKLOG_CRITICAL})")
        status = "critical"
    elif inbox_count >= INBOX_BACKLOG_WARNING:
        alerts.append(f"warning:inbox_backlog:{inbox_count} (≥{INBOX_BACKLOG_WARNING})")
        if status == "healthy":
            status = "warning"

    if overdue_count > 0:
        alerts.append(f"warning:needs_review_overdue:{overdue_count}")
        if status == "healthy":
            status = "warning"

    return {
        "status": status,
        "inbox_count": inbox_count,
        "needs_review_count": needs_review_count,
        "overdue_count": overdue_count,
        "resolution_rate": resolution_rate,
        "alerts": alerts,
    }


def check_routing_health(meta):
    """Check routing decision distribution for anomalies.

    Returns:
        dict: {status, total_routes, category_distribution,
               concentration_ratio, alerts}
    """
    routing_log = meta.get("routing_log", [])
    if not routing_log:
        return {
            "status": "healthy",
            "total_routes": 0,
            "category_distribution": {},
            "concentration_ratio": 0.0,
            "alerts": ["info:no_routing_data"],
        }

    # Count category selections from recent routing log
    category_counts = {}
    for entry in routing_log:
        for tag, score in entry.get("selected", []):
            category_counts[tag] = category_counts.get(tag, 0) + 1

    total = sum(category_counts.values())
    if total == 0:
        return {
            "status": "healthy",
            "total_routes": 0,
            "category_distribution": {},
            "concentration_ratio": 0.0,
            "alerts": ["info:no_routing_selections"],
        }

    # Compute concentration: max single category / total
    max_cat = max(category_counts.values())
    concentration = max_cat / total

    alerts = []
    status = "healthy"

    if concentration > ROUTING_CONCENTRATION_MAX:
        top_tag = max(category_counts, key=category_counts.get)
        alerts.append(f"warning:routing_concentration:{concentration:.1%} in '{top_tag}' "
                      f"(threshold {ROUTING_CONCENTRATION_MAX:.0%})")
        status = "warning"

    return {
        "status": status,
        "total_routes": total,
        "category_distribution": dict(sorted(category_counts.items(),
                                              key=lambda x: x[1], reverse=True)),
        "concentration_ratio": round(concentration, 4),
        "alerts": alerts,
    }


def check_conflict_rate(meta):
    """Check write conflict rate from conflict_log.

    Returns:
        dict: {status, total_writes, total_conflicts, conflict_rate,
               alerts}
    """
    now = datetime.now(CST)

    # Count conflicts from last 24h
    conflict_log = meta.get("conflict_log", [])
    recent_conflicts = 0
    for entry in conflict_log:
        ts = entry.get("timestamp", "")
        if ts:
            try:
                dt = datetime.fromisoformat(ts)
                if (now - dt).total_seconds() < 86400:
                    recent_conflicts += 1
            except (ValueError, TypeError):
                pass

    # Count writes from last 24h
    gate_state = meta.get("quality_gate_state", {})
    write_counters = gate_state.get("write_counters", {})
    total_writes_24h = write_counters.get("total_writes_24h", 0)

    # Bug fix: total_writes_24h is never populated, so conflict_rate is always 0.
    # Return healthy with hint when no write data is available.
    if total_writes_24h == 0:
        return {
            "status": "healthy",
            "total_writes_24h": 0,
            "total_conflicts_24h": recent_conflicts,
            "conflict_rate": 0.0,
            "alerts": ["info:no_write_data"] if recent_conflicts == 0 else [],
        }

    conflict_rate = (recent_conflicts / total_writes_24h) if total_writes_24h > 0 else 0.0

    alerts = []
    status = "healthy"

    if conflict_rate >= CONFLICT_RATE_CRITICAL:
        alerts.append(f"critical:conflict_rate:{conflict_rate:.1%} "
                      f"({recent_conflicts}/{total_writes_24h} in 24h, "
                      f"≥{CONFLICT_RATE_CRITICAL:.0%} → pause auto-write)")
        status = "critical"
    elif conflict_rate >= CONFLICT_RATE_WARNING:
        alerts.append(f"warning:conflict_rate:{conflict_rate:.1%} "
                      f"({recent_conflicts}/{total_writes_24h} in 24h)")
        if status == "healthy":
            status = "warning"

    return {
        "status": status,
        "total_writes_24h": total_writes_24h,
        "total_conflicts_24h": recent_conflicts,
        "conflict_rate": round(conflict_rate, 4),
        "alerts": alerts,
    }


def run_health_checks(meta):
    """Run all v0.4.5 health checks.

    Returns:
        dict: {inbox, routing, conflicts, overall_status}
    """
    inbox = check_inbox_backlog(meta)
    routing = check_routing_health(meta)
    conflicts = check_conflict_rate(meta)

    # Overall status = worst of all
    statuses = [inbox["status"], routing["status"], conflicts["status"]]
    if "critical" in statuses:
        overall = "critical"
    elif "warning" in statuses:
        overall = "warning"
    else:
        overall = "healthy"

    # Filter: only warning/critical alerts, not info
    all_alerts = [a for a in (inbox["alerts"] + routing["alerts"] + conflicts["alerts"])
                  if not a.startswith("info:")]

    return {
        "inbox": inbox,
        "routing": routing,
        "conflicts": conflicts,
        "overall_status": overall,
        "alert_count": len(all_alerts),
        "alerts": all_alerts,
        "checked_at": _now_iso(),
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="memory-guardian quality gate (v0.4.1 4-state)")
    p.add_argument("command", choices=["check", "status", "record", "force-normal", "intervention",
                                       "queue-status", "queue-flush", "queue-check", "auto-check"],
                   help="Command")
    p.add_argument("--content", default=None, help="Content to check (for check command)")
    p.add_argument("--workspace", default=None, help="Workspace root path")
    p.add_argument("--meta", default=None, help="Path to meta.json")
    p.add_argument("--pass-check", action="store_true", help="Record a pass")
    p.add_argument("--fail-check", action="store_true", help="Record a fail")
    p.add_argument("--reason", default="", help="Reason for record/force-normal/flush")
    p.add_argument("--action", default="ingest", help="Write action for intervention command (e.g., ingest/delete/modify)")
    args = p.parse_args()

    workspace = args.workspace or os.environ.get(
        "OPENCLAW_WORKSPACE", os.path.expanduser("~/workspace/agent/workspace")
    )
    meta_path = args.meta or os.path.join(workspace, "memory", "meta.json")
    telemetry_meta = load_normalized_meta(meta_path, persist=True) if os.path.exists(meta_path) else {"memories": []}
    telemetry_input_count = len(telemetry_meta.get("memories", []))

    if args.command == "check":
        cmd_check(args.content, meta_path, workspace)
    elif args.command == "status":
        cmd_status(meta_path, workspace)
    elif args.command == "record":
        if not args.pass_check and not args.fail_check:
            print("Error: --pass-check or --fail-check required")
            sys.exit(1)
        cmd_record(meta_path, workspace, args.pass_check, args.reason)
    elif args.command == "force-normal":
        cmd_force_normal(meta_path, workspace, args.reason)
    elif args.command == "intervention":
        cmd_intervention(meta_path, workspace, args.action)
    elif args.command == "queue-status":
        meta = load_normalized_meta(meta_path, persist=True)
        queue = meta.get("l2_write_queue", [])
        gate = meta.get("quality_gate_state", {})
        l2_cfg = get_l2_config(meta)
        pending = [e for e in queue if e.get("status") == "pending"]
        print(f"📋 L2 Write Queue Status")
        print(f"  Pending: {len(pending)} / {l2_cfg['queue_cap']}")
        print(f"  Total entries: {len(queue)}")
        entered = gate.get("l2_entered_at")
        if entered:
            try:
                elapsed = (datetime.now(CST) - datetime.fromisoformat(entered)).total_seconds() / 60
                remaining = max(0, l2_cfg["timeout_minutes"] - elapsed)
                print(f"  L2 entered: {entered[:16]} ({elapsed:.0f}min ago)")
                print(f"  Auto-flush in: {remaining:.0f}min")
            except (ValueError, TypeError):
                pass
        else:
            print(f"  L2 not active")
        if pending:
            print(f"\n  Queued writes:")
            for e in pending[-5:]:
                print(f"    [{e.get('id','?')[:20]}] {e.get('action','?')} — {(e.get('reason','') or '')[:50]}")
    elif args.command == "queue-flush":
        result = flush_queue(meta_path, args.reason or "manual_flush")
        print(f"🚰 Queue flushed: {result['flushed']} writes ({result['reason']})")
    elif args.command == "queue-check":
        result = check_l2_timeout(meta_path)
        if result["timed_out"]:
            print(f"L2 timeout: auto-flushed {result['flushed']} writes ({result['elapsed_minutes']}min)")
        else:
            meta = load_normalized_meta(meta_path, persist=True)
            l2_cfg = get_l2_config(meta)
            print(f"L2 active, {result['elapsed_minutes']}min / {l2_cfg['timeout_minutes']}min")

    elif args.command == "auto-check":
        meta = load_normalized_meta(meta_path, persist=True)
        gate_state = get_gate_state(meta)
        new_state, switched, info = transition_state(gate_state, "auto_check")
        if switched:
            save_gate_state(meta_path, meta, new_state)
            print(f"State change: {info}")
        else:
            print(f"No state change needed (current: {gate_state['state']})")
            if gate_state["state"] == STATE_WARNING:
                hours = _hours_since(gate_state.get("state_entered_at"))
                print(f"  WARNING for {hours:.1f}h / {WARNING_CRITICAL_HOURS}h threshold")
                print(f"  Failure rate: {gate_state['failure_rate']:.2%} / {WARNING_FAILURE_RATE:.0%}")

    record_module_run(
        workspace,
        "quality_gate",
        input_count=telemetry_input_count,
        output_count=telemetry_input_count,
    )
