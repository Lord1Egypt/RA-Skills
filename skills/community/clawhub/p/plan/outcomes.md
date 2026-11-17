# Outcome Tracking

Log home: `~/Clawic/data/plan/outcomes.md`. Layout: a **Current Defaults** block at the top (per task type: plan level, strategy, validation status), append-only records below. The defaults block is re-derived from records at review time; records are never edited after the fact.

## Recording Outcomes

Append after every L2+ task. L0/L1 are not logged unless they failed (→ SKILL.md, Learning Loop).

```
## [YYYY-MM-DD] [Brief description]
Type: [task category, e.g. migration/data]
Plan level: L[2-4]
Strategy: [sequential/parallel/iterative/spike/checkpoint]
Estimate: [the range given] → Actual: [what it took]

### Planned vs actual
- [step that deviated: skipped / reordered / output differed — and why]
- (none = plan held)

### Outcome
[✅ Success | ⚠️ Partial | ❌ Failed]

### Lesson
- [one line: what the plan caught, or what it missed]

### Adjustment
- [concrete change to depth, strategy, or format — or "none"]
```

The "Planned vs actual" section is the payload: deviations feed the replan trigger and next time's plan (`replanning.md`). The Estimate → Actual pair is the calibration data (`estimation.md`, Calibration Loop). A record with empty deviations and no lesson is still worth appending — success streaks are the currency of auto-execute promotion.

## Outcome Analysis

Analyze the **last 5 records per type**, not lifetime rates — old records predate your adjustments and small samples make percentages fiction.

```
migration/data:  ✅ ⚠️ ❌ ✅ ⚠️   ← 2+ non-successes in last 5: act
code/refactor:   ✅ ✅ ✅ ✅ ✅   ← candidate for demotion check
```

When a type shows 2+ non-successes in its last 5, pick the fix by failure shape:

| Failure shape | Fix |
|---------------|-----|
| Missed step, unhandled edge case, forgotten rollback | Promote plan depth |
| Right steps, wrong order or wrong approach | Change strategy (`strategies.md`) |
| Plan fine, execution drifted without replanning | Enforce the 2-consecutive-deviation replan trigger (`replanning.md`) |
| Estimate → Actual consistently off for the type | Apply the type's multiplier before presenting (`estimation.md`) |
| Unclear which | Promote depth first — cheaper to demote later than to fail again |

## Learning Triggers

Thresholds live in SKILL.md (Learning Loop); this is the procedure:

- **Promote:** on one attributable failure, write "[type] needs L[N+1]; L[N] missed [specific thing]". No specific thing named = no promotion.
- **Demote:** after 3 consecutive successes with unused depth, write "[type] fine at L[N-1]; [which sections] went unconsulted", update Current Defaults.
- **Strategy switch:** record why the old one failed and which alternative to test; the switch is confirmed only after the alternative succeeds once.

## Feedback Questions

After L3/L4 plans only (after L2, the questions cost more attention than they return):

- "Was this the right level of planning?"
- "Would you have wanted more or less detail?"
- "Did the plan miss anything you expected to see?"

A user who consistently trims your plans is data: bias that user's defaults one level down and note it in Current Defaults.

## Review Cadence

Trigger: every 10 new records, or monthly — whichever comes first. The review's only job is to re-derive the Current Defaults block from last-5-per-type analysis:

```
## Planning Review [date]
- Records since last review: [N]
- Defaults changed: [type: old → new, one line each]
- Watch next: [types in Learning state, streak counts]
```

A review that changes nothing is a valid result — record it, so the next review starts from a known point.
