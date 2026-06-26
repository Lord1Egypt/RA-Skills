# Architecture Overview

## System Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Windows Host                              │
│                                                                  │
│  ┌──────────────────┐     ┌───────────────────────────────────┐ │
│  │   Claude Code    │     │         Docker Desktop             │ │
│  │  (the Agent)     │     │                                   │ │
│  │                  │     │  ┌─────────────┐  ┌────────────┐ │ │
│  │  meeting_bot.py  │◄────┼──┤ vexa-meeting│  │vexa-whisper│ │ │
│  │  claude_client.py│     │  │    -bot     │  │  -proxy    │ │ │
│  │  agent_tool.py   │     │  │  :8056      │  │  :8000     │ │ │
│  └──────────────────┘     │  └──────┬──────┘  └─────┬──────┘ │ │
│                            │         │               │         │ │
│                            │  ┌──────▼──────┐  ┌────▼──────┐ │ │
│                            │  │ vexa-postgres│  │vexa-whisper│ │ │
│                            │  │   :5432      │  │  :8000    │ │ │
│                            │  └─────────────┘  └───────────┘ │ │
│                            └───────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                      │
                               Internet (HTTPS)
                                      │
                         ┌────────────▼────────────┐
                         │    Google Meet Server    │
                         │  (or Zoom, Teams, etc.)  │
                         └─────────────────────────┘
                                      │
                              Meeting participants
                                      │
                              ┌───────▼───────┐
                              │  Your browser │
                              │  (Zero G)     │
                              └───────────────┘
```

## Components

### 1. Vexa Meeting Bot (`vexaai/vexa-lite`)
- Docker container running a headless Chromium browser
- Joins meetings as a named participant ("OpenClaw Assistant")
- Captures participant microphone audio as WAV files
- Sends/receives meeting chat messages
- Provides REST API on port 8056
- Uses PostgreSQL for state persistence and Redis (internal) for streams

### 2. Whisper Transcription Server (`fedirz/faster-whisper-server`)
- Runs faster-whisper CPU inference
- Exposes OpenAI-compatible `/v1/audio/transcriptions` endpoint
- Pre-loads `Systran/faster-whisper-base` model
- NOT directly exposed to host (internal Docker network only)

### 3. Whisper Proxy (`whisper_proxy.py` in `python:3.11-slim`)
- Sits between Vexa and the whisper server
- **Critical**: rewrites `model=default` → `model=Systran/faster-whisper-base`
  in the multipart form body of transcription requests
- Vexa's internal `whisper_live.remote_transcriber` hardcodes `model=default`
  which the faster-whisper-server rejects as invalid
- Exposed on host port 8000 for manual testing

### 4. PostgreSQL (`postgres:16-alpine`)
- Stores meeting state, recordings metadata, transcript segments
- Persisted via Docker volume `vexa_pgdata`

### 5. Claude Code Agent (`meeting_bot.py` + `claude_client.py`)
- Runs on the host (Windows side via conda Python)
- Polls Vexa API every 5s for new chat messages
- Runs analysis loop every 30s (screenshot + transcript delta → Claude)
- Uses `ANTHROPIC_API_KEY` environment variable (no separate key needed
  when operated as a Claude Code skill — Claude Code IS the agent)

## Data Flow

### Audio Transcription Flow
```
Meeting Audio
    │
    ▼ (WebRTC, participant mics only)
vexa-meeting-bot
    │ streams audio chunks
    ▼
whisper_live WebSocket (internal port 9090)
    │ sends to remote transcriber
    ▼
whisper-proxy:8000/v1/audio/transcriptions
    │ rewrites model=default → Systran/faster-whisper-base
    ▼
vexa-whisper:8000/v1/audio/transcriptions
    │ faster-whisper inference
    ▼
transcript segments → stored in PostgreSQL
    │
    ▼
GET /transcripts/google_meet/{meeting_id}
    │
    ▼
Claude analysis → chat message
```

### Chat Interaction Flow
```
User types in meeting chat
    │
    ▼
Vexa bot captures chat
    │
GET /bots/google_meet/{id}/chat
    │
    ▼ (every 5 seconds)
_process_incoming_chat() in meeting_bot.py
    │
    ▼ (if message triggers response)
claude_client.respond_to_chat()
    │
    ▼
POST /bots/google_meet/{id}/chat  {"text": "...reply..."}
    │
    ▼
Message appears in meeting chat
```

## Networking Notes

- All Docker containers share the same compose-defined network (`172.18.x.x`)
- Vexa references whisper via Docker DNS: `http://whisper-proxy:8000`
- Host accesses Vexa API via `http://localhost:8056`
- **`host.docker.internal` does NOT work** in this Docker Desktop + WSL2 setup
  — containers cannot reach Windows host via this hostname
- The whisper proxy must run INSIDE Docker to be reachable by Vexa

## Key Design Decisions

| Decision | Reason |
|---|---|
| Google Meet over Zoom | `vexa-lite` Docker image lacks proprietary Zoom SDK native binaries |
| Whisper proxy in Docker | `host.docker.internal` unreachable from containers in this WSL2 setup |
| Python proxy (not nginx) | Needs to rewrite multipart form body content, not just headers |
| Claude Code as agent | No separate ANTHROPIC_API_KEY needed; Claude Code session IS the agent |
| `requests` library for API calls | Handles UTF-8 JSON encoding correctly vs PowerShell Invoke-WebRequest |
| X-API-Key header (not Bearer) | Vexa user token uses `X-API-Key`, not `Authorization: Bearer` |
