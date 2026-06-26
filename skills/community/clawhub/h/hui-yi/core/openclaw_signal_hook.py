#!/usr/bin/env python3
"""Minimal OpenClaw-facing hook stub for Hui-Yi session signal accumulation.

This script is intentionally thin. It does not decide whether Hui-Yi should be used.
Instead, it assumes the upper OpenClaw agent/skill-selection layer has already decided
that the current interaction truly matches Hui-Yi.

Its job is only:
- normalize a stable session_key
- call signal_pipeline.py with conservative defaults
- return machine-readable output for upper-layer logging / observation
"""
from __future__ import annotations

import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from core.common import resolve_memory_root, session_fingerprint
from core.signal_contract import build_session_key, resolve_trigger_defaults
from core.signal_pipeline import main as signal_pipeline_main


def call_signal_pipeline(memory_root: Path, query: str, session_key: str, *, limit: int, min_relevance: float, min_confidence: str, apply: bool) -> dict:
    argv = [
        "--memory-root",
        str(memory_root),
        "--query",
        query,
        "--session-key",
        session_key,
        "--limit",
        str(limit),
        "--min-relevance",
        str(min_relevance),
        "--min-confidence",
        min_confidence,
        "--json",
    ]
    if apply:
        argv.append("--apply")

    from io import StringIO
    import contextlib

    capture = StringIO()
    with contextlib.redirect_stdout(capture):
        exit_code = signal_pipeline_main(argv)
    output = capture.getvalue().strip()
    payload = json.loads(output) if output else {}
    if isinstance(payload, dict):
        payload.pop("session_key", None)
    return {
        "ok": exit_code == 0,
        "exitCode": exit_code,
        "sessionHash": session_fingerprint(session_key),
        "pipeline": payload,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Minimal OpenClaw-facing hook stub for Hui-Yi session signals")
    parser.add_argument("--query", required=True, help="current user query or short context summary")
    parser.add_argument("--channel", required=True, help="chat platform, e.g. feishu")
    parser.add_argument("--scope-type", required=True, choices=["user", "chat"], help="user for DM / chat for group")
    parser.add_argument("--scope-id", required=True, help="stable user or chat id")
    parser.add_argument("--thread-id", default=None, help="thread id when available")
    parser.add_argument("--memory-root", default=None)
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--min-relevance", type=float, default=None)
    parser.add_argument("--min-confidence", choices=["low", "medium", "high"], default=None)
    parser.add_argument("--trigger-source", choices=["skill_hit", "heuristic_fallback", "manual_probe"], default="skill_hit")
    parser.add_argument("--dry-run", action="store_true", help="detect only; do not apply weak activation")
    args = parser.parse_args()

    defaults = resolve_trigger_defaults(args.trigger_source)

    memory_root = resolve_memory_root(args.memory_root)
    session_key = build_session_key(args.channel, args.scope_type, args.scope_id, args.thread_id)
    result = call_signal_pipeline(
        memory_root,
        args.query,
        session_key,
        limit=args.limit if args.limit is not None else defaults["limit"],
        min_relevance=args.min_relevance if args.min_relevance is not None else defaults["min_relevance"],
        min_confidence=args.min_confidence if args.min_confidence is not None else defaults["min_confidence"],
        apply=not args.dry_run,
    )
    result["dryRun"] = args.dry_run
    result["triggerSource"] = args.trigger_source
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
