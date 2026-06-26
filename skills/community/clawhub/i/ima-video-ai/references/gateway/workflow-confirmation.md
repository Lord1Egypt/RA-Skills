# Workflow Confirmation

The workflow package is an internal confirmation-planning seam and testable helper. It exists in the runtime, but it is not part of the shipped CLI execution path.

## Active CLI Path

The shipped CLI path is:

- `scripts/ima_runtime_cli.py`
- `scripts/ima_runtime/cli_flow.py`
- `scripts/ima_runtime/capabilities/video/routes.py`

Current CLI execution routes requests through the video capability flow directly. It does not call `workflow/coordinator.py` or `build_confirmable_plan()` today.

## Current Contract

- `scripts/ima_runtime/gateway/planner.py` builds a `WorkflowPlanDraft`.
- `scripts/ima_runtime/workflow/__init__.py` is the package boundary and exports `build_confirmable_plan()`.
- `scripts/ima_runtime/workflow/coordinator.py` defines `build_confirmable_plan()`.
- `scripts/ima_runtime/workflow/confirmation.py` exposes `to_confirmable_plan()` and currently returns the draft unchanged.

Today this means:

- text requests and single-image requests become a one-step draft with the summary `Single-step video run`.
- requests with two or more images become a one-step draft with the summary `Clarify image roles before video execution`.
- every current draft contains the same `video-1` step targeting the `video` capability with the goal `Resolve route and execute the requested video task`.
- there is no persisted confirmation state machine in the current runtime.

## Why It Exists

The seam keeps planning logic isolated from the active CLI route and gives the repo a testable place to describe confirmation behavior. In the current codebase that makes it an internal seam, not an executed step in the operator-facing CLI path.
