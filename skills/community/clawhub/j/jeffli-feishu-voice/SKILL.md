---
name: feishu-voice-reply
description: Generate Feishu-native voice replies with a playable pause/resume bar by synthesizing text, converting it with ffmpeg to Ogg/Opus, and sending it as a voice message. Use when the user asks for 语音播放, voice playback, spoken summaries, or any reply that should appear in Feishu as both visible text and a tappable audio player instead of a raw mp3 file.
---

# Feishu Voice Reply

Create Feishu replies that contain both normal text and a real voice bubble/player. Avoid sending raw mp3 files when the goal is in-chat playback.

## Workflow

1. Draft the text reply first.
2. Keep the visible text and the spoken text aligned.
3. Use `scripts/build_feishu_voice.py` to synthesize Chinese speech with Edge TTS and convert it to Ogg/Opus through ffmpeg.
4. Send the text reply normally.
5. Send the generated `.ogg` file with the messaging tool as a voice message:
   - `mimeType: audio/ogg`
   - `asVoice: true`
6. If a message id is available, reply to the triggering message for both the text and the voice.

## Defaults

- Default language: Chinese
- Default voice: `zh-CN-XiaoxiaoNeural`
- Default channel behavior: Feishu text message + Feishu voice message

## Rules

- **语音文件必须存放在 Workspace 下**：使用 `/root/.openclaw/workspace/temp/voice/` 目录，不要用 /tmp。否则飞书只显示文件路径而不是语音播放条。
<<<<<<< HEAD
=======
- **Emoji 自动过滤**：脚本会自动过滤 emoji 字符再合成 TTS，显示的文本保留 emoji，但语音不会朗读 emoji（避免杂音）。无需手动处理。
>>>>>>> 8d2abf78b8490403831aae82052e8e107054b856
- Always show the text reply as well; do not send voice-only unless the user explicitly asks for that.
- Prefer concise spoken text. If the full answer is long, speak a compact summary and keep the full text visible.
- Use this skill specifically for Feishu playback UX. If the user only wants downloadable audio, normal attachments are fine.
- If synthesis succeeds but voice sending fails, tell the user clearly that Feishu voice delivery failed instead of pretending it worked.

## Script

### Build a Feishu-compatible voice file

Run:

```bash
python3 scripts/build_feishu_voice.py \
  --text "今天上海多云，气温十一度。" \
  --out-dir /root/.openclaw/workspace/temp/voice
```

The script prints JSON including:
- `ogg_path`: send this to Feishu as the voice file (必须在 Workspace 下)
- `mp3_path`: intermediate file
- `voice`: selected Edge TTS voice

## Sending pattern

After building the file:

1. Send the visible text reply.
2. Send `ogg_path` with:
   - channel `feishu`
   - `path` = generated `ogg_path`
   - `mimeType` = `audio/ogg`
   - `asVoice` = `true`

## Resource

- `scripts/build_feishu_voice.py`: deterministic synthesis + ffmpeg conversion for Feishu voice playback.
