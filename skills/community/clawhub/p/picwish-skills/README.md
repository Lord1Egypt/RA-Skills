# PicWish Skills

[中文文档](README-zh.md)

PicWish OpenClaw Skills — 11 atomic image processing skills powered by [PicWish API](https://picwish.com).

## Features

| Skill | Description |
|---|---|
| `picwish-segmentation` | Background removal (person, object, stamp) |
| `picwish-face-cutout` | Face/avatar cutout |
| `picwish-upscale` | Image super-resolution |
| `picwish-object-removal` | Mask-based object eraser |
| `picwish-watermark-remove` | Auto watermark detection & removal |
| `picwish-id-photo` | ID photo generation |
| `picwish-colorize` | B&W photo colorization |
| `picwish-compress` | Image compression & resizing |
| `picwish-ocr` | OCR text extraction |
| `picwish-smart-crop` | Document/object perspective correction |
| `picwish-clothing-seg` | Clothing semantic segmentation |

## Quick Start

### 1. Prerequisites

- Node.js ≥ 18
- PicWish API Key ([get one here](https://picwish.com/my-account?subRoute=api-key))

### 2. Set API Key

```bash
# Option 1: Environment variable (recommended)
export PICWISH_API_KEY="your_api_key_here"

# Option 2: OpenClaw config
openclaw config set skills.entries.picwish.apiKey "your_api_key_here"
```

**China mainland users** also set region:

```bash
export PICWISH_REGION=cn
```

### 3. Install via ClawHub

```bash
npm install -g clawhub
clawhub install picwish-skills
```

### 4. Usage

```bash
node scripts/run_task.mjs --skill picwish-segmentation --input-json '{"image_url":"https://example.com/photo.jpg"}'
node scripts/run_task.mjs --skill picwish-upscale --input-json '{"image_file":"/path/to/local.jpg","type":"clean"}'
```

## Project Structure

```
picwish-skills/
├── package.json
├── SKILL.md                  # Root routing skill
├── scripts/                  # Entry point & helpers (published)
│   ├── run_task.mjs          # Unified entry point
│   └── lib/
│       ├── client.mjs        # HTTP client
│       ├── errors.mjs        # Error classification
│       └── constants.mjs     # Base URLs, polling config, status codes
└── skills/                   # 11 sub-skill definitions
    ├── picwish-segmentation/SKILL.md
    ├── picwish-face-cutout/SKILL.md
    └── ...
```

## Configuration

| Environment Variable | Description | Default |
|---|---|---|
| `PICWISH_API_KEY` | API key | — |
| `PICWISH_REGION` | `cn` (mainland) / `global` | `global` |
| `PICWISH_BASE_URL` | Override API endpoint | — |
| `PICWISH_POLL_TIMEOUT_MS` | Visual task poll timeout | `30000` |
| `PICWISH_OCR_TIMEOUT_MS` | OCR task poll timeout | `120000` |
| `PICWISH_POLL_INTERVAL_MS` | Poll interval | `1000` |

## License

MIT
