# Media Specifications by Platform

## Supported Upload Content Types

| Content Type | Extension | Use For |
|---|---|---|
| `image/png` | .png | Images |
| `image/jpeg` | .jpeg/.jpg | Images |
| `image/gif` | .gif | Animated images |
| `image/webp` | .webp | Images |
| `video/mp4` | .mp4 | Video |
| `video/quicktime` | .mov | Video |
| `application/pdf` | .pdf | LinkedIn documents |
| `application/vnd.openxmlformats-officedocument.wordprocessingml.document` | .docx | LinkedIn documents |
| `application/vnd.openxmlformats-officedocument.presentationml.presentation` | .pptx | LinkedIn documents |

## Per-Platform Specs

### TikTok
- **Video**: MP4/MOV, H.264, ≤250MB, 3s-10min, best 15-30s
- **Dimensions**: 1080×1920 (9:16) recommended
- **Carousels**: 2-35 images (photo slideshows)
- **Caption**: max 2,200 characters
- **No standalone images** — images only in carousels
- **Cover**: `coverTimestamp` only (milliseconds). No custom cover image upload

### Instagram
- **Images**: JPEG/PNG, recommended 1080×1080 (1:1) or 1080×1350 (4:5)
- **Reels**: Video 3-90s, ≤1GB, 9:16 recommended
- **Stories**: Image or video, 9:16
- **Carousels**: Up to 10 images or videos
- **Caption**: max 2,200 characters
- **Reel cover**: `coverImageKey` (JPEG only, max 8MB) or `coverTimestamp` (milliseconds, fallback)

### Facebook
- **Images**: JPG/PNG, ≤30MB each, up to 10 per post
- **Video**: 1 per post
- **Reels**: Vertical video
- **Cannot mix** images and videos in same post
- **Caption**: max 63,206 characters
- **Reel cover**: `coverImageKey` (any format, max 10MB). `coverTimestamp` NOT supported

### YouTube
- **Shorts**: ≤3min, 9:16 or 1:1
- **Videos**: No duration limit
- **Codec**: H.264 video, AAC audio recommended
- **Copyrighted music**: limits Shorts to 60s
- **Title**: max 100 characters

### LinkedIn
- **Images**: Up to 9 per post
- **Video**: Up to 10 minutes
- **Documents**: PDF/PPTX/DOCX, ≤60MB (display as swipeable carousels)
- **Cannot mix** documents with regular media
- **Caption**: max 3,000 characters

### X (Twitter)
- **Images**: Up to 4 per post
- **No video** via PostFast API
- **Caption**: max 280 characters

### Pinterest
- **Images**: 2:3 ratio ideal (1000×1500)
- **Video**: Supported
- **Carousels**: 2-5 static images (no video in carousels)
- **Title**: max 100 characters (first line of content)
- **Description**: max 800 characters
- **Video cover**: `coverImageKey` (JPEG/PNG) or `coverTimestamp` (milliseconds, fallback)

### Bluesky
- **Images**: Up to 4
- **No video** via API
- **Caption**: max 300 characters

### Threads
- **Images**: Supported
- **Video**: Supported
- **Carousels**: Up to 10 images
- **Caption**: max 500 characters

### Google Business Profile
- **Images**: JPEG/PNG, 1 per post, max 5MB
- **No video** support
- **No carousels**
- **Caption**: max 1,500 characters
- Standard posts expire after 6 months; Event/Offer posts expire at end date

### Telegram
- **Images**: Up to 10
- **Video**: Supported
- **Mixed media**: Up to 10 items (images + videos together)
- **Caption**: max 4,096 characters
