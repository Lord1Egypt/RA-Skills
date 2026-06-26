# Media Compress

A lightweight skill for compressing and converting images and videos using ffmpeg.

## Features

- 🖼️ **Image compression**: JPG, PNG, WebP with quality control
- 🎬 **Video compression**: MP4, MOV, AVI and more with CRF-based quality
- 📦 **Batch processing**: Compress entire folders at once
- 🎯 **Smart defaults**: Quality 85 for images, CRF 23 for videos
- 📏 **Size targeting**: Specify exact file size limits
- 🔄 **Format conversion**: Convert between formats while compressing

## Requirements

- Python 3.6+
- ffmpeg (automatically checked)

## Installation

1. Install ffmpeg:
   ```bash
   # Ubuntu/Debian
   sudo apt install ffmpeg
   
   # macOS
   brew install ffmpeg
   ```

2. Install the skill via OpenClaw

## Quick Examples

```bash
# Compress image to 200KB
python scripts/compress_image.py photo.jpg --max-size 200kb

# Resize video to 720p
python scripts/compress_video.py video.mp4 --height 720

# Batch compress folder
python scripts/compress_image.py ./photos --output ./compressed
```

## License

MIT
