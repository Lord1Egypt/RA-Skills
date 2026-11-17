# NRQL Queries and Macros

Run ad-hoc NRQL queries against your New Relic account and manage reusable,
organization-scoped NRQL macros.

## Organization-Scoped Macros

A macro is a named expression fragment referenced as `$macroName` in NRQL. Macros
are shared across accounts in an organization; they are not limited to the account
selected by `--accountId`. Use a User API key with organization-level macro access:
**Organization product admin** or **Organization manager** for create/update/delete;
**Organization read only** grants reads. Never print or paste the key. Macros can
only be used in the organization's primary region; confirm the effective region
(including `NEW_RELIC_REGION`) matches it before troubleshooting a missing macro.

A selected profile alone does not establish the target: environment credentials
such as `NEW_RELIC_API_KEY` override stored profile fields. Before proposing a
write, inspect the effective authenticated organization using the same profile,
region, and environment that will be used for the write:

```bash
# Read-only identity preflight; compare the returned ID/name with the approved org
newrelic nerdgraph query '{ actor { organization { id name } } }' --format JSON
```

**Safety:** Require explicit authorization before creating, updating, or deleting
an organization macro. For create, agree on the organization ID, immutable name,
expression, and parameter count; no macro GUID exists yet. `--org-id` selects an
explicit creation target but does not grant access: confirm that target and access
separately if it differs from the authenticated organization. For update/delete,
read the existing macro first and agree on its exact GUID, name, organization and
proposed change (including expression/count when updating). Do not run a delete as
a test or silently substitute a different profile, region, key, or organization.

Updates affect referencing queries and dashboard widgets, but caching can briefly
delay propagation. A successful entity `get` verifies stored state, not that every
query already uses it. Product documentation says macros are **not supported in
alert conditions**, despite the CLI help's broader warning; do not claim alert
support based on that warning. Deletion is permanent and breaks macro expansion.

Before update/delete, search known saved queries, dashboard widget NRQL (through
approved UI or NerdGraph reads), and checked-in query/application configuration
for the literal `$macroName` reference (including backtick-wrapped special names).
The macro CLI has no reverse-reference lookup. In the approval request, list the
accounts/dashboards/repositories actually inspected, known consumers/owners, and
inaccessible or unsearched areas. Coverage may be partial; no match is not proof
of no consumers. Obtain the owner's explicit acceptance of remaining impact risk,
or stop if scope/access cannot be established. Do not claim an exhaustive impact
review from the macro list alone.

| Command | Flags and behavior |
|---|---|
| `newrelic nrql macros list` | No command-specific flags; organization is inferred from the API key. No `--org-id` or pagination flag. |
| `newrelic nrql macros get --id "$MACRO_ID"` | Required entity GUID, not the macro name; read-only. |
| `newrelic nrql macros create --name NAME --expression EXPRESSION` | Required `--name`/`-n` and `--expression`/`-e`; name is immutable. `--parameter-count` is required for an expression containing positional `$N` tokens. Optional `--org-id` overrides automatic organization lookup for creation only; it does not grant access. |
| `newrelic nrql macros update --id "$MACRO_ID"` | Required GUID and at least one of `--expression`/`-e` or `--parameter-count`. An explicitly empty expression is rejected. The name cannot be changed. |
| `newrelic nrql macros delete --id "$MACRO_ID"` | Required GUID; permanent write, with no command-specific confirmation flag. Obtain approval first. |

For positional tokens such as `$1` and `$2`, supply `--parameter-count` with the
number of distinct tokens **on both create and update whenever the submitted
expression contains `$N` tokens**. On update, omission means the CLI does not send
a count; it is not a guarantee that a parameterized expression update succeeds or
retains the existing count. Upstream documents an API error when that expression
is submitted without `numParameters`. Pass `--parameter-count 0` explicitly with a
parameter-free expression when removing parameters. The CLI forwards these values
rather than validating the token count locally.

Expressions must be valid NRQL expressions (not clauses such as `SELECT ...`), at
most 3,000 characters; subqueries must be parenthesized. Macro expressions cannot
reference another macro. Macros are not supported in time clauses such as `SINCE`,
`UNTIL`, or `TIMESERIES`. Because expansion is textual, parenthesize compound
expressions at definition or use time to preserve operator precedence.

**POSIX-shell quoting:** Single quotes preserve literal `$N` tokens only when the
expression has no embedded single quotes. If it also contains a NRQL string
literal, use double quotes around the shell argument and escape each dollar sign
(e.g. `\$1`), as in the update example below, or correctly escape/concatenate the
single-quoted shell strings. Do not nest unescaped single quotes: the shell can
silently remove the NRQL literal's quotes. Do not interpolate untrusted input.

`$macroName` belongs in `--query`, not another macro's `--expression`. Single-quote
the complete query only when it contains no embedded single quotes. When it has
NRQL single-quoted string literals, use double shell quotes and escape each dollar
sign, as in the mixed-literal query below (or correctly escape/concatenate the
single-quoted shell strings). The same quote-loss warning applies to `--query` as
to `--expression`. These nonparameterized queries demonstrate use; no unverified
parameterized-call syntax is implied.
The following are authored examples, not captured API responses or help output:

```bash
# Read-only inventory and exact-target inspection
newrelic nrql macros list --format JSON
newrelic nrql macros get --id "$MACRO_ID" --format JSON

# Set ORG_ID to the reviewed, approved organization ID from preflight.
# Only after approval: create a nonparameterized macro in that organization
newrelic nrql macros create \
  --name filterProd --org-id "$ORG_ID" \
  --expression "(appName = 'prod')"
# Set MACRO_ID from this create's returned GUID, then verify before proceeding
newrelic nrql macros get --id "$MACRO_ID" --format JSON

# Read-only query after verifying filterProd exists; preserve the literal macro name
newrelic nrql query --accountId "$NEW_RELIC_ACCOUNT_ID" \
  --query 'SELECT count(*) FROM Transaction WHERE $filterProd SINCE 1 hour ago'

# With a NRQL string literal, preserve both its quotes and the literal macro name
newrelic nrql query --accountId "$NEW_RELIC_ACCOUNT_ID" \
  --query "SELECT count(*) FROM Transaction WHERE environment = 'production' AND \$filterProd SINCE 1 hour ago"

# Only after separate approval: preserve literal parameter tokens and precedence
newrelic nrql macros create \
  --name filterStatusRegion --org-id "$ORG_ID" \
  --expression '(status = $1 AND region = $2)' \
  --parameter-count 2
# Set MACRO_ID from this create's returned GUID, then verify before proceeding
newrelic nrql macros get --id "$MACRO_ID" --format JSON

# Only after approval: mix a NRQL string literal with a literal parameter token
newrelic nrql macros update --id "$MACRO_ID" \
  --expression "(appName = 'prod' AND status = \$1)" --parameter-count 1
newrelic nrql macros get --id "$MACRO_ID" --format JSON
```

After each creation, use that response's entity GUID for `get`; after update, read
the same GUID back. Verify name, expression, organization scope, and count.
The CLI's entity JSON uses an integer with `omitempty` for `numParameters`, so a
decoded zero is omitted. On a successful exact-target read, normalize an absent
field to zero for count comparison (for example, `jq '.numParameters // 0'`), not
automatic failure. Absence alone does not prove a clearing write succeeded: also
check the write outcome and expected parameter-free expression, GUID, and scope.
Verify query behavior separately when propagation matters; entity read-back does
not bypass caching. After an authorized deletion, read the same GUID back and
confirm a not-found result rather than treating a transport/authentication error
as proof of deletion. Do not automatically retry an uncertain write.

Create/get/update return entity objects; list returns an array when results are
present. Empty inventory and deletion use info-log messages, not JSON entity data.
Use global `--format JSON` (default), `--format YAML`, or `--plain` as appropriate;
do not assume every successful command emits parseable JSON. The list implementation
issues one entity-search request without a cursor loop; do not treat a returned
page as a proven exhaustive inventory for destructive decisions.

Official implementation and command reference:
[`internal/nrql/command_macros.go`](https://github.com/newrelic/newrelic-cli/blob/91d426a0d1c19cd1127d60081323ff6e88ff83eb/internal/nrql/command_macros.go),
[`internal/nrql/README.md`](https://github.com/newrelic/newrelic-cli/blob/91d426a0d1c19cd1127d60081323ff6e88ff83eb/internal/nrql/README.md).

Product rules, permissions, and caching limitations:
[Create and manage NRQL macros](https://docs.newrelic.com/docs/nrql/nrql-macros/create-manage-nrql-macros/)
and [NRQL macro permissions](https://docs.newrelic.com/docs/nrql/nrql-macros/nrql-macros-overview/#macro-permissions).

---

## Basic Syntax

```bash
newrelic nrql query \
  --accountId $NEW_RELIC_ACCOUNT_ID \
  --query "YOUR NRQL HERE"
```

---

## Key Event Types

| Event Type | What it tracks |
|---|---|
| `Transaction` | Web/non-web request timings |
| `TransactionError` | Exceptions and errors |
| `DatabaseTrace` | Individual DB query timings |
| `ExternalTrace` | Outbound HTTP calls |
| `SystemSample` | Host CPU, memory, disk |
| `ProcessSample` | Per-process metrics |
| `Log` | Log lines (if log forwarding enabled) |
| `PageView` | Browser page load events |
| `JavaScriptError` | Front-end JS errors |

---

## Common Patterns

### Response Time

```nrql
SELECT average(duration), percentile(duration, 95, 99)
FROM Transaction
WHERE appName = 'my-app'
TIMESERIES 5 minutes
SINCE 1 hour ago
```

### Error Rate

```nrql
SELECT percentage(count(*), WHERE error IS true) AS 'Error %'
FROM Transaction
WHERE appName = 'my-app'
TIMESERIES 5 minutes
SINCE 1 hour ago
```

### Throughput (RPM)

```nrql
SELECT rate(count(*), 1 minute) AS 'RPM'
FROM Transaction
WHERE appName = 'my-app'
TIMESERIES
SINCE 1 hour ago
```

### Slowest Endpoints

```nrql
SELECT average(duration)
FROM Transaction
WHERE appName = 'my-app'
FACET name
SINCE 1 hour ago
LIMIT 10
ORDER BY average(duration) DESC
```

### DB Bottlenecks

```nrql
SELECT average(duration), count(*)
FROM DatabaseTrace
WHERE appName = 'my-app'
FACET statement
SINCE 1 hour ago
LIMIT 10
ORDER BY average(duration) DESC
```

### Compare Two Time Windows

```nrql
SELECT average(duration)
FROM Transaction
WHERE appName = 'my-app'
SINCE 1 hour ago
COMPARE WITH 1 day ago
```

### Count Errors by Type

```nrql
SELECT count(*)
FROM TransactionError
WHERE appName = 'my-app'
FACET error.class
SINCE 1 hour ago
```

### Host CPU

```nrql
SELECT average(cpuPercent)
FROM SystemSample
FACET hostname
TIMESERIES 5 minutes
SINCE 1 hour ago
```

### Host Memory

```nrql
SELECT average(memoryUsedPercent)
FROM SystemSample
FACET hostname
TIMESERIES 5 minutes
SINCE 1 hour ago
```

---

## Time Range Shortcuts

```
SINCE 30 minutes ago
SINCE 1 hour ago
SINCE 3 hours ago
SINCE 1 day ago
SINCE 1 week ago
SINCE '2026-02-01 00:00:00' UNTIL '2026-02-02 00:00:00'
```

---

## Useful Clauses

```nrql
FACET name          -- group by field
TIMESERIES 5 min    -- time series chart
LIMIT 20            -- max results
ORDER BY count() DESC
COMPARE WITH 1 day ago
WHERE appName = 'x' AND duration > 1
```

---

## Output Formatting

```bash
# Raw JSON
newrelic nrql query --accountId $NEW_RELIC_ACCOUNT_ID \
  --query "SELECT count(*) FROM Transaction SINCE 1 hour ago" \
  --format JSON

# JSON is the default; --plain emits compact text
newrelic nrql query --accountId $NEW_RELIC_ACCOUNT_ID \
  --query "SELECT count(*) FROM Transaction SINCE 1 hour ago"
```
