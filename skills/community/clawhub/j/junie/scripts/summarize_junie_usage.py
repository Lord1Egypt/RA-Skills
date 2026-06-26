#!/usr/bin/env python3
"""Summarize observable Junie usage from local session event logs.

Best-effort only: Junie log formats are owned by JetBrains and may change.
This script reads ~/.junie/sessions and prints aggregate model/cost/token usage.
It does not read credentials.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

TOKEN_KEYS = (
    "inputTokens",
    "outputTokens",
    "cacheInputTokens",
    "cacheCreateTokens",
    "cacheCreateInputTokens",
    "reasoningTokens",
    "webSearchCount",
)


def empty_totals() -> dict[str, float]:
    totals: dict[str, float] = {key: 0 for key in TOKEN_KEYS}
    totals["cost"] = 0.0
    totals["records"] = 0
    return totals


def normalize_usage(record: dict[str, Any]) -> dict[str, float]:
    out = empty_totals()
    out["records"] = 1
    for key in TOKEN_KEYS:
        value = record.get(key, 0)
        if isinstance(value, (int, float)):
            out[key] += value
    value = record.get("cost", 0)
    if isinstance(value, (int, float)):
        out["cost"] += value
    return out


def add_totals(target: dict[str, float], source: dict[str, float]) -> None:
    for key, value in source.items():
        target[key] += value


def find_model_usage_records(value: Any):
    """Yield Junie's LlmResponseMetadataEvent modelUsage records."""
    if isinstance(value, dict):
        records = value.get("modelUsage")
        if isinstance(records, list):
            for record in records:
                if isinstance(record, dict):
                    yield record
        # Some state.json files embed an escaped AgentState JSON string containing
        # assistantRequest.usage records. Parse those as fallback usage records.
        blob = value.get("blob")
        if isinstance(blob, str) and "usage" in blob:
            try:
                yield from find_assistant_usage_records(json.loads(blob))
            except json.JSONDecodeError:
                pass
        for child in value.values():
            yield from find_model_usage_records(child)
    elif isinstance(value, list):
        for child in value:
            yield from find_model_usage_records(child)


def find_assistant_usage_records(value: Any):
    """Yield generic assistantRequest.usage records from embedded state blobs."""
    if isinstance(value, dict):
        usage = value.get("usage")
        if isinstance(usage, dict) and any(key in usage for key in TOKEN_KEYS):
            record = dict(usage)
            record.setdefault("model", "unknown")
            yield record
        for child in value.values():
            yield from find_assistant_usage_records(child)
    elif isinstance(value, list):
        for child in value:
            yield from find_assistant_usage_records(child)


def session_dirs(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(
        (path for path in root.glob("session-*") if path.is_dir()),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )


def summarize_jsonl(path: Path) -> dict[str, dict[str, float]]:
    by_model: dict[str, dict[str, float]] = defaultdict(empty_totals)
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            for record in find_model_usage_records(event):
                model = str(record.get("model") or "unknown")
                add_totals(by_model[model], normalize_usage(record))
    return dict(by_model)


def summarize_session(session_dir: Path) -> dict[str, dict[str, float]]:
    events_path = session_dir / "events.jsonl"
    if events_path.exists():
        by_model = summarize_jsonl(events_path)
        # Prefer events.jsonl because state.json may repeat a partial snapshot of
        # the same conversation and can double-count usage.
        if by_model:
            return by_model

    state_path = session_dir / "state.json"
    by_model: dict[str, dict[str, float]] = defaultdict(empty_totals)
    if not state_path.exists():
        return {}
    try:
        data = json.loads(state_path.read_text(encoding="utf-8", errors="replace"))
    except json.JSONDecodeError:
        return {}
    for record in find_model_usage_records(data):
        model = str(record.get("model") or "unknown")
        add_totals(by_model[model], normalize_usage(record))
    return dict(by_model)


def print_totals(by_model: dict[str, dict[str, float]]) -> bool:
    if not by_model:
        print("  usage: unavailable (no usage records found)")
        return False
    grand = empty_totals()
    for totals in by_model.values():
        add_totals(grand, totals)
    print(f"  usage records: {int(grand['records'])}")
    print(f"  estimated cost: ${grand['cost']:.6f}")
    print(f"  input tokens: {int(grand['inputTokens'])}")
    print(f"  output tokens: {int(grand['outputTokens'])}")
    print(f"  cache read tokens: {int(grand['cacheInputTokens'])}")
    cache_write = grand["cacheCreateTokens"] + grand["cacheCreateInputTokens"]
    print(f"  cache write tokens: {int(cache_write)}")
    if grand["reasoningTokens"]:
        print(f"  reasoning tokens: {int(grand['reasoningTokens'])}")
    if grand["webSearchCount"]:
        print(f"  web searches: {int(grand['webSearchCount'])}")
    print("  by model:")
    for model, totals in sorted(by_model.items(), key=lambda item: item[1]["cost"], reverse=True):
        cache_write = totals["cacheCreateTokens"] + totals["cacheCreateInputTokens"]
        print(
            "    - "
            f"{model}: cost=${totals['cost']:.6f}, "
            f"in={int(totals['inputTokens'])}, out={int(totals['outputTokens'])}, "
            f"cache_read={int(totals['cacheInputTokens'])}, cache_write={int(cache_write)}"
        )
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize observable Junie usage from ~/.junie/sessions")
    parser.add_argument("--session", help="Specific Junie session directory name or path. Defaults to latest session.")
    parser.add_argument("--limit", type=int, default=1, help="Number of newest sessions to summarize when --session is omitted.")
    parser.add_argument("--sessions-root", default=str(Path.home() / ".junie" / "sessions"), help="Junie sessions root")
    args = parser.parse_args()

    root = Path(args.sessions_root).expanduser()
    if args.session:
        candidate = Path(args.session).expanduser()
        targets = [candidate if candidate.exists() else root / args.session]
    else:
        targets = session_dirs(root)[: max(1, args.limit)]

    if not targets:
        print(f"No Junie sessions found under {root}")
        return 1

    any_usage = False
    for session_dir in targets:
        print(f"Junie session: {session_dir.name}")
        any_usage = print_totals(summarize_session(session_dir)) or any_usage
    return 0 if any_usage else 2


if __name__ == "__main__":
    raise SystemExit(main())
