# MiniMax image-01 Text-to-Image Generator

**Skill Name:** minimax-image-gen
**Category:** Image Generation / Text-to-Image
**Author:** Mzusama
**Price:** Free

---

## Short Description
Generate images from text using MiniMax image-01 model. Supports both Global and China API endpoints. 50 free images/day via Token Plan.

## Features
- **Text-to-Image generation** using MiniMax image-01 model
- **Dual-region support**: China (api.minimax.chat) and Global (api.minimax.io)
- **Prompt enhancement**: Automatically enhances short prompts with professional photography/art parameters
- **Aspect ratio control**: 16:9, 1:1, 4:3, 9:16, 21:9, etc.
- **Batch generation**: Generate up to 9 images at once
- **Token Plan compatible**: Uses existing MiniMax Token Plan quota

### Quick Example
```
你：帮我画一张赛博朋克风格的城市夜景
→ Runs: python image_gen.py "cyberpunk city, neon lights..." --region cn

你：generate an image of a red sports car
→ Runs: python image_gen.py "red sports car on sunset highway" --region global
```

### Requirements
- MiniMax API key (get from MiniMax platform)
- Set `MINIMAX_API_KEY` environment variable
- Python with `requests` library

### Region Selection
- `--region cn` for China/MiniMax CN users
- `--region global` for International users

### ⚠️ Daily Quota (Token Plan)
| Plan | Daily Images | Notes |
|------|-------------|-------|
| Starter | 0 | No image generation |
| **Plus** | **50 images/day** | Default, recommended |
| Max | 120 images/day | |
| Ultra | 800 images/day | |

Quota resets daily at midnight. Uses your existing Token Plan balance — no extra cost.

### Model Info
- **Model:** MiniMax image-01
- **Endpoints:** api.minimax.io (Global) | api.minimax.chat (China)

### Author
**Mzusama**
