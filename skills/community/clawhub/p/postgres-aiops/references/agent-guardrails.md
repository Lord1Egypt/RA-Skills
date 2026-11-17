# Agent guardrails — running postgres-aiops with a smaller / local model

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
| "Don't invent a value when a field is missing" | A column the server returned as SQL `NULL` comes back as `null`, never as `""`. `lastAutovacuum: null` means the table was *never* autovacuumed; `unit: null` means the setting is not a numeric quantity; `plugin: null` means the replication slot is physical, not logical. Absent and empty are distinguishable in the payload. |
| "Tell me if the output was cut off" | Anything with a `limit` returns `{"statements": [...], "returned": N, "limit": L, "truncated": true/false}`. Truncation is **measured** — one extra row is fetched — not guessed from the row count happening to equal the limit. An analysis that pulled a truncated read also carries `sourceTruncated`. |
| "Preserve the ordering / tell me what's most urgent" | Ranked reads are already ordered worst-first (`table_bloat` by dead tuples, `index_bloat` by estimated bloat, `blocking_lock_chain_rca` by how many backends a root blocker holds up), and every finding cites the number that triggered it. |
| "Confirm before anything destructive" | Destructive operations require a `--dry-run`-able preview + double confirmation at the CLI for high-risk tiers such as `terminate_backend` and `drop_index`. |
| "Log what you did" | Every call is audited to `~/.postgres-aiops/audit.db` regardless of what the model says it did. Reversible writes (`create_index`, `drop_index`, `update_setting`) also record an undo token capturing the pre-change state. |

**Authorization is not this tool's job.** Whether a write is permitted is decided by the account
you connect it with (connect with a PostgreSQL role that has no write privileges — a read-only
role, or one without INSERT/UPDATE/DELETE/DDL — and the write fails at the server) or by your
agent's prompt. `POSTGRES_AUDIT_APPROVED_BY` / `POSTGRES_AUDIT_RATIONALE` are optional annotations
recorded on the audit row; they are never required and never block a call.

## What still needs a prompt

These are model-behaviour problems the harness cannot fix from the outside.
Recommended setup for a local model (adapt it to your agent client):

```text
You operate a PostgreSQL server through the postgres-aiops MCP tools.

TOOL USE
- Before answering any question about the current database, you MUST call a
  tool. Never answer from memory or assumption.
- Actually invoke the tool. Do not describe the call you would make, and do not
  emit an example JSON response in place of calling it.
- If a tool call fails, report the real error verbatim. Never fill the gap with
  a plausible-sounding answer.

READING RESULTS
- Read the whole result before concluding. If a result has "truncated": true
  (or "sourceTruncated": true), say so and re-run with a higher limit instead of
  treating the partial result as complete.
- A null field means the server returned SQL NULL for that column. Report it as
  "not available" or, where it is meaningful, as what the NULL means — a null
  lastAutovacuum means the table has never been autovacuumed. Never infer it.
- Report values exactly as returned. Do not normalise, translate, or prettify
  states, wait events, LSNs, or identifiers.
- Cite the measured number from each finding's "detail" when explaining a cause.

SCOPE
- Separate observation from interpretation. State what the tools returned, then
  any interpretation, clearly marked as such.
- Do not assert a performance, bloat, or replication problem unless a tool
  result supports it.
- Do not add generic PostgreSQL tuning advice that does not follow from the
  tool output.
- Keep the identifiers straight. A database, a schema, a relation (table), an
  index, a backend pid, and a queryid are all different things: a pid is an OS
  process id from pg_stat_activity, a queryid is a pg_stat_statements
  fingerprint, and a relation is named schema.table. Never pass one where
  another is expected, and never invent a schema qualification.
- pg_stat_statements counters are cumulative since the last stats reset, and
  idx_scan is cumulative too. Do not describe them as "recent" activity.
```

## Recommended setup for a local model

Until you trust the setup, connect the tool with a read-only PostgreSQL role
(no INSERT/UPDATE/DELETE/DDL) — that is real enforcement at the server, not a
prompt asking the model to behave:

```bash
postgres-aiops init       # point it at a read-only role
postgres-aiops doctor
```

Then, when you are ready to allow writes, point `init` (or `secret set`) at a
role with write privileges, and optionally set an approver so the audit trail
carries an accountable name:

```bash
export POSTGRES_AUDIT_APPROVED_BY="your.name@example.com"
export POSTGRES_AUDIT_RATIONALE="scheduled maintenance window 2026-07-20"
```

## If your model still struggles

Some behaviours are model-capacity limits rather than prompt problems:

- **Multi-tool workflows time out or drift.** Prefer the flagship analyses —
  `slow_query_rca`, `bloat_and_vacuum_analysis`, `blocking_lock_chain_rca` — and
  `overview`. They do the multi-step correlation inside one call, so the model
  does not have to chain reads and keep pids and queryids straight.
- **The model ignores later tool results in a long context.** Ask narrower
  questions and use `--limit` deliberately rather than pulling whole catalogs.
  `show_settings` in particular returns hundreds of rows without a pattern —
  always pass one.
- **The model describes calls instead of making them.** This is usually a
  runtime/tool-calling-format mismatch, not a prompt problem — check that your
  client advertises the tools in the format your model was trained on.

## A note on verification

Unlike a purely mocked integration, postgres-aiops has been exercised against a
real PostgreSQL 16 server: the bloat/vacuum RCA correctly identified a table with
~50% dead tuples, and the `create_index` / `drop_index` governance path was
confirmed end-to-end (audit row written, undo token capturing the prior
`pg_get_indexdef` output). Treat the read paths as verified and the more exotic
write paths as preview.

Feedback on running this with a specific local model is genuinely useful —
open an issue at
[github.com/AIops-tools/Postgres-AIops](https://github.com/AIops-tools/Postgres-AIops/issues)
with the model, runtime, and what went wrong.
