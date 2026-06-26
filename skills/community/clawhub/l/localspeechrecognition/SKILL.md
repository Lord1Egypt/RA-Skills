---
name: speech-recognition-local
description: 本地语音转文字 / Local Speech-to-Text. 使用 faster-whisper 在本地运行 Whisper 模型，无需 API 费用，完全免费。收到语音消息(.ogg .m4a .mp3)自动触发转录，支持中文/英文/日语/自动检测。| Free local STT/TTS alternative — runs Whisper on your machine, no API costs, auto-transcribes voice messages in seconds.
metadata: {"clawdbot":{"emoji":"🎙️","os":["linux","darwin","win32"]}}
---

# 本地语音识别 / Local Speech Recognition

> 使用 faster-whisper 在本地运行 Whisper 模型，无需任何 API 费用。免费、离线、保护隐私。
> Runs faster-whisper locally — no API keys, no costs, fully offline & private.

---

## 功能特点 / Features

- 🎙️ **全自动转录** — 收到语音消息自动触发，无需手动调用
- 💰 **完全免费** — 无需 API key，无任何费用
- 🔒 **隐私安全** — 所有处理在本地完成，音频不离开你的设备
- 🌐 **多语言支持** — 中文 / 英文 / 日语 / 自动检测
- ⚡ **快速响应** — VAD 静音过滤，模型内存缓存
- 📦 **主流格式** — .ogg .m4a .mp3 .wav

---

## 使用方式 / Usage

收到语音消息后，OpenClaw 自动调用转录脚本并将结果注入对话。

**转录命令 / Command:**
```bash
python3 ~/.openclaw/workspace/skills/speech-recognition-local/scripts/transcribe.py <audio_file> [language]
```

**参数说明 / Parameters:**

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `audio_file` | — | 音频文件路径 / Audio file path |
| `language` | `zh` | 语言：zh / en / ja / auto |

---

## 模型说明 / Model Info

- 默认模型 / Default: `base`（精度与速度平衡）
- 首次使用自动下载 / Auto-download on first use
- VAD 静音过滤已启用 / VAD filtering enabled
- 模型缓存在内存中 / Model cached in memory

---

## 适用场景 / Use Cases

| 场景 / Scenario | 说明 |
|----------------|------|
| 语音消息转文字 | 将微信/飞书/Telegram 语音转为可阅读文本 |
| 会议记录 | 录制音频后快速转录存档 |
| 播客字幕 | 将音频文件批量转为文字稿 |
| 隐私敏感场景 | 不希望音频数据上传第三方 |

---

## 限制 / Limitations

- 支持格式 / Supported: `.ogg` `.m4a` `.mp3` `.wav`
- 文件大小 / Max size: 25MB

---

## 安装前提 / Requirements

- Python 3.8+
- faster-whisper（首次使用自动安装）
