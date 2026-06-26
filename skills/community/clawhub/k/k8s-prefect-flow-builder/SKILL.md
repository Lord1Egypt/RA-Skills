---
name: prefect-flow-builder
description: Build, modify, and review Prefect-based offline orchestration in this repository. Use when adding a new Prefect flow, wrapping an existing offline computation as a flow or task, editing prefect.yaml, splitting deployments by resource profile, configuring resources or concurrency, or aligning CI, Prefect, and Kubernetes deployment behavior.
---

# Prefect Flow Builder

## Overview

Use this skill to add or refactor Prefect-managed offline workflows in this repository without mixing orchestration concerns into business logic.

## Workflow

1. Classify the change.
- New flow or major refactor: read `references/flow-design.md` and `references/template-prefect-yaml.md`.
- Deployment-only or config change: read `references/deployment-patterns.md`.
- Resource or concurrency tuning: read `references/resources-and-concurrency.md`.
- If the system model is unclear, read `references/architecture.md` first.

2. Keep orchestration separate from compute.
- Put heavy business logic in reusable job or service modules under `src/core/...`.
- Keep Prefect wrappers in `src/prefect_flows/...`.
- Use tasks for independently observable units or meaningful side effects; avoid exploding one logical step into many tiny tasks just for structure.
- Choose task invocation mode deliberately: direct call for simple serial execution, `.submit()` or `.map()` for in-flow concurrency, and `.delay()` only for background execution on separate infrastructure.
- If a child flow is intentionally serial, call tasks directly inside the loop and let the child flow own error aggregation and final failure semantics. Do not default to `.submit()` just because the unit is a task.
- Reserve `.submit()` for cases that actually need Prefect futures, parallel fan-out, or non-blocking wait and collection behavior, and make sure terminal futures are resolved before the flow returns.
- Introduce child flows only when you need a separate scaling, resource, or failure boundary.

3. Put concurrency controls at the right layer.
- Use task-runner concurrency for in-flow task execution only; it is not a substitute for deployment or infrastructure throttling.
- Use deployment, work-pool, worker, or work-queue limits to control how many flow runs the platform launches.
- Use tag-based concurrency limits when many tasks across flows share an external bottleneck such as a database, API, or memory-heavy resource.

4. Treat `prefect.yaml` as deployment source of truth.
- Put deployment names, schedules, work pool selection, resources, concurrency policies, and deployment parameter defaults in `prefect.yaml`.
- Let CI provide only deploy-time values such as `PREFECT_API_URL` and `PREFECT_DEPLOY_IMAGE`.
- Keep runtime business env in Kubernetes via `env_from`, not CI.
- Keep infrastructure choices aligned with Prefect's worker model: deployments target work pools, and workers poll compatible pools to execute runs.

5. Make failures observable.
- Raise exceptions instead of returning non-zero codes silently.
- Include key context in exception messages and logs.
- Use readable task and flow names so Prefect UI can identify the failing unit quickly.
- When a batch must continue after per-item failures, convert each item into a structured result, finish the batch, then raise once at the flow boundary if the aggregate outcome should be failed.

6. Validate in this order.
- Run focused tests for changed flow and job code.
- Review `prefect.yaml` for deployment or resource drift.
- Trigger a small manual run before enabling or changing schedules.
- If the question is about Prefect semantics rather than repo conventions, verify against the official v3 docs before codifying a pattern.

## Repository Anchors

- Flow entrypoints: `src/prefect_flows/`
- Reusable compute logic: `src/core/`
- Deployment definitions: `prefect.yaml`
- Team guide: `docs/cg_offline_prediction/prefect_orchestration_overview.md`

## Prefect v3 Defaults

- Tasks support three distinct execution modes in v3: direct call blocks and returns a result, `.submit()` returns a `PrefectFuture` for concurrent execution in the same flow, and `.delay()` is for background execution on separate workers.
- Task runners are optional. If you are not intentionally using concurrency, do not introduce `.submit()` or a task runner configuration just to preserve the task decorator.
- Task states are orchestrated client-side and may appear with eventual consistency in the UI, so design recovery and resume logic around durable business outcomes instead of assuming every intermediate task-state transition is the source of truth.

## References

- `references/architecture.md` for the system model and lifecycle.
- `references/deployment-patterns.md` for deployment design and config ownership.
- `references/flow-design.md` for wrapping existing jobs as flows and tasks.
- `references/resources-and-concurrency.md` for sizing and concurrency decisions.
- `references/template-prefect-yaml.md` for reusable deployment templates.
- Prefect v3 Tasks: https://docs.prefect.io/v3/concepts/tasks
- Prefect v3 Task runners: https://docs.prefect.io/v3/concepts/task-runners/
- Prefect v3 Flows: https://docs.prefect.io/v3/concepts/flows
- Prefect v3 Deployments: https://docs.prefect.io/v3/concepts/deployments
- Prefect v3 Workers: https://docs.prefect.io/v3/concepts/workers
- Prefect v3 Tag-based concurrency limits: https://docs.prefect.io/v3/concepts/tag-based-concurrency-limits
