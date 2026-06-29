#!/usr/bin/env python3
"""Compare expected lyrics with a post-generation transcript."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


TAG_RE = re.compile(r"\[[^\]]+\]")
WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ']+")
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "de",
    "el",
    "en",
    "for",
    "i",
    "in",
    "la",
    "le",
    "me",
    "mi",
    "of",
    "oh",
    "on",
    "the",
    "to",
    "tu",
    "un",
    "una",
    "with",
    "y",
}
TAG_WORDS = {"intro", "verse", "chorus", "bridge", "outro", "section", "lyrics"}


def _strip_tags(text: str) -> str:
    return TAG_RE.sub(" ", text)


def _words(text: str) -> list[str]:
    return [word.lower() for word in WORD_RE.findall(text)]


def _keywords(text: str) -> set[str]:
    return {word for word in _words(text) if len(word) > 2 and word not in STOPWORDS}


def transcript_from_json(data: dict[str, Any]) -> str:
    if isinstance(data.get("text"), str):
        return data["text"]
    segments = data.get("segments")
    if isinstance(segments, list):
        return " ".join(str(segment.get("text", "")) for segment in segments if isinstance(segment, dict))
    return ""


def compare_lyrics(expected_lyrics: str, transcript: str, min_overlap: float = 0.45) -> dict[str, Any]:
    expected_clean = _strip_tags(expected_lyrics)
    expected_keywords = _keywords(expected_clean)
    transcript_keywords = _keywords(transcript)
    matched = sorted(expected_keywords & transcript_keywords)
    overlap = (len(matched) / len(expected_keywords)) if expected_keywords else 0.0
    missing_keywords = sorted(expected_keywords - transcript_keywords)[:20]
    warnings: list[str] = []
    if overlap < min_overlap:
        warnings.append(
            f"low lyric overlap: {overlap:.2f} below threshold {min_overlap:.2f}"
        )
    sung_tag_words = sorted((transcript_keywords - _keywords(expected_clean)) & TAG_WORDS)
    if sung_tag_words:
        warnings.append(
            "possible sung structure tags in transcript: " + ", ".join(sung_tag_words)
        )
    return {
        "status": "failed" if overlap < min_overlap else ("warn" if warnings else "ok"),
        "word_overlap": round(overlap, 3),
        "matched_keywords": matched[:30],
        "missing_keywords": missing_keywords,
        "warnings": warnings,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify expected lyrics against a transcript.")
    parser.add_argument("--expected-lyrics-file", required=True, help="Path to expected lyrics text.")
    parser.add_argument("--transcript-json", help="Path to JSON from extract_lyrics_whisper.py.")
    parser.add_argument("--transcript-file", help="Plain-text transcript file.")
    parser.add_argument("--min-overlap", type=float, default=0.45)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    expected = Path(args.expected_lyrics_file).read_text(encoding="utf-8")
    if args.transcript_json:
        data = json.loads(Path(args.transcript_json).read_text(encoding="utf-8"))
        transcript = transcript_from_json(data)
    elif args.transcript_file:
        transcript = Path(args.transcript_file).read_text(encoding="utf-8")
    else:
        raise SystemExit("provide --transcript-json or --transcript-file")
    result = compare_lyrics(expected, transcript, min_overlap=args.min_overlap)
    json.dump(result, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    return 1 if result["status"] == "failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
