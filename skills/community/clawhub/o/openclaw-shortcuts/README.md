# openclaw-shortcuts

> OpenClaw plugin providing a config-driven `/shortcuts` command with safe placeholder defaults.

**Current version:** `0.1.0`

> **Replaces:** `openclaw-help` (deprecated — name was misleading; plugin never registered `/help` but `/shortcuts`)

---

## What it does

Registers `/shortcuts` in your OpenClaw agent.

Prints:
- Generic placeholder sections by default
- Custom sections injected via local `openclaw.json` config

**Security design:** The repo ships with placeholder-only content. All personal shortcuts, project names, and command mappings live in your local config — never in the repo.

---

## Install

```bash
clawhub install openclaw-shortcuts
```

Or local development:
```bash
openclaw plugins install -l ~/.openclaw/workspace/skills/openclaw-shortcuts
openclaw gateway restart
```

---

## Configure

In `~/.openclaw/openclaw.json` → `plugins.entries.openclaw-shortcuts.config`:

```json5
{
  "enabled": true,
  "includeTips": false,
  "sections": [
    {
      "title": "📁 Projects",
      "lines": [
        "/<project>   - Your project shortcut"
      ]
    },
    {
      "title": "🛠 Tools",
      "lines": [
        "/<command>   - Your custom command"
      ]
    }
  ]
}
```

---

## OPSEC rule

- Never put personal commands, phone numbers, group IDs, tokens, or internal workflows into this repo
- Keep all real shortcuts in local config only

---

## Changelog

### v0.1.0
- Initial release (merged from deprecated `openclaw-help`)
- Registers `/shortcuts` with `requireAuth: false`
- Config-driven sections via `openclaw.json`
- Safe placeholder defaults

---

## License

MIT
