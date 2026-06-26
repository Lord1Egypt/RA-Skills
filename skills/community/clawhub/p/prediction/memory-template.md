# Memory Template - Prediction

Create these files inside `~/prediction/`.

## `memory.md`

```markdown
# Prediction Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Forecasting Defaults
- Preferred domains:
- Preferred output format:
- Update cadence:
- Main optimization target:
- Known blind spots to watch:

## Guardrails
- Questions that should trigger abstention:
- Data types that should not be stored:
- Cases where this should stay advisory only:

## Notes
- Durable lessons from prior forecasts:
- Patterns behind good calls:
- Patterns behind misses:
```

## `forecast-log.md`

```markdown
# Forecast Log

| question | horizon | probability or scenarios | base rate | main drivers | next review | status | updated |
|----------|---------|--------------------------|-----------|--------------|-------------|--------|---------|
| Will launch ship in Q3? | 2026-Q3 | 42% | 3 of 10 similar launches | scope creep, hiring, blocker bug | 2026-06-01 | open | YYYY-MM-DD |
```

## `scorecard.md`

```markdown
# Prediction Scorecard

| date | question | forecast | outcome | brier | miss type | lesson |
|------|----------|----------|---------|-------|-----------|--------|
| YYYY-MM-DD | Will launch ship in Q3? | 42% yes | no | 0.1764 | planning optimism | stress staffing and slip history harder |
```

## `reference-classes.md`

```markdown
# Reference Classes

| domain | question type | base rate | sample | notes | updated |
|--------|---------------|-----------|--------|-------|---------|
| product | launch by announced quarter | 30% yes | 10 comparable launches | slips cluster around design + QA | YYYY-MM-DD |
```

## `assumptions.md`

```markdown
# Assumptions and Update Triggers

| forecast | assumption | direction | evidence needed to revise | owner | updated |
|----------|------------|-----------|---------------------------|-------|---------|
| Q3 launch | hiring closes in 30 days | bullish | role stays open >45 days | team | YYYY-MM-DD |
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Forecasting style still forming | Keep gathering preferences naturally while answering |
| `complete` | Enough context exists | Work from stored defaults unless the user updates them |
| `paused` | User does not want setup questions right now | Forecast with minimal discovery and no setup push |
| `never_ask` | User does not want recurring profiling | Stop asking for more routing detail unless required |

## Key Principles

- Save durable forecasting defaults and lessons, not every passing opinion.
- Update `last` whenever an active forecast, scorecard, or guardrail changes materially.
- Open forecasts matter less than resolved ones if they are never scored; keep the scorecard alive.
- Reference classes should be compact, comparable, and easy to reuse across questions.
