# Mambo TTS / 曼波音色 TTS

[中文](#中文) | [English](#english)

---

## English

### Overview

Quick-access TTS preset for lively and energetic Chinese female voice, based on Edge TTS.

### Voice Presets

| Preset | Voice | Pitch | Rate | Use Case |
|--------|-------|-------|------|----------|
| **Mambo** | zh-CN-XiaoyiNeural | +8% | default | Lively, energetic content |
| **Xiaoyi** | zh-CN-XiaoyiNeural | default | +30% | Fast-paced content, news |
| **Xiaoxiao** | zh-CN-XiaoxiaoNeural | default | default | Natural, general purpose |
| **Yunyang** | zh-CN-YunyangNeural | default | +10% | Narration, documentary |

### Quick Start

```bash
cd ~/.openclaw/workspace/skills/mambo-tts/scripts

# Mambo voice
node mambo.js "Your text here"

# Xiaoyi voice (fast-paced)
node xiaoyi.js "Your text here"
```

### Technical Notes

- **Engine**: Microsoft Edge TTS (free, no API key required)
- **Supported Parameters**: pitch, rate, volume
- **Not Supported**: style_tag, intonation (these are Azure SSML features)

### Requirements

- Node.js 18+
- node-edge-tts package (included in edge-tts skill)

---

## 中文

### 概述

快速调用预设音色进行文本转语音，活泼有活力的中文女声。

### 预设音色

| 预设名 | Voice | Pitch | Rate | 适用场景 |
|--------|-------|-------|------|---------|
| **曼波** | zh-CN-XiaoyiNeural | +8% | default | 活泼、有活力的内容 |
| **晓伊** | zh-CN-XiaoyiNeural | default | +30% | 快节奏内容、新闻 |
| **晓晓** | zh-CN-XiaoxiaoNeural | default | default | 自然、通用 |
| **云扬** | zh-CN-YunyangNeural | default | +10% | 旁白、纪录片 |

### 快速使用

```bash
cd ~/.openclaw/workspace/skills/mambo-tts/scripts

# 曼波音色
node mambo.js "你的文本"

# 晓伊音色（快节奏）
node xiaoyi.js "你的文本"
```

### 技术说明

- **底层引擎**：Microsoft Edge TTS（免费、无需 API Key）
- **支持参数**：pitch（音高）、rate（语速）、volume（音量）
- **不支持**：style_tag、intonation（这是 Azure SSML 功能）

### 依赖

- Node.js 18+
- node-edge-tts 包（已在 edge-tts skill 中安装）

---

## License

MIT

## Author

小飞 (Beta) - Human Beta Lab
