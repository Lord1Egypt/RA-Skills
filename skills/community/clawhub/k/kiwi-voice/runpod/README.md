# Qwen3-TTS RunPod Serverless (All Modes)

Docker image for Qwen3-TTS on RunPod Serverless with **all three modes**:

| Mode | Model | Use Case |
|------|-------|----------|
| **clone** | Base | Clone any voice from reference audio |
| **custom** | CustomVoice | 9 preset voices + style instructions |
| **design** | VoiceDesign | Generate voice from text description |

## Quick Start

### Build & Push

```powershell
cd runpod

# Set path to your local qwen_tts package
$env:QWEN_TTS_SOURCE = "/path/to/qwen_tts"

# Build and push to Docker Hub
.\build.ps1 -Username YOUR_DOCKERHUB_USERNAME -Push
```

### Deploy on RunPod

1. [RunPod Console](https://console.runpod.io/serverless) → New Endpoint
2. Image: `docker.io/YOUR_USERNAME/qwen3-tts:latest`
3. GPU: 24GB+ (L40, A5000, RTX 4090)
4. Env: `MODEL_SIZE=0.6B`

---

## API Reference

### Mode Auto-Detection

The handler automatically detects mode based on parameters:
- Has `ref_audio` → **clone**
- Has `voice_description` → **design**  
- Otherwise → **custom**

Or set `"mode": "clone"/"custom"/"design"` explicitly.

---

### 🎤 Clone Mode (Voice Cloning)

Clone any voice from a reference audio sample.

```json
{
  "input": {
    "mode": "clone",
    "text": "Привет! Как дела?",
    "ref_audio": "<base64 WAV/MP3>",
    "ref_text": "Transcript of what is said in ref_audio",
    "language": "Auto",
    "x_vector_only_mode": false
  }
}
```

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `text` | string | ✅ | - | Text to synthesize |
| `ref_audio` | string | ✅ | - | Base64 encoded reference audio |
| `ref_text` | string | ✅* | - | Transcript (*required if x_vector_only_mode=false) |
| `x_vector_only_mode` | bool | ❌ | false | Use only speaker embedding (faster, lower quality) |
| `language` | string | ❌ | "Auto" | Auto, Russian, English, Chinese, Japanese, Korean |

---

### 🎭 Custom Mode (Preset Voices)

Use one of 9 preset voices with style instructions.

```json
{
  "input": {
    "mode": "custom",
    "text": "Привет! Как дела?",
    "speaker": "ono_anna",
    "style": "playful",
    "language": "Russian"
  }
}
```

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `text` | string | ✅ | - | Text to synthesize |
| `speaker` | string | ❌ | "ono_anna" | Voice preset (see below) |
| `style` | string | ❌ | "neutral" | Style preset (see below) |
| `instruct` | string | ❌ | - | Custom instruction (overrides style) |

**Speakers:** `aiden`, `dylan`, `eric`, `ono_anna`, `ryan`, `serena`, `sohee`, `uncle_fu`, `vivian`

**Styles:** `neutral`, `excited`, `calm`, `confident`, `whisper`, `sad`, `angry`, `playful`, `serious`, `cheerful`

**Custom instruction example:**
```json
{
  "input": {
    "text": "...",
    "speaker": "vivian",
    "instruct": "Speak like an anime girl, high-pitched and cute"
  }
}
```

---

### 🎨 Design Mode (Voice from Description)

Generate a voice from a text description.

```json
{
  "input": {
    "mode": "design",
    "text": "Привет! Как дела?",
    "voice_description": "Young female voice, warm and friendly, slight Russian accent",
    "language": "Russian"
  }
}
```

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `text` | string | ✅ | - | Text to synthesize |
| `voice_description` | string | ✅ | - | Natural language description of desired voice |
| `language` | string | ❌ | "Auto" | Target language |

---

### Common Parameters (All Modes)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `max_tokens` | int | 2048 | Max tokens to generate |
| `temperature` | float | 0.7 | Sampling temperature |
| `top_p` | float | 0.9 | Top-p sampling |
| `top_k` | int | 50 | Top-k sampling |
| `repetition_penalty` | float | 1.05 | Repetition penalty |

---

### Response Format

```json
{
  "audio": "data:audio/wav;base64,...",
  "sample_rate": 24000,
  "duration": 3.5,
  "text": "Привет! Как дела?",
  "language": "Auto",
  "mode": "clone",
  "...mode-specific fields..."
}
```

---

## Python Client Example

```python
import base64
import requests
import time

ENDPOINT = "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID"
API_KEY = "your_api_key"

headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

# Example 1: Voice Clone
with open("reference.wav", "rb") as f:
    ref_audio = base64.b64encode(f.read()).decode()

response = requests.post(f"{ENDPOINT}/run", headers=headers, json={
    "input": {
        "text": "Привет!",
        "ref_audio": ref_audio,
        "ref_text": "This is what I said in the reference"
    }
})

# Example 2: Custom Voice
response = requests.post(f"{ENDPOINT}/run", headers=headers, json={
    "input": {
        "text": "Привет!",
        "speaker": "ono_anna",
        "style": "cheerful"
    }
})

# Example 3: Voice Design  
response = requests.post(f"{ENDPOINT}/run", headers=headers, json={
    "input": {
        "text": "Привет!",
        "voice_description": "Young energetic female, anime-style voice"
    }
})

# Poll for result
job_id = response.json()["id"]
while True:
    status = requests.get(f"{ENDPOINT}/status/{job_id}", headers=headers).json()
    if status["status"] == "COMPLETED":
        audio_b64 = status["output"]["audio"].split(",")[1]
        with open("output.wav", "wb") as f:
            f.write(base64.b64decode(audio_b64))
        break
    elif status["status"] == "FAILED":
        print(status)
        break
    time.sleep(2)
```

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MODEL_SIZE` | `0.6B` | Model size: `0.6B` or `1.7B` |
| `HF_HOME` | `/runpod-volume/huggingface` | HuggingFace cache directory |

---

## Notes

- **First request is slow** (~30-60s) as models download
- **Models load on demand**: Clone/Custom/Design use different models
- **0.6B** works on 16GB+ VRAM, **1.7B** needs 24GB+
- **Clone mode** gives best quality when ref_text matches ref_audio exactly
- **Network volume** recommended to persist models between cold starts
