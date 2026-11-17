# Agent guardrails — running inference-aiops with a smaller / local model

If you drive these tools with a local model (Llama, Qwen, Mistral … via Goose,
Ollama, LM Studio, or any OpenAI-compatible runtime), you will get noticeably
better results with a short system prompt. This page gives you one, and — more
importantly — tells you which guardrails you **no longer need to write**, because
the tool now enforces them itself.

The distinction matters. A guardrail in a prompt is a request. A guardrail in the
harness is a guarantee. Anything below that we could move into the harness, we did.

## Authorization is not this tool's job — decide it where it belongs

Whether a write should happen is your decision, or the environment's. The tool
does not gate it — there is no read-only switch and no approval prompt to
configure. The two right places to control read vs write:

- **The environment you connect it to.** Restrict the network path so the tool
  can only reach the read/metrics endpoints, or run the Ray dashboard without its
  job-submission API. A write then fails at the server, which is the only place
  the permission actually lives — no skill-side flag can be argued around by a
  model, but a blocked endpoint cannot.
- **Your agent's system prompt.** If you want an observe-only session, tell the
  model not to call the write tools (they are clearly tagged `[WRITE]`).

What the tool *does* guarantee is that you can always see what happened:

## What the tool now enforces — do not waste prompt budget on these

| You might be tempted to prompt | Why you don't need to |
|---|---|
| "Don't invent a value when a field is missing" | A field the engine or Ray dashboard did not return comes back as `null`, never as `""`. An absent job `entrypoint`, a model's `parent` adapter, a replica `state`, or a server-info `version` is distinguishable from an empty one. |
| "Tell me if the output was cut off" | `ray_job_list` returns `{"jobs": [...], "returned": N, "limit": L, "truncated": true/false}`. Truncation is measured against the full fetch, not guessed from a length coincidence. |
| "Say when a metric isn't available" | Signals the engine does not expose come back as `null` rather than `0`. SGLang and TGI expose fewer metrics than vLLM; `diagnose_engine_latency` skips a signal it cannot read instead of fabricating it, and `signalsChecked` shows exactly what it looked at. |
| "Don't suggest scaling on an engine that can't scale" | Multi-replica scale / drain / autoscale are Ray Serve control-plane actions. On a single-process engine (SGLang, TGI) those tools raise `EngineCapabilityError` with an explanation, rather than issuing a call that could never succeed. |
| "Confirm before anything disruptive" | Every traffic-affecting operation (`model_undeploy`, `deployment_redeploy`, `scale_to_zero`, `scale_replicas_down`, `drain_replica`, `replica_restart`, `lora_unload`, `model_sleep`) takes `dry_run=True` for a preview and is `risk=high`. ⚠️ **The double confirmation is a CLI feature, and only `scale_to_zero` has a CLI command** — every other one is reachable only over MCP, where nothing prompts. Keep your own confirmation for those. |
| "Log what you did" | Every call is audited to `~/.inference-aiops/audit.db` regardless of what the model says it did. |

## What still needs a prompt

These are model-behaviour problems the harness cannot fix from the outside.
Recommended setup for a local model (adapt it to your agent client):

```text
You operate a GPU inference cluster through the inference-aiops MCP tools
(vLLM / SGLang / TGI serving engines, plus a Ray Serve control plane).

TOOL USE
- Before answering any question about the current cluster, you MUST call a tool.
  Never answer from memory or assumption.
- Actually invoke the tool. Do not describe the call you would make, and do not
  emit an example JSON response in place of calling it.
- If a tool call fails, report the real error verbatim. Never fill the gap with
  a plausible-sounding answer. A read that fails returns an "error" field rather
  than raising — treat that as "unknown", not as "healthy".

READING RESULTS
- Read the whole result before concluding. If a result contains a "truncated"
  field that is true, say so and re-run with a higher limit instead of treating
  the partial result as complete.
- A null metric means the engine does not expose that signal. Report it as "not
  available" — never substitute 0, and never compare a null against a threshold.
- Report values exactly as returned. Do not normalise or prettify model ids,
  deployment names, replica states, or Ray job statuses.
- When diagnose_engine_latency or diagnose_latency_spike returns probableCauses,
  work through them in the order given and cite the measured number in each
  cause's "signal" — do not substitute your own theory of the bottleneck.

- Only `scale_to_zero` has a CLI command; every other traffic-affecting tool is MCP-only
  and nothing will ask you to confirm it. Call it with `dry_run=True` first, show the
  operator what would change, and wait for an explicit go-ahead.

SCOPE
- Separate observation from interpretation. State what the tools returned, then
  any interpretation, clearly marked as such.
- Do not assert a latency, throughput, or capacity problem unless a tool result
  supports it. High GPU utilisation is not by itself a fault.
- Do not confuse the identifier kinds: a Ray *application* name, a *deployment*
  name within it, a *replica* id, a Ray *job* id (raysubmit_…), and a served
  *model* id are four different things. Never pass one where another is expected.
- cost_per_token is arithmetic over a price you supply, not a billing figure.
  Present it as an estimate with its inputs.
```

## Recommended setup for a local model

Start with a path that *cannot* write — restrict the network route to the
read/metrics endpoints, or expose the Ray dashboard without its job-submission
API — verify, and widen access only when you trust the setup. The
traffic-affecting operations here (`scale_to_zero`, `drain_replica`,
`model_undeploy`) strand or drop live requests and are cheap to invoke:

```bash
inference-aiops doctor
```

Optionally annotate the audit trail with who is operating and why — recorded on
every row, never required:

```bash
export INFERENCE_AUDIT_APPROVED_BY="your.name@example.com"
export INFERENCE_AUDIT_RATIONALE="scaling llm-app down for the maintenance window"
```

## If your model still struggles

Some behaviours are model-capacity limits rather than prompt problems:

- **Multi-tool workflows time out or drift.** Prefer the `diagnose_*` tools —
  `diagnose_engine_latency`, `diagnose_latency_spike`, `diagnose_low_utilization`
  do the multi-signal correlation inside one call, so the model does not have to
  chain reads and keep deployment/replica ids straight.
- **The model ignores later tool results in a long context.** Ask narrower
  questions and use `limit` deliberately rather than dumping a cluster's whole
  job history.
- **The model describes calls instead of making them.** This is usually a
  runtime/tool-calling-format mismatch, not a prompt problem — check that your
  client advertises the tools in the format your model was trained on.

Feedback on running this with a specific local model is genuinely useful —
open an issue at
[github.com/AIops-tools/Inference-AIops](https://github.com/AIops-tools/Inference-AIops/issues)
with the model, runtime, and what went wrong.
