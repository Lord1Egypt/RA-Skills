---
name: jetson-cuda-voice
description: "High-performance offline voice pipeline for NVIDIA Jetson with wake word detection, STT, and TTS."
license: MIT-0
---

# Jetson CUDA Voice Skill

A high-performance, bilingual (English/Greek) local voice assistant pipeline designed specifically for resource-constrained platforms like the NVIDIA Jetson Xavier NX.

## Architecture

```
┌─────────────────────────────────────────────────┐
│ JETSON CUDA VOICE PIPELINE (COMPLETE STACK)     │
├─────────────────────────────────────────────────┤
│                                                  │
│ 1. ReSpeaker Microphone (hw:Array,0)            │
│    └─ Always listening                          │
│                                                  │
│ 2. Silero VAD (330ms)                           │
│    └─ "Is there speech?"                        │
│                                                  │
│ 3. Hey Jarvis Detection (137ms)                 │
│    └─ "Is wake word detected?"                  │
│                                                  │
│ 4. ReSpeaker LED Feedback                       │
│    └─ 🟣 Purple pulse = Listening               │
│                                                  │
│ 5. Fast-Path LLM Query (0.26s)                  │
│    └─ Groq LLaMA 3.1 8B instant query           │
│                                                  │
│ 6. Slow-Path LLM Query (with tools)             │
│    └─ OpenClaw Gateway Session (HA, Web, Weather)│
│                                                  │
│ 7. Edge TTS (el-GR-NestorasNeural / Edge)        │
│    └─ Generate Greek/English response           │
│                                                  │
│ 8. Speaker Output (hw:C2c,0)                    │
│    └─ Play response                             │
│                                                  │
└─────────────────────────────────────────────────┘
```

## Features

- **Double-Path Architecture**: 
  - **Fast-Path**: High-performance Groq-based direct query with ultra-low latency (~260ms) for casual queries.
  - **Slow-Path**: Fully-featured OpenClaw gateway connection with device control, web search, and weather integration.
- **Bilingual Processing**: Seamless support and automatic language matching for Greek and English.
- **Local Wake Word Detection**: Employs openWakeWord with a custom pre-trained model (`hey_jarvis_v0.1.onnx`) optimized for Jetson ARM64 architecture.
- **Systemd Integration**: Includes service templates for background daemonization and boot-persistent listening.
- **Visual LED Feedback**: Direct support for the ReSpeaker Mic Array LED indicators (purple pulse on listening).

## Installation & Setup

1. **System Dependencies**:
   Ensure `arecord` and Python 3.11 are installed.

2. **Required Environment Variables**:
   Configure the following environment variables in your systemd unit or `.bashrc`:
   - `OPENCLAW_GATEWAY_TOKEN`: OpenClaw Gateway authorization token.
   - `GATEWAY_URL`: Base URL of the OpenClaw instance (e.g., `http://127.0.0.1:18789`).
   - `GROQ_API_KEY`: API Key for fast-path inference.
   - `ALFRED_MIC`: Audio recording hardware interface (default: `hw:Array,0`).
   - `ALFRED_SPEAKER`: Audio output speaker interface (default: `hw:C2c,0`).

3. **Running the Daemon**:
   To start the pipeline daemon:
   ```bash
   ./scripts/manage.sh start
   ```

4. **Running as a Systemd Service**:
   Copy the service template to your user-level systemd directory (`~/.config/systemd/user/voice-pipeline.service`) and manage it via:
   ```bash
   systemctl --user daemon-reload
   systemctl --user enable voice-pipeline.service
   systemctl --user start voice-pipeline.service
   ```
