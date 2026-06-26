# MagicBrowse Statuses

## `act` Result Shape

`magicbrowse act` returns:

- `status: completed | blocked | needs_handoff | needs_approval |
  failed | max_steps | cancelled`
- `finalUrl: string | undefined` — last URL the navigator observed
- `finalMessage: string` — concise terminal report or stop explanation
- `stepCount: number` — navigator step count
- `blockedReason?: missing_input | item_unavailable | ambiguous | no_path`
  — required when `status` is `blocked`
- `handoff?: { kind, resumeObjective? }` — required when `status` is
  `needs_handoff`

JSON output shape:

```json
{
  "type": "result",
  "status": "needs_handoff",
  "finalUrl": "https://merchant.example/checkout",
  "finalMessage": "CAPTCHA challenge shown before the address form.",
  "handoff": { "kind": "captcha" },
  "stepCount": 14
}
```

Branch on `status`, then on `blockedReason` or `handoff.kind` when
present. Do not parse `finalMessage` to distinguish task success,
missing input, handoff subtype, approval, runtime failure, max steps, or
cancellation. Use `finalMessage` as text to show the user or pass to the
upstream orchestrator.

CLI exit codes:

| `status` | exit code |
| --- | ---: |
| `completed` | `0` |
| `blocked` | `0` |
| `needs_handoff` | `0` |
| `needs_approval` | `0` |
| `failed` | `1` |
| `max_steps` | `2` |
| `cancelled` | `130` |

A non-zero exit code means runtime failure, budget exhaustion, or
cancellation. `blocked`, `needs_handoff`, and `needs_approval` are
controlled browser-task stops and still exit `0`.

## Status Meanings

- `completed` — the delegated browser task reached the requested
  terminal state. Confirm with the visible evidence in `finalMessage`
  when the host needs an extra business-rule check.
- `blocked` — MagicBrowse cannot continue because ordinary
  input is missing, the requested item is unavailable,
  the delegated task is ambiguous, or the page state has no reasonable
  page-control path left inside the task. Read `blockedReason`.
- `needs_handoff` — the task reached Memory data or human
  verification: login, password, OTP, identity/KYC data, payment or
  banking fields, API keys/tokens/secrets, CAPTCHA, or a similar human
  check. Read `handoff.kind`. Surface `finalMessage` to the user and
  stop; do not retry through the barrier and do not invent or
  placeholder Memory values.
- `needs_approval` — the next useful action would commit an external
  side effect such as buy, book, pay, send, post, publish, accept
  terms, delete, or save account settings. Ask for approval before the
  exact final action unless a matching typed MagicPay approval already covers
  the unchanged page facts.
- `failed` — runtime, model, browser, or tool failure. Inspect
  `finalUrl` and the event stream before retrying.
- `max_steps` — the planner did not converge inside the step ceiling.
- `cancelled` — the act was cancelled mid-run, usually by SIGINT or a
  caller abort.

## When `status: blocked`

Treat this as a controlled stop. Branch on `blockedReason`:

- `missing_input` — ask the user for the missing ordinary input.
- `item_unavailable` — report that the requested item, route, result,
  appointment, or option is unavailable; do not retry the same page path.
- `ambiguous` — ask the user to clarify the delegated browser task or
  required choice.
- `no_path` — choose another strategy outside MagicBrowse, restart from
  a better entry point, or abort.

Do not blindly rerun the same `act` goal.

## When `status: needs_handoff`

Surface `finalMessage` to the user or orchestrator and stop. The wall is
real and `magicbrowse` will not pass it. Do not retry the same `act`
against the same wall. Do not invent credentials, identity values,
payment values, or CAPTCHA answers, and do not placeholder Memory-managed
fields to slip past.

Branch on `handoff.kind`:

- `memory_fill` — pass `{ kind: "memory_fill", resumeObjective }`
  to the orchestrator or MagicPay Memory fill workflow. After the
  Memory fill completes, call `magicbrowse act` with that page-local
  `resumeObjective`.
- `captcha` — have the user or an approved external solver clear the
  CAPTCHA, then run `magicbrowse mark-captcha-resolved` before the next
  `act`.
- `auth` — stop and ask the user to authenticate, approve the login, or
  provide the required auth step through an approved flow.
- `identity_verification` — stop and ask the user to complete or approve
  the identity/KYC step through an approved flow.

## When `status: needs_approval`

Ask the user to approve the exact visible action and page state. After
approval, re-run `observe` so target ids and page facts are fresh, then
execute only the approved action. If the page changed meaningfully,
ask again.

A successful typed MagicPay approval is enough for the exact payment,
signing, or confirmation action it approved. Do not ask again while the page
facts remain unchanged.

## When `status: max_steps`

The granule was likely too large or vague. Split it on a page-change
boundary or tighten the expected terminal state before retrying. Raise
`--max-steps` only when you have a specific reason to believe the task
needs the headroom.

## Layer-4 Primitive Results

`click`, `type`, `fill`, `select`, and `press` emit a JSON action
result on stdout. For these direct actions, `status: "completed"` means the
primitive ran through the action layer. It is not a semantic claim that the
intended page state changed. When the next step depends on changed page state,
re-`observe` and branch on the fresh snapshot. Use `act` for a delegated task
that needs its own completion check.

Common blocked reasons:

- `target_not_found` — the `<target-id>` does not match anything in
  the most recent observe snapshot. Re-`observe` and retry.
- `unsupported_target` — the target is not the right kind for the
  action, such as `type` on a button. Re-read the observe snapshot for
  the correct kind.
- `click_failed` / `input_failed` / `select_failed` / `press_failed`
  — the action reached the page but the page rejected it. Re-`observe`
  to see the new state.

## Browser Session Errors

- `magicbrowse launch` failure — the runtime could not start Chrome.
  Check permissions, keep the default headless mode unless a visible
  debug browser was explicitly requested, or switch to `attach` if a
  host browser is available.
- `magicbrowse attach <endpoint>` failure — the CDP endpoint is
  unreachable or rejected the connection. Verify the endpoint and
  retry.
- `browser-status` reports the session unreachable mid-task —
  reconnect with `launch` or `attach`, then re-`observe`. Treat all
  pre-disconnect target ids as stale.
