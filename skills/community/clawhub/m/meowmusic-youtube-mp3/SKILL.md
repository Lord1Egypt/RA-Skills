---
name: meowmusic-youtube-mp3
description: "Package and reuse the MeowMusicServer-patched YouTube fallback workflow: Windows Chrome cookie export/sync to server, server-side yt-dlp/yt-dlp-ejs/ffmpeg setup, old-source-first with YouTube fallback, and MV-to-MP3 extraction/caching. Use when Claude needs to wire YouTube audio acquisition into MeowMusicServer or a similar music service, debug YouTube download failures, refresh cookies from a Windows Chrome profile, or implement a local-cache MP3 flow from YouTube videos."
---

# MeowMusic YouTube MP3

Use this skill to rebuild the currently working MeowMusicServer-patched solution into another repo/server without rediscovering the whole stack.

## Workflow decision tree

1. **Need cookie sync from Windows Chrome to server?**
   - Use `scripts/youtube_cookie_sync.py`.
   - If the user wants a double-click workflow on Windows, also use `scripts/windows/sync_cookie.bat` and `scripts/windows/open_youtube.bat`.
   - If you need API shape or server handler details, read `references/cookie-api-and-sync.md`.

2. **Need to prepare a Linux server for YouTube download and MP3 extraction?**
   - Run `scripts/install_server_env.sh`.
   - If challenge solving or runtime behavior is flaky, read `references/server-runtime-notes.md`.

3. **Need to patch MeowMusicServer so old sources stay first and YouTube acts only as fallback/补源?**
   - Read `references/meowmusic-integration.md`.
   - Keep source priority as: `sources.json` → local library → cache → legacy upstreams → YouTube fallback.
   - Do **not** make YouTube the default first source unless the user explicitly asks.

4. **Need MV -> MP3 instead of direct streaming?**
   - Prefer `yt-dlp` to fetch bestaudio, then use `ffmpeg` to normalize/transcode into a stable cached `music.mp3`.
   - Read `references/meowmusic-integration.md` for the patch pattern and command shape.

## Core operating rules

- Prefer **old/legacy music sources first**. YouTube is a补源/fallback path, not the primary path.
- Prefer **local reusable cache/library** over repeated redownloads.
- Prefer returning a stable cached `music.mp3` path to devices instead of a fragile live stream.
- If a cookie file exists, pass it to `yt-dlp` automatically.
- When YouTube requires extra handling, prefer extractor args compatible with the known-good setup:
  - `youtube:player_client=tv,web;formats=missing_pot`
  - `youtube:player_skip=webpage,configs`
- Keep all cookie and bearer-token material out of the skill package. Use placeholders only.

## Recommended implementation shape

### 1. Windows cookie sync

On Windows, export cookies from Chrome with:

```bash
yt-dlp --cookies-from-browser chrome:Default --cookies youtube-cookies.txt --skip-download https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

Then POST the cookie file content to a server endpoint such as:

- `POST /api/admin/youtube-cookie/update`
- optional status check: `GET /api/admin/youtube-cookie/status`

Use `scripts/youtube_cookie_sync.py` unless the repo already has its own equivalent.

### 2. Server download strategy

Use this shape:

1. Search top YouTube MV/result for a song.
2. Download audio with `yt-dlp` into a per-track cache directory.
3. Convert the downloaded source into `music.mp3` with `ffmpeg`.
4. Return cached local URLs from the service.

### 3. MeowMusic source order

Use this order unless the user asks otherwise:

1. curated `sources.json`
2. local uploaded/downloaded library
3. existing cache hits
4. legacy remote music APIs
5. YouTube fallback

This keeps the product aligned with the current direction: local-first, old-source-first, YouTube only for missing tracks.

## Files in this skill

- `scripts/install_server_env.sh` — server bootstrap for Node 22, yt-dlp, yt-dlp-ejs, ffmpeg.
- `scripts/youtube_cookie_sync.py` — export Chrome/Edge/Firefox cookies and push them to the server.
- `scripts/windows/sync_cookie.bat` — Windows double-click wrapper.
- `scripts/windows/open_youtube.bat` — helper to open YouTube in Chrome.
- `references/cookie-api-and-sync.md` — cookie API contract and usage notes.
- `references/server-runtime-notes.md` — server environment and challenge-solver notes.
- `references/meowmusic-integration.md` — patch strategy and concrete Go snippets.

## Execution notes

- Read only the reference file relevant to the current task.
- When editing an existing repo, prefer minimal surgical patches over broad rewrites.
- When a download path already works, preserve behavior and only harden the flaky parts.
- If the target repo differs from MeowMusicServer, reuse the flow, not the exact filenames.
