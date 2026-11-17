# Agent guardrails — running monitoring-aiops with a smaller / local model

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

- **The account you connect with.** Give it a SolarWinds/PRTG/Zabbix login with
  read-only monitoring scope. A write then fails at the server, which is the
  only place the permission actually lives — no skill-side flag can be argued
  around by a model, but a revoked permission cannot be.
- **Your agent's system prompt.** If you want an observe-only session, tell the
  model not to call the write tools (they are clearly tagged `[WRITE]`).

What the tool *does* guarantee is that you can always see what happened:

## What the tool enforces — do not waste prompt budget on these

| You might be tempted to prompt | Why you don't need to |
|---|---|
| "Never write to the monitoring database" | `swql_query` accepts a single read-only `SELECT` and nothing else — no verb invoke, no multi-statement, no DELETE. Orion state changes only happen through the named, governed write tools. |
| "Don't invent a value when a field is missing" | A column the platform did not return comes back as `null`, never as `""`. An absent Orion `StatusDescription`, a PRTG sensor `message`, a Zabbix host `dns` — all distinguishable from a genuinely empty one. |
| "Tell me if the output was cut off" | Every row-capped read returns `returned` / `limit` / `truncated`: `swql_query`, `swql_canned`, `list_events`, `zabbix_events`, `zabbix_item_history`, and `interface_status` with a `top`. Truncation is measured — one row past the cap is fetched, or the full set is counted before the cut — never guessed from a length coincidence. |
| "Deduplicate the alert storm before showing me" | `active_alerts` already rolls repeats of the same message into one row with a `count` and up to three `examples`, worst-first. Report the rollup; do not re-count the raw list. |
| "Normalise severity across platforms" | Zabbix's 0–5 scale is already mapped to canonical `level` values (`info`/`warning`/`high`/`critical`) alongside the platform's own `severity` name. Use `level` for cross-platform statements and `severity` when quoting the platform. |
| "Confirm before anything disruptive" | `remove_node`, `unmanage_node`, `mute_alerts` and the maintenance-window writes all take `dry_run=True` for a preview, and `remove_node`, `unmanage_node` and `zabbix_delete_maintenance` are `risk=high`. ⚠️ **The double confirmation is a CLI feature, and of the writes only `alert_acknowledge` and `undo apply` have CLI commands** — every tool named here is reachable only over MCP, where nothing prompts. Keep your own confirmation for them. |
| "Log what you did" | Every call is audited to `~/.monitoring-aiops/audit.db` regardless of what the model says it did. |

## What still needs a prompt

These are model-behaviour problems the harness cannot fix from the outside.
Recommended setup for a local model (adapt it to your agent client):

```text
You operate an enterprise monitoring system through the monitoring-aiops MCP
tools. A target is SolarWinds Orion, Paessler PRTG, or Zabbix — check which
before reasoning about what a field means.

TOOL USE
- Before answering any question about the current monitored estate, you MUST
  call a tool. Never answer from memory or assumption.
- Actually invoke the tool. Do not describe the call you would make, and do not
  emit an example JSON response in place of calling it.
- If a tool call fails, report the real error verbatim. Never fill the gap with
  a plausible-sounding answer. A read that fails returns an "error" field rather
  than raising — treat that as "unknown", not as "everything is fine".
- Prefer the named canned SWQL (swql_library / swql_canned) over writing your
  own query. Hand-written SWQL is where small models most often produce
  syntactically valid nonsense.

READING RESULTS
- Read the whole result before concluding. If a result contains a "truncated"
  field that is true, say so and re-run with a higher limit instead of treating
  the partial result as complete. An alert count from a truncated read is not
  the number of alerts.
- A null field means the platform did not return that value. Report it as "not
  available" — never infer it.
- Report values exactly as returned. Do not translate status codes, severity
  names, node captions, or sensor names into your own vocabulary.
- Acknowledged is not the same as resolved. An acknowledged alert is still
  active; say which you mean.

- None of the node or maintenance-window writes has a CLI command, so nothing will ask you
  to confirm them — `remove_node` and `unmanage_node` least of all. Call with
  `dry_run=True` first and wait for an explicit go-ahead.

SCOPE
- Separate observation from interpretation. State what the tools returned, then
  any interpretation, clearly marked as such.
- Do not assert an outage, root cause, or business impact unless a tool result
  supports it. A down sensor is one sensor, not necessarily a down service.
- Do not confuse the identifier kinds: an Orion node Caption, an AlertActiveID,
  a PRTG objid, and a Zabbix eventid/triggerid/itemid are different namespaces
  and are not interchangeable across targets.
- Muting, unmanaging, and maintenance windows suppress alerting; they do not fix
  anything. Never describe them as a resolution.
```

## Recommended setup for a local model

Start with a connection that *cannot* write — a SolarWinds/PRTG/Zabbix account
with read-only monitoring scope — verify, and widen the account's permission
only when you trust the setup:

```bash
monitoring-aiops doctor
```

Optionally annotate the audit trail with who is operating and why — recorded on
every row, never required:

```bash
export MONITORING_AUDIT_APPROVED_BY="your.name@example.com"
export MONITORING_AUDIT_RATIONALE="change window CHG0041231, muting core-sw1"
```

## If your model still struggles

Some behaviours are model-capacity limits rather than prompt problems:

- **Multi-tool workflows time out or drift.** Lead with `noc_rollup` (SolarWinds)
  or `active_alerts` — they do the correlation and dedup inside one call, so the
  model does not have to chain reads and keep ids straight.
- **The model writes broken SWQL.** Use `swql_library` and `swql_canned` — the
  canned queries answer the most-asked questions and are already parameterised.
- **The model ignores later tool results in a long context.** Ask narrower
  questions and use `top` / `limit` deliberately rather than pulling every
  sensor in the estate.
- **The model describes calls instead of making them.** This is usually a
  runtime/tool-calling-format mismatch, not a prompt problem — check that your
  client advertises the tools in the format your model was trained on.

Feedback on running this with a specific local model is genuinely useful —
open an issue at
[github.com/AIops-tools/Monitoring-AIops](https://github.com/AIops-tools/Monitoring-AIops/issues)
with the model, runtime, and what went wrong.
