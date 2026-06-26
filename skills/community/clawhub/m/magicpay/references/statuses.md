# MagicPay Result States

MagicPay product work starts from an active workflow session created with
`magicpay start-session`. Browser-dependent states assume a browser child has
been launched or attached inside that product session.

## Reading CLI Results

For MagicPay JSON results, branch on fields, not on prose:

1. `success` — `true` means the command reached its typed success contract;
   `false` means a controlled blocked or failed outcome.
2. `outcomeType` — the command-specific success or blocked class.
3. `error` or `reason` — machine-readable subtype for blocked or terminal
   failure cases.

Use `message` and `reason` as text for the user or timeline. Do not parse them
to discover control flow.

## `plan-fill`

Read `plan-fill` results before calling `apply-fill`; apply only after the
active Memory fill plan is available.

Success shape:

```json
{
  "success": true,
  "plan": {
    "id": "plan_123",
    "valueVisibility": "handles_only",
    "fields": []
  },
  "nextAction": "apply-fill"
}
```

The plan is value-free. It may contain target refs, Memory field refs, safe
descriptor metadata, and value handles, but not raw saved values.

Blocked shape:

```json
{
  "success": false,
  "outcomeType": "blocked",
  "error": "matcher_unavailable",
  "message": "MagicPay could not complete the semantic Memory matcher request.",
  "reason": "The Memory matcher is unavailable through the current gateway configuration.",
  "nextAction": "ask-user"
}
```

`plan-fill.error` values:

- `browser_connection_failed` — the browser child is unreachable. `nextAction`
  is `attach`; rebind the approved browser/session before retrying.
- `page_resolution_failed` — the browser is reachable but the current page
  could not be resolved. Refresh or re-observe the browser state.
- `verification_required` — CAPTCHA, anti-bot, or human verification blocks
  planning. Use the CAPTCHA/auth handoff rules; do not retry through it.
- `redirect_loss` — checkout, booking, cart, or upstream redirect context was
  already lost. Stop; do not continue on a contextless page.
- `matcher_unavailable` — the semantic Memory matcher could not run. Fail
  closed and ask the user or retry only after gateway/tooling state changes.
- `match_ambiguous` or `match_unusable` — the model output could not be safely
  validated. Do not guess.
- `workflow_session_required` — there is no active MagicPay product workflow
  session. Start or restore the product session first.

## `apply-fill`

Read `plan-fill` results first, then call `apply-fill` only for the active
Memory fill plan.

Success shape:

```json
{
  "success": true,
  "status": "filled",
  "completedLedger": []
}
```

Branch on `success`, then `status`:

- `filled` — planned Memory values were filled. Refresh the browser state and
  continue with the page-control owner. If the next browser action is consequential,
  get matching typed MagicPay approval.
- `page_changed` or `stale_plan` — the live page no longer matches the active
  plan. Rerun `magicpay plan-fill` on the current page before applying again.

`fieldDiagnostics[]` is facts-only. Each entry contains `targetRef`,
display `fieldLabel`, `reasonCode`, `confidence`, and optional redacted `evidence`;
it does not contain a command or remediation field. Use `reasonCode` together
with required/optional field status, visible page context, task risk, and UX
constraints:

| `reasonCode` | Agent policy |
| --- | --- |
| `target_not_found`, `stale_target` | Refresh or re-observe the page, then rerun `plan-fill` before another `apply-fill`. |
| `target_not_writable` | Do not blind replan. Check whether the field is gated by a prerequisite, disabled until user action, optional/skippable, or a stop condition. |
| `memory.missing` | Ask the user or use the active Memory request flow; do not invent a value. |
| `memory.conflict` | Ask the user to choose the correct candidate. |
| `memory.ask_before_use` | Wait for approval or denial before materializing the value handle. |
| `provider_needs_reauth` | Use the provider reauth path before retrying provider-backed fill. |
| `provider_unavailable` | Retry only if provider state changed; otherwise skip optional field or stop. |
| `projection.invalid_value`, `projection.missing_select_option` | Ask/update Memory or stop, depending on field criticality and visible allowed options. |
| `projection.missing_format_hint` | Peek or re-observe target details, then refine format hints before retrying. |
| `projection.unsupported_shape`, `projection.ambiguous_value` | Use page-control fallback only when safe; otherwise ask or stop. |
| `unsupported_frame`, `unsupported_target` | Use page-control fallback only when the target is visible and the action remains value-safe; otherwise stop with the product error. |
| `magicbrowse_write_failed_uncertain`, `magicpay_internal_error` | Do not claim success. Refresh evidence, apply remaining safe fields, or stop and report the product error. |

Failure shape:

```json
{
  "success": false,
  "error": "active_plan_required",
  "message": "MagicPay could not find an active Memory fill plan.",
  "nextAction": "plan-fill"
}
```

Branch on `reason` and optional `error`:

- `denied`, `expired`, `failed`, `canceled`, `timeout` — stop the MagicPay
  path and report the exact state.
- `error: "active_plan_required"` — run `magicpay plan-fill` first.
- `error: "memory_materialization_failed"` — MagicPay could not materialize an
  approved value handle. Surface the blocker without exposing raw values.
- `error: "browser_fill_blocked"` — the browser fill layer refused the fill.
  Treat as blocked; refresh state before any retry.

## `fill-field`

Use `fill-field` only when the higher-automation path missed a field or chose
the wrong target and the agent can point to a specific observed `targetRef`.
It accepts value-free assignments from Memory item/field refs to browser
targets and returns the same apply-style result shape as `apply-fill`.

Success or partial shape:

```json
{
  "success": true,
  "status": "filled",
  "completedLedger": [],
  "fieldDiagnostics": []
}
```

Policy:

| Result | Agent policy |
| --- | --- |
| `filled` | Refresh the browser state and continue from the observed page. |
| `partial` | Inspect `fieldDiagnostics` per field before deciding whether to replan, ask, skip, or stop. |
| `needs_replan` with `target_not_found` / `stale_target` | Refresh or re-observe, then return to `plan-fill` unless the agent has a new concrete binding. |
| `blocked` with `target_not_writable` | Do not blind replan. Check prerequisite, user unlock, optional status, or stop. |
| Memory/provider diagnostics | Use the same user, approval, and provider paths as `apply-fill`; do not bypass them through raw values. |
| Projection diagnostics | Refine `projectionPart` only if the target is visibly a typed part; otherwise ask, skip optional, or stop. |

Failure shape:

```json
{
  "success": false,
  "error": "invalid_product_fill_field_request"
}
```

Never use `fill-field` as the default fill path. Start with `plan-fill`, use
`apply-fill`, and drop to `fill-field` only when the agent has better observed
target evidence than the matcher/planner result.

## Post-submit Result Policy

After any approved form submit, observe the page again before claiming success
or deciding recovery:

- If navigation happened or the page shows a clear confirmation/success state,
  continue from that observed state.
- If the page remains on the form with field-level validation messages,
  associate each visible error with its field. Treat saved-value errors as a
  possible Memory/provider value problem, but do not guess hidden values. Ask
  the user to update the relevant Memory item, choose another approved item, or
  stop.
- If the page shows only a general form error, stop and report the visible
  reason. Retry only after page, user, Memory, or provider facts change.
- Never claim success from the submit click alone, and never retry blindly on
  merchant validation errors.

## Request Paths

- `auto` — MagicPay resolved the request without waiting for a new user
  decision.
- `confirm` — MagicPay paused for explicit approval before using the protected
  data or action path.
- `provide` — MagicPay paused because the user needed to provide missing data
  or select the right item.
- terminal `denied`, `expired`, `failed`, `canceled`, or `timeout` — stop the
  MagicPay path and report the exact state.

### `session_stop`

A special variant of `canceled`: the whole workflow session was terminated
mid-flow by the user, a trust rule, or the backend. The result includes
`session_stop` details with a `code` and a human-readable `message`.

Do not retry the same request inside the same session. End the session with
`magicpay end-session`, then start a new one if the user wants to continue.

## Protected Actions

- `artifact` — a typed action command completed and returned the request
  artifact. Proceed with exactly that approved action; stop only if page facts
  changed.
- `pending` — a typed action command with `--return-pending` created the
  request and stored `currentRequestId`. The user can approve in MagicPay UI
  or provide the OTP they received. If they approve in UI, run `wait-request`;
  if they provide OTP, run `confirm-otp --otp <digits>` and then
  `wait-request`.
- `otp_invalid`, `otp_expired`, `otp_attempts_exceeded` — the OTP channel
  failed. Report the typed failure without repeating the OTP. While the
  request itself is still pending, keep MagicPay UI approval available.
- `request_already_resolved` — another channel already resolved the same
  pending request. Continue through `wait-request` or the returned terminal
  request state instead of applying a second decision.
