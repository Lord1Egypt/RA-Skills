---
name: minimax-feishu-music
description: Generate music using MiniMax music-2.6 or music-cover API and send as Feishu audio attachment. Use when user wants to generate and send a song or music clip to Feishu. Triggers on: "生成音乐", "唱首歌", "唱给我听", "send music", "generate song", "music generation", "翻唱".
---

# MiniMax Music Generation

Generate music using MiniMax `music-2.6` (text-to-music) or `music-cover` (cover/lyrics-swap) model and send as Feishu MP3 attachment.

## Two Generation Modes

### 1. Text-to-Music (`music-2.6`) — 从零生成
根据 prompt + lyrics 全新生成歌曲。

### 2. Cover (`music-cover`) — 保留旋律换歌词
上传参考音频，保留原曲旋律和结构，只换歌词内容。适合：修正歌词、保留原版风格。

## Setup

### Configure music_config.json

Create `~/.openclaw/workspace/skills/minimax-feishu-music/music_config.json`:

```json
{
  "api_key": "YOUR_MINIMAX_API_KEY"
}
```

## Lyrics Structure Tags

`lyrics` 使用 `\n` 分隔每行，支持以下结构标签：

| 标签 | 含义 | 作用 |
|------|------|------|
| `[Intro]` | 前奏 | 歌曲开头，引出主题 |
| `[Verse]` | 主歌 | 叙事部分，讲述故事 |
| `[Pre Chorus]` | 预副歌 | 主歌到副歌的过渡 |
| `[Chorus]` | 副歌 | 高潮部分，旋律最突出 |
| `[Interlude]` | 间奏 | 歌曲中间的纯音乐过渡 |
| `[Bridge]` | 桥段 | 打破重复，增加层次 |
| `[Outro]` | 尾奏 | 歌曲结尾渐弱结束 |
| `[Post Chorus]` | 后副歌 | 主歌后的副歌变体 |
| `[Transition]` | 转接 | 段落间的过渡 |
| `[Break]` | 停顿 | 突然的静默，制造戏剧效果 |
| `[Hook]` | 记忆点 | 最抓耳的旋律/歌词 |
| `[Build Up]` | 渐强 | 逐渐积累能量推向高潮 |
| `[Inst]` | 纯音乐 | instrumental，无人声 |
| `[Solo]` | 独奏 | 乐器solo段落 |

## Song Structure

歌曲结构由歌词内容和情感节奏决定，不按固定类型选择。根据以下判断：

- **叙事性强的歌词**（讲故事）→ 多用 `[Verse]` + `[Chorus]`
- **情绪递进强烈** → 加入 `[Pre Chorus]` `[Build Up]` `[Break]`
- **有器乐展示需求** → 加入 `[Interlude]` `[Solo]`
- **情感冲击大** → 加入 `[Hook]` `[Bridge]` `[Post Chorus]`
- **自然结束** → 结尾用 `[Outro]`；突然打断 → `[Break]`

用户说"完整版"时，默认使用包含全部标签的完整结构，但可根据歌词内容适当增删标签，以最适合歌曲为准。

## Quick Use

### 从零生成（music-2.6）

```bash
python3 ~/.openclaw/workspace/skills/minimax-feishu-music/skill-scripts/send_feishu_music.py \
  --prompt "<音乐风格描述>" \
  --lyrics "<歌词内容>" \
  --title "<文件名.mp3>" \
  <飞书用户的open_id>
```

### 翻唱模式（music-cover）— 保留旋律换歌词

```bash
python3 ~/.openclaw/workspace/skills/minimax-feishu-music/skill-scripts/send_feishu_music.py \
  --cover "<参考音频文件路径>" \
  --prompt "<目标音乐风格描述>" \
  --lyrics "<新歌词内容>" \
  --title "<文件名.mp3>" \
  <飞书用户的open_id>
```

**翻唱示例：**

```bash
python3 ~/.openclaw/workspace/skills/minimax-feishu-music/skill-scripts/send_feishu_music.py \
  --cover "/Users/ray/.openclaw/workspace/songs/original_song.mp3" \
  --prompt "轻柔抒情流行，温柔女声，慢节奏" \
  --lyrics "[Intro]
(Ooh-ooh)
(Yeah)
[Verse]
黄昏的咖啡店门口
风铃轻轻摇晃
你从远处走来
Smiling face, so beautiful
[Pre Chorus]
心跳突然加速
想说的话在嘴边
[Chorus]
风吹过街角
带走了沉默
你是我最想留住的温度
Be with you, always
[Outro]
就这样一直唱下去
唱到我们都老去" \
  --title "cover_song.mp3" \
  "<open_id>"
```

## API Parameters

| 参数 | 说明 |
|------|------|
| `model` | `music-2.6` 或 `music-cover` |
| `prompt` | 音乐风格描述（cover 模式必填，10-300字符） |
| `lyrics` | 歌词，必须包含 `\n` 分隔，标签首字母大写 |
| `--cover` | 参考音频文件路径（仅 cover 模式，脚本自动处理 base64） |
| `audio_setting.format` | 固定为 `mp3` |
| `audio_setting.sample_rate` | 44100 |
| `audio_setting.bitrate` | 256000 |
