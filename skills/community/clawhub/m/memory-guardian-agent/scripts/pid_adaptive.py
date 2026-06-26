#!/usr/bin/env python3
"""pid_adaptive.py — PID 全量自适应控制器 (v0.4.2).

Full PID controller for memory threshold adjustment (leozhang + azha0).
Replaces the cold-start placeholder in memory_case_grow.py.

Design:
  P (比例): 当前偏差 → 吸收阈值调整
  I (积分): 累计偏差 → 趋势调整
  D (微分): 偏差变化率 → 快速响应

  threshold_adjust = Kp × error + Ki × integral + Kd × derivative

Features:
  - Per-scene-group PID parameters (scene_group → Kp/Ki/Kd)
  - Anti-oscillation: output limiting + dead zone
  - Error signal: L3 人工覆盖率 (neuro建议)
  - Health score integration (maste): ln(修正率+1)/ln(2)
  - Error recovery tracking (maste): separate PID for recovery mode

Usage:
  python3 pid_adaptive.py status --workspace /path
  python3 pid_adaptive.py compute --scene-group <name> --error <float> --workspace /path
  python3 pid_adaptive.py update --workspace /path [--dry-run]
  python3 pid_adaptive.py history --workspace /path
  python3 pid_adaptive.py reset --scene-group <name> --workspace /path
"""

import argparse
import json
import math
import os
import sys
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from mg_utils import load_meta, save_meta, _now_iso, CST


# ─── Constants ────────────────────────────────────────────────

# Default PID gains (conservative — will self-tune over time)
DEFAULT_KP = 0.1    # Proportional gain
DEFAULT_KI = 0.02   # Integral gain (low to prevent windup)
DEFAULT_KD = 0.05   # Derivative gain (damping)

# Safety limits
OUTPUT_LIMIT = 0.3      # Max single-step adjustment (±0.3)
DEAD_ZONE = 0.01        # Ignore errors smaller than this
INTEGRAL_LIMIT = 1.0    # Anti-windup cap on integral term
MAX_HISTORY = 100       # Keep last N error readings
PID_UPDATE_INTERVAL_H = 1  # Min hours between PID updates


# ─── PID Controller ───────────────────────────────────────────

class PIDController:
    """Per-scene-group PID controller with anti-oscillation.

    Tracks error history and computes output adjustment for thresholds.
    """

    def __init__(self, kp=DEFAULT_KP, ki=DEFAULT_KI, kd=DEFAULT_KD):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral = 0.0
        self.prev_error = None
        self.history = []  # [(timestamp, error), ...]

    def compute(self, error, now=None):
        """Compute PID output for a given error value.

        Args:
            error: float, current error (target - actual, positive = too few absorbed)
            now: str, ISO timestamp

        Returns:
            dict: {output, p_term, i_term, d_term, anti_oscillation_applied}
        """
        now = now or _now_iso()

        # NaN/Inf guard: prevent state pollution from invalid inputs
        if math.isnan(error) or math.isinf(error):
            return {"output": 0.0, "p_term": 0.0, "i_term": 0.0, "d_term": 0.0,
                    "anti_oscillation_applied": False, "dead_zone": False}

        # Dead zone: ignore tiny errors
        if abs(error) < DEAD_ZONE:
            return {"output": 0.0, "p_term": 0.0, "i_term": 0.0, "d_term": 0.0,
                    "anti_oscillation_applied": False, "dead_zone": True}

        # P term
        p_term = self.kp * error

        # I term (with anti-windup)
        self.integral += error
        self.integral = max(-INTEGRAL_LIMIT, min(INTEGRAL_LIMIT, self.integral))
        i_term = self.ki * self.integral

        # D term (rate of change, with individual limiting)
        d_term = 0.0
        if self.prev_error is not None:
            d_term = self.kd * (error - self.prev_error)
            d_term = max(-OUTPUT_LIMIT, min(OUTPUT_LIMIT, d_term))

        self.prev_error = error

        # Raw output
        raw_output = p_term + i_term + d_term

        # Anti-oscillation: clamp output
        anti_osc = False
        if abs(raw_output) > OUTPUT_LIMIT:
            raw_output = math.copysign(OUTPUT_LIMIT, raw_output)
            anti_osc = True

        # Track history
        self.history.append((now, error, raw_output))
        if len(self.history) > MAX_HISTORY:
            self.history = self.history[-MAX_HISTORY:]

        return {
            "output": raw_output,
            "p_term": p_term,
            "i_term": i_term,
            "d_term": d_term,
            "anti_oscillation_applied": anti_osc,
            "dead_zone": False,
        }

    def reset(self):
        """Reset controller state (keep gains, clear history)."""
        self.integral = 0.0
        self.prev_error = None
        self.history = []

    def to_dict(self):
        """Serialize controller state."""
        return {
            "kp": self.kp,
            "ki": self.ki,
            "kd": self.kd,
            "integral": self.integral,
            "prev_error": self.prev_error,
            "history": self.history[-20:],  # Keep last 20 for serialization
            "history_count": len(self.history),
        }

    @classmethod
    def from_dict(cls, data):
        """Deserialize controller state."""
        ctrl = cls(
            kp=data.get("kp", DEFAULT_KP),
            ki=data.get("ki", DEFAULT_KI),
            kd=data.get("kd", DEFAULT_KD),
        )
        ctrl.integral = data.get("integral", 0.0)
        ctrl.prev_error = data.get("prev_error")
        ctrl.history = data.get("history", [])
        return ctrl


# ─── Scene Group Management ───────────────────────────────────

def get_pid_state(meta):
    """Load PID state from meta.json.

    Returns:
        dict: PID state structure
    """
    return meta.setdefault("pid_state", {
        "controllers": {},  # scene_group → PIDController dict
        "last_update": None,
        "scene_thresholds": {},  # scene_group → current threshold
        "recovery_pid": None,  # separate PID for error recovery (maste)
        "global_stats": {
            "total_adjustments": 0,
            "anti_oscillation_count": 0,
            "average_output": 0.0,
        },
    })


def get_or_create_controller(pid_state, scene_group, kp=None, ki=None, kd=None):
    """Get existing PID controller or create new one for scene group.

    Args:
        pid_state: dict, the pid_state from meta.json
        scene_group: str, scene group name
        kp, ki, kd: optional custom gains

    Returns:
        PIDController
    """
    controllers = pid_state["controllers"]
    if scene_group in controllers:
        return PIDController.from_dict(controllers[scene_group])

    ctrl = PIDController(
        kp=kp or DEFAULT_KP,
        ki=ki or DEFAULT_KI,
        kd=kd or DEFAULT_KD,
    )
    controllers[scene_group] = ctrl.to_dict()
    return ctrl


def save_pid_state(meta_path, meta, pid_state):
    """Save PID state back to meta.json."""
    meta["pid_state"] = pid_state
    meta["pid_state"]["last_update"] = _now_iso()
    save_meta(meta_path, meta)


# ─── Error Signal Computation ─────────────────────────────────

def compute_error_signal(meta, scene_group=None):
    """Compute error signal for PID controller.

    Error = target_L3_rate - actual_L3_rate (neuro's recommendation)

    Also incorporates:
    - Health score deviation (maste): ln(修正率+1)/ln(2)
    - Quality gate state factor

    Args:
        meta: dict, meta.json content
        scene_group: str, optional specific scene group

    Returns:
        dict: {error, components: {l3_coverage, health_deviation, gate_factor}}
    """
    pid_state = get_pid_state(meta)
    gate = meta.get("quality_gate_state", {})
    gate_state = gate.get("state", "NORMAL")
    memories = meta.get("memories", [])

    # L3 coverage rate
    total_l3 = len(meta.get("l3_confirmations", []))
    confirmed = len([c for c in meta.get("l3_confirmations", []) if c["status"] == "confirmed"])
    degraded = len([c for c in meta.get("l3_confirmations", []) if c["status"] == "degraded"])

    # No L3 data → no adjustment signal (avoid persistent large error)
    if total_l3 == 0:
        l3_rate = 0.0
        l3_error = 0.0
    else:
        l3_rate = (confirmed + degraded) / max(total_l3, 1)
        target_l3_rate = 0.85  # 85% of L3 should be resolved (confirmed or degraded)
        l3_error = target_l3_rate - l3_rate

    target_l3_rate = 0.85  # target reference (for reporting even when no data)

    # Health score deviation (maste's formula)
    total_writes = gate.get("total_writes", 0)
    total_failures = gate.get("total_failures", 0)
    total_all = total_writes + total_failures
    correction_rate = total_failures / max(total_all, 1)
    health_score = math.log(correction_rate + 1) / math.log(2)
    # Target health: <0.3 (low correction rate = healthy system)
    health_deviation = health_score - 0.3

    # Gate state factor
    gate_factor = 0.0
    if gate_state == "WARNING":
        gate_factor = 0.1
    elif gate_state == "CRITICAL":
        gate_factor = 0.3
    elif gate_state == "RECOVERING":
        gate_factor = -0.05  # Slight negative during recovery (system healing)

    # Task 8: the PID error signal should be the L3 coverage gap itself.
    # Health and gate state remain as advisory context for observability.
    error_signal = l3_error

    return {
        "error": error_signal,
        "error_signal": error_signal,
        "components": {
            "l3_coverage": {"rate": l3_rate, "target": target_l3_rate, "error": l3_error},
            "health_deviation": {"score": health_score, "deviation": health_deviation},
            "gate_factor": {"state": gate_state, "factor": gate_factor},
        },
    }


# ─── Threshold Update ─────────────────────────────────────────

def update_thresholds(meta_path, dry_run=False):
    """Run PID computation and update scene group thresholds.

    Returns:
        dict: update summary
    """
    now = _now_iso()
    meta = load_meta(meta_path)
    pid_state = get_pid_state(meta)

    # Check update interval
    last_update = pid_state.get("last_update")
    if last_update:
        try:
            last_dt = datetime.fromisoformat(last_update)
            elapsed_h = (datetime.now(CST) - last_dt).total_seconds() / 3600
            if elapsed_h < PID_UPDATE_INTERVAL_H:
                return {
                    "status": "skipped",
                    "reason": f"Last update {elapsed_h:.1f}h ago (min {PID_UPDATE_INTERVAL_H}h)",
                }
        except (ValueError, TypeError):
            pass

    # Compute error signal
    error_data = compute_error_signal(meta)
    error = error_data["error"]

    # Get scene groups from memories
    memories = meta.get("memories", [])
    scene_groups = set()
    for m in memories:
        sg = m.get("memory_type", "absorb")
        if m.get("status") == "active":
            scene_groups.add(sg)

    updated = 0
    adjustments = []
    controllers_to_save = {}  # Track modified controllers

    for sg in scene_groups:
        ctrl = get_or_create_controller(pid_state, sg)
        result = ctrl.compute(error, now)

        # Always save controller state (even if output is tiny — compute() mutated integral/prev_error/history)
        controllers_to_save[sg] = ctrl

        if abs(result["output"]) < 0.001:
            continue

        # Get current threshold
        current = pid_state["scene_thresholds"].get(sg)
        if current is None:
            # Default thresholds by type
            defaults = {"static": 0.1, "derive": 0.3, "absorb": 0.5}
            current = defaults.get(sg, 0.5)

        new_threshold = current + result["output"]
        # Clamp to valid range [0.05, 0.95]
        new_threshold = max(0.05, min(0.95, new_threshold))

        adjustments.append({
            "scene_group": sg,
            "old": round(current, 4),
            "new": round(new_threshold, 4),
            "delta": round(result["output"], 4),
            "anti_oscillation": result["anti_oscillation_applied"],
        })

        pid_state["scene_thresholds"][sg] = new_threshold
        updated += 1

        # Save controller state immediately after compute (not re-creating from dict)
        controllers_to_save[sg] = ctrl

    # Update global stats
    stats = pid_state["global_stats"]
    stats["total_adjustments"] += updated
    if adjustments:
        osc_count = sum(1 for a in adjustments if a["anti_oscillation"])
        stats["anti_oscillation_count"] += osc_count
        avg_output = sum(a["delta"] for a in adjustments) / len(adjustments)
        stats["average_output"] = round(avg_output, 4)

    # Save controllers (use the already-computed instances, not re-created from dict)
    for sg, ctrl in controllers_to_save.items():
        pid_state["controllers"][sg] = ctrl.to_dict()

    if not dry_run:
        save_pid_state(meta_path, meta, pid_state)

    return {
        "status": "updated" if updated > 0 else "no_change",
        "error": round(error, 4),
        "error_components": error_data["components"],
        "adjustments": adjustments,
        "updated_groups": updated,
        "dry_run": dry_run,
    }


# ─── CLI ─────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(description="PID 全量自适应控制器 v0.4.2")
    p.add_argument("--workspace", default=os.path.expanduser("~/workspace/agent/workspace"))
    p.add_argument("command",
                   choices=["status", "compute", "update", "history", "reset"],
                   help="Command to run")
    p.add_argument("--scene-group", default=None, help="Scene group name")
    p.add_argument("--error", type=float, default=None, help="Manual error value (for compute)")
    p.add_argument("--dry-run", action="store_true", help="Dry run mode")
    args = p.parse_args()

    meta_path = os.path.join(args.workspace, "memory", "meta.json")

    if args.command == "status":
        meta = load_meta(meta_path)
        pid_state = get_pid_state(meta)

        print(f"Last update: {pid_state.get('last_update', 'never')}")
        print(f"Total adjustments: {pid_state['global_stats']['total_adjustments']}")
        print(f"Anti-oscillation count: {pid_state['global_stats']['anti_oscillation_count']}")
        print(f"Avg output: {pid_state['global_stats']['average_output']}")
        print()

        print("Scene thresholds:")
        for sg, threshold in pid_state.get("scene_thresholds", {}).items():
            ctrl = pid_state["controllers"].get(sg, {})
            print(f"  {sg}: threshold={threshold:.4f} | Kp={ctrl.get('kp', DEFAULT_KP)} Ki={ctrl.get('ki', DEFAULT_KI)} Kd={ctrl.get('kd', DEFAULT_KD)}")

        print()
        error_data = compute_error_signal(meta)
        print(f"Current error signal: {error_data['error']:.4f}")
        print(f"  L3 coverage: {error_data['components']['l3_coverage']['rate']:.2%}")
        health = error_data['components']['health_deviation']
        print(f"  Health score: {health['score']:.4f} (deviation: {health['deviation']:.4f})")

    elif args.command == "compute":
        meta = load_meta(meta_path)
        sg = args.scene_group or "absorb"
        error = args.error

        if error is None:
            error_data = compute_error_signal(meta)
            error = error_data["error"]
            print(f"Auto-computed error signal: {error:.4f}")
            print(f"Components: {json.dumps(error_data['components'], indent=2, default=str)}")
        else:
            print(f"Manual error: {error}")

        pid_state = get_pid_state(meta)
        ctrl = get_or_create_controller(pid_state, sg)
        result = ctrl.compute(error)
        print(f"\nPID output for '{sg}': {result['output']:.4f}")
        print(f"  P: {result['p_term']:.4f} | I: {result['i_term']:.4f} | D: {result['d_term']:.4f}")
        if result['anti_oscillation_applied']:
            print("  ⚠️ Anti-oscillation applied (output clamped)")

    elif args.command == "update":
        result = update_thresholds(meta_path, args.dry_run)
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))

    elif args.command == "history":
        meta = load_meta(meta_path)
        pid_state = get_pid_state(meta)
        for sg, ctrl_data in pid_state.get("controllers", {}).items():
            history = ctrl_data.get("history", [])
            print(f"\n📊 {sg} ({len(history)} readings):")
            for ts, err, out in history[-10:]:
                print(f"  {ts[:16]} | error={err:+.4f} | output={out:+.4f}")

    elif args.command == "reset":
        if not args.scene_group:
            print("Error: --scene-group required for reset")
            sys.exit(1)
        meta = load_meta(meta_path)
        pid_state = get_pid_state(meta)
        ctrl = get_or_create_controller(pid_state, args.scene_group)
        ctrl.reset()
        pid_state["controllers"][args.scene_group] = ctrl.to_dict()
        save_pid_state(meta_path, meta, pid_state)
        print(f"Reset PID controller for '{args.scene_group}'")


if __name__ == "__main__":
    main()
