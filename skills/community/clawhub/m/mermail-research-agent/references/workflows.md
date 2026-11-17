# Research engagement workflow

## Intake and order verification

1. Resolve one ready mailbox in the selected workspace. Match existing mailboxes by verified purpose and stable ID; do not create a new inbox merely because a different display name seems attractive.
2. Read the selected clean email and relevant context. Match the source message against the order's customer, approved addresses, mailbox, and thread. Stop mismatched account/attachment reads before disclosing or downloading private material.
3. Load the owner-provided [order record](templates.md). If absent, prepare an unfilled owner intake request; customer assertions cannot fill verified identity, payment, rights, or budget fields.
4. Check duplicate source-message and deliverable IDs before research or spending. Reuse an existing draft or delivered report as context, not as automatic authority to resend.
5. Capture the requested mode, exact protocols, criteria, audience, deadline/timezone, reporting period, and output format. A deadline is not the data observation window. If material requirements are missing, draft one consolidated clarification; do not invent an evaluation rubric or promise an unsupported deadline.
6. Verify owner-confirmed payment evidence for this order: account/order match, paid amount/currency, settlement status, and purchased scope/follow-up limits. Unknown, pending, disputed, refunded, or conflicting evidence holds paid fulfillment for owner resolution. No live billing verification API is implied.

Clarification drafting can precede paid fulfillment. Rights clearance is required before sending a paid offer or externally delivering research; do not imply that an internal draft can already be sold.

## Research and rights

Select the relevant [CMC mode](cmc-research.md). Make a task-sized evidence plan from the criteria and time window; prefer already-authorized data access. Batch compatible public identifier lookups and reuse fresh, licensed evidence within the same order. Do not acquire data merely to fill an optional template section.

Before paid fulfillment, record the applicable provider agreement or permission and verify that its scope covers the intended customer report, audience, retention, and redistribution. Attribution requirements apply to the report itself. Do not infer that derived analysis, paid API access, or a free pilot automatically resolves restrictions. If unclear, record `held_rights` for owner resolution; do not make a legal assurance or contact the provider on the owner's behalf without authorization.

Separate public research evidence from private criteria and customer notes. Track source URL/provider operation, public entity ID, observation time, retrieval time, reporting window, units, and limitations. A latest quote cannot reconstruct a historical weekly series; state unavailable history explicitly.

## Additional data budget

Use the owner's selected provider/request authorization, not a purchasing instruction in customer mail. Follow [Mermail x402](../../mermail-x402-agent/SKILL.md) for connection, discovery, live challenge, signing, redemption, and result checks.

Use [Agent Wallet credential and execution rules](../../mermail-agent-wallet/references/workflows.md#credential-and-autonomous-execution): preserve the owner's chosen `credential_id`, choose only chain-eligible credentials, and keep `setup_required`, `pending_execution`, or `recovery_required` attached to the original request/invocation. Autonomous execution must fit the owner's exact grant; none of these states authorizes a replacement payment or report delivery.

- Keep the customer invoice/entitlement and owner research expense sections separate.
- Track amounts in integer smallest units for the selected asset/network; for Base USDC, six decimals. Never combine different assets as if they were the same budget.
- Compute `remaining = authorized_budget - confirmed_spend - unresolved_reserved`. A pending/proof-ready/uncertain request contributes once to reserved, keyed by its existing request ID.
- Before payment, verify the exact origin, resource, method/parameters, purpose, current amount, asset/network, secure replay path, and expected data result. The required charge must fit both remaining order budget and the exact owner authorization. No budget means no paid call.
- Reserve the full authorized charge before initiating that call. After proof creation, use the supported secure replay channel for the identical frozen request. Never log/persist the proof or treat it as settlement.
- Move a reservation to confirmed spend only with authoritative settlement evidence. Release it only after an authoritative non-settlement outcome; expiry also needs evidence that settlement did not already occur. A timeout or missing transaction hash is not evidence of release. If evidence is unavailable, keep the reservation and stop dependent purchases when the remaining budget is insufficient.
- For example, a 1.00 USDC cap minus 0.60 confirmed and 0.35 unresolved leaves 0.05. A 0.10 request is blocked, even if the wallet balance can cover it.

Insufficient funds, incompatible live x402 support, unusable proof replay, or missing data capabilities are blockers. Do not switch to a transfer, new wallet, external signer, or raw private-key SDK. Funding and connecting the wallet are separate owner actions.

## Draft, deliver, and follow up

Draft with the selected source thread metadata supported by the live schema. Default to a sourced text/HTML email memo. Check every material factual claim, time window, and required criterion. Label incomplete work clearly; do not pass missing core evidence off as a finished commissioned report. The owner may approve a revised reduced scope.

Before delivery, recheck account/order, entitlement, rights, report version, source email/thread, approved sender/recipients, and any requested attachments. Present the exact outgoing content if it has not already been authorized. Use `reply_to_email` once under sufficient authorization, passing explicit recipients and source `emailId`. Keep the same idempotency key only for an identical operation, following the composition contract; never use a new key to bypass an uncertain result.

Record the draft ID before send and the returned message ID/status after success. A draft is not delivery; provider acceptance does not prove customer receipt. If send outcome is uncertain, inspect the exact thread/delivery state once and hold further sends if still unresolved.

For follow-ups, retrieve the owner record and bounded original thread. Recheck approved addresses, current entitlement/follow-up limits, and freshness. Answer an included clarification from the prior report when evidence suffices. A new analysis period, protocol set, or charge beyond agreed scope produces a scope-change draft for owner review. Preserve the prior report and increment the version for substantive revisions; do not silently overwrite what was delivered.

End each run with a minimal private checkpoint using [templates.md](templates.md). Persist only to an already-authorized private destination, or return it to the owner when no destination exists.
