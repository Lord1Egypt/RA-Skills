---
name: lark-voice
description: Send voice messages on Lark (Feishu) by converting text to speech. Use when the user asks to send a voice message or reply with voice.
metadata: {
  "openclaw": {
    "requires": {
      "bins": ["ffmpeg"]
    }
  }
}
---

# Lark (Feishu) Voice

Convert text to speech and send as a voice message on Lark (Feishu).

## Requirements

- `ffmpeg` — audio format conversion
- At least one TTS source (skill or built-in tool)

## Usage

### 1. Discover TTS Source

Scan installed skills for names containing `tts`, and check if the OpenClaw built-in `tts` tool is available.

- User specified a TTS source → use it directly
- Not specified, only one available → use it directly
- Not specified, multiple available → ask the user to choose
- None available → use the OpenClaw built-in `tts` tool, and suggest installing a TTS skill for more voice options

### 2. Generate Audio

Call the selected TTS source to generate an audio file in wav/mp3 or other intermediate format, saved to `/tmp/openclaw/`.

### 3. Convert to Opus

Feishu voice messages only support the opus format (OGG container).

```bash
ffmpeg -y -i /tmp/openclaw/input.wav -c:a libopus -b:a 24k -ar 24000 -ac 1 /tmp/openclaw/voice.opus
```

### 4. Send Voice

Use the `message` tool to send. The openclaw-lark plugin automatically detects the `.opus` extension, parses the duration, and delivers it as a `msg_type: audio` voice bubble.

```
message(action=send, media="/tmp/openclaw/voice.opus", message="optional text")
```


