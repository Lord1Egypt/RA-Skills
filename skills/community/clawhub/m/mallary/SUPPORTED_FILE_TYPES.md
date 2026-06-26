# Supported File Types for Upload

Mallary CLI detects upload MIME types from file extensions and automatically uploads local files to Mallary's CDN before posting. The public upload path is built for image and video media. Audio, documents, and arbitrary binary files are not part of the normal public publishing flow.

## How It Works

The CLI infers the content type from the local filename:

```bash
mallary upload video.mp4
# Detected as: video/mp4

mallary upload image.png
# Detected as: image/png

mallary upload clip.webm
# Detected as: video/webm
```

## Supported File Types

### Images

| Extension       | MIME Type    | Supported |
| --------------- | ------------ | --------- |
| `.png`          | `image/png`  | Yes       |
| `.jpg`, `.jpeg` | `image/jpeg` | Yes       |
| `.webp`         | `image/webp` | Yes       |
| `.gif`          | `image/gif`  | Yes       |
| `.bmp`          | `image/bmp`  | Yes       |

Examples:

```bash
mallary upload photo.jpg
mallary upload logo.png
mallary upload animation.gif
mallary upload cover.webp
```

### Videos

| Extension       | MIME Type          | Supported |
| --------------- | ------------------ | --------- |
| `.mp4`          | `video/mp4`        | Yes       |
| `.mov`          | `video/quicktime`  | Yes       |
| `.webm`         | `video/webm`       | Yes       |
| `.mkv`          | `video/x-matroska` | Yes       |
| `.avi`          | `video/x-msvideo`  | Yes       |
| `.mpeg`, `.mpg` | `video/mpeg`       | Yes       |

Examples:

```bash
mallary upload video.mp4
mallary upload clip.mov
mallary upload recording.webm
mallary upload demo.mkv
```

### Audio

| Extension | MIME Type                  | Supported |
| --------- | -------------------------- | --------- |
| `.mp3`    | `application/octet-stream` | No        |
| `.wav`    | `application/octet-stream` | No        |
| `.ogg`    | `application/octet-stream` | No        |
| `.m4a`    | `application/octet-stream` | No        |

Notes:

- the public Mallary upload flow is designed for publishable social media image/video assets
- audio-only uploads are not part of the current public CLI workflow

### Documents

| Extension | MIME Type                  | Supported |
| --------- | -------------------------- | --------- |
| `.pdf`    | `application/octet-stream` | No        |
| `.doc`    | `application/octet-stream` | No        |
| `.docx`   | `application/octet-stream` | No        |

If you need a document-style asset, convert or export it into an image or video format that the destination platform supports.

### Other Files

For unknown extensions, the CLI falls back to:

- MIME type: `application/octet-stream`
- Result: usually not suitable for Mallary's public social publishing upload flow

## Usage Examples

### Upload an Image

```bash
mallary upload ./images/photo.jpg --json
```

Response:

```json
{
  "ok": true,
  "uploads": [
    {
      "source_path": "./images/photo.jpg",
      "filename": "photo.jpg",
      "media_url": "https://files.mallary.ai/uploads/photo.jpg",
      "storage_key": "uploads/photo.jpg",
      "content_type": "image/jpeg",
      "size": 12345
    }
  ]
}
```

### Upload a Video (MP4)

```bash
mallary upload ./videos/promo.mp4 --json
```

Response:

```json
{
  "ok": true,
  "uploads": [
    {
      "source_path": "./videos/promo.mp4",
      "filename": "promo.mp4",
      "media_url": "https://files.mallary.ai/uploads/promo.mp4",
      "storage_key": "uploads/promo.mp4",
      "content_type": "video/mp4",
      "size": 9876543
    }
  ]
}
```

### Upload and Use in Post

```bash
# 1. Upload the file
RESULT=$(mallary upload video.mp4 --json)

# 2. Extract the media URL
MEDIA_URL=$(echo "$RESULT" | jq -r '.uploads[0].media_url')

# 3. Use it in a post
mallary posts create \
  --message "Check out our latest demo." \
  --platform youtube \
  --profile-id AbC123xYz90 \
  --media "$MEDIA_URL"
```

Omit `--profile-id` to use the default Dashboard profile. Use `mallary profiles list` to find public profile IDs for non-default profiles.

### Upload Multiple Files

```bash
# Upload images
mallary upload image1.jpg image2.png image3.gif

# Upload videos
mallary upload video1.mp4 video2.mov
```

## Platform-Specific Notes

### TikTok

- video posts require exactly one video
- photo posts support up to 35 `jpg`, `jpeg`, or `webp` images
- `png` images are not accepted for TikTok photo posts

### YouTube

- requires exactly one video
- `post_type` can be `regular` or `shorts`
- custom thumbnails for regular videos can use `jpg`, `jpeg`, or `png` up to 2 MB; recommended `1280x720` 16:9
- YouTube Shorts thumbnails are skipped

### Instagram

- public publishing currently works best with one image or one video
- choose `feed`, `story`, `reel`, or `carousel` through `platform_options.instagram.post_type`
- video/Reels covers can be supplied with `media[].thumbnail_url`

### Facebook

- video thumbnails can use `jpg`, `jpeg`, or `png` up to 10 MB through `media[].thumbnail_url`

### Twitter/X

- supports up to 4 images, or 1 video, or 1 GIF

### LinkedIn

- current public path supports text-only posts or one image attachment

## Troubleshooting

### "Upload failed: Unsupported file type"

The file is probably not a supported image or video format for Mallary's public uploader.

Solution: convert it first.

```bash
# Convert a video to MP4
ffmpeg -i input.avi output.mp4

# Then upload
mallary upload output.mp4
```

### File Size Limits

Mallary's upload path accepts files up to 5 GB, but each social platform still enforces its own limits after upload.

### "MIME type mismatch"

Do not rename a file to a different extension just to force a MIME type.

```bash
# Wrong: PNG renamed to JPG
launch.jpg

# Correct: keep the real extension
launch.png
```

## Testing File Upload

```bash
# Set API key
export MALLARY_API_KEY="your_key"

# Test image upload
mallary upload test-image.jpg

# Test video upload
mallary upload test-video.mp4

# Unsupported example
mallary upload test-audio.mp3
```

## Error Messages

### File Not Found

Check the local path:

```bash
mallary upload ./missing-file.jpg
```

### No Permission

Make sure the file is readable by your current user.

### Invalid API Key

Set a valid Mallary API key:

```bash
export MALLARY_API_KEY="your_key"
mallary upload test-image.jpg
```

## Summary

- Mallary CLI supports image and video uploads for the public social publishing workflow.
- Uploaded media is hosted on `https://files.mallary.ai/...`.
- Audio, documents, and unknown binary types are not normal public upload targets.
- Always check platform media rules before sending the same asset to multiple destinations.
