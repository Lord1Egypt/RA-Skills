---
name: nano-gpt
description: Use when tasks need the NanoGPT API for text, image, or video generation through the local `nano-gpt` CLI and bundled wrapper scripts for OpenClaw or ClawHub workflows. This skill requires a NanoGPT API token.
homepage: https://docs.nano-gpt.com/
metadata:
  openclaw:
    homepage: https://docs.nano-gpt.com/
    primaryEnv: NANO_GPT_API_KEY
    requires:
      env:
        - NANO_GPT_API_KEY
---

# NanoGPT Skill

Use this skill when the task should run through the NanoGPT API from a local terminal environment. NanoGPT’s official docs describe it as an API for text, image, and video generation, with text generation generally matching OpenAI standards. This repository is the local CLI and skill wrapper for that API, not a generic prompt helper. Prefer the bundled wrapper scripts in `scripts/` so OpenClaw and direct CLI usage share the same behavior.

Official docs: <https://docs.nano-gpt.com/>

## Prerequisite check

Before invoking the skill, ensure the CLI is available:

```bash
./scripts/models.sh --json
```

If that fails because the local CLI is not built yet:

```bash
npm install
npm run build
```

If the repo is not present locally, install the published CLI instead:

```bash
npm install -g nano-gpt-cli
```

Authentication is token-based. This skill requires a NanoGPT API token. Set the token in `NANO_GPT_API_KEY`:

```bash
export NANO_GPT_API_KEY=YOUR_NANO_GPT_TOKEN
```

Or configure it once and store it in the local `nano-gpt-cli` user config:

```bash
nano-gpt config set api-key YOUR_API_KEY
```

Optional environment overrides:

```bash
export NANO_GPT_MODEL=moonshotai/kimi-k2.5
export NANO_GPT_IMAGE_MODEL=qwen-image
export NANO_GPT_VIDEO_MODEL=kling-video-v2
export NANO_GPT_BASE_URL=https://nano-gpt.com
export NANO_GPT_OUTPUT_FORMAT=text
```

## Quick start

Text prompt:

```bash
./scripts/prompt.sh "Summarize the latest build logs."
```

Streaming multimodal prompt:

```bash
./scripts/prompt.sh "Describe this image." --image ./assets/example.png
```

Interactive chat:

```bash
./scripts/chat.sh
```

Image generation:

```bash
./scripts/image.sh "A cinematic product shot of a silver mechanical keyboard" --output output/keyboard.png
```

Image-to-image generation:

```bash
./scripts/image.sh "Turn this product photo into a watercolor ad" --image ./assets/product.png --output output/product-watercolor.png
```

Video generation:

```bash
./scripts/video.sh "A cinematic drone flyover of a neon coastal city at dusk" --duration 5 --output output/neon-city.mp4
```

## Workflow

1. Use `scripts/prompt.sh` for one-shot text or vision prompts.
2. Use `scripts/chat.sh` for iterative back-and-forth.
3. Use `scripts/image.sh` for text-to-image or image-to-image generation.
4. Use `scripts/video.sh` for text-to-video or image-to-video generation.
5. Use `nano-gpt video-status REQUEST_ID` when a video run is asynchronous and needs a later status check.
6. Use `scripts/models.sh --json` when model discovery matters.
7. Prefer flags over editing scripts. The wrappers should stay thin.

## References

Open only what you need:

- Command reference: `references/cli.md`
- Common OpenClaw workflows: `references/workflows.md`

## Guardrails

- Prefer the wrapper scripts over calling NanoGPT HTTP APIs directly.
- Only use this skill when the user wants to call the NanoGPT API.
- Keep secrets out of prompts and logs; use config or env vars for API keys.
- Only upload local images or videos when the user explicitly provides the path or clearly asks to use that specific file.
- Do not search the filesystem for media to upload.
- Treat local `--image` and `--video` inputs as remote-upload actions. Do not send sensitive screenshots, exports, documents, or recordings unless the user explicitly requests it.
- Prompts and any provided media are sent to the configured NanoGPT API endpoint, which defaults to `https://nano-gpt.com`.
- Use `--json` when another tool or agent will parse the output.
- Use `--output` on `scripts/image.sh` when a file artifact is required.
- Use `--output` on `scripts/video.sh` when the final MP4 should be written locally.
