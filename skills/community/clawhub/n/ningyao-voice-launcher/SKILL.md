---
name: ningyao-voice-launcher
description: Install and configure a local browser-based Chinese voice chat launcher with the Ning Yao persona, including one-click Windows launchers, browser speech I/O, screen awareness, and a safe terminal panel. Use when the user wants a local voice companion, a persona-tuned voice chat setup, or help packaging/deploying the Ning Yao voice launcher.
---

# Ningyao Voice Launcher

Install the bundled launcher into a user-chosen folder, then configure `.env` and run it.

## Workflow

1. Copy `assets/voice-chat-local` into the target folder.
2. Install dependencies with `npm install` in the copied folder.
3. Copy `.env.example` to `.env` and fill in `OPENAI_API_KEY`.
4. Start with `start-voice-chat.cmd` or `start-voice-chat-bg.cmd`.

## Bundled Files

- `assets/voice-chat-local`: Browser voice chat app template.
- `scripts/install-launcher.ps1`: Windows installer/copy helper.

## Windows Install

Run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install-launcher.ps1 -Destination "$env:USERPROFILE\Desktop\ningyao-voice-chat"
```

The installer copies the template, skips `.env`, and can optionally run `npm install`.

## Configuration

Set these in `.env`:

- `OPENAI_API_KEY`: required
- `OPENAI_BASE_URL`: optional API-compatible endpoint
- `OPENAI_MODEL`: text + vision capable model if screen analysis is needed
- `OPENAI_TIMEOUT_MS`: request timeout
- `PORT`: local port
- `SYSTEM_PROMPT`: persona prompt

## Notes

- Prefer Chrome or Edge for browser speech recognition and speech synthesis.
- The terminal panel is intentionally restricted to a small whitelist.
- If screen analysis is enabled, choose a model that supports image input.
