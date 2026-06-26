#!/usr/bin/env python3
"""
Scan a batch of inputs from a JSONL file and emit a JSON report of which
ones are safe to forward downstream.

Each line of the input must be a JSON object containing at least:
  {"id": "<unique id>", "text": "<text to scan>"}

Additional keys are preserved verbatim under "input" in the output.

Usage:
  python3 scan_batch.py --jsonl inputs.jsonl --output report.json
  python3 scan_batch.py --jsonl inputs.jsonl --output report.json --only-safe safe_subset.jsonl
  python3 scan_batch.py --jsonl - --output -                 # stdin to stdout

Exit codes:
  0 = success
  3 = error
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from _core import (
    full_report,
    SAFE_THRESHOLD_DEFAULT,
    BLOCK_THRESHOLD_DEFAULT,
)

SAFE_PATH_RE = re.compile(r"^[\w./\-+ @=:%,()'\[\]]+$")


def safe_path(p: str) -> Path:
    if not SAFE_PATH_RE.match(p):
        raise ValueError(f"Refusing path with unsafe characters: {p!r}")
    return Path(p).expanduser()


def read_jsonl(source: str) -> List[Dict]:
    if source == "-":
        raw = sys.stdin.read()
    else:
        path = safe_path(source).resolve()
        if not path.is_file():
            raise FileNotFoundError(f"file not found: {path}")
        raw = path.read_text(encoding="utf-8")

    rows: List[Dict] = []
    for i, line in enumerate(raw.splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as e:
            raise ValueError(f"invalid JSON on line {i}: {e}")
        if not isinstance(obj, dict):
            raise ValueError(f"line {i}: expected object, got {type(obj).__name__}")
        if "id" not in obj or "text" not in obj:
            raise ValueError(f"line {i}: missing required keys 'id' and 'text'")
        rows.append(obj)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--jsonl", required=True, help="JSONL input file (or '-' for stdin)")
    parser.add_argument("--output", required=True, help="JSON report output (or '-' for stdout)")
    parser.add_argument(
        "--only-safe",
        default="",
        help="Optional path to write the safe subset as JSONL (verdict == 'safe').",
    )
    parser.add_argument(
        "--caution-at", type=int, default=SAFE_THRESHOLD_DEFAULT,
        help=f"Score >= this is 'caution' (default {SAFE_THRESHOLD_DEFAULT})",
    )
    parser.add_argument(
        "--block-at", type=int, default=BLOCK_THRESHOLD_DEFAULT,
        help=f"Score >= this is 'block' (default {BLOCK_THRESHOLD_DEFAULT})",
    )
    parser.add_argument(
        "--whitelist", action="append", default=[],
        help="Allow-list phrase. May be passed multiple times.",
    )
    parser.add_argument(
        "--whitelist-file",
        help="Path to a UTF-8 file with one whitelist phrase per line.",
    )
    args = parser.parse_args()

    if args.caution_at < 0 or args.caution_at > 100:
        print("error: --caution-at must be in 0..100", file=sys.stderr)
        return 3
    if args.block_at <= args.caution_at or args.block_at > 100:
        print("error: --block-at must be > --caution-at and <= 100", file=sys.stderr)
        return 3

    whitelist = list(args.whitelist or [])
    if args.whitelist_file:
        try:
            wl_path = safe_path(args.whitelist_file).resolve()
            if not wl_path.is_file():
                raise FileNotFoundError(f"whitelist file not found: {wl_path}")
            for raw in wl_path.read_text(encoding="utf-8").splitlines():
                s = raw.strip()
                if s and not s.startswith("#"):
                    whitelist.append(s)
        except (ValueError, FileNotFoundError) as e:
            print(f"error: {e}", file=sys.stderr)
            return 3

    try:
        rows = read_jsonl(args.jsonl)
    except (ValueError, FileNotFoundError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 3

    results = []
    counts = {"safe": 0, "caution": 0, "block": 0}
    safe_rows: List[Dict] = []

    for row in rows:
        text = row.get("text") or ""
        report = full_report(
            text,
            caution_at=args.caution_at,
            block_at=args.block_at,
            whitelist=whitelist or None,
        )
        record = {
            "id": row.get("id"),
            "verdict": report["verdict"],
            "risk_score": report["risk_score"],
            "matches": report["matches"],
            "category_scores": report["category_scores"],
            "combined_signal_bonus": report.get("combined_signal_bonus", 0),
            "distinct_categories": report.get("distinct_categories", 0),
            "recommendation": report["recommendation"],
            "char_count": report["char_count"],
            "input": {k: v for k, v in row.items() if k != "text"},
        }
        results.append(record)
        counts[report["verdict"]] += 1
        if report["verdict"] == "safe":
            safe_rows.append(row)

    summary = {
        "total": len(results),
        "thresholds": {"caution_at": args.caution_at, "block_at": args.block_at},
        "counts": counts,
        "results": results,
    }

    out_text = json.dumps(summary, indent=2, ensure_ascii=False) + "\n"
    if args.output == "-":
        sys.stdout.write(out_text)
    else:
        try:
            out_path = safe_path(args.output).resolve()
        except ValueError as e:
            print(f"error: {e}", file=sys.stderr)
            return 3
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(out_text, encoding="utf-8")
        print(
            f"Wrote {out_path}  total={summary['total']} "
            f"safe={counts['safe']} caution={counts['caution']} block={counts['block']}",
            file=sys.stderr,
        )

    if args.only_safe:
        try:
            sub_path = safe_path(args.only_safe).resolve()
        except ValueError as e:
            print(f"error: {e}", file=sys.stderr)
            return 3
        sub_path.parent.mkdir(parents=True, exist_ok=True)
        with sub_path.open("w", encoding="utf-8") as fh:
            for row in safe_rows:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(f"Wrote safe subset to {sub_path} ({len(safe_rows)} rows)", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
