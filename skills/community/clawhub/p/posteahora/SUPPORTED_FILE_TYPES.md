# Supported File Types

The PosteAhora CLI uploads media via `posteahora upload <file>`, which returns a
public URL you attach to a post with `--media`.

## Images

| Format | Extension | Content type |
|--------|-----------|--------------|
| JPEG | `.jpg`, `.jpeg` | `image/jpeg` |
| PNG | `.png` | `image/png` |
| WebP | `.webp` | `image/webp` |
| GIF | `.gif` | `image/gif` |

## Video

| Format | Extension | Content type |
|--------|-----------|--------------|
| MP4 | `.mp4` | `video/mp4` |
| QuickTime | `.mov` | `video/quicktime` |
| WebM | `.webm` | `video/webm` |
| M4V | `.m4v` | `video/x-m4v` |

The content type is detected from the file extension. Unknown extensions upload
as `application/octet-stream`.

## Usage

```bash
# Image
posteahora upload ./photo.jpg
posteahora post "Photo post" --to instagram:a1b2 --media https://cdn.posteahora.com/…

# Video
posteahora upload ./reel.mp4
posteahora post "Reel" --to instagram:a1b2 --post-type reel --media https://cdn.posteahora.com/…

# Carousel (multiple images)
posteahora post "Carousel" --to instagram:a1b2 \
  --media https://cdn.posteahora.com/1.jpg \
  --media https://cdn.posteahora.com/2.jpg
```

## Notes

- Uploads use presigned URLs and work for large video files.
- Per-network limits (dimensions, duration, size, aspect ratio) are enforced by
  each platform — check the target network's requirements for reels, stories, and
  video.
- TikTok photo posts must be served from the verified `cdn.posteahora.com`
  domain, which `posteahora upload` handles automatically.
