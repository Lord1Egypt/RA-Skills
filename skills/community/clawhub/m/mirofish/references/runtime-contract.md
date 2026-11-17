# Runtime Contract

Use this file before driving a live MiroFish backend.

## Backend URL

Use `MIROFISH_BASE_URL` when provided. Otherwise default to:

```text
http://localhost:5001
```

Do not hardcode the backend URL in generated scripts. Set:

```bash
BASE_URL="${MIROFISH_BASE_URL:-http://localhost:5001}"
```

## Authentication

The repository routes shown in this skill do not define a request-level API token.

The backend itself requires server-side environment variables:

- `LLM_API_KEY`
- `LLM_BASE_URL`
- `LLM_MODEL_NAME`
- `ZEP_API_KEY`

If requests fail with configuration errors, do not add client auth headers. Check the backend `.env`.

## File Ingestion

Ontology generation uses multipart form data.

Accepted file extensions:

- `pdf`
- `md`
- `txt`
- `markdown`

Maximum upload size is 50 MB.

Required form fields:

- `files`
- `simulation_requirement`

Optional form fields:

- `project_name`
- `additional_context`

## Polling Defaults

Use these defaults unless the user requests otherwise:

- graph build: every 5 seconds, timeout 20 minutes
- simulation prepare: every 10 seconds, timeout 45 minutes
- simulation run status: every 10 seconds, timeout depends on `max_rounds`
- report generation: every 10 seconds, timeout 45 minutes

Stop polling when status is one of:

- completed
- ready
- failed
- stopped
- error

If the status field is absent, inspect `success`, `error`, `message`, and `data.progress`.

## Status Field Map

Graph build:

- endpoint: `GET /api/graph/task/<task_id>`
- check: `data.status`
- completion: `completed`
- failure: `failed`

Simulation prepare:

- endpoint: `POST /api/simulation/prepare/status`
- check: `data.status`, `data.progress`, and `data.already_prepared`
- completion: `ready`, progress `100`, or `already_prepared: true`
- failure: `failed` or `success: false`

Simulation run:

- endpoint: `GET /api/simulation/<simulation_id>/run-status`
- check: `data.runner_status`
- active: `running`
- useful terminal states: `completed`, `stopped`, or `idle` with enough actions already collected

Report generation:

- endpoint: `POST /api/report/generate/status`
- check: `data.status`, `data.progress`, and `data.already_completed`
- completion: `completed`, progress `100`, or `already_completed: true`
- failure: `failed` or `success: false`

## Field Checks

After ontology generation:

- require `success: true`
- require `data.project_id`
- require `data.ontology.entity_types`
- require `data.ontology.edge_types`

After graph build:

- require `success: true`
- require `data.task_id`
- poll task until completed
- recover `graph_id` from task result when present
- if task result does not include `graph_id`, call `GET /api/graph/project/<project_id>` and read `data.graph_id`

After simulation create:

- require `data.simulation_id`
- require status `created`

After simulation prepare:

- require status `ready` or progress `100`
- require `already_prepared: true` or task completed
- require nonzero profiles or entities in `prepare_info` when present

After simulation start:

- require `runner_status` to be `running`, `completed`, or another non-error active state
- inspect `/run-status/detail` for nonzero `all_actions`

After report generation:

- require `report_id`
- poll until `completed`
- read sections and require at least one nonempty section

After interviews:

- require at least one response
- mark generic or evasive responses as non-informative
- stop after every key causal claim has one supporting or refuting interview, or after 3 interview rounds produce no new contradiction

## Recovery Matrix

Ontology generation fails:

- check file extension and upload size
- check `simulation_requirement`
- reduce broad seed material into a tighter brief

Graph build fails:

- check `ZEP_API_KEY`
- confirm project has ontology and extracted text
- retry with `chunk_size` 300 and `chunk_overlap` 30

Simulation prepare fails:

- narrow `entity_types`
- lower `parallel_profile_count`
- retry with `force_regenerate: true`

Simulation start fails:

- check prepare status
- restart with lower `max_rounds`
- use `force: true` only when clearing previous run logs is acceptable

Report generation fails:

- check simulation exists and has `graph_id`
- poll sections and progress for partial output
- retry with `force_regenerate: true` only after preserving useful partial sections

Interview fails:

- check `/api/simulation/env-status`
- check report status with `/api/report/check/<simulation_id>`
- use targeted batch interviews instead of `interview/all` if timeouts occur
