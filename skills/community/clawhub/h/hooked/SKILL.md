---
name: hooked-video-api
description: Create AI-powered videos via the Hooked Video API. Script-to-video, prompt-to-video, UGC ads, TikTok slideshows, avatar selection, voice cloning, and trend discovery. Use when the user wants to create videos, browse avatars/voices, check video status, or discover trending content.
---

# Hooked Video API

Create professional AI videos programmatically. Works with TikTok, Instagram, YouTube, and more.

## Authentication

All requests require an `x-api-key` header with your Hooked API key.

```bash
# Get your API key at https://hooked.so/settings/api
export HOOKED_API_KEY="your_api_key_here"
```

## Base URL

```
https://api.hooked.so
```

## Core Endpoints

### Create Script-to-Video

Create a video from a script with an AI avatar that lip-syncs.

```bash
POST /v1/project/create/script-to-video

{
  "script": "Hey everyone! Today I'm going to show you...",
  "avatarId": "avatar_sophia_casual",
  "voiceId": "voice_en_sarah",         # optional
  "musicId": "music_upbeat_01",         # optional
  "captionStyle": "karaoke",            # optional: karaoke, word-by-word, none
  "webhook": "https://your.webhook/url" # optional
}

# Response
{
  "videoId": "vid_abc123",
  "status": "processing",
  "estimatedSeconds": 45
}
```

### Create Prompt-to-Video

Let AI generate the script, visuals, and narration from a simple prompt.

```bash
POST /v1/project/create/prompt-to-video

{
  "prompt": "Create a 30-second product video for a fitness app targeting young professionals",
  "avatarId": "avatar_marcus_professional", # optional, AI picks if not specified
  "voiceId": "voice_en_james",              # optional
  "webhook": "https://your.webhook/url"     # optional
}
```

### Create TikTok Slideshow

Create viral TikTok-style slideshow content.

```bash
POST /v1/project/create/tiktok-slideshow

{
  "title": "5 Productivity Tips for Remote Workers",
  "slides": [
    { "text": "Tip 1: Start your day with deep work", "imageUrl": "https://..." },
    { "text": "Tip 2: Batch your meetings", "imageUrl": "https://..." },
    { "text": "Tip 3: Take walking breaks", "imageUrl": "https://..." }
  ],
  "voiceId": "voice_en_sarah", # optional
  "musicId": "music_chill_01", # optional
  "webhook": "https://..."     # optional
}
```

### Create UGC Ad

Create authentic UGC-style product ads.

```bash
POST /v1/project/create/ugc-ads

{
  "script": "Okay so I've been using this app for 2 weeks and...",
  "avatarId": "avatar_emma_casual",
  "productUrl": "https://mystore.com/product", # optional, extracts visuals
  "hook": "Stop scrolling! You need to see this", # optional
  "cta": "Link in bio",                          # optional
  "webhook": "https://..."                        # optional
}
```

## Resource Endpoints

### List Avatars

Browse available AI avatars.

```bash
GET /v1/avatar/list

# Response
{
  "avatars": [
    {
      "id": "avatar_sophia_casual",
      "name": "Sophia",
      "gender": "female",
      "style": "casual",
      "previewUrl": "https://...",
      "tags": ["young", "energetic", "lifestyle"]
    },
    ...
  ]
}
```

### List Voices

Browse available AI voices.

```bash
GET /v1/voice/list

# Response
{
  "voices": [
    {
      "id": "voice_en_sarah",
      "name": "Sarah",
      "language": "en",
      "accent": "american",
      "style": "conversational",
      "previewUrl": "https://..."
    },
    ...
  ]
}
```

### List Music

Browse background music tracks.

```bash
GET /v1/music/list

# Response
{
  "tracks": [
    {
      "id": "music_upbeat_01",
      "name": "Upbeat Energy",
      "mood": "energetic",
      "duration": 60,
      "previewUrl": "https://..."
    },
    ...
  ]
}
```

## Video Management

### Get Video Status

Check video rendering progress and get download URL.

```bash
GET /v1/video/{videoId}

# Response
{
  "videoId": "vid_abc123",
  "status": "completed", # processing, completed, failed
  "progress": 100,
  "downloadUrl": "https://...",
  "duration": 32,
  "createdAt": "2024-01-15T10:30:00Z"
}
```

### List Videos

List recent videos created by your team.

```bash
GET /v1/video/list?limit=20

# Response
{
  "videos": [
    {
      "videoId": "vid_abc123",
      "status": "completed",
      "title": "Product Demo",
      "duration": 32,
      "createdAt": "2024-01-15T10:30:00Z"
    },
    ...
  ]
}
```

## Trend Discovery

### Get Trending Videos

Discover what's trending for content inspiration.

```bash
GET /v1/trends/videos?platform=tiktok&niche=fitness

# Response
{
  "trends": [
    {
      "title": "30-day ab challenge",
      "platform": "tiktok",
      "views": 2300000,
      "engagement": "high",
      "hook": "Day 1 vs Day 30 results...",
      "tags": ["fitness", "transformation", "challenge"]
    },
    ...
  ]
}
```

Query parameters:
- `platform`: tiktok, youtube, instagram (optional)
- `niche`: fitness, tech, beauty, food, etc. (optional)

## Webhooks

All creation endpoints accept a `webhook` URL. When the video is ready, we'll POST:

```json
{
  "event": "video.completed",
  "videoId": "vid_abc123",
  "status": "completed",
  "downloadUrl": "https://...",
  "duration": 32
}
```

## Error Handling

```json
{
  "error": {
    "code": "INVALID_AVATAR",
    "message": "Avatar 'avatar_xyz' not found. Use GET /v1/avatar/list to see available avatars."
  }
}
```

Common error codes:
- `INVALID_API_KEY`: Check your x-api-key header
- `INVALID_AVATAR`: Avatar ID not found
- `INVALID_VOICE`: Voice ID not found
- `SCRIPT_TOO_LONG`: Script exceeds maximum length (5000 chars)
- `RATE_LIMITED`: Too many requests, wait and retry

## Pricing

- **Pro**: $39/month — 150 credits (~30 videos)
- **Premium**: $79/month — 350 credits (~70 videos)
- **Ultra**: $149/month — 750 credits (~150 videos)

The skill itself is free and open source. You only pay for video generation.

## Rate Limits

- 60 requests per minute

## Example: Full Workflow

```bash
# 1. List avatars to find a good fit
curl -X GET "https://api.hooked.so/v1/avatar/list" \
  -H "x-api-key: $HOOKED_API_KEY"

# 2. Create a video
curl -X POST "https://api.hooked.so/v1/project/create/script-to-video" \
  -H "x-api-key: $HOOKED_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "script": "Hey! In this video I am going to show you 3 productivity hacks...",
    "avatarId": "avatar_sophia_casual",
    "captionStyle": "karaoke"
  }'

# 3. Check status (poll until completed)
curl -X GET "https://api.hooked.so/v1/video/vid_abc123" \
  -H "x-api-key: $HOOKED_API_KEY"

# 4. Download when ready
# Use the downloadUrl from the response
```

## Tips for Agents

1. **Always list avatars first** if the user doesn't specify one
2. **Use prompt-to-video** for vague requests — it handles script generation
3. **Check video status** and notify the user when rendering completes
4. **Suggest trending content** when the user needs ideas
5. **Use webhooks** for autonomous workflows instead of polling

## Links

- API Docs: https://docs.hooked.so
- Dashboard: https://hooked.so
- Support: support@hooked.so
