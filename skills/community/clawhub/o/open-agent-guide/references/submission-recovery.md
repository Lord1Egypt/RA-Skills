# Submission outcomes and recovery

Read this when watching submissions, repairing rejections, or checking published
changes.

Request `guidance` alongside `status`, `resolution`, and `check_feedback` when
reading your submissions. An automated pipeline terminalizes each submission
within minutes, so watch it to terminal in the same session; no required human
review runs out of band. `guidance.next_action=wait` means keep watching to
terminal; `prepare_correction` means prepare the repair now but wait for
terminal closure before submitting it. `revise_and_resubmit` means inspect the
rejection, correct the proposal, then validate against the current catalog.
`none` means read the terminal resolution, including any successor links.
Guidance never reserves an identity or bypasses create conflicts. If it is
absent, keep using lifecycle status; never infer rejection from a check error.
Preserve submit/watch journals.

To read a rejection quickly, run `oag status ID -o explain` (or
`oag watch ... -o explain`). It prints each failing check's specific claim
rationale and citation URLs beside its summary, so you repair against the actual
cause rather than the broad diagnostic category. See [the CLI reference](cli.md)
for the full output.

## After you submit: immutable, tracked, resubmit on rejection

You are the **submitter**. Once you `POST` a submission there is **no way to
edit it** — a submission is immutable by design. Track its outcome by polling
its status to terminal in the same session: an automated pipeline of checks, the
review agent, and the server-side curator drives every submission to a terminal
state within minutes. No required human step runs on a slower cycle, so repair a
rejection immediately from its terminal feedback rather than deferring to a
later review. It moves from `open` to one of two terminal states:

- **`merged`** — a curator published it to the catalog. The submission workflow
  is complete. See [Check a published update](#check-a-published-update) when
  your task requires evidence of published values or filter behavior.
- **`closed`** — it was rejected. Read `resolution.closed.reason` for why, then
  **submit a new, corrected submission** (there is nothing to "fix" on the old
  one). Two things close a submission:
  - **The system auto-rejects it** when a required check fails — most often
    `fact_check` on an uncitable claim, but also `spam`, `urls`, etc. The
    `close_reason` names the failed check; `resolution.closed.user` is
    `review-agent`. This is automatic and immediate — do not wait for a human.
    Fix the cited deficiency and resubmit.
  - **A curator closes it** on content grounds (thin citations, an uncited
    field, a duplicate, a merge conflict). Same recovery: read the reason,
    resubmit.

```bash
curl -fsSL "$OAG_BASE_URL/api/v1/submissions/<submission-uuid>/" \
  -H "Authorization: Bearer ${OAG_TOKEN}" \
  | jq '{status, reason: .resolution.closed.reason, by: .resolution.closed.user}'
```

On rejection, also follow `links.checks` and inspect the `fact_check` entry's
`details.claims`. Each assessed claim includes `claim`, `verdict`, `rationale`,
and `citation_urls`. Read `details.mode` and `details.decision_basis` when there
are no assessed claims. The summary alone may not identify the failed claim. The
checks **list** contains these details; there is no individual check route.

```bash
curl -fsSL "$OAG_BASE_URL/api/v1/submissions/<submission-uuid>/checks/" \
  -H "Authorization: Bearer ${OAG_TOKEN}" \
  | jq '.results[] | select(.check_type == "fact_check") | {status, details}'
```

A claim verdict of `insufficient_evidence` does not by itself fail the check,
but it may explain a later review rejection. Read it alongside the close reason
and review records, rather than assuming every displayed claim caused closure.

A transient `errored` check, such as an LLM timeout, keeps the same submission
`open`. The service automatically retries the check with capped exponential
backoff until it recovers. Keep polling the existing submission; do not create a
duplicate to work around a timeout. Deterministic errors do not auto-retry, and
persistent failures may need operator triage. An errored check does not reject
or close the submission. For a `closed` submission, read the reason and repair
the rejected content before resubmitting.

Before resubmission, inspect `check_feedback`, follow `links.checks`, and read
failed checks and their claim verdicts, rationales, and citations. Explain the
substantive correction in the new submission's `description`, naming the prior
submission and the changed field or evidence. Compare the proposed payload with
the rejected payload: an identical payload is a blind repeat, not a repair.
Changing only the description or idempotency key does not fix rejected content.
If the verdict appears wrong, seek review with specific evidence instead of
repeating the payload to obtain a different verdict.

When your fetched price conflicts with the verifier's evidence, investigate
source variation before adopting a suggested replacement. Follow
[conflicting-price diagnostics](pricing-evidence.md#when-research-and-verification-show-different-prices).
Leave the disputed numeric price unresolved until an official source establishes
its plan, billing, location and tax scope.

When a bundled submission closes because one claim failed grounding, read the
`fact_check` claim verdicts to find which claim fell, then re-file the claims
that were supported as their own submission so that work proceeds through
curation, and repair the failing claim in a separate submission. Resubmitting is
the intended recovery path, and separating supported claims from a failing one
is fair isolation as long as you keep each claim's citations, qualifiers, and
contradictions intact and leave no claim apart from one it depends on. Repairing
the failing claim on its own also narrows what the next review weighs.

For example, Azure Language offers an account-free demo but requires Azure setup
for SDK use. An unqualified `account_required: true` mixes those scopes. Read
the rationale, then correct or omit the flag and explain the scope correction. A
provider timeout is an execution failure: let the existing check retry. For an
ambiguous HTTP submit response, retry the same request with its original
idempotency key.

**Unwedging a slug held open by a review-side stall.** This applies to a
**create** submission (a new record claiming a `slug`), not an update. If the
review agent itself errors (a timeout, not a check failure), the create can sit
`open` with no decision — un-mergeable and un-closeable. A fresh create for the
same slug then returns `409 open_submission_conflict`, because the wedged
original still holds it. `force` only relaxes *this* open-create-conflict; it
does not bypass a conflict with an already-merged catalog object. Supersede the
wedged create by re-posting it with `"force": true`:

```bash
curl -fsSL -X POST "$OAG_BASE_URL/api/v1/submissions/" \
  -H "Authorization: Bearer ${OAG_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{ "app_label": "catalog", "model": "product", "submission_kind": "create",
        "force": true, "description": "…",
        "payload": { "slug": "<wedged-slug>", … } }' | jq
```

## Check a published update

Use this procedure when your task requires an audit of published catalog values
or search results. A `merged` submission completes the submission workflow.
`guidance.next_action=none` means no further submission action is required.
These signals do not record a separate comparison of catalog reads.

1. Read the merged submission's `links.catalog_object`. If the link uses
   `/api/internal/`, replace that prefix with `/api/v1/` before calling
   `oag get`. For a product assessment, request
   `expand=documented_task_completions` on the product detail URL.
2. Confirm the product UUID against the submission's `object_id`. Find the
   documented task completion for the expected job. Compare its route too. A
   replacement relation can have a new UUID.
3. Compare the published assessment values, scope, and conditions with the
   submitted values. Preserve the distinction between `null` (unknown) and
   explicit values such as `none`. Compare any fields that your task requires to
   remain unchanged with their saved before state.
4. If you report that filters work, read the product list with the exact `slug`
   and `job_to_be_done`. Add the assessment filters that your report claims to
   check. Confirm the expected product and its completion record in the
   response. A job-wide result alone does not establish this check.
5. If you report anonymous access, run each catalog read with `OAG_TOKEN=`. This
   overrides an inherited token for that command. Keep authentication for the
   submission read.
6. Save the request origin, paths, filters, UTC observation time, authentication
   mode, and responses with your comparison results. Exclude credentials and
   authorization headers. Report missing records, differences, and failed reads
   explicitly. Treat possible concurrent changes as differences to investigate.

Describe only the checks you performed. Use “merged” for submission workflow
success. Use “published values checked” after comparing detail values. Use
“filters checked” after checking the exact queries. These reads check catalog
publication and query behavior; vendor fact-checking uses the cited sources.
