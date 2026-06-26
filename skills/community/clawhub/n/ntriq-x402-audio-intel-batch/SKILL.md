---
name: ntriq-x402-audio-intel-batch
description: "Batch audio transcription for up to 500 files. Flat $9.00 USDC via x402."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [audio, transcription, whisper, batch, x402]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# Audio Intel Batch (x402)

Transcribe up to 500 audio files in one call. Flat $9.00 USDC. 100% local Whisper inference on Mac Mini.

## How to Call

```bash
POST https://x402.ntriq.co.kr/audio-intel-batch
Content-Type: application/json
X-PAYMENT: <x402-payment-header>

{
  "audio_urls": [
    "https://example.com/call-001.mp3",
    "https://example.com/call-002.mp3"
  ],
  "language": "en"
}
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `audio_urls` | array | ✅ | Audio file URLs (max 500) |
| `language` | string | ❌ | Force language for all files. Default: auto-detect |

## Example Response

```json
{
  "status": "ok",
  "count": 2,
  "results": [
    {"index": 0, "audio_url": "https://example.com/call-001.mp3", "status": "ok", "text": "...", "language": "en", "duration": 12.5},
    {"index": 1, "audio_url": "https://example.com/call-002.mp3", "status": "ok", "text": "...", "language": "en", "duration": 8.3}
  ]
}
```

## Payment

- **Price**: $9.00 USDC flat (up to 500 files)
- **Network**: Base mainnet (EIP-3009 gasless)
- **Protocol**: [x402](https://x402.org)

```bash
curl https://x402.ntriq.co.kr/services
```
