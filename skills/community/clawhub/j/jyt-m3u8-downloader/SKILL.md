---
name: m3u8-downloader
description: "This skill should be used when the user wants to download videos from M3U8 streaming URLs. It handles parsing M3U8 playlists (including nested multi-bitrate playlists), downloading TS segments with multi-threading, handling AES-128 encryption keys, and merging segments into MP4 files using ffmpeg. Triggers: download m3u8 video, download streaming video, m3u8 download, download video from URL, download ts segments, HLS video download."
---

# M3U8 Video Downloader

## Overview

Download videos from M3U8/HLS streaming URLs by parsing playlists, downloading TS segments with multi-threading,
handling encrypted streams (AES-128), and merging all segments into a single MP4 file using ffmpeg.

## Prerequisites

Before executing, ensure the following are available:

1. **Python 3** with `requests` library installed: `pip install requests`
2. **ffmpeg** installed and added to system PATH (required for merging TS segments into MP4)
3. Network access to the M3U8 URL

## Workflow

### 1. Understand the User's Request

Extract from the user:
- **M3U8 URL**: The streaming playlist URL (required)
- **Output filename**: Name for the saved MP4 file (required, without extension)
- **Base64 key** (optional): For encrypted streams that require a manually provided AES-128 decryption key

### 2. Prepare the Environment

- Copy `scripts/M3u8Download.py` to the working directory
- Ensure `requests` is installed in the Python environment
- Verify `ffmpeg` is accessible from the command line: `ffmpeg -version`

### 3. Execute the Download

Use the `M3u8Download` class from `scripts/M3u8Download.py`:

```python
from M3u8Download import M3u8Download

M3u8Download(
    m3u8_url="<user_provided_url>",
    file_path="<output_name>",        # Without extension; TS temp dir and final MP4 use this name
    max_workers=64,                   # Concurrent download threads
    num_retries=10,                   # Retry count on download failure
    base64_key=None                   # Optional: base64-encoded AES-128 key for encrypted streams
)
```

#### Key Parameters

| Parameter | Description |
|-----------|-------------|
| `m3u8_url` | M3U8 playlist URL or local file path |
| `file_path` | Base name for temp folder and output MP4 file |
| `max_workers` | Max concurrent download threads (default: 64) |
| `num_retries` | Download retry count on failure (default: 10) |
| `base64_key` | Optional base64-encoded decryption key for AES-128 encrypted streams |

### 4. What Happens During Download

1. **Parse M3U8**: Fetches and parses the M3U8 playlist. If it is a master playlist (contains `EXT-X-STREAM-INF`), automatically follows the redirect to the media playlist.
2. **Download key**: If the playlist specifies `EXT-X-KEY`, the encryption key is downloaded (or uses the provided `base64_key`).
3. **Download segments**: All TS segments are downloaded concurrently with progress bar display.
4. **Merge**: ffmpeg merges all TS segments into a single MP4 file.
5. **Cleanup**: After verifying the MP4 file size matches the total TS size (within 10% tolerance), temporary TS files, key file, and M3U8 file are deleted automatically.

### 5. Handle Errors

- If ffmpeg is not found, inform the user to install it and add to PATH.
- If download fails due to network issues, the retry mechanism will attempt `num_retries` times.
- If the MP4 output size does not match the TS total size, temporary files are preserved for manual inspection.
- For encrypted streams without a provided key, the script attempts auto-download; if that fails, ask the user for the `base64_key`.

## Scripts

### `scripts/M3u8Download.py`

Main download script containing the `M3u8Download` class. This is the primary script to use for all M3U8 download operations.

## Notes

- The script supports both URL-based and local file-based M3U8 inputs.
- Chinese filenames and paths are supported.
- On Windows, `os.startfile()` is used to open the output directory after download completes.
- Do NOT modify the source code in `scripts/` - use it as-is.
