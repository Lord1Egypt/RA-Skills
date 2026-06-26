---
name: senseaudio-voice
version: 2.1.0
description: SenseAudio Voice - 语音合成 (TTS) + 语音识别 (ASR)，支持语言自动切换
metadata: {"openclaw":{"emoji":"🎤"}}
tags: [tts, asr, voice, senseaudio, edge, speech, audio, chinese, english, japanese, http]
---

# senseaudio-voice

> **SenseAudio Voice** - 语音合成 (TTS) + 语音识别 (ASR)，完整语音交互能力

基于 SenseAudio HTTP API + Edge TTS 实现，根据语言自动选择最佳方案。

## ✨ 特点

### 🎤 完整语音能力
- **TTS 语音合成** - 文字转语音，支持多声音
- **ASR 语音识别** - 语音转文字，高精度识别
- **HTTP 接口** - 简单可靠，无需复杂依赖
- **语言自动检测** - 中文用 SenseAudio，英语/日语用 Edge TTS

### 🌍 语言支持策略
| 语言 | TTS 方案 | ASR 方案 | 说明 |
|------|---------|---------|------|
| **中文** | SenseAudio | SenseAudio | 需要大陆手机号 + 身份认证，免费使用 |
| **英语** | Edge TTS | SenseAudio | 海外友好，无需认证 |
| **日语** | Edge TTS | SenseAudio | 海外友好，无需认证 |
| **其他** | Edge TTS | SenseAudio | 默认降级方案 |

### 🔧 技术优势
- **简单依赖** - 只需要 `requests` 库
- **WAV 格式** - 系统兼容性好，无需额外解码器
- **智能播放** - 自动检测设备支持的播放器
- **异常处理** - 完整的错误处理和降级方案

## 🚀 快速使用

```bash
# 基础用法（自动检测语言）
python {baseDir}/scripts/tts.py "你好，这是语音测试"
python {baseDir}/scripts/tts.py "Hello, this is a test"
python {baseDir}/scripts/tts.py "こんにちは、テストです"

# 指定声音（仅 SenseAudio）
python {baseDir}/scripts/tts.py --voice male_0004_a "你好呀"

# 指定输出文件
python {baseDir}/scripts/tts.py -o output.wav "语音内容"

# 生成并播放
python {baseDir}/scripts/tts.py --play "宝贝，该写作业啦"

# 强制使用 Edge TTS（英语/日语推荐）
python {baseDir}/scripts/tts.py --engine edge "Hello, how are you?"

# 强制使用 SenseAudio（仅中文）
python {baseDir}/scripts/tts.py --engine senseaudio "你好，今天天气不错"

# 检查系统播放器
python {baseDir}/scripts/tts.py --check-players
```

## 📁 文件存储

**音频文件保存位置**: `{workspace}/audio/YYYY-MM-DD/`

```
/home/wang/.openclaw/agents/kids-study/workspace/audio/
└── 2026-03-14/
    ├── 095221_male0004a_测试完成，文件应该在.mp3
    └── 095158_male0004a_你好，音频文件现在保.mp3
```

- 默认按日期分类存储
- 文件名格式：`HHMMSS_voice_文本前缀.mp3`
- 使用 `-o` 参数可指定自定义路径

## 🎤 可用语音

### SenseAudio 声音（中文）
| 声音 ID | 性别 | 描述 |
|--------|------|------|
| `child_0001_a` | 童声 | ✅ 默认，亲切活泼，适合学习场景 |
| `male_0004_a` | 男 | 温暖男声 |
| `male_0001_a` | 男 | 成熟男声 |
| `female_0001_a` | 女 | 温柔女声 |
| `female_0002_a` | 女 | 活泼女声 |

### Edge TTS 声音（英语/日语）
| 语言 | 声音代码 | 描述 |
|------|---------|------|
| **英语 (en-US)** | `en-US-JennyNeural` | 女声，清晰友好（默认） |
| | `en-US-GuyNeural` | 男声，温暖专业 |
| | `en-US-AriaNeural` | 女声，活泼自然 |
| **日语 (ja-JP)** | `ja-JP-NanamiNeural` | 女声，温柔清晰（默认） |
| | `ja-JP-KeitaNeural` | 男声，成熟稳重 |

## 📋 选项

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `--voice, -v` | 语音 ID | child_0001_a (中文) / en-US-JennyNeural (英语) / ja-JP-NanamiNeural (日语) |
| `--output, -o` | 输出文件 | audio/YYYY-MM-DD/*.wav |
| `--play, -p` | 生成后自动播放 | true |
| `--format` | 音频格式 (wav/mp3) | wav |
| `--speed` | 语速 (0.5-2.0) | 1.0 |
| `--volume` | 音量 (0-10) | 1.0 |
| `--engine, -e` | 引擎 (senseaudio/edge/auto) | auto (自动检测) |
| `--lang, -l` | 语言 (zh/en/ja/auto) | auto (自动检测) |

## 🔧 配置

**SenseAudio API Key**: 从 `~/.openclaw/openclaw.json` 的 `env.SENSE_API_KEY` 读取

**Edge TTS**: 无需 API Key，直接调用 Microsoft Edge 服务

### ⚙️ 使用建议
- **中国大陆用户**：配置 `SENSE_API_KEY`，中文使用 SenseAudio（免费，需手机号 + 身份认证）
- **海外用户**：无需配置，自动使用 Edge TTS（英语/日语支持好）
- **混合场景**：保持 `auto` 模式，根据语言自动选择最佳方案

## 📝 使用示例

### 中文场景（使用 SenseAudio）
```bash
# 默认童声（适合学习场景）
python {baseDir}/scripts/tts.py --play "宝贝，该写作业啦"

# 日常问候
python {baseDir}/scripts/tts.py --play "早上好呀，今天天气不错"

# 切换声音（男声）
python {baseDir}/scripts/tts.py --voice male_0004_a --play "该去上班啦"

# 调节语速
python {baseDir}/scripts/tts.py --speed 1.2 --play "这是快一点的语音"
python {baseDir}/scripts/tts.py --speed 0.8 --play "这是慢一点的语音"
```

### 英语场景（自动使用 Edge TTS）
```bash
# 英语问候（自动检测，使用 Edge TTS）
python {baseDir}/scripts/tts.py --play "Hello! How are you today?"

# 强制使用 Edge TTS
python {baseDir}/scripts/tts.py --engine edge --play "Good morning, everyone!"

# 使用男声
python {baseDir}/scripts/tts.py --voice en-US-GuyNeural --play "Let's start learning!"
```

### 日语场景（自动使用 Edge TTS）
```bash
# 日语问候（自动检测，使用 Edge TTS）
python {baseDir}/scripts/tts.py --play "こんにちは、お元気ですか？"

# 使用男声
python {baseDir}/scripts/tts.py --voice ja-JP-KeitaNeural --play "一緒に勉強しましょう！"
```

### 语言检测
```bash
# 自动检测语言并选择合适的引擎
python {baseDir}/scripts/tts.py --lang auto --play "Hello 你好 こんにちは"
```

## 🔌 API 接口

### SenseAudio（中文）
- **端点**: `POST https://api.senseaudio.cn/v1/t2a_v2`
- **鉴权**: `Authorization: Bearer <API_KEY>`
- **文档**: https://senseaudio.cn/docs/text_to_speech_api
- **限制**: 需要大陆手机号 + 身份认证，免费使用

### Edge TTS（英语/日语）
- **端点**: Microsoft Edge TTS Service
- **鉴权**: 无需 API Key
- **依赖**: `edge-tts` Python 库（可选）或直接 HTTP 调用
- **限制**: 无地区限制，海外友好

## ⚠️ 注意事项

### SenseAudio（中文）
- 需要联网（调用 SenseAudio 服务）
- 依赖 `SENSE_API_KEY` 环境变量或配置文件
- **仅限中国大陆地区**：需要手机号 + 身份认证才能免费使用
- 单次请求最大文本长度：10000 字符

### Edge TTS（英语/日语）
- 需要联网（调用 Microsoft Edge 服务）
- 无需 API Key，无地区限制
- 海外用户推荐使用

### 通用
- 音频播放器：自动检测，推荐安装 `aplay` (ALSA) 或 `paplay` (PulseAudio)
- **语言检测逻辑**：
  - 包含中文字符 → SenseAudio
  - 包含日文字符（假名/汉字）→ Edge TTS
  - 纯拉丁字母 → Edge TTS
  - 混合语言 → 按主要字符类型判断

## 🔧 播放器检测

```bash
# 检查系统支持的播放器
python {baseDir}/scripts/tts.py --check-players
```

**输出示例**:
```
🔊 系统音频播放器检测
============================================================
✅ 找到 2 个可用播放器:

1. ALSA (WAV 原生支持)
   命令：aplay -q
   支持格式：wav

2. PulseAudio
   命令：paplay
   支持格式：wav, mp3, flac, ogg

💡 推荐:
   播放 WAV: ALSA (WAV 原生支持) (优先级最高)
   播放 MP3: PulseAudio
```

**播放流程**:
1. 验证文件存在性和完整性
2. 检测系统可用的播放器
3. 按优先级尝试播放
4. 失败时自动降级到下一个播放器
5. 所有播放器失败时给出详细错误日志和建议
