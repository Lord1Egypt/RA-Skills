---
name: img-compress
description: Batch compress image file sizes (JPG/PNG), keep dimensions, reduce volume. Activate when user mentions: compress images, reduce image size, image optimization, batch compress images.
---

# img-compress

Batch image compression tool based on Pillow(PIL).

## Quick Usage

```bash
# Compress images over 100KB to 80KB
sudo python3 skills/img-compress/scripts/compress_img.py /path/to/images

# Custom target size (KB)
sudo python3 skills/img-compress/scripts/compress_img.py /path/to/images 150
```

## Compression Rules

- JPG/JPEG: Gradually reduce quality (85→50) + optimize until under target size
- PNG: Pillow PNG compression (limited), recommend pngquant for better results
- Files under target size are skipped
- Overwrites original files (in-place)

## Dependencies

- Python3
- Pillow: `pip3 install Pillow`

## Typical Scenarios

```bash
# Compress website static assets
sudo python3 skills/img-compress/scripts/compress_img.py /var/www/static/img 100
```
