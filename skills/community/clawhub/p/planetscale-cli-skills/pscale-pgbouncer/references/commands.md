# pscale pgbouncer command reference

> All help fences below are exact output from the official, checksum-verified PlanetScale CLI v0.324.0 macOS arm64 release binary after normalizing only trailing whitespace.

## pscale pgbouncer

```text
Manage dedicated PgBouncers for a PostgreSQL database branch.

Dedicated PgBouncers run separately from the database nodes and provide
connection pooling for primary or replica traffic. This is distinct from the
local PgBouncer on port 6432 and from pgbouncer.* parameters on
'pscale branch resize'.

This command is only available for PostgreSQL databases.

Usage:
  pscale pgbouncer [command]

Available Commands:
  create      Create a dedicated PgBouncer
  delete      Delete a dedicated PgBouncer
  list        List dedicated PgBouncers for a Postgres branch
  resize      Change a dedicated PgBouncer's size, replicas, target, or parameters
  show        Show a dedicated PgBouncer

Flags:
  -h, --help         help for pgbouncer
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

Use "pscale pgbouncer [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale pgbouncer list

```text
List dedicated PgBouncers for a Postgres branch

Usage:
  pscale pgbouncer list <database> <branch> [flags]

Aliases:
  list, ls

Flags:
  -h, --help   help for list

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

## pscale pgbouncer show

```text
Show a dedicated PgBouncer

Usage:
  pscale pgbouncer show <database> <branch> <name> [flags]

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

`list` has alias `ls`. Both accept root global flags, including `--org` and `--format human|json|csv`.

## pscale pgbouncer create

```text
Create a dedicated PgBouncer for a PostgreSQL database branch.

Target must be one of: primary, replica, replica_az_affinity.
Size is a PgBouncer SKU name (for example PGB_10). If omitted, the API picks
a default size. Name is optional and auto-generated when omitted (max 12
characters; "primary" and "replica" are reserved).

Usage:
  pscale pgbouncer create <database> <branch> [flags]

Flags:
  -h, --help                    help for create
      --name string             Name for the PgBouncer (optional; auto-generated if omitted)
      --replicas-per-cell int   Number of replica servers per cell (default 1)
      --size string             PgBouncer size SKU (e.g. PGB_10)
      --target string           Traffic target: primary, replica, or replica_az_affinity (required) (required)

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

The doubled `(required)` in the `--target` description is verbatim upstream output.

## pscale pgbouncer resize

```text
Change a dedicated PgBouncer's size, replicas-per-cell, traffic target, and/or
pgbouncer configuration parameters. Changes are queued as an asynchronous
resize request. Use "pscale pgbouncer resize status" to track it and
"pscale pgbouncer resize cancel" to cancel it while unfinished.

This is distinct from "pscale branch resize" pgbouncer.* parameters, which
configure the local PgBouncer on database nodes.

Usage:
  pscale pgbouncer resize <database> <branch> <name> [flags]
  pscale pgbouncer resize [command]

Examples:
  pscale pgbouncer resize mydb main read-pool --size PGB_10
  pscale pgbouncer resize mydb main read-pool --replicas-per-cell 2 --wait
  pscale pgbouncer resize mydb main read-pool --parameters pgbouncer.default_pool_size=100

Available Commands:
  cancel      Cancel unfinished resize requests for a dedicated PgBouncer
  status      Show the latest resize request for a dedicated PgBouncer

Flags:
  -h, --help                     help for resize
      --parameters stringArray   Set a PgBouncer parameter as namespace.name=value (e.g. pgbouncer.default_pool_size=100). Repeatable.
      --replicas-per-cell int    Number of PgBouncer replica servers per cell (default 1)
      --size string              PgBouncer size SKU (e.g. PGB_10)
      --target string            Traffic target: primary, replica, or replica_az_affinity
      --wait                     Wait for the resize request to complete before returning
      --wait-timeout duration    Maximum time to wait for the resize request to complete with --wait (default 10m0s)

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

Use "pscale pgbouncer resize [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale pgbouncer resize status

```text
Show the latest resize request for a dedicated PgBouncer

Usage:
  pscale pgbouncer resize status <database> <branch> <name> [flags]

Flags:
  -h, --help   help for status

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

## pscale pgbouncer resize cancel

```text
Cancel unfinished resize requests for a dedicated PgBouncer

Usage:
  pscale pgbouncer resize cancel <database> <branch> <name> [flags]

Flags:
  -h, --help   help for cancel

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

## pscale pgbouncer delete

```text
Delete a dedicated PgBouncer

Usage:
  pscale pgbouncer delete <database> <branch> <name> [flags]

Aliases:
  delete, rm

Flags:
      --force   Delete a PgBouncer without confirmation
  -h, --help    help for delete

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

All subcommands accept root global flags: `--api-token`, `--api-url`, `--config`, `--debug`, `--format`, `--no-color`, `--org`, `--service-token`, and `--service-token-id`.
