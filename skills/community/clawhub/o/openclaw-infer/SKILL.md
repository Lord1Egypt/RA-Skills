---
name: openclaw-infer
description: Use the OpenClaw `infer` CLI for provider-backed model, image, audio transcription, TTS, video, web-search, and embedding tasks.
homepage: https://docs.openclaw.ai/cli/infer
metadata:
  {
    "openclaw":
      {
        "emoji": "🦞",
        "requires": { "bins": ["openclaw"] },
        "install":
          [
            {
              "id": "node-openclaw",
              "kind": "node",
              "package": "openclaw",
              "bins": ["openclaw"],
              "label": "Install OpenClaw CLI (npm)",
            },
          ],
      },
  }
---

# OpenClaw Infer

Prefer `openclaw infer ...` as the first-party CLI for inference work.

Use `--json` when output should be machine-readable or piped into another step. The normal local path does not require the gateway to be running.

## Setup

Requires binary: `openclaw` on `PATH`.

Install if missing:

```bash
npm install -g openclaw
```

Quick verification:

```bash
openclaw infer model providers --json
```

If working from a local OpenClaw checkout instead of a global install, use that checkout's built `openclaw` CLI.

## Core commands

- Run text/model calls:
  - `openclaw infer model run --prompt "Reply with exactly: smoke-ok" --json`
  - `openclaw infer model providers --json`
- Generate or inspect images:
  - `openclaw infer image generate --prompt "friendly lobster illustration" --json`
  - `openclaw infer image describe --file ./photo.jpg --json`
- Transcribe audio:
  - `openclaw infer audio transcribe --file ./memo.m4a --language en --prompt "Focus on names and action items" --json`
- Synthesize speech:
  - `openclaw infer tts convert --text "hello from openclaw" --output ./hello.mp3 --json`
  - `openclaw infer tts providers --json`
- Generate or inspect video:
  - `openclaw infer video generate --prompt "cinematic sunset over the ocean" --json`
  - `openclaw infer video describe --file ./clip.mp4 --json`
- Search the web:
  - `openclaw infer web search --query "OpenClaw docs" --json`
  - `openclaw infer web providers --json`
- Create embeddings:
  - `openclaw infer embedding create --text "friendly lobster" --json`
  - `openclaw infer embedding providers --json`

## Selection rules

- Prefer `infer` over older wrapper skills or provider-specific CLIs unless the user explicitly asks for that provider or workflow.
- Prefer explicit `--provider` or `--model provider/model` only when the user asks for a specific backend.
- Keep the command family flat:
  - `infer image ...`
  - `infer audio ...`
  - `infer tts ...`
  - `infer video ...`
  - `infer web ...`
  - `infer embedding ...`
