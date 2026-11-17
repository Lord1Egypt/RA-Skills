# Remote Workflow

Choose the focused contract; this map does not add a second protocol.

| Intent | Start and continuation |
| --- | --- |
| Non-payment browser form | footprint (no session) → select a clear compatible match; ask only if ambiguous → exact resolver without `sessionId` (it creates the form session) → returned request if needed → same resolver with that `sessionId` → whole-batch fill. No candidate: fill from the task, then offer Save. Chat context never replaces the footprint. See [memory.md](memory.md). |
| Explicit Save with supplied values | Resolve the entity/template → `save_memory_item` → value-free receipt. Protected values use the same save; missing sensitive input may use optional host clipboard. See [memory.md](memory.md). |
| Known checkout URL | `create_checkout_session` → host inspects actual checkout → footprint → saved billing roles as `ordinaryFields` → `run_browser_payment` → same run → host fill and one authorized final action → bounded observation → `record_browser_payment_result`. See [host-browser-payments.md](host-browser-payments.md). |
| Exact crypto or x402 request | Corresponding composed payment run → `wait_payment` on the same run → settlement/recovery. See [payment-operations.md](payment-operations.md). |
| Unknown provider | `search_provider_methods` → verify current official docs → exact request under user authority; discovery grants no payment authority. |
| Candidate sellers | Known URL → normal payment intake once; optional `check_merchant` for comparisons. Use request-specific evidence as advice; respect explicit operator denies and unsafe destinations. |
| Material shortlist | One normalized choice request → exact durable selection → selected branch only. See [choices.md](choices.md). |

For travel, decline optional baggage, insurance, paid seats, priority, meals,
donations and assistance unless the user or applicable saved preference asks for
them. Keep included cabin allowance, meet the requested fare requirements and
mandatory child-seating rules, and summarize omitted extras once with the total.
Do not ask a separate choice for every upsell.

The host owns browsing. MagicPay owns authorization, materialization, and durable
payment state. A Memory fill is not a new submit authority; an intermediate
checkout control is not necessarily payment dispatch. After possible dispatch,
do not click again.

Preserve every exact session, request, run, attempt, operation, revision,
idempotency key, and returned continuation. Use [requests.md](requests.md) for
request waiting and hosted collection; abort returns control rather than
forcing a new wait loop. Host-mandated confirmations still apply.

Report settlement only from the durable completed operation. When the composed
browser result is fully projected and `completed`, its workflow is already
terminal: do not call a second closer. Use `complete_checkout_session` only
when its exact current continuation directs it.

Cancellation closes workflow authority, not necessarily financial exposure.
Follow the exact cleanup and same-operation reconciliation result. Preserve the
owning workflow's status: read the existing cleanup result for any already
closed workflow. Use `fail_checkout_session` only for an open workflow with a
non-retryable failure. Never relabel any terminal workflow.
When the backend explicitly reports `CARD_CANCELLATION_WRITTEN_OFF` and the
original workflow is closed, explain that the customer reserve was released
and MagicPay assumed the unresolved liability; do not call it an issuer decline.
Check booking/merchant state before following the returned fresh-payment
recovery action. Keep the replacement linked to the original and obtain its
normal exact payment approval. This disposition does not add issuer liquidity.
Otherwise, neither failure nor expiry permits a replacement payment. [statuses.md](statuses.md)
owns the complete recovery and fresh-start rules.
