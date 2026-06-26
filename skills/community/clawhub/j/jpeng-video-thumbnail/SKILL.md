---
name: jpeng-video-thumbnail
description: "Generate thumbnails from videos"
version: "1.0.0"
author: "jpeng"
tags: ["processing", "thumbnail", "video"]
---

# Video Thumbnail

Generate thumbnails from videos

## When to Use

- User needs processing related functionality
- Automating thumbnail tasks
- Video operations

## Usage

```bash
python3 scripts/video_thumbnail.py --input <input> --output <output>
```

## Configuration

Set required environment variables:

```bash
export THUMBNAIL_API_KEY="your-api-key"
```

## Output

Returns JSON with results:

```json
{
  "success": true,
  "data": {}
}
```
