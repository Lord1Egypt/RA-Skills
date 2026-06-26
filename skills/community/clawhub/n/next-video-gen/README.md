# Next Video Gen

<p align="center">
  <strong>AI image & video generation via Volcengine Ark API — text-to-image, text-to-video, image-to-video, video-to-video.</strong>
</p>

<p align="center">
  <a href="#what-it-does">Features</a> •
  <a href="#installation">Install</a> •
  <a href="#getting-an-api-key">API Key</a>
</p>

<p align="center">
  <strong>Languages:</strong>
  <a href="README.md">English</a> |
  <a href="README.zh-CN.md">简体中文</a> |
  <a href="README.zh-TW.md">繁體中文</a>
</p>

---

## What It Does

A skill for AI coding agents (Claude Code, Cursor, etc.) that enables image and video generation via the Seedance 2.0 model on Volcengine Ark platform.

| Skill | Description | Model |
|-------|-------------|-------|
| **Next Video Gen** | Text-to-image, text-to-video, image-to-video, video-to-video | Seedance 2.0 |

---

## Installation

### Quick Install

```bash
openclaw skills add https://github.com/vennduan/next-video-gen
```

### Manual Install

```bash
git clone https://github.com/vennduan/next-video-gen.git
cd next-video-gen
openclaw skills add .
```

---

## Getting an API Key

1. Sign up at [console.volcengine.com/ark](https://console.volcengine.com/ark)
2. Go to API Keys and create a new key
3. Set it in your environment:

```bash
export DOUBAO_API_KEY=your_key_here
```

---

## What It Can Do

- **Text-to-image** — Describe a scene, get a high-quality image (PNG/JPEG/WebP)
- **Text-to-video** — Describe a scene, get a video (silent)
- **Text-to-video with audio** — Describe scene + sound, generates synchronized audio/video (default)
- **Image-to-video** — Animate an image with a text prompt (silent)
- **Image-to-video with audio** — Image + prompt + auto audio (default when image provided)
- **Video-to-video** — Provide a video + prompt, generate a new video based on the source material
- **Multiple resolutions** — Images: 2K / 1K / HD; Videos: 480p, 720p, 1080p
- **Flexible duration** — 4–12 seconds (videos)
- **Aspect ratios** — Images: 1:1 / 16:9 / 9:16; Videos: 16:9, 9:16, 1:1

### Usage Examples

Just talk to your agent:

> "Generate an image of a futuristic city at sunset"

> "Generate a 5-second video of a cat playing piano"

> "Create a cinematic sunset over the ocean, 720p, 16:9"

> "Use this image and animate it into an 8-second video"

> "Take this video and make it more vibrant with faster motion"

> "Generate a video with background music and bird sounds"

The agent guides you through any missing details and handles the generation.

### Requirements

- `curl` and `jq` installed on your system
- `DOUBAO_API_KEY` environment variable set

### Script Reference

The skill includes `scripts/seedance-gen.sh` for direct command-line use:

```bash
# Text-to-image
./scripts/seedance-gen.sh "A futuristic city at sunset, neon lights" --mode txt2img

# Text-to-image (large)
./scripts/seedance-gen.sh "Abstract art, vibrant colors" --mode txt2img --quality 2K

# Text-to-video with audio (default)
./scripts/seedance-gen.sh "A cat running through a sunny meadow, birds singing" --mode txt2video --duration 5

# Text-to-video without audio
./scripts/seedance-gen.sh "Ocean sunset timelapse" --mode txt2video --no-audio

# Image-to-video with audio (default)
./scripts/seedance-gen.sh "Camera slowly pans in, cat turns to look" --mode img2video --image "https://example.com/cat.jpg"

# Image-to-video without audio
./scripts/seedance-gen.sh "Animate the image" --mode img2video --image "https://example.com/img.jpg" --no-audio

# Video-to-video
./scripts/seedance-gen.sh "Make it more vibrant, faster motion" --mode vid2video --video "https://example.com/input.mp4"

# Specify resolution and duration
./scripts/seedance-gen.sh "Drone footage over a valley" --mode txt2video --duration 8 --quality 1080p

# Vertical format for social media
./scripts/seedance-gen.sh "Waterfall flowing" --mode txt2video --aspect-ratio 9:16

# Disable watermark
./scripts/seedance-gen.sh "Abstract art animation" --mode txt2video --watermark false
```

Output is saved to `~/Videos/next-video-gen/` (configurable via `NEXT_VIDEO_GEN_OUTPUT_DIR`).

### API Parameters

See [references/api-params.md](references/api-params.md) for complete API documentation.

---

## File Structure

```
.
├── README.md                    # This file
├── README.zh-CN.md              # Simplified Chinese
├── README.zh-TW.md              # Traditional Chinese
├── SKILL.md                     # Agent skill definition
├── _meta.json                   # Skill metadata
├── references/
│   └── api-params.md            # Complete API parameter reference
└── scripts/
    └── seedance-gen.sh          # Generation script
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `jq: command not found` | Install jq: `apt install jq` / `brew install jq` |
| `401 Unauthorized` | Check your `DOUBAO_API_KEY` at [console.volcengine.com/ark](https://console.volcengine.com/ark) |
| `403 Forbidden` | Check API key permissions in the Volcengine console |
| `429 Too Many Requests` | Rate limited — wait and retry |
| `Content blocked` | Modify your prompt |
| Generation timeout | Videos can take 1–3 minutes, images are usually 5–15 seconds |

---

## License

MIT
