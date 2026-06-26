# MagicBrowse Guardrails

The Hard Rules from SKILL.md, expanded to long form.

## Consequential Actions

`magicbrowse` can navigate, inspect, draft, and prepare. It must not
silently commit an account-affecting or irreversible action.

Stop and ask the user before:

- submitting a form;
- posting or sending content;
- accepting terms or confirming consent;
- changing account data, account settings, permissions, or privacy
  controls;
- booking, buying, ordering, subscribing, or paying;
- deleting, overwriting, publishing, or otherwise modifying remote
  data.

After approval, re-run `observe` so the target-id and visible state are
fresh, then execute only the exact final action the user approved. If
the page changed meaningfully, ask again rather than widening the
approval.

A successful typed MagicPay approval counts for the exact payment, signing,
or confirmation action it approved. Use it only while the approved page facts
stay unchanged.

When LLM-backed `act` reaches this boundary, it returns
`status: needs_approval`. Treat that as a controlled stop, not a
browser failure.

## Memory Fill Boundary

The `magicbrowse` skill ends at the boundary of any memory fill.
It gets the host *to* the form; it never *into* it. Reach the page,
stop before entering Memory values, and return the handoff to the
orchestrator or MagicPay Memory fill workflow.

**Forbidden field categories.** Do not use `act`, `type`, `fill`, or
`select` on:

- **Login / signup credentials.** Email, username, password, OTP,
  TOTP, magic-link inputs, "remember me" toggles tied to credential
  entry, social-auth connectors that solicit OAuth credentials in the
  same flow.
- **Identity-document fields.** Passport number, national ID number,
  KYC/AML address, date of birth tied to a verified identity,
  document expiry, document-issuing country, machine-readable-zone
  inputs, photo-of-document upload buttons.
- **Payment-card and banking fields.** Cardholder name when bound to
  the PAN, PAN, CVV/CVC, expiry, IBAN, BIC/SWIFT, sort code, routing
  number, account number, billing-address fields when they are part
  of the card form.
- **Vault- or secret-store-sourced values.** Any value whose origin is
  the user's Memory, password manager, or other Memory store, even if
  the field type itself looks generic.
- **Any value you do not legitimately have.** If you do not know it,
  do not guess and do not fabricate.

The planner and navigator already refuse credential entry at the LLM
layer. This guardrail raises that refusal from a probabilistic LLM
behaviour to a host-facing contract: even if the planner *would*
refuse, the host must not attempt it. Stop before entering Memory-managed
values, surface the situation to the user or orchestrator, and never invent
or placeholder Memory values. Be honest about what `magicbrowse` cannot
do.

The narrow exception is **placeholder values to traverse an ordinary
screen during non-committal exploration** (e.g. typing dummy passenger
names to reveal the final fare in a flight-price check). Do not type
real identity data; use semantically obvious placeholders. The moment a
field starts asking for something Memory-managed, stop. If the flow is
expected to submit real data — booking, ordering, registering — do not
placeholder those fields at all: they are Memory-fill handoff targets,
and placeholder values left in a real submission corrupt it. End the
granule at that form instead.

## Act Before Snapshot Primitives

Within MagicBrowse, `act` is the default primitive. Do not begin a task
with `observe` plus `click`/`type`/`select`/`press`/`fill` unless `act`
has already failed to make progress on the same goal, or unless the
operation is deliberately a single-element recovery step.

The navigator has the current page context, the natural-language goal,
and its completion check in one planner loop. A host that starts from
snapshot ids has to preserve that intent externally while remembering
that every id expires after any page mutation or expected state change.
That is a recovery path, not the happy path.

When primitives are necessary, re-run `observe` after every page
mutation and use the fresh target id only for the next primitive.
For deterministic `click`/`type`/`fill`/`select`/`press`, a
`status: "completed"` result means the direct action was dispatched through
the action layer. It does not certify that a higher-level page condition is
now true. If the next step depends on changed page state, branch on a fresh
`observe` result. If the task needs its own completion check, use `act` with a
checkable terminal condition rather than treating a primitive result as task
success.

## Singleton Session

`$MAGICBROWSE_HOME/current-session.json` (default
`~/.magicbrowse/current-session.json`) is a singleton pointer. Concurrent
workflows on the same home silently overwrite each other's session state —
the second `launch` becomes the current session, the first one is orphaned
mid-task.

For multi-tenant or parallel use, set a distinct `MAGICBROWSE_HOME` per
workflow, or do not run the tasks in parallel. Per-user tools that may run
more than one `magicbrowse` flow simultaneously must scope homes per request,
not share the defaults.

This is not a security boundary — it is a correctness boundary.
Sharing default homes between concurrent workflows produces
silent cross-talk, not visible errors.

## Browser Authority

Use a fresh owned browser session by default. Existing CDP endpoints,
named profiles, and explicit `--user-data-dir` paths may already be
logged in to real accounts. Acting through them inherits that browser's
authority even though `magicbrowse` never receives the password.

Only use `magicbrowse attach`, `--profile`, or `--user-data-dir` when
the user explicitly approves that browser/session for the current
task. The exception is the browser child MagicPay launched inside the
current approved product workflow: attaching to it is the normal
in-workflow path for preparing pages in the same browser, not an
external attach that needs separate approval. Keep CDP endpoints
private and do not paste them into shared logs. Close or detach when
the overall browser workflow is done, and start a fresh session for
unrelated work. If MagicBrowse handed the current page to
another tool or the user, wait until that handoff finishes before closing a
MagicBrowse-owned disposable browser. Do not close an external/user-owned
browser or approved attach without explicit teardown approval.

## Page Context And Screenshots

LLM-backed `act` sends page state to the gateway. `act --use-vision`
can include screenshots. Treat both as external processing of the
current page context.

Avoid private, sensitive, or unrelated pages unless the user approves
that workflow. Do not use vision mode on sensitive pages unless it is
explicitly required and approved. At memory fills, stop and surface
to the user.

## CAPTCHA And Auth Walls

Both the planner and navigator are instructed to refuse to attempt
credential entry or solve CAPTCHAs. When `act` runs into either, it
returns `status: needs_handoff` with a `finalMessage` describing the
wall and a machine-readable `handoff.kind` — *not* `status: failed`.

- **Do not** retry the same `act` after a CAPTCHA or auth-wall handoff.
  The same prompt will hit the same wall.
- **Do not** try to solve CAPTCHA through `magicbrowse`. MagicBrowse does not
  solve CAPTCHA.
- **Do not** invent credentials, identity values, payment values, or
  CAPTCHA answers to get past the wall. Do not placeholder Memory-managed
  data either.
- **Do** surface `finalMessage` to the user or orchestrator and branch on
  `handoff.kind`. For `memory_fill`, pass
  `{ kind: "memory_fill", resumeObjective }` to the approved
  Memory fill workflow, then call `magicbrowse act` with that
  `resumeObjective` after the fill completes. For `captcha`, have the user
  or an external solver clear it; after a successful solve, run
  `magicbrowse mark-captcha-resolved` before the next `act`. For `auth` or
  `identity_verification`, stop for the user or approved flow. If the next
  `act` still returns `needs_handoff`, the wall was not cleared; do not
  re-mark.

## Diagnostics

- `magicbrowse browser-status` inspects the live browser/page/runtime
  state. Use for debugging, not as a control-flow signal.
- `magicbrowse doctor` inspects the gateway config. Use after
  `magicbrowse init` if `act` reports a missing-key error.
- `magicbrowse close` is teardown or recovery, never a success
  signal. Task success or stop reason comes from the `act` `status`;
  `finalMessage` explains that outcome. Use it after handoff work is done,
  not as part of Memory handoff completion itself.
- `magicbrowse act` can exit `0` for controlled stops such as `blocked`,
  `needs_handoff`, and `needs_approval`. Branch on `status`, not on the shell
  exit code.

## Ask The User When

- `doctor` fails and there is no configured API key available;
- the environment cannot launch or attach to a Chrome session;
- the task requires `attach`, `--profile`, or `--user-data-dir`;
- `--use-vision` would expose screenshots of a private or sensitive
  page;
- `act` returns `status: needs_handoff`;
- `act` returns `status: blocked` because ordinary input or a
  different strategy is needed;
- `act` returns `status: needs_approval`;
- the next action would submit, post, send, save, delete, accept,
  book, buy, order, pay, publish, or otherwise commit a consequential
  change, and there is no matching typed MagicPay approval for unchanged page
  facts;
- the task crosses into a memory fill — stop and surface, do not
  improvise, guess, or placeholder Memory values.
