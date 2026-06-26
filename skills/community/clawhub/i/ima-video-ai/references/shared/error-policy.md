# Error Policy

Execution failures are translated through `scripts/ima_runtime/shared/errors.py`, not from raw API payload dumps.

## Translation Rules

- extract a structured error code when possible from HTTP errors, API messages, or timeouts
- build a contextual diagnosis using task type, model params, current params, input count, and credit rules
- format a short failure message with likely cause, next actions, and an optional reference code
- keep technical details in local logs instead of echoing serialized create-task payloads to the user or embedding them in raised runtime errors

## Current Scope

This shared translation layer is only used around `execute_video_task()` in `cli_flow.py`.

- execution failures from task create, poll, backend error codes, and timeouts flow through `shared/errors.py`
- auth-shaped product-list failures now reuse the same API-key guidance path and point to `https://www.imaclaw.ai/imaclaw/apikey`
- non-auth product-list failures are still returned directly as `Product list failed: ...`
- input-prep failures are still returned directly from the CLI path
- model-lookup failures are still returned directly from the CLI path

## Current Error Categories

- auth and key errors: unauthorized / invalid key
- recommendation labels: `Seedance 2.0` means subscription-required, while `Seedance 2.0 Fast` is the explicit no-subscription recommendation
- billing errors: insufficient points
- rule mismatch errors: `6009`, `6010`, invalid product attribute, no matching rule
- timeout errors: poll exceeded configured max wait
- backend complexity errors: HTTP 500 / internal server error
- input issues: missing images for image-based task types

## Behavior Boundary

The runtime is diagnostic, not magical:

- it suggests retry steps such as removing custom params, reducing complexity, or switching to a lower-cost profile
- it does not silently mutate the request after a failure
- it keeps the user-visible message shorter than the raw backend error, but still includes a reference code when that code is useful
- it does not yet provide the same translated UX for pre-execution failures earlier in `cli_flow.py`

## Common Operator Errors

Detailed operator recovery steps live in `references/operations/troubleshooting.md`.

### API key missing or invalid

- symptoms: `401 Unauthorized`, `invalid API key`, `API key is required`
- first fix: create or regenerate a key at `https://www.imaclaw.ai/imaclaw/apikey`
- verification step: `python3 scripts/ima_runtime_doctor.py --task-type text_to_video`

### Subscription-required model

- symptoms: `403 Forbidden`, `4014`, `requires a subscription`
- likely cause: `ima-pro` (`Seedance 2.0`) on an account without an active plan
- first fix: switch to `ima-pro-fast` or activate a plan at `https://www.imaclaw.ai/imaclaw/subscription`

### Task creation or rule mismatch failure

- symptoms: `task creation failed`, `6009`, `6010`, `Invalid product attribute`, `no matching rule`
- likely cause: the chosen `model_id`, version leaf, and custom params do not fit the backend rule set
- first fix: remove `--extra-params`, rerun `python3 scripts/ima_runtime_doctor.py`, then confirm the current product list with `python3 scripts/ima_runtime_cli.py --task-type text_to_video --list-models`
