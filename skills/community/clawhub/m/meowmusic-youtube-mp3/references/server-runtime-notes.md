# Server Runtime Notes

Use this when bootstrapping or debugging the server runtime.

## Known-good baseline

- Linux host: Debian/Ubuntu-like
- Node.js: 22.x
- Python: 3.x
- `yt-dlp`: current pip-installed version
- `yt-dlp-ejs`: global npm install
- `ffmpeg`: apt package is usually fine

## Why Node 22 matters here

The already-working solution was stabilized after upgrading to Node.js 22 and aligning `yt-dlp`, `yt-dlp-ejs`, and extractor settings. If challenge solving suddenly regresses, verify Node first.

## yt-dlp shape

Recommended arguments in the known-good flow:

```bash
yt-dlp \
  --no-playlist \
  -f bestaudio/best \
  --extractor-args "youtube:player_client=tv,web;formats=missing_pot" \
  --extractor-args "youtube:player_skip=webpage,configs" \
  --cookies ./youtube-cookies.txt \
  -o ./files/cache/music/<artist>-<title>/source.%(ext)s \
  "https://www.youtube.com/watch?v=<id>"
```

If the cookie file is absent, omit `--cookies`.

## ffmpeg shape for MV -> MP3

```bash
ffmpeg -y -i source.webm -vn -ac 1 -ar 24000 -b:a 48k music.mp3
```

This is intentionally low-bitrate/normalized for embedded playback. If the target product later wants higher fidelity, change bitrate/sample rate deliberately rather than removing normalization entirely.

## Failure checklist

1. `node -v` is 22.x
2. `yt-dlp --version` works
3. `ffmpeg -version` works
4. cookie file exists and looks like Netscape cookie format
5. server process has permission to read `youtube-cookies.txt`
6. `yt-dlp` command succeeds manually outside the app
