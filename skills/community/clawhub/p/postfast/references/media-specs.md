# Media Specifications by Platform

## Supported Upload Content Types

| Content Type | Extension | Use For |
|---|---|---|
| `image/png` | .png | Images |
| `image/jpeg` | .jpeg/.jpg | Images (send `image/jpeg` for .jpg files: `image/jpg` is rejected) |
| `image/gif` | .gif | Animated images |
| `image/webp` | .webp | Images |
| `video/mp4` | .mp4 | Video |
| `video/quicktime` or `video/mov` | .mov | Video |
| `video/webm` | .webm | Video |
| `application/pdf` | .pdf | LinkedIn documents |
| `application/msword` | .doc | LinkedIn documents |
| `application/vnd.openxmlformats-officedocument.wordprocessingml.document` | .docx | LinkedIn documents |
| `application/vnd.ms-powerpoint` | .ppt | LinkedIn documents |
| `application/vnd.openxmlformats-officedocument.presentationml.presentation` | .pptx | LinkedIn documents |
| `application/x-subrip` | .srt | YouTube captions (`youtubeCaptionKey`) |
| `text/vtt` | .vtt | YouTube captions (`youtubeCaptionKey`) |

Any other content type returns `400` from `POST /file/get-signed-upload-urls`.

**Upload caps (all platforms):** 250MB per video (Bluesky 100MB, Telegram 50MB), 10MB per image, 60MB per document, 10MB per caption file (SRT/VTT).

## Per-Platform Specs

### TikTok
- **Video**: MP4/MOV, H.264, ≤250MB, 3s-10min, best 15-30s
- **Dimensions**: 1080×1920 (9:16) recommended
- **Carousels**: up to 10 images per photo post (TikTok itself allows 35; PostFast takes 10)
- **Caption**: max 2,200 characters
- **No standalone images**: images only in carousels
- **Cover**: `coverTimestamp` only (milliseconds). No custom cover image upload

### Instagram
- **Images**: JPEG/PNG, recommended 1080×1080 (1:1) or 1080×1350 (4:5)
- **Reels**: Video 3-90s, 9:16 recommended
- **Stories**: Image or video, 9:16
- **Carousels**: Up to 10 images and videos, mixed (Timeline only)
- **Caption**: max 2,200 characters
- **Reel cover**: `coverImageKey` (JPEG only, max 8MB) or `coverTimestamp` (milliseconds, fallback)

### Facebook
- **Images**: JPG/PNG, up to 10 per post
- **Video**: 1 per post
- **Reels**: Vertical video
- **Cannot mix** images and videos in same post
- **Caption**: max 63,206 characters
- **Reel cover**: `coverImageKey` (any format, max 10MB). `coverTimestamp` NOT supported

### YouTube
- **Video only**: 1 per post, no images
- **Shorts**: under 3min, 9:16 or 1:1
- **Videos**: No duration limit
- **Codec**: H.264 video, AAC audio recommended
- **Copyrighted music**: limits Shorts to 60s
- **Title**: max 100 characters
- **Description**: max 5,000 characters; no `<` or `>` in the title or description
- **Thumbnail**: JPEG/PNG/GIF, max 2MB, 1280×720 recommended (`youtubeThumbnailKey`)
- **Captions**: timed SRT or WebVTT in plain UTF-8, max 10MB, one track per video, in the language set by `youtubeLanguage` (`youtubeCaptionKey`)

### LinkedIn
- **Images**: Up to 10 per post
- **Video**: 1 per post (no mixing with images)
- **Documents**: PDF/DOC/DOCX/PPT/PPTX, ≤60MB (display as swipeable carousels)
- **Cannot mix** documents with regular media
- **Caption**: max 3,000 characters

### X (Twitter)
- **Images**: Up to 4 per post
- **Video**: 1 per post (no mixing with images)
- **Caption**: max 280 characters (4,000 with X Premium)

### Pinterest
- **Images**: 1 image, 2:3 ratio ideal (1000×1500)
- **Video**: 1 per Pin
- **Carousels**: 2-5 static images (no GIFs, no video in carousels)
- **Title**: max 100 characters (first line of content)
- **Description**: max 800 characters
- **Video cover**: `coverImageKey` (JPEG/PNG, up to 8MB) or `coverTimestamp` (milliseconds, fallback)

### Bluesky
- **Images**: Up to 10, JPEG/PNG/GIF/WebP, 2MB each (5-10 images show as a gallery)
- **Video**: 1 MP4, up to 100MB (not combined with images); Bluesky-hosted accounts need a verified email first
- **Caption**: max 300 characters

### Threads
- **Images**: Supported
- **Video**: Supported
- **Carousels**: Up to 10 images and videos, mixed
- **Caption**: max 500 characters

### Google Business Profile
- **Images**: JPEG/PNG, 1 per post, max 5MB
- **No video** support
- **No carousels**
- **Caption**: max 1,500 characters
- Standard posts expire after 6 months; Event/Offer posts expire at end date

### Telegram
- **Images**: Up to 10
- **Video**: Supported, up to 50MB
- **Mixed media**: Up to 10 items (images + videos together)
- **Caption**: max 4,096 characters
