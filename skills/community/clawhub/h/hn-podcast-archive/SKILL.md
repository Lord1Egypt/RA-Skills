---
name: hn-podcast-archive
description: Build and operate an automated archive workflow for the Hacker News podcast/feed: detect new episodes from RSS, download audio, transcribe locally with Whisper, generate markdown archives with metadata, and keep an index/history for repeatable ingestion. Use when setting up or maintaining a podcast transcription/archive pipeline, especially for RSS-based podcasts and local file archives.
---

# HN Podcast Archive

Set up or maintain a repeatable pipeline that:
1. reads an RSS feed,
2. detects new episodes,
3. downloads audio,
4. transcribes with local Whisper,
5. writes a markdown archive per episode,
6. updates index/state files.

## Workflow

1. Read `references/layout.md` to understand the expected archive layout and outputs.
2. Use `scripts/hn_podcast_archive.py` as the primary implementation.
3. Run `python3 scripts/hn_podcast_archive.py --help` to inspect options.
4. For first-time setup, ensure required binaries and Python modules exist.
5. For automation, schedule the script on a recurring cadence with a stable output directory.

## Required runtime dependencies

The script expects:
- `ffmpeg` in PATH
- `whisper` in PATH
- Python 3.10+
- Python package `feedparser`

If any dependency is missing, surface a clear setup note instead of pretending the pipeline is ready to execute.

## Recommended command

```bash
python3 skills/hn-podcast-archive/scripts/hn_podcast_archive.py \
  --feed-url "https://example.com/podcast.rss" \
  --output-dir ./data/hn-podcast-archive \
  --whisper-model turbo
```

## Output expectations

For each ingested episode, create:
- downloaded audio under `audio/`
- transcript under `transcripts/`
- markdown archive under `episodes/`

Keep these shared files current:
- `index.md`
- `state.json`
- `run-log.jsonl`

## Automation guidance

For automation, prefer a cron/standing-order style trigger that runs every few hours. The script is idempotent at the episode level by tracking processed GUIDs/URLs in `state.json`.

## Safe operating rules

- Never overwrite unrelated archive content.
- Skip already-processed episodes unless explicitly forced.
- Preserve source metadata (title, published date, audio URL, guid).
- If transcription fails after download, keep the audio and record the failure in the log/state.

## Customization points

Useful flags:
- `--limit N` to ingest only recent items during testing
- `--force` to reprocess already-seen items
- `--dry-run` to inspect actions without writing outputs
- `--whisper-model` to trade speed vs accuracy

## Packaging/publishing

Package the skill from its folder. Publish with ClawHub only after local validation passes and authentication is available.
