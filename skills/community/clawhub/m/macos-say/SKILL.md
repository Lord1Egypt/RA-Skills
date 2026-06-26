---
name: say-tts
description: Local text-to-speech using macOS `say` + ffmpeg for Telegram/Matrix voice messages
homepage: https://github.com
metadata:
  {
    "openclaw":
      {
        "emoji": "🎤",
        "requires": { "bins": ["say", "ffmpeg"] },
        "label": "Local TTS via say + ffmpeg"
      }
  }
---

# Say + FFmpeg TTS Pipeline

Use `say` (macOS native TTS) + `ffmpeg` to generate Opus voice messages for Telegram/Matrix.

## Why not just `say`?

- Telegram/Matrix require **Opus** codec voice messages
- `say` outputs AIFF/m4a; must convert to `.ogg` (Opus) before sending
- Telegram accepts: OGG/MP3/M4A as voice — but Opus OGG is the native format

## Workflow

```
say -v "<voice>" -o <tmpdir>/<name>.aiff "<text>"
ffmpeg -i <tmpdir>/<name>.aiff -acodec libopus <tmpdir>/<name>.ogg -y
```

Send with `message` tool:
```json
{
  "action": "send",
  "channel": "telegram",
  "media": "<tmpdir>/<name>.ogg",
  "asVoice": true,
  "target": "<chat_id>"
}
```

## Recommended workspace directory

```
~/.openclaw/workspace/tmp/audio/
```

(Whitelist this path in exec permissions for faster approval)

## Voice selection

Use `say -v '?'` to list available voices. Notable ones:
- `Trinoids` — robotic/electronic voice (popular for bots)
- `Samantha` — warm US female voice
- `Alex` — US male voice
- `Fred` — neutral US male voice
- `Karen` — Australian female voice

Note: pass just the voice **name** (e.g. `"Trinoids"`), not the full `en_US` suffix.

## Example: send a hello voice message

```bash
VOICE="Trinoids"
TEXT="Hello!"
DIR="$HOME/.openclaw/workspace/tmp/audio"
mkdir -p "$DIR"

say -v "$VOICE" -o "$DIR/hello.aiff" "$TEXT"
ffmpeg -i "$DIR/hello.aiff" -acodec libopus "$DIR/hello.ogg" -y

# Then send via message tool with asVoice: true
```

## Format notes

- Input to ffmpeg: AIFF (`.aiff`) works reliably; avoid `.m4a` with `say`
- Output: **Opus in Ogg container** (`libopus` codec) — required for Telegram voice messages
- Telegram `sendVoice` accepts: OGG, MP3, M4A — but native is Opus OGG
- Sample rate: `say` outputs 24kHz AIFF; ffmpeg re-encodes to Opus at 24kHz

## Integration with OpenClaw TTS

OpenClaw's built-in `messages.tts` only supports: ElevenLabs, Microsoft Edge, MiniMax, OpenAI.

This `say+ffmpeg` pipeline is a **workaround** for local-only TTS without API keys or cloud services. It's not auto-triggered by OpenClaw — call it manually via exec + message tool.

## Language Detection → Voice Mapping

When responding to a voice message, detect the language from the STT output (Parakeet auto-detects). Then pick the matching `say` voice using i18n locale codes.

**Finding voices by language:**
```bash
say -v '?' 2>&1 | grep -E "cs_CZ|en_US|de_DE|fr_FR|it_IT|es_ES"
```

**Language → voice selection priority:**
1. Use `<voice> (Premium)` if available
2. Fall back to `<voice> (Enhanced)` if available
3. Fall back to base `<voice>` name
4. Never use a voice that doesn't match the language

| Language | i18n code | Preferred Voice |
|---|---|---|
| Czech | `cs_CZ` | `Zuzana (Premium)` |
| English (US) | `en_US` | `Trinoids` (no Premium/Enhanced available) |
| German | `de_DE` | `Grandma (Premium)` if available |
| French | `fr_FR` | `Grandma (Premium)` if available |
| Spanish | `es_ES` | `Grandma (Premium)` if available |
| Italian | `it_IT` | `Grandma (Premium)` if available |


**Key:** Always use just the **voice name** (e.g. `"Trinoids"`, `"Zuzana"`), not the full locale suffix. The locale suffix in `say -v '?'` output is for grepping/identification only.


**Example workflow:**
```bash
LANG="cs_CZ"
# Find best available voice for this language (Premium > Enhanced > base)
VOICE=$(say -v '?' 2>&1 | grep "$LANG" | head -3 | awk '{print $1}' | sed -n '1p')
say -v "$VOICE" -o reply.aiff "Česká odpověď"
ffmpeg -i reply.aiff -acodec libopus reply.ogg -y
```

## TODOs

- [ ] Detect language from STT transcription and auto-select appropriate `say` voice
- [ ] Explore integrating into OpenClaw via custom TTS provider plugin
- [ ] Investigate if OpenClaw supports post-processing TTS output via a hook
- [ ] Test Matrix channel voice message format compatibility
