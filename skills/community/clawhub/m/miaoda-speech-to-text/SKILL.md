---
name: miaoda-speech-to-text
description: "Use when user needs to convert audio or voice recordings to text. Provides necessary command usage instructions for converting audio to text. Supports multiple languages. 触发词：语音转文字, 音频转文字, 语音识别, speech to text, STT, 转录, 听写, 会议记录转文字, 录音转文字, transcribe, 音频识别, voice to text, 语音转换"
---

# Speech to Text

通过 `miaoda-studio-cli speech-to-text` 将音频文件转换为文字。

## Quick Reference

| 参数 | 说明 | 必需 | 默认值 |
|------|------|------|--------|
| `--file` | 音频文件路径 | 是 | - |
| `--lang` | 语言代码 | 否 | zh |
| `--output, -o` | 输出格式: text/json | 否 | text |

## 支持的语言

| 代码 | 语言 | 代码 | 语言 |
|------|------|------|------|
| `zh` | 中文（默认） | `fr` | 法语 |
| `en` | 英语 | `es` | 西班牙语 |
| `ja` | 日语 | `pt` | 葡萄牙语 |
| `ko` | 韩语 | `id` | 印尼语 |
| `ru` | 俄语 | `ms` | 马来语 |

## 使用示例

```bash
# 中文音频转文字（默认语言）
miaoda-studio-cli speech-to-text --file meeting.mp3

# 英文音频转文字
miaoda-studio-cli speech-to-text --file interview.wav --lang en

# 获取 JSON 格式输出
miaoda-studio-cli speech-to-text --file recording.mp3 --lang zh --output json
```

## 使用场景

| 场景 | 用法 |
|------|------|
| 会议录音转文字 | `miaoda-studio-cli speech-to-text --file meeting.mp3 --lang zh` |
| 外语音频转录 | `miaoda-studio-cli speech-to-text --file audio.mp3 --lang en` |
| 转录后搜索补充资料 | 先 `miaoda-studio-cli speech-to-text` 转录，再用 `miaoda-studio-cli search-summary` 搜索关键内容（见 miaoda-web-search skill） |

## Common Mistakes

| 错误 | 正确做法 |
|------|----------|
| 音频文件超过 10 分钟 | 拆分为更短的音频片段后分别转录 |
| 音频语言与 `--lang` 不匹配 | 确认音频实际语言，指定正确的语言代码 |
| 混合语言音频用单一语言代码 | 以主要语言为准，或按语言段落拆分音频 |
| 需要后续处理但未加 `--output json` | 需要程序处理转录结果时加 `--output json` |
| 命令失败后不检查 | 退出码 `1` 表示失败，检查文件路径和格式后重试 |
