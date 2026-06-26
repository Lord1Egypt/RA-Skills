---
name: jable
description: Download videos from Jable.tv. Triggered when the user mentions "download Jable video", "jable download", or uses /skill jable.
---

# Jable Video Downloader Skill

This tool is dedicated to high-speed video downloads from Jable.tv, with automatic organization based on the actress's name and real-time progress web page.

## Dependencies

Before executing the download, the AI Agent MUST ensure the following tools are installed. If missing, prompt the user for installation or attempt to install them automatically:
1. **yt-dlp** (Core download and decryption tool)
2. **ffmpeg** (Muxing and format correction tool)
3. **python3** (Script execution environment)
4. **flask** (Web server for progress page)

## Usage

```bash
# Single video download (auto start server + send Telegram)
/skill jable "Video ID or URL" "Save Directory (Optional)"

# Actress search download (auto start server + send Telegram)
/skill jable --search "Actress Name" "Count" "Save Directory (Optional)"

# Start progress web server (manual)
/skill jable --server
```

**Input Formats:**
- **Video ID**: e.g., `dass-402`, `mina-340` (will be automatically expanded to `https://jable.tv/videos/ID/`)
- **Full URL**: e.g., `https://jable.tv/videos/mina-340/`
- **Save Directory** (Optional): Custom path, defaults to the system "Videos" directory.

## New Feature: Auto Server Start + Telegram Notification

**Automated Workflow:**
1. When executing download, automatically check if server is running
2. If server not running, automatically start in background
3. Send progress page link via Telegram
4. Download progress displays in real-time on the web page

**Telegram Notification Content:**
```
📥 Jable Download Started!

🔗 Progress Page: http://100.64.0.5:5000
```

## Access the Progress Page

- **Local:** http://localhost:5000
- **Network:** http://100.64.0.5:5000

**The page shows:**
- Current download status (idle/downloading/completed/error)
- Progress bar with percentage
- Download speed and ETA
- Number of completed/failed downloads
- Current file being downloaded

## Execution Steps

1. **Environment Check**: Verify if `yt-dlp`, `ffmpeg`, and `flask` are available.
2. **Auto Start Server**: When you start a download, the script automatically checks if the server is running. If not, it starts it in the background.
3. **Telegram Notification**: You'll receive a Telegram message with the progress page URL.
4. **Parse Input**: Identify whether the input is a Video ID or a URL.
5. **Execute Download**: Run `python3 jable_downloader.py <URL> <DIR>`.
    - The script automatically simulates browser headers to obtain the correct `hlsUrl`.
    - Invokes `yt-dlp` for high-speed downloading with 16 concurrent threads.
    - Updates progress in real-time to the web page.
6. **Post-processing**:
    - After the download completes, extract the actress's name from the video title.
    - Create a folder named after the actress in the target directory.
    - Move the `.mp4` video into that folder.
7. **Completion**: The page will show "completed" status when done.

## Examples

```bash
# Single video download (auto start server + send Telegram)
/skill jable "dass-402"
/skill jable "https://jable.tv/videos/mina-340/"

/skill jable "mina-300" "/home/user/Downloads"

# Actress search download (auto start server + send Telegram)
/skill jable --search "Mei" 10
/skill jable --search "Sakura" 5

# Manual server start
/skill jable --server
```

## Web Page Features

The progress page at `http://100.64.0.5:5000` includes:
- 🎨 Beautiful gradient UI design
- 📊 Real-time progress bar
- ⚡ Download speed display
- ⏱️ ETA (estimated time of arrival)
- 📁 Current file name
- ✅/❌ Completed/Failed counters
- 📱 Mobile-friendly responsive design
