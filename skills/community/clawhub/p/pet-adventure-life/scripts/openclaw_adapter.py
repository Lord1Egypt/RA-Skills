#!/usr/bin/env python3
"""Small JSON adapter for running pet-adventure-life from OpenClaw-style actions."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ENGINE = Path(__file__).with_name("pet_adventure.py")

ACTION_MAP = {
    "init": "init",
    "advance": "advance",
    "status": "status",
    "call": "call",
    "answer": "answer",
    "auto_resolve": "auto-resolve",
    "auto-resolve": "auto-resolve",
}


def run_engine(action: str, payload: dict[str, Any]) -> dict[str, Any]:
    if action not in ACTION_MAP:
        return {"ok": False, "error": f"Unsupported action: {action}"}
    workspace = payload.get("workspace", ".")
    cmd = [sys.executable, str(ENGINE), "--workspace", workspace, ACTION_MAP[action]]
    if action == "status":
        cmd.append("--json")
    for key, value in payload.items():
        if key == "workspace" or value is None or value is False:
            continue
        flag = "--" + key.replace("_", "-")
        if value is True:
            cmd.append(flag)
        else:
            cmd.extend([flag, str(value)])
    completed = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        return {
            "ok": False,
            "error": completed.stderr.strip() or completed.stdout.strip(),
            "returncode": completed.returncode,
        }
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError:
        return {"ok": True, "text": completed.stdout.strip()}


def main() -> None:
    parser = argparse.ArgumentParser(description="OpenClaw adapter for pet-adventure-life")
    parser.add_argument("action", choices=sorted(ACTION_MAP))
    parser.add_argument("--payload", help="JSON payload for the action")
    parser.add_argument("--payload-file", help="Path to a JSON payload file")
    args = parser.parse_args()
    payload: dict[str, Any] = {}
    if args.payload_file:
        payload = json.loads(Path(args.payload_file).read_text(encoding="utf-8"))
    elif args.payload:
        payload = json.loads(args.payload)
    result = run_engine(args.action, payload)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
