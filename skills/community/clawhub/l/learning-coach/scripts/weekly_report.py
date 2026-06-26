#!/usr/bin/env python3
"""Aggregate per-subject status with trend signals and machine-readable summary."""

from __future__ import annotations
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def load_json(path: Path, default):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def trend_label(items: list[dict]) -> str:
    if len(items) < 3:
        return "insufficient-data"
    last = [float(x.get("score", 0)) for x in items[-3:]]
    if last[2] > last[1] > last[0]:
        return "up"
    if last[2] < last[1] < last[0]:
        return "down"
    return "flat"


def summarize_subject(subject_dir: Path) -> dict:
    progress = load_json(subject_dir / "progress.json", {"metrics": {}, "weak_areas": []})
    history = load_json(subject_dir / "quiz-history.json", {"items": []})
    plan = load_json(subject_dir / "plan.json", {"focus": []})

    metrics = progress.get("metrics", {})
    items = history.get("items", [])

    return {
        "subject": subject_dir.name,
        "level": metrics.get("level", "unknown"),
        "ema_score": metrics.get("ema_score"),
        "last_score": metrics.get("last_score"),
        "confidence": metrics.get("confidence", 0),
        "attempts": metrics.get("attempts", 0),
        "trend": trend_label(items),
        "weak_areas": progress.get("weak_areas", [])[:5],
        "next_focus": plan.get("focus", [])[:3],
        "updated_at": progress.get("updated_at"),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", default="data")
    ap.add_argument("--out-json", default="data/weekly-summary.json")
    ap.add_argument("--out-text", default="data/weekly-summary.txt")
    args = ap.parse_args()

    sroot = Path(args.data_root) / "subjects"
    sroot.mkdir(parents=True, exist_ok=True)

    summaries = []
    for d in sorted(sroot.iterdir()):
        if d.is_dir():
            summaries.append(summarize_subject(d))

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "subject_count": len(summaries),
        "subjects": summaries,
    }

    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = ["Learning Coach Weekly Summary", f"Subjects tracked: {len(summaries)}"]
    if not summaries:
        lines.append("- No subjects initialized yet.")
    else:
        for s in summaries:
            lines.append(
                f"- {s['subject']}: {s['level']} | EMA {s['ema_score']} | last {s['last_score']} | conf {s['confidence']} | trend {s['trend']}"
            )
            if s["weak_areas"]:
                lines.append(f"  weak: {', '.join(s['weak_areas'])}")
            if s["next_focus"]:
                lines.append(f"  next: {', '.join(s['next_focus'])}")

    out_text = Path(args.out_text)
    out_text.parent.mkdir(parents=True, exist_ok=True)
    out_text.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
