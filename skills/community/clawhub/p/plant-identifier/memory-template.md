# Memory Template - Plant Identifier

Create `~/plant-identifier/memory.md` with this structure:

```markdown
# Plant Identifier Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Activation
- Use automatically when:
- Ask first when:
- Never activate for:

## Preferences
- Confidence bands by default: yes | no
- Save observations locally: yes | no
- Default response style: fast match | ranked shortlist | observation note

## Observation Context
- Main region or climate:
- Typical plant types: houseplants | trees | flowers | weeds | mixed
- Usually available photos:
- Safety-sensitive topics to treat conservatively:

## Recent Observations
- YYYY-MM-DD - short label - best match - confidence

## Notes
- Durable facts only.

---
*Updated: YYYY-MM-DD*
```

Create `~/plant-identifier/observations/YYYY-MM/{entry-id}.md`:

```markdown
# Plant Observation - {entry-id}

- Date:
- User label:
- Context or location:
- Photos reviewed:
- Best match:
- Confidence:
- Growth habit:
- Visible evidence:
- Missing evidence:
- Alternatives:
- Next photo or check:
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | context still evolving | keep learning from real plant identifications |
| `complete` | baseline is stable | reuse saved defaults with minimal setup questions |
| `paused` | storage or setup is paused | use current context without pushing |
| `never_ask` | user opted out | never prompt for setup again |

## Key Principles

- Store durable plant context, not every chat detail.
- Keep recent history short in hot memory and use per-entry files for saved observations.
- Never store precise home addresses or unrelated personal information.
- Update `last` whenever a meaningful identification or preference changes.
