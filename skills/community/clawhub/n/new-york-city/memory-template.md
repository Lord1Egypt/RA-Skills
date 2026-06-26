# New York City Memory

Create `~/new-york-city/memory.md` with this structure only if the user wants continuity across sessions:

```markdown
# New York City Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending

## Current Situation
- Mode: visitor / moving / resident / work-study
- Main borough:
- Neighborhood or base:
- Airport / station / commute anchor if known:

## Constraints
- Timeline:
- Budget pressure:
- Housing or hotel constraints:
- Commute, walking, and transit realities:
- Family, safety, or accessibility needs:

## Open Loops
- Task:
- Waiting on:
- Next deadline:

## Notes
- Natural-language observations that improve future NYC advice

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
- Borough, neighborhood, and commute anchor matter more than a generic "NYC" label.
- Save only details that will materially improve the next New York City answer.
- Keep the default memory coarse. Do not store full building details or sensitive identifiers unless the user explicitly asks for saved continuity at that level.
- Update `last` on each meaningful use.
