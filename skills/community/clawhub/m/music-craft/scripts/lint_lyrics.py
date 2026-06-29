#!/usr/bin/env python3
"""Lint generated or user-provided lyrics before spending a music generation."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ALLOWED_TAGS = {
    "intro",
    "verse",
    "pre chorus",
    "chorus",
    "bridge",
    "outro",
    "interlude",
    "transition",
    "post chorus",
    "hook",
    "break",
    "build up",
    "inst",
    "solo",
    "instrumental",
    "instrumental break",
}

TAG_RE = re.compile(r"\[[^\]]+\]")
VOWEL_GROUP_RE = re.compile(r"[aeiouyAEIOUYáéíóúÁÉÍÓÚàèìòùÀÈÌÒÙäëïöüÄËÏÖÜãõÃÕâêîôûÂÊÎÔÛ]+")
WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ']+")


def extract_tags(text: str) -> list[str]:
    return TAG_RE.findall(text)


def canonical_tag(tag: str) -> str:
    value = tag.strip()[1:-1].strip().lower()
    value = re.sub(r"[_-]+", " ", value)
    value = re.sub(r"\s+", " ", value)
    value = re.sub(r"\s+\d+$", "", value)
    return value


def invalid_tags(text: str) -> list[str]:
    invalid: list[str] = []
    for tag in extract_tags(text):
        if canonical_tag(tag) not in ALLOWED_TAGS:
            invalid.append(tag)
    return invalid


def count_syllables(text: str) -> int:
    total = 0
    for word in WORD_RE.findall(re.sub(TAG_RE, " ", text)):
        groups = VOWEL_GROUP_RE.findall(word)
        total += max(1, len(groups))
    return total


def estimate_duration(text: str, bpm: int | None, target_seconds: int | None = None) -> dict[str, Any]:
    syllables = count_syllables(text)
    if not bpm or bpm <= 0:
        return {
            "bpm": bpm,
            "syllables": syllables,
            "estimated_lyrics_seconds": None,
            "target_seconds": target_seconds,
            "recommendation": "provide BPM to estimate lyric pacing",
        }
    estimated = int(round((syllables / bpm) * 60 * 1.2))
    recommendation = "ok"
    if target_seconds and estimated > target_seconds * 1.15:
        recommendation = "lyrics are dense for the target duration; shorten lyrics or use a longer/exact-duration backend"
    elif target_seconds and target_seconds > 150 and estimated > target_seconds * 0.75:
        recommendation = "long lyric-heavy generation; cloud duration may undershoot, prefer ACE-Step if exact length matters"
    return {
        "bpm": bpm,
        "syllables": syllables,
        "estimated_lyrics_seconds": estimated,
        "target_seconds": target_seconds,
        "recommendation": recommendation,
    }


def lint_lyrics_text(text: str, bpm: int | None = None, target_seconds: int | None = None) -> dict[str, Any]:
    tags = extract_tags(text)
    bad_tags = invalid_tags(text)
    warnings: list[str] = []
    if not tags:
        warnings.append("no lyrics section tags found")
    if bad_tags:
        warnings.append(
            "invalid lyrics tags: "
            + ", ".join(bad_tags)
            + "; use only canonical structure tags because bracket text may be sung"
        )
    duration_estimate = estimate_duration(text, bpm=bpm, target_seconds=target_seconds)
    if duration_estimate["recommendation"] != "ok":
        warnings.append(duration_estimate["recommendation"])
    return {
        "status": "blocked" if bad_tags else "ok",
        "tags": tags,
        "invalid_tags": bad_tags,
        "allowed_tags": sorted(f"[{tag.title()}]" for tag in ALLOWED_TAGS),
        "duration_estimate": duration_estimate,
        "warnings": warnings,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lint lyrics tags and estimate lyric pacing.")
    parser.add_argument("lyrics_file", help="Path to a lyrics text file.")
    parser.add_argument("--bpm", type=int, help="Song BPM for lyric duration estimate.")
    parser.add_argument("--target-seconds", type=int, help="Target song duration in seconds.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    text = Path(args.lyrics_file).read_text(encoding="utf-8")
    result = lint_lyrics_text(text, bpm=args.bpm, target_seconds=args.target_seconds)
    json.dump(result, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    return 1 if result["status"] == "blocked" else 0


if __name__ == "__main__":
    raise SystemExit(main())
