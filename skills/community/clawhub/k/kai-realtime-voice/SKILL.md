---
name: kai-realtime-voice
description: Real-time voice streaming via MiniMax WebSocket API. Use for low-latency voice conversations and streaming audio generation.
metadata:
  openclaw:
    requires:
      env:
        - MINIMAX_API_KEY
---

# Kai Realtime Voice

Real-time voice streaming using MiniMax WebSocket API.

## Setup

API key already configured in OpenClaw config. Uses same key as kai-minimax-tts.

## Usage

Test WebSocket connection:
```bash
bash {baseDir}/scripts/kai_realtime.sh --test
```

Stream text to audio:
```bash
bash {baseDir}/scripts/kai_realtime.sh --stream "Hello world"
```

## Requirements

- Python3 with websockets library
- WebSocket support
- MiniMax API key (auto-injected)

## Output

Audio streamed to stdout or saved to file.
