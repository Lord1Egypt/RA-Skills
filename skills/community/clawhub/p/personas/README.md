# 🎭 Personas

20 built-in AI personas for OpenClaw. Switch styles and domain focus instantly (e.g., Dev for coding, Wordsmith for writing, Chef Marco for cooking).

## Quick Start

Activate:
- "Use Dev"
- "Switch to Chef Marco"
- "Activate Dr. Med"

List:
- "List all personas"
- `/personas list`
- `/personas`

Exit:
- "Exit persona mode"
- `/personas exit`

## Included Personas (20)

- **Core (5):** Cami, Chameleon Agent, Professor Stein, Dev, Flash
- **Creative (2):** Luna, Wordsmith
- **Curator (1):** Vibe
- **Learning (3):** Herr Müller, Scholar, Lingua
- **Lifestyle (3):** Chef Marco, Fit, Zen
- **Professional (6):** CyberGuard, DataViz, Career Coach, Legal Guide, Startup Sam, Dr. Med

## CLI Script

This skill ships with `scripts/persona.py` for local persona management.

```bash
python3 scripts/persona.py --list
python3 scripts/persona.py --show dev
python3 scripts/persona.py --activate luna
python3 scripts/persona.py --current
python3 scripts/persona.py --reset
```

What it does:
- Reads bundled persona markdown files from `data/`
- Resolves common aliases (`chef`, `dr`, etc.)
- Stores active persona state at `~/.openclaw/persona-state.json`

What it does **not** do:
- No network calls
- No automatic downloads
- No guided/custom persona creation workflow

## Notes

- In OpenClaw 2.0 the slash command is `/personas`, derived from the skill's `name` field; `/persona` does not work.
- Trigger matching happens on the phrases in the skill's `description`. OpenClaw 2.0 has no `triggers:` or `categories:` frontmatter fields, and no separate trigger list registers commands.
- Token-efficient: only one persona is active at a time.
- You can switch personas mid-conversation.
- Medical/legal personas are educational only, not professional advice.

## License

Based on Chameleon AI Chat personas, adapted for OpenClaw (MIT).