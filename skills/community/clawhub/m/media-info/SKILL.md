---
name: media-info
description: Analyze media files with MediaInfo CLI and compare behavior with ffprobe. Use when inspecting container/codec metadata, extracting width/height/duration/bitrate, troubleshooting files that ffprobe cannot parse, or classifying media by orientation (landscape/portrait).
---

# media-info

Install and run MediaInfo CLI in non-root environments.

## Quick start

1. Install MediaInfo locally:
   - `bash scripts/install_mediainfo_local.sh`
2. Verify installation:
   - `bash scripts/test_mediainfo.sh`
3. Inspect files:
   - `./vendor/mediainfo/MediaInfo/Project/GNU/CLI/mediainfo <file>`
   - `./vendor/mediainfo/MediaInfo/Project/GNU/CLI/mediainfo --Output=JSON <file>`

## Workflow

### Install

Run `scripts/install_mediainfo_local.sh`.

- Download MediaInfo source archive
- Build CLI locally
- Place binary at `vendor/mediainfo/MediaInfo/Project/GNU/CLI/mediainfo`

### Extract metadata

Use plain output for human reading and JSON output for automation.

### Classify orientation

Use Width/Height (and Rotation when present):

- landscape: effective width >= effective height
- portrait: effective width < effective height

When Rotation is 90/270, swap width and height before classification.

## Notes

- Do not require sudo.
- Prefer MediaInfo for files where ffprobe fails but container data still exists.
