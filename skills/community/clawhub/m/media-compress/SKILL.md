---
name: media-compress
description: Compress and convert images and videos using ffmpeg. Use when the user wants to reduce file size, change format, resize, or optimize media files. Handles common formats like JPG, PNG, WebP, MP4, MOV, WebM. Triggers on phrases like "compress image", "compress video", "reduce file size", "convert to webp/mp4", "resize image", "make image smaller", "batch compress", "optimize media".
---

# Media Compression Skill

Compress and convert images and videos with intelligent defaults. Supports single files and batch processing.

## Supported Formats

**Images:** JPG, PNG, WebP, BMP, TIFF, GIF → JPG, PNG, WebP
**Videos:** MP4, MOV, AVI, MKV, WebM, FLV, WMV, M4V → MP4

## Prerequisites

**ffmpeg must be installed:**
- Ubuntu/Debian: `sudo apt update && sudo apt install ffmpeg`
- macOS: `brew install ffmpeg`
- Windows: Download from https://ffmpeg.org/download.html and add to PATH

Verify installation: `ffmpeg -version`

## Quick Start

### Image Compression

```bash
# Compress to target size (auto-adjusts quality)
python scripts/compress_image.py photo.jpg --max-size 200kb

# Resize + compress
python scripts/compress_image.py photo.png --width 800 --output photo_small.jpg

# Convert to WebP (better compression)
python scripts/compress_image.py photo.jpg --format webp

# Batch compress entire folder
python scripts/compress_image.py ./photos --output ./compressed --quality 80

# Preview mode - see what will happen without compressing
python scripts/compress_image.py photo.jpg --max-size 500kb --preview

# Keep backup of original file
python scripts/compress_image.py photo.jpg --max-size 500kb --backup
```

### Video Compression

```bash
# Compress with default settings (good balance)
python scripts/compress_video.py video.mp4 --output video_small.mp4

# Resize to 720p
python scripts/compress_video.py video.mp4 --height 720

# Target specific file size (approximate)
python scripts/compress_video.py video.mp4 --target-size 50mb

# Lower quality for smaller file
python scripts/compress_video.py video.mp4 --crf 28

# Batch process all videos in folder
python scripts/compress_video.py ./videos --output ./compressed --height 480

# Preview mode - see what will happen without compressing
python scripts/compress_video.py video.mp4 --height 720 --preview

# Keep backup of original file
python scripts/compress_video.py video.mp4 --height 720 --backup
```

## Common Use Cases

### 1. Upload to Website (Image)
Most websites need images under 500KB:
```bash
python scripts/compress_image.py photo.jpg --max-size 500kb --format webp
```

### 2. Email Attachment (Image)
Email often has 25MB limit:
```bash
python scripts/compress_image.py scan.pdf.jpg --max-size 5mb --quality 90
```

### 3. Social Media Video
Platforms prefer 720p, smaller files:
```bash
python scripts/compress_video.py clip.mov --height 720 --crf 23 --preset fast
```

### 4. Archive Old Videos
Maximum compression for storage:
```bash
python scripts/compress_video.py old_video.avi --crf 28 --preset slow --height 480
```

### 5. Convert Format Only
Keep quality, just change format:
```bash
# Image
python scripts/compress_image.py image.png --format jpg --quality 95

# Video
python scripts/compress_video.py video.mov --output video.mp4 --crf 18
```

## Parameters Reference

### Image (`compress_image.py`)

| Parameter | Description | Default |
|-----------|-------------|---------|
| `input` | Input file or directory (required) | - |
| `--output, -o` | Output file or directory | Auto-generated |
| `--max-size` | Target max file size (e.g., 500kb, 2mb) | None |
| `--quality, -q` | JPEG/WebP quality (1-100) | 85 |
| `--width, -w` | Max width in pixels | Original |
| `--height` | Max height in pixels | Original |
| `--format, -f` | Output format: jpg, png, webp | Original format |
| `--no-strip` | Keep metadata (default: remove) | False |
| `--preview, -p` | Preview mode: show settings without compressing | False |
| `--backup, -b` | Keep backup of original file | False |

### Video (`compress_video.py`)

| Parameter | Description | Default |
|-----------|-------------|---------|
| `input` | Input file or directory (required) | - |
| `--output, -o` | Output file or directory | Auto-generated |
| `--crf` | Quality 0-51 (lower=better). 18=visually lossless, 23=default, 28=smaller | 23 |
| `--preset` | Encoding speed: ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow | medium |
| `--height` | Max height (480, 720, 1080) | Original |
| `--target-size` | Approximate target size (e.g., 50mb, 1gb) | None |
| `--fps` | Limit frame rate (e.g., 30, 24) | Original |
| `--audio-bitrate` | Audio quality (e.g., 128k, 192k) | 128k |
| `--preview, -p` | Preview mode: show settings without compressing | False |
| `--backup, -b` | Keep backup of original file | False |

## Quality Guidelines

### Images
- **90-95**: High quality, minimal compression artifacts
- **85**: Sweet spot (default) - good quality, significant size reduction
- **70-80**: Acceptable for web, smaller files
- **50-60**: Low quality, visible artifacts

### Videos (CRF)
- **17-18**: Visually lossless, archival quality
- **20-22**: High quality, professional use
- **23**: Default, good balance (recommended)
- **28**: Smaller files, acceptable quality
- **35+**: Low quality, preview/draft only

### Presets
- **ultrafast**: Fastest encoding, largest files
- **fast**: Quick results, slightly larger
- **medium**: Default balance
- **slow**: Better compression, smaller files
- **veryslow**: Maximum compression, smallest files

## Batch Processing

When input is a directory:
- All supported files are processed
- Output directory structure mirrors input
- Progress shown for each file
- Original and compressed sizes displayed

Example:
```bash
$ python scripts/compress_image.py ./vacation_photos --output ./compressed --max-size 500kb
找到 24 个图像文件
[1/24] 处理: IMG_001.jpg
  ✓ 2847.3KB → 456.2KB (84.0% 减少)
[2/24] 处理: IMG_002.png
  ✓ 1532.1KB → 298.5KB (80.5% 减少)
...
```

## Troubleshooting

### "ffmpeg not found"
Install ffmpeg first:
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# macOS
brew install ffmpeg
```

### "Permission denied"
Make scripts executable:
```bash
chmod +x scripts/*.py
```

### Quality too low
Increase quality setting:
```bash
# Image
python scripts/compress_image.py photo.jpg --quality 90

# Video
python scripts/compress_video.py video.mp4 --crf 20
```

### File not smaller
- Try lower quality or smaller dimensions
- Some files are already optimally compressed
- Use `--max-size` to force target size

### Batch processing stops
Check that all files in directory are valid images/videos. Corrupt files may cause errors.

## Advanced Tips

1. **Strip metadata** for privacy (default behavior)
2. **Use WebP** for best web compression
3. **720p height** is usually enough for mobile viewing
4. **CRF 23 + preset slow** gives great results for archiving
5. **Test with one file** before batch processing

## References

- [FFmpeg Guide](references/ffmpeg_guide.md) - Detailed ffmpeg commands and parameters
