# Methodology · Iteration (Time-boxed)

## Applicable Scenarios
Requirements moderately certain, regular delivery desired but strict Scrum ceremonies not required; or a larger team producing acceptable increments on fixed time boxes
(common as "bi-weekly iterations" or "monthly iterations" in large R&D organizations). Emphasizes **relatively fixed scope within an iteration** more than agile.

## Lifecycle (iteration cycle)
```
Iteration planning ──▶ Iteration execution (time box) ──▶ Iteration review ──▶ Iteration retrospective ──┐
   ▲                                                  │
   └──────────────── Next iteration ◀───────────────────────┘
```

| Activity | Frequency | Main template |
|------|------|----------|
| Iteration planning | at the start of each iteration | iteration/iteration_plan |
| Iteration execution | during the iteration | iteration/iteration_backlog (task board) |
| Iteration review | at the end of each iteration | iteration/iteration_review |
| Iteration retrospective | at the end of each iteration | agile/retro (reused) |

## Core Artifacts (iteration-specific templates)
- `templates/iteration/iteration_plan.md`: iteration goal, committed scope, key milestones, resources
- `templates/iteration/iteration_backlog.md`: this iteration's task list (ID/owner/estimate/status)
- `templates/iteration/iteration_review.md`: completed items / variance / demo conclusions / input to next iteration

## Cadence
- Fixed time box (e.g., 2 weeks), stable iteration length.
- Review + retrospective held at fixed points at iteration end; status reports issued per iteration (can reuse common/status_report).

## Key Metrics
- Iteration burndown, iteration completion rate = completed items / committed items, velocity trend (see `references/metrics.md`)

## Difference from Agile
- iteration: scope locked within the iteration, commitment-heavy; agile (Scrum): more emphasis on value pull, DoD, role-based ceremonies.
- Templates are interchangeable: iteration_backlog ≈ a lightweight version of sprint_plan; retrospectives share retro.

## Notes
- Iteration review must produce a "whether the commitment was met" conclusion; variances go into `raid.issues`.
- Register cross-iteration dependencies in `raid.dependencies` to avoid the next iteration being blocked.
