---
name: openclaw-mlx-audio
description: Local TTS/STT integration for OpenClaw using mlx-audio - Zero API keys, Zero cloud dependency
author: gandli
version: 0.2.0
metadata:
  openclaw:
    always: false
    emoji: 🎤
    os: [darwin]
    requires:
      bins: [brew, ffmpeg, uv]
triggers:
- "/mlx-tts ..."
- "/mlx-stt ..."
- "TTS ..."
- "STT ..."
- "语音合成 ..."
- "语音转文字 ..."
- "声音克隆 ..."
---

# OpenClaw MLX Audio

本地支持多语言文本转语音 (TTS) 和语音转文本 (STT)，完全在 Apple Silicon 设备上运行，无需云服务，保护数据隐私。

## 功能

- 🗣️ **TTS 文本转语音**: 支持中文、英文等多种语言
- 🎤 **STT 语音转文本**: 高准确率语音识别
- 🎭 **声音克隆**: 使用参考音频克隆声音
- 🔒 **完全本地**: 无需 API Key，数据不出设备

## 安装

```bash
# 安装依赖
brew install ffmpeg uv
uv tool install mlx-audio --prerelease=allow

# 安装插件
cp -r openclaw-mlx-audio ~/.openclaw/extensions/

# 重启 OpenClaw
openclaw gateway restart
```

## 使用

### TTS 命令

```bash
# 状态查询
/ mlx-tts status

# 测试生成
/ mlx-tts test "你好，这是测试语音"

# 模型列表
/ mlx-tts models
```

### STT 命令

```bash
# 状态查询
/ mlx-stt status

# 转录音频
/ mlx-stt transcribe /path/to/audio.wav

# 模型列表
/ mlx-stt models
```

### 工具调用

**TTS**:
```json
{
  "tool": "mlx_tts",
  "parameters": {
    "action": "generate",
    "text": "Hello World",
    "outputPath": "/tmp/speech.mp3"
  }
}
```

**STT**:
```json
{
  "tool": "mlx_stt",
  "parameters": {
    "action": "transcribe",
    "audioPath": "/tmp/audio.wav",
    "language": "zh"
  }
}
```

## 支持模型

### TTS 模型

| 模型 | 语言 | 速度 | 质量 |
|------|------|------|------|
| mlx-community/Kokoro-82M-bf16 | 8+ | ⚡⚡⚡ | Good |
| mlx-community/Qwen3-TTS-12Hz-0.6B-Base-bf16 | ZH/EN/JA/KO | ⚡⚡ | Better |
| mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16 | ZH/EN/JA/KO | ⚡ | Best |

### STT 模型

| 模型 | 语言 | 速度 | 精度 |
|------|------|------|------|
| mlx-community/whisper-large-v3-turbo-asr-fp16 | 99+ | ⚡⚡⚡ | Good |
| mlx-community/Qwen3-ASR-1.7B-8bit | ZH/EN/JA/KO | ⚡⚡ | Better |
| mlx-community/whisper-large-v3 | 99+ | ⚡⚡ | Best |

## 测试

**自动化测试**: 17 项 (100% 通过)
**真人测试**: 11 项 Discord 测试
**总体评分**: ⭐⭐⭐⭐ (3.85/5.0)

运行测试:
```bash
bash test/run_tests.sh
```

## 配置

在 `openclaw.json` 中添加:

```json
{
  "plugins": {
    "allow": ["@openclaw/mlx-audio"],
    "entries": {
      "@openclaw/mlx-audio": {
        "enabled": true,
        "config": {
          "tts": {
            "enabled": true,
            "model": "mlx-community/Qwen3-TTS-12Hz-0.6B-Base-bf16",
            "langCode": "zh"
          },
          "stt": {
            "enabled": true,
            "model": "mlx-community/Qwen3-ASR-1.7B-8bit",
            "language": "zh"
          }
        }
      }
    }
  }
}
```

## 系统要求

- macOS Apple Silicon (M1/M2/M3)
- Node.js 18+
- Python 3.10+
- ffmpeg
- uv

## 链接

- GitHub: https://github.com/gandli/openclaw-mlx-audio
- OpenClaw: https://docs.openclaw.ai
- ClawHub: https://clawhub.ai

## License

MIT
