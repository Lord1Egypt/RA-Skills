# Memory Template - Minecraft

Create `~/minecraft/memory.md` with this structure only if the user wants persistence:

```markdown
# Minecraft Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | paused | never_ask

## Context
- default edition and platform
- typical world type: survival, creative, Realm, dedicated server, or modded
- preferred answer style: concise checklist, build brief, command recipe, or debug ladder
- stable constraints such as material budget, low-lag preference, or safe-only admin changes

## Notes
- recurring build dimensions, farm goals, or world themes
- server or loader details worth remembering
- known version-specific quirks that repeatedly matter for this user

---
Updated: YYYY-MM-DD
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still learning | Capture reusable patterns gradually |
| `complete` | Enough context exists | Use stored defaults without extra setup |
| `paused` | User wants minimal persistence | Avoid asking for more memory unless needed |
| `never_ask` | User does not want persistence | Keep all future work session-only |

## Key Principles

- Store reusable Minecraft preferences, not full world saves or sensitive account data.
- Keep local notes focused on activation, edition, style, and stable constraints.
- Do not store credentials, paid account details, or private server tokens.
- If the user declines persistence, do not create or update `~/minecraft/`.
