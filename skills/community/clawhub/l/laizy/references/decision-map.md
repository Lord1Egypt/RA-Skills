# Laizy Decision Map

Use this file when `supervisor-tick` has already emitted a bundle and you need the exact next artifact to read.

## Bundle directory

By convention:

- snapshot: `state/runs/<run-name>.json`
- supervisor output dir: `state/runs/<run-name>.supervisor`

## Decisions

### `plan`

Expected artifacts:
- `supervisor-decision.json`
- `supervisor-manifest.json`
- `run-<id>.planner-request.json`
- `run-<id>.planner-spawn.json`

Do:
- read the planner request
- spawn/steer the planner
- let the planner author the first actionable milestone queue
- if the run started in `needs-plan`, re-bootstrap once the plan exists

### `replan`

Expected artifacts:
- `supervisor-decision.json`
- `supervisor-manifest.json`
- `run-<id>.planner-request.json`
- `run-<id>.planner-spawn.json`

Do:
- use the planner to repair or replace the current plan
- keep the change bounded to the drift/blockage that triggered replanning

### `continue`

Expected artifacts:
- `<milestone>.implementer-contract.json`
- `<milestone>.implementer-spawn.json`

Do:
- execute exactly that milestone
- do not widen scope
- re-run `supervisor-tick` after verification/commit/push

### `recover`

Expected artifacts:
- `run-<id>.recovery-plan.json`
- `run-<id>.recovery-spawn.json`

Do:
- resume safely from the bounded recovery plan
- keep the fix narrow
- re-run `supervisor-tick` after the repair lands

### `verify`

Expected artifacts:
- `<milestone>.verification-command.json`

Do:
- run the emitted command
- record the result before completion
- only mark the milestone complete after a passed verification record exists

### `closeout`

Expected artifacts:
- `run-<id>.watchdog-disable.json`

Do:
- disable/pause the watchdog
- stop the loop
- leave the repo clean and synced
