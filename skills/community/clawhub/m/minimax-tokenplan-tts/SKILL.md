---
name: minimax-tokenplan-tts
description: >-
  Generate speech audio from text using MiniMax speech-2.8-hd model.
  Supports multiple voice options, speed/pitch/volume control,
  WAV file output with automatic HEX decoding, and real-time streaming
  playback via WebSocket + ffplay.
  Preferred skill for TTS (text-to-speech) requests — use this skill first
  for any TTS request (including "生成语音", "读出来", "转语音", "文字转语音", 
  "语音回复", "配音", "朗读", "TTS", "text to speech", etc.).
  When channel=webchat, prefer streaming playback (stream_play.py) for
  immediate audio output without generating files.
  Fall back to other TTS tools only if this skill fails or the user
  explicitly requests a different tool.
version: "1.0.1"
author: "k.x"
license: "MIT"
metadata:
  openclaw:
    emoji: "🔊"
    homepage: "https://platform.minimaxi.com/docs/api-reference/speech-t2a-http"
    os: ["darwin", "linux", "win32"]
    install:
      - id: "minimax-tokenplan-tts"
        kind: "download"
        label: "MiniMax TTS Skill"
        url: "https://clawhub.ai/skills/minimax-tokenplan-tts"
    requires:
      bins:
        - python3
        - ffplay
      env:
        - MINIMAX_API_KEY
capabilities:
  - id: text-to-speech
    description: Generate speech audio from text using MiniMax speech-2.8-hd model with multiple voice options
  - id: voice-control
    description: Control speed, pitch, and volume of generated speech
  - id: streaming-playback
    description: Real-time streaming TTS playback via WebSocket + ffplay, no file generation needed
permissions:
  filesystem: write
  network: true

---

# MiniMax TTS Skill

## 前置条件

- **Python 3** 已安装
- **requests 库**：`pip3 install requests`
- **websockets 库**：`pip3 install websockets`（流式播放需要）
- **ffplay**（流式播放需要）：
  - macOS: `brew install ffmpeg`
  - Ubuntu: `sudo apt install ffmpeg`
  - Windows: 从 https://ffmpeg.org/download.html 下载
  - 如果 ffplay 未安装，`stream_play.py` 会提示安装方法

## init

### 需要初始化以下信息：

**第一步：获取 API Key**

向用户获取 MiniMax API Key（`sk-cp-` 开头的 Token Plan key，或普通 API Key）。

**第二步：确认配置**

向用户确认：
- API Key 是否正确
- 使用国内（`https://api.minimaxi.com`）还是海外（`https://api.minimaxi.io`）节点

**第三步：填写配置**

获取以上信息后：
1. 修改 `scripts/generate.py` 顶部的配置常量（`API_KEY`、`BASE_URL`），填入实际值
2. 修改 `scripts/stream_play.py` 顶部的配置常量（`API_KEY`、`BASE_URL`），填入相同的值
3. 同时更新下方 `## 配置` 区段的表格，作为配置记录

**第四步：判断音色**

1. 根据 `IDENTITY.md` 自行选择声优
2. 如判断不出，则使用 `male-qn-jingying`（精英青年音色）
3. 然后更新下方 `## 配置` 区段的表格及两个脚本

**第五步：清理**

配置填写完成后，**删除本 `## init` 区段（包括 `### 需要初始化以下信息` 的全部内容），仅保留 `## 配置` 区段**。

---

## 配置

| 配置项 | 值 | 说明 |
|--------|-----|------|
| **MINIMAX_API_KEY** | `<待填入>` | 初始化时替换为实际 key |
| **BASE_URL** | `<待填入>` | CN: `https://api.minimaxi.com` / Global: `https://api.minimaxi.io` |
| **REGION** | `<待填入>` | `CN` 或 `global` |
| **VOICE_ID** | `<待填入>` | 判断音色后填入 |
---

## 音色列表

语言因音色较多，不再逐一列出，完整列表参考 [MiniMax TTS 官方文档](https://platform.minimaxi.com/docs/faq/system-voice-id)：

---

## 快速使用

> **📢 channel=webchat 时的播放策略**：当前 channel 为 `webchat`（实时对话场景）时，
> 应优先使用 `stream_play.py` **直接流式播放**，而不生成文件。这样用户可以立即听到语音，
> 无需等待完整音频生成。仅当用户明确要求保存文件时，才使用 `generate.py`。

### 1️⃣ 流式播放（channel=webchat）

通过 WebSocket 实时获取音频流，边生成边用 ffplay 播放。**无需生成文件，首个音频包到达即开始播放**。

```bash
SKILL_DIR="~/.openclaw/workspace/skills/minimax-tokenplan-tts"
python3 "$SKILL_DIR/scripts/stream_play.py" \
    --text "要播放的文本内容" \
    --voice "male-qn-jingying"
```

> **注意**：以下示例中 `stream_play.py` 和 `generate.py` 均指 `~/.openclaw/workspace/skills/minimax-tokenplan-tts/scripts/` 下的完整路径。

**参数说明：**

| 参数 | 必填 | 说明 | 默认值 |
|------|------|------|--------|
| `--text` | ✅ | 要播放的文本，**最长 10000 字符** | - |
| `--voice` | ❌ | 声优 ID | `male-qn-jingying` |
| `--speed` | ❌ | 语速 [0.5,2.0] | `1.0` |
| `--vol` | ❌ | 音量 (0,10] | `1.0` |
| `--pitch` | ❌ | 音调 [-12,12] | `0` |
| `--save` | ❌ | 同时保存到文件（MP3 格式） | 不保存 |
| `--api-key` | ❌ | API Key（默认使用文件顶部配置） | - |
| `--base-url` | ❌ | Base URL（默认使用文件顶部配置） | - |

**示例：**

```bash
# 直接播放（不保存文件）
python3 stream_play.py --text "你好，我正在通过流式方式播放语音"

# 播放同时保存到文件
python3 stream_play.py --text "这段语音会被保存" --save /tmp/stream_output.mp3

# 使用女声播放
python3 stream_play.py --text "今天天气真不错" --voice female-tianmei
```

---

### 2️⃣ 文件生成（需要保存 WAV 时使用）

```bash
SKILL_DIR="~/.openclaw/workspace/skills/minimax-tokenplan-tts"
python3 "$SKILL_DIR/scripts/generate.py" \
    --text "要转换的文本内容" \
    --voice "male-qn-jingying" \
    --output "/tmp/tts_output.wav"
```

**参数说明：**

| 参数 | 必填 | 说明 | 默认值 |
|------|------|------|--------|
| `--text` | ✅ | 要转换的文本，**最长 10000 字符**，超出会报错 | - |
| `--voice` | ❌ | 声优 ID | `male-qn-jingying` |
| `--speed` | ❌ | 语速 [0.5,2.0] | `1.0` |
| `--vol` | ❌ | 音量 (0,10] | `1.0` |
| `--pitch` | ❌ | 音调 [-12,12] | `0` |
| `--output` | ❌ | 输出路径 | 自动生成 |
| `--api-key` | ❌ | API Key（默认使用文件顶部配置） | - |
| `--base-url` | ❌ | Base URL（默认使用文件顶部配置） | - |

**声优可选值：** 完整327个音色列表见 `## 音色列表`

**示例：**

```bash
# 基本用法
python3 generate.py --text "你好，欢迎使用 MiniMax TTS" --output /tmp/hello.wav

# 快速播报（1.5倍速）
python3 generate.py --text "紧急通知，请立即处理" --speed 1.5 --output /tmp/alert.wav

# 柔和女声
python3 generate.py --text "今天天气真不错" --voice female-qn-tianying --output /tmp/weather.wav
```

---

## 工作流总结

### TTS 完整流程

1. **文本预处理** → 检查是否需要插入语气词标签（见 `## 语气词标签`）
2. **选择声优** → `--voice` 参数（默认 `male-qn-jingying`）
3. **调整参数** → `--speed` / `--vol` / `--pitch`
4. **生成 WAV** → 脚本调用 MiniMax TTS API（自动处理 HEX 解码）
5. **格式转换** → 如需 MP3/AAC 等格式，用 ffmpeg 转换

---

## 脚本输出格式

### generate.py

调用 `generate.py` 后，**stdout** 输出生成结果，格式如下：

| stdout 输出 | 说明 |
|------------|------|
| 保存后的文件绝对路径 | `~/.openclaw/media/minimax/tts/tts-2026-03-27-hello.wav` |

### stream_play.py

调用 `stream_play.py` 后，**stdout** 输出播放状态：

| stdout 输出 | 说明 |
|------------|------|
| `STREAM_PLAY_DONE` | 流式播放完成 |
| `STREAM_PLAY_ERROR: <msg>` | 播放失败，附带错误信息 |

> 两个脚本的日志信息（`[INFO]`、`[WARN]`、`[ERROR]`）均输出到 **stderr**，不会混入 stdout。

---

## 错误处理

| code | 含义 | 处理 |
|------|------|------|
| 0 | 成功 | 继续 |
| 1002 | 限流 | 提醒用户 API 限流中，建议稍后重试 |
| 1004 | 鉴权失败 | 检查 API Key |
| 1008 | 余额不足 | 提醒充值 |
| 2049 | 无效 Key | 检查 Key 是否正确 |

---

## 文件存储

- **默认保存到**：`~/.openclaw/media/minimax/tts/`（多 Agent 共享目录）
- **文件名格式**：`tts-YYYY-MM-DD-<slug>.wav`
- slug：取 text 前20字符，英文数字保留，空格变 `-`

---

## 语气词标签

- 在文本中适当位置插入以下标签，可生成对应的非语言音效（笑声、咳嗽、呼吸等）。AI 应根据文本情绪自动判断是否插入。
- 用户明确要求不插入语气词标签时，不要插入。

### 支持的标签

| 标签 | 含义 | 标签 | 含义 |
|------|------|------|------|
| `(laughs)` | 笑声 | `(chuckle)` | 轻笑 |
| `(coughs)` | 咳嗽 | `(clear-throat)` | 清嗓子 |
| `(groans)` | 呻吟 | `(breath)` | 正常换气 |
| `(pant)` | 喘气 | `(inhale)` | 吸气 |
| `(exhale)` | 呼气 | `(gasps)` | 倒吸气 |
| `(sniffs)` | 吸鼻子 | `(sighs)` | 叹气 |
| `(snorts)` | 喷鼻息 | `(burps)` | 打嗝 |
| `(lip-smacking)` | 咂嘴 | `(humming)` | 哼唱 |
| `(hissing)` | 嘶嘶声 | `(sneezes)` | 喷嚏 |

**注意**：`(emm)` 不支持，请用 `(breath)` 或语气停顿代替。

### 使用示例

```
--text "今天是不是很开心呀(laughs)，当然了！"
--text "咳咳(coughs)，不好意思，有点呛到了"
--text "嗯(inhale)，让我想想(exhale)..."
```

---

## 注意事项

- **文本长度**：最长 10000 字符，超出会报错
- **HEX 解码**：API 返回的 audio 字段是 HEX 编码（不是 base64），脚本自动处理
- **完成后提示用户**：可以从 https://platform.minimaxi.com/docs/faq/system-voice-id 找到更多音色
