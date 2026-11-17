# Agent guardrails — running observability-aiops with a smaller / local model

If you drive these tools with a local model (Llama, Qwen, Mistral … via Goose,
Ollama, LM Studio, or any OpenAI-compatible runtime), you will get noticeably
better results with a short system prompt. This page gives you one, and — more
importantly — tells you which guardrails you **no longer need to write**, because
the tool now enforces them itself.

The distinction matters. A guardrail in a prompt is a request. A guardrail in the
harness is a guarantee. Anything below that we could move into the harness, we did.

## What the tool now enforces — do not waste prompt budget on these

| You might be tempted to prompt | Why you don't need to |
|---|---|
| "Don't invent a value when a field is missing" | A field the API did not return comes back as `null`, never as `""`. An alert with no `severity` label, a scrape target that has never errored, a recording rule with no alert `state`, a silence with no `comment` — all report `null`, distinguishable from a genuinely empty value. |
| "Tell me if the output was cut off" | Bounded reads (`loki_query`, `loki_tail_errors`, `loki_labels`, `loki_label_values`, `instant_query`, `range_query`, `label_values`, `series_metadata`, `undo_list`) return `{"returned": N, "limit": L, "truncated": true/false}` alongside the rows. For the Loki reads truncation is **measured** — one line beyond the limit is requested — not guessed from a length coincidence. |
| "Preserve the ordering / tell me what's most urgent" | The analysis tools already return worst-first: `firing_alert_rca` ranks by severity, `target_scrape_health_analysis` puts down targets before slow ones, `alert_noise_and_flap_analysis` sorts by instance count. Priority is the list order, and each entry carries the measured number it was ranked on. |
| "Confirm before anything destructive" | Every write tool takes `dry_run` for a preview, and `delete_dashboard` is `risk=high`. ⚠️ **Apart from `undo apply`, no write tool here has a CLI command**, so the CLI double confirmation never applies to one: they are reachable only over MCP, where nothing prompts. Keep your own confirmation for them. |
| "Log what you did" | Every call is audited to `~/.observability-aiops/audit.db` regardless of what the model says it did, and reversible writes record an undo token (`undo_list` / `undo_apply`). |
| "Don't hammer the same call in a loop" | The runaway guard trips a circuit breaker on tight poll/retry loops — a safety backstop, not authorization. |

Authorization is not this tool's job. Whether a write is allowed to happen is
decided by the account you connect it with, or by your agent's own judgement —
not by this harness. See "Recommended setup for a local model" below for how to
enforce read-only at the account instead of in a prompt.

## What still needs a prompt

These are model-behaviour problems the harness cannot fix from the outside.
Recommended setup for a local model (adapt it to your agent client):

```text
You operate a self-hosted observability stack (Prometheus, Alertmanager,
Grafana, Loki) through the observability-aiops MCP tools.

TOOL USE
- Before answering any question about the current state of the stack, you MUST
  call a tool. Never answer from memory or assumption.
- Actually invoke the tool. Do not describe the call you would make, and do not
  emit an example JSON response in place of calling it.
- If a tool call fails, report the real error verbatim. Never fill the gap with
  a plausible-sounding answer.

READING RESULTS
- Read the whole result before concluding. If a result contains a "truncated"
  field that is true, say so and re-run with a higher limit (or a narrower
  selector) instead of treating the partial result as complete.
- A null field means the API did not return that value. Report it as "not
  available" — never infer it. A missing "severity" label is not "info".
- Report values exactly as returned. Do not normalise, translate, or prettify
  alert names, severities, label values, or health strings.
- When an analysis tool returns ranked findings, work in the order given and
  cite the measured number the ranking is based on.

QUERIES
- PromQL goes to instant_query / range_query; LogQL goes to loki_query. They are
  different languages — do not send one to the other.
- A LogQL query MUST carry a stream selector (e.g. '{app="api"}'). A query
  without one is rejected by the tool, not silently widened.
- Use label_values / loki_labels / loki_label_values to discover real label
  names and values before writing a selector. Do not guess a job, instance, or
  app name.

- Apart from `undo apply`, no write tool here has a CLI command, so nothing will ask you
  to confirm one —
  `delete_dashboard` included. Call with `dry_run=True` first, show the operator what would
  change, and wait for an explicit go-ahead.

SCOPE
- Separate observation from interpretation. State what the tools returned, then
  any interpretation, clearly marked as such.
- Do not assert an outage, saturation, or regression unless a tool result
  supports it.
- Do not add generic advice that does not follow from the tool output.
- Keep the identifiers straight: an alertname is not a label value; a silence ID
  is not a dashboard UID; a "job" is a scrape config name while an "instance" is
  a single scraped endpoint.
```

## Recommended setup for a local model

There is no read-only switch to set — this tool does not decide whether a
write is permitted. If you want the connection to be read-only until you trust
the setup, enforce it at the account: give it a Grafana token with only Viewer
scope, and a Prometheus/Alertmanager reached without the admin/write API. Any
write attempt then fails at the server, which is the place that actually owns
the permission.

```bash
observability-aiops doctor
```

When you are ready to allow writes (silences, annotations, dashboards), connect
with a token that has write scope, and optionally name yourself on the audit
row — it is an annotation, not a gate:

```bash
export OBSERVABILITY_AUDIT_APPROVED_BY="your.name@example.com"
export OBSERVABILITY_AUDIT_RATIONALE="silencing NodeDiskFilling during the 2026-07-20 disk swap"
```

## If your model still struggles

Some behaviours are model-capacity limits rather than prompt problems:

- **Multi-tool workflows time out or drift.** Prefer the analysis tools —
  `firing_alert_rca`, `target_scrape_health_analysis`,
  `alert_noise_and_flap_analysis`, `log_error_burst_rca`, and
  `alert_log_context` do the multi-step correlation inside one call, so the
  model does not have to chain reads and keep alertnames, jobs, and selectors
  straight across turns.
- **The model ignores later tool results in a long context.** Ask narrower
  questions, scope PromQL and LogQL with real label matchers, and use `--limit`
  deliberately rather than pulling whole label sets or metric-name lists.
- **The model describes calls instead of making them.** This is usually a
  runtime/tool-calling-format mismatch, not a prompt problem — check that your
  client advertises the tools in the format your model was trained on.

## Verification status

These tools have been exercised against a real stack — Prometheus 3.x,
Alertmanager, and Grafana 13 — covering firing-alert and scrape-target RCA,
governed silence and dashboard writes, and undo replay. The behaviours described
above are observed, not only unit-tested.

Feedback on running this with a specific local model is genuinely useful —
open an issue at
[github.com/AIops-tools/Observability-AIops](https://github.com/AIops-tools/Observability-AIops/issues)
with the model, runtime, and what went wrong.
