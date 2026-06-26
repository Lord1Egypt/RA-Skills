---
name: grab-videos
alias:
  - grab-extract-frames
  - grab-frames
  - extract-frames
  - download-videos
description: |
  Download videos and extract frames using yt-dlp and ffmpeg. Use when:
  - Download YouTube videos/Shorts: `yt-dlp <url>`
  - Extract frames from video: `ffmpeg -ss <time> -i <video> -vframes 1 <output>`
  - Batch extract frames: multiple videos, random timestamps
  - Convert video formats, trim clips

  NOT for: streaming-only sites without yt-dlp support, copyright-protected content.
---

# Grab Videos and Frames Skill

Download videos and extract frames using yt-dlp + ffmpeg.

## Quick Reference

| Task | Command |
|------|---------|
| Download YouTube video | `yt-dlp -f best <url>` |
| Download Shorts | `yt-dlp <youtube.com/@user/shorts>` |
| Extract frame @ 5s | `ffmpeg -ss 5 -i video.mp4 -vframes 1 out.jpg` |
| Frames every 2s | `ffmpeg -i video.mp4 -vf fps=0.5 out%03d.png` |
| Random frame 5-15s | `ffmpeg -ss $((RANDOM%11+5)) -i video.mp4 -vframes 1 out.jpg` |

## YouTube Download

```bash
# Download best quality
yt-dlp -f best "https://www.youtube.com/watch?v=XXXX"

# Download Shorts playlist (first 20)
yt-dlp "https://www.youtube.com/@user/shorts" --playlist-items 1-20

# List available formats
yt-dlp -F "https://www.youtube.com/watch?v=XXXX"

# Download specific format (e.g., 1080p)
yt-dlp -f "best[height<=1080][ext=mp4]" "https://www.youtube.com/watch?v=XXXX"

# Download audio only
yt-dlp -x "https://www.youtube.com/watch?v=XXXX"
```

## Frame Extraction

```bash
# Single frame at timestamp
ffmpeg -ss 5 -i video.mp4 -vframes 1 -q:v 2 frame.jpg

# Random frame (5-15 seconds)
ffmpeg -ss $((RANDOM % 11 + 5)) -i video.mp4 -vframes 1 -q:v 2 frame.jpg

# Frames every N seconds
ffmpeg -i video.mp4 -vf "fps=0.5" frame_%03d.png  # every 2s

# Scale down for thumbnails
ffmpeg -ss 10 -i video.mp4 -vf "scale=640:-1" -vframes 1 -q:v 5 thumb.jpg

# Batch from all videos
for f in *.mp4; do ffmpeg -ss 5 -i "$f" -vframes 1 "${f%.mp4}_thumb.jpg"; done
```

## Batch Operations

```bash
# Download multiple URLs
for url in "url1" "url2" "url3"; do yt-dlp "$url"; done

# Extract frame from each video
for f in *.mp4 *.webm; do [ -f "$f" ] || continue; dur=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$f"); rnd=$((RANDOM % 11 + 5)); ffmpeg -ss "$rnd" -i "$f" -vframes 1 "frames/${f%.mp4}_${rnd}s.jpg" -y; done
```

## Output Directory

```bash
# Recommended structure
workspace/
├── downloads/     # Raw videos
├── frames/        # Extracted frames
├── thumbnails/    # Small thumbs
└── clips/         # Trimmed clips
```

## Important Notes

- **Rate limits**: YouTube may rate-limit excessive downloads
- **Format support**: yt-dlp supports 1700+ sites
- **Storage**: Videos can be large; use `-f best[height<=720]` for smaller files
- **Permissions**: May need `chmod +x` for scripts
- **yt-dlp JS**: Requires Node.js or deno for some YouTube formats
- **Installation**: Need install `yt-dlp` and `ffmpeg` tools with `apt install <tool-name>` on Linux and with `brew install <tool-name>` on macOS,
or ask user to download it from `https://github.com/yt-dlp/yt-dlp/releases` and `https://ffmpeg.org/download.html`

## Common Patterns

**Download + extract 1 frame:**
```bash
yt-dlp -o video.mp4 "https://www.youtube.com/watch?v=XXXX"
ffmpeg -ss 5 -i video.mp4 -vframes 1 -q:v 2 thumb.jpg
```

**Thumbnail batch:**
```bash
mkdir -p thumbnails
for f in *.mp4; do ffmpeg -ss 5 -i "$f" -vf "scale=320:-1" -vframes 1 -q:v 5 "thumbnails/${f%.mp4}.jpg" -y; done
```

**Duration check:**
```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 video.mp4
```

## Extented Abilities and skills

**Learn other abilities and skills from yt-dl help**
```bash
yt-dlp --help
```

**Learn other abilities and skills from ffmpeg help**
```bash
ffmpeg -h
```
