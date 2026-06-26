---
name: nova-canvas
description: >-
  Generate images using Amazon Nova Canvas via AWS Bedrock. Supports multiple AWS auth
  methods: environment variables, credentials file, named profiles, IAM instance roles,
  SSO, or direct access keys. Use when the user asks to generate, create, draw, or produce
  an image, picture, illustration, photo, artwork, poster, icon, banner, or any visual
  content. Triggers: "generate an image", "draw me", "create a picture", "make an
  illustration", "画一张", "帮我画", "生成图片", "做一张图", "AI绘图". Requires AWS
  Bedrock access with Nova Canvas model enabled. NOT for: editing existing images,
  generating video, or HTML/CSS canvas rendering.
---

# Nova Canvas

Generate images via Amazon Nova Canvas on AWS Bedrock.

## AWS Auth Methods

| Method | How to Use |
|--------|------------|
| **Bearer token** | `AWS_BEARER_TOKEN_BEDROCK` env var or `--bearer-token` |
| **Environment variables** | Set `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY` |
| **Credentials file** | Configure `~/.aws/credentials` |
| **Named profile** | `--profile my-profile` or `AWS_PROFILE` env var |
| **Direct keys** | `--access-key AKIA... --secret-key ...` |
| **Temporary credentials** | Add `--session-token` with direct keys |
| **IAM instance role** | Auto-detected on EC2/ECS/Lambda |
| **AWS SSO** | Run `aws sso login` first |

Auto-detection order: direct keys → profile → bearer token → env vars → credentials file → instance role → SSO.

## Quick Start

```bash
python3 {baseDir}/scripts/generate.py "your prompt" -o output.png
python3 {baseDir}/scripts/generate.py "your prompt" -o output.png --profile work
python3 {baseDir}/scripts/generate.py "your prompt" -o output.png --access-key AKIA... --secret-key ...
```

## Parameters

| Flag | Default | Description |
|------|---------|-------------|
| `prompt` | — | Text description of the image |
| `-o, --output` | output.png | Output file path |
| `-W, --width` | 1024 | Width 512-4096, divisible by 64 |
| `-H, --height` | 1024 | Height 512-4096, divisible by 64 |
| `-n, --count` | 1 | Number of images (1-5) |
| `-q, --quality` | standard | `standard` or `premium` |
| `-s, --seed` | random | Seed for reproducibility |
| `--negative` | — | Negative prompt (what to avoid) |
| `--cfg` | 8.0 | CFG scale 1.1-10.0 |
| `--region` | us-east-1 | AWS region |
| `--profile` | — | AWS named profile |
| `--access-key` | — | AWS Access Key ID |
| `--secret-key` | — | AWS Secret Access Key |
| `--session-token` | — | AWS Session Token |
| `--bearer-token` | — | Bearer token (overrides env) |

## Workflow

1. Craft a detailed English prompt (Nova Canvas performs best in English).
2. Choose size: square 1024×1024, landscape 1280×768, portrait 768×1280.
3. Run `generate.py` with `timeout=120`.
4. Send resulting image to user via `message` tool.

## Prompt Tips

- Detailed English prompts yield best results.
- Specify style: "oil painting", "watercolor", "3D render", "photograph", "anime".
- Use `--negative "blurry, low quality, text, watermark"` to exclude unwanted elements.
