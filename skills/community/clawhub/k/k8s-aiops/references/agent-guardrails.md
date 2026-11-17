# Agent guardrails — running k8s-aiops with a smaller / local model

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

- **The kubeconfig context you connect with.** Bind it to a ServiceAccount or
  user whose RBAC grants only `get`/`list`/`watch`, and every write fails at the
  apiserver — the only place the permission actually lives. No skill-side flag
  can be argued around by a model, but a revoked RBAC verb cannot be. This is
  strictly stronger than any in-process switch: it is enforced at the cluster.
- **Your agent's system prompt.** If you want an observe-only session, tell the
  model not to call the write tools (they are clearly tagged `[WRITE]`).

What the tool *does* guarantee is that you can always see what happened:

## What the tool enforces — do not waste prompt budget on these

| You might be tempted to prompt | Why you don't need to |
|---|---|
| "Log everything you do, over both MCP and the CLI" | Every operation is audited to `~/.k8s-aiops/audit.db` regardless of what the model says it did — and the CLI writes the same row the MCP path does, so there is no unaudited entry point. Reversible writes also record an undo token capturing the *prior* state. |
| "Don't invent a value when a field is missing" | A field the apiserver did not return comes back as `null`, never as `""`. An unscheduled pod's `node` is `null`; a pod with no phase yet has `phase: null`; an object with no readable creation timestamp has `age: null`. Absent and empty are distinguishable in the payload. |
| "Tell me if the output was cut off" | The limit-bearing reads return an envelope: `event_list` → `{"events": [...], "returned": N, "limit": L, "truncated": true/false}`, and `undo_list` → `{"undos": [...], "returned": N, "limit": L, "truncated": ...}`. Truncation is **measured** (one extra row is fetched), not guessed from `len(rows) == limit`. |
| "Preserve the ordering / tell me what's most urgent" | `pod_health_rca` and `workload_readiness_rca` findings carry an explicit 1-based `rank`, worst-first, and each finding's `detail` cites the measured signal (the waiting reason, the restart count, the ready/desired ratio). Priority is in the payload, not implied by list position. |
| "Confirm before anything destructive" | The destructive CLI commands (deployment/job/namespace delete, node cordon/drain, rollout undo) are `--dry-run`-able and require double confirmation. |
| "Don't get stuck retrying" | The runaway guard trips a circuit breaker if the same call is hammered in a tight loop — a stuck agent is stopped rather than left to burn calls and time. It is a safety backstop, not an authorization gate. |

## What still needs a prompt

These are model-behaviour problems the harness cannot fix from the outside.
Recommended setup for a local model (adapt it to your agent client):

```text
You operate a Kubernetes cluster through the k8s-aiops MCP tools.

TOOL USE
- Before answering any question about the current cluster, you MUST call a
  tool. Never answer from memory or assumption.
- Actually invoke the tool. Do not describe the call you would make, and do not
  emit an example JSON response in place of calling it.
- If a tool call fails, report the real error verbatim. Never fill the gap with
  a plausible-sounding answer.

READING RESULTS
- Read the whole result before concluding. If a result contains a "truncated"
  field that is true, say so and re-run with a higher limit instead of treating
  the partial result as complete.
- A null field means the apiserver did not return that value. Report it as "not
  available" — never infer it. In particular, a null "node" means the pod is
  not scheduled; it does not mean the node is unknown or missing.
- Report values exactly as returned. Do not normalise, translate, or prettify
  phases, conditions, container-state reasons, or resource names.
- When an RCA result has findings, work in "rank" order and cite the measured
  number in each finding's "detail".

SCOPE AND IDENTIFIERS
- Always state the namespace you are talking about. A bare pod or deployment
  name is ambiguous — the same name exists in many namespaces.
- Omitting the namespace means ALL namespaces, not the default one. Never
  silently widen a namespaced question into a cluster-wide answer.
- Do not confuse a namespace with a context (a cluster), a pod name with its
  deployment name, or a container name with the pod that contains it. A pod
  name generated by a ReplicaSet is not a stable identifier.
- Separate observation from interpretation. State what the tools returned, then
  any interpretation, clearly marked as such.
- Do not assert a capacity, performance, or availability problem unless a tool
  result supports it. Do not add generic advice that does not follow from the
  tool output.
```

## Recommended setup for a local model

Start with a kubeconfig context that *cannot* write — a ServiceAccount whose
RBAC grants only `get`/`list`/`watch` — verify, and widen its permission only
when you trust the setup. RBAC is enforced at the apiserver, so a write fails at
the cluster no matter what the model attempts:

```bash
# Point KUBECONFIG at a read-only ServiceAccount context, then:
k8s-aiops doctor
```

Optionally annotate the audit trail with who is operating and why — recorded on
every row, never required:

```bash
export K8S_AUDIT_APPROVED_BY="your.name@example.com"
export K8S_AUDIT_RATIONALE="incident INC-1234 — restart the stuck payments rollout"
```

## Kubernetes-specific notes

- **Namespace confusion is the single most common failure mode.** Every
  namespaced tool takes an optional `namespace`; omitting it lists across **all**
  namespaces. A smaller model reliably drops the namespace from a follow-up call
  and then reports a cluster-wide count as if it were the namespace's. Pin the
  namespace in your prompt (or in the target's `namespace:` in
  `~/.k8s-aiops/config.yaml`) and ask the model to restate it in every answer.
- **Context confusion is the expensive one.** `target` selects a *cluster*, not a
  namespace. If you have prod and staging contexts in the same kubeconfig, give
  the agent a config with only the cluster it should touch — the model has no way
  to notice it is on the wrong one, because both look plausible.
- **Authentication is delegated to your kubeconfig.** Unlike the other tools in
  this line, k8s-aiops has **no credential store**: there is nothing to encrypt
  and no master password. (`k8s-aiops secret ...` lists Kubernetes *Secret
  resources* by name — it is not a credential manager.) The agent inherits the RBAC of the
  kubeconfig user. That makes RBAC your strongest guardrail — a read-only
  ServiceAccount kubeconfig enforces read-only at the *cluster*, the only place
  the permission truly lives.
- **`drain_node` is the most dangerous tool here.** It evicts pods cluster-wide
  in effect, and its blast radius is not visible in its arguments. Keep it out of
  the RBAC role you hand the agent unless you specifically intend node drains.
- **Pod names are not stable.** A ReplicaSet-generated pod name changes on every
  rollout, so an id the model cached earlier in the conversation may already be
  gone. Prefer `deployment_get` / `rollout_status` over re-using a pod name.
- **Prefer the RCA tools over multi-step chains.** `pod_health_rca` and
  `workload_readiness_rca` do the list-then-correlate work inside one call, so a
  smaller model does not have to chain reads and keep names/namespaces straight.
- **Secrets are names-only by design.** `secret_list` returns key *names*, never
  values — there is no tool that can exfiltrate a secret payload.

## If your model still struggles

Some behaviours are model-capacity limits rather than prompt problems:

- **Multi-tool workflows time out or drift.** Prefer the `*_rca` tools — they do
  the multi-step correlation inside one call.
- **The model ignores later tool results in a long context.** Ask narrower
  questions, always scope to a namespace, and use `limit` deliberately rather
  than pulling whole-cluster inventories (`pod_list` with no namespace on a busy
  cluster will bury everything else in the context).
- **The model describes calls instead of making them.** This is usually a
  runtime/tool-calling-format mismatch, not a prompt problem — check that your
  client advertises the tools in the format your model was trained on.

Feedback on running this with a specific local model is genuinely useful —
open an issue at
[github.com/AIops-tools/K8s-AIops](https://github.com/AIops-tools/K8s-AIops/issues)
with the model, runtime, and what went wrong.
