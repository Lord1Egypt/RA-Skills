# API Contract

Default API base URL: `https://api.workcapacity.io`

## Endpoints

- `GET /v1/movements` is the primary discovery endpoint. Use it to confirm supported movement names, required inputs, alternative inputs, supported overrides, and assumptions before compute.
- `GET /.well-known/api-catalog` is the top-level discovery entrypoint for agents and API clients.
- `GET /openapi.json` returns the machine-readable API schema.
- `GET /v1/payment-requirements` returns the current public x402 route pricing metadata.
- `POST /v1/compute-power` is the compute endpoint.

## Contract stability

- `/v1` is the public API contract boundary for external users.
- Future breaking changes should not silently replace `v1` behavior in production. They should ship through a compatibility layer or a new versioned path.

## Gather the right inputs

Always collect:

- `athlete_uuid`
- `evaluation_context`
- top-level session `duration_seconds`
- `user.height` with unit `m`, `cm`, or `in`
- `user.body_mass` with unit `kg` or `lb`
- optional `user.age_years`
- optional `user.sex` as `female` or `male`
- ordered `splits[]`

Context rules:

- `completed` requires `performed_date`
- `planned` requires `planned_for_date`
- `planned` and `hypothetical` may include `scenario_label`
- `hypothetical` does not allow `performed_date` or `planned_for_date`

For each split, collect:

- optional `label`
- `duration_seconds` for active work only
- optional `rest_seconds_after`
- `work.movements[]`

For each movement entry, collect:

- `movement`
- `reps`
- `inputs` only when required for that supported movement
- `spec_overrides` only when the user explicitly wants an override that `/v1/movements` indicates is supported

## Conservative split defaults

- If the user gives shorthand such as `21 thrusters - 33 sec`, treat that timed segment as one split.
- If the user gives only one total workout time for an entire effort, use one split with that full duration as active work.
- Session time alone does not define completed volume. If performed rounds or reps are missing, ask for them before compute.
- If multiple rounds are described without split timing, keep the movement sequence in order inside one split instead of inventing per-round timing.
- Do not infer movement-specific power timing from grouped work.

## Request shape

```json
{
  "athlete_uuid": "11111111-1111-1111-1111-111111111111",
  "evaluation_context": "completed",
  "performed_date": "2026-03-20",
  "duration_seconds": 1200,
  "splits": [
    {
      "label": "2 rounds in order",
      "duration_seconds": 1200,
      "work": {
        "movements": [
          { "movement": "pull_up", "reps": 5, "spec_overrides": {} },
          { "movement": "push_up", "reps": 10, "spec_overrides": {} },
          { "movement": "air_squat", "reps": 15, "spec_overrides": {} },
          { "movement": "pull_up", "reps": 5, "spec_overrides": {} },
          { "movement": "push_up", "reps": 10, "spec_overrides": {} },
          { "movement": "air_squat", "reps": 15, "spec_overrides": {} }
        ]
      }
    }
  ],
  "user": {
    "height": { "value": 70, "unit": "in" },
    "body_mass": { "value": 180, "unit": "lb" }
  }
}
```

Notes:

- top-level `duration_seconds` is full session elapsed time
- split `duration_seconds` is active work time only
- `rest_seconds_after` is optional and stays outside split active-power denominators
- if session `duration_seconds` exceeds accounted split time, the remainder appears as `unattributed_duration_seconds`
- `response_units` is optional and should be omitted unless the user asked for specific output units
- `X-PowerOracle-Agent` is an optional header, for example `openclaw/power_oracle`

## Payment behavior

- Free discovery endpoints may be called without payment.
- In production, `POST /v1/compute-power` may respond with `402 Payment Required`.
- When that happens, read the `PAYMENT-REQUIRED` header.
- Build the x402 proof for that exact request.
- Retry the exact same compute request with `PAYMENT-SIGNATURE: <x402 proof>`.
- Keep the same validated payload when you retry. Payment does not change movement validation, required inputs, or split rules.
- Follow the live challenge and current server behavior.

Current production contract:

- Current x402 route prices are published at `GET /v1/payment-requirements`
- Authorized `2xx` responses settle the payment
- Authorized post-billable `4xx` responses also settle the payment
- `5xx` responses do not settle the payment
- If the live challenge or server behavior differs, treat the live server behavior as authoritative

Example challenge flow:

```bash
curl -i https://api.workcapacity.io/v1/compute-power \
  -H 'Content-Type: application/json' \
  --data @payload.json
```

Example challenge response shape:

```http
HTTP/1.1 402 Payment Required
PAYMENT-REQUIRED: <x402 payment requirement payload>
```

Example retry after payment:

```bash
curl https://api.workcapacity.io/v1/compute-power \
  -H 'Content-Type: application/json' \
  -H 'PAYMENT-SIGNATURE: <x402 proof>' \
  --data @payload.json
```

## Error handling

- `400` usually means the movement is unsupported or unimplemented.
- `422` usually means the request shape, units, required inputs, alternative inputs, or overrides are invalid.
- `500` means the compute failed unexpectedly.

If you get a request error, fix the payload before retrying. Do not resubmit the same invalid request.

## Summarize results

- report `results.session.total_work`
- report `results.session.average_power_elapsed`
- mention the strongest and weakest split when `results.summary` includes them
- call out split variation when it matters
- include `notes`, especially denominator clarifications

Important interpretation rule:

- session average power uses full session elapsed time
- split average power uses split active duration only
