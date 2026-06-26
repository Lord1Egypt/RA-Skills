---
name: pi-speaker
description: Play TTS or audio on the Raspberry Pi (or gateway host) default speaker. Use when the user asks for an announcement, alarm, news summary, or "say X on the Pi speaker" and the gateway runs on a Pi (or host with local audio).
metadata:
  {
    "openclaw":
      {
        "emoji": "🔊",
        "requires": { "anyBins": ["paplay", "pw-play"] },
      },
  }
---

# Pi speaker (local audio output)

Play text-to-speech or an audio file on the **gateway host default audio output**. Typical use: OpenClaw gateway on a Raspberry Pi with a Bluetooth speaker set as default sink; you ask for an announcement, alarm, or news summary and want to hear it on that speaker.

## When to use

- User asks to "play X on the Pi speaker," "announce X," "alarm at ... with message Y," or "give me a news summary and play it on the speaker."
- Gateway is running on the Pi (or another host with local audio); default sink is already set (e.g. Bluetooth speaker). See [Raspberry Pi audio](/platforms/raspberry-pi-audio) for setup.

## Quick procedure (do this in two tool calls)

There is **no** `openclaw skill pi-speaker` CLI. Use **tts** then **exec** only.

1. Call the **tts** tool with the announcement text. Keep announcement text short (e.g. one sentence) to avoid long TTS generation and request timeouts.
2. From the tool result, get the audio file path (e.g. `details.audioPath` or content like `MEDIA:/path/to/file`). Strip any `MEDIA:` prefix to get the real path on the host.
3. Call the **exec** tool with exactly one of: `pw-play <path>`, `paplay <path>`, or `$HOME/bin/openclaw-speaker-play.sh <path>`. Do not invent a CLI like `openclaw skill pi-speaker --text "..."`; there is no such command.

Only after exec returns success (exit 0), tell the user the phrase was played on the Pi speaker.

## How to do it (details)

Same as Quick procedure above. Generate audio with **tts**, then run **exec** with `pw-play <path>`, `paplay <path>`, or `$HOME/bin/openclaw-speaker-play.sh <path>`. Do not skip the exec step. If exec fails, report the error and do not claim that audio played.

## Notes

- The audio file is created on the gateway host; playback must run on that same host (bash tool without sandbox, or elevated).
- If playback fails, suggest checking: default sink is set (e.g. `pactl info` or `wpctl status`), gateway runs as a user with an audio session, and Bluetooth speaker is connected.
- After generating audio with the tts tool, **always** run the bash tool to play that file on the host (e.g. `pw-play /path/to/audio` or `$HOME/bin/openclaw-speaker-play.sh /path/to/audio`). Do not send the audio to the user in the conversation.
- Do not tell the user that audio was played until you have actually called the bash/exec tool with pw-play (or the script) and received a successful result.
- Example: after TTS returns path `/tmp/openclaw/tts-9vdLan/voice-1772897021460.mp3`, run: `pw-play /tmp/openclaw/tts-9vdLan/voice-1772897021460.mp3` via the bash tool.
