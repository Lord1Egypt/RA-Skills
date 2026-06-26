---
name: image-handler
description: Read, analyze, convert, and manipulate image files (PNG, JPG, GIF, WebP, TIFF, BMP, HEIC, SVG, ICO). Use when working with images: reading metadata, converting formats, resizing, rotating, compressing, or batch processing. Triggers on mentions of image files, file paths with image extensions, or requests to process/convert images.
---

# Image Handler

Analyze, convert, and manipulate image files.

## Supported Formats

| Format | Extensions | Read | Convert | Metadata |
|--------|------------|------|---------|----------|
| PNG | .png | ✅ | ✅ | ✅ |
| JPEG | .jpg, .jpeg | ✅ | ✅ | ✅ |
| GIF | .gif | ✅ | ✅ | ✅ |
| WebP | .webp | ✅ | ✅ | ✅ |
| TIFF | .tiff, .tif | ✅ | ✅ | ✅ |
| BMP | .bmp | ✅ | ✅ | ✅ |
| HEIC | .heic, .heif | ✅ | ✅ | ✅ |
| SVG | .svg | ✅ | ✅ | - |
| ICO | .ico | ✅ | ✅ | ✅ |

## Quick Commands

### Metadata (sips - built-in macOS)

```bash
# Get all properties
sips -g all image.jpg

# Get specific properties
sips -g pixelWidth -g pixelHeight -g format -g dpiWidth -g dpiHeight image.jpg

# JSON-like output (parseable)
sips -g all image.jpg 2>&1 | tail +2
```

### Convert Formats

```bash
# Convert to PNG
sips -s format png input.jpg --out output.png

# Convert to JPEG with quality
sips -s format jpeg -s formatOptions 85 input.png --out output.jpg

# Convert HEIC to JPEG
sips -s format jpeg input.heic --out output.jpg

# Batch convert (shell)
for f in *.heic; do sips -s format jpeg "$f" --out "${f%.heic}.jpg"; done
```

### Resize

```bash
# Resize to max dimensions (maintains aspect ratio)
sips --resampleWidth 1920 image.jpg --out resized.jpg
sips --resampleHeight 1080 image.jpg --out resized.jpg

# Resize to exact dimensions
sips --resampleWidth 1920 --resampleHeight 1080 image.jpg --out resized.jpg

# Scale by percentage
sips --resampleWidth 50% image.jpg --out half.jpg
```

### Rotate & Flip

```bash
# Rotate 90 degrees clockwise
sips --rotate 90 image.jpg --out rotated.jpg

# Rotate 180 degrees
sips --rotate 180 image.jpg --out rotated.jpg

# Flip horizontal
sips --flip horizontal image.jpg --out flipped.jpg

# Flip vertical
sips --flip vertical image.jpg --out flipped.jpg
```

### Crop

```bash
# Crop to specific pixels (x, y, width, height)
sips --cropToHeightWidth 500 500 image.jpg --out cropped.jpg

# Crop from center
sips --cropToHeightWidth 500 500 --cropOffset 100 100 image.jpg --out cropped.jpg
```

### Strip Metadata

```bash
# Remove EXIF and all metadata
sips --deleteProperty all image.jpg --out clean.jpg
```

### ffmpeg (advanced operations)

```bash
# WebP to PNG
ffmpeg -i input.webp output.png

# Extract frames from GIF
ffmpeg -i animation.gif frame_%03d.png

# Create GIF from images
ffmpeg -framerate 10 -i frame_%03d.png output.gif

# Resize with ffmpeg
ffmpeg -i input.jpg -vf scale=1920:-1 output.jpg

# Convert video to GIF
ffmpeg -i video.mp4 -vf "fps=10,scale=480:-1" output.gif
```

## Scripts

### image_info.sh

Get comprehensive image metadata.

```bash
~/Dropbox/jarvis/skills/image-handler/scripts/image_info.sh <image>
```

### convert_image.sh

Convert between formats with options.

```bash
~/Dropbox/jarvis/skills/image-handler/scripts/convert_image.sh <input> <output> [quality]
```

### batch_convert.sh

Convert all images in a directory.

```bash
~/Dropbox/jarvis/skills/image-handler/scripts/batch_convert.sh <input_dir> <output_format> [output_dir]
```

## Workflow

1. **Get info** — `sips -g all` for dimensions, format, metadata
2. **Convert if needed** — Change format for compatibility
3. **Resize/optimize** — Reduce file size for web/sharing
4. **Strip metadata** — Remove EXIF for privacy

## Notes

- `sips` is built into macOS — no installation needed
- `ffmpeg` handles WebP, animated GIFs, and video-to-image
- For HEIC (iPhone photos), convert to JPEG for compatibility
- SVG is text-based — use `cat` or text tools
- For OCR on images, use the document-handler skill