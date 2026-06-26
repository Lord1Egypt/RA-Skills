# Memories.ai Advanced API Reference

## VLM/ILM Chat (Video/Image Understanding)

Use AI models to chat with videos and images.

### Gemini VLM (Video)
```bash
POST /gemini/vlm/chat
{
  "video_url": "https://...",
  "messages": [{"role": "user", "content": "What happens in this video?"}]
}
```

### Gemini ILM (Image)
```bash
POST /gemini/ilm/chat
{
  "image_url": "https://...",
  "messages": [{"role": "user", "content": "Describe this image"}]
}
```

### Other Models
- `/nova/vlm/chat` - Amazon Nova VLM
- `/nova/ilm/chat` - Amazon Nova ILM
- `/qwen/vlm/chat` - Qwen VLM
- `/qwen/ilm/chat` - Qwen ILM
- `/gpt/ilm/chat` - GPT-4V

## Video Processing

### Extract Frames
```bash
POST /video/extract-frames
{
  "video_url": "https://...",
  "interval_seconds": 5
}
```

### Clip Video
```bash
POST /video/clip
{
  "video_url": "https://...",
  "start_time": 10,
  "end_time": 30
}
```

### Split Video
```bash
POST /video/split
{
  "video_url": "https://...",
  "segments": [
    {"start": 0, "end": 30},
    {"start": 30, "end": 60}
  ]
}
```

### Edit Video (AI-powered)
```bash
POST /video/edit
{
  "video_url": "https://...",
  "instructions": "Add subtitles and trim the first 5 seconds"
}
```

## Embeddings

### Text Embedding
```bash
POST /embeddings/text
{"text": "Your text here"}
```

### Image Embedding
```bash
POST /embeddings/image
{"image_url": "https://..."}
```

### Video Embedding
```bash
POST /embeddings/video
{"video_url": "https://..."}
```

## Stream Processing

### Start Audio Stream Transcription
```bash
POST /stream/audio/start
{
  "stream_url": "rtmp://...",
  "callback_url": "https://your-webhook.com/callback"
}
```

### Start Video Stream Moderation
```bash
POST /stream/video/start
{
  "stream_url": "rtmp://...",
  "callback_url": "https://your-webhook.com/callback",
  "detect_logo": true
}
```

## Upload & Storage

### Upload from URL
```bash
POST /upload
{
  "url": "https://direct-video-url.mp4",
  "name": "my_video"
}
```

### Get Signed Upload URL
```bash
POST /upload/signed-url
{"filename": "video.mp4", "content_type": "video/mp4"}
```

## Human Re-identification (ReID)

Track people across videos using reference images.

```bash
POST /human/reid
{
  "video_url": "https://...",
  "reference_images": ["https://face1.jpg", "https://face2.jpg"]
}
```

## Full API Documentation

- Index: https://api-tools.memories.ai/llms.txt
- OpenAPI Spec: https://api-tools.memories.ai/api-reference/openapi.json
- Console: https://api-platform.memories.ai
