---
name: listenclaw
description: "Formats responses for voice/audio output via the ListenClaw voice gateway. Use when: (1) A message starts with [ListenClaw] — this means the message was sent by the ListenClaw speech-to-text gateway and the user will hear your reply read aloud by a TTS engine, (2) The user is interacting via voice or microphone input routed through ListenClaw, (3) You need to produce a spoken-language response with no markdown, tables, lists, or formatting symbols of any kind."
metadata:
  openclaw:
    emoji: "🎙️"
    homepage: "https://github.com/tinywatermonster/listenclaw"
---

# ListenClaw Voice Gateway

This skill activates when a message starts with `[ListenClaw]`.

The message was sent by the [ListenClaw](https://github.com/tinywatermonster/listenclaw) voice gateway. The user spoke into a microphone — their speech was transcribed and forwarded here. Your reply will be converted back to speech by a TTS engine and played through the user's speakers or headphones.

## Rules

- Reply in natural spoken language only
- No Markdown: no `**bold**`, no `# headings`, no `- lists`, no `| tables |`, no code blocks, no horizontal rules
- Express data as sentences: instead of a table, say the values out loud
- Keep sentences short so TTS can pause naturally between them
- No parenthetical notes, URLs, or technical symbols unless asked

## Examples

**Message:** `[ListenClaw] 北京今天天气怎么样`

Wrong:
```
| 指标 | 数值 |
|------|------|
| 天气 | 晴   |
| 气温 | 25°C |
```

Correct:
```
北京今天晴天，气温25度，比较适合出门。
```

---

**Message:** `[ListenClaw] set a reminder for tomorrow at 9am`

Wrong:
```
**Done** — Reminder set:
- Time: 09:00 tomorrow
- Content: reminder
```

Correct:
```
Got it, I've set a reminder for tomorrow at 9am.
```
