#!/usr/bin/env python3
"""Static scan helper for MATLAB simulation optimization tasks."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


PATTERNS = {
    "entry_candidate": re.compile(r"^\s*(clear|clc|close all|rng|addpath|run\()", re.I),
    "for_loop": re.compile(r"^\s*(for|parfor)\b", re.I),
    "while_loop": re.compile(r"^\s*while\b", re.I),
    "dynamic_growth": re.compile(r"\[[^\]]*;\s*[A-Za-z]\w*|end\s*\+\s*1|\([^\)]*end\s*\+\s*1", re.I),
    "explicit_inverse": re.compile(r"\binv\s*\(", re.I),
    "randomness": re.compile(r"\b(rand|randn|randi|rng)\s*\(", re.I),
    "plotting": re.compile(r"\b(plot|semilogy|semilogx|figure|subplot|legend|saveas|exportgraphics)\s*\(", re.I),
    "file_io": re.compile(r"\b(load|save|fopen|fprintf|readmatrix|writematrix|csvread|csvwrite)\s*\(", re.I),
    "clear_all": re.compile(r"\bclear\s+all\b", re.I),
    "tic_toc": re.compile(r"\b(tic|toc|timeit|profile)\b", re.I),
    "hard_coded_numbers": re.compile(r"(?<![A-Za-z_])(?:\d+\.\d+|\d+e[+-]?\d+|[2-9]\d{1,})(?![A-Za-z_])", re.I),
}


def strip_comment(line: str) -> str:
    quote = False
    for i, ch in enumerate(line):
        if ch == "'":
            quote = not quote
        if ch == "%" and not quote:
            return line[:i]
    return line


def scan_file(path: Path) -> dict:
    result = {
        "path": str(path),
        "lines": 0,
        "function_defs": [],
        "hits": {key: [] for key in PATTERNS},
    }
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception as exc:
        result["error"] = str(exc)
        return result

    result["lines"] = len(lines)
    for lineno, raw in enumerate(lines, start=1):
        line = strip_comment(raw)
        if re.match(r"^\s*function\b", line, re.I):
            result["function_defs"].append({"line": lineno, "text": raw.strip()[:180]})
        for key, pattern in PATTERNS.items():
            if pattern.search(line):
                result["hits"][key].append({"line": lineno, "text": raw.strip()[:180]})
    return result


def summarize(files: list[dict]) -> dict:
    totals = {key: 0 for key in PATTERNS}
    hotspots = []
    for item in files:
        score = 0
        for key, hits in item.get("hits", {}).items():
            totals[key] += len(hits)
            if key in {"for_loop", "while_loop", "dynamic_growth", "explicit_inverse", "file_io", "plotting"}:
                score += len(hits)
        if score:
            hotspots.append({"path": item["path"], "score": score})
    hotspots.sort(key=lambda x: x["score"], reverse=True)
    return {"totals": totals, "hotspots": hotspots[:20]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", help="MATLAB source root")
    parser.add_argument("--out", help="Optional JSON output path")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"MATLAB source root does not exist: {root}")

    files = [scan_file(path) for path in sorted(root.rglob("*.m"))]
    payload = {
        "root": str(root),
        "file_count": len(files),
        "summary": summarize(files),
        "files": files,
    }
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).expanduser().resolve().write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
