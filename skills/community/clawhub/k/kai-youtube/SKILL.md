---
name: kai-youtube
description: Watch and transcribe YouTube videos using yt-dlp and Whisper CLI. Use when Blaze or Kai wants to watch a YouTube video together, get a video transcript, or summarize video content. Downloads audio with yt-dlp, transcribes with Whisper (OpenAI CLI), and saves everything to the workspace organized folder. Supports any YouTube URL. Trigger phrases: "watch this video", "transcribe this", "youtube", "what does this video say", "watch together".
metadata: {"openclaw": {"emoji": "📺", "requires": {"bins": ["yt-dlp", "whisper"]}}}
---

# Kai YouTube Skill

Watch YouTube videos by downloading audio and transcribing with Whisper.

## Organization

- **Download folder:** `/home/kai/.openclaw/workspace/kai-yt-videos/`
- **Audio files:** `kai-yt-videos/kai_yt_${VIDEO_ID}.mp3`
- **Transcripts:** `kai-yt-videos/kai_yt_${VIDEO_ID}.txt`

## Workflow

1. **Download audio** using yt-dlp:
```bash
yt-dlp --extract-audio --audio-format mp3 --output "{WORKSPACE}/kai_yt_${VIDEO_ID}.mp3" "<URL>"
```

2. **Transcribe** using Whisper CLI:
```bash
whisper "{WORKSPACE}/kai_yt_${VIDEO_ID}.mp3" --model base --output_format txt --output_dir "{WORKSPACE}"
```

3. **Read transcript** from `{WORKSPACE}/kai_yt_${VIDEO_ID}.txt`

## Requirements

- `yt-dlp` - YouTube audio downloader (brew install yt-dlp)
- `whisper` - OpenAI Whisper CLI (brew install openai-whisper)

## Usage

```bash
bash {baseDir}/scripts/youtube.sh "<YouTube_URL>" [--language <lang>]
```

## Tips

- Each video gets unique files (no caching issues)
- Long videos may take several minutes to transcribe
- Language auto-detected if not specified
- Add `--language <lang>` for specific language (e.g., `--language Spanish`)
- All files organized in `kai-yt-videos/` folder

## Video ID Extraction

Handles both URL formats:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
