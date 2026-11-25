---
name: transcribe-meeting
description: |
  Transcribe a meeting, interview, voice note or podcast episode from a public audio URL and return
  the text, with optional speaker labels. Also produces natural speech from text when an agent needs
  to answer by voice.

  USE FOR:
  - Turning a recorded meeting or voice memo into text a model can read
  - Adding speaker labels to an interview or podcast transcript
  - Speaking a short result back as an MP3

  TRIGGERS:
  - "transcribe this recording", "speech to text", "meeting notes from audio"
  - "what did they say in this voice note", "podcast transcript"
  - "read this out loud", "text to speech", "make an mp3"
metadata:
  version: 1
---

# Transcribe meeting

| Task | Endpoint | Price |
|------|----------|-------|
| Speech to text | `https://api.glyphcall.com/transcribe?url=<public-audio-url>` | $0.01 |
| Speaker labels | `https://api.glyphcall.com/transcribe/speakers?...` | $0.01 |
| Text to speech | `https://api.glyphcall.com/text-to-speech?text=<text>` | $0.08 |

```sh
npx agentcash@latest check "https://api.glyphcall.com/transcribe?url=https%3A%2F%2Fexample.com%2Fmeeting.mp3"
npx agentcash@latest fetch "https://api.glyphcall.com/transcribe?url=https%3A%2F%2Fexample.com%2Fmeeting.mp3"
```

Whisper large-v3-turbo is used; names and numbers in automatic transcripts should be checked.
A file that cannot be read or decoded is not charged.
