---
name: video-generation
description: Complete workflow for generating avatar videos
---

# Video Generation

## Overview

Videos are generated asynchronously. The workflow is:
1. Submit video creation request → Get Task ID
2. Retrieve video URL

## TTS Video (Text-to-Speech)

Generate video from text using an avatar and voice.

```bash
python scripts/idr_video_client.py create_video \
  --type tts \
  --text "Welcome to our service. We're excited to have you here." \
  --avatar "AVATAR_ID" \
  --avatar_res "RESOLUTION" \
  --voice "VOICE_ID"
```

### Output

```
Task started: 293838
Waiting for task 293838 to complete...
......
Task Completed!
Video URL: https://xy-avatar-prod.oss-cn-hangzhou.aliyuncs.com/.../a1_n_xxxxx_a1.mp4
```

## Audio-Driven Video

Generate video from pre-recorded audio.

```bash
python scripts/idr_video_client.py create_video \
  --type audio \
  --audio /path/to/narration.mp3 \
  --avatar "AVATAR_ID"
```

## Task Status

Check the status of any generation task:

```bash
python scripts/idr_video_client.py check_task \
  --id "TASK_ID" \
  --type video  # or "voice" or "avatar"
```

### Status Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Processing |
| 2 | Waiting in queue |
| 3 | Failed |

