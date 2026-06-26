---
name: openclaw-shortcuts
description: OpenClaw plugin providing a config-driven /shortcuts command with safe placeholder defaults. Use when you want a /shortcuts command that lists your local commands and project shortcuts without leaking private info to public repos.
---

# openclaw-shortcuts

Registers `/shortcuts` in your OpenClaw agent.

## What it does

- `/shortcuts` → prints configured sections (projects, commands, model switching, etc.)
- Ships with generic placeholder defaults — real shortcuts stay in local config
- `requireAuth: false` — gateway `commands.allowFrom` handles authorization

## Configure

Inject your shortcuts via `openclaw.json`:

```json5
{
  "plugins": {
    "entries": {
      "openclaw-shortcuts": {
        "enabled": true,
        "config": {
          "includeTips": false,
          "sections": [
            {
              "title": "📁 Projects",
              "lines": ["/myproject   - My project shortcut"]
            }
          ]
        }
      }
    }
  }
}
```

## OPSEC

Never commit personal shortcuts to the repo. Local config only.

**Version:** 0.1.0
