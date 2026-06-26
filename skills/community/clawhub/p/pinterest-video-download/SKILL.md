---
name: pinterest-video-download
description: Download the main video from a Pinterest pin and save it as a local MP4 for personal media workflows such as wallpaper saving, repost preparation, or Live Photo conversion. Use when the user gives a pinterest.com/pin/... URL or pin.it short link and wants the video file from that pin.
---

# Pinterest Video Download

1. Resolve the pin URL if the user gives a `pin.it` short link.
2. Open the pin in the browser and inspect page resources to find the HLS playlist (`.m3u8`) for the main video.
3. Prefer the highest available variant from the master playlist.
4. Download the video with `ffmpeg` using stream copy when possible.
5. Save the file under `~/.openclaw/workspace/downloads/` with a stable name based on the pin id.
6. Tell the user where the MP4 was saved. If the user asks, send the MP4 back through chat.

## Main features

- accepts both full Pinterest pin URLs and `pin.it` short links
- downloads the primary video from the current pin
- prefers the highest available playlist variant
- saves a normal MP4 for local use or forwarding
- works well as the first step before making an iPhone Live Photo

## Notes

- Use `ffmpeg`; install missing dependencies yourself when safe.
- Pinterest often serves HLS playlists from `v1.pinimg.com/videos/iht/hls/...`.
- Verify the saved file with `ffprobe` or `ffmpeg -i` when needed.
- If multiple videos are present on the page, pick the primary video visible in the current pin, not a suggested pin below it.
