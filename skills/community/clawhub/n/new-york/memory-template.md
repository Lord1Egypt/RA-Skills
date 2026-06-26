# New York (State) Memory

Create `~/new-york/memory.md` with this structure only if the user wants continuity across sessions:

```markdown
# New York (State) Memory

## Status
status: ongoing
version: 1.0.1
last: YYYY-MM-DD
integration: pending

## Current Situation
- Mode: visitor / moving / resident / business
- Main region:
- City or suburb:
- County / ZIP / district if known:

## Constraints
- Timeline:
- Budget pressure:
- Family or school needs:
- Vehicle, transit, and commute realities:
- Winter, flood, insurance, or health sensitivities:

## Open Loops
- Task:
- Waiting on:
- Next deadline:

## Notes
- Natural-language observations that improve future New York advice

---
Updated: YYYY-MM-DD
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still learning context | Keep gathering high-signal details naturally |
| `complete` | Enough stable context exists | Reuse what is already known before asking |
| `paused` | User does not want more setup right now | Help with current task and avoid extra intake |
| `never_ask` | User does not want this tracked | Stop collecting new background unless asked |

## Key Principles

- Keep notes in natural language, not config-style keys.
- Region, county, ZIP, and district matter more than a generic "upstate" label.
- Save only details that will materially improve the next New York answer.
- Keep the default memory coarse. Do not store full street addresses or sensitive identifiers unless the user explicitly asks for saved continuity at that level.
- Update `last` on each meaningful use.
