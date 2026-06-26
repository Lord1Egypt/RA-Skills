#!/usr/bin/env python3
"""Record blind audition ratings and critic alignment."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from record_preference import append_unique, load


DEFAULT_MEMORY = Path.home() / ".hermes" / "music-composer-preferences.json"


def parse_ratings(raw: str) -> dict[str, int]:
    raw = raw.strip()
    if not raw:
        raise ValueError("ratings are required, for example: A=4,B=2,C=5,D=3")
    if raw.startswith("{"):
        data = json.loads(raw)
        return {str(label).upper(): int(value) for label, value in data.items()}
    ratings: dict[str, int] = {}
    for part in raw.replace(" ", "").split(","):
        if not part:
            continue
        if "=" in part:
            label, value = part.split("=", 1)
        elif ":" in part:
            label, value = part.split(":", 1)
        else:
            raise ValueError(f"Could not parse rating segment: {part}")
        ratings[label.upper()] = int(value)
    return ratings


def load_manifest(candidate: dict[str, Any]) -> dict[str, Any]:
    path = Path(str(candidate["manifest_file"]))
    return json.loads(path.read_text(encoding="utf-8"))


def ensure_memory_shape(memory: dict[str, Any]) -> None:
    memory.setdefault("auditions", [])
    memory.setdefault("critic_calibration", {"agreements": 0, "disagreements": 0, "samples": []})
    memory.setdefault("liked_harmony", [])
    memory.setdefault("disliked_harmony", [])


def candidate_features(manifest: dict[str, Any]) -> dict[str, Any]:
    instruments = manifest.get("instruments", {})
    main_melody = instruments.get("main_melody", "") if isinstance(instruments, dict) else ""
    return {
        "genre": manifest.get("genre"),
        "main_melody": main_melody,
        "harmonic_strategy": manifest.get("harmonic_strategy"),
        "chords": manifest.get("chords"),
        "quality_score": manifest.get("quality_score"),
    }


def append_value(values: list[str], value: Any) -> None:
    text = str(value or "")
    if text:
        append_unique(values, text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Record blind audition ratings for music-composer.")
    parser.add_argument("audition", type=Path, help="Audition JSON from generate_audition.py.")
    parser.add_argument("--ratings", required=True, help='Ratings like "A=4,B=2,C=5,D=3" or JSON.')
    parser.add_argument("--opinion", default="", help="Optional free-form user notes.")
    parser.add_argument("--memory", type=Path, default=DEFAULT_MEMORY)
    args = parser.parse_args()

    audition = json.loads(args.audition.read_text(encoding="utf-8"))
    ratings = parse_ratings(args.ratings)
    manifests = {
        str(candidate["label"]).upper(): load_manifest(candidate)
        for candidate in audition.get("candidates", [])
    }
    missing = sorted(set(manifests) - set(ratings))
    if missing:
        raise ValueError("Missing ratings for: " + ", ".join(missing))

    ordered_by_user = sorted(ratings.items(), key=lambda item: (-item[1], item[0]))
    winner_label = ordered_by_user[0][0]
    loser_label = sorted(ratings.items(), key=lambda item: (item[1], item[0]))[0][0]
    critic_label = max(
        manifests,
        key=lambda label: (int(manifests[label].get("quality_score", 0)), -ord(label[0])),
    )
    agreement = winner_label == critic_label

    winner = manifests[winner_label]
    loser = manifests[loser_label]
    memory = load(args.memory)
    ensure_memory_shape(memory)

    winner_features = candidate_features(winner)
    loser_features = candidate_features(loser)
    append_value(memory["liked_genres"], winner_features["genre"])
    append_value(memory["liked_instruments"], winner_features["main_melody"])
    append_value(memory["liked_harmony"], winner_features["harmonic_strategy"])
    for chord in winner_features.get("chords") or []:
        append_value(memory["liked_harmony"], chord)

    append_value(memory["disliked_genres"], loser_features["genre"])
    append_value(memory["disliked_instruments"], loser_features["main_melody"])
    append_value(memory["disliked_harmony"], loser_features["harmonic_strategy"])

    calibration = memory["critic_calibration"]
    if agreement:
        calibration["agreements"] = int(calibration.get("agreements", 0)) + 1
    else:
        calibration["disagreements"] = int(calibration.get("disagreements", 0)) + 1
    calibration.setdefault("samples", []).append(
        {
            "title": audition.get("title"),
            "ratings": ratings,
            "winner": winner_label,
            "critic_pick": critic_label,
            "agreement": agreement,
            "winner_features": winner_features,
            "critic_features": candidate_features(manifests[critic_label]),
            "opinion": args.opinion,
        }
    )
    memory["auditions"].append(
        {
            "title": audition.get("title"),
            "audition_file": str(args.audition),
            "ratings": ratings,
            "winner": winner_label,
            "loser": loser_label,
            "critic_pick": critic_label,
            "agreement": agreement,
            "opinion": args.opinion,
        }
    )
    if args.opinion:
        memory["notes"].append(args.opinion)

    args.memory.parent.mkdir(parents=True, exist_ok=True)
    args.memory.write_text(json.dumps(memory, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "title": audition.get("title"),
        "winner": winner_label,
        "loser": loser_label,
        "critic_pick": critic_label,
        "agreement": agreement,
        "winner_features": winner_features,
        "memory_file": str(args.memory),
    }, indent=2))


if __name__ == "__main__":
    main()
