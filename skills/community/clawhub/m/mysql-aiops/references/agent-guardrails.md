# Agent guardrails — running mysql-aiops with a smaller / local model

If you drive these tools with a local model (Llama, Qwen, Mistral … via Goose,
Ollama, LM Studio, or any OpenAI-compatible runtime), you will get noticeably
better results with a short system prompt. This page gives you one, and — more
importantly — tells you which guardrails you **no longer need to write**, because
the tool now enforces them itself.

The distinction matters. A guardrail in a prompt is a request. A guardrail in the
harness is a guarantee. Anything below that we could move into the harness, we did.

## What the tool now enforces — do not waste prompt budget on these

Authorization is not this tool's job — decide it via the account you connect with or the
agent's prompt, not via a switch this skill provides. See below for the account-side way to
get a read-only setup.

| You might be tempted to prompt | Why you don't need to |
|---|---|
| "Never write SQL that modifies data" | The tool exposes no arbitrary-SQL surface at all. Every statement is built from a fixed template; identifiers are validated against a strict charset and backtick-quoted, and values are always bound as query parameters. `explain_query` runs `EXPLAIN`, not your statement. |
| "Don't invent a value when a field is missing" | A NULL column comes back as `null`, never as `""`. A sleeping session's `query` is `null` (it is running nothing), not blank; MariaDB's absent `gtid_mode` is `null`, not `""`. |
| "Tell me if the output was cut off" | `top_queries`, `table_sizes`, `table_fragmentation` and `table_status` return `{"statements"/"tables": [...], "returned": N, "limit": L, "truncated": true/false}`. Truncation is measured — one extra row is requested — not guessed from a length coincidence. |
| "Make it show the number it judged on" | Every finding cites the values that tripped it — `noIndexUsedPct`, `rowsExaminedPerSent`, `lockTimePct`, `tmpDiskTables` and `calls` for a statement (the `worst` block additionally reports `meanTimeMs` and `totalTimeMs`, which no check is tripped by); `ioThreadRunning`, `sqlThreadRunning` and `secondsBehindSource` for a replica — so a claim can be checked against a figure rather than taken on the model's word. `lock_wait_rca` returns no findings at all: it gives you `roots` ordered by `blockedCount` plus `worstRootId`, which names the blocker outright. |
| "Confirm before anything destructive" | `drop_index`, `kill_query`/`kill_session` and `optimize_table` require a `--dry-run`-able preview plus double confirmation at the CLI. `drop_index` captures the index's `SHOW CREATE` definition first, so the undo token can recreate it exactly. |
| "Log what you did" | Every governed call is audited to `~/.mysql-aiops/audit.db` regardless of what the model says it did. |

## What still needs a prompt

These are model-behaviour problems the harness cannot fix from the outside.

⚠️ **Do not read priority off list position — except from `lock_wait_rca`.** `slow_query_rca`
and `replication_lag_rca` append their `findings` in the order the checks run; the sort inside
`slow_query_rca` orders the *statements* it picks `worst` from, not the findings. Neither
finding carries a `rank` or a `severity`, so nothing in those two payloads says which finding
matters most. (`lock_wait_rca` is the exception — its `roots` are ordered by `blockedCount`
and `worstRootId` names the worst one.)

Recommended setup for a local model (adapt it to your agent client):

```text
You operate a MySQL or MariaDB server through the mysql-aiops MCP tools.

TOOL USE
- Before answering any question about the current database, you MUST call a
  tool. Never answer from memory or assumption.
- Actually invoke the tool. Do not describe the call you would make, and do not
  emit an example JSON response in place of calling it.
- If a tool call fails, report the real error verbatim. Never fill the gap with
  a plausible-sounding answer.

READING RESULTS
- Read the whole result before concluding. If a result contains a "truncated"
  field that is true, say so and re-run with a higher limit. The slowest query
  on the server may be the one just past the cut-off.
- Findings from `slow_query_rca` and `replication_lag_rca` are NOT ordered by severity and
  carry no rank. Weigh each finding's own numbers and say which one you acted on; never
  treat the first as the headline.
- A null field means the server returned NULL or had no such value. Report it
  as "not available" — never infer it. A session with a null "query" is idle,
  not running an unknown statement.
- Report values exactly as returned. Times are already converted to
  milliseconds; do not re-scale them. Do not prettify digests or table names.
- Cite the measured number. "mean_time 240ms over 15,000 calls" is useful;
  "this query is slow" is not.

SCOPE
- Separate observation from interpretation. State what the tools returned, then
  any interpretation, clearly marked as such.
- Do not recommend an index unless unused_indexes / redundant_indexes or an
  EXPLAIN in the result supports it. Adding an index is not free.
- Do not attribute replication lag to a cause the replication tools did not
  measure. Check whether the IO and SQL threads are actually running first.
- Do not confuse a thread id with a digest, a schema with a table, or
  rows_examined with rows_sent — the gap between those last two is the point.
- MySQL and MariaDB differ. The flavor is reported by server_version; do not
  suggest a MySQL-only feature (like gtid_mode) on MariaDB.
- performance_schema may be OFF, in which case top_queries returns nothing.
  That is a configuration fact, not "the server has no slow queries".
```

## Recommended setup for a local model

Point the tool at a read-only database account until you trust the setup — that is where
the guarantee actually lives, not in a switch this skill provides:

```bash
mysql-aiops doctor
```

Grant the connecting account only `SELECT`, `PROCESS` and `REPLICATION CLIENT` (no
`INSERT`/`UPDATE`/`DELETE`/DDL); any write tool the model calls will then fail at the server.
When you are ready to allow writes, grant the account write privileges and, if you want a
name on the audit trail, set an approver annotation (optional — it is recorded, never
required):

```bash
export MYSQL_AUDIT_APPROVED_BY="your.name@example.com"
export MYSQL_AUDIT_RATIONALE="index cleanup, change ticket DB-4412"
```

## If your model still struggles

Some behaviours are model-capacity limits rather than prompt problems:

- **Multi-tool workflows time out or drift.** Prefer the RCA tools —
  `slow_query_rca` correlates digests, index usage and examined-row ratios
  inside one call, so the model does not have to chain `top_queries`,
  `explain_query` and `index_stats` and keep digests straight.
- **The model ignores later tool results in a long context.** Statement digests
  are the big payload here. Use `--limit` deliberately rather than pulling 200
  digests when you want the top 10.
- **The model describes calls instead of making them.** This is usually a
  runtime/tool-calling-format mismatch, not a prompt problem — check that your
  client advertises the tools in the format your model was trained on.

Feedback on running this with a specific local model is genuinely useful —
open an issue at
[github.com/AIops-tools/MySQL-AIops](https://github.com/AIops-tools/MySQL-AIops/issues)
with the model, runtime, and what went wrong.
