#!/usr/bin/env python3
"""End-to-end session signal pipeline for Hui-Yi.

Detect high-confidence cold-memory hits from real conversation context,
then optionally write weak activation signals back to matching notes.
"""
from __future__ import annotations

import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

import argparse
import contextlib
import json
import sys
from datetime import date
from io import StringIO
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from core.signal_apply import main as signal_apply_main
from core.signal_contract import CONFIDENCE_ORDER, candidate_payload
from core.signal_detect import load_context_text, detect_match
from core.common import load_tags_payload, repetition_signal, resolve_memory_root


def run_apply(note_ref: str, memory_root: Path, session_key: str, strength: str, source: str, activated_at: str) -> tuple[int, str]:
    stderr = StringIO()
    with contextlib.redirect_stderr(stderr):
        exit_code = signal_apply_main(
            [
                note_ref,
                "--memory-root",
                str(memory_root),
                "--session-key",
                session_key,
                "--strength",
                strength,
                "--source",
                source,
                "--activated-at",
                activated_at,
            ]
        )
    return exit_code, stderr.getvalue().strip()


def collect_candidates(memory_root: Path, query_text: str, min_relevance: float, min_confidence: str, limit: int) -> tuple[list[dict], date]:
    payload = load_tags_payload(memory_root)
    notes = payload.get("notes", []) if isinstance(payload.get("notes"), list) else []
    today = date.today()

    candidates = []
    for note in notes:
        relevance, meta = detect_match(note, query_text)
        if relevance < min_relevance:
            continue
        confidence = meta.get("confidence", "none")
        if confidence == "none":
            continue
        if CONFIDENCE_ORDER.get(confidence, 0) < CONFIDENCE_ORDER[min_confidence]:
            continue
        candidate = candidate_payload(note, relevance, meta, today)
        candidate["repetition_signal"] = repetition_signal(note, today)
        candidates.append(candidate)

    candidates.sort(key=lambda item: (item["relevance"], item.get("repetition_signal", 0.0)), reverse=True)
    return candidates[:limit], today


def apply_candidates(memory_root: Path, candidates: list[dict], session_key: str, *, strength: str = "weak", source: str = "signal_pipeline", activated_at: str | None = None) -> tuple[list[str], list[str], list[str]]:
    activated_at = activated_at or date.today().isoformat()
    applied = []
    skipped = []
    errors = []
    for item in candidates:
        note_ref = item["path"] or item["title"] or ""
        exit_code, message = run_apply(
            note_ref,
            memory_root,
            session_key,
            strength=strength,
            source=source,
            activated_at=activated_at,
        )
        if exit_code == 0 and message.startswith("SKIP duplicate activation:"):
            skipped.append(note_ref)
        elif exit_code == 0:
            applied.append(note_ref)
        else:
            errors.append(message or f"failed to apply signal to {note_ref}")
    return applied, skipped, errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Detect and optionally apply Hui-Yi session activation signals")
    parser.add_argument("--memory-root", default=None)
    parser.add_argument("--query", default=None)
    parser.add_argument("--context-file", default=None)
    parser.add_argument("--stdin", action="store_true")
    parser.add_argument("--session-key", default=None)
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--min-relevance", type=float, default=0.30)
    parser.add_argument("--min-confidence", choices=["low", "medium", "high"], default="medium")
    parser.add_argument("--apply", action="store_true", help="write weak activation signals back to matched notes")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    query_text = load_context_text(args.query, args.context_file, args.stdin)
    if not query_text:
        print("No query/context provided.")
        return 1

    memory_root = resolve_memory_root(args.memory_root)
    candidates, today = collect_candidates(memory_root, query_text, args.min_relevance, args.min_confidence, args.limit)

    applied = []
    skipped = []
    apply_errors = []
    if args.apply:
        if not args.session_key:
            print("--apply requires --session-key")
            return 1
        applied, skipped, apply_errors = apply_candidates(
            memory_root,
            candidates,
            args.session_key,
            strength="weak",
            source="signal_pipeline",
            activated_at=today.isoformat(),
        )

    result = {
        "query": query_text,
        "session_key": args.session_key,
        "candidates": candidates,
        "applied": applied,
        "skipped": skipped,
        "apply_errors": apply_errors,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    if not candidates:
        print("No session activation candidates.")
        return 0

    print("Session signal pipeline candidates:")
    for item in candidates:
        print(f"- relevance={item['relevance']:.3f} confidence={item['confidence']} repeat={item.get('repetition_signal', 0.0):.3f} | {item['title']}")
        print(f"  overlap_terms={', '.join(item['overlap_terms']) or 'n/a'}")
        print(f"  matched_fields={', '.join(item['matched_fields']) or 'n/a'}")
        print(f"  path: {item['path']}")
    if applied:
        print("Applied weak activation to:")
        for item in applied:
            print(f"- {item}")
    if skipped:
        print("Skipped duplicate activation for:")
        for item in skipped:
            print(f"- {item}")
    if apply_errors:
        print("Signal apply errors:", file=sys.stderr)
        for item in apply_errors:
            print(f"- {item}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
