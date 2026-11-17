# Subscriptions

Inspect the final visible offer before classifying a Stripe link. Stripe Payment
Links and Checkout can sell recurring plans or one-time purchases; the hostname
and a save-card checkbox do not establish a subscription. Look for the billing
period, renewal language and selected plan/quantity. Paying an existing invoice
is payment of that invoice, not a new subscription signup.

When comparing plans, respect the user's billing cadence and amount due now;
an annual plan is not a monthly option because its monthly equivalent fits a
monthly limit. Ask one short region or ecosystem question when that changes the
available offer or price.

Create a checkout with `type: "subscription"`. Recurring intent follows the
session. On `run_browser_payment`, use `paymentType: "subscription"` and the
actual final action, including `subscribe`. Payment and recurring terms appear
in one MagicPay approval; continue the same run after approval or funding.

Provide optional `subscriptionDetails` at checkout creation or on the browser
payment run: `recurringAmount`, `recurringCurrency`, `intervalUnit`, `intervalCount`,
`recurringAmountKind`, optional legacy `interval`, `trialEndAt`, `nextRenewalAt`,
`introductoryPeriod: { count, unit }` for a stated paid introductory price,
`expiresAt`, `autoRenews`, `cancellationUrl`, `cancellationHint`, `serviceLogoUrl`,
and `estimatedRenewalUsd`. Decide reasonable dates from the checkout and your own
judgment. Missing values are fine; no invoice, proof upload or separate date
verification is needed. For non-USD renewals, the USD estimate should describe
the future recurring charge, which can differ from today's trial/discount.

Set recurring money to the actual full charge per billing period, not the amount
due today and not a manually divided monthly number. A $240 annual plan uses
`recurringAmount: 240`, `intervalUnit: "year"`, `intervalCount: 1`; $60 every three
months uses `intervalUnit: "month"`, `intervalCount: 3`. MagicPay stores a monthly
equivalent separately. Preserve the observed currency, quantity, tax qualifiers,
introductory price and setup fee. Use `recurringAmountKind: "variable"` for
usage-based/mixed pricing, or `"unknown"` when the recurring price is unavailable;
do not substitute zero or a first-charge discount. Reinspect changed plan or
quantity before submission; changed money, interval count or trial end requires
updated approval terms on the existing checkout. Never create a second purchase
to get past a conflict.

Use `trialEndAt` only for a real free trial. A paid introductory period is not
a trial; provide its observed duration through `introductoryPeriod` when known.

For Stripe-hosted checkout, keep `merchantDomain` equal to the checkout host and
supply the separately observed `sellerDomain` and `sellerName` on
`run_browser_payment` when known. Do not use Stripe as the seller or invent an
order reference from a URL. Missing seller identity may require explicit
attachment to the exact operation rather than automatic email matching.

Logos and unsubscribe hints are optional. Use a public HTTPS logo observed on the
actual service, without credentials, signed links or a separate search detour.
If unavailable, omit it and continue; MagicPay shows initials. Provide a short
plain-text `cancellationHint`, for example “Settings > Billing > Manage plan >
Cancel subscription; choose cancel at period end to keep paid access.” If it is
unknown, leave it absent; the UI supplies a general guide. Never invent a portal
URL. A missing logo, hint or invoice must not delay the payment reply.

For a zero-due enrollment that the user will complete manually, create a
subscription checkout session at the exact inspected URL, then call
`request_subscription_enrollment` with `amountDueNow: 0`, `executionOwner: "user"`,
a stable `clientRequestId`, full recurring amounts and intervals, and
`billingTerms` containing deferred fees, usage prices and included allowances.
Follow the same approval request with `get_request` and `wait_request`. The user
enters their own card and submits at the merchant. After observing the result,
call `complete_checkout_session` with `enrollmentOutcome`, including the exact
request ID, approved terms hash, checkout URL and observed outcome. This records
enrollment separately from settlement and releases no MagicPay card. Preserve an
ambiguous signup for reconciliation; never submit a second enrollment.

The positive-charge browser run still rejects zero. Automatic zero-due card
provisioning is unavailable. Never invent a nominal charge or weaken the amount.
A signup does not prove that the retained card or future renewal works.

After signup, report updated details with `record_browser_payment_result`.
Dates and hints are editable metadata; commercial amounts and recurrence still
belong to the approved payment. Save any original invoice to the exact operation/session using
[invoices.md](invoices.md), without waiting for extraction or replacing the
browser amount with a missing AI value. The saved subscription links to that same
original or hosted invoice; say it is attached only after the returned evidence
confirms it. The first invoice does not stand for later renewal invoices.

Use `list_subscriptions` or `show_subscriptions` to find saved subscriptions,
renewal/expiry dates and cancellation progress. An expected renewal date is a
reminder schedule, not proof that a merchant charge settled.

When the user asks to cancel:

1. Call `cancel_subscription({ subscriptionId })` for current details and hints.
2. Use the host browser to unsubscribe at the merchant. Hints are optional
   reference information; find the service's account/billing settings when they
   are missing or stale. Never invent a management URL or buy again. Reuse an
   existing signed-in browser session and prefer keeping remaining paid access.
3. If login is required, follow [Memory browser collection](memory.md#browser-collection-use-once-and-save)
   for this exact site and account: value-free footprint, matching saved details
   with permission, then the resolver-owned secure request for only missing
   required login fields. Use once is allowed; saving remains optional. Never
   request passwords or verification codes in chat or record them in notes.
   If Memory is denied/unavailable or secure input cannot complete, ask the user
   to sign in directly in the merchant browser. Missing credentials are a user
   step, not a reason to claim cancellation or repeat a denied request.
4. For MFA, CAPTCHA, inaccessible email, account mismatch or a material choice
   such as a cancellation fee/immediate loss of paid access, report `needs_user`
   with the exact safe page and action. Unavailable agent email does not rule out
   other legitimate account-access paths. A merchant failure without a current
   user action is `unsuccessful`. Keep renewal unchanged and avoid retry loops.
5. After the user completes that step, reread the same subscription and browser
   state and continue. If a cancellation click had an unknown result, inspect
   renewal state before submitting again. Do not create a replacement signup,
   payment, card closure, account deletion or refund.
6. Call the same tool with `outcome: "cancelled"` or `"already_cancelled"`, an
   expiration date if known, and a brief note. Your observation is sufficient;
   no additional backend evidence verifier is needed. If login or another step
   needs the user, report `"needs_user"`; otherwise report `"unsuccessful"` and
   the reason and next step. Neither outcome turns renewal off. Read back the
   saved result and tell the user whether renewal remains active and when paid
   access ends, if known. Notes are brief and contain no credentials or signed links.

If citing a screenshot as cancellation evidence, inspect that exact image and
confirm it shows the relevant subscription and renewal state.

If cancellation is not visibly complete, save a short `evidence` observation and `nextAction` on the same subscription. Choose `nextCheckAt` only when a follow-up time is useful. You may link an existing `supportSendId` and a short `supportDraft`; use agent email with the normal send approval if contacting the provider. A prepared or uncertain email is not a submitted case: read that same send before claiming that the provider is handling cancellation. On a reply notification, read the linked correspondence and cancellation history, interpret the provider's message, and report the next outcome. Acknowledgement alone does not establish cancellation. The agent decides what to ask the provider and whether another follow-up is needed; MagicPay only keeps the progress and correspondence together. If later evidence contradicts a saved success, reopen that subscription and say renewal is unconfirmed until resolved.

The UI Cancel button opens a modal with a prompt to copy into an agent. Opening
or copying it does not cancel the merchant subscription. Cancellation does not
create a payment or a new signup. Future reminders stop after reported success;
paid access remains visible until the saved expiration date.

Reminders use the saved renewal schedule and existing notification preferences.
For a known USD charge or USD estimate they include the current balance
shortfall. Unknown prices/balances still allow a reminder without inventing a
minimum top-up. The cron does not charge, cancel or top up anything.
