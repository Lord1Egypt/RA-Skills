---
name: jable-downloader-lite
description: Simple video downloader for Jable.tv. Download videos by ID or search by actress name.
---

# Jable Video Downloader

Download videos from Jable.tv with automatic organization by actress name.

## Dependencies

Before using, ensure these tools are installed:

- **yt-dlp** — Video download engine (`pip install yt-dlp` or `brew install yt-dlp`)
- **ffmpeg** — Video processing (`sudo apt install ffmpeg` or `brew install ffmpeg`)
- **xdg-user-dir** — (Linux only) For finding default Videos folder

## Usage

Tell the agent what you want to download:

- **Download by video ID:**
  - "Download jable video mina-340"
  - "幫我下載 jable Dass-402"

- **Download by actress search:**
  - "Download 10 jable videos of 五日市芽依"
  - "搜尋並下載 5 部 Mikami Yua 的作品"
  - Randomly selects available videos, skips already downloaded ones

The agent will automatically:
1. Find available videos
2. Download them to your Videos folder
3. Organize files by actress name

## Examples

```
User: Download jable video dass-402
Agent: ⬇️ Downloading Dass-402...
      ✅ Completed! Saved to ~/Videos/Dass-402/

User: Download 5 jable videos of Mikami Yua
Agent: 🔍 Found 20 videos...
      📥 Downloading 5 videos...
      ✅ Done! 5/5 videos downloaded
```

## Output Location

Videos are saved to your system's default Videos folder, organized by actress name:
```
~/Videos/
├── 五日市芽依/
│   └── mina-340.mp4
├── Mikami Yua/
│   ├── ssni-473.mp4
│   ├── ssni-409.mp4
│   ├── ssni-452.mp4
│   ├── ssni-618.mp4
│   └── ssni-644.mp4
```

## Features

- Simple text-based interface
- Automatic actress-based organization
- Progress display in console
- Cleanup temporary files after download
