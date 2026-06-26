---
name: hn-podcast-transcribe
description: >
  Download, transcribe, and archive Hacker News podcast episodes (e.g. "Hacker News Recap" by Wondercraft).
  Use when: (1) user wants to transcribe HN podcast episodes, (2) user asks to archive HN podcast content,
  (3) user wants searchable text from HN audio podcasts, (4) user mentions "HN podcast" + "transcribe" or "archive".
  Supports incremental processing — only new episodes are downloaded/transcribed on each run.
  Works with any podcast RSS feed, not just HN.
---

# HN Podcast Transcribe & Archive

Automatically download, transcribe, and archive Hacker News podcast episodes into a searchable local archive.

## Default Podcast

**Hacker News Recap** by Wondercraft.ai — daily AI-generated recap of top HN posts.
- RSS: `https://rss.buzzsprout.com/2170103.rss`

Override with `HN_PODCAST_RSS` env var for any podcast RSS feed.

## Workflow

### 1. Fetch new episodes

```bash
python3 scripts/fetch_episodes.py [--rss URL] [--archive DIR] [--limit N] [--no-download]
```

- Parses podcast RSS feed
- Compares against existing archive to skip already-processed episodes
- Downloads audio (mp3/m4a/wav) for each new episode
- Saves metadata as JSON alongside audio
- Default archive: `./hn-podcast-archive/`
- `--no-download`: save metadata only, skip audio download

**Download strategies** (tried in order):
1. Direct HTTP download — works for most podcast CDNs
2. yt-dlp fallback — handles some Cloudflare-protected hosts
3. If both fail, the episode directory is created with metadata; place audio manually

**Cloudflare note**: Some hosts (e.g. Buzzsprout) block automated downloads. If direct download fails:
- Use `--no-download` to create the directory structure
- Download audio manually via browser or podcast app
- Place the file as `audio.mp3` in the episode directory
- Re-run the transcribe step

### 2. Transcribe audio

```bash
python3 scripts/transcribe_episodes.py [--archive DIR] [--model MODEL] [--format FORMAT]
```

- Finds episodes with audio but no transcript
- Runs Whisper locally (no API key needed)
- Outputs: `txt`, `srt`, `vtt`, or `json` (default: `txt`)
- Default model: `turbo` (fast, good accuracy)
- Supports audio formats: mp3, m4a, wav, ogg, flac

### 3. Generate archive index

```bash
python3 scripts/build_index.py [--archive DIR]
```

- Creates `archive_index.json` with all episodes, dates, titles, and transcript paths
- Enables fast search across the archive

### 4. Search archive

```bash
python3 scripts/search_archive.py [--archive DIR] "search query"
```

- Full-text search across all transcribed episodes
- Returns matching episodes with context snippets

## One-shot: Full Pipeline

```bash
python3 scripts/pipeline.py [--rss URL] [--archive DIR] [--model MODEL] [--limit N]
```

Runs fetch → transcribe → index in sequence.

## Cron Integration

Set up periodic processing with OpenClaw cron:

```
# Daily at 6am — process new HN Recap episodes
cron add --name "hn-podcast-digest" --schedule "0 6 * * *" --payload '{"kind":"agentTurn","message":"Run the HN podcast transcription pipeline: python3 scripts/pipeline.py --limit 3"}'
```

## Archive Structure

```
hn-podcast-archive/
├── archive_index.json
├── 2026-05-10_hardware-attestation-as-monopoly-enabler/
│   ├── episode.json
│   ├── audio.mp3
│   └── transcript.txt
├── 2026-05-09_a-recent-experience-with-chatgpt-5-5-pro/
│   ├── episode.json
│   ├── audio.mp3
│   └── transcript.txt
└── ...
```

## Configuration

| Env Var | Default | Description |
|---|---|---|
| `HN_PODCAST_RSS` | Buzzsprout HN Recap feed | Podcast RSS feed URL |
| `HN_ARCHIVE_DIR` | `./hn-podcast-archive` | Archive directory |
| `WHISPER_MODEL` | `turbo` | Whisper model name |
| `WHISPER_FORMAT` | `txt` | Transcript output format |

## Requirements

- Python 3.10+
- `openai-whisper` (`pip install openai-whisper`)
- `requests` (`pip install requests`)
- `static-ffmpeg` (`pip install static-ffmpeg`) — auto-provides ffmpeg
- `yt-dlp` (optional, for fallback downloads)
- Whisper models auto-download to `~/.cache/whisper` on first use
