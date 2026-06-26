#!/usr/bin/env bash
set -euo pipefail

FEED_URL="${1:-https://example.com/podcast.rss}"
OUTPUT_DIR="${2:-./data/hn-podcast-archive}"
MODEL="${3:-turbo}"

python3 skills/hn-podcast-archive/scripts/hn_podcast_archive.py \
  --feed-url "$FEED_URL" \
  --output-dir "$OUTPUT_DIR" \
  --whisper-model "$MODEL"
