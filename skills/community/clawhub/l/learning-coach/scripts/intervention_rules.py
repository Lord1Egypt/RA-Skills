#!/usr/bin/env python3
"""Generate intervention recommendations from per-subject progress signals."""

from __future__ import annotations
import argparse
import json
from pathlib import Path


def load_json(path: Path, default):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def recommend(metrics: dict, weak_areas: list[str]) -> dict:
    ema = float(metrics.get("ema_score") or 0)
    conf = float(metrics.get("confidence") or 0)
    delta = float(metrics.get("delta_vs_ema") or 0)

    actions = []
    mode = "maintain"

    if ema >= 75 and conf >= 60 and delta >= 0:
        mode = "speed-up"
        actions = [
            "Increase problem difficulty one notch",
            "Add 1 case-based quiz this week",
            "Shift 20% time to projects"
        ]
    elif ema < 50 or (delta < -8 and conf < 50):
        mode = "slow-down"
        actions = [
            "Reduce weekly scope by 25%",
            "Revisit fundamentals with short drills",
            "Schedule re-test in 48 hours"
        ]
    else:
        mode = "stabilize"
        actions = [
            "Keep current pace",
            "Rotate examples for weak areas",
            "Maintain spaced review cadence"
        ]

    if weak_areas:
        actions.append(f"Focus weak areas: {', '.join(weak_areas[:3])}")

    return {"mode": mode, "actions": actions}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", required=True)
    ap.add_argument("--data-root", default="data")
    ap.add_argument("--out")
    args = ap.parse_args()

    slug = args.subject.strip().lower().replace(" ", "-")
    sdir = Path(args.data_root) / "subjects" / slug
    progress = load_json(sdir / "progress.json", {"metrics": {}, "weak_areas": []})

    payload = {
        "subject": args.subject,
        "recommendation": recommend(progress.get("metrics", {}), progress.get("weak_areas", [])),
    }

    out = Path(args.out) if args.out else (sdir / "intervention.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(str(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
