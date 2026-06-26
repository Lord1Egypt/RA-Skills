# Image Quality Filter

Detect and filter out low-quality images including blurry, dark, too bright, or low resolution images. Use when user wants to clean up image datasets by removing poor quality images.

## Features

- **Blur Detection**: Detect blurry images using Laplacian variance
- **Brightness Analysis**: Find too dark or too bright images
- **Resolution Filter**: Remove low-resolution images
- **Quality Score**: Compute overall quality score
- **Batch Processing**: Process large image folders
- **Multiple Actions**: List, delete, or move low-quality images

## Usage

```bash
# Scan for low quality images
python scripts/quality_filter.py scan /path/to/images/

# Filter with custom thresholds
python scripts/quality_filter.py scan /path/to/images/ \
  --blur-threshold 100 \
  --min-resolution 640x480 \
  --min-brightness 30 \
  --max-brightness 220

# Delete low quality images
python scripts/quality_filter.py scan /path/to/images/ --action delete
```

## Examples

```
$ python scripts/quality_filter.py scan ./images/

Scanning 150 images...
Analyzing quality...
Found 12 low-quality images:

[BLUR]   photo_blurry.jpg (score: 45)
[BLUR]   image_low.jpg (score: 62)
[DARK]   dark_photo.jpg (score: 38)
[BRIGHT] overexposed.jpg (score: 41)
[RES]    tiny_image.png (320x240)

Total: 12 low-quality images removed
```

## Quality Criteria

| Criterion | Threshold | Description |
|-----------|-----------|-------------|
| Blur | < 100 | Laplacian variance (lower = blurrier) |
| Brightness | 30-220 | Out of range is poor |
| Resolution | > 640x480 | Below minimum is low quality |

## Installation

```bash
pip install pillow numpy opencv-python
```

## Options

- `--blur-threshold`: Blur threshold (default: 100)
- `--min-resolution`: Minimum resolution (default: 640x480)
- `--min-brightness`: Minimum brightness 0-255 (default: 30)
- `--max-brightness`: Maximum brightness 0-255 (default: 220)
- `--action`: What to do (list, delete, move)
- `--output`: Output folder for --action move
