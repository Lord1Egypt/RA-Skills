---
name: hn-podcast-transcriber
description: Automatically fetch, transcribe, and archive Hacker News podcast episodes (Hacker News Morning Brief). Use when the user wants to set up a podcast transcription pipeline, archive HN podcast episodes as searchable text, transcribe podcast audio to markdown, or schedule periodic HN podcast ingestion. Also use for any podcast RSS feed transcription workflow.
---

# HN Podcast Transcriber

Fetch new episodes from the Hacker News Morning Brief podcast RSS feed, transcribe with Whisper, and archive as searchable markdown.

## Prerequisites

- **whisper** CLI installed (`pip install openai-whisper`)
- **ffmpeg** on PATH (required by whisper; download from https://ffmpeg.org)
- **python3** with standard library (no extra deps for the fetch script)
- Disk space for audio files (~5-10 MB per episode)

## Quick Start

Run the main script to fetch and transcribe all new episodes:

```bash
bash scripts/fetch_and_transcribe.sh --archive ~/hn-podcast-archive
```

First run processes all episodes. Subsequent runs only process new ones (tracked via `state.json`).

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--feed URL` | HN Morning Brief RSS | Podcast RSS feed URL |
| `--archive DIR` | `./hn-podcast-archive` | Archive root directory |
| `--model MODEL` | `turbo` | Whisper model (tiny/base/small/medium/large/turbo) |
| `--limit N` | 0 (all) | Max new episodes to process per run |

## Custom Feeds

Point at any podcast RSS feed:

```bash
bash scripts/fetch_and_transcribe.sh --feed "https://example.com/podcast/feed.xml" --archive ./my-podcast-archive
```

## Scheduling

Set up an OpenClaw cron job for daily checks:

1. Create an isolated cron job that runs the script
2. Or add a heartbeat check in HEARTBEAT.md

## Archive Structure

See [references/archive-layout.md](references/archive-layout.md) for directory layout and state.json schema.

## Workflow Summary

1. Download RSS feed → parse `<item>` entries
2. Skip already-processed episodes (state.json lookup)
3. Download audio (mp3/m4a) to episode directory
4. Run `whisper` to produce `.txt` transcript
5. Generate cleaned `transcript.md` with title + date header
6. Update state.json with processed episode ID

## Notes

- Whisper models cache to `~/.cache/whisper` after first download
- Use `--model tiny` for speed, `--model large` for best accuracy
- Average episode (~6 min) takes ~1-2 min with turbo model on CPU
- For GPU acceleration, install ffmpeg with CUDA support