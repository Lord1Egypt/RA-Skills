# Direct Browser Payments

Use this path when `browserPaymentRun.status: "ready"` and
`executionMode: "agent_direct"`. The host's built-in Browser owns the live tab.
MagicPay owns the exact approval, operation, payment-scoped card, result, and
reconciliation state. Do not add a second browser controller.
If the host cannot inspect and fill the required live targets, report the
unsupported capability. Shared guidance is not proof of another host's live
browser support.

## One run, one approval

Questions during approval are normal conversation. Answer the user's actual
question using the known task state while leaving the approval open. Answer
before entering another wait, including when the message starts a new turn
after an earlier turn ended with a pending approval. Asking a
question does not approve or deny payment. If the host can interrupt a read-only
`wait_payment` call, yield to the message and resume that same run afterward.
If it cannot process messages during a tool call, use bounded waits of at most
30 seconds, within its tool budget, so control returns regularly. Keep the
same `runId` and progress cursor; a paused or timed-out wait is not a failed
payment and does not permit a replacement purchase. Use the host's normal
conversation tools; hosted chat reply tools are not required in other hosts.

Create the checkout session for the known destination. Use the Browser to reach
the actual payment-dispatch surface without activating it, then observe the
merchant/recipient, exact merchant amount and currency, recurrence, payment
type, actual final-action meaning, and the ordinary semantic roles visible now.

For recurring signup, use [subscriptions.md](subscriptions.md) to supply the
recurring terms and optional dates/hints with this same checkout.

## Fixed USD price for non-USD checkouts

For a USD checkout, pass the exact merchant money unchanged as both `amount`
and `maximumDebit`. For another merchant currency, preserve that exact local
money in `amount` and form one fixed USD `maximumDebit` before the first
`run_browser_payment` call:

1. Fetch only the direct Frankfurter pair
   `https://api.frankfurter.dev/v2/rate/{MERCHANT_CURRENCY}/USD`, replacing the
   placeholder with the observed uppercase ISO currency. Require a successful
   JSON response whose `base` is that merchant currency, whose `quote` is
   `USD`, and whose `rate` is positive. Do not use a search result, a broad rate
   table, an inverted pair, or a model-generated rate.
2. Treat the returned rate as USD per one merchant-currency unit. Apply the
   fixed 5% beta FX allowance and round upward exactly once to a USD cent:
   `usdCents = ceil(merchantMajorAmount × rate × 1.05 × 100)`.
3. Set `maximumDebit` to `{ quantity: String(usdCents), scale: 2, currency:
   "USD" }`. Never relabel the local amount as USD or compare the two atomic
   quantities.
4. Show the user the exact merchant money, the Frankfurter pair/date/rate, the
   fixed 5% allowance, and the resulting fixed USD price. If the direct fetch,
   pair validation, or calculation fails, stop before creating a payment run.

The first run call binds that fixed USD price. Reuse the same `maximumDebit`,
`clientRequestId`, and `runId` throughout approval, waits, ordinary-field
resolution, browser preparation, and exact-operation recovery. Never refetch
or reprice the same run. A decline, possible submission, uncertain click, or
reconciliation requirement never permits a replacement run or another final
click. A fresh run may use a fresh rate only when the prior exact checkout has
durably returned fresh-start authority under the normal recovery rules.

Call `run_browser_payment` once with one stable `clientRequestId`. Do not wrap it
in separate balance, capability, approval, or card-preparation calls. Approval
creates checkout authority for the unchanged merchant and payment. Honor the
returned expiry and host-required confirmations; MagicPay adds no redundant
confirmation of the same approved facts, and neither do you. After MagicPay
approval the only confirmation left is one the host itself requires for the
final action; do not ask the user to approve the same payment again in chat.
Use `browserExecution.card.billingAddress` when provided. Adapt it to the
merchant's current form; if required billing details are still missing, use
Memory or the existing input flow. Without a card address, follow the ordinary
field request as usual. Do not invent missing components or save the card's
billing address as the user's personal address. Keep the same payment run.
For a card checkout's separate receipt email, use the exact agent's ready managed
email by default. A saved personal email alone does not override receipt routing.
Use the user's personal email for account registration/ownership, login/recovery,
KYC, profiles, traveler/patient records, or a checkout field that also owns the
merchant account. Follow explicit user-selected addresses and preserve fixed
merchant identity and an address already submitted; do not default general forms
to agent email.
When one checkout email field also controls merchant login or account ownership,
use the account email and explain that receipts may go there too. Promise separate
receipt routing only when the seller provides a separate receipt field or confirms it.
For visible ordinary fields (such as billing name), use `get_memory_footprint`
before the first run: pass saved candidates as `ordinaryFields` references, or
request missing roles through `ordinaryFieldRoles`. If a role appears later,
continue this same run after its current approval is resolved; do not create a
separate Memory request while that approval is waiting. See
[Memory's direct-checkout guidance](memory.md#direct-browser-checkout).
If `CHECKOUT_MEMORY_STALE` reports changed saved details before preparation,
reread Memory under its current reuse policy and resume with current references,
the same `clientRequestId`/`runId`, and unchanged payment terms.
For receipt email precedence and an inbox that is not ready yet, follow
[invoices.md](invoices.md); inbox provisioning must not delay this run.
Never remove a previously observed role. Passwords, OTPs, identity documents,
tax identifiers, bank credentials, private keys, seeds, and unrelated secrets
are outside this payment authority. A separately authorized non-payment Memory
task follows [memory.md](memory.md); otherwise hand off safely.

| Run state | Continue with |
| --- | --- |
| `waiting_for_user` | Present the exact approval URL; wait on the same `runId`. |
| `ordinary_field_required` | Resolve only the returned roles and resume the same run; this is not a new payment approval. |
| `preparing_browser` | Wait on the same run. |
| `ready_for_browser` | Fill the unchanged checkout in the exact live tab. |
| `external_pending` | Reconcile the same operation; never click again. |
| `reconciliation_required` | Reconcile the exact operation; never replace it. |
| `completed` | Report success only from the durable completed operation. |

If a pending merchant page later confirms success **or displays a payment error**,
report that observation with the original execution-attempt and result identifiers.
Keep the original click and submission posture; later merchant failure is not proof
that the issuer never received a request. Include available subscription/invoice
details for success, or the value-free visible error and observation time for failure.
Continue reconciliation of the same operation. Explain a visible failure promptly;
do not promise eventual confirmation while the checkout reports an error.

A paid receipt or a paid booking confirmation is a successful merchant payment
even when ValutNet keeps the purchase row `PENDING`; the associated fee may show
success first. State the successful purchase clearly, including its amount and
booking/order reference. Re-record the later `merchantOutcome: success` with the
original run, execution attempt and client result ID. MagicPay finalizes that
same operation using the matched card debit and releases unused authorization.
Do not close only the workflow and leave the payment observation as pending.
Provider clearing can be described separately when relevant, without presenting
the confirmed purchase as failed or requiring another Pay. Omit internal
operation/request IDs from normal success messages; include them only for an
explicit support/debugging request.

## Browser ownership and rendered state

Use the host's normal visual and interaction capabilities for the unchanged
approved checkout. Inspect the intended visible fields and final control; a
hidden DOM entry or accessibility presence alone does not prove visibility.
Before recommending accommodation or proposing a booking payment, inspect the
seller's overall and cleanliness ratings and material recent review concerns.
Apply the user's quality requirements before selecting the offer, and disclose
poor ratings or cleanliness concerns alongside the price, deposit, remaining
payment and possible surcharges. Attribute review reports to the seller or guests;
do not present them as independently verified conditions.
Use screenshots freely as normal visual perception before and after filling,
without a prescribed count or field order. After a page transition, reacquire
current controls. Stop submission if the bound payment facts changed.

For travel, default optional extras off unless the user or applicable saved
preferences request them: keep included cabin baggage; decline extra checked
bags, insurance, disruption assistance, paid seats, priority, meals and donations.
Choose the base fare meeting the stated requirements. Do not ask a separate
question for every upsell; summarize these defaults once with the final itinerary
and total. Ask only for a mandatory unresolved choice, material fare restriction,
budget change or preference conflict. With children, respect required seating
rules and choose free adjacent assignment where available; never silently accept
child/adult separation or an unavoidable paid seating charge.

Resolve known tax/shipping choices before approval when possible. If the final
price changes later, the old approval does not cover it. Record the observed
`not_submitted` result and finish cleanup; follow [safe replacement after terminal
release](statuses.md#safe-replacement-after-terminal-release) before starting fresh.
When no final payment action was activated, record `result: "not_clicked"`,
`submissionState: "not_submitted"`, and `nonSubmissionReason: "checkout_total_changed"`
so the exact cause survives cleanup. Never use this reason after a click or with
uncertain submission.
When the same purchase still fits the user's existing budget, continue with the
final total and a fresh exact MagicPay approval/policy, without another chat
confirmation. Stabilize the final total first. Retain host-required approvals;
ask the user only for an above-budget total or a material product/recurrence
change. Uncertain submission or unresolved cleanup keeps the original operation
in recovery; this is not permission to retry a decline or a canceled purchase.

Payment-method selectors, accordions, and next/continue controls may reveal a
form without submitting payment. Determine the actual action from the rendered
page, not its label. Do not record these intermediate interactions as payment
dispatch. Correct merchant validation in the same run; refill only allowed
fields that current evidence shows need correction, without unbounded loops.

Fill returned values using host-supported browser input for the exact approved
tab, including documented host REPL calls where applicable. A clipboard or focus
error from `.fill()` does not require repeating that same method. Re-observe the
intended visible, enabled field, reacquire its current frame and control when
needed, and use supported targeted native per-key input. Click the intended
control only if needed. This applies to ordinary fields and authorized payment
fields, including iframe fields. Replace partial input only when current
evidence shows it needs correction. Verify ordinary field values normally;
for payment credentials, verify presence and merchant validation without
reading values back.
Do not invent a generic sensitive-fill API, inject credentials with arbitrary
page-evaluation code, or switch to raw browser-protocol control.
Keep final dispatch separate from fill and navigation: invoke the identified
payment control once in an isolated host action.

Native screenshots may incidentally contain payment fields before or after
fill. Read visible controls, amounts and validation normally. Keep credentials
out of exported evidence; ordinary non-sensitive screenshots may be shared when
useful or requested. The V1 visibility boundary is defined in the skill router;
neither a screenshot nor a successful fill authorizes submission or proves
settlement.

## Pre-dispatch Browser interruption

A tab binding can become stale without invalidating the Browser binding. When a
fill/navigation call is definitely before the isolated final action, do not
call `record_browser_payment_result`, fail, cancel, release, or create another
run merely because of the interruption. Recover within the host's documented
capabilities. If only a field action failed, keep the live page and use the
targeted input recovery above. Do not use `goto(currentUrl)` as a reload or
input-recovery step: a checkout can depend on POST state that a new GET loses.
If the tab binding is stale:

1. discard only the stale tab binding;
2. reacquire the exact live tab from the existing Browser binding, or reopen
   the same approved HTTPS checkout when that tab no longer exists;
3. replay the same `clientRequestId` and `runId`;
4. re-observe and refill only missing allowed fields; and
5. continue with the same execution-attempt ID.

If bounded recovery cannot restore the unchanged pre-dispatch checkout, hand
the exact checkout to the user without replacing the payment. Do not infer that
a tab or browser can be reopened after possible dispatch.

If the interruption overlaps the isolated final-action call, record
`click_uncertain` and reconcile the same operation. Never reopen for another
click. A timeout or missing output is not permission to retry dispatch.

## Challenges and unusual states

Handle challenges under the host's capabilities and policy; hand the same tab
to the user when needed. A pre-dispatch challenge does not fail or replace the
payment. After any possible dispatch, observation is read-only and recovery
stays with the same operation.

## Record the action once and update later observations

After submission or a human handoff, inspect the current rendered page before
asking for more login or payment steps. Use a fresh screenshot when useful;
recognize a completed receipt or thank-you page in its checkout context.
For a card payment, `list_card_transactions` reads the card associated with the
same checkout session ID. Compare nearby timestamps, currency and approximately the
charged amount (including ordinary fees or FX differences). Assess merchant
descriptors in context: a processor, trading name or abbreviated label may differ
from the checkout name. Use your judgment; no exact-name match is required for
this observation. A pending row or empty page may simply need more time.
Report merchant confirmation and a probable card charge clearly, then read or
reconcile the original operation for its accounting state. Do not request login
or repeat checkout merely because that accounting update is still pending.

After the final action, observe fresh rendered state until a receipt, explicit
error, challenge, or an observation deadline (normally up to 60 seconds). A
processing spinner is intermediate. Use screenshots freely and inspect the
existing browser's network inventory for payment/tokenization failures when
useful. Separate the click, merchant request, merchant outcome and issuer outcome;
a merchant processing error plus no issuer row does not prove non-submission.
Record pending if the observation deadline expires, then continue read-only
observation on the same attempt. Call
`record_browser_payment_result` for the exact run and execution attempt.
Observation failure is not permission to click again:

- `not_clicked` only when the isolated payment-dispatch control definitely was
  not activated;
- `clicked` when it was activated, with the separately observed submission and
  merchant outcome; or
- `click_uncertain` when activation may have occurred.

Pass an ordinary receipt address only in `checkoutEmail`, never in
`valueFreeEvidence`. Approval, card materialization, field fill, click, and
merchant visibility are not settlement. When the composed result is
`completed`, stop payment execution; do not call a second checkout closer.
Finish any product delivery requested in the original task: inspect the
merchant's visible delivery instructions and follow its explicit download or
success link, including one on the original product page when the payment
confirmation has none. Retrieve and present the original purchased file using
the host's supported file/result surface without waiting for another human
prompt. Do not guess hidden URLs, submit checkout again, or create another
payment. If no usable delivery route is available, report payment completion
and product retrieval as separate outcomes with the observed next step. A
purchased PDF is the product, not an invoice; do not attach it as a receipt.
Handle returned `invoiceFollowUp` and later original-document processing through
[invoices.md](invoices.md), without waiting for mail or AI before the payment reply.
