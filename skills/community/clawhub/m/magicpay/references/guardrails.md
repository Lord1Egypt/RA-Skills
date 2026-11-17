# Guardrails

- The host browser is the only page-control owner.
- One-time card values appear only after finalized payment approval; Memory
  values follow their own exact resolver and approval policy. Neither grants
  authority for a different task or target.
- Durable state is remote. Keep no second local workflow record.
- Changed payment facts require current authority. A document or frame rerender
  requires fresh target inspection, not automatically a replacement approval.
- Use materialized values only through the authorized host input path. Keep
  values and screenshots containing them out of replies, helper files, logs,
  telemetry, and exported evidence. The final seller deliverable from a
  completed purchase is user-owned
  output, not protected input, even when a seller names it `credentials`,
  `token`, `key`, or `code`.
- Keep an explicitly seller-declared continuation capability out of the final
  response; use it only to retrieve the final seller deliverable.
- Never treat approval, protected fill, click, page copy, or HTTP transport as
  settlement.
- Keep an ambiguous payment for reconciliation; do not repeat its payment dispatch.
- Let the host browser use its normal visual and interaction capabilities for
  ordinary and intermediate page controls. Do not turn payment-method selection,
  form revelation, navigation, validation, or correction into a payment result.
- After possible payment dispatch, take a bounded fresh observation and record
  the exact result. `clicked` and `click_uncertain` are never replayable, even
  when observation fails.
- Bind native approval to the exact intent session, operation ID, stable
  operation-owned `approval.requestId`, and routable UUID
  `approval.runtimeRequestId`. Continue only through the composed run and its
  generic exact request; never route with the mpr_ identity or create a
  substitute approval.
- Preserve atomic quantities, direct-transfer facts, x402 URL/method/body, and
  the original idempotency key exactly. Same-operation recovery is the only
  retry path.
- Only authoritative unified user-balance funding_required may automatically
  show top-up. Card-pool insufficiency is a temporary service issue and never
  authorizes `show_topup`, a hosted top-up link, or a replacement payment.
- Funding recovery may resume only the exact operation after durable same-user
  settlement, unchanged facts and fingerprint, valid approval, and definite
  non-submission. A failed wake remains retryable coordination and cannot change
  top-up settlement truth.
- A held reservation remains held until the exact backend operation and Ledger
  projection release it. Approval expiry and cancellation are not release
  evidence.
- Honor cancellation before recovery work. A successful cancellation closes
  workflow authority even when a possibly dispatched operation remains held;
  reconcile that exact operation separately and never replay it.
- `retry.allowed:false` applies to replaying that exact failed action, not to
  screenshots, ordinary field correction, diagnosis or other authorized work.
  Do not repeat a possibly dispatched payment. For a separately
  authorized additional purchase, follow [statuses.md](statuses.md); never reuse
  any old identity or authority or treat unresolved funds as released.
