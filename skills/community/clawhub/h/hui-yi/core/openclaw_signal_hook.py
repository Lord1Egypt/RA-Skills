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
from core.signal_detect import load_context_text
from core.signal_pipeline import run_pipeline


def call_signal_pipeline(memory_root: Path, query: str, session_key: str, *, limit: int, min_relevance: float, min_confidence: str, apply: bool) -> dict:
    # Hook results are diagnostics, not a retrieval response. Allowlist counts
    # rather than deleting selected fields from an expanding pipeline payload.
    try:
        payload = run_pipeline(memory_root, query, session_key, limit=limit,
                               min_relevance=min_relevance, min_confidence=min_confidence,
                               apply=apply)
        ok = bool(payload.get("ok")) and not payload.get("apply_errors")
        pipeline = {
            "candidateCount": len(payload.get("candidates", [])),
            "appliedCount": len(payload.get("applied", [])),
            "skippedCount": len(payload.get("skipped", [])),
            "errorCount": len(payload.get("apply_errors", [])),
        }
        if not ok:
            pipeline["error"] = "pipeline_failed"
    except (OSError, ValueError, TypeError, OverflowError):
        ok = False
        pipeline = {"error": "pipeline_failed", "errorCount": 1}
    return {
        "ok": ok,
        "exitCode": 0 if ok else 1,
        "sessionHash": session_fingerprint(session_key),
        "pipeline": pipeline,
    }


def run_hook(memory_root: Path, query: str, channel: str, scope_type: str, scope_id: str, *,
             thread_id: str | None = None, trigger_source: str = "skill_hit", dry_run: bool = False,
             limit: int | None = None, min_relevance: float | None = None,
             min_confidence: str | None = None) -> dict:
    defaults = resolve_trigger_defaults(trigger_source)
    session_key = build_session_key(channel, scope_type, scope_id, thread_id)
    result = call_signal_pipeline(memory_root, query, session_key,
        limit=limit if limit is not None else defaults["limit"],
        min_relevance=min_relevance if min_relevance is not None else defaults["min_relevance"],
        min_confidence=min_confidence if min_confidence is not None else defaults["min_confidence"],
        apply=not dry_run)
    result["dryRun"] = dry_run
    result["triggerSource"] = trigger_source if trigger_source in {"skill_hit", "heuristic_fallback", "manual_probe"} else "manual_probe"
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Minimal OpenClaw-facing hook stub for Hui-Yi session signals")
    parser.add_argument("--query", default=None, help="current query; use --stdin to keep query text out of process arguments")
    parser.add_argument("--stdin", action="store_true", help="read private query/context from stdin")
    parser.add_argument("--channel", required=True, help="chat platform, e.g. feishu")
    parser.add_argument("--scope-type", required=True, choices=["user", "chat"], help="user for DM / chat for group")
    parser.add_argument("--scope-id", required=True, help="stable user or chat id")
    parser.add_argument("--thread-id", default=None, help="thread id when available")
    parser.add_argument("--memory-root", default=None)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--min-relevance", type=float, default=None)
    parser.add_argument("--min-confidence", choices=["low", "medium", "high"], default=None)
    parser.add_argument("--trigger-source", choices=["skill_hit", "heuristic_fallback", "manual_probe"], default="skill_hit")
    parser.add_argument("--dry-run", action="store_true", help="detect only; do not apply weak activation")
    args = parser.parse_args(argv)
    try:
        query = load_context_text(args.query, None, args.stdin)
        result = run_hook(resolve_memory_root(args.memory_root), query, args.channel, args.scope_type,
                          args.scope_id, thread_id=args.thread_id, trigger_source=args.trigger_source,
                          dry_run=args.dry_run, limit=args.limit, min_relevance=args.min_relevance,
                          min_confidence=args.min_confidence)
    except (OSError, ValueError, TypeError, OverflowError):
        result = {"ok": False, "exitCode": 1, "error": "hook_input_failed"}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
