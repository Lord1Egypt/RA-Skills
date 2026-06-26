---
name: minimax-tts-gyh
description: MiniMax TTS 文字转语音模型，支持 speech-02/speech-01 系列，生成高质量语音。使用 MINIMAX_API_KEY 环境变量。
metadata: {"openclaw":{"emoji":"🎙️","requires":{"bins":["python3"]}}}
---

# MiniMax TTS 文字转语音

使用 MiniMax TTS API 将文本转换为语音。

## 支持的模型

| 模型 | 说明 |
|------|------|
| `speech-02-hd` | 高清语音，情感丰富 |
| `speech-02-turbo` | 高速语音 |
| `speech-01-hd` | 标准高清 |
| `speech-01-turbo` | 标准高速 |

## 前置要求

- Python 3
- `pip3 install requests`
- 设置环境变量 `MINIMAX_API_KEY`

## 使用方法

```bash
# 基本语音生成
python3 {baseDir}/scripts/tts.py --text "你好，欢迎使用MiniMax语音合成" --output hello.mp3

# 指定模型和声音
python3 {baseDir}/scripts/tts.py \
  --model speech-02-hd \
  --text "今天天气真不错" \
  --voice_id female_healthy \
  --output weather.mp3

# 英文语音
python3 {baseDir}/scripts/tts.py \
  --model speech-02-hd \
  --text "Hello, this is a test of MiniMax text to speech" \
  --voice_id male_tianmei \
  --output hello.mp3
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--model` | 模型名称 | `speech-02-hd` |
| `--text` | 要转换的文本 | - |
| `--voice_id` | 声音 ID | `female_tianmei` |
| `--speed` | 语速 (0.5-2.0) | 1.0 |
| `--pitch` | 音调调整 | 0 |
| `--volume` | 音量 (0.5-2.0) | 1.0 |
| `--emotion` | 情感风格 | `neutral` |
| `--language` | 语言 | `auto` |
| `--output` | 输出文件路径 | `output.mp3` |
