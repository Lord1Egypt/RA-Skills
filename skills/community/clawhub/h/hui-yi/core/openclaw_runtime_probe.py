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
from core.common import WORKSPACE_ROOT, resolve_path
from core.openclaw_signal_hook import run_hook
from core.signal_detect import load_context_text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Prototype runner for Hui-Yi OpenClaw hook integration")
    parser.add_argument("--query", default=None, help="current query; use --stdin to keep query text out of process arguments")
    parser.add_argument("--stdin", action="store_true", help="read private query/context from stdin")
    parser.add_argument("--channel", required=True)
    parser.add_argument("--scope-type", required=True, choices=["user", "chat"])
    parser.add_argument("--scope-id", required=True)
    parser.add_argument("--thread-id", default=None)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--memory-root", default="memory/cold")
    parser.add_argument("--trigger-source", choices=["skill_hit", "heuristic_fallback", "manual_probe"], default="manual_probe")
    args = parser.parse_args(argv)
    try:
        query = load_context_text(args.query, None, args.stdin)
        # Preserve the previous workspace-relative CLI path semantics without
        # launching a child process or exposing its command line/output.
        memory_root = resolve_path(args.memory_root, base=WORKSPACE_ROOT)
        hook_result = run_hook(memory_root, query, args.channel, args.scope_type, args.scope_id,
                               thread_id=args.thread_id, trigger_source=args.trigger_source,
                               dry_run=args.dry_run)
    except (OSError, ValueError, TypeError, OverflowError):
        hook_result = {"ok": False, "exitCode": 1, "error": "probe_input_failed"}
    returncode = 0 if hook_result.get("ok") else 1
    result = {
        "ok": returncode == 0,
        "result": hook_result,
        "returncode": returncode,
        "integrationMode": "workspace-prototype",
        "runtimePatchApplied": False,
        "recommendedRuntimeHookPoint": "after Hui-Yi skill selection, before recall/resurface execution",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return returncode


if __name__ == "__main__":
    raise SystemExit(main())
