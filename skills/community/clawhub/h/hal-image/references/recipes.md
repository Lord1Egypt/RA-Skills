# hal-image recipes — less common operations

Depth for operations beyond the core `SKILL.md`. Every command here is verified
to run as written with ImageMagick 7 (`magick`). Same disciplines apply:
compress before delivering, never expose local paths, fail open.

## Borders and padding

```bash
# Solid border (12px) around the image
magick in.png -bordercolor "#1e2530" -border 12 out.png

# Pad to a fixed canvas (e.g. 600x600), centered, on a background color
magick in.png -background "#0b0e14" -gravity center -extent 600x600 out.png
```

## Thumbnails (exact size, fill and crop)

The `^` makes the resize *fill* the box (shorter side fits), then `-extent`
crops the overflow — produces an exact NxN thumbnail with no distortion.

```bash
magick in.png -resize 200x200^ -gravity center -extent 200x200 thumb.png
```

## Rounded corners

Build an alpha mask with rounded corners and copy it onto the image's opacity:

```bash
magick in.png \
  \( +clone -alpha extract \
     -draw 'fill black polygon 0,0 0,20 20,0 fill white circle 20,20 20,0' \
     \( +clone -flip \) -compose Multiply -composite \
     \( +clone -flop \) -compose Multiply -composite \) \
  -alpha off -compose CopyOpacity -composite out.png
```

(The `20` is the corner radius in pixels; raise it for rounder corners. Output
must be a format with alpha, e.g. PNG.)

## Format / quality trade-offs

```bash
# JPEG at a chosen quality (lossy; 80-88 is a good size/quality balance)
magick in.png -quality 85 out.jpg

# Flatten transparency onto a solid color when going to JPEG (no alpha)
magick in.png -background "#ffffff" -flatten out.jpg
```

For *lossless* size reduction, prefer the compressors in `SKILL.md` (oxipng /
jpegoptim / cwebp) over dropping JPEG quality.

## EXIF / metadata

```bash
# Apply EXIF orientation then drop the EXIF (so the pixels are upright and the
# rotation tag won't double-apply later)
magick in.jpg -auto-orient -strip out.jpg

# Strip all metadata without other changes
magick in.png -strip out.png
```

`oxipng --strip safe` (in `SKILL.md`) also strips non-essential PNG metadata
losslessly — prefer it for PNG.

## Animated GIF from frames

```bash
# 50 = delay between frames in 1/100s (so 0.5s per frame); loop forever by default
magick -delay 50 frame1.png frame2.png frame3.png anim.gif
```

GIFs get large fast — for a long sequence consider WebP (`cwebp`) or hand it to
`ffmpeg` if it is available.

## Scripting helpers

```bash
# Just the width / height (no decoration) — for conditional logic
W=$(identify -format '%w' in.png)
H=$(identify -format '%h' in.png)

# File size in bytes
identify -format '%[size]' in.png
```

Use these to decide whether to resize/compress before reading a large image
into context or sending it.

## Batch processing

```bash
# Resize every PNG in a directory to 1200px wide, writing to out/
mkdir -p out
for f in *.png; do magick "$f" -resize 1200x "out/$f"; done

# Compress every PNG in a directory in place
for f in *.png; do oxipng -o max --strip safe "$f"; done
```

Keep batches bounded and log what you processed — don't silently skip files.

## When to reach for another tool

- **`ffmpeg`** — video frames, video↔GIF, or heavy animation work.
- **`cwebp` / `dwebp`** — WebP encode/decode (lossless WebP can beat PNG on
  photographic content).

ImageMagick handles the vast majority of everyday still-image needs; only add
another tool when the task genuinely needs it (YAGNI).
