#!/usr/bin/env python3
"""Update per-subject progress with EMA trend + confidence tracking."""

from __future__ import annotations
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ALPHA = 0.35


def level_from_score(score: float) -> str:
    if score < 45:
        return "beginner"
    if score < 75:
        return "intermediate"
    return "advanced"


def load_json(path: Path, default):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", required=True)
    ap.add_argument("--grading", required=True, help="Path to grading JSON (references/grading-schema.md)")
    ap.add_argument("--data-root", default="data")
    args = ap.parse_args()

    now = datetime.now(timezone.utc).isoformat()
    subject_slug = args.subject.strip().lower().replace(" ", "-")

    base = Path(args.data_root) / "subjects" / subject_slug
    base.mkdir(parents=True, exist_ok=True)

    progress_path = base / "progress.json"
    history_path = base / "quiz-history.json"

    progress = load_json(progress_path, {
        "subject": args.subject,
        "metrics": {
            "attempts": 0,
            "ema_score": None,
            "last_score": None,
            "delta_vs_ema": None,
            "confidence": 0,
            "level": "beginner"
        },
        "weak_areas": [],
        "updated_at": None
    })

    history = load_json(history_path, {"items": []})
    grading = json.loads(Path(args.grading).read_text(encoding="utf-8"))

    score = float(grading.get("overall_percent", 0))
    weak = grading.get("weak_concepts", []) if isinstance(grading.get("weak_concepts", []), list) else []

    m = progress.setdefault("metrics", {})
    attempts = int(m.get("attempts", 0)) + 1
    prev_ema = m.get("ema_score")
    ema = score if prev_ema is None else (ALPHA * score + (1 - ALPHA) * float(prev_ema))
    delta = score - ema

    # confidence rises with attempts and consistency (smaller abs delta)
    consistency_bonus = max(0.0, 20.0 - min(20.0, abs(delta)))
    confidence = min(100.0, attempts * 6.0 + consistency_bonus)

    m.update({
        "attempts": attempts,
        "ema_score": round(ema, 2),
        "last_score": round(score, 2),
        "delta_vs_ema": round(delta, 2),
        "confidence": round(confidence, 2),
        "level": level_from_score(ema),
    })

    progress["weak_areas"] = weak[:15]
    progress["updated_at"] = now

    history.setdefault("items", []).append({
        "at": now,
        "score": round(score, 2),
        "ema_score": round(ema, 2),
        "level": level_from_score(ema),
        "weak_concepts": weak[:10],
        "summary": grading.get("summary", "")
    })
    history["items"] = history["items"][-300:]

    progress_path.write_text(json.dumps(progress, indent=2), encoding="utf-8")
    history_path.write_text(json.dumps(history, indent=2), encoding="utf-8")

    print(str(progress_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
