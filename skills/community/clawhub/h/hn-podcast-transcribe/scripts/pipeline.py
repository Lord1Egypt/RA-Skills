#!/usr/bin/env python3
"""One-shot pipeline: fetch → transcribe → index."""

import argparse
import os
import sys

# Add scripts dir to path
sys.path.insert(0, os.path.dirname(__file__))

from fetch_episodes import fetch_episodes
from transcribe_episodes import transcribe_all
from build_index import build_index

DEFAULT_RSS = "https://rss.buzzsprout.com/2170103.rss"
DEFAULT_ARCHIVE = os.environ.get("HN_ARCHIVE_DIR", "./hn-podcast-archive")
DEFAULT_MODEL = os.environ.get("WHISPER_MODEL", "turbo")
DEFAULT_FORMAT = os.environ.get("WHISPER_FORMAT", "txt")


def main():
    parser = argparse.ArgumentParser(description="HN Podcast: fetch → transcribe → index")
    parser.add_argument("--rss", default=os.environ.get("HN_PODCAST_RSS", DEFAULT_RSS))
    parser.add_argument("--archive", default=DEFAULT_ARCHIVE)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--format", default=DEFAULT_FORMAT, choices=["txt", "srt", "vtt", "json"])
    parser.add_argument("--limit", type=int, default=0, help="Max new episodes (0=all)")
    args = parser.parse_args()

    print("=== Step 1: Fetch episodes ===")
    fetch_episodes(args.rss, args.archive, args.limit)

    print("\n=== Step 2: Transcribe ===")
    transcribe_all(args.archive, args.model, args.format)

    print("\n=== Step 3: Build index ===")
    build_index(args.archive)

    print("\n✅ Pipeline complete!")


if __name__ == "__main__":
    main()
