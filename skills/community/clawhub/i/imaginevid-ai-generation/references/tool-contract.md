# ImagineVid Agent Tool Contract

Use the live tool schemas as the source of truth. This reference records the
stable orchestration contract for ImagineVid's public remote MCP.

## Tools

| Tool | Purpose | Required facts |
| --- | --- | --- |
| `models_list` | Discover available capabilities | Optional `feature`; returns stable capability `id` (used as downstream `capabilityId`), output kind, model label, fields, constraints, and estimated credits/time when available. |
| `credits_get` | Read the authenticated user's spendable credits | No user ID in the request; the principal comes from the authenticated OAuth connection. |
| `generation_quote` | Validate product values and compute the server quote | `capabilityId`, optional `prompt`, `values`, and `assetIds`; returns `quotedCredits` and a normalized summary. |
| `generation_create` | Reserve credits and start one generation | The same `capabilityId`, `prompt`, `values`, and `assetIds` as the quote, plus `confirmedCredits` and stable `clientRequestId`. |
| `generation_get` | Read one owned generation | `generationId`; returns status, progress, safe error, and normalized result metadata. |

Product values are capability fields, not raw provider request parameters. Asset
inputs are opaque, user-owned `assetId` values returned by a trusted upload
surface and grouped under `assetIds.images`, `assetIds.videos`, or
`assetIds.audios`. The gateway performs capability validation, ownership checks,
quote parity, credit reservation, provider submission, and result ownership.

## Transport and identity

- Remote `https://imaginevid.io/api/mcp` is Streamable HTTP and OAuth-first.
  OAuth access tokens are resource-bound and scope-checked before a tool runs.
- Request only the scopes needed by the operation: `models:read` for
  `models_list`, `credits:read` for `credits_get`, `generations:create` for
  `generation_quote` and `generation_create`, and `generations:read` for
  `generation_get`.
- A principal always resolves to one user. Never send a user ID to select the
  account, ask the user to paste a token, or accept browser session cookies as
  bearer credentials.

## Stable error meanings

`unauthorized`, `forbidden_scope`, `invalid_input`, `capability_not_found`,
`asset_not_found`, `asset_expired`, `insufficient_credits`, `quote_changed`,
`parallel_limit_reached`, `idempotency_conflict`, `submission_unknown`, and
`provider_failed` retain the same meaning across the remote MCP contract;
`generation_not_found` is also returned when an owned generation cannot be
found. The host may change tool-content formatting, but must preserve the code
and a safe message.

`submission_unknown` is deliberately non-retryable: the provider outcome is
ambiguous, reserved credits remain durable, and the existing generation must be
polled or investigated instead of duplicated or automatically refunded.
