# Baseline Record

> This document records the point in time and scope at which the project plan was **frozen as a baseline**, serving as the reference baseline for subsequent operational control (PM Control Engine).
> Once a baseline is established, any change to scope / schedule / budget must go through change control (CCB).

| Item | Content |
|----|------|
| Project Name | {{ project.name }} ({{ project.id }}) |
| Methodology | {{ project.methodology }} |
| Baseline Date | {{ baseline.on }} |
| Baseline By | {{ baseline.by }} |
| Lifecycle State | {{ project.lifecycle_state }} |
| Baseline Snapshot File | {{ baseline.file }} |
| Planned Baseline Date | {{ project.baselined_on }} |

## Baseline Scope (Frozen Content)

The baseline snapshot (`{{ baseline.file }}`) locks in the following plan elements as the control reference:

- **WBS / Work Packages**: scope, estimates, dependency network, deliverables, and DoD
- **Milestones**: target dates and owners
- **Risk Register**: probability / impact / score / severity (5×5 calibration)
- **EVM Baseline**: Budget at Completion (BAC / PV) and initial measurements

## Control Discipline

1. Non-baselined (no `baseline` pointer) waterfall / hybrid projects **must not** enter the execution/monitoring phase.
2. After entering `operational`, `control_engine.py` periodically inspects against this baseline per `control.cadence`.
3. If any control item breaches a threshold → escalate an alert (exit 1) and trigger `change_request` to assess whether re-baselining is needed.

## Related Artifacts

- Control Register: `control_register.md` (defines what / how often / who to inspect)
- Control Report: `control_report.md` (output of each inspection)
