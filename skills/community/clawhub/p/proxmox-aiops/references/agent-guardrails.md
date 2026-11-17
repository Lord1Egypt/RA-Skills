# Agent guardrails — running proxmox-aiops with a smaller / local model

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
| "Don't invent a value when a field is missing" | A field the API did not return comes back as `null`, never as `""`. Absent and empty are distinguishable in the payload. |
| "Tell me if the output was cut off" | Anything with a `limit` returns `{"lines": [...], "returned": N, "limit": L, "truncated": true/false}`. Truncation is measured (one extra row is fetched), not guessed. |
| "Preserve the ordering / tell me what's most urgent" | `diagnose` findings carry an explicit 1-based `rank`, worst-first. Priority is in the payload, not implied by list position. |
| "Confirm before anything destructive" | Destructive operations require a `--dry-run`-able preview + double confirmation at the CLI. |
| "Log what you did" | Every call is audited to `~/.proxmox-aiops/audit.db` regardless of what the model says it did. |

## What still needs a prompt

These are model-behaviour problems the harness cannot fix from the outside.
Recommended setup for a local model (adapt it to your agent client):

```text
You operate a Proxmox VE environment through the proxmox-aiops MCP tools.

TOOL USE
- Before answering any question about the current Proxmox environment, you MUST
  call a tool. Never answer from memory or assumption.
- Actually invoke the tool. Do not describe the call you would make, and do not
  emit an example JSON response in place of calling it.
- If a tool call fails, report the real error verbatim. Never fill the gap with
  a plausible-sounding answer.

READING RESULTS
- Read the whole result before concluding. If a result contains a "truncated"
  field that is true, say so and re-run with a higher limit instead of treating
  the partial result as complete.
- A null field means the API did not return that value. Report it as "not
  available" — never infer it.
- Report values exactly as returned. Do not normalise, translate, or prettify
  status strings, severities, or IDs.
- When a diagnose result has findings, work in "rank" order and cite the
  measured number in each finding's "detail".

SCOPE
- Separate observation from interpretation. State what the tools returned, then
  any interpretation, clearly marked as such.
- Do not assert a capacity, performance, or availability problem unless a tool
  result supports it.
- Do not add generic advice that does not follow from the tool output.
- Do not confuse a VMID with a node name, or a task UPID with either.
```

## Recommended setup for a local model

Authorization is not this tool's job — decide it via the account you connect
with or the agent's prompt, not a switch in the tool. To work read-only, connect
with a Proxmox VE user or API token granted only read privileges (no
`VM.*`/`Datastore.*` write roles); a write then fails at the server, the place
that actually owns the permission.

```bash
proxmox-aiops doctor          # verify connectivity with your least-privilege token
```

Optionally, annotate who is running changes and why — these land on the audit
row, and are never required and never blocking:

```bash
export PROXMOX_AUDIT_APPROVED_BY="your.name@example.com"
export PROXMOX_AUDIT_RATIONALE="scheduled maintenance window"
```

## If your model still struggles

Some behaviours are model-capacity limits rather than prompt problems:

- **Multi-tool workflows time out or drift.** Prefer the `diagnose` tools — they
  do the multi-step correlation inside one call, so the model does not have to
  chain reads and keep IDs straight.
- **The model ignores later tool results in a long context.** Ask narrower
  questions and use `--limit` deliberately rather than pulling whole inventories.
- **The model describes calls instead of making them.** This is usually a
  runtime/tool-calling-format mismatch, not a prompt problem — check that your
  client advertises the tools in the format your model was trained on.

Feedback on running this with a specific local model is genuinely useful —
open an issue at
[github.com/AIops-tools/Proxmox-AIops](https://github.com/AIops-tools/Proxmox-AIops/issues)
with the model, runtime, and what went wrong.
