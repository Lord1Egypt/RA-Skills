#!/usr/bin/env python3
"""Build a searchable index of the podcast archive."""

import argparse
import json
import os
from pathlib import Path

DEFAULT_ARCHIVE = os.environ.get("HN_ARCHIVE_DIR", "./hn-podcast-archive")


def build_index(archive_dir: str) -> dict:
    archive = Path(archive_dir)
    if not archive.exists():
        print(f"Archive not found: {archive_dir}", file=sys.stderr)
        return {}

    index = {"episodes": []}
    for d in sorted(archive.iterdir(), reverse=True):
        if not d.is_dir():
            continue
        meta_path = d / "episode.json"
        if not meta_path.exists():
            continue
        with open(meta_path) as f:
            meta = json.load(f)

        entry = {
            "slug": d.name,
            "title": meta.get("title", ""),
            "pub_date": meta.get("pub_date", ""),
            "transcribed": meta.get("transcribed", False),
            "has_audio": any((d / n).exists() for n in ("audio.mp3", "audio.m4a", "audio.wav", "audio.ogg", "audio.flac")),
        }

        # Check for transcript files
        for fmt in ("txt", "srt", "vtt", "json"):
            t = d / f"transcript.{fmt}"
            if t.exists():
                entry["transcript_path"] = str(t)
                entry["transcript_format"] = fmt
                break

        index["episodes"].append(entry)

    index["total"] = len(index["episodes"])
    index["transcribed"] = sum(1 for e in index["episodes"] if e["transcribed"])

    # Write index
    out_path = archive / "archive_index.json"
    with open(out_path, "w") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    print(f"Index: {index['total']} episodes, {index['transcribed']} transcribed → {out_path}")
    return index


def main():
    parser = argparse.ArgumentParser(description="Build archive index")
    parser.add_argument("--archive", default=DEFAULT_ARCHIVE)
    args = parser.parse_args()
    build_index(args.archive)


if __name__ == "__main__":
    main()
