---
name: pixeldojo
description: Access PixelDojo's API for AI image and video generation. Use when an agent needs to create images or videos, choose a model from the live PixelDojo catalog, check async job status, or download finished assets. PixelDojo is a subscription-based creative platform that exposes multiple generation models through one API, including general image, editing-oriented image, and video workflows.
metadata:
  author: Brian Lovett
  homepage: https://pixeldojo.ai
  source: https://pixeldojo.ai
  openclaw:
    requires:
      env:
        - PIXELDOJO_API_KEY
      bins:
        - curl
        - jq
        - python3
---

# PixelDojo

Use PixelDojo's async API to generate and download AI images or videos.

## Setup

Runtime requirements:
- Environment variable: `PIXELDOJO_API_KEY`
- Binaries: `curl`, `jq`, `python3`
- Optional override: `PIXELDOJO_API_BASE`

Set the API key before running any helper:

```bash
export PIXELDOJO_API_KEY=your_api_key_here
```

Optional local env file:

```bash
cp ~/.openclaw/skills/pixeldojo/.env.example ~/.openclaw/skills/pixeldojo/.env
```

Default API base: `https://pixeldojo.ai/api/v1`

## Workflow

1. Check the live model catalog first.
2. Pick a model that matches the requested workflow.
3. Submit the job with `generate.sh` or the Nano Banana helper.
4. Poll status until complete, then return the downloaded asset path.

Do not guess model IDs.

## Check the live catalog

```bash
bash ~/.openclaw/skills/pixeldojo/models.sh
```

For a pinned snapshot of known-good model IDs and example picks, read:
- `references/model-catalog.md`

## Generate an image

```bash
bash ~/.openclaw/skills/pixeldojo/generate.sh image "editorial product photo of a silver robot" flux-2-pro --aspect-ratio 16:9
```

Good defaults:
- Best general image quality: `flux-2-max`
- Prompt adherence and typography: `nano-banana-2`
- Editing-oriented image work: `flux-kontext-pro`

## Generate a video

```bash
bash ~/.openclaw/skills/pixeldojo/generate.sh video "cinematic ocean waves at sunset" seedance-1.5 --duration 5
```

Use `--image-url` for image-to-video models:

```bash
bash ~/.openclaw/skills/pixeldojo/generate.sh video "slow camera push-in" wan-2.6-flash --image-url https://example.com/input.png --duration 5
```

## Nano Banana helper

Use this when the user specifically wants Nano Banana 2 or strong prompt adherence:

```bash
python3 ~/.openclaw/skills/pixeldojo/scripts/generate-nano-banana.py "clean ecommerce hero shot of running shoes" --aspect-ratio 16:9 --output ~/Desktop/shoes.png
```

## Check job status

```bash
bash ~/.openclaw/skills/pixeldojo/status.sh job_abc123
```

## Output paths

Default download folders:
- `~/Pictures/AI Generated/images/`
- `~/Pictures/AI Generated/videos/`

Override with:

```bash
--output /path/to/file.png
```

## Notes

- `generate.sh` supports `--aspect-ratio`, `--duration`, `--image-url`, `--output`, `--poll-interval`, and `--max-wait`.
- `generate.sh` covers the shared prompt-based API flow. If a request needs model-specific editing payloads, inspect the live catalog and API behavior before improvising.
- PixelDojo markets full commercial rights for generated output, but the user is still responsible for complying with the service terms and any third-party model restrictions.
