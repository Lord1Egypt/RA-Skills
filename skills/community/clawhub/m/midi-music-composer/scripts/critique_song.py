#!/usr/bin/env python3
"""Critique a generated music-composer manifest.

This is intentionally deterministic and lightweight. It gives Hermes a second
pass that can catch structural problems without needing to render or listen to
audio.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


TONIC_ENDINGS = {"Iadd9", "i9"}
EXPECTED_FORM = ["intro", "A theme", "B variation", "A return", "coda", "resolution"]


def section_names(manifest: dict[str, Any]) -> list[str]:
    return [section.get("name", "") for section in manifest.get("form", [])]


def phrase_signatures(events: list[dict[str, Any]]) -> dict[int, tuple[int, ...]]:
    bars: dict[int, list[int]] = defaultdict(list)
    for event in events:
        bar = int(event.get("bar", 0))
        degree = int(event.get("degree", 0))
        if bar > 0 and degree > 0:
            bars[bar].append(degree)
    return {bar: tuple(degrees) for bar, degrees in bars.items()}


def harmonic_interest(manifest: dict[str, Any]) -> tuple[int, list[str]]:
    chords = [str(chord) for chord in manifest.get("chords", [])]
    strategy = str(manifest.get("harmonic_strategy", "template_color"))
    joined = " ".join(chords)
    score = 0
    findings = []
    non_diatonic_markers = ["b", "#", "/", "dim", "V/"]
    tension_markers = ["V7", "dim", "aug", "iv", "bVI", "bVII", "V/"]
    non_diatonic_count = sum(marker in joined for marker in non_diatonic_markers)
    tension_count = sum(marker in joined for marker in tension_markers)

    if strategy == "template_color" and non_diatonic_count == 0:
        findings.append("Harmony is safe; try a borrowed, dominant, pedal, or diminished strategy.")
        score -= 6
    if strategy != "template_color":
        score += 4
    if non_diatonic_count:
        score += min(8, non_diatonic_count * 3)
    if tension_count >= 2:
        score += 4
    if len(set(chords)) < 4:
        findings.append("Chord loop has too little variety.")
        score -= 5
    return score, findings


def critique(manifest: dict[str, Any]) -> dict[str, Any]:
    findings: list[str] = []
    score = 100

    duration = float(manifest.get("duration_seconds", 0))
    if not 55 <= duration <= 65:
        findings.append(f"Duration is {duration:.2f}s; target is 55-65s.")
        score -= 15

    names = section_names(manifest)
    missing_sections = [name for name in EXPECTED_FORM if name not in names]
    if missing_sections:
        findings.append("Missing form sections: " + ", ".join(missing_sections) + ".")
        score -= 12

    if manifest.get("final_chord") not in TONIC_ENDINGS:
        findings.append("Final chord is not a tonic resolution.")
        score -= 20

    harmonic_score, harmonic_findings = harmonic_interest(manifest)
    score += harmonic_score
    findings.extend(harmonic_findings)

    instruments = manifest.get("instruments", {})
    if manifest.get("main_melody_owner") != instruments.get("main_melody"):
        findings.append("Main melody owner does not match instruments.main_melody.")
        score -= 15

    events = manifest.get("main_melody_events", [])
    signatures = phrase_signatures(events)
    resolution_bar = None
    for section in manifest.get("form", []):
        if section.get("name") == "resolution":
            resolution_bar = int(section.get("start_bar", 0))
            break

    if resolution_bar:
        pre_resolution = [
            signatures.get(bar, tuple())
            for bar in range(max(1, resolution_bar - 4), resolution_bar)
            if signatures.get(bar, tuple())
        ]
        unique_pre_resolution = set(pre_resolution)
        if len(pre_resolution) >= 3 and len(unique_pre_resolution) <= 2:
            findings.append("The last four bars before resolution are too repetitive.")
            score -= 15
        if pre_resolution and pre_resolution[-1] and pre_resolution[-1][-1] not in {1, 2, 3}:
            findings.append("The final pre-resolution phrase does not point strongly toward tonic.")
            score -= 8

    for section in manifest.get("form", []):
        if section.get("name") == "A return" and int(section.get("bar_count", 0)) > 8:
            findings.append("A return is long enough to risk feeling static; keep the coda active.")
            score -= 5

    if not findings:
        findings.append("No structural issues found.")

    return {
        "title": manifest.get("title"),
        "score": max(0, min(100, score)),
        "findings": findings,
        "checks": {
            "duration_seconds": duration,
            "form": names,
            "final_chord": manifest.get("final_chord"),
            "harmonic_strategy": manifest.get("harmonic_strategy"),
            "main_melody_owner": manifest.get("main_melody_owner"),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Critique a generated music-composer manifest.")
    parser.add_argument("manifest", help="Path to the JSON manifest generated by generate_song.py.")
    args = parser.parse_args()

    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    print(json.dumps(critique(manifest), indent=2))


if __name__ == "__main__":
    main()
