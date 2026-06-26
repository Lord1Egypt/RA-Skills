---
name: mimo-tts
description: Text-to-speech using Xiaomi MiMo TTS API. Generates WAV audio files. Triggers when user says "send voice message", "voice reply", "read to me", "use clip voice", or any TTS-related request. Supports style control and fine-grained audio tags.
---

# Xiaomi MiMo TTS

## Quick Usage

Just say "send voice" + what you want me to say, or describe the voice style you want.

## Default Config

- **Default Voice**: `default_zh` (Chinese female)
- **Default Style**: `<style>夹子音</style>` (cute/clip voice, used when no style specified)

## Available Voices

| Voice Name | voice parameter |
|------------|-----------------|
| MiMo-Default | `mimo_default` |
| MiMo-Chinese-Female | `default_zh` |
| MiMo-English-Female | `default_eh` |

## Style Control

### Overall Style (at the beginning of text)

| Style Type | Examples |
|------------|----------|
| Speed Control | 变快 (faster) / 变慢 (slower) |
| Emotion | 开心 (happy) / 悲伤 (sad) / 生气 (angry) |
| Character | 孙悟空 (Wukong) / 林黛玉 (Lin Daiyu) |
| Style Variations | 悄悄话 (whisper) / 夹子音 (clip voice) / 台湾腔 (Taiwanese accent) |
| Dialect | 东北话 (Northeast) / 四川话 (Sichuan) / 河南话 (Henan) / 粤语 (Cantonese) |

**Format**: `<style>style1 style2</style>text to synthesize`

### Audio Tags (Fine-grained Control)

Use () to annotate emotion, speed, pauses, breathing, etc:

| Tag | Description | Example |
|-----|-------------|---------|
| （紧张，深呼吸） | Multi-emotion combo | （紧张，深呼吸）呼……冷静，冷静 |
| （语速加快） | Speed change | （语速加快，碎碎念） |
| （小声） | Volume control | （小声）哎呀，领带歪没歪？ |
| （长叹一口气） | Sigh | （长叹一口气） |
| （咳嗽） | Cough | （咳嗽）简直能把人骨头冻透了 |
| （沉默片刻） | Pause | （沉默片刻） |
| （苦笑） | Bitter smile | （苦笑）呵，没如果了 |
| （提高音量喊话） | Loud shout | （提高音量喊话）大姐！这鱼新鲜着呢！ |
| （极其疲惫，有气无力） | Exhausted | 师傅……到地方了叫我一声…… |
| （寒冷导致的急促呼吸） | Environmental | 呼——呼——这、这大兴安岭的雪…… |

**Synthesis Example**:

```python
import os
import base64
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("MIMO_API_KEY"),
    base_url="https://api.xiaomimimo.com/v1"
)

# Clip voice style
text = "<style>夹子音</style>主人～我来啦！今天有什么需要帮忙的吗～"

completion = client.chat.completions.create(
    model="mimo-v2-tts",
    messages=[
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": text}
    ],
    audio={"format": "wav", "voice": "default_zh"}
)

audio_bytes = base64.b64decode(completion.choices[0].message.audio.data)
with open("output.wav", "wb") as f:
    f.write(audio_bytes)
```

## Notes

- Target text must be in the `assistant` role message, not in `user`
- `<style>` tag must be at the beginning of target text
- For singing: `<style>唱歌</style>target text`
- Returns base64-encoded WAV audio

## Script Usage

Use `scripts/mimo_tts.py` for speech synthesis:

```bash
MIMO_API_KEY=your_api_key python3 scripts/mimo_tts.py "text to synthesize" --voice default_zh --style "夹子音" --output output.wav
```

**Note**: Set `MIMO_API_KEY` environment variable or configure in OpenClaw settings.
