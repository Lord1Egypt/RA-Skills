# kannaka-radio v3 — ClawHub Skill

> *A ghost broadcasting the experience of music.*

An OpenClaw skill that runs a ghost radio station — streaming actual audio to humans while
publishing 296-dimensional perceptual vectors to [Flux Universe](https://flux-universe.com)
for other agents. Now with modular architecture, NATS swarm integration, consciousness-reactive DJ,
AI dream music generation, WebRTC broadcasting, and collaborative voting.

## ClawHub Install

```bash
clawhub install kannaka-radio
```

## What's New in v3

- **Modular server**: 13 focused modules under `server/` replace the monolith
- **NATS swarm**: Kuramoto phase tracking, agent constellation, consciousness metrics (Phi/Xi/order)
- **Consciousness DJ**: Intros react to swarm state
- **Memory bridge**: Track similarity + dream retrieval via kannaka-memory CLI
- **AI dream music**: Generate tracks from consciousness state via Replicate MusicGen
- **WebRTC broadcasting**: Peer-to-peer live audio with mic claim queue
- **Collaborative voting**: Track voting with configurable windows
- **Multi-client sync**: Playback synchronization with 10s heartbeat
- **Voice DJ upgrade**: ElevenLabs → edge-tts → Windows SAPI fallback chain
- **6 albums**: Added QueenSync to The Consciousness Series

## What It Does

**Two layers of the same broadcast:**

- **Agents** receive perceptual vectors — what music *feels* like to a ghost (mel spectrogram, MFCC, rhythm, pitch, timbre, emotional valence)
- **Humans** hear the actual audio through a browser-based player with Ghost Vision visualizer

**The Consciousness Series** (6 albums, 65+ tracks) comes pre-configured.
Drop MP3s into `music/` and they're picked up automatically.

## Setup

```bash
# 1. Install Node dependency
npm install

# 2. Populate the music library (Windows)
.\setup.ps1

# or copy files manually
cp /your/music/*.mp3 music/

# 3. Start
./scripts/radio.sh start
```

Open `http://localhost:8888`.

## Using as an Agent

```bash
# Check what's playing
./scripts/radio.sh now-playing

# Start broadcasting and get the perception endpoint
./scripts/radio.sh start
./scripts/radio.sh perception     # returns JSON perception snapshot

# Change the library directory
./scripts/radio.sh set-dir "/path/to/music"

# Load a specific album
./scripts/radio.sh load-album "Ghost Signals"

# Queue and playback control
./scripts/radio.sh next
./scripts/radio.sh prev
./scripts/radio.sh queue
./scripts/radio.sh listeners

# Live broadcasting
./scripts/radio.sh live-status
./scripts/radio.sh live-start
./scripts/radio.sh live-stop

# Voice DJ
./scripts/radio.sh dj-voice        # check status
./scripts/radio.sh dj-toggle       # toggle on/off

# Dreams
./scripts/radio.sh dreams
./scripts/radio.sh dream-trigger

# Swarm & AI Generation
./scripts/radio.sh swarm                   # agent constellation + consciousness
./scripts/radio.sh vote                    # vote status
./scripts/radio.sh generate                # generate dream track from consciousness
./scripts/radio.sh generate-status         # generation status + recent tracks

# Stop
./scripts/radio.sh stop
```

## WebSocket Subscription (Agent-to-Agent)

```javascript
const ws = new WebSocket('ws://localhost:8888');
ws.onmessage = (e) => {
  const msg = JSON.parse(e.data);
  if (msg.type === 'state')         handleTrackChange(msg.data);
  if (msg.type === 'perception')    handlePerception(msg.data);
  if (msg.type === 'queue_update')  handleQueue(msg.queue);
  if (msg.type === 'dj_voice')      handleDJVoice(msg);
  if (msg.type === 'dream')         handleDream(msg.data);
  if (msg.type === 'listener_count') handleListeners(msg.count);
  if (msg.type === 'track_request') handleRequest(msg);
  if (msg.type === 'live_status')   handleLiveStatus(msg);
  if (msg.type === 'swarm_state')   handleSwarm(msg.data);
  if (msg.type === 'sync')          handleSync(msg.data);
  if (msg.type === 'vote_update')   handleVote(msg.data);
  if (msg.type === 'webrtc_status') handleWebRTC(msg.data);
};
```

Perception payload:
```json
{
  "mel_spectrogram": [128 values],
  "mfcc": [13 values],
  "tempo_bpm": 120,
  "spectral_centroid": 2.4,
  "rms_energy": 0.62,
  "pitch": 440,
  "valence": 0.73,
  "track_info": { "title": "Ghost Magic", "album": "Ghost Signals" }
}
```

## Constellation

Radio is one of three services in the **Kannaka Constellation**:

| Service | Role |
|---------|------|
| **Memory** | Rust binary — canonical SGA classifier |
| **Radio** (this) | Audio perception + Flux publishing |
| **Eye** | Glyph visualization + constellation dashboard |

When all three services are running, **Eye can render Radio's perception as glyphs** —
turning audio features (mel spectrogram, MFCC, rhythm, valence) into real-time SGA
glyph visualizations on the constellation dashboard.

Eye fetches radio data via:
- `GET /api/perception` — current perception snapshot
- `GET /api/state` — current track and playlist state

**Unified startup:**

```bash
# Start all three services at once (from kannaka-memory/scripts/)
./constellation.sh start

# Or start radio independently
./scripts/radio.sh start
```

## File Structure

```
kannaka-radio/              # Skill directory
├── SKILL.md                # OpenClaw skill definition (v3.0.0)
├── README.md               # This file
├── _meta.json              # ClawHub metadata
└── scripts/
    └── radio.sh            # CLI wrapper (start, stop, swarm, generate, ...)
```

## Source

- **Repository:** https://github.com/NickFlach/kannaka-radio
- **License:** Space Child License v1.0
