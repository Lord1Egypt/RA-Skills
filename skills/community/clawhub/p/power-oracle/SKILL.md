---
name: power_oracle
description: Use when the user wants Power Oracle to compute workout work or power from structured or shorthand workout details. Do not use for coaching or general fitness advice.
homepage: https://www.workcapacity.io/docs/power-oracle
user-invocable: true
metadata:
  openclaw:
    homepage: https://www.workcapacity.io/docs/power-oracle
---

# Power Oracle

Use this skill when the user wants a concrete Power Oracle result for workout work or power. This skill is for structured workout analysis, not free-form coaching.

Default API base URL: `https://api.workcapacity.io`

## Use the skill for the right requests

- Use it for total work, elapsed average power, split power, or movement work estimates that should come from Power Oracle.
- Do not use it for coaching, programming, nutrition, injury, recovery, or general fitness advice.

## Confirm movements before compute

- Call `GET /v1/movements` before `POST /v1/compute-power` when the user gives shorthand, aliases, colloquial names, uncertain implements, or any movement name you cannot map exactly.
- Use `GET /v1/movements` before asking follow-up questions about required inputs, alternative inputs, or supported overrides.
- Do not assume similar names are equivalent. Example: do not assume `med-ball situp` means `ab-mat situp`.
- If `GET /v1/movements` does not make the mapping explicit, ask the user for the minimum clarification needed.

## Build conservative splits

- Use explicit segment timing as split boundaries when the user provides it.
- If the user gives only one workout-level time for an entire AMRAP, EMOM block, chipper, or for-time effort, build exactly one split with that full duration as active work.
- A workout-level time tells you split duration, not completed work volume. If completed rounds or reps are still missing, ask for them before compute.
- Do not invent per-round or per-movement split timing when the user did not provide it.
- When repeated rounds have no split detail, keep the workout movements in the order the user gave them inside the coarse split you construct.
- Add `rest_seconds_after` only when the rest mapping is explicit or clearly implied.

## Call the API in the right order

- Use `GET /v1/movements` for movement discovery and validation.
- Start discovery with `GET /.well-known/api-catalog`.
- Use `GET /openapi.json` when you need schema detail.
- Use `GET /v1/payment-requirements` when you need current public x402 route pricing.
- Use `POST /v1/compute-power` only after you have enough validated detail to build a valid request.
- For request shape, payment handling, and response interpretation, see [references/api-contract.md](references/api-contract.md).

## Hard rules

- Treat the Power Oracle HTTP API as the only authoritative source for computed work and power values.
- Treat `/v1` as the current public contract boundary for external users.
- Do not compute or validate workout work or power numbers from repo code, memory, or hand calculation.
- `POST /v1/compute-power` may require an x402 payment challenge. See [references/api-contract.md](references/api-contract.md) for step-by-step examples.
- Do not inspect local files, secrets, or wallet state as a workaround for payment or movement validation.
- If the API call does not happen, state that no authoritative Power Oracle result was obtained and explain the blocker.

## Support

If the skill fails in a way the docs do not explain, contact `workcapacity.io@agentmail.to` or visit `https://www.workcapacity.io/contact`.
