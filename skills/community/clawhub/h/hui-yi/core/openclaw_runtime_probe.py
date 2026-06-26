#!/usr/bin/env python3
"""Workspace-side prototype runner for Hui-Yi OpenClaw integration.

Purpose:
- avoid patching OpenClaw dist/node_modules directly
- simulate the upper-layer skill-hit hook contract
- provide a concrete runner for validating Hui-Yi signal hook behavior from real session metadata
"""
from __future__ import annotations

import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

import argparse
import json
import subprocess

from core.common import WORKSPACE_ROOT


def main() -> int:
    parser = argparse.ArgumentParser(description="Prototype runner for Hui-Yi OpenClaw hook integration")
    parser.add_argument("--query", required=True)
    parser.add_argument("--channel", required=True)
    parser.add_argument("--scope-type", required=True, choices=["user", "chat"])
    parser.add_argument("--scope-id", required=True)
    parser.add_argument("--thread-id", default=None)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--memory-root", default="memory/cold")
    parser.add_argument("--trigger-source", choices=["skill_hit", "heuristic_fallback", "manual_probe"], default="manual_probe")
    args = parser.parse_args()

    workspace = WORKSPACE_ROOT
    hook_script = workspace / "skills" / "hui-yi" / "core" / "openclaw_signal_hook.py"
    cmd = [
        sys.executable,
        str(hook_script),
        "--query",
        args.query,
        "--channel",
        args.channel,
        "--scope-type",
        args.scope_type,
        "--scope-id",
        args.scope_id,
        "--memory-root",
        args.memory_root,
        "--trigger-source",
        args.trigger_source,
    ]
    if args.thread_id:
        cmd.extend(["--thread-id", args.thread_id])
    if args.dry_run:
        cmd.append("--dry-run")

    proc = subprocess.run(cmd, cwd=str(workspace), capture_output=True, text=True)
    result = {
        "ok": proc.returncode == 0,
        "command": cmd,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "returncode": proc.returncode,
        "integrationMode": "workspace-prototype",
        "runtimePatchApplied": False,
        "recommendedRuntimeHookPoint": "after Hui-Yi skill selection, before recall/resurface execution",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if proc.returncode == 0 else proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
