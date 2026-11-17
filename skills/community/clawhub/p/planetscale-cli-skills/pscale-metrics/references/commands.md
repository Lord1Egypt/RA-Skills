# `pscale metrics` command reference

Unless a section says otherwise, help fences below are exact output from the official, checksum-verified PlanetScale CLI v0.324.0 macOS arm64 release binary after normalizing only trailing whitespace.

## `pscale metrics`

```text
Query PlanetScale's metrics service for a database branch.

Human output summarizes historical series and formats current values for quick
inspection. JSON preserves the API response, while CSV emits one row per sample
or current value for use in scripts and analysis tools.

Usage:
  pscale metrics [command]

Available Commands:
  instant     Show current metric values
  report      Produce a grouped performance metrics report
  show        Show historical metric series

Flags:
  -h, --help         help for metrics
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

Use "pscale metrics [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## `pscale metrics show`

```text
Show historical metric series

Usage:
  pscale metrics show <database> <branch> [flags]

Examples:
  # Summarize query volume and p99 latency over the last hour
  pscale metrics show mydb main --org myorg --metric queries --metric latency_p99 --period 1h

  # Export every sample as CSV
  pscale metrics show mydb main --org myorg --metric queries --period 1h --format csv

  # Preserve the complete metrics API response
  pscale metrics show mydb main --org myorg --metric queries --period 1h --format json

Flags:
      --budget-id string     Filter by traffic budget ID
      --container string     Filter by container
      --fingerprint string   Filter by query fingerprint
      --from string          Start of a custom time range as an ISO 8601 timestamp
  -h, --help                 help for show
      --keyspace string      Filter by keyspace
      --metric strings       Metric to query (repeat or comma-separate) (required)
      --period string        Named time period to query (for example 1h, 12h, or 1d; defaults to 12h)
      --pod string           Filter by one pod
      --pods strings         Filter by pods (repeat or comma-separate)
      --query-id strings     Filter by query pattern ID (repeat or comma-separate)
      --role string          Filter by Postgres role
      --rule-id string       Filter by traffic rule ID
  -q, --search string        Filter by search terms
      --shard string         Filter by shard
      --steps int            Requested number of data points
      --tablet-type string   Filter by tablet type
      --to string            End of a custom time range as an ISO 8601 timestamp

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

## `pscale metrics instant`

```text
Show current metric values

Usage:
  pscale metrics instant <database> <branch> [flags]

Examples:
  # Show current disk utilization for every Postgres pod
  pscale metrics instant mydb main --org myorg --metric planetscale_volume_usage_percentage

  # Preserve the complete instant metrics API response
  pscale metrics instant mydb main --org myorg --metric planetscale_volume_usage_percentage --format json

Flags:
      --container string   Filter by container
  -h, --help               help for instant
      --metric strings     Metric to query (repeat or comma-separate) (required)
      --pod string         Filter by pod
      --role string        Filter by Postgres role
      --shard string       Filter by shard

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

## `pscale metrics report`

The help fence below is exact output from the official, checksum-verified PlanetScale CLI v0.334.0 macOS arm64 release binary after normalizing only trailing whitespace. The archive SHA-256 is `16b156fa969edb36ec6ebde28b40165cbeb928ae07ba97110d3359fb588245bd`.

```text
Produce a curated performance report for a database branch.

The database engine is detected automatically. MySQL, PostgreSQL, and Neki
reports use different metric sections, including current-value sections where
applicable. Section headings are bold in human output and plain text with
--no-color.

Usage:
  pscale metrics report <database> <branch> [flags]

Examples:
  # Daily human-readable performance report
  pscale metrics report mydb main --org myorg --period 1d

  # Weekly report without terminal styling
  pscale metrics report mydb main --org myorg --period 7d --no-color

  # Composite JSON report for automation
  pscale metrics report mydb main --org myorg --period 1d --format json

Flags:
      --from string     Start of a custom time range as an ISO 8601 timestamp
  -h, --help            help for report
      --period string   Named report period (15m, 1h, 3h, 6h, 12h, 1d, 2d, 7d, or 8d) (default "1d")
      --steps int       Requested number of historical data points
      --to string       End of a custom time range as an ISO 8601 timestamp

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

## Scope and output behavior

- Pass `--org` explicitly to avoid relying on the configured default organization; each selected subcommand also takes `<database> <branch>`.
- `show` and `instant` require one or more `--metric` values.
- `--from` and `--to` must be used together and cannot be combined with `--period`; `--steps`, when set, must be greater than zero.
- Human `show` output summarizes each returned series; CSV emits every timestamped sample; JSON preserves the complete metrics API response.
- `report` selects curated sections by database engine. PostgreSQL and Neki include both historical and selected current-value sections; unsupported engines fail rather than returning a partial report.

## pscale metrics parent with specialized commands

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Query PlanetScale's metrics service for a database branch.

Human output summarizes historical series and formats current values for quick
inspection. JSON preserves the API response, while CSV emits one row per sample
or current value for use in scripts and analysis tools.

Usage:
  pscale metrics [command]

Available Commands:
  instant         Show current metric values
  keyspace-tables Show table storage metrics by keyspace
  queries         Show metrics for SQL queries
  report          Produce a grouped performance metrics report
  show            Show historical metric series
  tables          Show table storage metrics
  tablets         Show tablet metric series
  tags            Show metrics grouped by query tags

Flags:
  -h, --help         help for metrics
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

Use "pscale metrics [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale metrics queries

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Show metrics for SQL queries

Usage:
  pscale metrics queries <database> <branch> [flags]

Flags:
      --budget-id string     Filter by traffic budget ID
      --fingerprint string   Filter by query fingerprint
      --from string          Start of a custom time range as an ISO 8601 timestamp
  -h, --help                 help for queries
      --keyspace string      Keyspace for the query fingerprint
      --metric strings       Metric to query (repeat or comma-separate) (required)
      --period string        Named time period to query (for example 1h, 12h, or 1d; defaults to 12h)
      --query-id strings     Filter by query pattern ID (repeat or comma-separate)
      --rule-id string       Filter by traffic rule ID
  -q, --search string        Filter by search terms
      --steps int            Requested number of data points
      --tablet-type string   Filter by tablet type
      --to string            End of a custom time range as an ISO 8601 timestamp

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

## pscale metrics tables

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Show table storage metrics

Usage:
  pscale metrics tables <database> <branch> [flags]

Flags:
  -h, --help   help for tables

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

## pscale metrics tablets

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Show tablet metric series

Usage:
  pscale metrics tablets <database> <branch> [flags]
  pscale metrics tablets [command]

Available Commands:
  instant     Show current tablet metric values

Flags:
      --from string       Start of a custom time range as an ISO 8601 timestamp
  -h, --help              help for tablets
      --keyspace string   Filter by keyspace
      --metric strings    Metric to query (repeat or comma-separate) (required)
      --period string     Named time period to query (for example 1h, 12h, or 1d; defaults to 12h)
      --pod string        Filter by pod
      --shard string      Filter by shard
      --steps int         Requested number of data points
      --to string         End of a custom time range as an ISO 8601 timestamp
      --workflow string   Filter by VReplication workflow

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

Use "pscale metrics tablets [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale metrics tags

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Show metrics grouped by query tags

Usage:
  pscale metrics tags <database> <branch> [flags]

Flags:
      --budget-id string      Filter by traffic budget ID
      --from string           Start of a custom time range as an ISO 8601 timestamp
  -h, --help                  help for tags
      --metric strings        Metric to query (repeat or comma-separate) (required)
      --period string         Named time period to query (for example 1h, 12h, or 1d; defaults to 12h)
      --rule-id string        Filter by traffic rule ID
  -q, --search string         Filter by search terms
      --steps int             Requested number of data points
      --tablet-type string    Filter by tablet type
      --tag-set stringArray   Tag set as key=value pairs. Repeat for independent series; comma-separate keys in one set (for example Busername=alice,Senv=production)
      --to string             End of a custom time range as an ISO 8601 timestamp

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
