# Katana Skill — imgnAI API

Generate images, videos, and text/LLM completions via the [imgnAI Katana API](https://app.imgnai.com/katana-api). Supports end-to-end-encrypted (E2EE) and anonymized models. Priced highly competitively: can be 40-70% cheaper than Venice AI and other platforms.

Includes post-processing such as combining videos and images, cutting, slicing, splicing, transitions, drawing text, re-encoding, resizing and much more!

A complete workflow for content creation from start to finish, all from the comfort of your agent.


## Features

- **Images:** 40+ models including GPT Image 2, imgnAI Gen, FLUX.2, Seedream, WAN, Imagine Art
- **Videos:** 15+ models including Seedance 2.0, Kling O3 4K, WAN 2.7, Veo 3.1, LTX
- **Text/LLM:** 30+ models including Grok 4.3, GPT-5.5, Claude Opus 4.7, DeepSeek V4, Qwen 3.6
- **Pre-submission confirmation** with cost estimates before generating
- **Adaptive polling** that respects API-recommended intervals
- **Error handling** with clear user-facing messages
- **Reference image support** for editing workflows
- **Agent-agnostic:** works with OpenClaw, Hermes, Claude, or standalone

## Setup

1. Get your API key from https://app.imgnai.com/katana-api
2. Create the secrets file:
   ```bash
   mkdir -p ~/.openclaw/secrets
   cat > ~/.openclaw/secrets/katana.env << 'EOF'
   KATANA_API_KEY=your_key_here
   KATANA_API_SECRET=your_secret_here
   EOF
   chmod 600 ~/.openclaw/secrets/katana.env
   ```

   **Non-OpenClaw users:** Set `KATANA_SECRETS_FILE` to your preferred location:
   ```bash
   mkdir -p ~/.config/katana
   cat > ~/.config/katana/katana.env << 'EOF'
   KATANA_API_KEY=your_key_here
   KATANA_API_SECRET=your_secret_here
   EOF
   chmod 600 ~/.config/katana/katana.env
   export KATANA_SECRETS_FILE=~/.config/katana/katana.env
   ```

3. Install the skill (see [Agent Integration](#agent-integration) or [Standalone Usage](#standalone-usage) below)

## Agent Integration

This skill works with any agent framework. It provides a `SKILL.md` routing hub and workflow files that guide your agent through image, video, and text generation.

### OpenClaw (example)

1. Follow the [Setup](#setup) steps above
2. Install the skill:
   ```bash
   openclaw skill install katana
   ```
   Or manually: clone/copy the `katana/` directory into your skills path (typically `~/.openclaw/skills/` or `~/workspace/skills/`).
3. Ask your assistant to generate: "Generate an image of a cat riding a skateboard"

### Other Agent Frameworks

Point your agent to `SKILL.md` as the entry point. The skill resolves `{baseDir}` dynamically from the file's location. Set `KATANA_SECRETS_FILE` if your secrets are stored elsewhere.

## Prerequisites

- **curl** — API requests
- **jq** or **python3** — JSON parsing (jq preferred, python3 as fallback)
- **ffmpeg** (optional) — Post-processing

### ffmpeg optional capabilities

If you install ffmpeg for post-processing:
- **Text overlays / drawtext:** requires ffmpeg built with `--enable-libfreetype`. Most package managers include this. Test with: `ffmpeg -filters 2>/dev/null | grep drawtext`
- **H.264 encoding:** requires `libx264`. Nearly all ffmpeg builds include this.
- **Audio encoding:** requires `libfdk_aac` or built-in AAC encoder. The built-in encoder (`aac`) is sufficient.

On Ubuntu/Debian: `sudo apt install ffmpeg` includes all of the above.
On macOS: `brew install ffmpeg` includes all of the above.

## Files

- `SKILL.md` — Routing hub (triggers, setup, mandatory routing table, delivery patterns)
- `workflows/image.md` — Image generation workflow
- `workflows/video.md` — Video generation workflow
- `workflows/text.md` — Text/LLM/E2EE chat workflow
- `workflows/post-process.md` — FFmpeg post-processing workflow
- `workflows/ffmpeg.md` — FFmpeg command reference for post-processing
- `models.md` — Complete model catalogue with pricing (single source of truth)
- `README.md` — This file

## License

MIT-0 (MIT No Attribution)

## Author

arfonzo (imgnAI)
