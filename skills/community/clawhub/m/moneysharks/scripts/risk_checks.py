#!/usr/bin/env python3
"""
Hard risk limit enforcement. All checks must pass before an order is placed.
Input (stdin JSON):
  {
    "daily_loss_hit": bool,
    "exposure_after_trade": float,
    "max_total_exposure": float,
    "notional": float,
    "max_notional_per_trade": float,
    "available_margin": float,
    "required_margin": float
  }
Output: {"ok": bool, "failures": [str, ...]}
"""
import json
import sys


def main() -> int:
    payload = json.load(sys.stdin)
    failures = []

    # Daily loss limit (always enforced)
    if payload.get("daily_loss_hit"):
        failures.append("daily_loss_hit")

    # Total exposure cap (only enforced if limit is set > 0)
    max_exposure = float(payload.get("max_total_exposure", 0))
    if max_exposure > 0 and float(payload.get("exposure_after_trade", 0)) > max_exposure:
        failures.append("max_total_exposure")

    # Per-trade notional cap (only enforced if limit is set > 0)
    max_notional = float(payload.get("max_notional_per_trade", 0))
    if max_notional > 0 and float(payload.get("notional", 0)) > max_notional:
        failures.append("max_notional_per_trade")

    # Margin availability
    available = float(payload.get("available_margin", 0))
    required = float(payload.get("required_margin", 0))
    if required > 0 and available < required:
        failures.append("insufficient_margin")

    # Zero quantity guard
    if float(payload.get("notional", 0)) <= 0:
        failures.append("zero_notional")

    print(json.dumps({"ok": not failures, "failures": failures}, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
