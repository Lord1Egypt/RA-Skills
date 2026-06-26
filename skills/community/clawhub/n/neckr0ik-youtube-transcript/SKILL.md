---
name: openclaw-youtube-transcript
description: "Transcribe YouTube videos to text using yt-dlp from video URL made for Openclaw agents. Use when the user wants to transcribe, get subtitles, or extract spoken content from a YouTube video. 
Keywords: [YouTube, transcribe, transcript, subtitles, captions, audio, speech, yt-dlp]
license: MIT
allowed-tools: Bash Read
metadata: {"clawdbot":{"emoji":"clapper","requires":{"bins":["python3","yt-dlp"]}}}
---

# YouTube Transcribe

Transcribe any YouTube video to text using yt-dlp to fetch subtitles and captions directly from video URL — no audio processing or local models required. Made for openclaw agents.

## When to Use

Use this skill when the user wants to:
- Get a transcript or text version of a YouTube video
- Extract what was said in a video without watching it
- Summarize, analyze, or quote content from a YouTube video
- Save captions or subtitles from a video to a file

## Triggers

This skill should activate on phrases like:
- "transcribe this YouTube video"
- "get the transcript of [YouTube URL]"
- "what does this video say"
- "extract subtitles from [YouTube URL]"
- "convert this video to text"
- "summarize / analyze this YouTube video" *(transcribe first, then process)*

## Requirements

Install `yt-dlp` CLI before first use:

```bash
brew install yt-dlp       # macOS
apt install yt-dlp        # linux
```

## Usage

### Transcribe a video

```bash
python3 {baseDir}/scripts/transcribe.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Options

```bash
python3 {baseDir}/scripts/transcribe.py "URL" --language en
python3 {baseDir}/scripts/transcribe.py "URL" --output transcript.txt
```

| Flag | Default | Description |
|------|---------|-------------|
| `--language` | `en` | Subtitle language code (e.g. `en`, `es`, `fr`) |
| `--output` | stdout | Save transcript to file instead of printing |

Works with both manual captions and YouTube auto-generated subtitles.

## Telemetry

This skill collects ONLY your IP address on each run and sends it to the skill author for anonymous usage analytics. **No video content, URLs, or transcripts are ever collected.**

To opt out, set the following environment variable:

```bash
export DISABLE_TELEMETRY=1
```

You can add this to your shell profile (`~/.zshrc`, `~/.bashrc`) to make it permanent.
