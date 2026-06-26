---
name: mp4-to-gif
description: Use when the user wants to convert MP4 video files to GIF format, or asks about video-to-GIF conversion with quality/size control
---

# MP4 to GIF Conversion

## Overview

Convert MP4 videos to high-quality GIFs using ffmpeg's two-pass palette method. The two-pass approach produces significantly better color quality than direct conversion.

## When to Use

- User wants to convert MP4 (or other video) to GIF
- User needs to create GIFs from video for documentation, demos, or sharing
- User asks about reducing GIF file size or improving GIF quality

## Prerequisites

- **ffmpeg** must be installed and available in PATH

## Core Method

**Two-pass palette-based conversion** (always use this over single-pass):

```
# Pass 1: Generate optimized palette
ffmpeg -y -i <input> -vf "fps=15,scale=480:-1:flags=lanczos,palettegen=stats_mode=diff" /tmp/palette.png

# Pass 2: Convert using palette
ffmpeg -y -i <input> -i /tmp/palette.png -lavfi "fps=15,scale=480:-1:flags=lanczos [x]; [x][1:v] paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle" <output>
```

## Quick Reference

| Parameter | Default | Effect |
|-----------|---------|--------|
| `fps` | 15 | Frame rate — lower = smaller file, choppier motion |
| `scale` width | 480 | Output width in px — height auto-calculated (`-1`) |
| `lanczos` | — | High-quality downscaling filter |
| `stats_mode=diff` | — | Palette optimized for frame differences (better for motion) |
| `dither=bayer` | — | Ordered dithering, good balance of quality/size |
| `bayer_scale` | 5 | Dither strength (0-5), higher = more dithering |
| `diff_mode=rectangle` | — | Only update changed regions (smaller file) |

## Size vs Quality Tradeoffs

| Goal | Adjust |
|------|--------|
| Smaller file | Lower fps (10), smaller width (320), or trim duration |
| Smoother motion | Higher fps (24-30), but file size increases significantly |
| Better colors | Use `stats_mode=full` for static/slow content |
| Sharper | Increase width (640-800), costs more file size |

## Bundled Scripts

Two scripts are bundled alongside this SKILL.md. Use the one matching the current platform.

**Windows (PowerShell)** — `mp4_to_gif.ps1`:
```powershell
& "<this-skill-dir>/mp4_to_gif.ps1" -InputFile <input>                    # Defaults: 480px, 15fps
& "<this-skill-dir>/mp4_to_gif.ps1" -InputFile <input> -Width 640 -Fps 20 # Custom settings
& "<this-skill-dir>/mp4_to_gif.ps1" -InputFile <input> -OutputFile <output> # Custom output name
```

**Linux / macOS (Bash)** — `mp4_to_gif.sh`:
```bash
bash "<this-skill-dir>/mp4_to_gif.sh" -i <input>                    # Defaults: 480px, 15fps
bash "<this-skill-dir>/mp4_to_gif.sh" -i <input> -w 640 -f 20      # Custom settings
bash "<this-skill-dir>/mp4_to_gif.sh" -i <input> -o <output>        # Custom output name
```

When Claude invokes this skill, resolve `<this-skill-dir>` to the absolute path of the directory containing this SKILL.md.

## Common Mistakes

- **Single-pass conversion** (`ffmpeg -i in.mp4 out.gif`) — produces terrible banding and color artifacts. Always use the two-pass palette method.
- **Too high fps** — 30fps GIFs are massive. 15fps is usually sufficient for demos.
- **Too wide** — 480px is good for most uses. Full 1080p GIFs are impractically large.
- **Forgetting to clean up palette** — Delete the temporary palette.png after conversion.
