---
name: magic-hour
description: Generate AI video and images with the Magic Hour API (Sora 2, Veo 3.1, Kling 3.0, WAN 2.2, GPT-image, Nano Banana Pro). Text-to-video, image-to-video, image generation; free tier available.
version: 1.0.0
homepage: https://github.com/RhythmP28/clawhub-magic-hour
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "requires": { "bins": ["python3"], "python": ["magic_hour"], "env": ["MAGIC_HOUR_API_KEY"] },
        "primaryEnv": "MAGIC_HOUR_API_KEY",
      },
  }
---

# Magic Hour

One API key for many video/image models: Sora 2, Veo 3.1, Kling 3.0, Seedance, MiniMax H3, WAN 2.2, LTX 2.3 (video) and GPT-image, Nano Banana Pro, Seedream, Flux, Z-Image (image). Jobs are async; the scripts below submit, poll every ~5s, and print a single JSON line when done.

## Fastest route: hosted MCP server (zero install)

Magic Hour runs a remote MCP server at `https://mcp.magichour.ai/` (docs: https://magichour.ai/mcp). If your agent can attach MCP servers, add it with header `Authorization: Bearer $MAGIC_HOUR_API_KEY` (Claude web/desktop uses OAuth, client id `magic-hour-mcp`). It exposes image, video and audio generation tools plus upload (`videoAssets_generatePresignedUrl`) and wait/status tools, so no local SDK is needed. The scripts below are the fallback for agents without MCP, or when you want plain JSON from a shell.

## Setup (script route)

1. Free key (400 credits on signup + 100/day, no card): https://magichour.ai/developer
2. `export MAGIC_HOUR_API_KEY=mhk_...`
3. `pip install magic_hour` (official SDK, Python >= 3.9)

## Scripts

All scripts print one JSON object to stdout: `{project_id, status, model, url, urls, credits_charged, ...}` and exit non-zero with `{"status":"error","error":{...}}` on failure. Add `--download-dir DIR` to also save the file locally (`downloaded_paths` in the output). Add `--no-wait` to return immediately (`status: "queued"`) and check later with `status.py`.

```bash
# Text -> video (default: wan-2.2, 5s, 480p, 16:9 = 120 credits, free tier)
python3 {baseDir}/scripts/text_to_video.py "a corgi surfing at golden hour, slow-motion, cinematic" \
  --model wan-2.2 --duration 5 --resolution 480p --aspect-ratio 16:9 --download-dir ./out

# Image -> video (local file is uploaded automatically; public https URL also works)
python3 {baseDir}/scripts/image_to_video.py ./photo.png "slow push-in, hair moves in the wind" \
  --model kling-3.0 --duration 5 --resolution 720p

# Text -> image(s)
python3 {baseDir}/scripts/generate_image.py "isometric cozy coffee shop, soft morning light" \
  --model nano-banana-pro --count 2 --aspect-ratio 1:1

# Poll a queued project
python3 {baseDir}/scripts/status.py <project_id> --kind video --wait
```

## Choosing a video model

| Model | Durations (s) | Credits/sec | Notes |
|---|---|---|---|
| `wan-2.2` | 3-10, 15 | 24 | FREE. Default. Cheap general-purpose clips. |
| `ltx-2.3` | 1-10, 15, 20, 25, 30 | 24 | FREE. Longest free clips (30s). |
| `minimax-h3` | 1-10, 15, 20, 25, 30 | 24 | FREE. Up to 1080p. |
| `seedance-1.5` | 4-12 | 30 | Good value step up. |
| `kling-2.6` | 5, 10 | 36 | |
| `kling-3.0` | 3-15 | 48 | Best motion/physics for the price. |
| `veo3.1-lite` | 4, 6, 8, 16...56 | 48 | |
| `veo3.1` / `veo3.1-audio` | 4, 6, 8, 16...56 | 96 | Cinematic; `-audio` adds sound (`--audio`). |
| `sora-2` | 4, 8, 12, 24, 36, 48, 60 | 120 | Complex multi-shot scenes. 720p max. |
| `seedance-2.0-mini` / `2.0` / `2.5` | 4-15 / 4-15 / 4-30 | 96 / 120 / 120 | 720p max. |

Rules of thumb:
- Cost = credits/sec x duration (e.g. kling-3.0 5s = 240). Failed jobs are auto-refunded. Tell the user the estimated cost before spending more than ~500 credits.
- Stay on `wan-2.2` / `ltx-2.3` / `minimax-h3` unless the user asks for quality or has a paid plan; the free tier is ~100 credits/day.
- Duration must be in the model's allowed list or the API rejects the job. The scripts warn on stderr if it is not.
- Use `9:16` for shorts/reels, `16:9` for landscape, `1:1` for social tiles.
- Image-to-video: keep the prompt about motion ("camera slowly orbits", "she turns and smiles"); the image already defines the look.

## Image models

`default` (good all-rounder), `gpt-image-2` (text rendering, instructions), `nano-banana-pro` (photoreal, editing), `seedream-5-pro`, `flux-2-klein` (fast), `z-image-turbo` (fastest), `qwen-edit` (edits). Images are cheap (roughly 5-50 credits each depending on model).

## Prompting tips

- Video prompts: subject + action + camera move + lighting/style + mood, 1-3 sentences. Avoid listing many scenes for short clips.
- Rendering takes ~1-5 minutes for video, seconds for images. Output URLs expire after a while; download with `--download-dir` if the user needs the file.
- If `status` is `error`, read `error.message`, fix the request (usually duration/resolution/model), and retry once.

## References

- `{baseDir}/references/api.md` - raw HTTP endpoints, poll loop, file upload (use if the SDK is unavailable, e.g. with curl).
- `{baseDir}/references/models.md` - full model catalogue and pricing.
- Docs: https://docs.magichour.ai - Other integrations: PyPI `langchain-magic-hour`, `llama-index-tools-magic-hour`; npm `langchain-magic-hour`, `magic-hour-ai-provider`; hosted MCP https://mcp.magichour.ai/ (legacy self-hosted: github.com/magichourhq/magic-hour-mcp).
