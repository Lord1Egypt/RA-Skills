---
name: pscale-insights
description: Query PlanetScale server-side performance insights, execution samples, query details/summaries, query traffic budgets, query tags, error details, anomaly correlations, and schema recommendations. Use when ranking slow or expensive queries, drilling into individual executions, summarizing one fingerprint, inspecting a query traffic budget, attributing load by sqlcommenter or system tags, investigating the queries behind a full error fingerprint, correlating queries with a resource anomaly, reviewing/showing/dismissing index/schema recommendations, or when a user asks for pscale insights. Triggers on pscale insights, query insights, query show, query summary, traffic budget, query samples, query tags, sqlcommenter, slow queries, query errors, error fingerprint, anomalies, correlated queries, schema recommendations, recommendation show, missing indexes, unused indexes, database bloat.
---

# pscale insights

Use PlanetScale's server-side analysis of production traffic to investigate query performance and schema health. These commands complement the point-in-time, connection-level checks in `pscale inspect`.

## Common commands

```bash
# Rank queries by cumulative execution time (default sort)
pscale insights queries <database> <branch> --org <org> --format json

# Find inefficient read patterns over the last day
pscale insights queries <database> <branch> --org <org> \
  --sort rowsReadPerReturned --period 1d --limit 25 --format json

# Find high-tail-latency queries over the last hour
pscale insights queries <database> <branch> --org <org> \
  --sort p99Latency --period 1h --format json

# Drill into recent executions using fingerprint and keyspace from the query list
pscale insights queries samples <database> <branch> <fingerprint> --org <org> \
  --keyspace <keyspace> --period 1h --limit 25 --format json
pscale insights queries show <database> <branch> <query-id> --org <org> --format json
pscale insights queries summary <database> <branch> <fingerprint> --org <org> \
  --keyspace <keyspace> --period 1h --format json
pscale insights queries traffic-budgets <database> <branch> <fingerprint> --org <org> \
  --keyspace <keyspace> --page 1 --per-page 25 --format json

# Attribute load by friendly query-tag names from the Insights UI
pscale insights tags <database> <branch> --org <org> --format json
pscale insights tags summaries <database> <branch> --org <org> \
  --tags username --tags app --sort totalTime --format json

# Inspect aggregated query failures and detected resource anomalies
pscale insights errors <database> <branch> --org <org> --period 1d --format json
pscale insights errors show <database> <branch> <full-error-fingerprint> --org <org> --period 1d --format json
pscale insights anomalies <database> <branch> --org <org> --format json
pscale insights anomalies show <database> <branch> <anomaly-id> --org <org> --format json

# Review database-level schema recommendations and their proposed DDL
pscale insights recommendations <database> --org <org> --format json
pscale insights recommendations show <database> <number> --org <org> --format json
```

Always pass `--org` explicitly in agent workflows so the organization target is unambiguous. Prefer `--format json` so full normalized SQL, metrics, recommendation details, and proposed DDL remain machine-readable.

## Query ranking

`pscale insights queries` defaults to `--sort totalTime --dir desc --limit 15`. Supported sort keys are:

- `totalTime`, `count`, `errorCount`
- `rowsRead`, `rowsReturned`, `rowsAffected`, `rowsReadPerReturned`
- `p50Latency`, `p99Latency`, `maxLatency`
- `cpuTime`, `ioTime`, `lastRun`

Use `--dir asc|desc`, `--limit <n>`, and an API-supported period such as `1h` or `1d` to keep comparisons explicit. Do not compare differently scoped periods as though they represented the same workload.

## Execution samples

Each JSON record from `pscale insights queries` includes a `fingerprint` and `keyspace`. Pass both to `queries samples`; `--keyspace` is required because the same fingerprint can exist in more than one keyspace.

Samples expose individual executions, including start time, duration, user, rows read/returned, normalized SQL, errors, and attached tags. Use them to validate whether an aggregate represents one outlier or a recurring pattern. Query samples can contain sensitive SQL context, usernames, addresses, or tag values, so do not paste raw output into public issues or logs without review.

`queries show` reads one query execution by query ID. `queries summary` reads fingerprint-level aggregate statistics for one fingerprint/keyspace/time window. `queries traffic-budgets` lists Traffic Control budgets that apply to one fingerprint/keyspace and is paginated; empty later pages mean no rows on that page, not necessarily that no budget exists.

```bash
pscale insights queries show <database> <branch> <query-id> --org <org> --format json
pscale insights queries summary <database> <branch> <fingerprint> \
  --org <org> --keyspace <keyspace> --period 1h --format json
pscale insights queries traffic-budgets <database> <branch> <fingerprint> \
  --org <org> --keyspace <keyspace> --page 1 --per-page 25 --format json
```

Use the exact query ID, fingerprint, and keyspace returned by Insights. These Insights commands forward identifiers to the API as-is, and metrics query selectors are also forwarded opaquely; if a command returns no data or not-found, verify the selector before concluding the query had no activity or budgets.

## Error and anomaly details

The human `errors` table displays the full fingerprint. For JSON automation, copy `error_fingerprint` from the list and pass it unchanged to `errors show`; do not use a shortened display ID. The detail command returns individual failed executions, including users, keyspaces, statements, and error messages.

```bash
pscale insights errors <database> <branch> --org <org> --period 1h --format json
pscale insights errors show <database> <branch> <error_fingerprint> \
  --org <org> --period 1h --limit 25 --format json
```

`anomalies show` returns one anomaly plus queries whose activity correlates with it. Correlation is evidence for investigation, not proof that a query caused the resource event.

```bash
pscale insights anomalies <database> <branch> --org <org> --format json
pscale insights anomalies show <database> <branch> <anomaly-id> \
  --org <org> --format json
```

Treat detailed executions and normalized SQL as potentially sensitive. Compare the anomaly interval with query timing, metrics, and application changes before proposing a fix.

## Query tags

Use `pscale insights tags` to list observed sqlcommenter and system tag keys. The command returns friendly names matching the PlanetScale Insights UI, such as `app`, `controller`, and `username`.

```bash
# Show values observed for one friendly tag name
pscale insights tags show <database> <branch> app --org <org> --period 1h --format json

# Group workload by one or more repeatable tag keys
pscale insights tags summaries <database> <branch> --org <org> \
  --tags app --tags controller --sort p99Latency --period 1d --format json
```

List tags before using `show` or `summaries`. Pass friendly names, not internal `S...`/`B...` IDs. If a friendly name exists in both sources, disambiguate it as `sql:<name>` or `system:<name>`. Optional `--fingerprint` and `--keyspace` filters on `tags` narrow attribution to the intended query or keyspace.

## Investigation workflow

1. Confirm the organization, database, branch, and time window.
2. Rank queries by the metric related to the symptom (`totalTime`, `p99Latency`, `rowsReadPerReturned`, or `errorCount`).
3. Use the returned fingerprint and keyspace to inspect recent `queries samples` when execution-level evidence is needed.
4. List and summarize query tags to attribute the workload to applications, controllers, users, or other observed dimensions.
5. Inspect `errors` and `anomalies` for the same branch and time window, then drill into the relevant full error fingerprint or anomaly ID.
6. Use `queries summary`, `queries show`, or `queries traffic-budgets` when one query needs execution detail, aggregate context, or Traffic Control attribution.
7. Run `pscale inspect all <database> <branch> --org <org> --format json` for live connection-level evidence.
8. Review database-level `recommendations` and `recommendations show` for index, bloat, and sequence-risk findings.
9. Summarize evidence separately from proposed changes.

A not-found response for branch-scoped insights can mean the database/branch does not exist **or** Query Insights is not enabled. Verify both before concluding that there is no data.

## Recommendation safety

Recommendations can include ready-to-apply DDL in JSON output. Use `pscale insights recommendations show <database> <number>` to inspect one recommendation and its full DDL before proposing action. Treat that DDL as a proposal, not an instruction to execute automatically:

- Confirm engine, keyspace/schema, table, and production target.
- Check whether an index is still required by a low-frequency or seasonal workload.
- Review lock/runtime impact and use a branch plus deploy-request workflow where supported.
- Obtain explicit user approval before executing schema changes.
- Verify the result and keep a rollback plan.

Dismissal is also a write: `pscale insights recommendations dismiss <database> <number>`. Confirm the organization, database, and recommendation sequence number from the current list/show output, explain why the finding is inapplicable, and obtain explicit approval before dismissing it. Prefer an informative `--reason`; use `--force` only for already-approved non-interactive execution, then verify the recommendation state.

## Related skills

- **pscale-inspect** — point-in-time, read-only diagnostics against one database connection target
- **pscale-sql** — deliberate one-off SQL queries with role and destructive-query safeguards
- **pscale-deploy-request** — reviewed Vitess/MySQL schema deployment workflow

## References

See [references/commands.md](references/commands.md) for the verified command synopsis and flags.
