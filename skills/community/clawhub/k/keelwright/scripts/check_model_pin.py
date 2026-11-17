#!/usr/bin/env python3
# Copyright (c) 2026 ratingtesting — MIT-0 (see LICENSE). Free to use/modify/redistribute, no attribution required.
"""check_model_pin.py — verify the running model matches the pinned run contract (T16, v1.8.0).

WHY: R9 (model-version drift) is a DISCIPLINE, not an enforced gate. keelwright records the
model but cannot detect a provider silently swapping it mid-run. This script makes the pin
checkable: a loop driver passes the model string it is actually using; the script compares it
against `model-pin.json` and exits non-zero on drift. The agent then escalates instead of
trusting an unverified model.

USAGE:
  python check_model_pin.py --model "nous/tencent-hy3:free"
  python check_model_pin.py --model "nous/tencent-hy3:free" --role architect
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PIN_FILE = os.path.join(HERE, "..", "model-pin.json")


def load_pin() -> dict:
    try:
        with open(PIN_FILE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, help="model string actually in use")
    ap.add_argument("--role", default=None, help="optional role key to look up in model-pin.json")
    args = ap.parse_args()

    pin = load_pin()
    allowed = pin.get("allowed_models", [])
    role_pin = None
    if args.role and isinstance(pin.get("roles"), dict):
        role_pin = pin["roles"].get(args.role)

    if role_pin and args.model != role_pin:
        print(f"MODEL-PIN DRIFT: role '{args.role}' pinned to '{role_pin}', got '{args.model}'. Escalate.")
        return 1
    if allowed and args.model not in allowed:
        print(f"MODEL-PIN DRIFT: '{args.model}' not in allowed_models {allowed}. Escalate.")
        return 1
    print(f"MODEL-PIN OK: '{args.model}' matches contract.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
