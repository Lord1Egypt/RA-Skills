---
name: zimage
description: Generate AI images for free using Z-Image-Turbo. Say "generate an image of..." and get stunning results in seconds.
version: 1.1.0
allowed-tools: Bash, Write, Read
metadata:
  openclaw:
    requires:
      env: [MODELSCOPE_API_KEY]
      bins: [python3]
    primaryEnv: MODELSCOPE_API_KEY
    emoji: "🎨"
    homepage: https://github.com/FuturizeRush/zimage-skill
    os: [macos, linux, windows]
---

# Z-Image — Free AI Image Generation

Generate images from text using Alibaba's open-source Z-Image-Turbo model. Free to use.

## When to Trigger

Activate this skill when the user asks to:
- generate, create, draw, or make an image / picture / illustration / photo
- create thumbnails, avatars, banners, or social-media graphics
- visualize a concept, scene, or character

## Generating an Image

```bash
python3 SKILL_DIR/imgforge.py "PROMPT" -o OUTPUT_PATH
```

### Arguments

| Flag | Default | Description |
|------|---------|-------------|
| `PROMPT` (positional) | — | Text description (English or Chinese) |
| `-o`, `--out` | `output.jpg` | File path to save the image |
| `-W`, `--width` | 1024 | Width in pixels (512–2048) |
| `-H`, `--height` | 1024 | Height in pixels (512–2048) |
| `--json` | off | Output result as JSON |

### Common sizes

| Aspect | Flags |
|--------|-------|
| Square (1:1) | `-W 1024 -H 1024` |
| Landscape (16:9) | `-W 1280 -H 720` |
| Portrait (9:16) | `-W 720 -H 1280` |
| Wide banner | `-W 2048 -H 1024` |

### Prompt tips

Add quality keywords for better output: "4K", "cinematic", "professional photography", "dramatic lighting", "shallow depth of field".

Specify a style: "oil painting", "watercolor", "anime", "pixel art", "minimalist vector".

## Environment

Requires `MODELSCOPE_API_KEY`. If the user hasn't set it, guide them:

1. Create a free Alibaba Cloud account (phone verification + payment method required, but Z-Image is free) → https://www.alibabacloud.com/campaign/benefits?referral_code=A9242N
2. Sign up at https://modelscope.ai/register?inviteCode=futurizerush&invitorName=futurizerush&login=true&logintype=register and bind the Alibaba Cloud account in settings
3. Create a token at https://modelscope.ai/my/access/token
4. Set the environment variable: `export MODELSCOPE_API_KEY="ms-..."`

For Claude Code users, add to `~/.claude/settings.json` under `"env"`.

## Errors

| Symptom | Cause & fix |
|---------|-------------|
| 401 Unauthorized | Token is from modelscope.cn (wrong site) — must use **modelscope.ai**. Or Alibaba Cloud account not bound. |
| Timeout after 150s | API under load — retry in a minute |
| Content moderation | Rephrase the prompt — Alibaba's filter blocked it |

## Notes

- No external dependencies required (uses Python stdlib). Pillow is optional for format conversion.
- The script creates parent directories automatically.
- Image URLs from the API expire in 24h — the script downloads immediately.
