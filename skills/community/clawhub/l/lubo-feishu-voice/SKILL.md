---
name: feishu-voice
description: "Send voice messages to Feishu using NoizAI TTS. Use this whenever the user wants you to speak, send a voice message, or reply with audio on Feishu. Wraps noizai-tts + Feishu voice delivery into one reliable workflow."
permissions:
  - network
  - filesystem
metadata: {"openclaw": {"primaryEnv": "NOIZ_API_KEY"}}
---

# feishu-voice — 飞书语音消息技能

让 AI 助手在飞书发送**真正的语音气泡**（不是文件附件），使用 NoizAI 云端 TTS，**免费，无需 API Key**。

## 前置要求

1. **OpenClaw** 已安装并运行
2. **noizai-tts** 技能已安装（底层 TTS 引擎）
3. **Python 3.6+** 可用
4. **飞书** 已配置为消息渠道

### 安装

```bash
# 先装底层依赖
clawhub install noizai-tts

# 再装本技能
clawhub install lubo-feishu-voice
```

---

## 完整使用流程（3 步）

### 第 1 步：生成语音文件

运行 `voice.py`，传入要说的话，生成 `.opus` 音频文件：

```bash
python skills/feishu-voice/scripts/voice.py "你好，这是一条语音消息"
```

**参数说明：**
```
python skills/feishu-voice/scripts/voice.py <文字> [输出路径] [音色ID]
```

| 参数 | 必填 | 说明 |
|------|------|------|
| 文字 | ✅ | 要转成语音的文字内容 |
| 输出路径 | ❌ | 输出的 `.opus` 文件路径（默认自动生成到 `workspace/media/`） |
| 音色ID | ❌ | 声音风格（默认 `b4775100` = 悦悦） |

**示例：**
```bash
# 最简用法 — 自动生成文件
python skills/feishu-voice/scripts/voice.py "今天天气不错"

# 指定输出路径
python skills/feishu-voice/scripts/voice.py "你好" "/tmp/hello.opus"

# 指定音色（婉青）
python skills/feishu-voice/scripts/voice.py "晚安" "/tmp/night.opus" "77e15f2c"
```

**成功后**：脚本会在 stdout 输出生成的文件绝对路径，例如：
```
C:\Users\you\.openclaw\workspace\media\voice_1778253339868.opus
```

**⚠️ 注意**：PowerShell 可能会显示红色错误提示（`[noiz-guest] Using guest mode...`），这是正常的 info 日志被误当成错误，**不影响功能**。只要脚本输出了文件路径，就是成功了。

### 第 2 步：确认文件生成

检查上一步输出的文件确实存在且有内容（> 100 bytes）：
```bash
# 查看文件大小
ls <输出的文件路径>
```

如果文件不存在或大小为 0，说明生成失败，检查：
- Python 是否可用
- noizai-tts 是否已安装
- 文字是否为空

### 第 3 步：发送到飞书

使用 OpenClaw 的 `message` 工具发送。**三个关键参数缺一不可**：

```
action: send
channel: feishu
asVoice: true              ← 必须！否则发成文件附件
contentType: audio/opus    ← 必须！飞书语音要求 opus 格式
filePath: <第1步输出的文件路径>
```

**发送成功后**，飞书端会显示一个**语音气泡**（带播放按钮），用户点击即可播放。

**如果是在当前对话回复**，发送完语音后回复 `NO_REPLY`（避免重复发送文字）。

---

## 可用中文音色（免费 Guest 模式）

| voice_id | 名称 | 性别 | 风格 | 适合场景 |
|---|---|---|---|---|
| `b4775100` | 悦悦｜社交分享 | 女 | 欢快 | 日常对话、分享、闲聊 ← **默认** |
| `77e15f2c` | 婉青｜情绪抚慰 | 女 | 平静 | 安慰、睡前、冥想 |
| `ac09aeb4` | 阿豪｜磁性主持 | 男 | 平静 | 播报、新闻、正式场合 |
| `87cb2405` | 建国｜知识科普 | 男 | 平静 | 知识讲解、教程 |
| `3b9f1e27` | 小明｜科技达人 | 男 | 欢快 | 科技话题、轻松分享 |

---

## 常见问题

### Q: 发出去是文件附件而不是语音气泡？
**A:** 发送时必须设 `asVoice: true` 和 `contentType: audio/opus`。两个都要有。

### Q: 脚本报错 exit code 1 但文件生成了？
**A:** 这是 PowerShell 的 stderr 处理问题。`[noiz-guest]` 日志走 stderr，PowerShell 把它当错误。看 stdout 有没有输出文件路径就行。

### Q: 想用英文音色？
**A:** 可以，NoizAI guest 模式也有英文音色（见 noizai-tts 文档）。直接传英文文字就行。

### Q: 文字太长怎么办？
**A:** 建议 200 字以内效果最好。超长文字也能生成，但质量可能下降。可以分段发送多条语音。

### Q: 不想用飞书，能用其他渠道吗？
**A:** 核心是生成 opus 文件，发送逻辑根据渠道不同调整。Telegram/Discord 等也支持语音，但发送参数不同。

---

## 依赖关系

```
feishu-voice (本技能)
  └── noizai-tts (TTS 引擎，必须先装)
        └── Python 3.6+
        └── requests (pip)
```

## 安全说明

- Guest 模式不发送任何身份信息
- 文字内容会上传到 `https://noiz.ai/v1/` 进行语音合成
- 本地只保存生成的音频文件
- 不修改音频文件以外的任何文件
