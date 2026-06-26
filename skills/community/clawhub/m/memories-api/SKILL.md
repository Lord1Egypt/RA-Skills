---
name: memories-api
description: Memories.ai V2 API for video intelligence - transcripts, embeddings, AI analysis, and video operations. Use when working with video transcription, video embeddings, AI video/image analysis (VLM/ILM with Gemini/Nova/Qwen/GPT), or video editing operations. Supports YouTube, TikTok, Instagram, and Twitter videos.
metadata:
  openclaw:
    emoji: "🎬"
    requires:
      env: ["MEMORIES_API_KEY"]
---

# Memories.ai V2 API Skill

Video intelligence API for transcripts, embeddings, AI analysis (VLM/ILM), and video operations.

## Setup

```bash
# Set your API key
export MEMORIES_API_KEY="sk-mavi-your-key-here"

# Set your webhook URL for async callbacks (optional)
export MEMORIES_WEBHOOK_URL="https://your-server.com/webhook"
```

## Quick Start

```python
from memories_sdk import MemoriesAI, Platform, ModelProvider

# Initialize client (uses MEMORIES_API_KEY and MEMORIES_WEBHOOK_URL env vars)
client = MemoriesAI()

# Or pass credentials directly
client = MemoriesAI(
    api_key="sk-mavi-...",
    webhook_url="https://your-server.com/webhook"  # for async callbacks
)
```

## API Endpoints

### 1. Social Video Transcripts (Sync)

Get transcripts from YouTube, TikTok, Instagram, Twitter:

```python
# Auto-detect platform
result = client.process_social_video("https://youtube.com/watch?v=abc123")

# Or specify platform
result = client.get_transcript(Platform.TIKTOK, "https://tiktok.com/@user/video/123")
```

### 2. MAI Transcripts (Async with Webhook)

Deep video analysis with visual + audio transcription:

```python
# Submit async task
task_id = client.submit_mai_transcript(
    Platform.YOUTUBE,
    "https://youtube.com/watch?v=abc123",
    callback_url="https://your-webhook.com/callback"  # optional
)

# Wait for result (polling)
status = client.wait_for_task(task_id, poll_interval=5, timeout=600)
print(status.data)

# Or use the workflow helper
result = client.process_video_mai_flow("https://youtube.com/watch?v=abc123", Platform.YOUTUBE)
```

### 3. Embeddings

```python
# Text embedding
embedding = client.get_text_embedding("Your text here")

# Image embedding
embedding = client.get_image_embedding("https://example.com/image.jpg")

# Video embedding
embedding = client.get_video_embedding("https://example.com/video.mp4")
```

### 4. AI Vision/Image Language Models

Supported providers: `gemini`, `nova`, `qwen`, `gpt`

```python
# Video analysis (VLM)
response = client.ai_vlm(
    ModelProvider.GEMINI,
    video_url="https://example.com/video.mp4",
    prompt="Describe what happens in this video"
)

# Image analysis (ILM)
response = client.ai_ilm(
    ModelProvider.GPT,
    image_url="https://example.com/image.jpg",
    prompt="What objects are in this image?"
)
```

### 5. Video Operations

```python
# Clip video
result = client.clip_video(video_url, start=10.0, end=30.0)

# Split video into segments
result = client.split_video(video_url, segments=[
    {"start": 0, "end": 10},
    {"start": 20, "end": 40}
])

# Extract frames at timestamps
result = client.extract_frames(video_url, timestamps=[1.0, 5.0, 10.0])

# Get video metadata
metadata = client.get_video_metadata(video_url)

# Upload local video
asset_url = client.upload_video("/path/to/video.mp4")

# Download video
client.download_video(video_url, "/path/to/save.mp4")

# Delete asset
client.delete_asset(asset_id)
```

### 6. Task Status

```python
# Check task status
status = client.get_task_status(task_id)
print(status.status)  # pending, processing, completed, failed
print(status.is_finished)
print(status.data)

# Wait for completion with timeout
status = client.wait_for_task(task_id, poll_interval=5, timeout=600)
```

## Webhook Handling

For async endpoints, results are delivered via webhook. Set up your own webhook server:

```python
from memories_sdk import WebhookCallbackHandler

# In your FastAPI/Flask endpoint:
def webhook_handler(request_body):
    data = WebhookCallbackHandler.parse_callback(request_body)
    result = WebhookCallbackHandler.handle_status(data)
    return result
```

**Note:** You must provide your own webhook URL via `MEMORIES_WEBHOOK_URL` env var or `webhook_url` parameter.

## Error Handling

```python
from memories_sdk import MemoriesError, APIError, AuthenticationError, TaskError

try:
    result = client.get_transcript(Platform.YOUTUBE, url)
except AuthenticationError as e:
    print(f"Auth failed: {e}")
except APIError as e:
    print(f"API error {e.status_code}: {e.response}")
except TaskError as e:
    print(f"Task failed: {e}")
except MemoriesError as e:
    print(f"General error: {e}")
```

## API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/{platform}/video/transcript` | POST | Sync transcript |
| `/{platform}/video/mai/transcript` | POST | Async MAI transcript |
| `/async/generate/video/transcript` | POST | Async video transcript |
| `/async/generate/audio/transcript` | POST | Async audio transcript |
| `/async/generate/speaker/transcript` | POST | Speaker diarization |
| `/embeddings/text` | POST | Text embedding |
| `/embeddings/image` | POST | Image embedding |
| `/embeddings/video` | POST | Video embedding |
| `/{provider}/vlm` | POST | Video language model |
| `/{provider}/ilm` | POST | Image language model |
| `/video-clip` | POST | Extract video clip |
| `/video-split` | POST | Split video |
| `/video-edit` | POST | Edit video |
| `/extract-frames` | POST | Extract frames |
| `/upload` | POST | Upload file |
| `/download` | POST | Download file |
| `/delete` | POST | Delete asset |
| `/get-metadata` | POST | Get video metadata |
| `/get-task-status/{task_id}` | GET | Check task status |

## Pricing (Approximate)

- **MAI Transcript**: ~$0.10 per 40s video
- **Simple Transcript**: ~$0.02 per video
- **Embeddings**: Token-based pricing
- **VLM/ILM**: Per-request + token pricing

## Links

- **API Docs**: https://api-tools.memories.ai/llms.txt
- **OpenAPI Spec**: https://api-tools.memories.ai/api-reference/openapi.json
