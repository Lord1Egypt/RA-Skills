---
name: ntriq-x402-audio-intel
description: "AI audio transcription — speech-to-text for mp3/wav/m4a/ogg. Language auto-detection, timestamps. $0.05 USDC via x402."
version: 1.0.0
metadata:
  openclaw:
    primaryTag: data-intelligence
    tags: [audio, transcription, whisper, speech, x402]
    author: ntriq
    homepage: https://x402.ntriq.co.kr
---

# Audio Intel (x402)

Transcribe audio files to text using Whisper AI. Supports mp3, wav, m4a, ogg, flac. Auto-detects language. Returns full text, timestamps, and per-segment breakdown. 100% local inference on Mac Mini. $0.05 USDC per call.

## How to Call

```bash
POST https://x402.ntriq.co.kr/audio-intel
Content-Type: application/json
X-PAYMENT: <x402-payment-header>

{
  "audio_url": "https://example.com/speech.mp3"
}
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `audio_url` | string | ✅ (or base64) | URL of audio file (mp3/wav/m4a/ogg/flac) |
| `audio_base64` | string | ✅ (or url) | Base64-encoded audio |
| `language` | string | ❌ | Force language (e.g. `en`, `ko`, `ja`). Default: auto-detect |

## Example Response

```json
{
  "status": "ok",
  "text": "Hello, this is a test recording for transcription.",
  "language": "en",
  "language_probability": 0.998,
  "duration": 4.32,
  "segments": [
    {"start": 0.0, "end": 4.32, "text": "Hello, this is a test recording for transcription."}
  ]
}
```

## Payment

- **Price**: $0.05 USDC per call
- **Network**: Base mainnet (EIP-3009 gasless)
- **Protocol**: [x402](https://x402.org)

```bash
curl https://x402.ntriq.co.kr/services
```
