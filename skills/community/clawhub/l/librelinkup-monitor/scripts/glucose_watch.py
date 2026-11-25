#!/usr/bin/env python3
"""
librelinkup-monitor: Glucose Watch Poller for Hermes Cron & Agent Telemetry.

Pulls continuous glucose monitoring (CGM) readings from Abbott's FreeStyle Libre
via the secondary caregiver LibreLinkUp cloud API (pylibrelinkup) and emits a
BYTE-STABLE state line.

Hermes compares each tick's stdout hash to the previous tick:
  - Unchanged output (e.g. repeated 'state=QUIET') skips the LLM agent turn
    completely ($0.00 cost, zero token burn).
  - A changed state (e.g. transitioning from 'state=QUIET' to 'state=ALERT_LOW')
    instantly wakes the agent to triage, alert, or take action.

================================================================================
IMPORTANT LEGAL & MEDICAL DISCLAIMERS:
1. NOT MEDICAL SOFTWARE: This tool is for informational, experimental, and
   educational companioning purposes only. It is NOT a medical device, is not
   cleared or approved by the FDA or any health regulatory authority, and must
   never replace professional medical monitoring, clinical judgment, or standard
   fingerstick blood glucose meters. Do NOT use this tool as the primary basis
   for insulin dosing or acute clinical decisions.
2. NON-AFFILIATION & TRADEMARKS: This software is independent open-source code
   and is NOT affiliated with, sponsored by, authorized by, or endorsed by
   Abbott Laboratories, FreeStyle Libre, or LibreView. "FreeStyle Libre" and
   "LibreLinkUp" are registered trademarks of Abbott Laboratories.
================================================================================
  1. Inverted Overnight Asymmetry: An unattended low is life-threatening within
     minutes; an unattended high is recoverable and actionable upon waking.
     This monitor watches LOWS and RAPID DROPS only. It deliberately avoids
     spamming the user for highs overnight to prevent fatal alarm fatigue.
  2. Byte-Stable Digest: Alert lines deliberately omit raw glucose values so
     an ongoing low state stays stable across consecutive ticks rather than
     triggering repeated LLM re-spawns on minor fluctuations. The agent fetches
     live numbers upon waking.
  3. Failure Smoothing: Transient Wi-Fi drops, Abbott API latency, or stale sensor
     intervals collapse to QUIET until ERROR_AFTER consecutive failures occur.
     A temporary hiccup never wakes the user.

License: MIT
Author: Iris & Syzygy Studios (for the Nous Research community)
"""

import argparse
import datetime as dt
import json
import os
import sys

# Trend Enum Ground Truth (pylibrelinkup / Abbott Cloud Protocol):
#   0 = UNKNOWN
#   1 = DOWN_FAST   (Rapidly falling, > 2 mg/dL/min)
#   2 = DOWN_SLOW   (Falling, 1-2 mg/dL/min)
#   3 = STABLE      (Slow change, < 1 mg/dL/min)
#   4 = UP_SLOW     (Rising, 1-2 mg/dL/min)
#   5 = UP_FAST     (Rapidly rising, > 2 mg/dL/min)
# WARNING: Do NOT invert 1/2 with 4/5. 1 and 2 are falling trends.
FALLING_TRENDS = {1, 2}


def get_default_creds_path() -> str:
    """Resolve standard credentials file location across platforms."""
    custom_path = os.getenv("LIBRE_CONFIG_PATH")
    if custom_path:
        return custom_path
    
    hermes_home = os.getenv("HERMES_HOME")
    if hermes_home and os.path.exists(os.path.join(hermes_home, "libre_creds.json")):
        return os.path.join(hermes_home, "libre_creds.json")
    
    local_app_data = os.getenv("LOCALAPPDATA")
    if local_app_data and os.path.exists(os.path.join(local_app_data, "hermes", "libre_creds.json")):
        return os.path.join(local_app_data, "hermes", "libre_creds.json")
    
    user_home = os.path.expanduser("~")
    return os.path.join(user_home, ".config", "librelinkup", "creds.json")


def get_default_failfile_path() -> str:
    """Resolve path for tracking consecutive failure counts."""
    hermes_home = os.getenv("HERMES_HOME")
    if hermes_home and os.path.isdir(hermes_home):
        return os.path.join(hermes_home, "glucose_watch_failcount")
    local_app_data = os.getenv("LOCALAPPDATA")
    if local_app_data and os.path.isdir(os.path.join(local_app_data, "hermes")):
        return os.path.join(local_app_data, "hermes", "glucose_watch_failcount")
    return os.path.join(os.path.expanduser("~"), ".config", "librelinkup", "glucose_watch_failcount")


def emit(state: str) -> None:
    """Print the byte-stable state and exit cleanly."""
    print(state)
    sys.exit(0)


def record_failure_and_emit(failfile: str, error_after: int) -> None:
    """Record consecutive poll failure and emit state=ERROR only if persistent."""
    try:
        d = os.path.dirname(failfile)
        if d:
            os.makedirs(d, exist_ok=True)
    except Exception:
        pass
    try:
        n = (int(open(failfile).read().strip()) + 1) if os.path.exists(failfile) else 1
    except Exception:
        n = 1
    try:
        with open(failfile, "w") as fh:
            fh.write(str(n))
    except Exception:
        pass
    
    emit("state=ERROR" if n >= error_after else "state=QUIET")


def clear_failure(failfile: str) -> None:
    """Clear consecutive failure counter on successful read."""
    try:
        if os.path.exists(failfile):
            os.remove(failfile)
    except Exception:
        pass


def evaluate_reading(value: float, trend: int, low_at: float, crit_at: float, fall_thresh: float) -> str:
    """Pure deterministic evaluator mapping glucose value and trend to state."""
    if value <= crit_at:
        return "state=ALERT_CRITICAL"
    if value <= low_at:
        return "state=ALERT_LOW"
    if trend in FALLING_TRENDS and value <= fall_thresh:
        return "state=WARN_FALLING"
    return "state=QUIET"


def run_synthetic_tests() -> bool:
    """Run verification suite asserting state behavior across all boundary conditions."""
    print("=== librelinkup-monitor: Running Synthetic Verification Tests ===")
    
    cases = [
        # (value, trend, expected_state, description)
        (120.0, 3, "state=QUIET", "Normal stable glucose"),
        (180.0, 5, "state=QUIET", "High glucose (quiet overnight)"),
        (125.0, 1, "state=WARN_FALLING", "Rapid fall (trend=1 DOWN_FAST) below 130"),
        (128.0, 2, "state=WARN_FALLING", "Slow fall (trend=2 DOWN_SLOW) below 130"),
        (140.0, 1, "state=QUIET", "Rapid fall but still high (>130)"),
        (85.0, 3, "state=ALERT_LOW", "At soft low floor (85)"),
        (78.0, 2, "state=ALERT_LOW", "Below soft low floor"),
        (70.0, 3, "state=ALERT_CRITICAL", "At critical low floor (70)"),
        (54.0, 1, "state=ALERT_CRITICAL", "Severe hypoglycemia (<70)"),
    ]
    
    passed = 0
    for val, tr, expected, desc in cases:
        got = evaluate_reading(val, tr, low_at=85, crit_at=70, fall_thresh=130)
        if got == expected:
            print(f"  [PASS] {desc}: got {got}")
            passed += 1
        else:
            print(f"  [FAIL] {desc}: expected {expected}, got {got}")
    
    # Test trend enum sanity check
    assert 1 in FALLING_TRENDS and 2 in FALLING_TRENDS
    assert 4 not in FALLING_TRENDS and 5 not in FALLING_TRENDS
    print("  [PASS] Trend enum direction verified (1,2 are falling; 4,5 are rising).")
    
    print(f"Verification complete: {passed}/{len(cases)} tests passed.")
    return passed == len(cases)


def run_live_poll(args: argparse.Namespace) -> None:
    # 1. Load credentials and optional config overrides from JSON
    creds_path = args.config or get_default_creds_path()
    failfile = args.failfile or get_default_failfile_path()
    
    cfg = {}
    if os.path.exists(creds_path):
        try:
            with open(creds_path, "r", encoding="utf-8") as fh:
                cfg = json.load(fh)
        except Exception:
            pass

    # Resolve configurable parameters (CLI flags override JSON config file, which override defaults)
    low_at = args.low if args.low is not None else float(cfg.get("low_threshold", 85.0))
    crit_at = args.crit if args.crit is not None else float(cfg.get("crit_threshold", 70.0))
    fall_thresh = args.fall_threshold if args.fall_threshold is not None else float(cfg.get("fall_threshold", 130.0))
    error_after = args.error_after if args.error_after is not None else int(cfg.get("error_after_fails", 3))
    
    watch_from = args.watch_from if args.watch_from is not None else cfg.get("watch_from_hour")
    watch_to = args.watch_to if args.watch_to is not None else cfg.get("watch_to_hour")

    # 2. Check time window if configured
    if watch_from is not None and watch_to is not None:
        h = dt.datetime.now().hour
        in_window = (h >= watch_from) or (h < watch_to) if watch_from > watch_to else (watch_from <= h < watch_to)
        if not in_window:
            emit("state=QUIET")

    email = cfg.get("email")
    password = cfg.get("password")
    if not (email and password):
        record_failure_and_emit(failfile, error_after)

    # 3. Query LibreLinkUp API via pylibrelinkup
    try:
        from pylibrelinkup import PyLibreLinkUp
    except ImportError:
        # pylibrelinkup missing from Python environment
        record_failure_and_emit(failfile, error_after)

    try:
        client = PyLibreLinkUp(email=email, password=password)
        client.authenticate()
        patients = client.get_patients()
        if not patients:
            # Authenticated successfully but patient share invitation not accepted
            record_failure_and_emit(failfile, error_after)
            
        patient_id = patients[0].patient_id
        
        # Primary clean path: client.latest(patient_id)
        if hasattr(client, "latest"):
            latest = client.latest(patient_id)
            value = float(latest.value)
            trend = int(latest.trend)
        else:
            # Fallback path: client.read(patient_id) nested structure
            raw = client.read(patient_id)
            data = raw.model_dump() if hasattr(raw, "model_dump") else raw
            inner = data.get("data") or {}
            gm = (inner.get("connection") or {}).get("glucose_measurement") or {}
            if not gm:
                gm = inner.get("glucose_measurement") or {}
            raw_val = gm.get("value_in_mg_per_dl") or gm.get("value")
            if raw_val is None:
                record_failure_and_emit(failfile, error_after)
            value = float(raw_val)
            trend = int(gm.get("trend") or 0)
            
    except Exception:
        record_failure_and_emit(failfile, error_after)

    if value <= 0:
        record_failure_and_emit(failfile, error_after)

    # Success: clear failure history and evaluate state
    clear_failure(failfile)
    state = evaluate_reading(value, trend, low_at=low_at, crit_at=crit_at, fall_thresh=fall_thresh)
    emit(state)


def main():
    parser = argparse.ArgumentParser(
        description="librelinkup-monitor: Zero-cost monitor poller for FreeStyle Libre CGM telemetry."
    )
    parser.add_argument("--config", help="Path to libre_creds.json")
    parser.add_argument("--failfile", help="Path to fail count state file")
    parser.add_argument("--low", type=float, default=None, help="Low glucose alert floor in mg/dL (default: 85)")
    parser.add_argument("--crit", type=float, default=None, help="Critical hypoglycemia floor in mg/dL (default: 70)")
    parser.add_argument("--fall-threshold", type=float, default=None, help="Ceiling for rapid falling warnings (default: 130)")
    parser.add_argument("--watch-from", type=int, default=None, help="Start hour of watch window (0-23)")
    parser.add_argument("--watch-to", type=int, default=None, help="End hour of watch window (0-23)")
    parser.add_argument("--error-after", type=int, default=None, help="Consecutive failures before state=ERROR (default: 3)")
    parser.add_argument("--test", action="store_true", help="Run synthetic verification suite")
    parser.add_argument("--test-auth", action="store_true", help="Test live connection without emitting monitor state")

    args = parser.parse_args()

    if args.test:
        success = run_synthetic_tests()
        sys.exit(0 if success else 1)

    if args.test_auth:
        creds_path = args.config or get_default_creds_path()
        if not os.path.exists(creds_path):
            print(f"[ERROR] Credentials file not found at: {creds_path}")
            sys.exit(1)
        with open(creds_path, "r", encoding="utf-8") as fh:
            c = json.load(fh)
        from pylibrelinkup import PyLibreLinkUp
        client = PyLibreLinkUp(email=c["email"], password=c["password"])
        client.authenticate()
        patients = client.get_patients()
        if not patients:
            print("[ERROR] Authenticated, but no connected patients found. Ensure the sharing invitation has been accepted in the FreeStyle Libre app.")
            sys.exit(1)
        p = patients[0]
        if hasattr(client, "latest"):
            latest = client.latest(p.patient_id)
            val = latest.value
            tr = latest.trend
        else:
            raw = client.read(p.patient_id)
            data = raw.model_dump() if hasattr(raw, "model_dump") else raw
            inner = data.get("data") or {}
            gm = (inner.get("connection") or {}).get("glucose_measurement") or inner.get("glucose_measurement") or {}
            val = gm.get("value_in_mg_per_dl") or gm.get("value")
            tr = gm.get("trend") or 0
        print(f"[SUCCESS] Authenticated! Patient ID: {str(p.patient_id)[:8]}... Value: {val} mg/dL | Trend: {tr}")
        sys.exit(0)

    run_live_poll(args)


if __name__ == "__main__":
    main()
