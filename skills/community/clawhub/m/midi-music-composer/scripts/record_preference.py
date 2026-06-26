#!/usr/bin/env python3
"""Record simple user preference memory from generated song manifests."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DEFAULT_MEMORY = {
    "liked_genres": [],
    "disliked_genres": [],
    "liked_instruments": [],
    "disliked_instruments": [],
    "liked_harmony": [],
    "disliked_harmony": [],
    "liked_form": [],
    "disliked_form": [],
    "liked_texture": [],
    "disliked_texture": [],
    "notes": [],
    "rated_songs": [],
}


def load(path: Path) -> dict[str, Any]:
    if not path.exists():
        return dict(DEFAULT_MEMORY)
    data = json.loads(path.read_text(encoding="utf-8"))
    merged = dict(DEFAULT_MEMORY)
    merged.update(data)
    return merged


def append_unique(values: list[str], value: str) -> None:
    if value and value not in values:
        values.append(value)


def infer_rating(opinion: str) -> str:
    lower = opinion.lower()
    positive = ["liked", "love", "good", "better", "great", "beautiful", "nice", "works", "cool"]
    negative = ["disliked", "bad", "flat", "boring", "repetitive", "wrong", "hate", "meh", "busy"]
    pos_score = sum(word in lower for word in positive)
    neg_score = sum(word in lower for word in negative)
    return "like" if pos_score >= neg_score else "dislike"


def extract_tags(opinion: str) -> dict[str, list[str]]:
    lower = opinion.lower()
    tags = {
        "harmony": [],
        "form": [],
        "texture": [],
    }
    harmony_terms = ["chord", "chords", "harmony", "progression", "cadence", "resolution", "flat", "spicy"]
    form_terms = ["intro", "theme", "variation", "return", "coda", "ending", "repetitive", "loop"]
    texture_terms = ["instrument", "lead", "bass", "drums", "pad", "flute", "synth", "strings", "busy", "sparse"]
    for term in harmony_terms:
        if term in lower:
            tags["harmony"].append(term)
    for term in form_terms:
        if term in lower:
            tags["form"].append(term)
    for term in texture_terms:
        if term in lower:
            tags["texture"].append(term)
    return tags


def local_sentiment(opinion: str, term: str, fallback: str) -> str:
    lower = opinion.lower()
    index = lower.find(term)
    if index < 0:
        return fallback
    window = lower[max(0, index - 32): index + len(term) + 32]
    positive = ["liked", "like", "love", "good", "great", "better", "nice"]
    negative = ["flat", "boring", "repetitive", "bad", "busy", "meh", "wrong", "dislike"]
    pos_score = sum(word in window for word in positive)
    neg_score = sum(word in window for word in negative)
    if pos_score > neg_score:
        return "like"
    if neg_score > pos_score:
        return "dislike"
    return fallback


def record_tag(memory: dict[str, Any], category: str, tag: str, sentiment: str) -> None:
    key = f"{'liked' if sentiment == 'like' else 'disliked'}_{category}"
    append_unique(memory[key], tag)


def main() -> None:
    parser = argparse.ArgumentParser(description="Record preference memory for music-composer.")
    parser.add_argument("manifest", type=Path, help="Generated song manifest JSON.")
    parser.add_argument("--memory", type=Path, default=Path.home() / ".hermes" / "music-composer-preferences.json")
    parser.add_argument("--rating", choices=["like", "dislike"], default=None)
    parser.add_argument("--note", default="")
    parser.add_argument("--opinion", default="", help="Free-form user opinion; rating is inferred if --rating is omitted.")
    args = parser.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    memory = load(args.memory)
    note = args.note or args.opinion
    rating = args.rating or infer_rating(note)
    genre = str(manifest.get("genre", ""))
    instruments = manifest.get("instruments", {})
    main_melody = str(instruments.get("main_melody", "")) if isinstance(instruments, dict) else ""
    tags = extract_tags(note)

    if rating == "like":
        append_unique(memory["liked_genres"], genre)
        append_unique(memory["liked_instruments"], main_melody)
    else:
        append_unique(memory["disliked_genres"], genre)
        append_unique(memory["disliked_instruments"], main_melody)
    for tag in tags["harmony"]:
        record_tag(memory, "harmony", tag, local_sentiment(note, tag, rating))
    for tag in tags["form"]:
        record_tag(memory, "form", tag, local_sentiment(note, tag, rating))
    for tag in tags["texture"]:
        record_tag(memory, "texture", tag, local_sentiment(note, tag, rating))

    if note:
        memory["notes"].append(note)
    memory["rated_songs"].append(
        {
            "title": manifest.get("title"),
            "rating": rating,
            "genre": genre,
            "main_melody": main_melody,
            "quality_score": manifest.get("quality_score"),
            "note": note,
            "tags": tags,
        }
    )

    args.memory.parent.mkdir(parents=True, exist_ok=True)
    args.memory.write_text(json.dumps(memory, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(memory, indent=2))


if __name__ == "__main__":
    main()
