"""Explicit state transition helpers for quality gate anomaly modes."""

from __future__ import annotations

from datetime import datetime, timedelta

from mg_utils import CST, _now_iso


ANOMALY_MODE_NORMAL = "normal_decay"
ANOMALY_MODE_ANOMALY = "anomaly"
ANOMALY_MODE_ERROR_RECOVERY = "error_recovery"


def update_anomaly_mode_state(meta, gate_state, passed, trigger, now=None):
    """Advance anomaly mode using the three-state rules from the refactor plan."""
    now_iso = now or _now_iso()
    history = meta.get("quality_gate_state", {}).get("check_history", [])
    recent_10 = history[-10:] if len(history) >= 10 else history
    recent_failures = sum(1 for entry in recent_10 if not entry.get("passed", True))
    recent_failure_rate = recent_failures / max(len(recent_10), 1)
    consecutive_clean = gate_state.get("consecutive_clean", 0)
    current_mode = meta.get("anomaly_mode", ANOMALY_MODE_NORMAL)
    new_mode = current_mode
    reason = meta.get("anomaly_mode_reason", "")

    anomaly_count = meta.get("anomaly_count", 0)

    if current_mode == ANOMALY_MODE_NORMAL:
        if (recent_failure_rate >= 0.3
                and recent_failures >= 5):
            anomaly_count += 1
            if anomaly_count >= 2:
                new_mode = ANOMALY_MODE_ANOMALY
                reason = f"failure_rate={recent_failure_rate:.2f} failures={recent_failures}/10 anomaly_count={anomaly_count}"
        else:
            # Failure rate subsided — decay the counter
            anomaly_count = max(0, anomaly_count - 1)

    elif current_mode == ANOMALY_MODE_ANOMALY:
        if gate_state.get("state") == "CRITICAL":
            new_mode = ANOMALY_MODE_ERROR_RECOVERY
            reason = "CRITICAL state entered"
        elif passed and consecutive_clean >= 5 and gate_state.get("state") == "NORMAL":
            new_mode = ANOMALY_MODE_NORMAL
            anomaly_count = 0
            reason = ""

    elif current_mode == ANOMALY_MODE_ERROR_RECOVERY:
        if passed and gate_state.get("state") == "NORMAL" and consecutive_clean >= 5:
            new_mode = ANOMALY_MODE_NORMAL
            anomaly_count = 0
            reason = ""

    meta["anomaly_count"] = anomaly_count

    meta["anomaly_mode"] = new_mode
    if new_mode == ANOMALY_MODE_NORMAL:
        meta.pop("anomaly_mode_entered_at", None)
        meta.pop("anomaly_mode_reason", None)
    else:
        meta["anomaly_mode_entered_at"] = now_iso
        meta["anomaly_mode_reason"] = reason

    return {
        "mode": new_mode,
        "entered_at": meta.get("anomaly_mode_entered_at"),
        "reason": meta.get("anomaly_mode_reason", ""),
        "recent_failures": recent_failures,
        "recent_failure_rate": recent_failure_rate,
    }


def auto_heal_anomaly_mode(meta, now=None, auto_heal_hours=168):
    """Reset stale anomaly mode after a long clean period."""
    mode = meta.get("anomaly_mode", ANOMALY_MODE_NORMAL)
    entered = meta.get("anomaly_mode_entered_at")
    if mode not in (ANOMALY_MODE_ANOMALY, ANOMALY_MODE_ERROR_RECOVERY) or not entered:
        return {"healed": False, "mode": mode}

    current = now or datetime.now(CST)
    try:
        entered_dt = datetime.fromisoformat(entered)
    except (TypeError, ValueError):
        return {"healed": False, "mode": mode}

    if current - entered_dt <= timedelta(hours=auto_heal_hours):
        return {"healed": False, "mode": mode}

    history = meta.get("quality_gate_state", {}).get("check_history", [])
    recent_5 = history[-5:] if len(history) >= 5 else history
    if recent_5 and all(entry.get("passed", True) for entry in recent_5):
        meta["anomaly_mode"] = ANOMALY_MODE_NORMAL
        meta.pop("anomaly_mode_entered_at", None)
        meta.pop("anomaly_mode_reason", None)
        return {"healed": True, "mode": ANOMALY_MODE_NORMAL}

    return {"healed": False, "mode": mode}
