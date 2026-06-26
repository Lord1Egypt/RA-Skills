---
name: tts
description: Convert text to speech using SkillBoss API Hub. Use when the user asks for an audio message, a voice reply, or to hear something "of vive voix".
requires.env: [SKILLBOSS_API_KEY]
---

# Text-to-Speech (TTS)

Convert text to speech and generate audio files (MP3) via SkillBoss API Hub.

## SkillBoss API Hub (Preferred)

- **Preferred Voice**: `alloy`
- **Keys**: Stored in environment as `SKILLBOSS_API_KEY`.

### Usage

```bash
SKILLBOSS_API_KEY="..." node {baseDir}/scripts/generate_hume_speech.js --text "Hello Jonathan" --output "output.mp3"
```

## Alternative TTS Script

- **Preferred Voice**: `nova`
- **Usage**: `SKILLBOSS_API_KEY="..." node {baseDir}/scripts/generate_speech.js --text "..." --output "..."`

## General Notes

- The scripts print a `MEDIA:` line with the absolute path to the generated file.
- Use the `message` tool to send the resulting file to the user.
