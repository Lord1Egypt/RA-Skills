---
name: novita-multimodal
description: |
  Execute multimodal tasks using Novita AI: text-to-image, image-to-image, text-to-video, image-to-video, TTS, STT.
  Use for: generating images, generating videos, text-to-speech, speech recognition.
---

# Novita AI Multimodal Execution

## Configuration (choose one, by priority)

### Method 1: Config File (Recommended)

Create file `~/.novita/config.json`:

```json
{
  "api_key": "YOUR_API_KEY"
}
```

**One command setup:**
```bash
mkdir -p ~/.novita && echo '{"api_key": "YOUR_API_KEY"}' > ~/.novita/config.json
```

### Method 2: Environment Variable

```bash
export NOVITA_API_KEY="YOUR_API_KEY"
```

### Method 3: Direct Parameter

Include in request: `Please use API Key sk_xxx to generate an image...`

---

## API Key Reading Logic

```
1. Check if user message contains API Key (starts with sk_)
2. Check config file ~/.novita/config.json
3. Check environment variable NOVITA_API_KEY
4. None found → Return configuration guide
```

**Configuration guide (only shown when not configured):**

```
You have not configured your Novita AI API Key.

Quick setup (copy and run):
mkdir -p ~/.novita && echo '{"api_key": "YOUR_KEY"}' > ~/.novita/config.json

Get Key: https://novita.ai/settings/key-management
```

---

## Execution Flow (Important!)

```
User request → Identify task → Get Key → ⚠️ Send prompt first → Execute task → Return result
```

### ⚠️ Must Send Progress Prompt First

**Before calling the API, you must reply to the user with a message:**

```
🎨 Got it! Generating your image...

Task type: Text-to-Image
Model: Seedream 5.0 Lite
Estimated time: 5-15 seconds
Estimated cost: ~$0.035

Please wait, will send as soon as it's ready ⏳
```

**This message must be sent BEFORE executing the API call!** This way users know the task is being processed and won't think the system is stuck.

### Progress Templates for Different Tasks

**Text-to-Image:**
```
🎨 Got it! Generating your image...
Model: Seedream 5.0 Lite
Estimated time: 5-15 seconds
```

**Text-to-Video:**
```
🎬 Got it! Generating your video...
Model: Vidu Q3 Pro
Estimated time: 1-3 minutes (video generation is slower, please be patient)
```

**TTS:**
```
🔊 Got it! Generating your audio...
Model: MiniMax Speech 2.8 Turbo
Estimated time: 5-15 seconds
```

### Completion Response

```
✅ Generation complete!

[Image/Video/Audio URL]

Actual cost: $0.035
```

### Video Task Polling Updates

Video generation requires polling, update status every 15 seconds:

```
🎬 Video generating...
Current status: Processing
Elapsed: 30 seconds
Estimated remaining: 1-2 minutes
```

---

## API Configuration

| Setting | Value |
|---------|-------|
| Base URL | `https://api.novita.ai` |
| Auth | `Authorization: Bearer <API_KEY>` |
| Get Key | https://novita.ai/settings/key-management |

## Task Types and Endpoints

| Task | Endpoint | Model |
|------|----------|-------|
| Text-to-Image | `/v3/seedream-5.0-lite` | Seedream 5.0 Lite |
| Image Editing | `/v3/seedream-5.0-lite` | Seedream 5.0 Lite |
| Text-to-Video | `/v3/async/vidu-q3-pro-t2v` | Vidu Q3 Pro |
| Image-to-Video | `/v3/async/vidu-q3-pro-i2v` | Vidu Q3 Pro |
| TTS | `/v3/async/minimax-speech-2.8-turbo` | MiniMax Speech 2.8 |
| STT | `/v3/glm-asr` | GLM ASR |
| Task Query | `/v3/async/task-result?task_id=xxx` | - |

---

## Execution Templates

### Text-to-Image

```bash
curl -X POST "https://api.novita.ai/v3/seedream-5.0-lite" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "description"}'
```

### Image Editing

```bash
curl -X POST "https://api.novita.ai/v3/seedream-5.0-lite" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "edit instruction", "reference_images": ["image_url"]}'
```

### Text-to-Video

```bash
curl -X POST "https://api.novita.ai/v3/async/vidu-q3-pro-t2v" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "description", "duration": 4}'
```

### Image-to-Video

```bash
curl -X POST "https://api.novita.ai/v3/async/vidu-q3-pro-i2v" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "motion description", "images": ["image_url"]}'
```

### TTS

```bash
curl -X POST "https://api.novita.ai/v3/async/minimax-speech-2.8-turbo" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "text to convert",
    "voice_setting": {"voice_id": "male-qn-qingse", "speed": 1.0},
    "audio_setting": {"format": "mp3"}
  }'
```

**Available voices:**
- Male: `male-qn-qingse`, `male-qn-jingying`
- Female: `female-shaonv`, `female-yujie`

### STT

```bash
curl -X POST "https://api.novita.ai/v3/glm-asr" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"file": "audio_url_or_base64"}'
```

### Task Result Query

```bash
curl "https://api.novita.ai/v3/async/task-result?task_id=$TASK_ID" \
  -H "Authorization: Bearer $API_KEY"
```

**Status:** `TASK_STATUS_QUEUED` → `TASK_STATUS_PROCESSING` → `TASK_STATUS_SUCCEED`

---

## Error Handling

| Code | Meaning | Action |
|------|---------|--------|
| 401 | Invalid Key | Check configuration |
| 402 | Insufficient balance | Top up at https://novita.ai/billing |
| 429 | Rate limited | Wait and retry |

## Pricing

https://novita.ai/pricing
