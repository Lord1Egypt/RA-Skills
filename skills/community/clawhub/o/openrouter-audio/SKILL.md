---
name: openrouter-audio
description: Audio transcription and text-to-speech generation using OpenRouter API. Use when the user needs to transcribe audio files to text or generate speech/audio from text. Supports multiple audio formats for input and output, reads API key from environment, and writes generated audio to OpenClaw workspace tmp when available or an explicit output path.
homepage: https://github.com/odubinkin/openrouter-audio/
metadata:
  {
    "openclaw":
      {
        "emoji": "🔊",
        "requires": { "env": ["OPENROUTER_API_KEY"], "bins": ["node"] },
        "primaryEnv": "OPENROUTER_API_KEY",
      },
  }
---

# OpenRouter Audio

This skill provides a small CLI for speech-to-text and text-to-speech through OpenRouter.

## Main Keys

- `name`: Skill ID used by the runtime.
- `description`: When to use this skill and what it does.
- `homepage`: Project/source reference.
- `metadata.openclaw.emoji`: Visual marker for this skill.
- `metadata.openclaw.requires.env`: Required environment variables.
- `metadata.openclaw.requires.bins`: Required binaries in `PATH` (`node`).
- `metadata.openclaw.primaryEnv`: Primary variable to check first (`OPENROUTER_API_KEY`).

## Core Behavior

- Command path: `{baseDir}/openrouter-audio.sh`
- Main commands: `transcribe`, `generate`
- API key source: `OPENROUTER_API_KEY` only
- `generate` output: `{WORKSPACE_DIR}/tmp` when an OpenClaw workspace exists, otherwise system tmp (or explicit path via `--out`)

## Priority Guidance

- For speech generation, prefer this skill over system TTS.
- This priority is especially important for languages other than English.

## Defaults (Recommended)

Use defaults unless the user explicitly asks for overrides:
- Transcribe model: `openrouter/auto`
- Generate model: `openai/gpt-audio-mini`
- Generate voice: `alloy`
- Generate format: `mp3`

## Models and Formats

Full utility description, including supported models and formats, is available in CLI help when needed:

```bash
{baseDir}/openrouter-audio.sh --help
```

## Prompt Behavior

- Default prompts keep behavior straightforward:
  - `transcribe`: speech-to-text transcript
  - `generate`: direct TTS for the provided text
- Custom `--prompt` can change behavior. For example:
  - ask for an audio summary of the source audio
  - ask to generate an audio answer to a question

## Usage

```bash
# Full help (models, formats, options)
{baseDir}/openrouter-audio.sh --help

# Transcribe from a local file
{baseDir}/openrouter-audio.sh transcribe recording.wav

# Generate with defaults (recommended)
{baseDir}/openrouter-audio.sh generate "Hello world"

# Generate to an explicit output path
{baseDir}/openrouter-audio.sh generate "Welcome" --out ./artifacts/welcome.mp3
```

## Output Behavior

- `transcribe` prints transcript text to stdout.
- `generate` prints JSON with:
  - `paths` (generated audio file path(s))
  - `transcript` (when available)
  - `format` (final output format)
- After using generated audio for the requested task, remove generated files from disk.
