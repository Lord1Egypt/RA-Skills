---
name: photo-cinematic
description: "Professional photo processing and cinematic color grading powered by Pillow + NumPy. Use when a user asks to: (1) Edit, enhance, or retouch photos, (2) Apply cinematic/film color grading, (3) Remove haze or improve clarity, (4) Adjust saturation, vibrance, or exposure, (5) Add light effects, vignette, or film grain. Triggers on keywords like: 调色/修图/照片处理/电影感/通透/去雾/饱和度/自然饱和度/色阶。"
---

# Photo Cinematic Editor

Cinematic photo processing toolkit with Pillow + NumPy. Supports HEIC/JPEG/PNG input.

## Quick Start

```bash
# All-in-one cinematic processing (dehaze → grade → light → sharpen)
python3 scripts/photo_editor.py input.jpg output.jpg

# Custom pipeline
python3 scripts/photo_editor.py input.jpg output.jpg dehaze grade saturation=1.3 light sharpen
```

## Effects Reference

| Effect | Params | Description |
|--------|--------|-------------|
| `dehaze` | strength=1.0 | Local contrast dehazing + clarity |
| `grade` | strength=1.0 | Cinematic S-curve + teal/orange split tone + glow + vignette |
| `saturation` | saturation=1.0 | Simple saturation multiplier |
| `vibrance` | vibrance=1.0 | Smart saturation (boosts muted colors more) |
| `levels` | shadows=0 midtones=1.0 highlights=255 | Photoshop-style levels adjustment |
| `light` | strength=1.0 | Warm light streaks + highlight boost |
| `sharpen` | strength=1.0 | Unsharp mask sharpening |
| `blur` | strength=1.0 | Gaussian blur (radius in pixels) |

All params accept `strength=N` to control intensity.

## Usage Examples

```bash
# Dehaze only
python3 scripts/photo_editor.py photo.jpg out.jpg dehaze

# Cinematic from scratch
python3 scripts/photo_editor.py photo.jpg out.jpg grade

# Vibrant cinematic
python3 scripts/photo_editor.py photo.jpg out.jpg dehaze grade saturation=1.2 light sharpen

# Soft natural look
python3 scripts/photo_editor.py photo.jpg out.jpg dehaze grade vibrance=0.85 light=0.6 sharpen

# Manual levels adjustment
python3 scripts/photo_editor.py photo.jpg out.jpg levels shadows=15 midtones=1.1 highlights=240 sharpen
```

## Requirements

```bash
pip3 install Pillow numpy pillow-heif --break-system-packages
```

## Scripts

- `scripts/photo_editor.py` — Main editor with pipeline processing
- `scripts/cinematic_grade.py` — V1 classic cinematic grading
- `scripts/cinematic_v2.py` — V2 with dehaze + light texture

## References

See `references/photo-editing-guide.md` for technique explanations and advanced workflows.
