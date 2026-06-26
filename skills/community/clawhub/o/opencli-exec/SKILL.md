---
name: opencli-exec
description: Deprecated compatibility alias for the canonical `opencli` skill. Use only when an older note, memory, or prompt still refers to `opencli-exec`; then immediately follow the canonical `opencli` skill at `/Users/ShiXin/.openclaw/skills/opencli/SKILL.md`.
---

# opencli-exec

`opencli-exec` is kept only as a backward-compatible alias.

The canonical skill is now:

```bash
/Users/ShiXin/.openclaw/skills/opencli/SKILL.md
```

Use the canonical wrapper:

```bash
/Users/ShiXin/.openclaw/skills/opencli/scripts/opencli.sh <args...>
```

## Why this alias exists

- older workspace memory and prompts still mention `opencli-exec`
- the active skill name going forward should be `opencli`

## Minimum routing rules

- for tweet IDs or status URLs, use `twitter thread`, not `twitter search`
- `twitter search` syntax is `opencli twitter search <query>`
- there is no `twitter id` subcommand
- use `list -f json` as the current command source of truth

## References

See:

- `/Users/ShiXin/.openclaw/skills/opencli/SKILL.md`
- `/Users/ShiXin/.openclaw/skills/opencli/references/commands.md`
