---
name: neodomain-ai
description: Generate images and videos via Neodomain AI API. Supports text-to-image, image-to-video, text-to-video, and motion control video generation. Use when user wants to create AI-generated images or videos using the Neodomain platform.
metadata:
  {
    "openclaw":
      {
        "emoji": "🎨",
        "requires": { "bins": ["python3"], "env": ["NEODOMAIN_ACCESS_TOKEN"] },
        "primaryEnv": "NEODOMAIN_ACCESS_TOKEN",
      },
  }
---

# Neodomain AI Content Generator

Generate images and videos using the Neodomain AI platform API.

## Setup

Set your access token as an environment variable:

```bash
export NEODOMAIN_ACCESS_TOKEN="your_access_token_here"
```

Or pass it directly to scripts via `--token` flag.

## Image Generation

### Get Available Models

```bash
python3 {baseDir}/scripts/image_models.py --token $NEODOMAIN_ACCESS_TOKEN
```

### Generate Images

```bash
# Basic text-to-image
python3 {baseDir}/scripts/generate_image.py --prompt "A futuristic city at sunset" --token $NEODOMAIN_ACCESS_TOKEN

# With options
python3 {baseDir}/scripts/generate_image.py \
  --prompt "A beautiful mountain landscape" \
  --negative-prompt "blurry, low quality" \
  --model "doubao-seedream-4-0" \
  --aspect-ratio "16:9" \
  --num-images 4 \
  --size "2K" \
  --output-dir ./output/images \
  --token $NEODOMAIN_ACCESS_TOKEN
```

### Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--prompt` | Text description for image generation | Required |
| `--negative-prompt` | Things to exclude from image | Empty |
| `--model` | Model name (see models list) | `gemini-3.1-flash-image-preview` |
| `--aspect-ratio` | Image aspect ratio: `1:1`, `16:9`, `9:16`, `4:3`, `3:4` | `1:1` |
| `--num-images` | Number of images to generate: `1` or `4` | `1` |
| `--size` | Image size: `1K`, `2K`, `4K` | `2K` |
| `--guidance-scale` | Prompt adherence (1.0-20.0) | `7.5` |
| `--seed` | Random seed for reproducibility | Random |
| `--output-format` | Output format: `jpeg`, `png`, `webp` | `jpeg` |
| `--output-dir` | Where to save images | `./output` |

### Image Generation with Reference Images

Use `generate_image_ref.py` to generate images with character reference(s). Supports up to 10 reference images per generation:

```bash
# Single reference image
python3 {baseDir}/scripts/generate_image_ref.py \
  --prompt "A woman walking in a forest" \
  --reference-image "https://example.com/character1.jpg" \
  --model "doubao-seedream-5-0-260128" \
  --aspect-ratio "16:9" \
  --token $NEODOMAIN_ACCESS_TOKEN

# Multiple reference images (up to 10)
python3 {baseDir}/scripts/generate_image_ref.py \
  --prompt "A conversation between two people" \
  --reference-image "https://example.com/character1.jpg" \
  --reference-image "https://example.com/character2.jpg" \
  --reference-image "https://example.com/character3.jpg" \
  --model "doubao-seedream-5-0-260128" \
  --aspect-ratio "16:9" \
  --token $NEODOMAIN_ACCESS_TOKEN
```

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--reference-image` | Reference image URL(s) - can specify multiple (up to 10) | - |

## Video Generation

### Get Available Models

```bash
python3 {baseDir}/scripts/video_models.py --token $NEODOMAIN_ACCESS_TOKEN
```

### Generate Videos

#### Text-to-Video

```bash
python3 {baseDir}/scripts/generate_video.py \
  --prompt "A serene lake at dawn with mist rising from the water" \
  --model "veo3" \
  --generation-type "TEXT_TO_VIDEO" \
  --aspect-ratio "16:9" \
  --resolution "720p" \
  --duration "8s" \
  --token $NEODOMAIN_ACCESS_TOKEN
```

#### Image-to-Video

```bash
python3 {baseDir}/scripts/generate_video.py \
  --prompt "The camera slowly pans across the landscape" \
  --model "veo3" \
  --generation-type "IMAGE_TO_VIDEO" \
  --first-frame "https://example.com/image.jpg" \
  --aspect-ratio "16:9" \
  --resolution "720p" \
  --duration "8s" \
  --token $NEODOMAIN_ACCESS_TOKEN
```

#### Motion Control (Image + Video Reference)

```bash
python3 {baseDir}/scripts/motion_control.py \
  --image "https://example.com/ref_image.jpg" \
  --video "https://example.com/ref_video.mp4" \
  --prompt "Make the character dance" \
  --mode "pro" \
  --duration 5000 \
  --token $NEODOMAIN_ACCESS_TOKEN
```

### Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--prompt` | Text description for video | Required |
| `--model` | Model name: `veo3`, `hailuo02`, `doubao` | `veo3` |
| `--generation-type` | Type: `TEXT_TO_VIDEO`, `IMAGE_TO_VIDEO`, `REFERENCE_TO_VIDEO` | `TEXT_TO_VIDEO` |
| `--first-frame` | First frame image URL (for IMAGE_TO_VIDEO) | - |
| `--last-frame` | Last frame image URL (optional) | - |
| `--image-urls` | Reference images (comma-separated, for REFERENCE_TO_VIDEO) | - |
| `--aspect-ratio` | Video aspect: `16:9`, `9:16`, `1:1` | `16:9` |
| `--resolution` | Resolution: `720p`, `768p`, `1080p` | `720p` |
| `--duration` | Duration: `4s`, `5s`, `6s`, `8s`, `10s`, `16s` | `8s` |
| `--fps` | Frame rate | `24` |
| `--seed` | Random seed | Random |
| `--generate-audio` | Generate audio (true/false) | `false` |
| `--enhance-prompt` | Enhance prompt (true/false) | `false` |
| `--output-dir` | Where to save output | `./output` |

## Authentication

> **重要**: 每次 token 过期或首次使用时，动态询问用户登录账号（手机号/邮箱），不要硬编码保存。

If you need to obtain an access token:

```bash
# 1. 发送验证码 (询问用户手机号或邮箱)
python3 {baseDir}/scripts/login.py --send-code --contact "用户手机号或邮箱"

# 2. 用户提供验证码后，登录获取 token
python3 {baseDir}/scripts/login.py --login --contact "用户手机号或邮箱" --code "验证码"
```

The login script will output an access token that you can store in `NEODOMAIN_ACCESS_TOKEN`.

## Workflow

1. **Authenticate** (first time only): Get your access token
2. **Get models**: Check available models for your needs
3. **Generate**: Create content with appropriate parameters
4. **Wait**: Scripts automatically poll for results
5. **Download**: Images/videos saved to output directory

## Output

- Images: `*.jpg`, `*.png`, or `*.webp` files
- Videos: `*.mp4` files with thumbnail
- `metadata.json` with generation details
