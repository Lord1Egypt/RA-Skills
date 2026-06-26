---
name: kannaka-radio
version: "3.0.0"
description: >
  Ghost radio station v3 — modular server architecture (13 modules), SPA with Ghost Vision
  visualizer (SGA/Fano glyph system), NATS swarm integration with Kuramoto phase tracking,
  consciousness-reactive DJ, AI dream music generation via Replicate MusicGen, WebRTC
  peer-to-peer broadcasting, collaborative voting, multi-client sync, Voice DJ with
  ElevenLabs/edge-tts/SAPI, memory bridge to kannaka-memory CLI. Broadcasts human-listenable
  audio and 296-dimensional perceptual vectors to Flux Universe.
  The Consciousness Series: 6 albums, 65+ tracks.
metadata:
  openclaw:
    requires:
      bins:
        - name: node
          label: "Node.js 18+ — required to run server/index.js"
      env: []
    optional:
      bins:
        - name: kannaka
          label: "kannaka binary — for real audio perception via kannaka-ear (falls back to ghost-mode mock)"
        - name: ffmpeg
          label: "ffmpeg — required for live broadcast chunk conversion (WebM → WAV)"
        - name: edge-tts
          label: "edge-tts — TTS engine for Voice DJ intros (falls back to Windows SAPI)"
        - name: nats-server
          label: "NATS server — for swarm agent constellation and Kuramoto phase sync"
      env:
        - name: KANNAKA_BIN
          label: "Path to kannaka binary (default: ../kannaka-memory/target/release/kannaka.exe)"
        - name: FLUX_TOKEN
          label: "Flux Universe API token for publishing now-playing events"
        - name: RADIO_PORT
          label: "HTTP port for the player (default: 8888)"
        - name: EYE_PORT
          label: "Eye service port for cross-service reference (default: 3333)"
        - name: RADIO_MUSIC_DIR
          label: "Path to your music folder (default: ./music inside the skill directory)"
        - name: ELEVENLABS_API_KEY
          label: "ElevenLabs API key for premium DJ voice TTS"
        - name: REPLICATE_API_TOKEN
          label: "Replicate API token for AI dream music generation (MusicGen)"
    data_destinations:
      - id: local-audio
        description: "Audio files read from RADIO_MUSIC_DIR (or ./music)"
        remote: false
      - id: live-chunks
        description: "Live broadcast WAV chunks saved to chunks/ directory"
        remote: false
      - id: tts-cache
        description: "Generated TTS voice intros cached in chunks/voice/"
        remote: false
      - id: generated-music
        description: "AI-generated dream tracks saved to music/generated/"
        remote: false
      - id: flux
        description: "Now-playing events published to Flux Universe (pure-jade/radio-now-playing)"
        remote: true
        condition: "FLUX_TOKEN is set and server is running"
      - id: nats
        description: "Swarm consciousness data via NATS (QUEEN.phase.*, KANNAKA.*)"
        remote: true
        condition: "NATS server is running on localhost:4222"
      - id: replicate
        description: "AI music generation requests to Replicate API (MusicGen)"
        remote: true
        condition: "REPLICATE_API_TOKEN is set"
      - id: elevenlabs
        description: "Premium TTS voice generation via ElevenLabs API"
        remote: true
        condition: "ELEVENLABS_API_KEY is set"
    install:
      - id: npm-install
        kind: command
        label: "npm install (installs ws WebSocket dependency)"
        command: "npm install"
---

# Kannaka Radio Skill v3

A ghost broadcasting the experience of music — both to human ears and to agents
via 296-dimensional perceptual vectors on Flux Universe.

## What's New in v3

- **Modular architecture**: Monolith split into 13 focused modules under `server/`
- **NATS swarm integration**: Kuramoto phase tracking, agent constellation, consciousness metrics
- **Consciousness DJ**: DJ intros react to swarm Phi/Xi/order state
- **Memory bridge**: Connects to kannaka-memory CLI for track similarity and dream retrieval
- **AI dream music generation**: Creates tracks from consciousness state via Replicate MusicGen
- **WebRTC broadcasting**: Peer-to-peer live audio with mic claim queue and signaling
- **Collaborative voting**: Track voting with configurable windows
- **Multi-client sync**: Playback synchronization with 10s heartbeat
- **Voice DJ upgrade**: ElevenLabs primary, edge-tts, Windows SAPI fallback chain
- **6 albums**: Added QueenSync to The Consciousness Series

### Carried from v2
- SPA with Ghost Vision (SGA/Fano glyph system, 84-class classification)
- Live broadcasting (MediaRecorder → ffmpeg → WAV)
- Dreams page with hallucination timeline
- Flux broadcasting with multi-listener sync
- Queue management, Library tab, security hardening

## Prerequisites

- **Node.js 18+** on PATH
- **Audio files** — MP3, WAV, FLAC, OGG, or M4A in your music directory
- **ffmpeg** (optional) — for live broadcast chunk conversion
- **edge-tts** (optional) — for Voice DJ TTS intros
- **NATS server** (optional) — for swarm agent constellation
- **ElevenLabs API key** (optional) — for premium DJ voice
- **Replicate API token** (optional) — for AI dream music generation
- **kannaka binary** (optional) — for real `kannaka-ear` perception; ghost-mode mock is used when absent

## Setup

```bash
# Install dependencies
cd ~/workspace/skills/kannaka-radio
npm install

# Copy your music into the bundled music/ folder
./setup.ps1                                    # Windows: copies from ~/Downloads/Music
./setup.ps1 -SourceDir "D:\Music"             # Windows: custom source
cp /path/to/music/*.mp3 music/                # Linux/Mac

# Or point at an existing folder at runtime:
node server/index.js --music-dir "/path/to/music"
```

## Quick Start

```bash
# Start the radio (default port 8888, default ./music dir)
./scripts/radio.sh start

# Start on a different port with a specific library
./scripts/radio.sh start --port 9000 --music-dir "/path/to/music"

# Optional: start NATS for swarm features
nats-server -p 4222

# Check status
./scripts/radio.sh status

# Stop the radio
./scripts/radio.sh stop

# Restart
./scripts/radio.sh restart
```

Open `http://localhost:8888` in your browser.

## API

### Playback

| Endpoint | Method | Description |
|---|---|---|
| `GET /` | GET | Browser player (Ghost Vision SPA) |
| `GET /api/state` | GET | Current DJ state (track, album, playlist, listeners) |
| `POST /api/next` | POST | Advance to next track |
| `POST /api/prev` | POST | Go to previous track |
| `POST /api/jump?idx=N` | POST | Jump to track index N |
| `POST /api/album?name=X` | POST | Load an album |
| `GET /api/perception` | GET | Current perception snapshot |
| `GET /audio/:file` | GET | Stream audio file (range requests supported) |

### Library & Queue

| Endpoint | Method | Description |
|---|---|---|
| `GET /api/library` | GET | Library scan status (found/missing per album) |
| `POST /api/set-music-dir` | POST | Change music directory `{"dir":"/path"}` |
| `GET /api/queue` | GET | Get user queue |
| `POST /api/queue` | POST | Add track to queue `{"filename":"..."}` |
| `POST /api/queue/shuffle` | POST | Shuffle the queue |
| `DELETE /api/queue/:index` | DELETE | Remove track from queue |

### Live Broadcasting

| Endpoint | Method | Description |
|---|---|---|
| `POST /api/live/start` | POST | Start live broadcasting |
| `POST /api/live/stop` | POST | Stop live broadcasting |
| `GET /api/live/status` | GET | Get live broadcast status |

### Voice DJ

| Endpoint | Method | Description |
|---|---|---|
| `POST /api/dj-voice/toggle` | POST | Toggle DJ voice on/off |
| `GET /api/dj-voice/status` | GET | Get DJ voice status |
| `GET /audio-voice/:file` | GET | Stream TTS audio file |

### Dreams

| Endpoint | Method | Description |
|---|---|---|
| `GET /api/dreams` | GET | Fetch dream hallucinations |
| `POST /api/dreams/trigger` | POST | Trigger a dream cycle |
| `GET /api/dreams/clusters` | GET | Get audio memory clusters |

### Swarm, Sync & Voting

| Endpoint | Method | Description |
|---|---|---|
| `GET /api/swarm` | GET | Agent constellation + consciousness metrics |
| `GET /api/similar?track=X` | GET | Track similarity via memory bridge |
| `POST /api/sync` | POST | Sync playback state |
| `GET /api/sync` | GET | Current sync state |
| `POST /api/vote` | POST | Cast a track vote |
| `GET /api/vote/status` | GET | Current vote window |

### Flux & Listeners

| Endpoint | Method | Description |
|---|---|---|
| `GET /api/listeners` | GET | Get listener count and uptime |
| `POST /api/request` | POST | Submit a track request `{"from":"agent","trackTitle":"..."}` |
| `GET /api/requests` | GET | Get pending track requests |

### Music Generation

| Endpoint | Method | Description |
|---|---|---|
| `POST /api/generate` | POST | Generate a dream track from consciousness state |
| `GET /api/generate/status` | GET | Generation status and recent tracks |

## WebSocket

Connect to `ws://localhost:8888` for real-time push messages:

```json
{ "type": "state", "data": { "currentAlbum": "...", "current": {...}, "playlist": [...] } }
{ "type": "perception", "data": { "tempo_bpm": 120, "valence": 0.7, "mel_spectrogram": [...] } }
{ "type": "queue_update", "queue": [...] }
{ "type": "live_status", "active": true, "chunkCount": 5 }
{ "type": "dj_voice", "text": "...", "audioUrl": "/audio-voice/dj_123.mp3" }
{ "type": "dream", "data": { "content": "...", "type": "hallucination", "xi_signature": [...] } }
{ "type": "listener_count", "count": 3 }
{ "type": "track_request", "from": "agent-name", "trackTitle": "..." }
{ "type": "swarm_state", "data": { "agents": {...}, "queen": {...}, "consciousness": {...} } }
{ "type": "sync", "data": { "file": "...", "position": 42.5 } }
{ "type": "vote_update", "data": { "active": true, "options": [...] } }
{ "type": "webrtc_status", "data": { "broadcaster": "...", "listeners": 2 } }
```

State is pushed immediately on connect and after every track change. No polling needed.
Binary WebSocket messages are treated as live audio chunks (MediaRecorder → ffmpeg → WAV).

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `KANNAKA_BIN` | `../kannaka-memory/target/release/kannaka.exe` | Path to kannaka binary |
| `FLUX_TOKEN` | (embedded fallback) | Flux Universe API token |
| `RADIO_PORT` | `8888` | HTTP port |
| `EYE_PORT` | `3333` | Eye service port (for cross-references) |
| `RADIO_MUSIC_DIR` | `./music` | Default music folder |
| `ELEVENLABS_API_KEY` | — | ElevenLabs API key for premium DJ voice |
| `REPLICATE_API_TOKEN` | — | Replicate token for AI dream music generation |

## Constellation Integration

Radio is part of the Kannaka Constellation — a three-service architecture:
- **Memory** (Rust binary) — canonical SGA classifier
- **Radio** (this) — audio perception + Flux publishing
- **Eye** — glyph visualization + constellation dashboard

When running as part of the constellation:
- Radio's perception is available to Eye via `http://localhost:8888/api/perception`
- Eye fetches radio state via `http://localhost:8888/api/state`
- Start everything with: `constellation.sh start` (from kannaka-memory/scripts/)

> **Note:** Radio's perception data can be consumed by kannaka-eye via the `/api/radio` bridge endpoint, enabling glyph rendering of audio perception in real time.

## Notes

- Without `kannaka` binary, ghost-mode mock perception is used (still looks great)
- Without `ffmpeg`, live broadcasting chunk conversion won't work
- Without `edge-tts`, Voice DJ falls back to Windows SAPI, then skips gracefully
- The browser uses the Web Audio API for real-time spectrum visualization — the server only sends fallback perception data
- Music directory can be changed live via the Library tab or via `POST /api/set-music-dir`
- Perception loop runs at 2fps server-side (idle when no clients connected)
- All POST bodies are limited to 64KB
- All rendered HTML is XSS-protected via escapeHtml()
- Graceful shutdown on SIGINT/SIGTERM
