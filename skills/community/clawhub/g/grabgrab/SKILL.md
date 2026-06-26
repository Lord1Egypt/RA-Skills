---
name: GrabGrab
description: Use when the user wants to download a video or audio from a URL. Supports 20+ platforms including YouTube, X/Twitter, TikTok, Instagram, Facebook, Reddit, Bilibili, Vimeo, Dailymotion, SoundCloud, Twitch, Pinterest, Snapchat, Bluesky, VK, OK.ru, Rutube, Streamable, Loom, Tumblr, Newgrounds, Xiaohongshu and more. Trigger when user says "download video", "save video", "grab video", provides a video URL and wants to download it, or mentions downloading from supported platforms.
---

# GrabGrab - Video & Audio Downloader

Download videos and audio from 20+ platforms by URL. Powered by [GrabGrab](https://www.grabgrab.fun).

## Supported Platforms (20+)

| Platform | Example URLs |
|----------|-------------|
| YouTube | `youtube.com/watch`, `youtu.be/`, `youtube.com/shorts/`, `music.youtube.com` |
| X / Twitter | `x.com/.../status/`, `twitter.com/.../status/` |
| TikTok | `tiktok.com/@.../video/`, `vm.tiktok.com/` |
| Instagram | `instagram.com/p/`, `instagram.com/reel/`, `instagram.com/stories/` |
| Facebook | `facebook.com/.../videos/`, `fb.watch/` |
| Reddit | `reddit.com/r/.../comments/` |
| Bilibili | `bilibili.com/video/`, `b23.tv/` |
| Vimeo | `vimeo.com/<id>` |
| Dailymotion | `dailymotion.com/video/` |
| SoundCloud | `soundcloud.com/` |
| Twitch | `twitch.tv/`, `clips.twitch.tv/` |
| Pinterest | `pinterest.com/pin/` |
| Snapchat | `snapchat.com/` |
| Bluesky | `bsky.app/` |
| VK | `vk.com/video`, `vk.com/clip` |
| OK.ru | `ok.ru/video/` |
| Rutube | `rutube.ru/video/` |
| Streamable | `streamable.com/` |
| Loom | `loom.com/share/` |
| Tumblr | `tumblr.com/` |
| Newgrounds | `newgrounds.com/` |
| Xiaohongshu | `xiaohongshu.com/`, `xhslink.com/` |

## Workflow

### Step 1: Call the GrabGrab API

Use `curl` via the Bash tool to call the API:

```bash
curl -s -X POST "https://www.grabgrab.fun/api/download" \
  -H "Content-Type: application/json" \
  -d '{"url": "<VIDEO_URL>", "videoQuality": "<QUALITY>"}'
```

**Video quality options** (ask user if not specified, default to `1080`):
- `max` - Best available quality
- `2160` - 4K
- `1440` - 2K
- `1080` - Full HD (default)
- `720` - HD
- `480` - SD
- `360` - Low
- `144` - Minimum

**Download mode options** (default to `auto`):
- `auto` - Video with audio (default)
- `audio` - Audio only
- `mute` - Video without audio

### Step 2: Parse the API Response

The API returns JSON. Handle each response type:

**Direct download** (`type: "direct"`):
```json
{
  "success": true,
  "type": "direct",
  "url": "https://...",
  "filename": "video.mp4",
  "proxyUrl": "/api/proxy?url=..."
}
```
Action: Download the file using `curl -L -o <filename> "<url>"`.

**Picker** (`type: "picker"`) — multiple items found (e.g., Instagram carousel):
```json
{
  "success": true,
  "type": "picker",
  "items": [
    {"type": "video", "url": "https://...", "proxyUrl": "/api/proxy?url=..."},
    {"type": "photo", "url": "https://...", "proxyUrl": "/api/proxy?url=..."}
  ]
}
```
Action: Show the user the list of items and ask which ones to download, or download all videos.

**Error**:
```json
{
  "success": false,
  "error": "Error message here"
}
```
Action: Show the error message to the user.

### Step 3: Download the File

For direct downloads:
```bash
curl -L -o "<filename>" "<download_url>"
```

For tunnel/redirect URLs that need the proxy, use the signed `proxyUrl` returned by the API:
```bash
curl -L -o "<filename>" "https://www.grabgrab.fun<proxyUrl>"
```

IMPORTANT: `/api/proxy` requires a short-lived signature. Do not construct proxy URLs manually; use the `proxyUrl` field from the API response.

### Step 4: Confirm to User

After download completes:
- Report the filename and file size
- Report the download location (current working directory or user-specified path)

## Important Notes

- The API has a rate limit of 30 requests per minute. If you get a 429 error, wait and retry.
- Always use `-L` flag with curl to follow redirects.
- If the user asks for audio only, set `downloadMode` to `"audio"`.
- If the user wants the best quality, set `videoQuality` to `"max"`.
- Default download location is the current working directory unless the user specifies otherwise.
- The API automatically detects the platform from the URL — no need to specify the platform manually.

## Examples

**User**: "Download this YouTube video: https://www.youtube.com/watch?v=dQw4w9WgXcQ"

Actions:
1. Call API: `curl -s -X POST "https://www.grabgrab.fun/api/download" -H "Content-Type: application/json" -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "videoQuality": "1080"}'`
2. Parse response to get download URL and filename
3. Download: `curl -L -o "filename.mp4" "<url>"`
4. Report: "Downloaded filename.mp4 (15.2 MB) to current directory."

**User**: "Save the audio from this TikTok: https://www.tiktok.com/@user/video/123"

Actions:
1. Call API with `downloadMode: "audio"`: `curl -s -X POST "https://www.grabgrab.fun/api/download" -H "Content-Type: application/json" -d '{"url": "https://www.tiktok.com/@user/video/123", "downloadMode": "audio"}'`
2. Parse and download the audio file
3. Report the result

**User**: "/GrabGrab https://www.bilibili.com/video/BV1xx411c7mD"

Actions:
1. Call API with default settings (1080p, auto mode)
2. Download the video
3. Report the result
