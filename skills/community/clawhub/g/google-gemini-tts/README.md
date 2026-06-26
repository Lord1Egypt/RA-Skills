# gemini-tts

ClawHub-ready packaging for a Gemini text-to-speech skill.

Default target: Gemini 3.1 Flash TTS Preview.
Backward compatibility: Gemini 2.5 Flash Preview TTS and Gemini 2.5 Pro Preview TTS still work when passed with `-m`.

## What is in the bundle

- `SKILL.md`: publishable skill definition
- `scripts/gemini_tts.sh`: runnable shell wrapper for the Gemini REST API
- `.clawhubignore`: excludes generated artifacts from the bundle

## Why the new default matters

Gemini 3.1 Flash TTS Preview is the right default now because it combines:

- low-latency speech generation
- stronger naturalness
- expressive audio tags
- multilingual output
- single-speaker and two-speaker generation in one simple workflow

This makes the skill more than a plain narrator. It is good for agents that need controllable voice output, not just generic TTS.

## Prompting nuance

- audio tags like `[short pause]` and `[whisper]` work best inside a structured transcript or a clear instruction block
- a bare tag-heavy prompt without enough framing can return no audio
- practical takeaway: wrap tags in a real narration prompt, not just a pile of modifiers

## Tested prompt patterns that worked

Single speaker:

```text
Say in a spooky voice:
"By the pricking of my thumbs... [short pause]
[whisper] Something wicked this way comes"
```

Multi-speaker:

```text
Make Speaker1 sound tired and bored, and Speaker2 sound excited and happy:

Speaker1: So... [yawn] what's on the agenda today?
Speaker2: You're never going to guess!
```

## What agents can do with this

This model is especially useful when agents need to deliver output with intent.

Examples:

- Voice replies in chat: an agent can answer with a short spoken memo instead of plain text
- Daily briefings: a research agent can turn its morning findings into a narrated update
- Newsletter voice preview: a content agent can turn a written summary into a quick audio rundown
- Social content drafts: a marketing agent can generate spoken hooks, trailers, or teaser clips
- Podcast-style synthesis: two-agent conversations can become clean host and guest audio
- Demo agents: product agents can narrate walkthroughs, onboarding, or feature explanations
- Emotional delivery: agents can add pauses, whispers, excitement, boredom, or emphasis where it helps the message land

The main unlock is controllability. You are not just picking a voice. You are giving the agent delivery instructions.

## Usage examples

Default model:

```bash
scripts/gemini_tts.sh "Hello, welcome to the show!"
```

Pick a voice:

```bash
scripts/gemini_tts.sh -v Puck "This is Puck speaking."
```

Add style guidance:

```bash
scripts/gemini_tts.sh -s "Say in a warm, calm tone:" "Take a deep breath."
```

Use explicit audio tags in the transcript:

```bash
scripts/gemini_tts.sh -o /tmp/tagged.wav 'Say in a spooky voice:
"By the pricking of my thumbs... [short pause]
[whisper] Something wicked this way comes"'
```

Two-speaker audio:

```bash
scripts/gemini_tts.sh --multi "Host:Kore,Guest:Puck" \
  "Host: Welcome to the podcast! Guest: Thanks for having me."
```

Fallback model selection:

```bash
scripts/gemini_tts.sh -m gemini-2.5-pro-preview-tts "Long-form narration example"
```

## Requirements

Declared in `SKILL.md` under `metadata.openclaw.requires` — `GEMINI_API_KEY` (or `GOOGLE_API_KEY` as an alias), plus `curl`, `jq`, `base64`, and `ffmpeg` on the host.

## Suggested publish flow

1. Review `SKILL.md`
2. Confirm the version number
3. Submit the folder through the ClawHub publisher
4. After publish, smoke test with a real API key
