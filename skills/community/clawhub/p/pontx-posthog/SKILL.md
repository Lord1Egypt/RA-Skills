---
name: pontx-posthog
description: Use for PostHog project-token runtime capture, event batching, and remote feature-flag evaluation with caller-owned tokens, local previews, and explicit confirmation before any provider request.
---

# PostHog runtime API

Begin with live Pontx discovery instead of copying request fields into an
application:

~~~bash
pontx-hub search "PostHog feature flag or event capture" --type endpoint --json
pontx-hub show <returned-resource-id>
pontx-hub sdk posthog
~~~

Use @pontx/posthog in application code and pontx-posthog for the optional local
CLI. PostHog's public project-token runtime API accepts event capture and
remote feature-flag evaluation. It is caller-directed: Pontx Hub never retains
the project token, proxies the traffic, or stores provider responses.

## Keep tokens and requests local

Supply the project token only from the caller's local environment or client
options. Never paste a token into source, a request example, terminal history,
logs, Hub, or chat. Capture requests can write event, person, or group data.
Remote feature-flag evaluation can affect PostHog usage quota. Treat both as
consequential requests even when the immediate response is successful.

Resolve the current Endpoint and Schema, then render the exact local preview:

~~~bash
pnpm exec pontx-posthog preview captureEvent --json '{"event":"checkout_completed","distinct_id":"user_123"}'
~~~

Preview never sends a provider request. Review the destination, event or
identity properties, and any batch scope. Execute only after the caller gives
explicit confirmation; if inputs change, create and review a fresh preview.

## Choose the narrowest workflow

Use single capture for one deliberate event and batch capture only when the
caller has already bounded and reviewed every entry. For feature flags, resolve
the current evaluation inputs before deciding whether configuration should be
included. Do not infer a flag outcome, silently retry a quota-limited result,
or use a project token from a different environment.

## Few-shot workflows

### Scenario 1: Preview a checkout event

**User:** "Track checkout_completed for user_123, but don't send it yet."

**Approach:** Resolve the current capture contract, prepare a local redacted
preview, verify the event and identity values, and wait for explicit approval
before any request can write analytics data.

### Scenario 2: Evaluate a rollout flag

**User:** "Check whether the new checkout is enabled for this user."

**Approach:** Discover the current feature-flag contract, prepare the local
preview with the caller's token kept private, explain possible quota impact,
and require explicit confirmation before the remote evaluation.

### Scenario 3: Submit a reviewed backfill

**User:** "Send this approved set of migration events as one batch."

**Approach:** Resolve the current batch constraints, confirm that every event
belongs to the intended project and scope, preview the exact body, then ask
for a fresh explicit confirmation before sending the write request.
