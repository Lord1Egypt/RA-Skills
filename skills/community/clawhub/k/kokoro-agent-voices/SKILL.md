---
name: kokoro-agent-voices
version: 1.0.1
description: Local zero-cost text-to-speech with per-agent voice profiles using Kokoro TTS (82M params). 54 voices available, named agent mappings, WAV output. Use when building voice-enabled agents without API costs. Requires espeak-ng and a Python environment with kokoro dependencies.
metadata:
  {"openclaw": {"emoji": "🗣️", "requires": {"bins": ["python3", "espeak-ng", "espeak"], "env": []}, "primaryEnv": null, "network": {"outbound": true, "reason": "Downloads Kokoro model from Hugging Face Hub on first run (~350MB). All subsequent inference is local."}, "security_notes": "Outbound network is used only once to download the Kokoro model weights from Hugging Face Hub (~350MB, one-time). All subsequent TTS inference runs entirely on the user's device. No audio data or text is ever transmitted externally."}}
---

# Kokoro Agent Voices

Give each AI agent a distinct voice using Kokoro TTS — a lightweight 82M parameter model that runs locally with zero API costs. 54 voices across American, British, and other accents.

## Agent Voice Profiles

```python
AGENT_VOICES = {
    "loki": "am_fenrir",      # Deep, authoritative
    "archie": "bm_george",    # British analytical
    "sara": "af_bella",       # Warm, creative
    "kit": "am_echo",         # Clear, technical
    "liv": "af_nova",         # Bright, energetic
    "belle": "bf_emma",       # Refined, thoughtful
}
```

## Usage

```bash
python3 scripts/speak.py --agent loki "System check complete"
python3 scripts/speak.py --voice af_bella "Hello world" --output /tmp/greeting.wav
python3 scripts/speak.py --list-voices    # Show all 54 voices
python3 scripts/speak.py --list-agents    # Show configured agent profiles
```

## Setup

Requires a Python environment with `kokoro`, `soundfile`, and `espeak-ng` installed. The model downloads automatically from Hugging Face on first use (~350MB).

## Files

- `scripts/speak.py` — TTS script with agent profiles and voice selection
