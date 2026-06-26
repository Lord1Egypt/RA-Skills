# MiniMax TTS FeiShu Skill

[English](#english) | [中文](#中文)

---

## English

### Overview

This is an **OpenClaw Skill** for generating natural Chinese speech via MiniMax API and sending audio to Feishu. Features emotion detection, pause markers, and sound effect tags.

### Features

- **Text-to-Speech**: Convert text to natural Chinese speech
- **34+ Chinese Voices**: Built-in voice library with switching support
- **Automatic Emotion Detection**: Detects emotion (happy/sad/angry/surprised/calm) based on text keywords
- **Sound Effect Tags**: Auto-inserts laughter `(laughs)`, gasps `(gasps)`, sighs `(sighs)` etc.
- **Smart Pauses**: Automatically adds pause markers at punctuation (，。？！)
- **Feishu Integration**: Sends generated audio directly to Feishu chat
- **Conversational Trigger**: Users can say "转语音" to convert recent messages to speech

### Requirements

- **MiniMax API Key** — Get from [MiniMax Platform](https://platform.minimaxi.com)
- **Feishu App ID & Secret** — Create a Feishu app at [Feishu Open Platform](https://open.feishu.cn)
- **Feishu User Open ID** — Target user's Open ID for audio delivery
- OpenClaw environment

### Installation

1. Install via ClawHub:
```bash
npx clawhub install minimax-tts-feishu
```

2. Set required environment variables:
```bash
export MINIMAX_API_KEY="your-minimax-api-key"
export FEISHU_APP_ID="your-feishu-app-id"
export FEISHU_APP_SECRET="your-feishu-app-secret"
export FEISHU_USER_OPEN_ID="target-user-open-id"
```

### Quick Start

```bash
# Basic TTS
bash scripts/tts_wrapper.sh tts "要转换的文字"

# With specific voice
bash scripts/tts_wrapper.sh tts "文字内容" "Chinese (Mandarin)_Gentle_Senior"

# Design custom voice
bash scripts/tts_wrapper.sh design "温柔的女性声音" "这是一段试听文本" "要说的内容"

# List available voices
bash scripts/tts_wrapper.sh list

# Update voice catalog
bash scripts/tts_wrapper.sh update
```

### Parameters

| Command | Description |
|---------|-------------|
| `tts <text> [voice_id]` | Convert text to speech and send to Feishu |
| `design <prompt> <preview> <text>` | Design custom voice and generate speech |
| `list` | Show available voice list |
| `update` | Update local voice catalog from API |
| `save <text>` | Save last message for "转语音" trigger |
| `trigger <user_text> <open_id>` | Trigger TTS from chat context |

### Emotion Detection

The system automatically detects emotion based on text keywords:

| Emotion | Keywords |
|---------|----------|
| happy | 开心、高兴、太好了、哈哈、太棒了 |
| sad | 伤心、难过、可惜、算了、唉 |
| angry | 生气、讨厌、哼、气死了 |
| surprised | 惊讶、真的吗、什么、怎么 |
| calm | 平静、淡定、好吧、嗯 |

### Sound Effect Tags

| Tag | Effect |
|-----|--------|
| `(laughs)` | Laughter |
| `(gasps)` | Gasp / surprise |
| `(sighs)` | Sigh |
| `(clear-throat)` | Throat clear |

### ⚠️ Security Warnings

#### 1. API Key Security
- 🔐 You MUST set `MINIMAX_API_KEY`, `FEISHU_APP_ID`, `FEISHU_APP_SECRET` environment variables
- 🔐 Never commit API keys to version control
- 🔐 Use scoped API keys with billing limits when possible

#### 2. Feishu Credentials
- 🔐 Feishu App ID and Secret control bot behavior
- 🔐 `FEISHU_USER_OPEN_ID` determines where audio is sent
- 🔐 Do NOT expose these credentials publicly

#### 3. Network Access
- 🌐 This skill accesses `https://api.minimaxi.com` (MiniMax TTS)
- 🌐 This skill accesses `https://open.feishu.cn` (Feishu API)
- 🌐 Ensure your network allows access to the above domains

#### 4. File Write
- 📁 Voice catalog: `voices/voices-map.md` (configurable via `TTS_VOICES_MAP_PATH`)
- 📁 Audio output: `/tmp/` directory
- 📁 Last message cache: `/tmp/last_miss_m_message.txt`

#### 5. Audio Delivery
- 🔊 Generated audio is sent to the specified `FEISHU_USER_OPEN_ID`
- 🔊 Ensure the target user intends to receive TTS audio

### License

MIT License

---

## 中文

### 概述

这是面向 **OpenClaw** 的 **MiniMax 文字转语音 Skill**。通过 MiniMax API 生成自然中文语音并发送到飞书，支持情绪检测、停顿标记和语气词音效。

### 功能特点

- **文字转语音**：将文本转换为自然中文语音
- **34+ 中文音色**：内置音色库，支持查询和切换
- **自动情绪检测**：根据文本关键词自动判断情绪（开心/悲伤/愤怒/惊讶/平静等）
- **语气词音效**：自动插入笑声、叹气、惊讶等音效标签
- **智能停顿**：在标点处自动添加停顿标记，提升语音自然度
- **飞书集成**：将生成的语音直接发送到飞书聊天窗口
- **对话式触发**：用户说"转语音"可将最近的消息转换为语音

### 环境要求

- **MiniMax API Key** — 从 [MiniMax 开放平台](https://platform.minimaxi.com) 获取
- **飞书应用 App ID 和 Secret** — 在 [飞书开放平台](https://open.feishu.cn) 创建应用
- **飞书用户 Open ID** — 接收语音的目标用户 Open ID
- OpenClaw 环境

### 安装方式

1. 通过 ClawHub 安装：
```bash
npx clawhub install minimax-tts-feishu
```

2. 设置必需的环境变量：
```bash
export MINIMAX_API_KEY="your-minimax-api-key"
export FEISHU_APP_ID="your-feishu-app-id"
export FEISHU_APP_SECRET="your-feishu-app-secret"
export FEISHU_USER_OPEN_ID="target-user-open-id"
```

### 快速开始

```bash
# 基础文字转语音
bash scripts/tts_wrapper.sh tts "要转换的文字"

# 指定音色
bash scripts/tts_wrapper.sh tts "文字内容" "Chinese (Mandarin)_Gentle_Senior"

# 设计自定义音色
bash scripts/tts_wrapper.sh design "温柔的女性声音" "这是一段试听文本" "要说的内容"

# 查询可用音色
bash scripts/tts_wrapper.sh list

# 更新音色目录
bash scripts/tts_wrapper.sh update
```

### 命令说明

| 命令 | 说明 |
|------|------|
| `tts <文字> [音色ID]` | 将文字转换为语音并发送到飞书 |
| `design <描述> <试听文本> <内容>` | 设计自定义音色并生成语音 |
| `list` | 显示可用音色列表 |
| `update` | 从 API 更新本地音色目录 |
| `save <文字>` | 保存最后一条消息（用于"转语音"触发） |
| `trigger <用户消息> <用户OpenID>` | 从对话上下文触发 TTS |

### 情绪检测

系统根据文本关键词自动判断情绪：

| 情绪 | 关键词示例 |
|------|----------|
| happy（开心）| 开心、高兴、太好了、哈哈、太棒了 |
| sad（悲伤）| 伤心、难过、可惜、算了、唉 |
| angry（愤怒）| 生气、讨厌、哼、气死了 |
| surprised（惊讶）| 惊讶、真的吗、什么、怎么 |
| calm（平静）| 平静、淡定、好吧、嗯 |

### 语气词音效

| 标签 | 效果 |
|------|------|
| `(laughs)` | 笑声 |
| `(gasps)` | 倒吸气/惊讶 |
| `(sighs)` | 叹气 |
| `(clear-throat)` | 清嗓子 |

### 停顿标记

文本自动在标点后添加停顿：
- `，` → 0.3秒停顿
- `。？！` → 0.5秒停顿

### ⚠️ 安全风险提示

#### 1. API 密钥安全
- 🔐 **必须设置 `MINIMAX_API_KEY`、`FEISHU_APP_ID`、`FEISHU_APP_SECRET` 环境变量**
- 🔐 请勿将 API 密钥提交到版本控制系统
- 🔐 建议使用有限额的 API Key，定期轮换

#### 2. 飞书凭证安全
- 🔐 飞书 App ID 和 Secret 控制机器人行为
- 🔐 `FEISHU_USER_OPEN_ID` 决定语音发送目标
- 🔐 请勿公开这些凭证

#### 3. 网络访问
- 🌐 本 skill 会访问 `https://api.minimaxi.com`（MiniMax TTS 接口）
- 🌐 本 skill 会访问 `https://open.feishu.cn`（飞书 API）
- 🌐 请确认您的网络环境允许访问上述地址

#### 4. 文件写入
- 📁 音色目录：`voices/voices-map.md`（可通过 `TTS_VOICES_MAP_PATH` 环境变量配置）
- 📁 音频输出：`/tmp/` 目录
- 📁 最后消息缓存：`/tmp/last_miss_m_message.txt`

#### 5. 语音发送
- 🔊 生成的语音会发送到指定的 `FEISHU_USER_OPEN_ID`
- 🔊 请确认目标用户有意接收 TTS 语音

### 开源协议

MIT License
