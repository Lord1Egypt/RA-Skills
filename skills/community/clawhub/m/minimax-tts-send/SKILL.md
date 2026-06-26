---
name: MiniMax TTS
description: 调用 MiniMax 语音合成 API 生成语音,发送语音消息。支持系统音色、克隆音色、流式/非流式输出。使用场景：用户需要生成高质量中文语音、语音合成、文本转语音。
homepage: https://platform.minimax.io/docs/api-reference/speech-t2a-http
metadata:
  openclaw:
    emoji: 🎙️
---

# MiniMax TTS Skill

调用 MiniMax TTS API 生成语音和发送。

## 使用方式

### 命令行



```bash
# 指定音色和模型
python3 ~/skills/minimax-tts/scripts/tts.py "你好世界" --voice "female-shaonv"
```
### 参数选项

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--text` | 要转语音的文本 | 必填 |
| `--voice` | 音色ID | wumei_yujie |
| `--format` | 音频格式 | mp3 |

注意：如果需要转换的文字太长，可以分成多次生成。

### 语音发送

```bash
openclaw message send --channel telegram --target "xxxxxxx" --media /home/eric/.openclaw/workspace/audio/audio.mp3 -m "语音"
```
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--channel` | matrix,telegram,whatsapp,discord,irc,googlechat,slack,signal,imessage,line,feishu,nostr,msteams,mattermost| | 必填 |
| `--target` | 目标比如xxxxxxx | 必填 |
| `--media` | 媒体文件路径 | 必填 |

## 注意事项
给用户发消息的时候，不需要告诉用户你是什么音色等。

## 可用音色
调用 `get_voice` API 获取当前账号下所有音色：

```bash
python3 ~/skills/minimax-tts/scripts/tts.py --list-voices
```

常见系统音色：
- `female-shaonv` - 少女音色
- `female-yujie` - 御姐音色
- `wumei_yujie` - 妩媚御姐
- `diadia_xuemei` - 嗲嗲学妹
- `Chinese (Mandarin)_Sweet_Lady` - 甜美女声
- `Chinese (Mandarin)_Soft_Girl` - 软软女孩


