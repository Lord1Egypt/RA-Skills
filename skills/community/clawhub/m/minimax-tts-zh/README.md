# MiniMax TTS 中文版（交互向导）

使用 MiniMax `speech-2.8-hd` 模型将文字转换为 MP3 语音文件，支持交互向导引导用户完成配置。

## 安装

### 方式一：通过 ClawHub 安装（推荐）

```bash
openclaw skills install minimax-tts-zh
```

### 方式二：手动安装

```bash
cp -r minimax-tts-cn ~/.openclaw/workspace/skills/minimax-tts-zh
```

安装完成后运行 `openclaw skills`，看到 `MiniMax TTS` 状态为 `✓ ready` 即成功。

## 必要配置：防止 AI 用喇叭播放

openclaw 默认的 AGENTS.md 有"Voice Storytelling"指引，会导致 AI 收到"文字转语音"指令时用 `say` 命令通过电脑喇叭朗读，而不是生成 MP3 文件。

**需要为每个聊天 workspace 的 TOOLS.md 加以下内容。**

找到对应 workspace 目录（如 `~/.openclaw/workspace/weixin-xxx/TOOLS.md`），在文件顶部添加：

```markdown
## TTS / 文字转语音

**当用户说"文字转语音"、"TTS"、"生成语音"、"生成音频"、"转MP3"等词时，严格执行以下规则：**

- **唯一允许的方法**：调用 MiniMax TTS skill 的 `tts` 命令
- **以下方式全部禁止**，违反即为错误：
  - 禁止 `say` 命令（无论是否加 `-o` 输出到文件）
  - 禁止 `ffmpeg` 合成音频
  - 禁止任何系统 TTS / macOS 原生语音
  - 禁止直接调用任何 TTS API（必须通过 skill 的 tts 命令）
- 必须按 MiniMax TTS SKILL.md 的交互流程走，包括询问音色选择
- AGENTS.md 的 Voice Storytelling 指引对此场景无效
```

如果有多个聊天 workspace（微信、Telegram 等），每个都需要加。

## 使用

安装并配置完成后，在聊天里说"文字转语音"，AI 会按以下流程引导：

1. **检查 Token** — 首次使用会提示输入 MiniMax API Token，自动保存，后续无需重复输入
2. **输入文字** — 如初始消息已含文字内容则自动提取，跳过此步
3. **选择音色** — 从 6 种音色中选择
4. **生成发送** — 生成 MP3 文件发给用户（Telegram 以语音消息形式发送，微信以文件形式发送）

## 可用音色

| 编号 | ID | 名称 |
|------|----|------|
| 1 | `female-tianmei-jingpin` | 甜美女声 ★精品 |
| 2 | `female-yujie-jingpin` | 御姐 ★精品 |
| 3 | `male-qn-badao-jingpin` | 霸道总裁 ★精品 |
| 4 | `Chinese (Mandarin)_News_Anchor` | 新闻女声 |
| 5 | `Chinese (Mandarin)_Male_Announcer` | 新闻男声 |
| 6 | `Chinese (Mandarin)_Radio_Host` | 电台男声 |

## 获取 MiniMax API Token

前往 [minimaxi.com](https://minimaxi.com) 开放平台注册并创建 API Key。

> **注意**：Token 保存在 skill 目录的 `server/.env` 中，同一 openclaw 实例下的所有 agent 共用同一个 Token。

## 文件说明

```
minimax-tts-zh/
├── SKILL.md        # skill 描述、触发条件、交互流程
├── server/
│   └── index.py   # 核心逻辑（API 调用、Token 管理）
└── README.md       # 本文件
```

Token 保存在 `server/.env`（首次使用后自动创建），不包含在安装包内。
