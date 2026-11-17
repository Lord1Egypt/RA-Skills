# Customer identity and merge workflow

Use the tool schemas exposed by the connected MCP server or installed CLI. Identity tools require a supporting server rollout and client version; documentation alone does not prove they are deployed. The five tools are in the `identity` toolset: when they are absent from an MCP connection, load it with `outlit_load_toolset`. If a tool is still absent, check the installed CLI help and available published upgrade. Do not invent a command or bypass an agent policy.

The earlier names `outlit_get_customer_identity`, `outlit_list_identity_merge_suggestions`, `outlit_reject_identity_merge_suggestion` and `outlit_get_customer_merge_status`, with their earlier inputs, answer as aliases until 2026-12-11. Use the names and inputs below.

## Diagnose before combining records

`outlit_get_identity` takes `{ customer, include? }`. `customer` is a customer ID, domain or name; `include: ["links"]` adds the customer's records in other systems. It returns `customer`, `checkedAt`, the search `window`, `completeness` (`complete_within_bounds` or `incomplete`, with reasons), `limits` (calls, domains and candidates read), and up to 10 `candidates`. Each candidate has a `customer`, its `type`, and `reasons`: a participant domain and the call `source` it was seen in, which `outlit_get_source` opens. With candidates, `next` says how to compare the first one. Its current search is bounded by call-participant domains, not every possible identity source. Candidates are leads, not proof, and do not grant access to another customer's evidence. Treat an `incomplete` result as unknown coverage.

```sh
outlit customers identity <customerId> --json
```

Inspect exact customer records and source evidence within your existing access. A shared consultant, similar company name, related domain, or parent/subsidiary relationship is not enough to establish that the records represent the same company. If uncertain, stop at diagnosis and explain the uncertainty.

## Saved suggestions and existing work

`outlit_list_merge_suggestions` accepts optional `customer`, `filters: { id, status, confidence }`, `include`, `limit` and `cursor`. It returns `{ items, page, canManage }`, plus `coverage` when `items` is empty. The default limit is 25 and the maximum is 100. Status filters are `suggested`, `processing`, `merged` and `rejected`; confidence filters are `high`, `medium` and `low`. `include` adds `impact`, `scope`, `jev` or `cluster` sections; leave it out unless you need them.

```sh
outlit identity suggestions list --customer-id <customerId> --json
outlit identity suggestions list --suggestion-id <suggestionId> --json
```

Each suggestion includes its `id`, `status`, `confidence`, `survivor`, `duplicate`, `explanation`, review details, `mergeBlockedReason`, `canMerge`, `canReject` and a nullable `latestJob`. Inspect one suggestion with `filters.id`; there is no separate suggestion-get tool. Follow `page.nextCursor` as `cursor` (`--cursor` in the CLI) for more pages.

When `latestJob.operation` is non-null, pass its `id` to `outlit_get_merge`. `latestJob.id` is a job ID, not an operation ID. A null operation ID means there is no matching tracked operation for that job; do not substitute the job ID or infer that no work has happened. An empty suggestion list does not rule out an unsuggested merge. Reuse an operation ID from an earlier execution response when available.

If a merge is already queued or running, track it rather than submitting a new request. If prior execution is uncertain, retry only the identical execution input with its original request ID. Do not generate a new ID to get around a conflict. If prior execution is uncertain and neither the original request ID nor operation ID is available, stop execution and report the unresolved state.

To reject a suggestion when the user asks, use `outlit_reject_merge_suggestion` with `{ id, note?, requestId }`. `id` is the suggestion's `id`; `requestId` is your stable ID, so a retry with the same ID rejects once. Its response is `{ suggestion: { id, status: "rejected" }, next }`; rejection keeps the records separate.

```sh
outlit identity suggestions reject <suggestionId> --review-notes "Distinct companies" --request-id <stableRequestId> --json
```

Without `--request-id` the CLI makes a new one, so pass the same ID when retrying.

## Preview, execute, and track

`outlit_merge_customers` is the single preview/execute tool. Input:

- Required: `survivor` and `duplicate`, exact customer IDs, which must be distinct.
- Optional: `suggestionId`, and for execution `note`.
- `mode` defaults to `preview`.
- Execution requires `mode: "execute"`, the reviewed preview's `preview.token` as `previewToken`, and a stable `requestId`.

Without `suggestionId`, both records must be of type `company`. Any pair involving an `individual` requires an eligible saved suggestion for that exact pair and survivor. A suggestion does not prove a match or grant merge authority.

Preview first:

```sh
outlit customers merge <survivorId> <duplicateId> --json
```

The preview returns `mode: "preview"`, `survivor` and `duplicate`, `preview: { token, expiresAt }`, `evaluatedAt`, `impact` counts, `warnings`, `links` (the linked records both customers share, the ones that conflict, and the ones only one side holds), and `next`. There is no `eligible` boolean; unsupported pairs fail. Add `--suggestion-id <suggestionId>` when using a saved suggestion, including for individual records. Review the survivor, identifiers, affected data, and access relationships before execution.

**Execution is dangerous and has no supported undo.** Only execute with explicit user authorization, certainty that both records represent the same customer, and merge permission. A preview grants no authority. Preserve the reviewed pair and relevant options; the server rejects a stale identity preview.

```sh
outlit customers merge <survivorId> <duplicateId> --execute \
  --preview-token <returnedToken> --request-id <stableRequestId> --json
```

Include the same `--suggestion-id` if used. The CLI's `--review-notes` is the tool's `note`. Retry with identical execution input and the same request ID. Never interpret a successful request as a completed merge.

Execution returns `mode: "execute"` with an `operation`, and `outlit_get_merge` returns the same `operation`: its `id`, `survivor`, `duplicate`, `status`, `phase`, and a nullable `failure: { code, message }`. Status is `queued`, `running`, `completed` or `failed`. `outlit_get_merge` takes `{ id }`, the `operation.id`; while the merge is queued or running, its `next` says to poll again:

```sh
outlit customers merge-status <operationId> --json
```

Only `completed` reports completion. For `failed`, read `failure.code`: `not_started` means nothing moved, so preview the pair again; `incomplete` means the merge began and the records stay reserved while Outlit recovers it, so never execute it again. Do not invent restart, cancel, or undo operations. Possessing an operation ID does not grant access. Rejection, preview, execution, and status are separate outcomes; a preview or queued operation has not merged the records.

## Permissions and tool metadata

- API keys: `customer_intelligence:read` for diagnosis, suggestions, previews, and status; `customer_identity:review` for rejection; `customer_identity:merge` for execution. A complete preview/execute/track workflow needs both read and merge grants. The merge grant requires an explicit Custom-key selection and is excluded from Full workspace access.
- OAuth MCP: current user permissions and record access apply. Under the default member/admin roles, members can diagnose accessible customers; admins have identity management permissions.
- Outlit-owned agents cannot perform identity writes, even when representing an admin. Churn and Renewal can diagnose only their assigned customer. Do not bypass this boundary through a different client or credential.
- MCP merge metadata includes `readOnlyHint: false` and `destructiveHint: true`, reflecting its maximum effect even though preview is the default. Its description warns about permanent changes, certainty, permissions, and asynchronous execution. Hints do not enforce authorization; the server does.
- CLI merge help uses that same canonical description. `--execute` is explicit and defaults off; `--preview-token` and `--request-id` are required with it. Check stderr and exit status for failures.
- Pi's default and analytical toolsets do not automatically include these identity tools; custom selection is required. Inclusion does not confer permission.
