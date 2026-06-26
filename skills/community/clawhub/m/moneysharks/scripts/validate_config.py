#!/usr/bin/env python3
"""
Validate MoneySharks config.json.
Input (stdin JSON): config dict.
Output: {"ok": bool, "errors": [...], "warnings": [...]}
"""
import json
import sys

REQUIRED_FIELDS = [
    "mode",
    "allowed_symbols",
    "base_value_per_trade",
    "min_leverage",
    "max_leverage",
    "max_notional_per_trade",
    "max_total_exposure",
    "max_concurrent_positions",
    "max_daily_loss",
]

VALID_MODES = {"paper", "approval", "live", "autonomous_live"}


def main() -> int:
    config = json.load(sys.stdin)
    errors = []
    warnings = []

    # Required fields
    for field in REQUIRED_FIELDS:
        if field not in config:
            errors.append(f"missing required field: {field}")

    # Mode
    mode = config.get("mode")
    if mode and mode not in VALID_MODES:
        errors.append(f"invalid mode: {mode}. Must be one of {VALID_MODES}")

    # Autonomous live consent
    if mode == "autonomous_live" and not config.get("autonomous_live_consent"):
        errors.append("autonomous_live mode requires autonomous_live_consent=true")

    # Leverage bounds
    min_lev = config.get("min_leverage", 0)
    max_lev = config.get("max_leverage", 0)
    if min_lev <= 0:
        errors.append("min_leverage must be > 0")
    if max_lev <= 0:
        errors.append("max_leverage must be > 0")
    if min_lev > max_lev:
        errors.append("min_leverage must be <= max_leverage")
    if max_lev > 125:
        warnings.append("max_leverage > 125 is extremely high risk")
    elif max_lev > 20:
        warnings.append("max_leverage > 20 is high risk")

    # Notional vs exposure
    notional = config.get("max_notional_per_trade", 0)
    exposure = config.get("max_total_exposure", 0)
    if notional > exposure and exposure > 0:
        warnings.append("max_notional_per_trade > max_total_exposure — single trade could exceed total exposure limit")

    # Symbols
    symbols = config.get("allowed_symbols", [])
    if not symbols:
        errors.append("allowed_symbols must be a non-empty list")

    # Daily loss
    daily_loss = config.get("max_daily_loss", 0)
    if daily_loss <= 0:
        warnings.append("max_daily_loss not set or zero — no daily loss protection")

    # Risk per trade
    if "risk_pct_per_trade" not in config:
        warnings.append("risk_pct_per_trade not set — will default to 1% per trade")

    # Cron settings for autonomous_live
    if mode == "autonomous_live":
        cron = config.get("cron", {})
        if not cron.get("enabled"):
            warnings.append("cron.enabled=false in autonomous_live mode — agent won't run on schedule")
        scan_interval = cron.get("scan_interval_minutes", 5)
        if scan_interval < 1:
            warnings.append("cron.scan_interval_minutes < 1 — very high API usage risk")

    ok = len(errors) == 0
    print(json.dumps({"ok": ok, "errors": errors, "warnings": warnings}, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
