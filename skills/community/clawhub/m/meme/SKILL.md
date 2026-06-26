---
name: senseaudio-voice-meme-maker
description: Create funny voice memes with various styles, effects, and templates. Use when users want to make humorous audio content, voice memes, or entertaining sound clips for social media.
metadata:
  openclaw:
    requires:
      env:
        - SENSEAUDIO_API_KEY
    primaryEnv: SENSEAUDIO_API_KEY
    homepage: https://senseaudio.cn
compatibility:
  required_credentials:
    - name: SENSEAUDIO_API_KEY
      description: API key from https://senseaudio.cn/platform/api-key
      env_var: SENSEAUDIO_API_KEY
---

# SenseAudio Voice Meme Maker

Create hilarious voice memes with preset templates and voice effects powered by the SenseAudio TTS API.

## 简介（中文）

**SenseAudio Voice Meme Maker** 是一个基于 SenseAudio TTS 接口的语音梗图生成工具。通过调节语速（speed）、音调（pitch）和音量（vol）参数，可以快速生成各种搞笑风格的语音片段，适用于社交媒体、短视频配音、表情包制作等场景。

**内置模板：**

| 模板名 | 风格 | 参数特点 |
|--------|------|----------|
| `dramatic_narrator` | 夸张旁白 | 语速慢、音调低沉 |
| `shocked_reaction` | 震惊反应 | 语速快、音调高亢 |
| `robot_voice` | 机器人 | 正常语速、极低音调 |
| `speed_ramble` | 急速碎碎念 | 最快语速 |
| `deep_voice` | 超低音 | 慢速、极低音调 |

**使用前提：** 在 [SenseAudio 控制台](https://senseaudio.cn/platform/api-key) 创建 API Key，并设置环境变量 `SENSEAUDIO_API_KEY`。

---

## Prerequisites

```bash
pip install requests
```

## Workflow

1. Choose a template or define custom `speed` / `pitch` / `vol` values
2. Provide the meme text
3. Call the TTS API — response returns audio as a hex string
4. Decode hex and save to an MP3 file

## Implementation

```python
import os
import requests

API_KEY = os.environ["SENSEAUDIO_API_KEY"]

# Preset meme templates: speed [0.5-2.0], pitch [-12-12], vol [0.01-10]
TEMPLATES = {
    "dramatic_narrator": {"speed": 0.75, "pitch": -3,  "vol": 1.5},
    "shocked_reaction":  {"speed": 1.6,  "pitch": 6,   "vol": 2.0},
    "robot_voice":       {"speed": 1.0,  "pitch": -8,  "vol": 1.0},
    "speed_ramble":      {"speed": 2.0,  "pitch": 2,   "vol": 1.2},
    "deep_voice":        {"speed": 0.8,  "pitch": -10, "vol": 1.5},
}

def make_voice_meme(text, template="dramatic_narrator", voice_id="male_0004_a", output="meme.mp3"):
    settings = TEMPLATES[template]
    payload = {
        "model": "SenseAudio-TTS-1.0",
        "text": text,
        "voice_setting": {
            "voice_id": voice_id,
            "speed": settings["speed"],
            "pitch": settings["pitch"],
            "vol":   settings["vol"],
        },
        "audio_setting": {"format": "mp3", "sample_rate": 32000},
    }
    resp = requests.post(
        "https://api.senseaudio.cn/v1/t2a_v2",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json=payload,
    )
    resp.raise_for_status()
    audio_hex = resp.json()["data"]["audio"]
    with open(output, "wb") as f:
        f.write(bytes.fromhex(audio_hex))
    return output
```

## Usage Examples

```python
# Dramatic narrator meme
make_voice_meme("This is fine.", template="dramatic_narrator", output="fine.mp3")

# Shocked reaction
make_voice_meme("Wait, WHAT?!", template="shocked_reaction", output="shocked.mp3")

# Custom effect (no template)
def make_custom_meme(text, speed=1.0, pitch=0, vol=1.0, voice_id="male_0004_a", output="custom.mp3"):
    payload = {
        "model": "SenseAudio-TTS-1.0",
        "text": text,
        "voice_setting": {"voice_id": voice_id, "speed": speed, "pitch": pitch, "vol": vol},
        "audio_setting": {"format": "mp3", "sample_rate": 32000},
    }
    resp = requests.post(
        "https://api.senseaudio.cn/v1/t2a_v2",
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json=payload,
    )
    resp.raise_for_status()
    with open(output, "wb") as f:
        f.write(bytes.fromhex(resp.json()["data"]["audio"]))
    return output
```

## Tips

- Keep meme text short (under 50 chars) for punchy delivery
- Combine `<break time=300>` pauses in text for comedic timing, e.g. `"Wait... <break time=500> WHAT?!"`
- Browse available `voice_id` values at [SenseAudio Voice List](https://senseaudio.cn/docs/voice_api)
- `pitch` range is `-12` to `12`; values beyond ±8 produce the most exaggerated effects

## Reference

- [SenseAudio TTS API](https://senseaudio.cn/docs/text_to_speech_api)
- [SenseAudio Voice List](https://senseaudio.cn/docs/voice_api)
