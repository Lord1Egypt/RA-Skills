# Pillow Image Processing Skill

English | [简体中文](README_CN.md)

A comprehensive skill for image processing using Pillow (PIL). Provides powerful tools for editing, batch processing, watermarking, and analyzing images.

## Features

- **Image Editing**: Resize, crop, rotate, flip, adjust colors and apply filters
- **Batch Processing**: Process multiple images in parallel with consistent operations
- **Watermarking**: Add text or image watermarks with custom positioning and opacity
- **Image Analysis**: Extract detailed information, metadata, and EXIF data
- **Format Conversion**: Convert between JPEG, PNG, GIF, BMP, TIFF, WebP and more

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### Edit a Single Image
```bash
# Resize with aspect ratio
python scripts/image_editor.py input.jpg output.jpg --width 800

# Crop and rotate
python scripts/image_editor.py photo.jpg edited.jpg \
    --crop 100 100 800 600 \
    --rotate 90

# Adjust brightness and contrast
python scripts/image_editor.py dark.jpg bright.jpg \
    --brightness 1.5 \
    --contrast 1.2
```

### Batch Process Multiple Images
```bash
# Create thumbnails for all images
python scripts/batch_processor.py ./photos ./thumbnails \
    --thumbnail 300 300

# Convert all images to JPEG
python scripts/batch_processor.py ./images ./output \
    --format JPEG \
    --quality 90
```

### Add Watermark
```bash
# Text watermark
python scripts/watermark.py input.jpg output.jpg \
    --text "© 2026 MyCompany" \
    --position bottom-right

# Image watermark
python scripts/watermark.py photo.jpg watermarked.jpg \
    --image logo.png \
    --scale 0.15 \
    --opacity 180
```

### Extract Image Information
```bash
# Display image info
python scripts/image_info.py photo.jpg

# Save info as JSON
python scripts/image_info.py photo.jpg -o info.json --format json
```

## Directory Structure

```
pillow-skill/
├── SKILL.md                    # Main skill documentation (English)
├── SKILL_CN.md                 # Main skill documentation (Chinese)
├── README.md                   # This file
├── README_CN.md                # Chinese README
├── EXAMPLES.md                 # Usage examples (English)
├── EXAMPLES_CN.md              # Usage examples (Chinese)
├── requirements.txt            # Python dependencies
├── scripts/
│   ├── image_editor.py        # Single image editing tool
│   ├── batch_processor.py     # Batch processing tool
│   ├── watermark.py           # Watermarking tool
│   └── image_info.py          # Image information extractor
├── references/
│   ├── common_operations.md   # Pillow operations reference
│   └── best_practices.md      # Image processing best practices
└── assets/
    └── templates/             # Template images and resources
```

## Documentation

- **SKILL.md / SKILL_CN.md**: Complete skill documentation with all capabilities
- **EXAMPLES.md / EXAMPLES_CN.md**: Comprehensive usage examples and tutorials
- **references/common_operations.md**: Quick reference for Pillow operations
- **references/best_practices.md**: Best practices and optimization techniques

## Use Cases

- ✅ Create thumbnails for web galleries
- ✅ Batch resize images for mobile apps
- ✅ Add watermarks to protect copyrights
- ✅ Convert images for web optimization
- ✅ Extract and analyze image metadata
- ✅ Apply filters and effects to photos
- ✅ Automate image processing workflows

## Requirements

- Python 3.8+
- Pillow 10.0+

## License

MIT License
