#!/usr/bin/env python3
"""Summarize Demucs stems into a small arranger-oriented report.

This is intentionally lightweight. It reads the `stems.json` emitted by
extract_stems.py, validates paths, and produces a non-musician-friendly report
that can guide whether deeper per-stem analysis is worth running.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


EXPECTED_STEMS = ("vocals", "drums", "bass", "other")


def _load_stems(stems_json: Path) -> dict[str, Path]:
    data = json.loads(stems_json.read_text(encoding="utf-8"))
    raw_stems = data.get("stems")
    if not isinstance(raw_stems, dict):
        raise ValueError("stems.json must contain a 'stems' object")
    stems = {name: Path(path) for name, path in raw_stems.items()}
    missing = [name for name in EXPECTED_STEMS if name not in stems]
    if missing:
        raise ValueError(f"missing expected stems: {', '.join(missing)}")
    return stems


def _duration_seconds(path: Path) -> float | None:
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(path),
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None
    try:
        return round(float(result.stdout.strip()), 2)
    except ValueError:
        return None


def build_stem_report(stems_json: Path) -> dict[str, object]:
    stems = _load_stems(stems_json)
    report: dict[str, object] = {
        "status": "ok",
        "stems_json": str(stems_json),
        "stems": {},
        "mix_notes": [],
        "recommendations": [],
    }
    stem_entries: dict[str, dict[str, object]] = {}
    sizes: dict[str, int] = {}
    for name, path in stems.items():
        exists = path.exists()
        size = path.stat().st_size if exists else 0
        sizes[name] = size
        stem_entries[name] = {
            "path": str(path),
            "exists": exists,
            "size_bytes": size,
            "duration_seconds": _duration_seconds(path) if exists else None,
        }
    report["stems"] = stem_entries

    if any(not entry["exists"] for entry in stem_entries.values()):
        report["status"] = "missing_stems"
        report["recommendations"] = ["Re-run extract_stems.py before per-stem analysis."]
        return report

    total = sum(sizes.values()) or 1
    dominant_name, dominant_size = max(sizes.items(), key=lambda item: item[1])
    dominant_ratio = dominant_size / total
    quiet = [name for name, size in sizes.items() if size / total < 0.08]
    notes: list[str] = []
    recommendations: list[str] = []
    if dominant_ratio > 0.45:
        notes.append(f"{dominant_name} appears dominant by file size ({dominant_ratio:.0%} of stem bytes).")
        recommendations.append(f"Review the {dominant_name} stem first; it may be masking other layers.")
    if quiet:
        notes.append(f"Quiet or low-information stems by size: {', '.join(sorted(quiet))}.")
        recommendations.append("Check whether quiet stems are intentional or stem-separation bleed/artifacts.")
    recommendations.append("Run full-mix Whisper for lyrics; use stems for timbre, pitch, and mix decisions.")
    recommendations.append("Use this report as triage, then run deeper analysis only on suspicious stems.")
    report["mix_notes"] = notes or ["No single stem is obviously dominant by file-size heuristic."]
    report["recommendations"] = recommendations
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build a lightweight per-stem report from stems.json")
    parser.add_argument("stems_json", type=Path)
    parser.add_argument("--output", "-o", type=Path)
    args = parser.parse_args(argv)

    try:
        report = build_stem_report(args.stems_json.expanduser())
    except Exception as exc:  # noqa: BLE001 - CLI should emit JSON error
        report = {"status": "error", "error": str(exc)}
        rc = 1
    else:
        rc = 0
    text = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
