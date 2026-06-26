---
name: MiniMax TTS Plus
description: |
  MiniMax TTS skill (enhanced). Multi-agent voice support (each agent can select a unique voice written in SOUL.md), native voice message for Telegram (MP3) and Feishu (OGG/Opus).
  Activate when user explicitly requests text-to-speech. Say "文字模式" or "关闭语音" to stop voice generation.
  Note: This skill uses the MiniMax secret key for API authentication. The API endpoint is https://api.minimaxi.com (not platform.minimax.io). See setup section for details.
homepage: https://platform.minimax.io/docs/api-reference/speech-t2a-http
metadata:
  openclaw:
    emoji: 🎙️
    requires:
      bins: [python3, ffmpeg]
      env: [MINIMAX_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_TARGET]
      pip: [requests]
    primaryEnv: MINIMAX_API_KEY
    envHelp:
      MINIMAX_API_KEY:
        required: true
        description: MiniMax API Key (secret key for API authentication)
        howToGet: |
          1. Open https://platform.minimax.io
          2. Register and log in
          3. Get your API Secret Key (Account Management → API Keys)
        url: https://platform.minimax.io
      TELEGRAM_BOT_TOKEN:
        required: false
        description: Telegram Bot Token (from @BotFather) — only needed for sending voice to Telegram. Use --generate-only or direct Python call if you only need audio generation.
      TELEGRAM_TARGET:
        required: false
        description: Telegram chat ID — only needed together with TELEGRAM_BOT_TOKEN
---

# MiniMax TTS Plus

Multi-agent + multi-channel native voice message TTS skill.

## Core Script

All operations go through `tts-xiaoye.sh` (TTS generation + channel delivery).

## Quick Start

```bash
bash tts-xiaoye.sh "Text to speak"
```

## Multi-Channel Usage

| Channel | Command | Format | Notes |
|---------|---------|--------|-------|
| Telegram | `tts-xiaoye.sh "Text"` | MP3 | Direct send, no transcoding |
| Feishu | `tts-xiaoye.sh --feishu "Text"` | OGG/Opus | Auto-transcode to native voice bubble |
| Generate only | `tts-xiaoye.sh --generate-only "Text"` | MP3 | Generate file without sending |

### Send Feishu Native Voice Message (Full Flow)

```bash
OPUS=$(bash tts-xiaoye.sh --feishu "Feishu voice content" 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin)['audio_file'])")
openclaw message send --channel feishu --account personal --target <FeishuUserID> --media "$OPUS"
```

## Multi-Agent Voice Configuration

Each agent can choose a unique voice and write it into their `SOUL.md` Voice Identity section:

```markdown
## Voice Identity
- TTS model: speech-2.8-hd
- TTS voice: Chinese (Mandarin)_Warm_Girl
- TTS script: scripts/tts-xiaoye.sh
```

Recommended voices (verified):
| Voice ID | Style | Use Case |
|----------|-------|----------|
| Chinese (Mandarin)_Warm_Girl | Warm Girl | Personal Assistant |
| female-shaonv | Sweet Girl | Default / General |
| female-tianmei | Sweet Female | Gentle style |
| male-qn-qingse | Youthful Male | Male voice scenario |
| Chinese (Mandarin)_Sweet_Lady | Sweet Lady | Formal场合 |

## List Available Voices

```bash
python3 tts-xiaoye.sh --list-voices
# or directly:
python3 scripts/tts.py --list-voices
```

This calls the MiniMax API and prints all available voices organized by category (System Voices, Cloned Voices, Generated Voices).

## Available Models

| Model | Characteristic |
|-------|---------------|
| speech-2.8-hd | Highest quality (recommended) |
| speech-2.8-turbo | Faster, slightly lower quality |

## Full Parameters

```bash
tts-xiaoye.sh --text "Text" [--voice VoiceID] [--model Model] [--caption Caption]
```

## Technical Notes

- TTS outputs MP3 natively. Telegram sends directly via Bot API `sendVoice` (MP3 supported natively).
- Feishu native voice messages require OGG/Opus format. FFmpeg handles conversion (~25ms per audio, negligible).
- FFmpeg installation: `brew install ffmpeg` (Linuxbrew/macOS) or `apt install ffmpeg` (Linux).

## Setup

1. Copy `setup.txt` to `.env` and fill in your credentials:
```bash
cp skills/minimax-tts-cn/setup.txt skills/minimax-tts-cn/.env
# Then edit .env with your real values
```

2. The script loads credentials from `.env` at runtime — **no hardcoded tokens in scripts**.

**Required env vars:**
| Variable | Required | Description |
|----------|----------|-------------|
| `MINIMAX_API_KEY` | ✅ Yes | MiniMax API secret key (from platform.minimax.io) |
| `TELEGRAM_BOT_TOKEN` | ❌ No | Telegram bot token — only needed for sending |
| `TELEGRAM_TARGET` | ❌ No | Telegram chat ID — only needed together with bot token |

> ⚠️ **Security note:** Credentials are loaded from `.env` only — no tokens are hardcoded in shell scripts. The `.env` file is gitignored and never published.

> 💡 **API endpoint:** The TTS API uses `https://api.minimaxi.com` (MiniMax's official API server), which is separate from the developer portal at `platform.minimax.io`.

---

# MiniMax TTS Plus（多语言增强版）

多 Agent + 多渠道原生语音条增强版 TTS 技能。

## 核心脚本

所有操作通过 `tts-xiaoye.sh` 完成（TTS 生成 + 渠道发送）。

## 快速使用

```bash
bash tts-xiaoye.sh "要转语音的文字"
```

## 多渠道用法

| 渠道 | 命令 | 格式 | 说明 |
|------|------|------|------|
| Telegram | `tts-xiaoye.sh "文字"` | MP3 | 直接发送语音条，无需转码 |
| 飞书 | `tts-xiaoye.sh --feishu "文字"` | OGG/Opus | 自动转码，发原生语音条 |
| 仅生成 | `tts-xiaoye.sh --generate-only "文字"` | MP3 | 只生成文件，不发送 |

### 发送飞书原生语音条（完整流程）

```bash
OPUS=$(bash tts-xiaoye.sh --feishu "飞书语音内容" 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin)['audio_file'])")
openclaw message send --channel feishu --account personal --target <飞书用户ID> --media "$OPUS"
```

## 多 Agent 音色配置

每个 Agent 可以选择不同音色，写入各自的 `SOUL.md` 的 Voice Identity 节即可：

```markdown
## Voice Identity
- TTS model: speech-2.8-hd
- TTS voice: Chinese (Mandarin)_Warm_Girl
- TTS script: scripts/tts-xiaoye.sh
```

推荐音色（已验证）：
| 音色ID | 风格 | 适用场景 |
|--------|------|---------|
| Chinese (Mandarin)_Warm_Girl | 温暖少女 | 个人助理 |
| female-shaonv | 甜美少女 | 默认/通用 |
| female-tianmei | 甜美女性 | 温柔风格 |
| male-qn-qingse | 青涩青年男 | 男声场景 |
| Chinese (Mandarin)_Sweet_Lady | 甜美女声 | 正式场合 |

## 可用模型

| 模型 | 特点 |
|------|------|
| speech-2.8-hd | 最高质量（推荐） |
| speech-2.8-turbo | 快速，质量略低 |

## 完整参数

```bash
tts-xiaoye.sh --text "文字" [--voice 音色ID] [--model 模型] [--caption 文字]
```

## 技术说明

- TTS 原生输出 MP3，Telegram 直接发送（Bot API sendVoice 支持 MP3）
- 飞书原生语音条需要 OGG/Opus 格式，通过 FFmpeg 转换（耗时约 25ms/音频，可忽略）
- FFmpeg 安装方式：
  - macOS/Linuxbrew: `brew install ffmpeg`
  - Ubuntu/Debian: `apt install ffmpeg`
