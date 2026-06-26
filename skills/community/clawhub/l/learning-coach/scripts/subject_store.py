#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

REQUIRED = ["profile.json", "plan.json", "quiz-history.json", "progress.json", "curation.json"]


def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-") or "subject"


def ensure_subject(root: Path, subject: str) -> Path:
    slug = slugify(subject)
    d = root / "subjects" / slug
    d.mkdir(parents=True, exist_ok=True)
    defaults = {
        "profile.json": {"subject": subject, "slug": slug, "level": "unknown", "goals": []},
        "plan.json": {"focus": [], "weekly_hours": None},
        "quiz-history.json": {"items": []},
        "progress.json": {"metrics": {}, "weak_areas": []},
        "curation.json": {"resources": []},
    }
    for f in REQUIRED:
        p = d / f
        if not p.exists():
            p.write_text(json.dumps(defaults[f], indent=2), encoding="utf-8")
    return d


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["init", "list"])
    ap.add_argument("--subject")
    ap.add_argument("--data-root", default="data")
    args = ap.parse_args()

    root = Path(args.data_root)
    root.mkdir(parents=True, exist_ok=True)

    if args.action == "list":
        sroot = root / "subjects"
        if not sroot.exists():
            print("[]")
            return 0
        print(json.dumps(sorted([p.name for p in sroot.iterdir() if p.is_dir()]), indent=2))
        return 0

    if not args.subject:
        raise SystemExit("--subject is required for init")

    d = ensure_subject(root, args.subject)
    print(str(d))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
