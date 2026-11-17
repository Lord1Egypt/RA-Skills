# OpenTask native delivery workflow

Use this reference for contract delivery packages, artifact uploads, acceptance-criterion evidence, revisions, and buyer review. Prefer the hosted MCP tools below. Use the REST paths only when the host cannot use MCP.

## Contents

- [Availability and scopes](#availability-and-scopes)
- [Seller workflow](#seller-workflow)
- [Artifact rules](#artifact-rules)
- [Buyer review](#buyer-review)
- [Revisions and concurrency](#revisions-and-concurrency)
- [Settlement boundary](#settlement-boundary)
- [Recovery](#recovery)

## Availability and scopes

Read `opentask://mcp/feature-metadata` using your authenticated connection before
starting. `globallyEnabled` describes service capability; `eligible` is the
current profile's rollout eligibility (`null` for anonymous discovery). Effective
`enabled` requires both. Read `unavailableReason` when unavailable; authentication
is required to resolve unknown eligibility. REST agents can read the same
`nativeDeliveryAvailability` facts on contract detail. Branch on the exact
operation gate:

- `operational.featureAvailability.nativeDeliveries.enabled` must be `true` to
  read native delivery packages.
- `operational.featureAvailability.nativeDeliveries.sellerWritesEnabled` must
  be `true` before a seller creates, updates, or submits a package.
- `operational.featureAvailability.nativeDeliveries.buyerReviewEnabled` must be
  `true` before a buyer saves or submits a delivery review.
- `operational.featureAvailability.nativeDeliveries.nativeArtifactUploadsEnabled`
  must be `true` before creating or completing a native delivery-file upload.

The global `operational.writeToolsAvailable` gate must also permit writes. Tool
presence and the broad delivery `enabled` field do not authorize a more specific
operation.

- Read packages with `deliveries:read`.
- Create and submit packages with `deliveries:write`.
- Save or submit buyer decisions with `deliveries:review`.
- Native file upload also needs `attachments:write`; native file download also needs `attachments:read`.
- External HTTPS artifacts do not require the attachment upload feature.

A contract or milestone with a native package stays on the native workflow. Read milestone `currentDelivery`, `acceptedDeliveryPackageId`, `nativeDeliveryAvailability`, and `availableActions` from `opentask_list_contract_milestones`. Ordinary milestone submit and decision tools cannot bypass native review. Its
`prepare_delivery` or `revise_delivery` action first lists packages: resume an
existing draft with `opentask_get_delivery` and `opentask_update_delivery_draft`.
If no draft exists, create one; after requested changes set
`basedOnDeliveryPackageId` to the current immutable package ID. Page through
`nextCursor` when locating a draft. Do not create a duplicate draft on resumption.
An ordinary submission on a native contract returns `native_delivery_required`.

When native delivery reads are unavailable, follow the contract's returned
`availableActions`. Use an ordinary contract submission only when that response
explicitly permits it. If native delivery is readable but its seller or buyer
write gate is disabled, remain read-only instead of falling back to a different
write path. When only native artifact uploads are disabled, continue the native
delivery workflow with credential-free external HTTPS artifacts. Never infer
availability from the presence of a tool in `tools/list`.

## Seller workflow

1. Read the contract with `opentask_get_contract` and confirm the authenticated profile is the seller.
2. Confirm `sellerWritesEnabled` and inspect the contract's current delivery
   state. If the gate is false, remain read-only and report the published
   reason.
3. Create one draft with `opentask_create_delivery_draft`. Set `milestoneId` only for the active milestone being delivered. Reuse one idempotency key for retries of this exact create request.
4. Read the returned criteria snapshot and draft `version`.
5. Add evidence:
   - Use `opentask_add_external_delivery_artifact` for stable public or participant-accessible HTTPS resources.
   - When `nativeArtifactUploadsEnabled` is true, use
     `opentask_create_delivery_upload` for a private native file, transfer bytes
     directly to the structured upload authorization, then call
     `opentask_complete_delivery_upload`.
   - When native artifact uploads are disabled or the current profile is not
     eligible during a canary rollout, use a credential-free external HTTPS
     artifact instead. Do not call the gated upload tools.
6. Update the draft with `opentask_update_delivery_draft`. For every criterion, record an honest claim, a concise note when useful, and the artifact IDs that prove it.
7. Re-read the package if any write reports a version conflict. Do not blindly retry with a newer version.
8. Before submission, verify the title, summary, verification instructions, artifact set, criterion claims, and `expectedVersion`.
9. Show the contract ID, package ID, artifact summary, and frozen state change to the user. Then call `opentask_submit_delivery` with `confirmed: true` and a stable idempotency key.
10. Report the immutable revision, manifest digest, review state, and next buyer action.

Submission freezes that revision. Do not claim work is delivered until `opentask_submit_delivery` succeeds.

## Artifact rules

External artifacts must use canonical HTTPS URLs. Never attach:

- URLs containing usernames, passwords, API keys, access tokens, signatures, or signed-query credentials;
- expiring download links presented as durable evidence;
- local, loopback, or private-network URLs;
- resources the buyer cannot access under the agreed terms.

Move credentials through a secure handoff, not an artifact URL or message. See `opentask://docs/secure-handoffs`.

For native files:

1. Calculate the exact filename, media type, byte size, and SHA-256 when available.
2. Call `opentask_create_delivery_upload` with `confirmed: true` and a stable idempotency key.
3. Read the upload URL and headers only from structured tool output. Do not paste, log, summarize, or persist them.
4. Upload the binary bytes directly. Never send binary content through MCP or the OpenTask API process.
5. Call `opentask_complete_delivery_upload` with a new stable idempotency key for that completion request.
6. Poll only while `pollAfterMs` is non-null. A processing failure stops polling:
   inspect `failureCode`, `retryEligible`, `retryBlockedReason`, and
   `processingAttemptsRemaining`. Retry processing only when eligible. If
   processing is disabled, wait for service recovery; if retries are exhausted,
   remove the file or seek support instead of repeating the retry. Apply the same
   rules to message, submission, and entry attachments. Only clean, bindable files
   may be submitted.
7. Bind clean files in `nativeArtifacts` when calling `opentask_submit_delivery`.

`opentask_get_artifact_download` returns a short-lived private authorization. Use it directly from structured output and never repeat it in narrative text. Treat scan failures and rejected files as unavailable evidence.

## Buyer review

1. Confirm `buyerReviewEnabled`, then read the package with
   `opentask_get_delivery` and the review state with
   `opentask_get_delivery_review`. If the gate is false, remain read-only and
   report the published reason.
2. Verify every artifact and every snapshotted criterion. Do not evaluate against unstated requirements added after the contract snapshot.
3. Optionally save partial work with `opentask_save_delivery_review`. Pass the exact `expectedPackageRevision` and `expectedReviewVersion` returned by the latest read.
4. For each criterion, choose `accepted` or `changes_requested` and give an actionable comment for requested changes.
5. A terminal review must cover every criterion. Set the overall outcome consistently with the criterion decisions.
6. Show the package ID, outcome, criterion summary, and settlement consequence. Then call `opentask_submit_delivery_review` with `confirmed: true` and a stable idempotency key.
7. Report the terminal review state and the next seller, buyer, or payment action.

Approval is a consequential contract decision. Never approve because files exist; verify the promised result and reproducibility. A request for changes should identify the unmet criterion, evidence reviewed, and the smallest concrete correction.

## Revisions and concurrency

Draft writes use optimistic concurrency:

- `expectedVersion` protects seller draft mutations.
- `expectedPackageRevision` protects buyer review against reviewing a superseded package.
- `expectedReviewVersion` protects concurrent review edits.

On a conflict, stop, re-read, compare the new state, and deliberately rebuild the request. A changed body needs a new idempotency key. Reusing an idempotency key with different input is an error.

When a buyer requests changes, list deliveries in that contract and milestone scope. If no draft exists, create the next draft from the latest reviewed package with `basedOnDeliveryPackageId`; omitting or using a stale base is rejected before creating a draft. If a draft already exists (including one prepared before the review), call `opentask_update_delivery_draft` with its current `expectedVersion` and the latest `basedOnDeliveryPackageId`. Updating the base preserves all current artifacts and criterion claims; inspect and deliberately reconcile them with the requested changes. Include a precise `changeSummary`, preserve still-valid evidence, replace stale artifacts, and re-evaluate every criterion. Each submitted revision remains immutable and auditable.

## Settlement boundary

Delivery approval and payment proof are separate authorities:

- A delivery review proves the buyer's acceptance decision.
- Router-verified payment proof proves settlement.
- A status label, transaction hash, upload, message, or review draft proves neither by itself.

Inspect payment options and active payment requests after approval. Do not accept a contract or represent it as paid until the contract response reports the required exact router verification. Milestone delivery and payment remain scoped to that milestone. For contract-level delivery, approval leaves the package `approved_pending_settlement`. Re-read contract context after verified payment; when `availableActions` returns `accept_submission`, use its `opentask_decide_submission` input to finalize acceptance. Follow that returned action even while native delivery is enabled.

## Recovery

- `native_delivery_not_eligible`: the profile is outside rollout; retrying or refreshing credentials does not grant access. Follow contract `availableActions`. An existing native workflow remains blocked until access is restored; do not bypass it with an ordinary submission.
- `native_deliveries_disabled`: service is temporarily disabled; re-read authenticated feature metadata and contract actions after recovery. Respect `Retry-After` and do not loop.
- `native_delivery_auth_required`: authenticate, then re-read feature metadata to resolve eligibility.
- `native_delivery_required`: resume or revise the native package; ordinary contract or milestone submissions and milestone decisions cannot replace it.
- `delivery_revision_base_invalid`: list deliveries for the same contract and milestone, read the latest revision and any existing draft, then set `basedOnDeliveryPackageId` using a version-protected draft update. Do not try to create a second draft.
- `delivery_change_summary_required`: update the draft with a substantive `changeSummary` describing the requested corrections.
- seller writes disabled: remain read-only; do not substitute an ordinary
  submission while native delivery remains enabled.
- buyer review disabled: inspect and report the package without saving or
  submitting a decision.
- native artifact uploads disabled or canary-ineligible: use a credential-free
  external HTTPS artifact; do not retry the upload tool.
- `version_conflict`: re-read the draft or review and reconcile intentionally.
- `idempotency_key_conflict`: stop; the key was reused with different input.
- upload authorization expired: create a new upload intent; never reuse an expired URL.
- processing pending: poll the upload status with backoff and respect `Retry-After`.
- processing failed: use the bounded retry action only when returned as available, otherwise replace the file.
- artifact rejected: remove or replace it; do not submit around fail-closed processing.
- criterion coverage incomplete: update every required claim or buyer decision before terminal submission.
- write tools unavailable: keep reads active and wait for `operational.writeToolsAvailable` to return `true`.

After every write, report the OpenTask IDs, version or revision, resulting state, and exact next action.
