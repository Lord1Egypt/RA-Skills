# MagicPay Command Guide

The hard rules from `SKILL.md` apply to every current command: protect the
MagicPay API key and CDP endpoint, use only the browser/session approved for
this task, keep Memory fill to plan/apply without final submission, and get
the matching typed MagicPay approval before any submit, protected action,
purchase, login, identity submission, account change, or other consequential
action.

## Setup And Readiness

### `magicpay init <apiKey> [--api-url <url>]`

Save the API key to the MagicPay config file. By default this is
`~/.magicpay/config.json`; when `MAGICPAY_HOME` is set, it is
`$MAGICPAY_HOME/config.json`. When `--api-url` is provided, `init` also stores
the gateway base URL there. Omit `--api-url` for normal setup; the CLI uses
its bundled default MagicPay gateway URL. Pass `--api-url <url>` only for a
non-default staging, self-hosted, or test gateway.

Do not print, log, or share the API key or the persisted config. If this
machine or workspace is shared or compromised, ask the user to rotate or
revoke the key before continuing.

### `magicpay status`

Check CLI health, authenticated identity, and update state. Use this as the
normal preflight command before a MagicPay Memory fill task.

### `magicpay doctor`

Inspect the local config file when `status` still fails after `init`.

### `magicpay --version`

Print the installed CLI version.

## Product Session And Browser Child Control

### `magicpay start-session [name] [--merchant-name <name>]`

Start the MagicPay product workflow session. This is the parent operation for
normal MagicPay product work; it creates the product workflow before any
browser child is required.

`start-session` attempts to cancel/clear a stale previous workflow binding
before it creates the new product session. If that recovery is still blocked,
start manual recovery with `magicpay status`, then either `magicpay
end-session` or a fresh `start-session`.

### `magicpay launch [url] [--profile <name>]`

Launch a browser child inside the active MagicPay product workflow session.

Use this after `magicpay start-session` when MagicPay should create the
browser execution resource. The optional URL places the new browser child at
the starting page. The browser child does not replace the product workflow
identity.

The success result includes the child's `cdpUrl`. Use it when a
page-control tool (for example `magicbrowse attach`) should drive the
same browser inside the workflow; keep the endpoint private.

### `magicpay attach <cdp-url> [--provider <name>]`

Attach an already running browser as the browser child inside the active
MagicPay product workflow session.

Use only a private CDP endpoint for the browser/session the user approved for
this task. Treat the endpoint as sensitive because it inherits the browser's
logged-in state. Run `attach` after `start-session` when MagicPay is not yet
bound to the approved browser child, or when the CDP endpoint changed.
Re-attaching the same endpoint is allowed but is not required as a ritual.

### `magicpay browser-status`

Inspect the browser child bound to the active MagicPay product workflow.

This is a browser-dependent diagnostic command. Browser-only state is not
enough; the command requires an active product workflow and a matching browser
child binding.

### `magicpay close`

Close or clear the browser child bound to the active MagicPay product
workflow.

This does not end the product workflow session. Use it when the browser child
should be cleaned up or replaced, then continue the same product workflow with
another `launch` or `attach` if needed.

### `magicpay solve-captcha [--timeout <s>]`

Solve a confirmed CAPTCHA on the current browser child inside the active
MagicPay product workflow.

Only call this when a real CAPTCHA is confirmed present. The command uses the
current bound browser child, and does not close or recreate the browser. After
a successful solve, continue the ordinary browser or Memory fill flow from the
current page. If the next step is through MagicBrowse, call
`magicbrowse mark-captcha-resolved`, then continue with `magicbrowse act
"continue..."`.

### `magicpay end-session`

Complete the active product workflow session and product root run.

This is workflow completion only. After it succeeds, return page control to the
page-control owner. A browser tool or orchestrator that launched an owned
disposable browser may clean up its own session when the overall task is done;
an external/user-owned browser stays open unless the user explicitly approves
teardown. `end-session` does not require a live browser child.

## Memory Fill

### `magicpay plan-fill`

Run `magicpay plan-fill` before `magicpay apply-fill` to plan Memory field fill
from the active browser page. The command observes the current page, fetches
value-free Memory descriptors from MagicPay, asks the Memory matcher for
semantic target matches, validates the model output, and stores a short-lived
fill plan in the active workflow. Optional usage:
`magicpay plan-fill --planner-hint <text>`. Use the hint only for short
human-readable context about the current form.

Do not pass target matches, Memory catalogs, raw values, materializers, browser
writers, or page target lists. The plan result must remain handles-only. If the
Memory matcher is unavailable, fail closed and report the blocked state instead
of guessing.

### `magicpay list-memory-items --url <current-url> [--status <status>]`

List value-free Memory item metadata for the current site scope. Use
`--all-sites` instead of `--url` only for explicit global Memory review or
editing. The command returns item ids, labels, statuses, read-only markers, and
field refs with labels/hints, never raw values.

### `magicpay list-memory-items --all-sites [--status <status>]`

List value-free Memory item metadata across sites. Use this only for explicit
global review or editing, not as the default page-fill path.

### `magicpay get-memory-item --item-id <itemId>`

Get one value-free Memory item by stable item id. Use it when a prior list
result identified the item that needs inspection before editing.

### `magicpay delete-memory-item --item-id <itemId>`

Soft-delete one editable Memory item by stable item id. Do not delete
provider-backed read-only items.

### `magicpay create-memory-item --item-label <label>`

Create a new Memory item. Add fields with UX-first shortcuts:

```bash
magicpay create-memory-item \
  --item-label "Airline login" \
  --site airline.example \
  --text "Login email=ada@example.com" \
  --secret-text "Password=correct-horse"

magicpay create-memory-item \
  --item-label "Traveler profile" \
  --person "Full name=Ada Lovelace" \
  --date "Date of birth=1815-12-10" \
  --phone "Phone=+14155550100" \
  --secret-phone "Backup phone=+14155550101"
```

Create shortcuts use `"Label=value"` because the fields are new and have no
`fieldRef` yet. Use `--text` for ordinary direct fill, `--date` for
`YYYY-MM-DD`, `--phone` for E.164 phone numbers such as `+14155550100`, and
`--person` for a full name. The `--secret-*` variants set the same value type
with secret display/logging metadata.

### `magicpay add-memory-field --item-id <itemId> --label <label> --value <value>`

Add exactly one field to an existing editable item:

```bash
magicpay add-memory-field \
  --item-id mem_airline_login \
  --label "Recovery code" \
  --value "123456" \
  --secret true \
  --hint "One-time recovery code"
```

Optional flags are `--type text|date|phone_number|person_name`, `--secret
true|false`, and `--hint <text>`. `--type text` means ordinary untyped direct
fill.

### `magicpay update-memory-field --field-ref <fieldRef>`

Update one existing editable field by stable `fieldRef`:

```bash
magicpay update-memory-field --field-ref field_phone --value "+14155550101"
magicpay update-memory-field --field-ref field_phone --secret true
magicpay update-memory-field --field-ref field_phone --type text
magicpay update-memory-field \
  --field-ref field_password \
  --label "Account password" \
  --hint "Account password"
```

Existing fields are never addressed by label. List or get Memory first, choose
the intended `fieldRef`, then update that ref. `--secret true|false` is mutable
display/logging metadata for any field, including phone fields. It is not
encryption and not a value type. `--type text` clears semantic value type.

### `magicpay delete-memory-field --field-ref <fieldRef>`

Remove one existing editable field by stable `fieldRef`:

```bash
magicpay delete-memory-field --field-ref field_recovery_code
```

If a `fieldRef` is unknown or duplicated, field-level commands fail closed with
a structured CLI error and do not mutate Memory.

Raw JSON is an advanced service/debug escape hatch only:
`magicpay create-memory-item --raw-item-json <json>` and `magicpay
update-memory-item --item-id <itemId> --raw-item-json <json>`. Do not use it as
the normal agent path.

When MagicPay Memory has a provider-backed payment card but the active
workflow session has not been authorized for payment-card reveal, `plan-fill`
keeps the plan value-free and reports machine state instead of card handles:

```json
{
  "kind": "payment_card.authorization_required",
  "category": "payment_card",
  "status": "authorization_required",
  "reason": "payment_authorization_required",
  "blocking": false
}
```

The CLI also adds a diagnostic warning explaining that the card exists and
requires payment authorization before reveal. If the card is needed for the
current payment, collect `amount`, `currency`, `recipient`, optional
`description`, and optional `recurring`, run `magicpay authorize-payment`,
then rerun `plan-fill` for the current page. Do not ask the user for raw card
details and do not bypass this through lower-level Memory or materialization
calls.

### `magicpay apply-fill`

Run `magicpay plan-fill` before `magicpay apply-fill`; apply only the active
Memory fill plan. Optional usage: `magicpay apply-fill --plan <planId>` when a
recovery flow needs a specific stored plan. The command refreshes the browser page state,
materializes only the approved values needed by the plan, writes the planned
fields through the browser bridge, and stops before final commitment actions.

If the result includes `memory.choose_candidate`, ask the user which displayed
candidate to use, then run `magicpay choose-memory --choice <choiceId>`.
`choiceId` is the selector; candidate labels are display text only.

After a successful fill, refresh the visible page state through the browser
owner and continue from that state. Use typed action approval before any final
Pay, Book, Send, Submit, login, identity submission, account change, or other
consequential action.

### `magicpay fill-field --request-json <json>`

Use `fill-field` only as a lower-automation recovery step after `plan-fill` /
`apply-fill` missed a field or matched the wrong target. The agent supplies
explicit value-free assignments. Each assignment identifies an approved Memory
field and one currently observed browser target:

```json
{
  "assignments": [
    {
      "itemRef": "mem_profile",
      "fieldRef": "field.email",
      "targetRef": "selector:1"
    }
  ]
}
```

Use `itemRef` or `itemId` to narrow the Memory item when needed, `fieldRef` to
select the field, and `targetRef` from the current browser observation. Do not
invent refs; if the target evidence is stale, re-observe or rerun
`plan-fill` instead.

The command fetches the current Memory catalog, resolves each assignment to a
backend value handle, refreshes current target state, validates approval,
provider, target writability, and projection constraints, then writes through
the same browser bridge as `apply-fill`. It returns the same apply-style shape:
`status`, `fields`, `fieldDiagnostics`, and `completedLedger`.

Optional `projectionPart` is allowed for explicit typed recovery: `year`,
`month`, `day`, `country_code`, `national_number`, `given`, `family`,
`segment_1`, `segment_2`, `segment_3`, or `segment_4`. Unsupported parts return
projection diagnostics.

Do not use `fill-field` as the default fill path, do not pass raw values, and
do not pass target lists, Memory catalogs, materializers, or browser writers.

### `magicpay choose-memory --choice <choiceId>`

Choose one backend-owned Memory candidate returned by `apply-fill` and continue
the active fill plan. Do not choose by number or label in the CLI contract.

### `magicpay authorize-payment --amount <number> --currency <code> --recipient <name> [--description <text>] [--recurring <true|false>] [--authorization-ref <ref>] [--item-ref <vaultItemId>] [--return-pending]`

Request approval for a payment authorization through the structured
`authorize_payment` action contract.

Before calling it, collect these visible transaction facts from the current
checkout/review page and the user's task:

- `amount` — final amount in major units as a JSON number, not cents and not a
  formatted string.
- `currency` — explicit three-letter currency code.
- `recipient` — merchant or payee the user believes they are paying.
- `description` — optional short order, plan, subscription, or purpose summary.
- `recurring` — optional boolean; ask the user if recurring status matters and
  is unclear.

`--item-ref` remains the existing Memory item selector. It is not placed in
`params`, and this command does not change how MagicPay discovers or selects
Memory items.

After successful approval, continue with that exact payment: protected payment
artifact use, payment form fill, and final Pay/Submit are covered while
`amount`, `currency`, `recipient`, and `recurring` stay unchanged. Stop and ask
again if any of those facts change.

Use `--return-pending` when the agent needs to hand approval to the user
without blocking the command. It creates the same pending request, stores
`currentRequestId`, and returns the request handle. The user can then approve
in MagicPay web/mobile UI or provide the OTP they received. OTP is optional.

### `magicpay sign-message --item-ref <walletItemId> --message <text> [--return-pending]`

Request approval to sign one exact wallet message with the selected wallet
item. Use this for wallet message signing only. After approval, sign exactly
that message; stop and ask again if the message changes.

Use `--return-pending` for the same non-blocking approval handoff described
above.

### `magicpay confirm-action --summary <text> [--details <text>] [--return-pending]`

Request approval for a non-payment consequential action that has no more
specific typed command. Use a concise summary that names the visible action;
add details when the page context, recipient, account, or consequences need to
be explicit.

Use this only for consequential actions without a dedicated typed MagicPay
command. Payments use `authorize-payment`; wallet message signing uses
`sign-message`.

Use `--return-pending` for the same non-blocking approval handoff described
above.

### `magicpay confirm-otp --otp <digits> [--session <id>] [--request <id>]`

Confirm the active pending runtime request by OTP. Use this only after a
pending approval request exists and only when the user provides the OTP for
that request. By default the command uses the active workflow session and
`currentRequestId`; `--session` and `--request` are recovery selectors.

Do not repeat the OTP in chat, summaries, logs, saved notes, or command
reports. If OTP is invalid, expired, or exhausted, report that typed failure
and keep MagicPay UI approval available while the request itself remains
pending.

### `magicpay wait-request [--session <id>] [--request <id>]`

Resume waiting for the active pending runtime request and claim its result
when it reaches a terminal result. Run this after either MagicPay UI approval
or OTP confirmation. The command clears `currentRequestId` only after a
terminal result or unrecoverable failure; timeout leaves the request resumable.
