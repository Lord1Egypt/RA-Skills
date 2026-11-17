---
name: greatwait
description: Schedule a call to the user's own app or any API, and read whether it was delivered, through GreatWait's MCP server, HTTP API or command line.
metadata:
  version: "e15ebd2c3abb"
---

# GreatWait

Use this when a user wants something to happen later, or on a recurring
schedule, by having GreatWait call their app or an API they choose.

Source digest sha256:e15ebd2c3abbe878c9676558697c2d6da7cf237701e6a92a5d7d5a6095e02f21. It describes the production API at build 46febfc8d86e and, from npm, @greatwait/api-client@0.3.1, @greatwait/cli@0.3.1 and @greatwait/contracts@0.3.1.

## Connect

- MCP: `https://api.greatwait.dev/mcp`, discovery at `https://api.greatwait.dev/.well-known/oauth-protected-resource/mcp`. OAuth 2.1 with S256 PKCE, or a scoped API key.
- HTTP API: `https://api.greatwait.dev`, with `Authorization: Bearer`.
- Command line: `npm install --global @greatwait/cli`.

## Plan the call

1. Use the authorized project and inspect existing schedules and endpoints when relevant. Identify the user's intended callback endpoint or HTTPS URL, method and data. A timer without a destination cannot deliver a user-visible reminder. Ask where it should call if no receiver was chosen. Never select or create a third-party test URL without the user's approval.
2. Resolve an explicit duration to `delaySeconds`, an exact instant to `at`, a fixed interval to `everySeconds`, or a wall-clock recurrence to `cron` with an IANA `timeZone`. Ask for a precise clock time and the user's time zone when words such as 'tomorrow morning' are ambiguous. Do not turn 'every day at nine' into a 24-hour interval; cron observes local time. Explain GreatWait's daylight-saving behavior when it may change the intended instant: a skipped local time runs at the first instant after the gap, and a repeated time runs once at its earlier instant.
3. Show the resolved trigger, destination, method and data before creating when any material choice is uncertain. A new `url` can silently create an endpoint and needs `endpoints:write`; confirm that destination and access rather than requesting a new grant or credential as part of scheduling.

## Create and verify

1. After the user authorizes the resolved plan, freeze the exact `schedules_create` request body and one `Idempotency-Key` before the first call. GreatWait uses the project's endpoint at `url`, or creates one without returning its signing secret. Never change the key or recompute a relative `at` while recovering an uncertain response.
2. If create returns no certain result, inspect `schedules_read` when an id is known, or `schedules_list` to reconcile the project's schedules. Do not blindly create again. An authorized replay within the 24-hour idempotency receipt window must use the same key and identical body; a changed body is refused. If the result remains uncertain or the receipt may have expired, report that uncertainty and ask before any further create.
3. Read the schedule and `occurrences_read`; use `attempts_list` for actual attempts. A planned occurrence or passed due time is not delivery. Report pending, failed, cancelled, skipped or ambiguous states as such. Say GreatWait observed a receiver response only when the occurrence succeeded and an actual attempt succeeded with its response status. That response does not prove a downstream email, message or business action completed. Bound polling and report an unsettled result rather than waiting indefinitely.
4. If the user asks to cancel, inspect the schedule and occurrence first. Cancel a one-shot before delivery starts; cancellation may still win a race as it becomes due. Cancelling a recurring schedule stops future work, not callbacks already sent. Use `schedules_cancel` only for the authorized schedule, read back its state, and treat `state_conflict` as not cancelled. Never claim cancellation undid a receiver action.

## Rules

- A destination's signing secret and an API key are shown once. Never print, log, or pass either on a command line.
- Use only a destination the user authorized. For an explicitly approved disposable test, ask for the user's unique webhook.site URL (for example, `https://webhook.site/paste-your-unique-id`). It is a third party and must receive no real data. Do not create or call a test destination just because the user asked to see GreatWait work.
- Preserve the default structured envelope unless the receiver needs direct JSON. POST and PUT support both modes; GET has no body. Header rows have a Secret checkbox; ordinary values read back, secret values are write-only. Keep, replace, remove and inherited-header suppression are explicit actions.
- For custom calls and safe credential input, read https://docs.greatwait.dev/guides/http-calls. Never print a receiver token or put it in command arguments.
- Send an `Idempotency-Key` on every create. A replay is safe only with the original request body and key while its receipt remains valid; never use a fresh key to resolve an uncertain create.
- Branch on a refusal's `code`, never on its prose.
- Delivery is at least once: a receiver must tolerate the same delivery twice.
- A connection works in one project; to work in another, the user connects again.

## Read more

- https://docs.greatwait.dev/llms.txt
- https://docs.greatwait.dev/llms-full.txt
- https://docs.greatwait.dev/openapi.json
