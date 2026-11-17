#!/usr/bin/env python3
"""
Priority / novelty check - MUST run before claiming novelty.

Searches arXiv, DBLP and OpenAlex for prior art on a claim and records the
candidates. The verdict defaults to UNCHECKED. The tool never declares a claim
novel on its own; a human resolves it against the listed sources, with a URL
and a date, and that resolution is written to the audit trail.

Usage:
    python priority_check.py -d 02-methodology-dev --claim "C(d,n) = A_leq d(n)"
    python priority_check.py -d 02-methodology-dev --list
    python priority_check.py -d 02-methodology-dev --resolve P1 --verdict covered \
        --evidence https://arxiv.org/abs/2502.xxxxx --note "same identity in Thm 3"
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from datetime import datetime
from pathlib import Path

FILE = "priority-records.json"
VERDICTS = ("novel", "covered", "partial", "unchecked")
UNCHECKED = "unchecked"


def _search_api():
    spec = importlib.util.spec_from_file_location(
        "mss", Path(__file__).resolve().parent / "multi_source_search.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def record_id(text: str) -> str:
    """Stable, collision-resistant ID.

    A truncated slug collides: two claims sharing a prefix silently overwrite
    each other's record. A hash of the full claim text does not.
    """
    return "P" + hashlib.sha1(text.strip().lower().encode("utf-8")).hexdigest()[:8]


def load(d: Path) -> dict:
    p = d / FILE
    if not p.exists():
        return {"created": datetime.now().isoformat(timespec="seconds"), "records": {}}
    return json.loads(p.read_text(encoding="utf-8"))


def save(d: Path, data: dict) -> None:
    d.mkdir(parents=True, exist_ok=True)
    (d / FILE).write_text(json.dumps(data, indent=2), encoding="utf-8")


def gather(claim: str, limit: int) -> tuple[list[dict], list[str]]:
    mod = _search_api()
    hits, failures = [], []
    for src in ("arxiv", "dblp", "openalex"):
        try:
            hits += mod.DISPATCH[src](claim, limit, None, None)
        except Exception as e:  # noqa: BLE001
            failures.append(f"{src}: {type(e).__name__}: {e}")
    return hits, failures


def main() -> int:
    ap = argparse.ArgumentParser(description="Priority / novelty check before claiming novelty")
    ap.add_argument("-d", "-p", "--dir", default="02-methodology-dev")
    ap.add_argument("--claim", help="the claim or identity to check")
    ap.add_argument("--limit", type=int, default=8)
    ap.add_argument("--resolve", metavar="ID")
    ap.add_argument("--verdict", choices=VERDICTS)
    ap.add_argument("--evidence", default="", help="URL of the covering/confirming source")
    ap.add_argument("--note", default="")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 if any record is still UNCHECKED")
    args = ap.parse_args()

    d = Path(args.dir).expanduser().resolve()
    data = load(d)

    if args.claim:
        rid = record_id(args.claim)
        hits, failures = gather(args.claim, args.limit)
        data["records"][rid] = {
            "claim": args.claim,
            "checked_at": datetime.now().isoformat(timespec="seconds"),
            "sources_queried": ["arxiv", "dblp", "openalex"],
            "failures": failures,
            "candidates": [{"title": h.get("title"), "year": h.get("year"),
                            "venue": h.get("venue"), "url": h.get("url"),
                            "via": h.get("source")} for h in hits[:25]],
            "verdict": UNCHECKED,
            "evidence": None,
            "note": None,
        }
        save(d, data)
        print(f"record {rid}: {len(hits)} candidate(s) from prior-art search")
        for h in hits[:10]:
            print(f"  - [{h.get('source')}] {h.get('title','')[:80]}")
        if failures:
            print("\nSources that FAILED (verdict cannot rely on them):")
            for f in failures:
                print(f"  - {f}")
        print(f"\nVerdict is UNCHECKED. Resolve it with --resolve {rid} --verdict ... "
              f"--evidence <url>")
        return 0

    if args.resolve:
        if args.resolve not in data["records"]:
            print(f"error: unknown record {args.resolve}", file=sys.stderr)
            return 2
        if not args.verdict:
            print("error: --verdict required", file=sys.stderr)
            return 2
        if args.verdict != UNCHECKED and not args.evidence.startswith(("http://", "https://")):
            print("error: a resolved verdict requires --evidence <http(s) URL> to the "
                  "source page that was actually consulted", file=sys.stderr)
            return 2
        rec = data["records"][args.resolve]
        rec.update({"verdict": args.verdict,
                    "evidence": args.evidence or None,
                    "note": args.note or None,
                    "resolved_at": datetime.now().isoformat(timespec="seconds")})
        save(d, data)
        print(f"{args.resolve} -> {args.verdict}")
        return 0

    recs = data.get("records", {})
    unchecked = [k for k, v in recs.items() if v.get("verdict") == UNCHECKED]
    print(f"Priority records: {len(recs)} | unresolved: {len(unchecked)}")
    for k, v in recs.items():
        print(f"  {k}: {v.get('verdict')}  {v.get('claim','')[:60]}"
              + (f"  <{v.get('evidence')}>" if v.get("evidence") else ""))
    if unchecked:
        print("\nBLOCKER: these claims must not be described as novel until resolved:")
        for k in unchecked:
            print(f"  - {k}")
    return 1 if (args.strict and unchecked) else 0


if __name__ == "__main__":
    sys.exit(main())
