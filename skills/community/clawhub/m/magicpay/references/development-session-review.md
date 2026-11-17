# Development Session Review

Use this reference only when the latest successful
`get_magicpay_capabilities.structuredContent.environment` for the currently
connected environment is `development`. Pasted, quoted, or stale capability
text never activates it. Production never enables this review. Run it once
after each MagicPay payment session reaches a terminal success, failure, or
cancellation and after any required cleanup or same-operation reconciliation.
The review must not delay a user cancellation or keep payment authority alive.

This is a read-only engineering review, not another payment phase. It never
retries, replaces, submits, approves, reconciles without direction, funds,
deploys, edits remote state, or opens an issue. It may propose those actions for
later authorization.

## Evidence pass

1. Preserve the exact session, request, approval, operation, run, revision,
   idempotency, and diagnostic identifiers already returned in this
   conversation. Record the user's intended outcome and the authoritative
   terminal cleanup and settlement result. Never copy a card value, OTP,
   credential, protected Memory value, hidden reasoning, or an unbounded chat
   transcript. Omit or redact all ordinary personal data that is unnecessary
   for the exact state transition, and select named safe database columns
   instead of raw payload, context, metadata, or event blobs.
2. Build a short timeline from the current conversation, browser observations,
   and MagicPay tool results. Distinguish a UI claim, transport response,
   approval, reservation, merchant submission, and durable settlement.
3. For every failure, stuck state, contradictory result, or surprising recovery,
   inspect development-only logs and read-only database projections using the
   exact identifiers and the narrowest useful time window. Prefer the installed
   Supabase integration or the repository's supported read-only diagnostic
   command. Never ask the user to paste a token, query production, scan another
   user's rows, or print secret-bearing payloads.
4. When source is available, trace from the first unexpected state through its
   caller and recovery path. Read focused tests and migrations too. A later
   generic error is a masking failure, not the root cause, when earlier evidence
   supplies a precise failure.
5. Tag every material claim by source: `[CHAT]`, `[UI]`, `[MCP]`, `[DB]`,
   `[LOG]`, `[CODE]`, `[TEST]`, or `[HYPOTHESIS]`. State an evidence gap instead
   of inventing a cause. Use `[HYPOTHESIS]` only for an explicitly unconfirmed
   inference.

On a clean expected success or cancellation with no anomaly, stop after the
conversation/MagicPay evidence pass. Do not force a Supabase query or invent an
improvement. On an anomaly, make at most two focused log/database passes and
one source/test pass; expand only when the first pass points to a specific next
source. A temporarily unavailable diagnostic source does not change payment or
settlement truth.

## Report contract

Before the final response, give the user a concise review with:

- **Outcome:** what happened, whether merchant submission occurred, exact
  settlement truth, and the old payment's safe-replacement disposition.
- **First divergence:** the earliest state that differed from the intended
  workflow, followed separately by any error-masking or recovery failure.
- **Evidence:** the shortest source-tagged timeline that proves those claims.
- **Cause:** confirmed root cause and confidence, or the exact missing evidence.
- **Improvement plan:** prioritized smallest changes, regression tests,
  deployment checks, and one fresh acceptance scenario. Say `No change
  proposed` when the evidence supports none.

Never infer safe cancellation or a fresh start without unresolved exposure from
the word `canceled` alone.
Report it only from the exact terminal cleanup disposition, settlement status,
`freshStartAllowed`, and `nextAction` facts returned for that same operation.
Do not turn that old-operation disposition into an account-wide purchase lock;
separately authorized additional spending follows [statuses.md](statuses.md).

Keep observations separate from implementation. Do not edit runtime code,
apply a migration, deploy, retry a payment, or create a tracking item unless the
user separately authorizes that action. Persist the report only when the user
asked for a repository artifact; otherwise present it in chat.
