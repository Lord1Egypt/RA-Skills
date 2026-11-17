#!/usr/bin/env python3
"""Single deterministic entry point for hua-personal-strategy v4.3.0 decisions."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from .decision_core import decide, finish, base_result
    from .policy_store import default_state_root, load_current, user_key
except ImportError:
    from decision_core import decide, finish, base_result
    from policy_store import default_state_root, load_current, user_key


def load_object(path: str) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("input JSON must be an object")
    return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="JSON containing context, cash, aiView, and optionally policy")
    parser.add_argument("--user-id", default=None, help="load the current policy for this HuahuaDaily user")
    parser.add_argument("--state-dir", default=None, help="override the investor policy state directory")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    payload: dict[str, Any] = {}
    try:
        payload = load_object(args.input)
        if not isinstance(payload.get("policy"), dict) and args.user_id:
            root = Path(args.state_dir).expanduser().resolve() if args.state_dir else default_state_root()
            payload["policy"] = load_current(root, user_key(args.user_id))
        result = decide(payload)
    except Exception as exc:
        result = base_result("ENGINE_BLOCKED", "ENGINE_BLOCKED", [f"ENGINE_EXCEPTION:{type(exc).__name__}"])
        result["errorSummary"] = str(exc)[:300]
        result = finish(result, payload)
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
