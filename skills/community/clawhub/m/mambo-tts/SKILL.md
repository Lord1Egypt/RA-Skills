---
name: mambo-tts
version: 1.0.0
description: "曼波音色 TTS 快速调用 - 活泼有活力的中文女声预设，基于 Edge TTS (zh-CN-XiaoyiNeural + pitch +8%)"
author: "小飞"
tags: ["tts", "voice", "mambo", "chinese"]
---

# 曼波音色 TTS

## 概述

快速调用预设音色进行文本转语音，无需记忆复杂参数。

## 预设音色

| 预设名 | Voice | Pitch | Rate | 适用场景 |
|--------|-------|-------|------|---------|
| **曼波** | zh-CN-XiaoyiNeural | +8% | default | 活泼、有活力的内容 |
| **晓伊** | zh-CN-XiaoyiNeural | default | +30% | 快节奏内容、新闻 |
| **晓晓** | zh-CN-XiaoxiaoNeural | default | default | 自然、通用 |
| **云扬** | zh-CN-YunyangNeural | default | +10% | 旁白、纪录片 |

## 快速使用

### 方式 1：直接调用脚本

```bash
cd ~/.openclaw/workspace/skills/edge-tts/scripts

# 曼波音色
node tts-converter.js "你的文本" --voice zh-CN-XiaoyiNeural --pitch +8%

# 晓伊音色（快节奏）
node tts-converter.js "你的文本" --voice zh-CN-XiaoyiNeural --rate +30%

# 云扬音色（旁白）
node tts-converter.js "你的文本" --voice zh-CN-YunyangNeural --rate +10%
```

### 方式 2：使用便捷脚本

```bash
cd ~/.openclaw/workspace/skills/mambo-tts/scripts

# 曼波
./mambo.sh "你的文本"

# 晓伊
./xiaoyi.sh "你的文本"

# 云扬
./yunyang.sh "你的文本"
```

## 技术说明

- **底层引擎**：Microsoft Edge TTS（免费、无需 API Key）
- **支持参数**：pitch（音高）、rate（语速）、volume（音量）
- **不支持**：style_tag、intonation（这是 Azure SSML 功能）

## 输出

- 默认格式：MP3
- 默认保存位置：`~/.openclaw/workspace/output/`

## 依赖

- Node.js 18+
- node-edge-tts 包（已在 edge-tts skill 中安装）

## 参考

- [Edge TTS Skill](../edge-tts/SKILL.md)
- [node-edge-tts 文档](../edge-tts/references/node_edge_tts_guide.md)
