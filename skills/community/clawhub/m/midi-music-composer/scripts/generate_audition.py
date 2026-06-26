#!/usr/bin/env python3
"""Generate blind candidate sets for user rating."""

from __future__ import annotations

import argparse
import json
import string
import time
from pathlib import Path
from random import Random
from typing import Any

from generate_song import build_song, load_preferences, slugify, stable_seed


def public_candidate(label: str, manifest: dict[str, Any]) -> dict[str, Any]:
    midi_file = str(manifest.get("midi_file", ""))
    return {
        "label": label,
        "midi_file": midi_file,
        "audio_file": manifest.get("audio_file"),
        "manifest_file": midi_file.replace(".mid", ".json"),
        "composition_file": manifest.get("composition_file"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a blind audition set for music-composer.")
    parser.add_argument("title")
    parser.add_argument("--out", default="out", help="Output directory.")
    parser.add_argument("--candidates", type=int, default=4, help="Number of blind candidates to generate.")
    parser.add_argument("--preferences", type=Path, default=None, help="Optional JSON preference memory file.")
    parser.add_argument("--render-audio", action="store_true", help="Try to render WAV previews when local tools exist.")
    parser.add_argument("--soundfont", type=Path, default=None, help="Optional soundfont path for fluidsynth.")
    args = parser.parse_args()

    count = max(2, min(args.candidates, len(string.ascii_uppercase)))
    labels = list(string.ascii_uppercase[:count])
    preferences = load_preferences(args.preferences)
    run_id = time.strftime("%Y%m%d-%H%M%S")
    audition_dir = Path(args.out) / f"{slugify(args.title)}-audition-{run_id}"
    audition_dir.mkdir(parents=True, exist_ok=True)

    variants = list(range(count))
    rng = Random(stable_seed(args.title, 30_000 + count))
    rng.shuffle(variants)

    candidates = []
    for label, variant in zip(labels, variants):
        manifest = build_song(
            args.title,
            audition_dir,
            variant=variant,
            suffix=f"-{label.lower()}",
            preferences=preferences,
            render_audio=args.render_audio,
            soundfont=args.soundfont,
        )
        candidates.append(public_candidate(label, manifest))

    audition = {
        "title": args.title,
        "created_at": run_id,
        "mode": "blind_audition",
        "candidate_count": count,
        "candidates": candidates,
        "instructions": "Ask the user to rate each label from 1-5 without showing score, genre, harmony, or critic metadata.",
    }
    audition_path = audition_dir / "audition.json"
    audition_path.write_text(json.dumps(audition, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "audition_file": str(audition_path),
        "title": args.title,
        "candidates": candidates,
    }, indent=2))


if __name__ == "__main__":
    main()
