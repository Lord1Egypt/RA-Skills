# Memory Template - Maps

Create `~/maps/memory.md` with this structure:

```markdown
# Maps Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Activation Preferences
<!-- Always-on, explicit-only, or keyword-based activation rules -->

## Provider Defaults
<!-- Preferred providers for search, geocoding, routing, and link launching -->

## Geography Defaults
<!-- Typical cities, countries, units, language bias, and time formatting -->

## Privacy and Cost Boundaries
<!-- What providers to avoid, when to ask before live calls, and paid-call limits -->

## Recurring Context
<!-- User-approved recurring origins, destinations, and map contexts -->

## Failure Patterns
<!-- Ambiguous results, provider-specific bugs, and the recovery that worked -->

## Notes
<!-- Short context that improves the next map workflow -->

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Context is still evolving | Ask only when missing details change correctness, privacy, or cost |
| `complete` | Stable map defaults exist | Prioritize execution and targeted clarification |
| `paused` | User paused setup | Keep current defaults and avoid new setup prompts |
| `never_ask` | User does not want setup prompts | Use only explicit instructions unless safety requires clarification |

## Key Principles

- Keep memory in natural language, not raw request dumps.
- Store only context that improves provider choice, accuracy, privacy, or cost.
- Update `last` after meaningful changes to provider defaults or recurring map contexts.
- Preserve recurring failure patterns because they prevent repeat geography mistakes.
- Never persist API keys, private itineraries, or sensitive location history by default.
