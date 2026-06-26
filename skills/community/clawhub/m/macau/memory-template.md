# Macau - Memory Template

Create `~/macau/memory.md` with this structure:

```markdown
# Macau Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending

## Context
- Purpose:
- Timeline:
- Arrival path:
- Budget:
- Preferred districts:
- Constraints:

## Notes
- Border notes:
- Hotel or housing pattern:
- Food or nightlife priorities:
- Family, study, or work context:
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Still learning | Keep collecting context naturally |
| `complete` | Enough context exists | Reuse without asking much |
| `paused` | User does not want setup now | Work with current context only |
| `never_ask` | User explicitly declined | Never ask for more setup |

## Principles

- Store natural-language context, not rigid config keys.
- Update `last` whenever the skill is used.
- Keep only durable preferences and constraints.
- Do not store sensitive personal data that the skill does not need.
