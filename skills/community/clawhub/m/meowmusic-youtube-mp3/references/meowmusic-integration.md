# MeowMusic Integration Notes

Use this when patching MeowMusicServer or a similar service.

## Product direction to preserve

- Prefer existing/legacy music sources first.
- Prefer local music library and cache reuse.
- Use YouTube only as fallback/补源.
- Return stable cached `music.mp3` URLs instead of relying on live streaming by default.

## Search and cache shape

Minimal Go shape:

```go
func searchYouTubeTopMV(query string) (*ytSearchEntry, error) {
    searchQuery := fmt.Sprintf("ytsearch5:%s MV 官方版", query)
    cmd := exec.Command("yt-dlp",
        "--dump-single-json",
        "--flat-playlist",
        "--no-warnings",
        searchQuery,
    )
    output, err := cmd.Output()
    // unmarshal JSON and pick first entry
}
```

## Download and transcode shape

Prefer downloading source audio first, then transcoding with ffmpeg:

```go
outputTemplate := filepath.Join(dirName, "source.%(ext)s")
args := []string{
    "--no-playlist",
    "-f", "bestaudio/best",
    "--extractor-args", "youtube:player_client=tv,web;formats=missing_pot",
    "--extractor-args", "youtube:player_skip=webpage,configs",
    "-o", outputTemplate,
}
if _, err := os.Stat("./youtube-cookies.txt"); err == nil {
    args = append(args, "--cookies", "./youtube-cookies.txt")
}
args = append(args, videoURL)
cmd := exec.Command("yt-dlp", args...)
```

Then resolve the downloaded source file (`source.webm`, `source.m4a`, `source.mp4`, `source.mp3`) and convert:

```go
ffmpegArgs := []string{
    "-y",
    "-i", sourcePath,
    "-vn",
    "-ac", "1",
    "-ar", "24000",
    "-b:a", "48k",
    filepath.Join(dirName, "music.mp3"),
}
```

## Source priority

Recommended `requestAndCacheMusic()` strategy:

1. try legacy sources (`kuwo`, `netease`, `migu`, `baidu` or repo-specific set)
2. only if all miss, call the YouTube fallback path

If the repo already has working legacy-source logic, keep it untouched and add the YouTube path behind it.

## API behavior

For device playback, prefer returning:

- `AudioURL: /cache/music/<artist>-<title>/music.mp3`
- `AudioFullURL: /cache/music/<artist>-<title>/music.mp3`

This is more stable than a live on-the-fly stream endpoint.

## Notes for local-first evolution

A good future direction is:

- upload local tracks via Web UI
- store downloaded YouTube fallbacks into the same local/cache-visible namespace
- when the same track is requested again, serve local/cache hit instead of downloading again
