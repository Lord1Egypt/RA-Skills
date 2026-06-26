# MagicPay Boundaries

## What This Skill Owns

- Start or continue the MagicPay product workflow session.
- Launch or attach an approved browser as a child resource inside that active
  workflow session.
- Plan Memory field fill with `magicpay plan-fill`.
- Apply approved Memory values with `magicpay apply-fill` without submitting.
- Return post-fill page continuation to the page-control owner.
- Run typed protected action approvals through `authorize-payment`,
  `sign-message`, or `confirm-action`.
- Complete the MagicPay workflow with `magicpay end-session`, then return
  browser lifecycle decisions to the caller-owned browser tool or
  orchestrator. `magicpay close` closes or clears only the browser child.
- Recover from a confirmed real CAPTCHA on the current browser child with
  `solve-captcha`, then call `magicbrowse mark-captcha-resolved` before
  continuing through MagicBrowse when MagicBrowse owns the next step.

## Consequential Action Approval

Before any submit, protected action, purchase, login, identity submission,
account change, or other consequential action, get the matching typed
MagicPay approval for:

- the current site or merchant;
- the exact action to be taken;
- the visible amount, account, identity, or other data being submitted;
- whether the user wants final submission now.

MagicPay fills planned fields only. After `magicpay apply-fill`, continue with
the page-control owner from a refreshed page state. Do not treat filled fields as
approval to submit.

After typed approval, proceed with exactly that action; do not ask for a
second approval unless approved page facts changed. `authorize-payment` covers
the matching payment artifact use, payment form fill, and final Pay/Submit
while `amount`, `currency`, `recipient`, and `recurring` stay unchanged.
`sign-message` covers the exact message only. `confirm-action` covers only the
summarized non-payment consequential action.

After any approved submit, observe the resulting page before claiming success,
progress, or failure. If the page is still on the same form with validation
errors, classify the visible result before choosing a recovery path. Do not
infer or reveal hidden Memory values from the error text.

## Readiness Rules

- Use `magicpay status` before a new MagicPay Memory fill task.
- If `status` reports a missing or invalid API key, run `magicpay init`.
- If `status` reports `cliUpdate`, use only
  `npm i -g @mercuryo-ai/magicpay-cli@latest`, then rerun `status`.
- Use `doctor` only when local config still looks broken after `init`.
- Normal product work starts with `magicpay start-session` before
  `magicpay launch` or `magicpay attach`.

Do not print, log, or share `MAGICPAY_API_KEY`, the local MagicPay config
file, or CDP endpoints. The config file is `~/.magicpay/config.json` by
default or `$MAGICPAY_HOME/config.json` when `MAGICPAY_HOME` is set. Memory
item ids are operational refs: pass them only between MagicPay commands that
require them, and never show them to the user or put them in reports/external
logs. If the environment is shared or compromised, stop and ask the user to
revoke or rotate the key.

## Browser Authority

Use `magicpay launch` or `magicpay attach` only inside an active product
workflow session. Use `attach` only for the private browser/session the user
approved for this task. A CDP endpoint inherits the authority of any logged-in
browser state. Keep endpoints private and do not paste them into shared logs.
Run `attach` when MagicPay is not yet bound to the approved browser child, or
when the CDP endpoint changed. Re-attaching the same endpoint is allowed but
is not required as a ritual.

Browser teardown remains outside MagicPay's product-session authority.
`magicpay close` closes or clears the browser child while keeping the product
workflow active. If the browser was launched as an owned disposable session by
another tool, that tool can clean up after the overall task is done. If the
browser was external, user-owned, or handed to the user for inspection, leave
it open unless the user explicitly approves teardown.

## CAPTCHA Recovery

Only call `magicpay solve-captcha [--timeout <s>]` when a real CAPTCHA is
confirmed present on the current browser child inside the active product
workflow. Do not use it as page waiting, challenge detection, or a generic
retry.

When the next step is owned by MagicBrowse and the solve succeeded, call
`magicbrowse mark-captcha-resolved`, then continue with
`magicbrowse act "continue..."`. The marker only tells MagicBrowse that an
external participant resolved CAPTCHA for this page; MagicBrowse still checks
the actual page state and must stop again if CAPTCHA or human verification is
still visible.

## Memory Fill Rules

- Start from `magicpay plan-fill` on the current page, not from old
  assumptions. Use `--planner-hint <text>` only for short human-readable
  context when needed.
- Do not apply a stale plan after page changes.
- Keep the plan request small: purpose/options only, never raw values, target
  matches, Memory catalogs, materializers, browser writers, or page target
  lists.
- Treat `payment_card.authorization_required` as a non-blocking Memory
  availability state: the card exists, but provider-backed card handles remain
  hidden until `authorize-payment` succeeds in the active workflow session.
  Never ask for raw card details or route around this state through lower-level
  materialization calls.
- Use `magicpay apply-fill` to fill and stop before final commitment controls.
- Use `magicpay fill-field` only as value-free recovery when the higher-level
  plan/apply path missed a visible field or chose the wrong target. The agent
  may bind Memory refs to observed target refs; it must not pass raw values.
- If Memory candidates are ambiguous, explain the displayed candidate facts to
  the user and submit the selected `choiceId` with
  `magicpay choose-memory --choice <choiceId>`. Do not use labels or list
  positions as CLI selectors.
- If apply reports that the page changed, refresh the page state and rerun
  `magicpay plan-fill` before retrying.

## Protected-Action Rules

- Start typed action commands only when an active product workflow session
  exists.
- Before `authorize-payment`, collect visible `amount`, `currency`,
  `recipient`, optional `description`, and optional `recurring` from the
  current page and the user's task.
- Prefer merchant/payee names over payment processor names. Use page title,
  host, or URL only as supporting signals unless they clearly identify the
  merchant.
- Ask the user when amount, currency, merchant/payee, recurring status, or
  task/page facts are missing, conflicting, or ambiguous.
- Use `magicpay authorize-payment` for payment authorization.
- Use `magicpay sign-message --item-ref <walletItemId> --message <text>` for
  wallet message signing, and ask again if the message changes.
- Use `magicpay confirm-action --summary <text> [--details <text>]` only for
  consequential actions without a more specific typed command.
- Keep `itemRef` on the existing selector path. Do not put it inside
  `params`, and do not change how MagicPay discovers or selects Memory items.
- For approval handoff, add `--return-pending` to the typed action command,
  then either MagicPay UI approval plus `wait-request` or OTP confirmation
  plus `wait-request`.
- Do not ask for OTP until a pending approval request exists. OTP is optional,
  not a replacement for MagicPay UI approval.
- Do not print, log, summarize, save, or repeat OTP digits. Treat them as
  sensitive user input.

## Secrecy And Safety

- Never type, print, summarize, or log protected values manually.
- Never type, print, summarize, or pass card PAN, CVV, wallet private keys,
  passwords, or other protected values through action params.
- Do not pass raw Memory values through chat, logs, reports, summaries, or
  public command arguments.
- Never print, log, summarize, or share `MAGICPAY_API_KEY`, local config, or
  CDP endpoints. Memory item ids may be passed between MagicPay commands as
  operational refs, but never show them to the user or external services.
- Never include OTP digits in logs, reasoning summaries, saved notes, task
  reports, or command summaries.
- Base progress claims on the visible form state.
- Base post-submit success claims on a fresh observed result page, not on the
  click/submit action itself.
- After page-level changes, rerun `magicpay plan-fill` before acting on old
  fill plans.

## Ask The User When

- a browser-dependent step is needed but there is no browser child and neither
  `magicpay launch` nor an approved private CDP endpoint is available;
- the browser/session to attach was not explicitly approved for this task;
- the next step would submit, login, purchase, send identity data, change an
  account, run a protected action, or otherwise commit a consequential action,
  and there is no matching typed approval for the unchanged current facts;
- payment authorization facts are missing or ambiguous: final amount,
  currency, merchant/payee recipient, recurring status, or a conflict between
  the user's task and the visible checkout page;
- Memory planning remains ambiguous or unavailable;
- approval reaches a terminal blocked state;
- client-side validation or merchant-specific recovery needs a human choice.
