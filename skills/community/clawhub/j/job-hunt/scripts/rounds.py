#!/usr/bin/env python3
"""judge-round-<n>.json: read and merge, never blind-overwrite.

Two programs write this file — check_render_freshness records the dispatch
hashes before the judges run, parse_verdicts writes the verdicts after — and a
plain write from either would erase the other's evidence. Merging at the top
level keeps both, which is the only reason the freshness check can be verified
against the same round it was recorded for.
"""
from __future__ import annotations

import json
import pathlib


def round_path(workspace, n: int) -> pathlib.Path:
    return pathlib.Path(workspace) / f"judge-round-{int(n)}.json"


def load_round(workspace, n: int) -> dict:
    path = round_path(workspace, n)
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def merge_round(workspace, n: int, updates: dict) -> dict:
    path = round_path(workspace, n)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = load_round(workspace, n)
    data.update(updates)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
                    encoding="utf-8")
    return data
