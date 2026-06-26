---
name: minimax-feishu-voice
description: Send native Feishu voice bubble messages using MiniMax TTS. Use when user wants to send a voice message as a playable Feishu voice bubble (not MP3 attachment). Triggers on: "send voice message", "voice bubble", "语音气泡", "send audio to Feishu", or when replying with voice is requested. Requires: MiniMax TTS API key in voice_config.json, Feishu channel configured, ffmpeg installed.
---

# Feishu Voice Bubble

Send a native Feishu voice message (playable bubble, not attachment) using MiniMax TTS.

## Setup

### 1. Configure voice_config.json

Create `~/.openclaw/workspace/skills/minimax-feishu-voice/voice_config.json`:

```json
{
  "voice_id": "female-yujie-jingpin",
  "speed": 1.0,
  "vol": 1.0,
  "pitch": 0,
  "api_key": "YOUR_MINIMAX_API_KEY"
}
```

- `api_key`: 你的 MiniMax TTS API Key（必填）
- `voice_id`: 语音ID（见下方列表）
- `speed`/`vol`/`pitch`: 可选参数

### 2. Recommended Voice IDs

完整列表：https://platform.minimaxi.com/docs/faq/system-voice-id

| Voice ID | Name | Notes |
|---|---|---|
| `female-tianmei` | 甜美女性音色 | 甜，温柔，适合撒娇 |
| `female-shaonv` | 少女音色 | 年轻可爱 |
| `female-yujie` | 御姐音色 | 成熟御姐 |
| `female-yujie-jingpin` | 精选御姐音色 | 娇媚型御姐，推荐 |
| `female-chengshu` | 成熟女性音色 | 成熟稳重 |
| `wumei_yujie` | 妩媚御姐 | 娇媚型御姐 |
| `diadia_xuemei` | 嗲嗲学妹 | 撒娇学妹 |
| `qiaopi_mengmei` | 俏皮萌妹 | 俏皮可爱 |
| `tianxin_xiaoling` | 甜心小玲 | 甜心少女 |
| `Korean_SweetGirl` | 韩系甜妹 | 异域风情 |

默认值：`female-yujie-jingpin`

## Quick Use

```bash
python3 ~/.openclaw/workspace/skills/minimax-feishu-voice/scripts/send_feishu_voice.py "<text>" <飞书用户的open_id>
```

## Example

```bash
python3 ~/.openclaw/workspace/skills/minimax-feishu-voice/scripts/send_feishu_voice.py \
  "你好，这是一条语音消息" \
  "<飞书用户的open_id>"
```

## How It Works

1. Reads `api_key` from `voice_config.json`
2. Calls MiniMax TTS API → hex audio → MP3
3. Decodes MP3 → PCM → re-encodes as **opus in OGG container** at **16kHz** (Feishu requirement)
4. Extracts `duration_ms` from WAV header
5. Uploads to Feishu with `file_type=opus` + `duration` param → gets `file_key`
6. Sends `msg_type: "audio"` message with `file_key` → **native voice bubble**

## Prerequisites

- **MiniMax TTS API Key** in `voice_config.json` → `api_key`
- **Feishu channel** configured with `appId` + `appSecret` in `openclaw.json`
- **ffmpeg** installed with `libopus` support

## Notes

- Feishu requires **16kHz** sample rate (not 32kHz or 24kHz)
- Duration (ms) must be included in upload request for bubble display
- User's open_id is available as `sender_id` in message metadata
