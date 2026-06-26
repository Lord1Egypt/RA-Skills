# Security And Network

This repo sends generation requests to `api.imastudio.com`.

For local image uploads it uses `imapi.liveme.com` to obtain upload tokens and upload bytes before image generation.

The runtime stores:

- preferences in `~/.openclaw/memory/ima_prefs.json`
- logs in `~/.openclaw/logs/ima_skills/`

These paths are part of the runtime contract and should stay synchronized with `clawhub.json`.
