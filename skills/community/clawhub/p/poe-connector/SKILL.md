---
name: poe-connector
version: 1.1.0
author: dzwalker
description: >
  Access Poe.com AI models by running bash commands. Use when user mentions Poe, wants to use Poe models, or generate media via Poe.
  IMPORTANT: This is a bash-tool skill. You MUST use the bash/shell tool to execute commands. Do NOT use sessions_spawn, do NOT use browser, do NOT try to use Poe as a model provider.
triggers:
  - poe
  - Poe
  - poe.com
  - ask poe
  - use poe
  - via poe
  - poe chat
  - poe image
  - poe video
  - poe audio
  - poe models
repository: https://github.com/dzwalker/poe-connector
license: MIT
dependencies: []
tools:
  - poe_chat
  - poe_media
  - poe_models
metadata: {"clawdbot":{"emoji":"🤖","requires":{"anyBins":["python3","bash"],"config":["skills.entries.poe-connector.env.POE_API_KEY"]},"os":["linux","darwin","win32"]}}
---

# Poe Connector — USE BASH TOOL

**You MUST use the `bash` or `shell` tool to run these commands. No other method works.**

## Commands

Chat with AI:
```bash
bash ~/.openclaw/workspace/skills/poe-connector/poe.sh chat Tell me 10 jokes
```

Generate image:
```bash
bash ~/.openclaw/workspace/skills/poe-connector/poe.sh image A sunset over mountains
```

Generate video:
```bash
bash ~/.openclaw/workspace/skills/poe-connector/poe.sh video A cat playing piano
```

Generate audio:
```bash
bash ~/.openclaw/workspace/skills/poe-connector/poe.sh audio Hello world in a cheerful voice
```

List models:
```bash
bash ~/.openclaw/workspace/skills/poe-connector/poe.sh models
```

Search models:
```bash
bash ~/.openclaw/workspace/skills/poe-connector/poe.sh search claude
```

## Sending generated media (images/video/audio) to the user

After generating an image/video/audio, the script prints a `[MEDIA_SEND_HINT]` line with the local file path.
**You MUST use the `message` tool to deliver the file** — do NOT just paste the URL or embed it in markdown.
Telegram cannot render markdown images (`![alt](url)`); it requires `sendPhoto` / `sendDocument` which the `message` tool handles automatically.

```
message send --media "/path/to/poe_generated_image.png"
```

If `message send` is not available, you can also use the `--to last` flag or specify the channel explicitly.
Always include a short text caption so the user knows what the media is about.

## DO NOT

- Do NOT embed image/media URLs in markdown like `![image](url)` — Telegram will NOT display them
- Do NOT use `sessions_spawn` — it will fail
- Do NOT use browser to visit poe.com — it will fail
- Do NOT set poe as a model provider — it will fail
- Do NOT use any approach other than `bash` tool — only bash works

## Setup (required before first use)

This skill requires a Poe API key. Get one at https://poe.com/api/keys, then add to `~/.openclaw/openclaw.json`:

```json
{ "skills": { "entries": { "poe-connector": { "env": { "POE_API_KEY": "your-key" } } } } }
```

## Notes

- All commands use sensible default models (configured in poe_config.json)
- If you get a POE_API_KEY error, tell the user to run the setup above
- File attachments (--files) are base64-encoded and sent to Poe — do not attach sensitive files unless the user intends to share them with Poe
