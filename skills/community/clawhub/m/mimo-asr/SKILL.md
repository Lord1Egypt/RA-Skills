---
name: mimo-asr
description: 小米 MiMo-V2.5-ASR 语音识别技能。通过 Gradio API 调用，将音频转录为文字，支持中英文自动检测和显式指定。无需本地模型，无需 API Key。当用户请求语音转文字、音频转录、提取对话内容时使用。
---

# MiMo-V2.5-ASR 语音识别 / Speech Recognition (中文/English)

> 通过小米官方 Gradio 免费 API 调用语音识别模型，**无需本地模型、无需 API Key**。
> Transcribe audio via Xiaomi's free public Gradio API — **no local model, no API key needed**.

## 为什么选这个？/ Why This One?

比起安装 4GB 本地模型 + `mimo-audio` 包，这个版本：
- ✅ 零依赖（只需要 `requests`）
- ✅ 零配置（不需要下载任何东西）
- ✅ 免费无限调用
- ✅ 支持中文/英文/自动检测
- ❌ 需要网络（音频传云端处理）

## 快速开始 / Quick Start

```bash
# 安装唯一依赖 / Install the only dependency
pip install requests

# 自动语言检测 / Auto language detection
python scripts/mimo_asr_api.py recording.wav

# 指定中文 / Specify Chinese
python scripts/mimo_asr_api.py speech.mp3 --language zh

# 指定英文 / Specify English
python scripts/mimo_asr_api.py lecture.wav --language en

# 输出到文件 / Output to file
python scripts/mimo_asr_api.py meeting.wav --output transcript.txt
```

## 参数 / Parameters

| 参数 | 说明 | 默认值 |
|---|---|---|
| `audio` | 音频文件路径（wav/mp3/m4a 等） | 必填 |
| `--language` | 语言：`auto`（自动）、`zh`（中文）、`en`（英文） | `auto` |
| `--output` | 输出文本文件路径（可选） | 打印到终端 |

## 示例 / Examples

```bash
# 🪟 Windows
python scripts/mimo_asr_api.py C:\Users\abc15\Desktop\录音.wav --language zh --output output.txt

# 🍎 macOS / 🐧 Linux
python scripts/mimo_asr_api.py ~/Desktop/meeting.mp3 --language auto
```

## API 内部原理 / How It Works

该脚本通过 Gradio API 调用 HuggingFace 上的小米官方空间：
The script calls Xiaomi's official HuggingFace space via the Gradio API:

```
https://xiaomimimo-mimo-v2-5-asr.hf.space
```

步骤 / Steps:
1. **上传音频** → `/gradio_api/upload`
2. **启动推理** → `/gradio_api/call/infer`（传音频 URL + 语言标签）
3. **轮询结果** → 获取转录文本

## 支持的文件格式 / Supported Formats

WAV、MP3、M4A、FLAC、OGG 等主流音频格式。
WAV, MP3, M4A, FLAC, OGG and common audio formats.

## 注意事项 / Notes

- 大文件处理时间较长 / Large files take longer
- 需网络连接 / Internet connection required
- 不需要 MIMO API Key / No MIMO_API_KEY needed
- 免费使用 / Free to use
