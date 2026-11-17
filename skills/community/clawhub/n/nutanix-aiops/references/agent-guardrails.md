# Agent guardrails — running nutanix-aiops with a smaller / local model

If you drive these tools with a local model (Llama, Qwen, Mistral … via Goose,
Ollama, LM Studio, or any OpenAI-compatible runtime), you will get noticeably
better results with a short system prompt. This page gives you one, and — more
importantly — tells you which guardrails you **no longer need to write**, because
the tool now enforces them itself.

The distinction matters. A guardrail in a prompt is a request. A guardrail in the
harness is a guarantee. Anything below that we could move into the harness, we did.

## What the tool now enforces — do not waste prompt budget on these

Authorization is not this tool's job — decide it via the account you connect it
with, or the agent's own prompt. What the harness does guarantee:

| You might be tempted to prompt | Why you don't need to |
|---|---|
| "Fetch the ETag before you change anything" | Prism Central v4 requires an `If-Match` ETag on most mutations (optimistic concurrency). Every write tool fetches the entity's current ETag itself and sends it back. There is **no ETag parameter for the model to get wrong**, and no read it must remember to run first. |
| "Don't invent a value when a field is missing" | A field Prism Central did not return comes back as `null`, never as `""`. Absent and empty are distinguishable in the payload — which matters here, because v4 omits a great many fields (`description`, `hypervisorType`, host and cluster names, LCM version strings, alert `impactType`). |
| "Tell me if the output was cut off" | Every list tool returns `{"<items>": [...], "returned": N, "limit": L, "truncated": true/false}`. Truncation is **measured** (one extra row is fetched), not guessed from a length coincidence. `vm_list`, `cluster_list`, `host_list`, `alert_list`, `event_list`, `audit_list`, `task_list`, `image_list`, `category_list`, `subnet_list`, `snapshot_list`, `recovery_point_list`, `protection_domain_list`, `storage_container_list`, `lcm_inventory` and `undo_list` all take a `limit` and report against it. One exception to true/false: `vm_list` reads AHV and ESXi from separate endpoints, and if the ESXi read fails it returns the AHV rows with `esxiError` set and `truncated: null` (completeness unknown) — treat that as a partial list, not as "no ESXi VMs". |
| "Preserve the ordering / tell me what's most urgent" | `cluster_health_rca` and `alert_triage_rca` findings carry an explicit 1-based `rank`, worst-first. Priority is in the payload, not implied by list position, and every finding cites the measured percentage or the raw Prism state string that tripped it. |
| "Confirm before anything destructive" | Destructive tools (`vm_delete`, `vm_migrate`, `snapshot_delete`, `snapshot_restore`, `image_delete`, `subnet_delete`, `storage_container_delete`, `lcm_update`, `pd_failover`) take `dry_run=True` for a preview and are `risk=high`, tagged `review` on the audit row. ⚠️ **The CLI double confirmation exists only for `vm_delete` and `vm_migrate`** — the other seven have no CLI command and are reachable only over MCP, where nothing prompts. Keep your own confirmation for those. |
| "Run the LCM precheck before upgrading" | `lcm_update` **refuses** unless you hand back the `taskExtId` from `lcm_precheck` as `precheck_task_ext_id` and that task reached `SUCCEEDED`. The `dry_run` preview enforces it too, so a preview can never promise an upgrade the real call would refuse. The ordering is a guarantee, not a suggestion the model can skip. |
| "Undo it if it goes wrong" | Reversible writes record an inverse descriptor capturing the **prior** state (power state, CPU/memory, capacity/RF, source host). `undo_list` shows them; `undo_apply` replays one through the same governed path. Irreversible deletes still record what was there: `subnet_delete` captures the subnet's name, description, type, VLAN id, cluster and IP config/pools, so a wrongly deleted subnet can be rebuilt by hand from the audit row. |
| "Log what you did" | Every call is audited to `~/.nutanix-aiops/audit.db` regardless of what the model says it did (relocatable via `NUTANIX_AIOPS_HOME`). |

## What still needs a prompt

These are model-behaviour problems the harness cannot fix from the outside.
Recommended setup for a local model (adapt it to your agent client):

```text
You operate a Nutanix Prism Central (v4) environment through the nutanix-aiops
MCP tools.

TOOL USE
- Before answering any question about the current Nutanix environment, you MUST
  call a tool. Never answer from memory or assumption.
- Actually invoke the tool. Do not describe the call you would make, and do not
  emit an example JSON response in place of calling it.
- If a tool call fails, report the real error verbatim. Never fill the gap with
  a plausible-sounding answer.

IDENTIFIERS
- Every entity is identified by an opaque extId (a UUID). Copy an extId verbatim
  from a tool result. Never retype, abbreviate, reformat, or reconstruct one.
- extIds are NOT interchangeable by type. A VM extId, a cluster extId, a host
  extId, a subnet extId, a storage-container extId, a recovery-point extId and
  a task extId are different namespaces that look identical. Passing a cluster
  extId where a VM extId is wanted is the single most common failure here.
- Call cluster_list first — most other tools need a clusterExtId from it, and
  vm_list / host_list give you the VM and host extIds.

READING RESULTS
- Read the whole result before concluding. If a result has "truncated": true,
  say so and re-run with a higher limit instead of treating the partial result
  as complete.
- A null field means Prism Central did not return that value. Report it as "not
  available" — never infer it.
- Report values exactly as returned. Do not normalise, translate, or prettify
  power states, severities, fault-tolerance states, or extIds.
- When a cluster_health_rca or alert_triage_rca result has findings, work in
  "rank" order and cite the measured number in each finding's "detail".

WRITES
- Run the dry_run=True form of a destructive tool and show the operator what it
  would change before running it for real.
- Async writes return a task extId, not a result. Poll task_list for its status
  rather than assuming the operation finished.

- Only `vm_delete` and `vm_migrate` have CLI commands. The other seven destructive tools
  are MCP-only and nothing will ask you to confirm them: call with `dry_run=True` first,
  show the operator what would change, and wait for an explicit go-ahead.

SCOPE
- Separate observation from interpretation. State what the tools returned, then
  any interpretation, clearly marked as such.
- Do not assert a capacity, resiliency, or performance problem unless a tool
  result supports it.
- Do not add generic advice that does not follow from the tool output.
```

## Nutanix-specific notes

- **AHV and ESXi VMs are both visible, and they are not equivalent.** Prism
  Central sees ESXi-backed VMs in a hypervisor-migration estate, so `vm_list`
  returns them by default and the `hypervisor` field distinguishes them. AHV-only
  operations (snapshot create/restore via the AHV VM API, live migrate to a
  target AHV host) will fail against an ESXi-managed VM. Pass
  `include_esxi=false` to `vm_list` when you only want VMs the AHV lifecycle
  tools can act on, and check the `hypervisor` field before proposing a write.
- **ETags are handled for you.** v4 mutations use `If-Match` for optimistic
  concurrency. `vm_get` and `subnet_get` surface the current `_etag` if you want
  it, but no write tool asks for one — do not prompt the model to fetch it, and
  do not treat a missing ETag as a blocker.
- **Writes are asynchronous.** Most v4 mutations return a task extId
  (`taskExtId`) rather than the finished entity. A snapshot may not exist the
  instant `snapshot_create` returns — the tool resolves the real snapshot extId
  best-effort, and honestly records no undo when it could not.
- **`snapshot_restore` and `pd_failover` are not undoable.** A revert overwrites
  the VM's current state and a failover is a DR event. Both declare no inverse
  rather than pretending to one.
- **Storage headroom is not the same as free space.** Nutanix reserves capacity
  to rebuild after a node or disk failure, which is why `cluster_health_rca`
  flags containers and pools at 80% (warning) / 90% (critical) rather than
  waiting for full.

## Recommended setup for a local model

Authorization is not this tool's job, so enforce it where it actually belongs:
connect with a Prism Central account holding only a read-only (Viewer) role
until you trust the setup — writes then fail at the server, not at a switch in
this tool.

```bash
nutanix-aiops doctor
```

Then, when you are ready to allow writes, point the account at a role with the
write permissions it needs, and optionally set an approver so the audit trail
carries an accountable name:

```bash
export NUTANIX_AUDIT_APPROVED_BY="your.name@example.com"
export NUTANIX_AUDIT_RATIONALE="scheduled maintenance window 2026-07-20"
```

## If your model still struggles

Some behaviours are model-capacity limits rather than prompt problems:

- **Multi-tool workflows time out or drift.** Prefer `cluster_health_rca`,
  `alert_triage_rca` and `analyze_alert` — each does the multi-step correlation
  inside one call, so the model does not have to chain reads and keep extIds
  straight across turns.
- **The model mixes up extIds.** Ask for one entity type at a time, and use
  `overview` first to orient before drilling in.
- **The model ignores later tool results in a long context.** Ask narrower
  questions and use `limit` deliberately rather than pulling whole inventories.
- **The model describes calls instead of making them.** This is usually a
  runtime/tool-calling-format mismatch, not a prompt problem — check that your
  client advertises the tools in the format your model was trained on.

Feedback on running this with a specific local model is genuinely useful —
open an issue at
[github.com/AIops-tools/Nutanix-AIops](https://github.com/AIops-tools/Nutanix-AIops/issues)
with the model, runtime, and what went wrong.
