---
name: ntriq-video-intelligence-analyzer
description: "AI-powered multimodal analysis for images and videos. Structured tags, scene descriptions, mood analysis, virality scores. 15 languages. Users provide their own URLs — this tool does not scrape or ..."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [media,content]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# Video Intelligence Analyzer

Multimodal AI analysis for images and videos. Returns structured tags, scene descriptions, mood analysis, virality potential scores, and content classification across 15 languages. Users provide their own URLs — no scraping or external data collection.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `media_url` | string | ✅ | Image or video URL |
| `analyses` | array | ❌ | `tags`, `scenes`, `mood`, `virality`, `content_safety` |
| `language` | string | ❌ | Output language ISO code (default: `en`) |
| `audience` | string | ❌ | Target audience context for virality scoring |

## Example Response

```json
{
  "tags": ["sunset", "beach", "golden hour", "ocean", "serene", "travel"],
  "scenes": [
    {"timestamp": "0:00–0:12", "description": "Wide beach panorama, orange sunset sky reflecting on wet sand"},
    {"timestamp": "0:12–0:31", "description": "Close-up of waves breaking, slow motion, foam patterns"}
  ],
  "mood": {"primary": "peaceful", "secondary": "nostalgic", "valence": 0.82},
  "virality_score": 78,
  "virality_factors": ["cinematic quality", "emotional resonance", "trending aesthetic"],
  "content_safety": "safe",
  "language": "en"
}
```

## Use Cases

- Social media content performance prediction before posting
- Brand content library automated tagging at scale
- Ad creative performance pre-screening

## Access

```bash
# x402 endpoint — pay $0.05 USDC per call (Base mainnet)
POST https://x402.ntriq.co.kr/video-intel

# Service catalog
curl https://x402.ntriq.co.kr/services
```

[x402 micropayments](https://x402.ntriq.co.kr) — USDC on Base, gasless EIP-3009
