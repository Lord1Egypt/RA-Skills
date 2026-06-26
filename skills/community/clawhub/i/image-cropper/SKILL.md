# Image Cropper

Crop images based on bounding box annotations. Supports COCO, YOLO, VOC, and LabelMe formats. Use when user needs to extract objects from images based on annotation boxes.

## Features

- **Multi-format Support**: COCO, YOLO, VOC, LabelMe
- **Batch Processing**: Crop entire datasets
- **Padding**: Add padding around bounding boxes
- **Output Options**: Individual files or sprite sheet
- **Handle Missing**: Gracefully handle images without annotations

## Usage

```bash
# Crop YOLO annotations
python scripts/cropper.py yolo images/ labels/ output/

# Crop COCO annotations
python scripts/cropper.py coco annotations.json images/ output/

# Crop with padding
python scripts/cropper.py yolo images/ labels/ output/ --padding 10

# Crop all objects to individual files
python scripts/cropper.py yolo images/ labels/ output/ --objects
```

## Examples

```
$ python scripts/cropper.py yolo ./images ./labels ./output

Processing 100 images...
✓ Cropped 250 objects from image_001.jpg
✓ Cropped 180 objects from image_002.jpg
...
Total: 500 cropped images
```

## Installation

```bash
pip install pillow
```

## Options

- `--padding`: Padding around box (pixels, default: 0)
- `--objects`: Save each object as separate file
- `--min-size`: Minimum box size to crop (pixels)
- `--format`: Output format (jpg, png, default: jpg)
- `--quality`: JPEG quality 1-100 (default: 95)
