# Planner-Needed Bootstrap Template

Use this when a new multi-step request needs Laizy to generate the first actionable milestone queue.

Create a local `IMPLEMENTATION_PLAN.md` like this in the target repo:

```md
# IMPLEMENTATION_PLAN.md

Goal: <user goal>

## Execution rules
- This plan is the authoritative execution queue for the current Laizy run.
- Advance one highest-priority incomplete milestone at a time.
- After each completed milestone: update this file, verify, commit exactly once, and push immediately.
- Keep scope narrow and compatibility-safe.
- Use `laizy start-run` once, then `laizy supervisor-tick` for every later decision.

## Planner bootstrap state
- No actionable milestones are authored yet.
- A planner worker should produce the first bounded milestone queue for this request.
```

Then bootstrap the run:

```bash
laizy start-run \
  --goal "<user goal>" \
  --plan IMPLEMENTATION_PLAN.md \
  --out state/runs/<run-name>.json

laizy supervisor-tick \
  --snapshot state/runs/<run-name>.json \
  --out-dir state/runs/<run-name>.supervisor
```

If the emitted decision is `plan`, read the generated `planner.request` artifact and hand it to a planner worker.

Important operational detail:
- if you reuse the exact same run files after switching from `needs-plan` to an actionable plan, old event logs can keep the run anchored to the earlier state
- safest approach: archive or remove the old run artifacts, then re-run `start-run` against a clean snapshot path after the planner lands the new plan
