---
name: poster-forge
description: Universal image and poster generator with Chinese/English text support. Use when asked to create posters, social media images, cover images, infographics, comparison charts, tutorial cards, or any visual content. Three rendering engines with auto-fallback — AI generation (Pollinations.ai), HTML/CSS templates (Chromium screenshot), and pure PIL text rendering. Supports presets for Xiaohongshu, WeChat, Instagram, Twitter, and A4 print. Triggers on "make a poster", "generate image", "create cover", "design a card", "生成海报", "做封面图", "画图".
---

# Poster Forge

Universal poster/image generator with 3 engines and auto-fallback.

## Engines

| Engine | How | Best For | Reliability |
|--------|-----|----------|-------------|
| `ai` | Pollinations.ai (flux model) | Artistic/photo backgrounds | ~90% (network dependent) |
| `html` | Chromium headless screenshot | Precise layouts, text-heavy | ~99% (needs Chromium) |
| `text` | PIL solid color + text overlay | Simple text posters | 100% |

Default mode is `auto`: tries AI → HTML → text fallback.

## Quick Start

```bash
# Simple poster with AI background
python3 scripts/generate.py --title "你的标题" --prompt "watercolor sunset" --output poster.jpg

# Split comparison (HTML engine, no network needed)
python3 scripts/generate.py --title "A vs B" --mode html --template split \
  --left-label "方案A" --right-label "方案B" \
  --left-items "优点1|优点2" --right-items "优点1|优点2" --output compare.jpg

# Tutorial card
python3 scripts/generate.py --title "教程标题" --mode html --template tutorial \
  --code-content "print('hello')" --tagline "底部提示语" --output tutorial.jpg
```

## Parameters

### Core
- `--title` (required): Main title
- `--subtitle`: Secondary text
- `--tagline`: Bottom tagline
- `--mode`: `ai` | `html` | `text` | `auto` (default: auto)
- `--output`: Output file path

### Templates (HTML engine)
- `--template`: `split` | `gradient` | `card` | `tutorial`

### Size presets
- `--preset`: `xiaohongshu` (1080×1440) | `wechat` (900×500) | `instagram` (1080×1080) | `twitter` (1200×675) | `a4` (2480×3508)
- `--width` / `--height`: Custom dimensions

### Split template
- `--left-label` / `--right-label`: Side labels
- `--left-items` / `--right-items`: Pipe-separated content items
- `--left-color` / `--right-color`: R,G,B colors

### Text overlay
- `--text-position`: `bottom` | `center` | `top` | `none`
- `--font-title-size` / `--font-sub-size`: Font sizes
- `--no-overlay`: Skip PIL text overlay (when HTML already has text)

### AI engine
- `--prompt`: English description for Pollinations.ai

## Workflow for Agents

1. Decide content and style
2. Choose mode: `auto` for flexibility, `html` for reliability, `ai` for aesthetics
3. Run `scripts/generate.py` with appropriate args
4. If using `html` mode with `--template`, add `--no-overlay` (text is already in the HTML)
5. Send output image to user

## Requirements
- Python 3 + Pillow (PIL)
- curl (for AI engine font download)
- Chromium/Chrome (for HTML engine, optional)
