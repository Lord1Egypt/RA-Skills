# Image Deduplicator

Find and remove duplicate or similar images in a folder using perceptual hashing. Use when user wants to clean up duplicate images, find near-duplicates, or deduplicate an image dataset.

## Features

- **Exact Duplicates**: Find images with identical content
- **Similar Images**: Detect visually similar images (threshold configurable)
- **Hash-based**: Fast MD5 hashing for exact duplicates
- **Perceptual Hash**: pHash for finding similar images
- **Batch Processing**: Process large image folders
- **Multiple Actions**: List, delete, or move duplicates

## Usage

```bash
# Find exact duplicates
python scripts/dedupe.py scan /path/to/images/

# Find similar images (90% similarity)
python scripts/dedupe.py scan /path/to/images/ --threshold 90

# Delete duplicates (keeps first occurrence)
python scripts/dedupe.py scan /path/to/images/ --action delete

# Move duplicates to a folder
python scripts/dedupe.py scan /path/to/images/ --action move --output /path/to/dupes/
```

## Examples

```
$ python scripts/dedupe.py scan ./images/

Scanning images...
Found 150 images
Computing hashes...
Found 5 duplicate groups:

Group 1 (3 files):
  ./images/photo1.jpg
  ./images/photo1_copy.jpg
  ./images/photo1_final.jpg

Group 2 (2 files):
  ./images/screenshot.png
  ./images/screenshot (1).png

Total: 5 duplicate groups, 8 duplicate files
```

## Installation

```bash
pip install pillow imagehash
```

## Options

- `--threshold`: Similarity threshold (0-100), default: 100 (exact)
- `--action`: What to do with duplicates (list, delete, move)
- `--output`: Output folder for --action move
- `--extensions`: File extensions to scan (default: jpg,jpeg,png,bmp)
