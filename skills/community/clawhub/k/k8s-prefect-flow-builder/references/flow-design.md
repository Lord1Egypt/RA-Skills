# Flow Design

## Start from existing compute logic

Before adding Prefect wrappers:
- extract heavy business logic into a reusable module under `src/core/...`;
- make it callable without Prefect;
- define explicit inputs and a structured result.

## Choose the orchestration boundary

- Use a flow for orchestration.
- Use a task for one independently observable execution unit.
- Use a child flow only when you need a separate scaling, resource, or failure boundary.

## Failure propagation

- Do not return non-zero values silently.
- Raise exceptions so Prefect marks the task or flow as failed.
- Add key context to exception messages so Prefect state messages remain useful after pod logs expire.

## Naming and logs

Use readable names in Prefect UI:
- `task_run_name` for tasks;
- `flow_run_name` for child flows launched by a parent.

Prefer names that expose the unit being processed, such as a batch id or target id.

Keep logs short and structured. A failed unit should emit one log line with enough context to debug without re-reading the pod log.

## Validation checklist

Before enabling a schedule:
- run focused tests;
- verify failure propagation;
- verify task and flow names in Prefect UI;
- run one small manual validation.
