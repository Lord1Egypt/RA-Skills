---
name: image-nuke
description: "Nuclear-grade image metadata cleanser. Strip ALL EXIF/GPS/camera data, re-encode with noise injection. Forensically untraceable, reverse image search resistant."
metadata:
  openclaw:
    emoji: "☢️"
    requires:
      bins: ["python3"]
---

# Image Nuke - Nuclear Metadata Cleanser

Strip everything. Re-encode. Inject noise. Forensically untraceable.

## What Gets Destroyed

- ALL EXIF data (camera, lens, exposure, timestamps, software)
- GPS / location coordinates
- ICC color profiles
- XMP / IPTC metadata
- Adobe tags and editing history
- Embedded thumbnails

## Nuclear Operations

- Sub-pixel Gaussian noise injection (invisible to human eye)
- Micro color shift (undetectable hue rotation)
- Per-pixel brightness variation
- Random micro-crop (changes dimensions by 1-3px)
- Fresh JPEG re-encoding with randomized quality/subsampling
- Different perceptual hash (reverse image search resistant)

## Usage

```bash
# Single image - nuclear mode
python3 {baseDir}/scripts/nuke_image.py photo.jpg

# Custom output + max noise
python3 {baseDir}/scripts/nuke_image.py photo.jpg clean.jpg --noise 5

# Batch process entire directory
python3 {baseDir}/scripts/nuke_image.py --batch ./photos/ ./clean/

# Lower quality for harder reverse matching
python3 {baseDir}/scripts/nuke_image.py photo.jpg --quality 80 --noise 4
```

## Noise Levels

| Level | Sigma | Use Case |
|-------|-------|----------|
| 1 | 0.8 | Light cleanse - metadata only feel |
| 2 | 1.6 | Standard - good balance |
| 3 | 2.4 | Default - recommended |
| 4 | 3.2 | Heavy - reverse search resistant |
| 5 | 4.0 | Nuclear - maximum anonymization |

## Requirements

- Python 3
- Pillow (`pip install Pillow`)
- NumPy (`pip install numpy`)

## Notes

- Output is always JPEG (even if input is PNG)
- Original file is never modified
- Each run produces a unique output (randomized noise)
