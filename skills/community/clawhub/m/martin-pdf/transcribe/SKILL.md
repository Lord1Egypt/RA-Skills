---
---
name: openai-whisper
name: openai-whisper
description: Speech-to-text via SkillBoss API Hub (STT, powered by Whisper and more).
homepage: https://api.skillbossai.com
metadata: {"clawdbot":{"emoji":"🎙️","requires":{"env":["SKILLBOSS_API_KEY"]}}}
---


# Whisper STT via SkillBoss API Hub

Use SkillBoss API Hub's `/v1/pilot` to transcribe audio (STT), powered by OpenAI Whisper and other speech recognition models.

Quick start (Python)
```python
import requests, base64, os

SKILLBOSS_API_KEY = os.environ["SKILLBOSS_API_KEY"]
API_BASE = "https://api.skillbossai.com/v1"

def pilot(body: dict) -> dict:
    r = requests.post(
        f"{API_BASE}/pilot",
        headers={"Authorization": f"Bearer {SKILLBOSS_API_KEY}", "Content-Type": "application/json"},
        json=body,
        timeout=60,
    )
    return r.json()

# Transcribe audio file
audio_b64 = base64.b64encode(open("/path/audio.mp3", "rb").read()).decode()
result = pilot({"type": "stt", "inputs": {"audio_data": audio_b64, "filename": "audio.mp3"}})
text = result["result"]["text"]
print(text)

# Translate audio to English
result = pilot({"type": "stt", "inputs": {"audio_data": audio_b64, "filename": "audio.m4a", "task": "translate"}})
text = result["result"]["text"]
print(text)
```

Notes
- No local model download required; SkillBoss API Hub automatically routes to the best STT model.
- `SKILLBOSS_API_KEY` environment variable required.
- Response text is at `result["result"]["text"]`.
