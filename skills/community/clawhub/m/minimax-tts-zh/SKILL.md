---
name: MiniMax TTS
description: "使用 MiniMax API 将文字转换为 MP3 语音文件。触发词：文字转语音、TTS、生成语音、生成音频、把文字转成语音、文字转MP3、生成MP3。触发后按交互流程引导用户完成 Token 配置、文字输入、音色选择，最终生成 MP3 文件发给用户。严禁使用 say 命令或通过喇叭播放，必须生成 MP3 文件。"
version: 1.2.1
icon: 🔊
metadata:
  clawdbot:
    emoji: 🔊
    requires:
      bins:
        - python3
    install:
      - id: brew-python
        kind: brew
        formula: python3
        bins:
          - python3
        label: Install Python via Homebrew
    commands:
      tts: python3 {baseDir}/server/index.py tts
      voices: python3 {baseDir}/server/index.py voices
      save-token: python3 {baseDir}/server/index.py save-token
---

# 🔊 MiniMax TTS 文字转语音

使用 MiniMax `speech-2.8-hd` 模型将文字转换为 MP3 音频，通过交互向导引导用户完成配置。

## ⚠️ 重要约束

- **必须生成 MP3 文件发给用户**，禁止调用 `say` 命令或通过电脑喇叭播放
- 这是消息平台工具（微信、Telegram 等），输出是文件，不是本地音频播放
- 禁止用 `fetch`/`curl` 直接调用 API，必须通过 `tts` 命令

## 触发条件

用户说以下内容时触发，并**严格按照【交互流程】执行**：

- "文字转语音"、"TTS"、"生成语音"、"生成音频"
- "把文字转成语音"、"把这段话转成音频"
- "文字转MP3"、"生成MP3"

## 交互流程

每步等待用户回复后再进入下一步，不得跳步或一次性问多个问题。

### 第一步：检查 Token

运行 `voices` 命令，根据输出判断：

- Token **已配置** → 跳至第二步
- Token **未配置** → 发送以下消息，等待回复：

  > 请输入你的 MiniMax API Token（在 minimaxi.com 开放平台获取）：

  收到后运行 `save-token --token <token>`，然后进入第二步。

### 第二步：收集文字内容

先检查用户初始消息是否已含文字（如"帮我把'你好世界'转成语音"）：
- 已包含 → 提取文字，跳至第三步
- 未包含 → 发送以下消息，等待回复：

  > 请输入要转换为语音的文字内容：

### 第三步：选择音色

发送以下消息，等待回复：

> 请选择音色：
> 1. 甜美女声（默认）
> 2. 御姐
> 3. 霸道总裁
> 4. 新闻女声
> 5. 新闻男声
> 6. 电台男声

音色 ID 映射：
- 1 → `female-tianmei-jingpin`
- 2 → `female-yujie-jingpin`
- 3 → `male-qn-badao-jingpin`
- 4 → `Chinese (Mandarin)_News_Anchor`
- 5 → `Chinese (Mandarin)_Male_Announcer`
- 6 → `Chinese (Mandarin)_Radio_Host`

用户输入数字或名称均可识别。

### 第四步：生成并发送

运行：
```
tts --text "<文字>" --voice "<voice ID>"
```

命令输出中会有一行以 `FILE:` 开头，例如：
```
成功! 已保存到: /tmp/openclaw/tts_1234567890.mp3 (256 KB)
FILE:/tmp/openclaw/tts_1234567890.mp3
```

从 `FILE:` 开头的行提取绝对路径（去掉 `FILE:` 前缀）。

**⚠️ 发送文件的唯一正确方式：在回复文本中用 `MEDIA:` 前缀，让平台自动发送文件：**

```
🔊 <音色名称> · <文件大小>KB
MEDIA:/tmp/openclaw/tts_1234567890.mp3
```

- `MEDIA:` 这一行必须单独占一行，路径就是 `FILE:` 后面提取的路径
- `MEDIA:` 行会被系统解析并自动以文件/语音发出，不会作为文字显示给用户
- **禁止**用 `<file>` 标签、`sessions_send`、`message` 工具或其他方式，只用 `MEDIA:` 语法
- Telegram 会自动以语音消息形式发送，微信会以文件形式发送

### 异常处理

| 情况 | 处理 |
|------|------|
| Token 无效（401） | 提示重新输入，运行 `save-token` 更新 |
| 音色 ID 不存在 | 提示重新选择，只用列表内的 6 个音色 |
| 文字为空 | 提示重新输入 |

## 命令参考

### `tts`

```
tts --text "文字内容" [--voice female-tianmei-jingpin] [--speed 1.0] [--output /path/to/output.mp3]
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `--text` | ✅ | 要转换的文字 |
| `--voice` | | 音色ID，默认 `female-tianmei-jingpin` |
| `--speed` | | 语速 0.5-2.0，默认 1.0 |
| `--vol` | | 音量 0.1-2.0，默认 1.0 |
| `--pitch` | | 音调 -12~12，默认 0 |
| `--output` | | 输出路径，默认 `/tmp/tts_{timestamp}.mp3` |

### `save-token`

```
save-token --token "your-minimax-api-token"
```

保存 Token 到本地 `server/.env`，下次无需重复输入。

### `voices`

列出可用音色，并显示当前 Token 配置状态。

## 可用音色

| ID | 名称 |
|-----|------|
| `female-tianmei-jingpin` | 甜美女声 ★精品 |
| `female-yujie-jingpin` | 御姐 ★精品 |
| `male-qn-badao-jingpin` | 霸道总裁 ★精品 |
| `Chinese (Mandarin)_News_Anchor` | 新闻女声 |
| `Chinese (Mandarin)_Male_Announcer` | 新闻男声 |
| `Chinese (Mandarin)_Radio_Host` | 电台男声 |

## 工作原理

1. `voices` / `save-token` 管理本地 Token（存于 `server/.env`）
2. `tts` 调用 `https://api.minimaxi.com/v1/t2a_v2`
3. API 返回 hex 编码音频，解码后写入 MP3 文件
4. 将文件路径打印到 stdout，AI 解析路径后调用 `message` 工具（`media=<绝对路径>`）发送给用户
