---
name: memory-driven-execution-loop
description: Deterministic external-memory execution loop using rules/goal/plan/progress/notes/lessons with strict preflight, one-step execution, and measurable lesson quality gates.
---

# Memory-Driven Execution Loop

Run execution from external state files only.

## Required Files
- `rules.md`
- `goal.md`
- `plan.md`
- `progress.md`
- `notes.md`
- `lessons.md`

## Strict Loop
1. Read `rules.md` first.
2. Read all other memory files.
3. Validate one clear next action.
4. Write reasoning in notes.
5. Execute one step only.
6. Update progress and notes.
7. Convert failures into lessons.

## Timed Task Rule
If user specifies duration (e.g., 30 minutes):
- satisfy wall-clock duration first
- never substitute with output count
- completion requires start/end/elapsed proof

## Lesson Quality Gate (Universal but actionable)
Every universal lesson must include:
- Trigger
- Action
- Metric/threshold
- Boundary conditions
- At least 2 cross-field examples

Missing fields => lesson invalid.
