#!/usr/bin/env python3
"""Collect and rank learning resources for a subject from web/X/YouTube link lists.

This script ranks candidate URLs; upstream retrieval can come from agent web search
or optional integrations. Keep output deterministic JSON for coaching workflows.
"""

from __future__ import annotations
import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-") or "subject"


def score_item(item: dict, goals: list[str], weak_areas: list[str]) -> float:
    title = (item.get("title") or "").lower()
    desc = (item.get("snippet") or "").lower()
    url = (item.get("url") or "").lower()
    text = f"{title} {desc} {url}"

    relevance = sum(1 for g in goals if g.lower() in text) * 8
    weakness = sum(1 for w in weak_areas if w.lower() in text) * 10

    credibility = 0
    if any(x in url for x in ["docs.", "developer.", "arxiv.org", "edu", "mozilla.org", "khanacademy.org"]):
        credibility += 20
    if "youtube.com" in url or "youtu.be" in url:
        credibility += 8
    if "x.com" in url or "twitter.com" in url:
        credibility += 4

    depth = 6 if any(k in text for k in ["guide", "deep dive", "tutorial", "walkthrough", "course"]) else 0
    freshness = float(item.get("freshness", 0))  # caller may pass 0..10

    return round(relevance + weakness + credibility + depth + freshness, 2)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", required=True)
    ap.add_argument("--candidates", required=True, help="Input JSON array of {title,url,snippet,source,freshness?}")
    ap.add_argument("--data-root", default="data")
    ap.add_argument("--limit", type=int, default=12)
    ap.add_argument("--out")
    args = ap.parse_args()

    slug = slugify(args.subject)
    sdir = Path(args.data_root) / "subjects" / slug
    sdir.mkdir(parents=True, exist_ok=True)

    profile = {}
    progress = {}
    pp = sdir / "profile.json"
    pg = sdir / "progress.json"
    if pp.exists():
        profile = json.loads(pp.read_text(encoding="utf-8"))
    if pg.exists():
        progress = json.loads(pg.read_text(encoding="utf-8"))

    goals = profile.get("goals", []) if isinstance(profile.get("goals", []), list) else []
    weak_areas = progress.get("weak_areas", []) if isinstance(progress.get("weak_areas", []), list) else []

    candidates = json.loads(Path(args.candidates).read_text(encoding="utf-8"))
    ranked = []
    for item in candidates:
        s = score_item(item, goals, weak_areas)
        ranked.append({
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "snippet": item.get("snippet", ""),
            "source": item.get("source", "web"),
            "score": s,
            "why": "Matched goals/weak areas + source quality heuristics",
        })

    ranked.sort(key=lambda x: x["score"], reverse=True)
    curated = {
        "subject": args.subject,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "count": min(args.limit, len(ranked)),
        "resources": ranked[: args.limit],
    }

    out = Path(args.out) if args.out else (sdir / "curation.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(curated, indent=2), encoding="utf-8")
    print(str(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
