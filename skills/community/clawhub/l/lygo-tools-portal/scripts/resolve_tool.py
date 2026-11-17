#!/usr/bin/env python3
"""Resolve user intent to LYGO public URL or skill slug (stdout JSON)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "references" / "TOOLS_MANIFEST.json"


def score(query: str, intents: list[str]) -> int:
    q = query.lower()
    return sum(2 if t in q else 0 for t in intents)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("query", nargs="+", help="e.g. bpm finder online")
    args = ap.parse_args()
    q = " ".join(args.query)
    if not MANIFEST.is_file():
        print(json.dumps({"error": "missing manifest"}))
        return 1
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    best_page = None
    best_score = 0
    for page in data.get("public_pages", []):
        s = score(q, page.get("intents", []))
        if s > best_score:
            best_score = s
            best_page = page
    best_skill = None
    best_skill_score = 0
    for sk in data.get("clawhub_skills", []):
        s = score(q, sk.get("intents", []))
        if s > best_skill_score:
            best_skill_score = s
            best_skill = sk
    out = {
        "query": q,
        "public_page": best_page,
        "clawhub_skill": best_skill if best_skill_score > 0 else None,
        "hubs": data.get("hubs", {}),
    }
    if best_page and best_score > 0:
        urls = best_page.get("urls", {})
        prefer = best_page.get("prefer", "stack")
        out["recommended_url"] = urls.get(prefer) or urls.get("stack") or urls.get("excavationpro") or urls.get("live")
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())