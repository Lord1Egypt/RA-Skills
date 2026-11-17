# `pscale insights` command reference

Unless a section says otherwise, help fences below are exact output from the official, checksum-verified PlanetScale CLI v0.324.0 macOS arm64 release binary after normalizing only trailing whitespace.

## `pscale insights`

```text
Surface PlanetScale's server-side analysis of a database: aggregated query
statistics (latency percentiles, rows read, errors), detected anomalies, and
schema recommendations, all computed from production traffic.

For live, connection-level diagnostics (table sizes, locks, running queries),
see pscale inspect.

Usage:
  pscale insights [command]

Available Commands:
  anomalies       List detected resource anomalies (CPU, memory, IOPS, rows read/written)
  errors          List queries that are failing with errors
  queries         List the top queries by a performance metric
  recommendations List schema recommendations (unused/duplicate indexes, bloat, missing indexes)
  tags            List query tag keys (sqlcommenter / system)

Flags:
  -h, --help         help for insights
      --org string   The organization for the current user

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Use "pscale insights [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## `pscale insights queries`

```text
List the top queries by a performance metric

Usage:
  pscale insights queries <database> <branch> [flags]
  pscale insights queries [command]

Examples:
  # Queries taking the most cumulative time
  pscale insights queries mydb main --org myorg

  # Most expensive read patterns (rows read vs returned)
  pscale insights queries mydb main --org myorg --sort rowsReadPerReturned

  # Highest p99 latency over the last hour
  pscale insights queries mydb main --org myorg --sort p99Latency --period 1h

  # Recent executions for a fingerprint from the list (keyspace is required)
  pscale insights queries samples mydb main b129e8fa --org myorg --keyspace mydb

Available Commands:
  samples     List recent executions for a query fingerprint

Flags:
      --dir string      Sort direction: asc or desc (default "desc")
  -h, --help            help for queries
      --limit int       Number of queries to return (default 15)
      --period string   Time period to aggregate over (e.g. 1h, 1d)
      --sort string     Metric to rank queries by, one of: totalTime, count, errorCount, rowsRead, rowsReturned, rowsAffected, rowsReadPerReturned, p50Latency, p99Latency, maxLatency, cpuTime, ioTime, lastRun (default "totalTime")

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Use "pscale insights queries [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

JSON query records include the `fingerprint` and `keyspace` needed by `queries samples`, plus normalized SQL, statement type, tables, index usage, query/error counts, latency metrics, rows read/returned/affected, CPU/I/O duration, and last-run time.

## `pscale insights queries samples`

```text
List individual query executions for a fingerprint from
'pscale insights queries <database> <branch>'.

--keyspace is required (use the keyspace column from the queries list).
Useful for seeing who ran the query, when, duration, and any error message.

Usage:
  pscale insights queries samples <database> <branch> <fingerprint> [flags]

Examples:
  pscale insights queries samples mydb main b129e8fa --org myorg --keyspace mydb
  pscale insights queries samples mydb main b129e8fa --org myorg --keyspace mydb --period 1h --limit 25

Flags:
  -h, --help              help for samples
      --keyspace string   Keyspace for the fingerprint (required; from insights queries) (required)
      --limit int         Number of samples to return (default 25)
      --period string     Time period to look back (e.g. 1h, 1d)

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## `pscale insights errors`

```text
List aggregated query errors for a branch.

Pass a value from the fingerprint column to 'pscale insights errors show' to
see the individual queries behind an error.

Usage:
  pscale insights errors <database> <branch> [flags]
  pscale insights errors [command]

Available Commands:
  show        Show the queries behind an error fingerprint

Flags:
  -h, --help            help for errors
      --limit int       Number of errors to return (default 15)
      --period string   Time period to aggregate over (e.g. 1h, 1d)

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Use "pscale insights errors [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## `pscale insights errors show`

```text
Show the individual query executions that failed with an error fingerprint.

Use the fingerprint column from 'pscale insights errors <database> <branch>'
(error_fingerprint in JSON), not the truncated id.

Useful for seeing which users, keyspaces, and statements produced the error.

Usage:
  pscale insights errors show <database> <branch> <fingerprint> [flags]

Examples:
  pscale insights errors show mydb main b129e8fa --org myorg
  pscale insights errors show mydb main b129e8fa --org myorg --period 1h --limit 50

Flags:
  -h, --help            help for show
      --limit int       Number of queries to return (default 25)
      --period string   Time period to look back (e.g. 1h, 1d)

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## `pscale insights anomalies`

```text
List detected resource anomalies (CPU, memory, IOPS, rows read/written)

Usage:
  pscale insights anomalies <database> <branch> [flags]
  pscale insights anomalies [command]

Available Commands:
  show        Show an anomaly and its correlated queries

Flags:
  -h, --help   help for anomalies

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Use "pscale insights anomalies [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## `pscale insights anomalies show`

```text
Show a single anomaly from 'pscale insights anomalies <database> <branch>',
along with the queries whose activity correlates with it.

Usage:
  pscale insights anomalies show <database> <branch> <anomaly-id> [flags]

Examples:
  pscale insights anomalies show mydb main anomaly-id --org myorg

Flags:
  -h, --help   help for show

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## `pscale insights tags`

```text
List query tag keys observed on a branch.

Tag names match the Key picker in the PlanetScale Insights UI (e.g. app,
username, controller). Use those names with "tags summaries --tags".

Typical agent flow:
  1. pscale insights tags <database> <branch> --format json
  2. pscale insights tags summaries <database> <branch> --tags <name> --format json

Usage:
  pscale insights tags <database> <branch> [flags]
  pscale insights tags [command]

Examples:
  pscale insights tags mydb main --org myorg
  pscale insights tags mydb main --org myorg --period 1h

Available Commands:
  show        Show a query tag key and its values
  summaries   List query statistics grouped by tag keys

Flags:
      --fingerprint string   Only tags seen on this query fingerprint
  -h, --help                 help for tags
      --keyspace string      Filter tags to a keyspace
      --limit int            Number of top values to show in human output (default 3)
      --period string        Time period to look back (e.g. 1h, 1d)

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Use "pscale insights tags [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## `pscale insights tags show`

```text
Show one tag key and the values observed for it.

<tag> is the friendly name from 'pscale insights tags' (e.g. app, username),
matching the Insights UI Key picker. Source-qualified names (sql:app,
system:username) are accepted when a name exists in both sources.

Usage:
  pscale insights tags show <database> <branch> <tag> [flags]

Examples:
  pscale insights tags show mydb main app --org myorg
  pscale insights tags show mydb main username --org myorg --period 1h

Flags:
  -h, --help              help for show
      --keyspace string   Filter tag values to a keyspace
      --period string     Time period to look back (e.g. 1h, 1d)

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## `pscale insights tags summaries`

```text
Group query statistics by one or more tag keys.

--tags takes friendly names from 'pscale insights tags' / the Insights UI Key
picker (e.g. app, username, controller) — not the internal S/B ids.

If a name exists as both sql and system, disambiguate with sql:name or
system:name.

Usage:
  pscale insights tags summaries <database> <branch> [flags]

Examples:
  # List keys first, then summarize (matches the app Tags page)
  pscale insights tags mydb main --org myorg
  pscale insights tags summaries mydb main --org myorg --tags username

  # Group by multiple keys
  pscale insights tags summaries mydb main --org myorg --tags app --tags controller --sort totalTime

Flags:
      --dir string         Sort direction: asc or desc (default "desc")
  -h, --help               help for summaries
      --limit int          Number of summary rows to return (default 25)
      --period string      Time period to aggregate over (e.g. 1h, 1d)
      --sort string        Metric to rank by, one of: dimensions, totalTime, count, errorCount, rowsRead, rowsReturned, rowsAffected, rowsReadPerReturned, p50Latency, p99Latency, maxLatency, cpuTime, ioTime, lastRun (default "totalTime")
      --tags stringArray   Tag key name from 'pscale insights tags' (repeatable; e.g. --tags username --tags app) (required)

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## `pscale insights recommendations`

```text
List PlanetScale's schema recommendations for a database: unused tables and
indexes, duplicate indexes, bloated tables and indexes, missing indexes
derived from production query patterns, and sequence overflow risks. Each
recommendation includes ready-to-apply DDL (shown with --format json).

Use "pscale insights recommendations dismiss" to dismiss a recommendation.

Usage:
  pscale insights recommendations <database> [flags]
  pscale insights recommendations [command]

Aliases:
  recommendations, recommendation

Available Commands:
  dismiss     Dismiss a schema recommendation

Flags:
  -h, --help   help for recommendations

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Use "pscale insights recommendations [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## `pscale insights recommendations dismiss`

```text
Dismiss a schema recommendation so it no longer appears as open.

<number> is the recommendation sequence number from
'pscale insights recommendations <database>'.

Usage:
  pscale insights recommendations dismiss <database> <number> [flags]

Flags:
      --force           Dismiss without confirmation
  -h, --help            help for dismiss
      --reason string   Optional reason for dismissing the recommendation

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## Scope and failure interpretation

- `queries`, `queries samples`, `errors`, `anomalies`, and `tags` require `<database> <branch>`.
- `recommendations` and `recommendations dismiss` are database-scoped.
- A branch-scoped not-found response can mean the branch is absent or Query Insights is disabled for the database.
- These commands analyze server-side production-traffic data. Use `pscale inspect` for point-in-time engine statistics and live connection-level checks.
- Treat recommendation DDL and recommendation dismissal as separate writes requiring explicit approval.

## pscale insights parent and query/recommendation updates

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Surface PlanetScale's server-side analysis of a database: aggregated query
statistics (latency percentiles, rows read, errors), detected anomalies, and
schema recommendations, all computed from production traffic.

For live, connection-level diagnostics (table sizes, locks, running queries),
see pscale inspect.

Usage:
  pscale insights [command]

Available Commands:
  anomalies       List detected resource anomalies (CPU, memory, IOPS, rows read/written)
  errors          List queries that are failing with errors
  queries         List the top queries by a performance metric
  recommendations List schema recommendations (unused/duplicate indexes, bloat, missing indexes)
  tags            List query tag keys (sqlcommenter / system)

Flags:
  -h, --help         help for insights
      --org string   The organization for the current user

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Use "pscale insights [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale insights queries

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
List the top queries by a performance metric

Usage:
  pscale insights queries <database> <branch> [flags]
  pscale insights queries [command]

Examples:
  # Queries taking the most cumulative time
  pscale insights queries mydb main --org myorg

  # Most expensive read patterns (rows read vs returned)
  pscale insights queries mydb main --org myorg --sort rowsReadPerReturned

  # Highest p99 latency over the last hour
  pscale insights queries mydb main --org myorg --sort p99Latency --period 1h

  # Recent executions for a fingerprint from the list (keyspace is required)
  pscale insights queries samples mydb main b129e8fa --org myorg --keyspace mydb

Available Commands:
  samples         List recent executions for a query fingerprint
  show            Show an individual query execution
  summary         Show aggregate statistics for a query fingerprint
  traffic-budgets List traffic budgets affecting a query fingerprint

Flags:
      --dir string      Sort direction: asc or desc (default "desc")
  -h, --help            help for queries
      --limit int       Number of queries to return (default 15)
      --period string   Time period to aggregate over (e.g. 1h, 1d)
      --sort string     Metric to rank queries by, one of: totalTime, count, errorCount, rowsRead, rowsReturned, rowsAffected, rowsReadPerReturned, p50Latency, p99Latency, maxLatency, cpuTime, ioTime, lastRun (default "totalTime")

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Use "pscale insights queries [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```
## pscale insights queries show

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Show one query execution using an ID returned by
'pscale insights queries samples'. The query ID is an execution/sample ID,
not the fingerprint used by the samples and summary commands.

Usage:
  pscale insights queries show <database> <branch> <query-id> [flags]

Examples:
  pscale insights queries show mydb main exec-1 --org myorg

Flags:
  -h, --help   help for show

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale insights queries summary

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Show aggregate statistics for a fingerprint from
'pscale insights queries <database> <branch>'.

--keyspace is required (use the keyspace column from the queries list).
The fingerprint identifies a query pattern; it is not an execution/sample ID.

Usage:
  pscale insights queries summary <database> <branch> <fingerprint> [flags]

Examples:
  pscale insights queries summary mydb main b129e8fa --org myorg --keyspace mydb
  pscale insights queries summary mydb main b129e8fa --org myorg --keyspace mydb --period 1h
  pscale insights queries summary mydb main b129e8fa --org myorg --keyspace mydb --from 2026-08-25T14:00:00Z --to 2026-08-25T15:00:00Z

Flags:
      --from string       Start of a custom time range as an ISO 8601 timestamp
  -h, --help              help for summary
      --keyspace string   Keyspace for the fingerprint (required; from insights queries) (required)
      --period string     Named time period to summarize (for example 1h, 12h, or 1d)
      --to string         End of a custom time range as an ISO 8601 timestamp

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale insights queries traffic-budgets

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
List traffic budgets affecting a query fingerprint

Usage:
  pscale insights queries traffic-budgets <database> <branch> <fingerprint> [flags]

Flags:
  -h, --help              help for traffic-budgets
      --keyspace string   Keyspace for the fingerprint
      --page int          Page number to fetch
      --per-page int      Number of results per page (default 25)

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```
## pscale insights recommendations

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
List PlanetScale's schema recommendations for a database: unused tables and
indexes, duplicate indexes, bloated tables and indexes, missing indexes
derived from production query patterns, and sequence overflow risks. Each
recommendation includes ready-to-apply DDL (shown with --format json).

Use "pscale insights recommendations show" to print a recommendation and its
full DDL. Use "pscale insights recommendations dismiss" to dismiss one.

Usage:
  pscale insights recommendations <database> [flags]
  pscale insights recommendations [command]

Aliases:
  recommendations, recommendation

Available Commands:
  dismiss     Dismiss a schema recommendation
  show        Show a schema recommendation and its DDL

Flags:
  -h, --help   help for recommendations

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Use "pscale insights recommendations [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale insights recommendations show

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Show a single schema recommendation, including the full ready-to-apply DDL.

<number> is the recommendation sequence number from
'pscale insights recommendations <database>', the same value used by
'pscale insights recommendations dismiss'.

Usage:
  pscale insights recommendations show <database> <number> [flags]

Examples:
  pscale insights recommendations show mydb 1 --org myorg
  pscale insights recommendations show mydb 1 --org myorg --format json

Flags:
  -h, --help   help for show

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --org string                The organization for the current user
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```
