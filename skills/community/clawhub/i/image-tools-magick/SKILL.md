---
name: Image Tools
description: Comprehensive image editing toolkit using ImageMagick. Resize, crop, composite (overlay), pad, annotate, adjust (brightness/contrast/blur/rotate/flip), remove backgrounds, convert formats, and get image info. All operations are non-destructive (output to new file).
metadata: {"openclaw":{"emoji":"🖼️","os":["linux","darwin"]}}
---

# Image Tools (ImageMagick)

Pixel-level image manipulation via shell scripts. For AI-based editing (add/remove content with prompts), see `nano-banana-pro`.

**Requires:** `imagemagick` (`apt install imagemagick` / `brew install imagemagick`)

## Scripts

All scripts are in `scripts/` relative to this skill. All output to a new file (non-destructive).

### 🔧 resize.sh — Resize images
```bash
scripts/resize.sh <input> <geometry> [output]
```
| Geometry | Effect |
|----------|--------|
| `800x` | Width 800, keep aspect ratio |
| `800x600` | Fit within 800x600 |
| `800x600!` | Force exact 800x600 (distort) |
| `50%` | Scale to 50% |
| `800x800\>` | Shrink only if larger |

### ✂️ crop.sh — Crop images
```bash
scripts/crop.sh <input> <WxH+X+Y> [output]
```
- `500x500+100+50` — crop 500x500 starting at pixel (100, 50)
- `500x500+center` — center crop (special mode)

### 🧩 composite.sh — Overlay / place image on image
```bash
scripts/composite.sh <background> <overlay> [output] [options]
```
Options: `--gravity`, `--offset +X+Y`, `--resize GEO`, `--opacity PCT`
- Place logo on photo: `scripts/composite.sh bg.jpg logo.png out.jpg --gravity southeast`
- Watermark: `scripts/composite.sh bg.jpg mark.png out.jpg --opacity 30 --resize 200x200`

### 📐 pad.sh — Add padding / extend canvas
```bash
scripts/pad.sh <input> <WxH> [output] [--color COL] [--gravity POS]
```
- Make square: `scripts/pad.sh wide.jpg 1080x1080 --color white`
- Transparent pad: `scripts/pad.sh icon.png 512x512 --color none`

### 🎨 adjust.sh — Brightness, contrast, rotate, flip, blur, etc.
```bash
scripts/adjust.sh <input> [output] [options]
```
Options: `--brightness N`, `--contrast N`, `--saturation N`, `--rotate N`, `--flip`, `--flop`, `--grayscale`, `--blur 0xN`, `--sharpen 0xN`, `--negate`, `--border WxH`, `--border-color COL`

### 🔤 annotate.sh — Add text overlay
```bash
scripts/annotate.sh <input> <text> [output] [options]
```
Options: `--font`, `--size`, `--color`, `--bg`, `--gravity`, `--offset`, `--stroke`, `--stroke-width`

### 🧹 remove-bg.sh — Remove solid background color → transparent
```bash
scripts/remove-bg.sh <input> <output> [tolerance%] [color]
```
- Remove white: `scripts/remove-bg.sh icon.png clean.png`
- Remove green screen: `scripts/remove-bg.sh photo.png clean.png 25 "#00FF00"`

### 🔄 convert-format.sh — Format conversion
```bash
scripts/convert-format.sh <input> <output> [--quality N] [--strip]
```
Supports: PNG, JPG, WebP, GIF, BMP, TIFF

### ℹ️ info.sh — Image metadata
```bash
scripts/info.sh <image>
```

## Direct ImageMagick (for anything not covered by scripts)
```bash
# Tile/montage multiple images
montage img1.jpg img2.jpg img3.jpg -geometry 300x300+5+5 montage.jpg

# Generate app icon set
for size in 1024 512 256 128 64 32 16; do
  convert icon.png -resize ${size}x${size} icon-${size}.png
done

# Rounded corners
convert input.png \( +clone -alpha extract -draw 'fill black polygon 0,0 0,15 15,0 fill white circle 15,15 15,0' \
  \( +clone -flip \) -compose Multiply -composite \( +clone -flop \) -compose Multiply -composite \) \
  -alpha off -compose CopyOpacity -composite rounded.png

# Append images (horizontal / vertical)
convert img1.jpg img2.jpg +append horizontal.jpg    # side by side
convert img1.jpg img2.jpg -append vertical.jpg      # stacked
```

## AI-Based Editing

For adding/removing objects, style transfer, or content-aware edits, use the **nano-banana-pro** skill (Gemini image editing):
```bash
uv run /root/shared/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "remove the person on the left" \
  --input-image photo.jpg \
  --filename edited.png
```
