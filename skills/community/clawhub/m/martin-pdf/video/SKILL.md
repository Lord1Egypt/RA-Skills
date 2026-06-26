---
---
name: veo
name: veo
description: Generate video using SkillBoss API Hub (video generation, auto-routed via /v1/pilot).
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "requires":
          {
            "env": { "SKILLBOSS_API_KEY": "" },
            "bins": ["uv"],
          },
      },
  }
---


# Veo (Video Generation via SkillBoss API Hub)

Generate video clips using SkillBoss API Hub's video generation capability.

Generate video
```bash
uv run {baseDir}/scripts/generate_video.py --prompt "your video description" --filename "output.mp4"
```

Options
- `--duration` / `-d`: Video duration in seconds (default: 8, max varies by model)
- `--aspect-ratio` / `-a`: Aspect ratio (16:9, 9:16, 1:1)
- `--model`: Optional model hint (SkillBoss API Hub auto-routes to optimal video model)

API key
- `SKILLBOSS_API_KEY` env var

Notes
- SkillBoss API Hub automatically routes to the best available video model
- Output is MP4 format
- Supports image-to-video with `--input-image`
- The script prints a `MEDIA:` line for Clawdbot to auto-attach on supported chat providers.
