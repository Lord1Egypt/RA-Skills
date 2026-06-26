---
name: google-gemini-tts
description: "Generate spoken audio from text using Google's Gemini TTS models (default is Gemini 3.1 Flash TTS Preview, with fallback to Gemini 2.5 Flash/Pro preview TTS). Use when an agent needs to convert text to speech, produce voice replies, narrate briefings or newsletters, create podcast-style two-speaker conversations, generate audio with expressive style control (whispers, pauses, accents, emotion), or output WAV files for voice-enabled workflows. Supports 30 prebuilt voices, 70+ languages, single and multi-speaker modes, and natural-language style prompts. Requires a GEMINI_API_KEY from Google AI Studio (the script also accepts GOOGLE_API_KEY as an alternative name for the same key)."
version: 1.0.3
author: Shubham Saboo
compatibility: Requires curl, jq, base64, ffmpeg, and a GEMINI_API_KEY from Google AI Studio. Preview model names may change as Google promotes them to GA.
metadata:
  openclaw:
    emoji: "🔊"
    homepage: https://ai.google.dev/gemini-api/docs/speech-generation
    requires:
      env:
        - GEMINI_API_KEY
      bins:
        - curl
        - jq
        - base64
        - ffmpeg
    primaryEnv: GEMINI_API_KEY
---

# Gemini TTS

Generate speech audio from text using Gemini TTS models. The default is Gemini 3.1 Flash TTS Preview, and the script still supports Gemini 2.5 preview TTS models when you pass `-m`.

## What this skill does

- Single-speaker text to speech
- Two-speaker podcast-style audio
- Style control with natural language prompts
- WAV output that can be sent directly in chat or used in apps

## Files

- `scripts/gemini_tts.sh`: CLI wrapper around the Gemini REST API

## Quick start

```bash
# Show all options
scripts/gemini_tts.sh --help

# Single speaker, default voice (Kore)
scripts/gemini_tts.sh "Hello, welcome to the show!"

# Pick a voice
scripts/gemini_tts.sh -v Puck "This is Puck speaking."

# With style control
scripts/gemini_tts.sh -s "Say in a warm, calm tone:" "Take a deep breath."

# Save to a specific file
scripts/gemini_tts.sh -o /tmp/greeting.wav "Hey there!"

# Multi-speaker conversation
scripts/gemini_tts.sh --multi "Host:Kore,Guest:Puck" \
  "Host: Welcome to the podcast! Guest: Thanks for having me."
```

The script prints the output WAV file path.

## Models

| Model | Best for |
|---|---|
| `gemini-3.1-flash-tts-preview` (default) | Best default now: low-latency, natural output, expressive narration |
| `gemini-2.5-flash-preview-tts` | Backward-compatible fast preview model |
| `gemini-2.5-pro-preview-tts` | Long-form narration and higher-end creative work |

Current note: Gemini 3.1 Flash TTS Preview is live and should be the default path for this skill. Gemini 2.5 preview TTS models remain useful as compatibility fallbacks.

> **Preview model note:** `gemini-3.1-flash-tts-preview` is a preview model. If Google renames or retires it, pass `-m gemini-2.5-flash-preview-tts` as a fallback, or check the [current model list](https://ai.google.dev/gemini-api/docs/models).

Switch model examples:

```bash
scripts/gemini_tts.sh -m gemini-2.5-pro-preview-tts "Your text here"
scripts/gemini_tts.sh -m gemini-2.5-flash-preview-tts "Your text here"
```

## Voices

Available prebuilt voices:

`Zephyr`, `Puck`, `Charon`, `Kore`, `Fenrir`, `Leda`, `Orus`, `Aoede`, `Callirrhoe`, `Autonoe`, `Enceladus`, `Iapetus`, `Umbriel`, `Algieba`, `Despina`, `Erinome`, `Gacrux`, `Pulcherrima`, `Achird`, `Zubenelgenubi`, `Vindemiatrix`, `Sadachbia`, `Sadaltager`, `Sulafat`, `Laomedeia`, `Achernar`, `Schedar`, `Rasalgethi`, `Nashira`, `Enif`

The same 30-voice library is shared between `gemini-3.1-flash-tts-preview` and the `gemini-2.5-flash-preview-tts` / `gemini-2.5-pro-preview-tts` fallbacks, so a voice you pick for the default model will still work if you drop back to a fallback via `-m`.

## Style control

Gemini 3.1 Flash TTS reads plain transcripts naturally, but gives you two complementary ways to steer the delivery when you want more control.

### Inline audio tags

Drop bracketed directions into the transcript. They modify what follows, can appear anywhere, and can stack or repeat across a single script:

```text
[excitedly] Massive update today — [whispers] but keep it between us. [laughs]
```

Tags are open-ended; anything in `[ ]` is treated as a direction to the model. A useful starting set:

- **Emotion** — `[excitedly]`, `[bored]`, `[reluctantly]`, `[amazed]`, `[curious]`, `[mischievously]`, `[panicked]`, `[sarcastic]`, `[serious]`, `[tired]`, `[trembling]`
- **Pace and volume** — `[very fast]`, `[very slowly]`, `[asmr]`, `[deep and loud shouting]`, `[whispers]`
- **Non-verbal** — `[gasp]`, `[giggles]`, `[sighs]`, `[snorts]`, `[cough]`, `[laughs]`, `[crying]`
- **Character / style** — `[like dracula]`, `[like a dog]`, `[singing]`, `[sarcastically, one painfully slow word at a time]`

### Structured context prompt

For longer pieces where you want a consistent persona, prepend an `AUDIO PROFILE / SCENE / DIRECTOR'S NOTES / TRANSCRIPT` block. The four headers are load-bearing — the model uses them to separate performance context from the script it should actually speak:

```text
# AUDIO PROFILE: Jaz, London morning-show radio DJ

## THE SCENE: 10 PM, neon-lit studio, "ON AIR" tally blazing.
Jaz is bouncing on their heels, hands on the faders, infectious energy.

### DIRECTOR'S NOTES
Style: vocal smile always audible; punchy consonants; elongated vowels on excitement words.
Accent: Brixton, London.
Pace: energetic, bouncing cadence, no dead air.

#### TRANSCRIPT
[excitedly] Yes, massive vibes in the studio! [shouting] Turn it up!
```

Inline tags inside `#### TRANSCRIPT` override the baseline direction when you want a specific beat.

### Tips

- Keep the script and direction coherent — the speaker, what is said, and how it is said should agree.
- Don't overspecify. Give the model space to fill gaps; it reads better.
- A simple preamble ("Say cheerfully: ...") still works for quick one-offs, but inline tags give you per-phrase control and structured prompts give you persona consistency.

Full prompting reference: [Gemini speech-generation docs](https://ai.google.dev/gemini-api/docs/speech-generation).

## Multi-speaker

Up to 2 speakers. Use `--multi "Name1:Voice1,Name2:Voice2"` and make sure the speaker names in the text match.

## Supported languages

70+ languages are supported, including Arabic, Bengali, Chinese, English, French, German, Hindi, Indonesian, Italian, Japanese, Korean, Portuguese, Russian, Spanish, Turkish, Ukrainian, Urdu, Vietnamese, and many more. See the [Gemini speech-generation docs](https://ai.google.dev/gemini-api/docs/speech-generation) for the full locale list.

## Limitations

- Audio output only
- Maximum 2 speakers in multi-speaker mode
- Preview model names may change
- No SSML support
- No custom voice cloning

## Verification

Basic smoke test once your API key is set:

```bash
export GEMINI_API_KEY=your_key_here   # GOOGLE_API_KEY is also accepted
scripts/gemini_tts.sh -o /tmp/gemini-test.wav "This is a Gemini TTS smoke test."
file /tmp/gemini-test.wav
```

Expected result: a playable WAV file is created (24 kHz mono, 16-bit PCM WAV).
