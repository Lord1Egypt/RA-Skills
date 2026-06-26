#!/usr/bin/env python3
"""Analyze a playlist JSON and output taste profile.

Usage: python3 analyze_taste.py < playlist.json

Input: JSON array from fetch_playlist.py
Output: Human-readable taste profile to stdout, JSON stats to stderr.
"""

import json
import random
import sys
from collections import Counter


def is_cjk(char: str) -> bool:
    return any(
        start <= ord(char) <= end
        for start, end in [
            (0x4E00, 0x9FFF),  # CJK Unified
            (0x3400, 0x4DBF),  # CJK Extension A
            (0x3000, 0x303F),  # CJK Symbols
        ]
    )


def is_hiragana_katakana(char: str) -> bool:
    return 0x3040 <= ord(char) <= 0x30FF


def analyze(tracks: list[dict]) -> dict:
    artist_counter = Counter()
    lang_counter = Counter({"chinese": 0, "english": 0, "japanese": 0, "korean": 0, "other": 0})

    for t in tracks:
        # Count artists
        for a in t.get("artists", "").split("/"):
            a = a.strip()
            if a:
                artist_counter[a] += 1

        # Estimate language from title
        name = t.get("name", "")
        has_cjk = any(is_cjk(c) for c in name)
        has_jp = any(is_hiragana_katakana(c) for c in name)
        has_latin = any("a" <= c.lower() <= "z" for c in name)

        if has_jp:
            lang_counter["japanese"] += 1
        elif has_cjk:
            lang_counter["chinese"] += 1
        if has_latin and not has_cjk:
            lang_counter["english"] += 1
        elif not has_cjk and not has_latin:
            lang_counter["other"] += 1

    total = len(tracks)
    top_artists = artist_counter.most_common(20)

    return {
        "total_tracks": total,
        "unique_artists": len(artist_counter),
        "top_artists": top_artists,
        "language_distribution": dict(lang_counter),
    }


if __name__ == "__main__":
    tracks = json.load(sys.stdin)
    stats = analyze(tracks)

    print("=== Taste Profile ===")
    print(f"Total tracks: {stats['total_tracks']}")
    print(f"Unique artists: {stats['unique_artists']}")
    print()
    print("Top Artists:")
    for name, count in stats["top_artists"]:
        print(f"  {name}: {count}")
    print()
    print("Language Mix:")
    for lang, count in stats["language_distribution"].items():
        if count > 0:
            pct = round(count / stats["total_tracks"] * 100, 1)
            print(f"  {lang}: {count} ({pct}%)")

    # Output JSON stats to stderr
    json_stats = {k: v for k, v in stats.items() if k != "top_artists"}
    json_stats["top_artists"] = [(n, c) for n, c in stats["top_artists"]]
    print(json.dumps(json_stats, ensure_ascii=False), file=sys.stderr)
