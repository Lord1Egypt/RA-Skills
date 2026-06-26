# Architecture

## Audio Pipeline

```
Mic (24kHz) / Browser WebSocket
  → Audio Callback (energy detection + Silero VAD)
  → Audio Queue
  → KiwiListener._record_loop()
  → STT (Faster Whisper | ElevenLabs | MLX Whisper)
  → Wake Word Detection ("kiwi" — text fuzzy match or ML pre-detection)
  → Speaker ID (pyannote embedding → cosine similarity)
  → Priority Gate (OWNER > FRIEND > GUEST > BLOCKED)
  → Voice Security (DangerousCommandDetector → Telegram approval)
  → OpenClaw Gateway (WebSocket v3: chat.send → delta/final events)
  → LLM response stream (delta → sentence chunking)
  → Streaming TTS (Kokoro / Piper / Qwen3 / ElevenLabs)
  → Speaker Output (with barge-in detection)
  → Loop back to listening
```

## Key Modules

| Module | File | Purpose |
|--------|------|---------|
| **Service** | `kiwi/service.py` | Main orchestrator, lifecycle management |
| **Listener** | `kiwi/listener.py` | Microphone capture, VAD, STT, wake word |
| **OpenClaw WS** | `kiwi/openclaw_ws.py` | WebSocket client to OpenClaw Gateway |
| **Speaker Manager** | `kiwi/speaker_manager.py` | Voiceprint storage, identification, priority |
| **Voice Security** | `kiwi/voice_security.py` | Dangerous command detection, Telegram approval |
| **Soul Manager** | `kiwi/soul_manager.py` | Personality loading and switching |
| **i18n** | `kiwi/i18n.py` | Internationalization (`t()` function) |
| **Event Bus** | `kiwi/event_bus.py` | Internal pub/sub event system |
| **API Server** | `kiwi/api/server.py` | REST API + WebSocket events, aiohttp |
| **TTS Providers** | `kiwi/tts/` | ElevenLabs, Kokoro, Piper, Qwen3 |

## Mixins

The main service class uses mixins to separate concerns:

| Mixin | File | Responsibility |
|-------|------|----------------|
| `LLMCallbacks` | `kiwi/mixins/llm_callbacks.py` | LLM token/completion/exec approval handlers |
| `DialoguePipeline` | `kiwi/mixins/dialogue_pipeline.py` | Dialogue stages including approval checks |

## Event Bus

Kiwi uses an internal event bus (`kiwi/event_bus.py`) for decoupled communication between modules:

```python
from kiwi.event_bus import EventBus

bus = EventBus()
bus.subscribe("WAKE_WORD_DETECTED", handler)
bus.emit("WAKE_WORD_DETECTED", {"text": "kiwi"})
```

Events are also forwarded to the WebSocket API (`/api/events`) for the dashboard and external integrations.

Key events: `STATE_CHANGED`, `WAKE_WORD_DETECTED`, `SPEECH_RECOGNIZED`, `SPEAKER_IDENTIFIED`, `TTS_STARTED`, `TTS_FINISHED`, `LLM_TOKEN`, `LLM_COMPLETE`, `EXEC_APPROVAL_REQUESTED`, `EXEC_APPROVAL_RESOLVED`, `SOUL_CHANGED`, `ERROR`.

## OpenClaw Protocol

Kiwi communicates with OpenClaw via WebSocket Gateway v3:

1. Connect to `ws://127.0.0.1:18789`
2. Send `chat.send` with user message
3. Receive `delta` events (streaming tokens) and `final` event (complete response)
4. Subscribe to `exec.approval.requested` for shell command approvals
5. Send `exec.approval.resolve` with approve/deny decision

## Threading Model

- **Main thread:** Service lifecycle, signal handling
- **Audio thread:** Microphone callback (daemon)
- **Record loop:** STT + wake word + command processing (daemon)
- **TTS thread:** Audio output (daemon)
- **API thread:** aiohttp server in separate event loop (daemon)
- **WebSocket thread:** OpenClaw Gateway connection (daemon)

All background threads are daemon threads with crash protection (try/except + sleep + continue in loops). Shared resources are guarded by `threading.Lock`.
