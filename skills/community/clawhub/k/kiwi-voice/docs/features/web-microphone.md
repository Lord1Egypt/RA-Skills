# Web Microphone

The dashboard includes a **Web Microphone** that lets you talk to Kiwi directly from the browser — no local microphone setup or pyaudio installation needed.

## How it Works

1. **Browser captures audio** via [AudioWorklet](https://developer.mozilla.org/en-US/docs/Web/API/AudioWorklet) — low-latency audio processing off the main thread
2. **PCM Int16 audio** is streamed to Kiwi over a WebSocket (`/api/audio`)
3. Kiwi processes it through the same pipeline: STT → wake word → Speaker ID → LLM → TTS
4. **TTS responses** are streamed back to the browser and played via AudioWorklet
5. Live volume bars show audio level in real time

## Usage

Click the microphone button in the dashboard to connect. The button animates with concentric rings while active. Volume bars show live input level.

!!! tip
    The browser will ask for microphone permission on first use. Make sure to allow it.

## Configuration

```yaml
web_audio:
  enabled: true
  sample_rate: 16000
  max_clients: 3
```

| Field | Description |
|-------|-------------|
| `enabled` | Enable/disable web audio streaming |
| `sample_rate` | Audio sample rate in Hz (default: 16000) |
| `max_clients` | Maximum simultaneous browser connections |

## WebSocket Protocol

The web audio endpoint is at `ws://localhost:7789/api/audio`.

**Client → Server:** Raw PCM Int16 audio frames as binary WebSocket messages.

**Server → Client:** TTS audio frames as binary WebSocket messages for browser playback.

## Requirements

- Modern browser with AudioWorklet support (Chrome, Firefox, Edge, Safari 14.1+)
- HTTPS or localhost (AudioWorklet requires a secure context)
- Microphone permission granted
