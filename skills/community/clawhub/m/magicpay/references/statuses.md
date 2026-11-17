# Status Meanings

Interpret a status within its returned request, run, session, or operation;
the same word is not a universal workflow transition.

## Requests and Memory

- Request `waiting_user`: preserve the exact request and follow
  [requests.md](requests.md). A generic choice also follows
  [choices.md](choices.md); payment approval is not a chat choice.
- Request `fulfilled`: consume only the stored artifact and exact continuation.
  For a choice, report the recorded selected ID, never a local draft.
  For protected Memory, resume the original materializer/resolver; generic
  request reads, waits, and claims never release the collected values.
- Request `denied`, `expired`, `canceled`, or `failed`: stop that request; do
  not fabricate a selection or present its options as a new pending prompt.
- Memory `ready`: use only the returned values for the approved current scope.
- Memory `request_required`: resolve the exact returned request, then rerun
  the same materialization or resolver input.
- Memory `fallback_required`: follow its safe fallback, without partial fill.

## Browser and payment runs

- `clicked`: dispatch occurred; settlement remains unknown.
- `click_uncertain`: dispatch may have occurred; reconcile and never replay.
- "merchant_confirmed": the merchant visibly confirmed the submitted checkout.
  Close the workflow with structured `checkoutOutcome`; provider settlement may
  remain pending on the exact operation.
- `awaiting_approval`: retain stable operation-owned `approval.requestId`, then
  continue the same remote session using the distinct routable UUID
  `approval.runtimeRequestId`; do not create another approval. If the runtime
  request is missing, approval setup is blocked: do not tell the user an
  approval is available or invent its URL.
- Payment-run `running`: carry the same `runId` and `nextProgressCursor` into
  `wait_payment`; it is neither failure nor permission to restart.
- Payment-run `waiting_for_user`: report the exact returned request URL and,
  immediately call `wait_payment` on the same run; its one bounded call polls
  every three seconds while approval is open. Never require a chat reply or
  create a replacement request.
- Payment-run `reconciliation_required`: reconcile only its exact returned
  operation. A missing x402 result after financial completion does not itself
  authorize another purchase.
- funding_required: only authoritative insufficient unified user balance
  automatically opens `show_topup`. Durable top-up settlement may wake only the
  same approved, unchanged, definitely-not-submitted operation; continue its
  same run and never replace it.
- service_unavailable with card-pool insufficiency: this is a temporary card
  service capacity issue, not a user-balance funding request. Do not call any
  top-up or fresh payment tool; direct the user to support@magiccard.ai.
- `revoked`: canceled pre-submit approval authority. The historical approval
  decision may remain auditable, but it cannot resume, materialize, or authorize
  any payment operation.
- `external_not_submitted`: follow only the exact operation's returned retry
  guidance; provider non-submission is not permission to create a replacement.
- `external_pending`: a direct transfer was submitted successfully and is in
  normal blockchain confirmation. Report that no action is needed and MagicPay
  will notify the user after settlement, stop foreground polling, and retain the
  exact operation/session. Only `completed` proves settlement.
- `reconciliation_required`: reconcile the same operation only.
- `completed`: terminal only when the operation/provider evidence agrees.
- `definitively_failed`: terminal for that operation attempt. Do not retry when
  `retry.allowed:false` or the failure is non-retryable. Failure alone does not
  prove release; follow the terminal closure rules below.
- `canceled`: terminal for workflow authority immediately. A separately
  preserved dispatched or uncertain operation may still be nonterminal and
  require same-operation reconciliation; cancellation does not release its
  held Ledger reservation by itself. Use the current operation, settlement and
  cleanup outcome for that payment. `freshStartAllowed` is a legacy summary,
  not permission to browse, recover fields or perform another authorized task.
- `cleanup_pending`: the workflow is canceled and background recovery is checking
  the exact reservation. Read its status when useful; a second cancellation or
  continuous foreground polling is not required.
- `failed`: the workflow closes through `fail_checkout_session` with one exact
  failure code and stable idempotency key. A separately unresolved or possibly
  dispatched operation remains bound to the returned same-operation
  reconciliation action; failure alone does not release it or authorize a new
  payment. Distinguish safe replacement after release from a separately
  authorized additional purchase below.

## Safe replacement after terminal release

To establish that a replacement has no unresolved exposure from the old
payment, require its workflow to be durably closed and its current result to
return all of:

- `cleanupDisposition`: `released_pre_submit` or `released_after_failure`;
- `settlementStatus`: `failed` or `not_started`;
- `nextAction: none`.

`released_pre_submit` proves the exact non-submitted operation authority or
hold was released. `released_after_failure` proves the exact submitted native
operation is definitively failed and its own Ledger release consequence was
recorded. Neither disposition makes the old attempt retryable or releases
unrelated reservations. Missing or unresolved evidence forbids treating a
replacement as safely released. These facts do not themselves authorize spending.

## Explicit platform-liability release

`cleanupDisposition: released_platform_liability` with the workflow canceled,
`CARD_CANCELLATION_WRITTEN_OFF`, and `nextAction: none` confirms that the
customer's hold was released and MagicPay assumed the unresolved cost. The
issuer outcome can remain pending. Do not call this pre-submit release or a
verified issuer decline. Keep the old checkout closed and never repeat its Pay.
If the user still wants the purchase, verify merchant failure/no booking, then
use fresh exact payment approval within the user's budget and available issuer
funding. Link the original operation in the new session's metadata as
replaces_payment_operation_ref. This release does not reset spend limits or
create card liquidity. A still-pending ledger release does not qualify.

## Separately authorized additional purchase

The legacy `freshStartAllowed:false` does not block another task or purchase.
Unrelated purchases follow normal authorization. For another purchase of the
same item or service while the first is unresolved, the user must explicitly
authorize the additional spend, including the possibility that both purchases
charge. Explain that possibility once; if the user already accepted it, do not
ask again in chat. Missing output, elapsed time, cancellation, or a generic
"continue" alone is not that authority.

Use a new workflow, request, approval, operation, reservation, run and idempotency
identity, including a new seller idempotency key where supported. Apply the new
purchase's bounded debit ceiling and normal MagicPay approval/policy, available
balance and spend limits. The old unresolved reservation still reduces available
funds. Never reuse old authority or identities, release an unresolved hold,
resubmit the old operation, or infer permission for repeated additional purchases.

Keep the old workflow canceled when canceled, with its exact operation available
for reconciliation. Do not make manual recovery of that old payment or continuous
foreground polling a prerequisite for the authorized new purchase. Background
recovery continues independently of the new payment.

Status, cancellation, and reconciliation reads remain silent supporting calls.
An error, hard stop, separately pending reconciliation, or required user action does not
request a widget; report it in normal conversation unless the user separately
asks for the corresponding view. Present a returned `hostedUrl`, `hosted_url`,
or `app_url` for its stated purpose. An activity/status link is not a direct
approval link. When an exact runtime request exists but its `request_url`
could not be created, report the link failure and retain the same request/run;
do not claim Telegram delivery without evidence. A missing runtime request is
an approval-setup failure, not a prompt to approve elsewhere. Valid approval
links still use the immediate same-run wait above, with no chat reply required.
For funding presentation, follow [payment-operations.md](payment-operations.md#funding);
for new choices, follow [commands.md](commands.md).
