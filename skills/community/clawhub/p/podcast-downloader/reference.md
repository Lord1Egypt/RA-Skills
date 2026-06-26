# Podcast Downloader Reference

Advanced usage, batch download, and troubleshooting for podcast-downloader skill.

## API Details

### Episode Info Extraction

Xiaoyuzhou uses Next.js. Data is embedded in `__NEXT_DATA__` script tag:

```bash
curl -s "https://www.xiaoyuzhoufm.com/episode/{episode_id}" \
  -H "User-Agent: Mozilla/5.0" | \
  grep -o '__NEXT_DATA__" type="application/json">[^<]*' | \
  sed 's/__NEXT_DATA__" type="application\/json">//' | \
  jq -r '.props.pageProps.episode'
```

**Response fields**:
- `title` - Episode title
- `podcast.title` - Podcast name
- `enclosure.url` - Audio file URL
- `shownotes` - Show notes (HTML)
- `duration` - Duration in seconds

### Audio URL Format

```
https://media.xyzcdn.net/{hash}/{filename}.m4a
```

## MP3 Quality Settings

| `-q:a` | Bitrate | Size/Hour | Quality | Use Case |
|--------|---------|-----------|---------|----------|
| `0` | ~130 kbps | ~59MB | Best | Audiophiles, archival |
| `1` | ~110 kbps | ~50MB | High | General use |
| `2` | ~100 kbps | ~45MB | Good | Casual listening |
| `3` | ~90 kbps | ~40MB | Medium | Podcasts, spoken word |
| `4` | ~80 kbps | ~35MB | Normal | Voice-only, save space |

**Recommendation**: Use `-q:a 0` for best quality. File size is similar to original m4a.

## Batch Download

### Download Multiple Episodes

Create a script:

```bash
#!/bin/bash
# batch_download.sh

EPISODES=(
  "abc123def456ghi789jklmno"
  "xyz987wvu654tsr321qpo"
  "def456ghi789jkl012mno"
)

for EPISODE_ID in "${EPISODES[@]}"; do
  echo "Downloading $EPISODE_ID..."
  ./scripts/download.sh "https://www.xiaoyuzhoufm.com/episode/$EPISODE_ID"
  sleep 2  # Rate limiting: be nice to the server
done
```

### Download All Episodes from a Podcast

```bash
# Get all episode IDs from a podcast
PODCAST_ID="abc123def456ghi789jklmno"

curl -s "https://www.xiaoyuzhoufm.com/podcast/$PODCAST_ID" \
  -H "User-Agent: Mozilla/5.0" | \
  grep -o '__NEXT_DATA__" type="application/json">[^<]*' | \
  sed 's/__NEXT_DATA__" type="application\/json">//' | \
  jq -r '.props.pageProps.podcast.episodes[].eid'
```

## Show Notes Processing

Show Notes are in HTML format with:

- Episode description
- Timestamps with clickable links
- Participant information
- Related links

**Extract timestamps**:

```bash
# Extract timestamp links
grep -oE '[0-9]{2}:[0-9]{2}' shownotes.md | head -10

# Convert to seconds for audio players
grep -oE '[0-9]{2}:[0-9]{2}' shownotes.md | \
  awk -F: '{print $1*60 + $2}'
```

## File Naming Convention

| Component | Pattern | Example |
|-----------|---------|---------|
| Directory | `{podcast}-{title}` | `PodcastName-Episode123` |
| Audio | `{title}.mp3` | `Episode123.mp3` |
| Notes | `{title}.md` | `Episode123.md` |

**Special characters**: Keep Chinese, English, numbers, spaces. Avoid `/ : * ? " < > |`.

## Troubleshooting

### Audio URL not found

**Cause**: Xiaoyuzhou may have updated page structure.

**Solution**:

```bash
# Check page structure manually
curl -s "https://www.xiaoyuzhoufm.com/episode/{episode_id}" \
  -H "User-Agent: Mozilla/5.0" | grep -i "audio"
```

### ffmpeg not found

**Solution**:

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg
```

### jq not found

**Solution**:

```bash
# macOS
brew install jq

# Ubuntu/Debian
sudo apt install jq
```

### Permission denied

**Solution**:

```bash
chmod +x scripts/download.sh
```

### File too large for cloud sync

**Solution**:
- m4a files are deleted by default
- To keep m4a: `KEEP_M4A=true ./scripts/download.sh <URL>`

## Rate Limiting

Xiaoyuzhou CDN has no strict rate limiting, but recommend:

- 2-second delay between batch downloads
- Use `--progress-bar` for single file downloads

## Related Tools

- `yt-dlp` - YouTube/Bilibili video download
- `gallery-dl` - Image gallery download
- `podcast-dl` - Generic podcast downloader

## API Reference

### download.sh

**Usage**:

```bash
./scripts/download.sh <episode_url>
```

**Arguments**:

| Argument | Required | Description |
|----------|----------|-------------|
| `episode_url` | Yes | Full Xiaoyuzhou episode URL |

**Environment Variables**:

| Variable | Default | Description |
|----------|---------|-------------|
| `PODCAST_DIR` | `/Users/zym/Documents/podcast/` | Output directory |
| `AUDIO_QUALITY` | `0` | ffmpeg `-q:a` value (0-4) |
| `KEEP_M4A` | `false` | Keep original m4a file |

**Exit Codes**:

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Invalid URL or missing argument |
| 2 | Failed to fetch episode info |
| 3 | Download failed |
| 4 | Conversion failed |

**Output**:

- `{podcast}-{title}/{title}.mp3` - Audio file
- `{podcast}-{title}/{title}.md` - Show notes
