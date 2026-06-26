---
name: minimax-tts
description: Text-to-speech (TTS) generation using MiniMax API. Converts text into natural-sounding speech with support for multiple voices, adjustable speed and pitch, and multiple audio formats (MP3/WAV/PCM). Use when the user wants to convert text to speech, generate voice narration, create audio from scripts, or convert articles/essays into audio.
metadata:
  openclaw:
    emoji: "🔊"
    requires:
      env:
        - MINIMAX_API_KEY
      bins:
        - python3
    primaryEnv: MINIMAX_API_KEY
---

# MiniMax TTS (Text-to-Speech)

> ⚠️ Requires a **MiniMax API Key with TTS/Speech access**
> - **Coding Plan key** (sk-cp-xxx) → **不支持 TTS**，仅限 M2.7 聊天模型
> - **通用 API Key** → 请在 [MiniMax 开放平台](https://platform.minimaxi.com) 确认您的订阅是否包含语音合成
> - **TTS 独立套餐**: 访问 [MiniMax 语音合成产品](https://www.minimaxi.com/models/speech)

Text-to-speech synthesis using MiniMax's speech synthesis API. Supports 40+ languages, multiple voices, adjustable speed/pitch, and various audio formats.

---

## Setup

### 1. Configure API Key

```bash
openclaw config set skills.entries.minimax-tts.apiKey "sk-your-key"
```

Or add to `openclaw.json` skills entries:

```json
{
  "skills": {
    "entries": {
      "minimax-tts": {
        "apiKey": "sk-your-key"
      }
    }
  }
}
```

### 2. Dependencies

```bash
pip install requests
```

---

## Architecture

```
~/.openclaw/workspace/skills/minimax-tts/
├── SKILL.md
├── _meta.json
└── scripts/
    └── minimax_tts.py
```

---

## Usage

### From terminal

```bash
# Basic TTS - text to speech
MINIMAX_API_KEY="sk-your-key" python3 scripts/minimax_tts.py "你好，欢迎使用 MiniMax 语音合成"

# With voice selection
MINIMAX_API_KEY="sk-your-key" python3 scripts/minimax_tts.py "Hello world" --voice female-shaonv

# Adjust speed and pitch
MINIMAX_API_KEY="sk-your-key" python3 scripts/minimax_tts.py "快速播报新闻" --speed 1.5 --pitch 2

# Save to file
MINIMAX_API_KEY="sk-your-key" python3 scripts/minimax_tts.py "输出到文件" --output speech.mp3

# List available voices
MINIMAX_API_KEY="sk-your-key" python3 scripts/minimax_tts.py --list-voices

# Multi-segment (audiobook/podcast with multiple voices)
MINIMAX_API_KEY="sk-your-key" python3 scripts/minimax_tts.py --segments segments.json --output combined.mp3
```

### From code

```python
from minimax_tts import generate_speech

# Basic TTS
result = generate_speech(text="你好世界", voice="female-shaonv", output_path="hello.mp3")

# With options
result = generate_speech(
    text="这是一段测试语音",
    model="speech-2.8-hd",
    voice="female-tianmei",
    speed=1.0,
    pitch=0,
    audio_format="mp3",
    output_path="test.mp3"
)
```

---

## Tool Definition

**Name:** `minimax_tts`

**Input Schema:**
```json
{
  "type": "object",
  "properties": {
    "text": {
      "type": "string",
      "description": "Text to convert to speech (max 10000 chars per request)"
    },
    "model": {
      "type": "string",
      "enum": ["speech-2.8-hd", "speech-2.6-hd", "speech-02-hd"],
      "default": "speech-2.8-hd",
      "description": "TTS model: speech-2.8-hd (recommended, high quality with emotion control), speech-2.6-hd (Coding Plan NOT supported), speech-02-hd (compact HD voice)"
    },
    "voice": {
      "type": "string",
      "default": "female-tianmei",
      "description": "Voice ID: female-tianmei, female-shaonv, female-yujie, female-chengshu, male-qn-qingse, male-qn-jingying, male-qn-badao, male-qn-daxuesheng"
    },
    "speed": {
      "type": "number",
      "default": 1.0,
      "minimum": 0.5,
      "maximum": 2.0,
      "description": "Speech speed, range 0.5-2.0, default 1.0"
    },
    "pitch": {
      "type": "number",
      "default": 0,
      "minimum": -12,
      "maximum": 12,
      "description": "Voice pitch adjustment, range -12 to 12, default 0"
    },
    "audio_format": {
      "type": "string",
      "enum": ["mp3", "wav", "pcm"],
      "default": "mp3",
      "description": "Output audio format"
    },
    "output_path": {
      "type": "string",
      "description": "Save audio to this file path. Default: saved to ~/.openclaw/workspace/tmp/tts_<timestamp>.mp3"
    }
  },
  "required": ["text"]
}
```

**Output:** JSON with success status and audio file path

---

## Common Voice IDs

| voice_id | Description | Gender |
|----------|-------------|--------|
| `female-tianmei` | 甜美女声 | Female |
| `female-shaonv` | 少女音 | Female |
| `female-yujie` | 御姐音色 | Female |
| `female-chengshu` | 成熟女性 | Female |
| `male-qn-qingse` | 青年男声（青涩） | Male |
| `male-qn-jingying` | 青年男声（精英） | Male |
| `male-qn-badao` | 青年男声（霸道） | Male |
| `male-qn-daxuesheng` | 青年大学生 | Male |

---

## Multi-Segment Generation (Audiobooks / Podcasts)

For multi-character content, create a `segments.json` file and use `--segments`:

```bash
python3 scripts/minimax_tts.py --segments segments.json --output combined.mp3
```

### segments.json Format

```json
[
  {
    "text": "Morning sunlight streamed into the room.",
    "voice": "female-tianmei",
    "speed": 1.0
  },
  {
    "text": "Welcome to today's episode.",
    "voice": "male-qn-qingse",
    "speed": 1.0
  }
]
```

---

## Error Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1002 | Rate limit - try again later |
| 1004 | Auth failed - check API Key |
| 1008 | Insufficient balance |
| 1026 | Content violation |
| 2013 | Parameter error |
| 2049 | Invalid API Key |
