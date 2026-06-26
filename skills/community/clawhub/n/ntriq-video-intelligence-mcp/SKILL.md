---
name: ntriq-video-intelligence-mcp
description: "Video analysis: object detection, scene classification, activity recognition, and summarization."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [video,intelligence,analysis]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# Video Intelligence MCP

Comprehensive video analysis: object detection, scene classification, activity recognition, and narrative summarization. Returns timestamped object tracks, scene labels, detected activities, and an executive summary of video content.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `video_url` | string | ✅ | Video file URL |
| `tasks` | array | ❌ | `objects`, `scenes`, `activities`, `summary` (default: all) |
| `confidence_threshold` | float | ❌ | Min detection confidence 0.0–1.0 (default: 0.7) |
| `frame_sample_rate` | integer | ❌ | Frames per second to sample (default: 1) |

## Example Response

```json
{
  "duration_seconds": 98.3,
  "objects_detected": [
    {"label": "person", "count": 3, "first_seen": "0:02", "confidence": 0.97},
    {"label": "laptop", "count": 2, "first_seen": "0:08", "confidence": 0.89}
  ],
  "scenes": [
    {"timestamp": "0:00–0:35", "label": "office_meeting", "confidence": 0.93},
    {"timestamp": "0:35–1:38", "label": "product_demo", "confidence": 0.88}
  ],
  "activities": ["discussion", "screen_sharing", "whiteboard_drawing"],
  "summary": "Three-person product demo meeting. Presenter shows software on laptop. Whiteboard session at 0:52."
}
```

## Use Cases

- Security camera automated incident detection
- Video content moderation at scale
- Sports video highlight clip identification

## Access

```bash
# x402 endpoint — pay $0.05 USDC per call (Base mainnet)
POST https://x402.ntriq.co.kr/video-intel-mcp

# Service catalog
curl https://x402.ntriq.co.kr/services
```

[x402 micropayments](https://x402.ntriq.co.kr) — USDC on Base, gasless EIP-3009
