# Agent guardrails — running minio-aiops with a smaller / local model

If you drive these tools with a local model (Llama, Qwen, Mistral … via Goose,
Ollama, LM Studio, or any OpenAI-compatible runtime), you will get noticeably
better results with a short system prompt. This page gives you one, and — more
importantly — tells you which guardrails you **no longer need to write**, because
the tool now enforces them itself.

The distinction matters. A guardrail in a prompt is a request. A guardrail in the
harness is a guarantee. Anything below that we could move into the harness, we did.

## Authorization is not this tool's job — decide it where it belongs

Whether a write should happen is your decision, or the account's. The tool does
not gate it — there is no read-only switch and no approval prompt to configure.
The two right places to control read vs write:

- **The access key you connect with.** Give it a read-only IAM policy. A write
  then fails at the server, which is the only place the permission actually
  lives — no skill-side flag can be argued around by a model, but a revoked
  permission cannot be.
- **Your agent's system prompt.** If you want an observe-only session, tell the
  model not to call the write tools (they are clearly tagged `[WRITE]`).

What the tool *does* guarantee is that you can always see what happened:

## What the tool enforces — do not waste prompt budget on these

| You might be tempted to prompt | Why you don't need to |
|---|---|
| "Don't invent a value when a field is missing" | A field the API did not return comes back as `null`, never as `""` — a bucket with no `createdAt`, an object with no `lastModified`/`versionId`, an upload with no `initiated` time. Absent and empty are distinguishable in the payload. |
| "Tell me if the object list was cut off" | Every bounded listing returns `{"objects": [...], "returned": N, "limit": L, "truncated": true/false}` (and the same shape with `buckets` / `uploads`). Truncation is measured — `object_ls` fetches one row past the limit, the bucket/upload/usage listings measure against the full set — never guessed from the count equalling the limit. |
| "Tell me which exposed bucket to fix first" | `bucket_exposure_audit` returns findings sorted riskiest-first with an explicit `riskScore` and `riskLevel`; `capacity_rca`, `healing_health`, and `lifecycle_gap_analysis` each attach a `severity` plus `cause` and `suggestedAction` to every finding. The priority is in the payload, not implied by list position. |
| "Confirm before anything destructive" | Destructive operations require a `--dry-run`-able preview + double confirmation at the CLI. `bucket_delete` additionally refuses unless the bucket is verifiably empty (including noncurrent versions and delete markers). |
| "Log what you did" | Every call is audited to `~/.minio-aiops/audit.db` regardless of what the model says it did. Reversible writes record their prior state (`priorState`) so `undo_list` / `undo_apply` can roll them back. |

## What still needs a prompt

These are model-behaviour problems the harness cannot fix from the outside.
Recommended setup for a local model (adapt it to your agent client):

```text
You operate a MinIO object-storage deployment through the minio-aiops MCP tools.

TOOL USE
- Before answering any question about the current MinIO deployment, you MUST
  call a tool. Never answer from memory or assumption.
- Actually invoke the tool. Do not describe the call you would make, and do not
  emit an example JSON response in place of calling it.
- If a tool call fails, report the real error verbatim. Never fill the gap with
  a plausible-sounding answer.

READING RESULTS
- Read the whole result before concluding. If a result contains a "truncated"
  field that is true, say so and re-run with a higher limit (or a narrower
  prefix) instead of treating the partial result as complete. An object listing
  is a page of a bucket, not the bucket.
- A null field means the API did not return that value. Report it as "not
  available" — never infer it.
- Report values exactly as returned. Do not normalise, translate, or prettify
  bucket names, object keys, versioning states, or upload IDs.
- When an analysis returns findings, work in severity order (critical, then
  warning, then info) and cite the measured number in each finding's "cause".

SCOPE
- Separate observation from interpretation. State what the tools returned, then
  any interpretation, clearly marked as such.
- Do not assert a capacity, exposure, or durability problem unless a tool result
  supports it. "usedRatio" and "failureToleranceRemaining" are the numbers that
  support such a claim.
- Do not add generic S3 advice that does not follow from the tool output.
- Do not confuse a bucket name with an object key, or an uploadId with a
  versionId. A bucket name is the whole bucket; an object key is one object
  inside it.
- "Enabled", "Suspended", and "Off" are three distinct versioning states.
  A suspended bucket is not an unversioned bucket — old versions still exist.
```

## Recommended setup for a local model

Start with a connection that *cannot* write, verify, and widen the key's
permission only when you trust the setup — a `bucket_delete` or a policy change
is cheap to invoke and expensive to get wrong:

```bash
# Connect with an access key whose IAM policy is read-only, then:
minio-aiops doctor
```

Optionally annotate the audit trail with who is operating and why — recorded on
every row, never required:

```bash
export MINIO_AUDIT_APPROVED_BY="your.name@example.com"
export MINIO_AUDIT_RATIONALE="lifecycle cleanup window 2026-07-20"
```

## If your model still struggles

Some behaviours are model-capacity limits rather than prompt problems:

- **Multi-tool workflows time out or drift.** Prefer the analysis tools —
  `fleet_overview`, `capacity_rca`, `bucket_exposure_audit`,
  `lifecycle_gap_analysis`, `healing_health` — they do the multi-step
  correlation inside one call, so the model does not have to chain reads and
  keep bucket names straight.
- **The model ignores later tool results in a long context.** Ask narrower
  questions and use `limit`/`prefix` on `object_ls` deliberately rather than
  paging through a whole bucket.
- **The model describes calls instead of making them.** This is usually a
  runtime/tool-calling-format mismatch, not a prompt problem — check that your
  client advertises the tools in the format your model was trained on.

Feedback on running this with a specific local model is genuinely useful —
open an issue at
[github.com/AIops-tools/MinIO-AIops](https://github.com/AIops-tools/MinIO-AIops/issues)
with the model, runtime, and what went wrong.
