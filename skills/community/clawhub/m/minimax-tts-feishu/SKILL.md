---
name: minimax-tts
description: MiniMax 文字转语音，支持中文音色、自动情绪检测、语气词音效和停顿标记
metadata: {"openclaw": {"homepage": "https://github.com/lixiang92229/lx-minimax-tts-feishu"}}
---

# minimax-tts

MiniMax 文字转语音 Skill，支持中文音色选择、情绪检测、停顿标记。

## 核心功能

### 1. 文字转语音 (tts)

生成语音并发送到飞书，支持自动情绪检测和停顿标记。

```bash
tts_wrapper.sh tts "<文本>" [voice_id] [user_open_id]
```

### 2. 音色设计 (voice_design)

通过描述创建自定义音色。

```bash
tts_wrapper.sh design "<音色描述>" "<试听文本>" "<要说的内容>"
```

### 3. 查询音色列表 (list)

```bash
tts_wrapper.sh list
```

### 4. 更新音色目录 (update)

从 API 获取最新音色并更新本地 voices-map.md。

```bash
tts_wrapper.sh update
```

---

## 交互式语音生成

### 使用方式

在飞书对话中输入 **"转语音"** 即可触发。

- 直接发送：`转语音` → 将我最近一条消息转成语音
- 回复某条消息发送：`转语音` → 将那条消息转成语音

### 支持的触发词

- 转语音
- 转成语音
- 变成语音
- 说一遍
- 语音播放

### 工作原理

1. 用户说"转语音"后，系统从以下来源获取要转换的文字：
   - 被回复的那条消息（如果有）
   - 我最近发送的文字（保存在本地）
2. 对文字进行预处理（情绪检测 + 停顿标记）
3. 调用 MiniMax TTS API 生成语音
4. 将语音消息发送到飞书

---

## 文本预处理功能

### 自动情绪检测

系统会根据文本关键词自动判断情绪，并在 API 参数中使用：

| 情绪 | 关键词示例 |
|------|----------|
| happy | 开心、高兴、太好了、哈哈、太棒了 |
| sad | 伤心、难过、遗憾、可惜、唉 |
| angry | 生气、气死了、讨厌、哼 |
| fearful | 害怕、担心、恐怖 |
| disgusted | 恶心、厌恶 |
| surprised | 惊讶、吃惊、没想到 |
| calm | 平静、淡定、好吧 |

### 停顿标记

文本会自动在标点后插入停顿标记，提升语音自然度：
- `，` → 0.3秒停顿
- `。` → 0.5秒停顿
- `？` → 0.5秒停顿
- `！` → 0.5秒停顿

示例：
- 原文：`真的吗？太好了！哈哈哈！`
- 处理后：`真的吗？<#0.5#>太好了！<#0.5#>哈哈哈！<#0.5#>`
- 情绪：happy

### 手动指定情绪

如需强制指定情绪，可传入 emotion 参数覆盖自动检测。

---

## 环境变量

| 变量 | 说明 |
|------|------|
| `MINIMAX_API_KEY` | MiniMax API Key |
| `FEISHU_APP_ID` | 飞书 App ID |
| `FEISHU_APP_SECRET` | 飞书 App Secret |

---

## 文件结构

```
skills/minimax-tts/
├── SKILL.md
├── index.js
└── scripts/
    ├── tts.py                  # 核心 TTS 功能
    ├── voice_design.py         # 音色设计
    ├── list_voices.py          # 查询音色列表
    ├── update_voices_map.py    # 更新音色目录
    ├── text_preprocessor.py   # 文本预处理（情绪+停顿）
    ├── tts_from_chat.py        # 对话式转语音
    └── tts_wrapper.sh          # 统一入口
```

## 默认音色

**Chinese (Mandarin)_Gentle_Senior（温柔学姐）** - 温柔、知性、略带亲切感的声音
