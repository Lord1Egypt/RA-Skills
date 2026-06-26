---
name: life-state
description: Daily mood / energy / soreness / sleep capture primitive. Other lifekit skills read this to make state-aware suggestions instead of generic templates.
author: Denys Sychov
version: 0.1.0
triggers:
  - "how am I feeling"
  - "mood check"
  - "morning check-in"
  - "log mood"
  - "log energy"
  - "I feel"
  - "feeling tired"
  - "feeling good"
  - "feeling sore"
  - "energy is"
  - "slept badly"
  - "slept well"
  - "today I am"
---

# life-state

A boring, durable state primitive. NOT a chat experience — it's the integration glue that lets other skills (`morning_brief`, future workout suggester, bedtime brief) adapt to your current state instead of returning the same template every day.

## When to invoke

User describes how they feel, their energy level, soreness, or sleep quality. Examples:

- "feeling tired today, energy 4, sore chest"
- "slept well, energy 8"
- "good mood but quads are wrecked"
- "headache, low energy"
- "morning check-in: normal mood, energy 6, slept ok"

## How to invoke

Use the `life-state` CLI via Bash. YAML output to stdout.

### Capture state (merge semantics — only updates the fields you pass)

```bash
life-state set --mood tired --energy 4 --sore chest,triceps --sleep poor --note "headache, late night"
```

Flags (all optional, at least one required):
- `--mood <m>` — `great | good | normal | tired | terrible` (freeform accepted; lowercased)
- `--energy <n>` — 1-10 (rejected outside that range)
- `--sleep <q>` — `good | ok | poor` (freeform accepted)
- `--sore <list>` — comma-separated muscle groups (e.g. `chest,triceps`)
- `--note "<text>"` — free-text annotation
- `--date YYYY-MM-DD` — override (default: today)

**Merge semantics:** calling `set` twice on the same day updates only the fields passed. Morning check-in + post-workout check-in compose cleanly.

### Read today's state

```bash
life-state get
life-state get --date 2026-05-15
```

### Week aggregate

```bash
life-state week              # last 7 days
life-state week --days 14    # last 14 days
```

Returns avg energy, mood histogram, top soreness areas, and per-day rollup.

## Data location

`~/.life/state/<date>.json` — one JSON file per day. Stable, known location every other lifekit skill should read from.

Schema:
```json
{
  "date": "2026-05-15",
  "mood": "tired",
  "energy": 4,
  "soreness": ["chest", "triceps"],
  "sleep_quality": "poor",
  "note": "headache, late night",
  "updated_at": "2026-05-15T19:30:00.000Z"
}
```

## Notes for the agent

- **Don't be Sol.** This skill has no personality — capture the state and confirm tersely. Personality belongs in `morning_brief`, not here.
- **Parse loosely from natural language.** "feeling tired, energy 4" → `--mood tired --energy 4`. "sore chest and triceps" → `--sore chest,triceps`.
- **Merge, don't replace.** If user adds "energy 6 now" later in the day, only update `--energy`. Don't wipe morning mood.
- **Recommend the enum values** when you summarize back, but accept freeform — if a user says "drained" or "wired," store it verbatim; downstream skills can pattern-match or pass-through.
- **Other skills should read this state** at the start of their flow:
  - `morning_brief`: read yesterday's `sleep_quality` + today's `energy` to vary breakfast / day prep
  - workout suggester (when built): read today's `energy` + `soreness` to adapt volume
  - bedtime brief: read today's `note` to tailor wind-down
