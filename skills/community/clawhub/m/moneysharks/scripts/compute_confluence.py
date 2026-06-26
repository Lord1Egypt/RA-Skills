#!/usr/bin/env python3
"""
Compute confluence score for a trade setup.
Input (stdin JSON):
  {
    "signal": "long"|"short"|"wait"|"hold"|"close",
    "features_1h": {...},
    "features_4h": {...},
    "min_reward_risk": float,
    "entry": float,
    "stop_loss": float,
    "take_profit": float,
    "max_concurrent_positions": int,
    "current_positions": int,
    "max_total_exposure": float,
    "current_exposure": float,
    "checks": {...}   ← optional override (legacy)
  }
Output:
  {
    "passed": [str, ...],
    "failed": [str, ...],
    "count": int,
    "total": int,
    "confidence": float
  }
"""
import json
import sys

ALL_CHECKS = [
    "trend_alignment",
    "momentum_confirmation",
    "volume_confirmation",
    "rsi_zone",
    "macd_alignment",
    "reward_risk_ok",
    "exposure_capacity_ok",
    "position_capacity_ok",
    "timeframe_confluence",
]


def derive_checks(payload: dict) -> dict:
    """Derive confluence checks from features and order parameters."""
    sig = payload.get("signal", "wait")
    f1h = payload.get("features_1h") or {}
    f4h = payload.get("features_4h") or f1h
    entry = float(payload.get("entry", 0) or 0)
    stop = float(payload.get("stop_loss", 0) or 0)
    target = float(payload.get("take_profit", 0) or 0)
    min_rr = float(payload.get("min_reward_risk", 1.5))
    max_pos = int(payload.get("max_concurrent_positions", 3))
    cur_pos = int(payload.get("current_positions", 0))
    max_exp = float(payload.get("max_total_exposure", 0) or 0)
    cur_exp = float(payload.get("current_exposure", 0) or 0)

    is_long = sig == "long"
    is_short = sig == "short"

    checks = {}

    # Trend alignment: 1H and 4H both agree
    t1h = f1h.get("trend", "neutral")
    t4h = f4h.get("trend", "neutral")
    if is_long:
        checks["trend_alignment"] = t1h == "up" and t4h in ("up", "neutral")
    elif is_short:
        checks["trend_alignment"] = t1h == "down" and t4h in ("down", "neutral")
    else:
        checks["trend_alignment"] = True  # irrelevant for wait/hold

    # Momentum
    m1h = f1h.get("momentum", "neutral")
    if is_long:
        checks["momentum_confirmation"] = m1h == "up"
    elif is_short:
        checks["momentum_confirmation"] = m1h == "down"
    else:
        checks["momentum_confirmation"] = True

    # Volume
    checks["volume_confirmation"] = float(f1h.get("volume_ratio", 0)) >= 0.75

    # RSI in the right zone
    rsi = f1h.get("rsi14")
    if rsi is not None:
        if is_long:
            checks["rsi_zone"] = 40 <= rsi <= 70
        elif is_short:
            checks["rsi_zone"] = 30 <= rsi <= 60
        else:
            checks["rsi_zone"] = True
    else:
        checks["rsi_zone"] = False

    # MACD alignment
    macd = f1h.get("macd")
    macd_sig = f1h.get("macd_signal")
    if macd is not None and macd_sig is not None:
        if is_long:
            checks["macd_alignment"] = macd > macd_sig
        elif is_short:
            checks["macd_alignment"] = macd < macd_sig
        else:
            checks["macd_alignment"] = True
    else:
        checks["macd_alignment"] = False

    # Reward:risk ratio
    if entry and stop and target:
        risk = abs(entry - stop)
        reward = abs(target - entry)
        checks["reward_risk_ok"] = reward >= risk * min_rr if risk > 0 else False
    else:
        checks["reward_risk_ok"] = False

    # Exposure capacity
    if max_exp > 0:
        checks["exposure_capacity_ok"] = cur_exp < max_exp * 0.90
    else:
        checks["exposure_capacity_ok"] = True

    # Position count capacity
    checks["position_capacity_ok"] = cur_pos < max_pos

    # Multi-timeframe confluence
    if is_long:
        checks["timeframe_confluence"] = t1h == "up" and t4h == "up"
    elif is_short:
        checks["timeframe_confluence"] = t1h == "down" and t4h == "down"
    else:
        checks["timeframe_confluence"] = True

    return checks


def main() -> int:
    payload = json.load(sys.stdin)
    # Allow manual override
    checks_override = payload.get("checks")
    if checks_override:
        checks = checks_override
    else:
        checks = derive_checks(payload)

    passed = [name for name in ALL_CHECKS if checks.get(name)]
    failed = [name for name in ALL_CHECKS if not checks.get(name)]
    confidence = len(passed) / len(ALL_CHECKS)

    print(json.dumps({
        "passed": passed,
        "failed": failed,
        "count": len(passed),
        "total": len(ALL_CHECKS),
        "confidence": confidence,
        "checks": checks,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
