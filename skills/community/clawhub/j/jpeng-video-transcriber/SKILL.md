---
name: jpeng-video-transcriber
description: "Transcribe speech from videos"
version: "1.0.0"
author: "jpeng"
tags: ["ai", "transcription", "video"]
---

# Video Transcriber

Transcribe speech from videos

## When to Use

- User needs ai related functionality
- Automating transcription tasks
- Video operations

## Usage

```bash
python3 scripts/video_transcriber.py --input <input> --output <output>
```

## Configuration

Set required environment variables:

```bash
export TRANSCRIPTION_API_KEY="your-api-key"
```

## Output

Returns JSON with results:

```json
{
  "success": true,
  "data": {}
}
```
