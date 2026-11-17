The following complete help sections were captured from the official, checksum-verified PlanetScale CLI v0.349.0 macOS arm64 binary: `branch`, `branch maintenance`, `branch maintenance run`, `branch connections`, `branch connections top`, `branch connections kill`, `branch connections kill-transaction`, `branch vtctl`, `branch promote`, and `branch demote`. Each has its own adjacent capture note. The environment was an empty credential-free HOME/XDG/config working directory with `NO_COLOR=1` and `TERM=dumb`. Archive SHA-256: `1bdad82d821ab4eb65207672b38dfa063006460226715cb0937588ec671179a6`. Only terminal padding and trailing whitespace were normalized.

This scoped attribution does not relabel any other fence. Earlier notes below record superseded captures where indicated; unchanged, unlabelled fences retain the legacy default defined below.

Previous `pscale branch`, `branch connections`, and `branch connections top` help captures come from the official, checksum-verified PlanetScale CLI v0.348.0 macOS arm64 binary with `NO_COLOR=1`, an empty credential-free home, and only trailing-whitespace normalization. Archive SHA-256: `528bb8951d4d93f7ca869850787163f5d49ba405acc58d4146b9b3427e83b7e7`. The `branch extensions`, `branch extensions list`, `branch parameters`, and `branch vtgate` captures retain their v0.344.0 provenance (archive SHA-256 `1b59b271590d9b49dd52aafbb0e5c0cd788b44c00a5627d6487cd0d18815cf53`), with the same color and whitespace settings. Complete toggle, parameter-list, and VTGate rollout help surfaces are in [branch-configuration-commands.md](branch-configuration-commands.md). Other sections retain their stated earlier provenance.

Unless noted otherwise, help fences below are exact output from the official, checksum-verified PlanetScale CLI v0.324.0 macOS arm64 release binary after normalizing only trailing whitespace. The `pscale branch create` surface was recaptured from the checksum-verified v0.325.0 binary. The explicit current-section list and adjacent capture notes above/below identify newer captures. The preceding historical-family paragraph identifies the v0.348.0 parent/connection captures and the retained v0.344.0 extension/parameter/VTGate captures; maintenance and other recaptured sections identify their own provenance.

## pscale branch

Historical v0.348.0 capture note (verbatim; superseded for the parent fence):

> Complete parent help has the v0.348.0 capture provenance identified in the introduction. The upstream parent still labels connections under “MySQL and Postgres”; the connections help and operational skill explicitly cover read-only Neki sessions.

Current commentary: the current parent still groups `connections` under MySQL and Postgres. The current connections help and source-backed action note below cover Neki; historical read-only restrictions are not current authorization rules.

Complete help captured from the official, checksum-verified PlanetScale CLI v0.349.0 macOS arm64 binary, in an empty credential-free HOME/XDG/config working environment with `NO_COLOR=1` and `TERM=dumb`. Archive SHA-256: `1bdad82d821ab4eb65207672b38dfa063006460226715cb0937588ec671179a6`. Only terminal padding and trailing whitespace were normalized.

```text
Create, delete, diff, and manage branches

Usage:
  pscale branch [command]

MySQL, Postgres, and Neki branch commands:
  create          Create a new branch from a database
  delete          Delete a branch from a database
  list            List all branches of a database
  schema          Show the schema of a branch
  show            Show a specific branch of a database
  switch          Switches the current project to use the specified branch
  update          Update a branch's name or deletion protection

MySQL and Postgres:
  connections     Show and kill branch connections
  demote          Demote a production branch to development
  promote         Promote a branch to production

Vitess/MySQL-specific:
  diff            Show the schema diff of a MySQL branch
  lint            Lint the schema of a MySQL branch
  query-patterns  List, show, delete, and download query pattern reports for a MySQL branch
  refresh-schema  Refresh the schema for a MySQL branch
  routing-rules   Fetch or update routing rules for a MySQL branch
  safe-migrations Enable or disable safe migrations on a MySQL branch
  vtctl           Run vtctl commands against a branch
  vtgate          Manage VTGate size and parameters for a Vitess branch

Postgres-specific:
  extensions      List extensions available on a Postgres branch
  parameters      List the configuration parameters of a Postgres branch
  resize          Change a Postgres branch's cluster size, replicas, or parameters
  switchover      Switch over the primary of a Postgres branch (Postgres only)

Postgres and Neki:
  maintenance     Manage maintenance for a Postgres or Neki branch

Neki-specific:
  admin           Manage the admin config for a Neki database branch
  changes         List change requests across a Neki branch
  config-profile  Manage configuration profiles for a Neki database branch
  data-topology   Fetch or update the data topology of a Neki branch
  router          Manage routers for a Neki database branch
  shard           Manage shards for a Neki database branch

Flags:
  -h, --help         help for branch
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

Use "pscale branch [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale logs

Help fence in this section is exact output from the official, checksum-verified PlanetScale CLI v0.332.0 macOS arm64 release binary with `NO_COLOR=1`, after normalizing only trailing whitespace. The archive SHA-256 is `61eadf71c9d5e6423587fbf01fd698800d8a944775a06519a1c2ac38fcb89287`.

```text
Query recent logs for a PostgreSQL or Neki branch.

The command obtains a signed logs URL from the PlanetScale API, builds a LogsQL
query, and prints parsed log entries. By default it returns up to 100 logs from
the primary server over the last hour, newest first.

Usage:
  pscale logs <database> <branch> [flags]

Examples:
  # Recent primary logs
  pscale logs <database> <branch> --org <org> --format json

  # Errors from a selected pod over the last six hours
  pscale logs <database> <branch> --org <org> --format json --period 6h --level ERROR --server <pod>

  # Logs from a custom ISO 8601 time range
  pscale logs <database> <branch> --org <org> --format json \
    --from 2026-08-20T16:00:00Z --to 2026-08-20T18:00:00Z

  # Search and filter with LogsQL syntax
  pscale logs <database> <branch> --org <org> --format json --query 'connection refused'

Flags:
      --from string      Start of a custom time range as an ISO 8601 timestamp
  -h, --help             help for logs
      --level strings    Log levels to include (comma-separated or repeatable): DEBUG, INFO, WARNING, ERROR
      --limit int        Maximum number of logs to return (default 100)
      --org string       The organization for the current user
      --page int         Page number to fetch (default 1)
      --period string    Time period to query: 15m, 1h, 3h, 6h, 12h, 1d, 7d, or 8d (default "1h")
      --query string     Text or LogsQL expression to search for
      --server strings   Servers to include (comma-separated or repeatable); primary selects the primary role, other values select pod names (default [primary])
      --shard strings    Neki shards to include (comma-separated or repeatable)
      --to string        End of a custom time range as an ISO 8601 timestamp

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch create

```text
Create a new branch from a database

Usage:
  pscale branch create <source-database> <branch> [options] [flags]

Aliases:
  create, b

Flags:
      --cluster-size string    Cluster size for the branch. Defaults to PS_DEV for regular branches, or PS-10 for branches created from a backup or with seed-data. Use 'pscale size cluster list' to see the valid sizes.
      --from string            Parent branch to create the new branch from. Cannot be used with --restore
  -h, --help                   help for create
      --major-version string   For PostgreSQL databases, the PostgreSQL major version to use for the branch. Defaults to the major version of the parent branch if it exists or the database's default branch major version. Ignored for branches restored from backups.
      --max-storage int        Maximum storage size in bytes for autoscaling
      --min-storage int        Minimum storage size in bytes
      --region string          Region for the branch to be created in.
      --restore string         ID of Backup to restore into branch.
      --restore-point string   For PostgreSQL databases, restore from a point-in-time recovery timestamp (e.g. 2023-01-01T00:00:00Z).
      --seed-data              Add seed data using the Data Branching™ feature. This branch will be created with the same resources as the base branch.
      --wait                   Wait until the branch is ready

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

## pscale branch update

```text
Update a branch's name or deletion protection.

Only the flags you pass are sent. At least one flag is required.

Usage:
  pscale branch update <database> <branch> [flags]

Examples:
  pscale branch update mydb main --new-name trunk
  pscale branch update mydb main --deletion-protected
  pscale branch update mydb main --deletion-protected=false

Flags:
      --deletion-protected   Protect the branch from deletion (use --deletion-protected=false to disable)
  -h, --help                 help for update
      --new-name string      Rename the branch

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

## pscale branch switchover

```text
Switch over the primary of a Postgres branch. Postgres only.

On a branch with replicas the primary steps down and a replica is promoted in
its place; use --candidate to pick the replica, otherwise one is selected
automatically. A branch running a single instance has nothing to promote, so
that instance is restarted in place and the branch is unreachable while it
comes back. Writes are briefly interrupted while the switch completes.

Usage:
  pscale branch switchover <database> <branch> [flags]

Flags:
      --candidate string   Name of the replica to promote, as returned by 'branch infra'. Omit to select automatically. Only applies to branches with replicas
  -h, --help               help for switchover

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

## pscale branch maintenance

Previous capture note (superseded for this fence): Help fences in this section and the next (`maintenance`, `maintenance run`) are exact output from the official, checksum-verified PlanetScale CLI v0.332.0 macOS arm64 release binary with `NO_COLOR=1`, after normalizing only trailing whitespace. The archive SHA-256 is `61eadf71c9d5e6423587fbf01fd698800d8a944775a06519a1c2ac38fcb89287`.

Complete help captured from the official, checksum-verified PlanetScale CLI v0.349.0 macOS arm64 binary, in an empty credential-free HOME/XDG/config working environment with `NO_COLOR=1` and `TERM=dumb`. Archive SHA-256: `1bdad82d821ab4eb65207672b38dfa063006460226715cb0937588ec671179a6`. Only terminal padding and trailing whitespace were normalized.

```text
Manage maintenance for a Postgres or Neki branch.

'pscale branch maintenance run' upgrades a branch to the latest image now.

PlanetScale schedules maintenance that restarts Postgres, such as security
fixes and image updates, in each Postgres branch's weekly maintenance window,
with at least 7 days' notice. Use 'pscale branch maintenance window' to see or
change the window, and 'pscale branch maintenance event' to see and reschedule
upcoming maintenance.

See https://planetscale.com/docs/postgres/operations-philosophy

Usage:
  pscale branch maintenance [command]

Available Commands:
  event       List, show, and reschedule maintenance events for a Postgres branch
  run         Run maintenance for a Postgres or Neki branch now
  window      Show and set the maintenance window of a Postgres branch

Flags:
  -h, --help   help for maintenance

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

Use "pscale branch maintenance [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch maintenance run


Complete help captured from the official, checksum-verified PlanetScale CLI v0.349.0 macOS arm64 binary, in an empty credential-free HOME/XDG/config working environment with `NO_COLOR=1` and `TERM=dumb`. Archive SHA-256: `1bdad82d821ab4eb65207672b38dfa063006460226715cb0937588ec671179a6`. Only terminal padding and trailing whitespace were normalized.

```text
Run maintenance for a Postgres or Neki branch, updating it to the latest
available image. Vitess (MySQL) databases are not supported.

This is how regular version bumps, bugfixes, and quality-of-life improvements
reach a branch right away. On Postgres, PlanetScale also schedules some updates
in the branch's maintenance window (see 'pscale branch maintenance event').

The upgrade is applied to the replicas first, followed by a switchover from the
old primary to an upgraded replica. That failover leads to a short period of
database unavailability (seconds), and all direct connections are terminated, so
your application should have retry logic. A branch running a single instance has
no replica to switch over to and is unavailable until it comes back.

Pass --update-postgres-minor-version to also upgrade the branch to the latest
PostgreSQL minor version during the run.

Maintenance cannot start while a change request (see 'branch resize') is still
in progress.

See https://planetscale.com/docs/postgres/operations-philosophy

Usage:
  pscale branch maintenance run <database> <branch> [flags]

Flags:
  -h, --help                            help for run
      --update-postgres-minor-version   Upgrade the branch to the latest PostgreSQL minor version during maintenance

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

## pscale branch extensions

```text
List extensions available on a Postgres branch's cluster image.

This is the catalog of extensions the image can load, not the result of
CREATE EXTENSION. Enable and disable queue an asynchronous branch change
request; only extensions marked "can enable" can be toggled. Toggling an
extension may restart the database.

Usage:
  pscale branch extensions <database> <branch> [flags]
  pscale branch extensions [command]

Available Commands:
  disable     Disable an extension on a Postgres branch
  enable      Enable an extension on a Postgres branch
  list        List extensions available on a Postgres branch

Flags:
  -h, --help   help for extensions

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

Use "pscale branch extensions [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

`pscale branch extensions <database> <branch>` accepts the same flags and is equivalent to `extensions list`. This is a read-only cluster-image catalog, not installed extension state.

## pscale branch extensions list

```text
List extensions available on a Postgres branch's cluster image.

This is the catalog of extensions the image can load, not the result of
CREATE EXTENSION. Enable and disable queue an asynchronous branch change
request; only extensions marked "can enable" can be toggled. Toggling an
extension may restart the database.

Usage:
  pscale branch extensions list <database> <branch> [flags]

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

Unless a command-specific help block repeats them inline, every `pscale branch`
subcommand accepts these global flags:

```text
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
```

## pscale branch list

```text
List all branches of a database

Usage:
  pscale branch list <database> [flags]

Aliases:
  list, ls

Flags:
  -h, --help           help for list
      --page int       Page number to fetch
      --per-page int   Number of results per page (default 100)
  -w, --web            List branches in your web browser.

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

## pscale branch parameters

```text
List the configuration parameters of a Postgres branch, including their
current and default values. Values from a queued change request are reflected.

To change parameters, use 'pscale branch resize <database> <branch> --parameters namespace.name=value'.

Usage:
  pscale branch parameters <database> <branch> [flags]
  pscale branch parameters [command]

Aliases:
  parameters, params

Available Commands:
  list        List the configuration parameters of a Postgres branch

Flags:
      --extension          Only show parameters that configure an extension (--extension=false hides them).
  -h, --help               help for parameters
      --internal           Only show internal parameters, which cannot be changed (--internal=false hides them).
      --namespace string   Only show parameters in this namespace (e.g. pgconf, pgbouncer, patroni).

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

Use "pscale branch parameters [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

`pscale branch parameters list <database> <branch>` accepts the same flags. The bare `parameters <database> <branch>` form is an alias for `parameters list`. Prefer `--format json` before a change so `restart`, current, and default values remain explicit. Use `--internal=false` to inventory changeable parameters; do not depend on the removed `immutable` or `extension` fields.

## pscale branch resize

```text
Change a Postgres branch's cluster size, replica count, and/or configuration
parameters. All requested changes are combined into a single change request
that is applied asynchronously. Use "pscale branch resize status" to track it
and "pscale branch resize cancel" to cancel it while queued.

Usage:
  pscale branch resize <database> <branch> [flags]
  pscale branch resize [command]

Examples:
  pscale branch resize mydb main --cluster-size PS_10_GCP_X86
  pscale branch resize mydb main --parameters pgconf.max_connections=200
  pscale branch resize mydb main --cluster-size PS_20_GCP_X86 --replicas 2 --parameters pgconf.max_connections=500 --wait

Available Commands:
  cancel      Cancel the queued change request for a Postgres branch
  status      Show the latest change request for a Postgres branch

Flags:
      --cluster-size string      New cluster size for the branch (a fully-qualified SKU name, e.g. PS_10_GCP_X86). Use 'pscale size cluster list --engine postgresql' to see the valid sizes.
  -h, --help                     help for resize
      --parameters stringArray   Set a configuration parameter as namespace.name=value (e.g. pgconf.max_connections=200). Repeatable. Use 'pscale branch parameters list' to see available parameters.
      --replicas int             Desired number of replicas for the branch.
      --wait                     Wait for the change request to complete before returning.
      --wait-timeout duration    Maximum time to wait for the change request to complete with --wait. (default 10m0s)

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

Use "pscale branch resize [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

At least one change flag is required. When the best-effort catalog fetch succeeds, parameter preflight rejects names absent from the `internal=false` catalog and checks restart impact; a failed fetch skips that local validation, so obtain a successful fresh catalog read before an approved write. Values marked `restart` restart the database when applied. Without `--wait`, poll `resize status`; `queued`, `pending`, and `resizing` are non-terminal, while `completed` and `canceled` are terminal.

## pscale branch resize status

```text
Show the latest change request for a Postgres branch

Usage:
  pscale branch resize status <database> <branch> [flags]

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

## pscale branch resize cancel

```text
Cancel the queued change request for a Postgres branch

Usage:
  pscale branch resize cancel <database> <branch> [flags]

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

Cancel is an operational write. Confirm the target and latest request state before running it, then re-run `resize status` to verify the result.

## pscale branch connections

Historical v0.348.0 capture note (verbatim; superseded for the parent/top/kill-transaction fences and the re-captured kill attribution):

> This complete parent fence and the complete `connections top` fence below were captured from the checksum-verified v0.348.0 binary identified above; only trailing whitespace was normalized. `connections show`, `kill`, and `kill-transaction` help was re-executed and is unchanged. Their action examples are not applicable to Neki.

Current commentary: the historical Neki exclusion above describes the earlier release only. Current Neki actions follow the matching client dispatch/tests documented below; `connections show` retains its unchanged earlier help capture.

Complete help captured from the official, checksum-verified PlanetScale CLI v0.349.0 macOS arm64 binary, in an empty credential-free HOME/XDG/config working environment with `NO_COLOR=1` and `TERM=dumb`. Archive SHA-256: `1bdad82d821ab4eb65207672b38dfa063006460226715cb0937588ec671179a6`. Only terminal padding and trailing whitespace were normalized.

```text
Show and kill MySQL, Postgres, or Neki branch connections.

MySQL (Vitess):
  show/kill/top with --keyspace and --shard.

Postgres:
  show/top with --instance or --role.
  kill-transaction terminates a transaction_id from show.

Neki:
  show/top list client sessions across the branch's routers.
  kill-transaction terminates a transaction_id from show.

Agent workflow:
  1. Run: pscale branch connections show <database> <branch> --format json
  2. Inspect query_id, transaction_id, and connection_id from the selected row.
  3. Explain the proposed action and wait for user approval before running it.
  4. Run exactly one action command with the matching ID.
  5. Run show again to verify the result.

Action semantics:
  kill <database> <branch> <query-id> --query        Cancels the listed query_id.
  kill-transaction <database> <branch> <transaction-id>
                                                     Postgres and Neki only. destructive. Terminates the listed transaction_id if it still matches server state.
  kill <database> <branch> <connection-id>           destructive. Terminates the listed connection_id.

Use --format json when an agent or script needs to inspect query_id,
transaction_id, and connection_id fields. Human output uses vertical records so
query text and action IDs are not truncated.

Usage:
  pscale branch connections [command]

Available Commands:
  kill             Kill a branch connection or query
  kill-transaction Kill a Postgres or Neki branch transaction
  show             Show branch connections once
  top              Show live branch connection activity

Flags:
  -h, --help   help for connections

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

Use "pscale branch connections [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch connections show

```text
Show branch connections once.

Use --format json when an agent or script needs to inspect query_id,
transaction_id, and connection_id fields. Human output uses vertical records so
query text and action IDs are not truncated.

Usage:
  pscale branch connections show <database> <branch> [flags]

Flags:
  -h, --help              help for show
      --instance string   Postgres instance to target
      --keyspace string   Vitess keyspace to target
      --role string       Postgres instance role to target: primary or replica
      --shard string      Vitess shard to target

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

## pscale branch connections top

Previous capture note (superseded for this fence): Complete v0.348.0 binary capture; same archive checksum and normalization as the connections parent above.

Complete help captured from the official, checksum-verified PlanetScale CLI v0.349.0 macOS arm64 binary, in an empty credential-free HOME/XDG/config working environment with `NO_COLOR=1` and `TERM=dumb`. Archive SHA-256: `1bdad82d821ab4eb65207672b38dfa063006460226715cb0937588ec671179a6`. Only terminal padding and trailing whitespace were normalized.

```text
Show live branch connection activity.

Run interactively in a terminal to launch the TUI. Pipe or redirect output to
run headlessly with --capture; --duration bounds either mode and without
--duration the command runs until interrupted. Pass --replay FILE to render a
previously captured trace in the TUI — actions are rejected in replay mode.

For Postgres, connections top shows session activity across instances. For
Vitess, pass --keyspace and --shard or run interactively to select them when
the server reports available targets. For Neki, connections top shows client
sessions across the branch's routers.

Usage:
  pscale branch connections top [database] [branch] [flags]

Flags:
      --capture string      Write captured samples to a trace file. Required in headless mode.
      --duration duration   Run for this duration. Default is to run until interrupted.
  -h, --help                help for top
      --instance string     Filter the live view to a single instance (by id from the list response).
      --interval duration   Refresh interval. (default 1s)
      --keyspace string     Vitess keyspace to target.
      --replay string       Replay a previously captured trace file in the TUI. Mutually exclusive with --capture.
      --role string         Filter the live view to rows whose instance role is primary or replica.
      --shard string        Vitess shard to target.

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

## pscale branch connections kill

The Neki sub-list in parent help names `show/top` and `kill-transaction`, but is not an exhaustive action-support matrix. In the immutable [client command dispatch](https://github.com/planetscale/cli/blob/05bded8a8fdbcda5b4ee47dd015460a20bb8a238/internal/cmd/branch/connections_commands.go#L57-L101), `kill` resolves the engine, validates engine-specific flags, then dispatches query cancellation or connection termination for that engine. The matching [`TestConnectionsSendsNekiActions` fixture](https://github.com/planetscale/cli/blob/05bded8a8fdbcda5b4ee47dd015460a20bb8a238/internal/cmd/branch/connections_test.go#L546-L573) covers Neki query, connection, and transaction actions. This establishes CLI request support, not live server entitlement or guaranteed success. Use fresh server-issued action IDs, exact-target approval, and read-back; stop on feature/permission failures rather than substituting IDs or retrying automatically.

Complete help captured from the official, checksum-verified PlanetScale CLI v0.349.0 macOS arm64 binary, in an empty credential-free HOME/XDG/config working environment with `NO_COLOR=1` and `TERM=dumb`. Archive SHA-256: `1bdad82d821ab4eb65207672b38dfa063006460226715cb0937588ec671179a6`. Only terminal padding and trailing whitespace were normalized.

```text
Kill a branch connection or query.

This is destructive. Pass a connection_id from connections show to terminate a
connection, or pass --query with a query_id from connections show to cancel only
the current query.

Usage:
  pscale branch connections kill <database> <branch> <id> [flags]

Flags:
  -h, --help              help for kill
      --keyspace string   Vitess keyspace to target
      --query             Cancel the query_id instead of terminating the connection_id
      --shard string      Vitess shard to target

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

## pscale branch connections kill-transaction


Complete help captured from the official, checksum-verified PlanetScale CLI v0.349.0 macOS arm64 binary, in an empty credential-free HOME/XDG/config working environment with `NO_COLOR=1` and `TERM=dumb`. Archive SHA-256: `1bdad82d821ab4eb65207672b38dfa063006460226715cb0937588ec671179a6`. Only terminal padding and trailing whitespace were normalized.

```text
Kill a Postgres or Neki branch transaction.

This is destructive. Pass a transaction_id from connections show to terminate
the matching connection.

Usage:
  pscale branch connections kill-transaction <database> <branch> <transaction-id> [flags]

Flags:
  -h, --help   help for kill-transaction

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

## pscale branch infra

```text
Show infrastructure (pods) for a branch

Usage:
  pscale branch infra <database> <branch> [flags]

Flags:
  -h, --help   help for infra

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

## pscale branch query-patterns

```text
List, show, delete, and download query pattern reports for a branch

Usage:
  pscale branch query-patterns [command]

Available Commands:
  delete      Delete a query pattern report
  download    Download a CSV report of the query patterns for a branch
  list        List query pattern reports for a branch
  show        Show a query pattern report

Flags:
  -h, --help   help for query-patterns

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

Use "pscale branch query-patterns [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch query-patterns list

```text
List query pattern reports for a branch

Usage:
  pscale branch query-patterns list <database> <branch> [flags]

Aliases:
  list, ls

Flags:
  -h, --help                    help for list
      --limit int               Number of results to return (max 100) (default 25)
      --starting-after string   Cursor to fetch the next page of reports

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

## pscale branch query-patterns show

```text
Show a query pattern report

Usage:
  pscale branch query-patterns show <database> <branch> <report-id> [flags]

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

## pscale branch query-patterns delete

```text
Delete a query pattern report

Usage:
  pscale branch query-patterns delete <database> <branch> <report-id> [flags]

Aliases:
  delete, rm

Flags:
      --force   Delete the report without confirmation
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

## pscale branch query-patterns download

```text
Download a CSV report of the query patterns for a branch

Usage:
  pscale branch query-patterns download <database> <branch> [flags]

Flags:
  -h, --help            help for download
      --output string   Output file name, or - to write to stdout. Defaults to query-patterns-<organization>-<database>-<branch>-<timestamp>.csv.

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

## pscale branch refresh-schema

Complete help capture from the official, checksum-verified PlanetScale CLI v0.345.0 macOS arm64 binary, executed with `env -i`, an empty credential-free `HOME`, minimal `PATH`, and `NO_COLOR=1`. Only trailing whitespace was normalized. Archive SHA-256: `d774eb31cd764dee4c01a1671f3ea17e1d3cb9b8aefe829e82cce2c3358fe028`.

```text
Refresh the schema for a MySQL branch. Waits until the updated schema snapshot is ready so later commands, such as routing-rules, see it.

Usage:
  pscale branch refresh-schema <database> <branch> [flags]

Flags:
  -h, --help   help for refresh-schema

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

## pscale branch routing-rules

This parent and its `update` help fence are exact output from the official, checksum-verified PlanetScale CLI v0.339.0 macOS arm64 release binary after normalizing only trailing whitespace. The archive SHA-256 is `1e396701709cd49d1d1cccca252e2bd81f224b2830ca189a84a16983bde182e8`. The `get` fence was subsequently recaptured at v0.350.0 and has its own adjacent attribution below.

```text
Fetch or update routing rules for a MySQL branch

Usage:
  pscale branch routing-rules [command]

Available Commands:
  get         Show the routing rules of a MySQL branch
  update      Replace the routing rules of a MySQL branch

Flags:
  -h, --help   help for routing-rules

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

Use "pscale branch routing-rules [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch routing-rules get

Compatibility: `routing-rules show` aliases `routing-rules get` starting with PlanetScale CLI v0.350.0. Both inspect the same MySQL schema snapshot and preserve its warnings; neither is the live `vtctl get-routing-rules` reader or the full-replacement `routing-rules update` write. Unknown non-runnable subcommands point to the owning parent's help (for example, `pscale branch routing-rules --help`) in human errors and JSON `UNKNOWN_COMMAND` next steps. Suggestions are discovery aids, not write authorization.

This complete fence has been recaptured from the official, checksum-verified v0.350.0 macOS arm64 binary (archive SHA-256 `aa17d5be045b30665d8ffaaf42159254fe3259186763c47304260af4f6aa56df`), normalizing only terminal padding/trailing whitespace. It replaces the earlier section-level v0.339.0 attribution for `get`; that attribution now covers only the parent and `update` fences. The `show` alias was separately captured and matches canonical `get`; the routing-rules and branch parent help were also captured and match their stored fences. Other fences retain their original provenance.

```text
Show the routing rules of a MySQL branch

Usage:
  pscale branch routing-rules get <database> <branch> [flags]

Aliases:
  get, show

Flags:
  -h, --help   help for get

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

## pscale branch routing-rules update

```text
Replace the branch routing rules. This is a full replacement, not a merge. The request fails while a vtctld schema mutation is in progress or the branch schema snapshot is not ready, because the rules you read may not describe live routing.

Usage:
  pscale branch routing-rules update <database> <branch> --routing-rules <file> [flags]

Flags:
  -h, --help                   help for update
      --routing-rules string   The routing to set

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

## pscale branch vtgate

```text
Manage VTGate size and parameters for a Vitess branch

Usage:
  pscale branch vtgate [command]

Available Commands:
  changes     Manage VTGate parameter changes for a Vitess branch
  parameters  List the VTGate parameters of a Vitess branch
  resize      Resize VTGates for a Vitess production branch
  show        Show the current VTGate configuration for a Vitess branch
  update      Change the VTGate parameters of a Vitess branch

Flags:
  -h, --help   help for vtgate

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

Use "pscale branch vtgate [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch vtgate show

```text
Show the current VTGate configuration for a Vitess branch

Usage:
  pscale branch vtgate show <database> <branch> [flags]

Examples:
  pscale branch vtgate show mydb main
  pscale branch vtgate show mydb main --format json

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

Use `--format json` to preserve `vtgate_size`, per-availability-zone `vtgate_count`, `vtgate_autoscaling`, `vtgate_max_count`, and `vtgate_target_cpu_utilization` for agent review.

## pscale branch vtgate resize

```text
Resize the VTGate SKU, count, and/or autoscaling for a Vitess production branch.

Development branches cannot be resized. Use "pscale branch vtgate resize status"
to track a resize and "pscale branch vtgate resize cancel" to cancel one while
queued.

Usage:
  pscale branch vtgate resize <database> <branch> [flags]
  pscale branch vtgate resize [command]

Examples:
  pscale branch vtgate resize mydb main --vtgate-size VTG_320
  pscale branch vtgate resize mydb main --vtgate-size VTG_1280 --vtgate-count 2
  pscale branch vtgate resize mydb main --vtgate-size VTG_320 --vtgate-autoscaling --vtgate-count 2 --vtgate-max-count 8 --vtgate-target-cpu-utilization 50

Available Commands:
  cancel      Cancel a queued VTGate resize for a Vitess branch
  status      Show the latest VTGate resize for a Vitess branch

Flags:
  -h, --help                                help for resize
      --vtgate-autoscaling                  Enable or disable VTGate autoscaling (use --vtgate-autoscaling=false to disable)
      --vtgate-count int                    Number of VTGates per availability zone (minimum when autoscaling is enabled)
      --vtgate-max-count int                Maximum VTGates per availability zone when autoscaling is enabled
      --vtgate-size string                  VTGate size SKU (e.g. VTG_320, VTG_1280)
      --vtgate-target-cpu-utilization int   Target CPU utilization percent when autoscaling is enabled

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

Use "pscale branch vtgate resize [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

At least one resize flag is required. Omitted flags are not sent as changes; boolean disablement therefore requires explicit `--vtgate-autoscaling=false`.

## pscale branch vtgate resize status

```text
Show the latest VTGate resize for a Vitess branch

Usage:
  pscale branch vtgate resize status <database> <branch> [flags]

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

## pscale branch vtgate resize cancel

```text
Cancel a queued VTGate resize for a Vitess branch

Usage:
  pscale branch vtgate resize cancel <database> <branch> [flags]

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

Cancel is an operational write. Confirm the target and latest request state before running it, then re-run `resize status` and `vtgate show` to verify the result and applied configuration.

## pscale branch vtctl

Previous capture note (superseded for this fence): The `vtctl` parent fence below is exact output from the official, checksum-verified PlanetScale CLI v0.341.0 macOS arm64 release binary after normalizing only trailing whitespace. The archive SHA-256 is `422dbd3568e62c2167c0aa629658ce31cedd5a3595d8c801eff88f7653bc4323`. The legacy `vtctld` alias was also executed and verified to render the same canonical `vtctl` parent surface. The previous parent omitted advanced children (`list-tablets`, `lookup-vindex`, `materialize`, and `planned-reparent-shard`); the current parent lists them. Subsequent child fences through `get-routing-rules` retain their previously recorded v0.339.0 provenance unless noted otherwise.

Complete help captured from the official, checksum-verified PlanetScale CLI v0.349.0 macOS arm64 binary, in an empty credential-free HOME/XDG/config working environment with `NO_COLOR=1` and `TERM=dumb`. Archive SHA-256: `1bdad82d821ab4eb65207672b38dfa063006460226715cb0937588ec671179a6`. Only terminal padding and trailing whitespace were normalized.

```text
Run vtctl commands against a branch. This command is only supported for Vitess databases.

Usage:
  pscale branch vtctl [command]

Aliases:
  vtctl, vtctld

Available Commands:
  apply-keyspace-routing-rules Replace live keyspace routing rules for a branch
  get-keyspace-routing-rules   Get live keyspace routing rules for a branch
  get-routing-rules            Get live routing rules for a branch
  get-shard                    Get a shard record for a branch
  list-keyspaces               List vtctld keyspaces for a branch
  list-tablets                 List tablets for a branch, grouped by keyspace and shard
  list-workflows               List vtctld workflows for a branch
  lookup-vindex                Manage Lookup Vindex operations
  materialize                  Manage Materialize workflows
  move-tables                  Manage MoveTables workflows
  planned-reparent-shard       Reparent a shard to a new primary
  refresh-state-by-shard       Reload tablet records for all tablets in a shard
  set-shard-tablet-control     Update shard tablet controls for a branch
  start-workflow               Start a workflow on a branch
  stop-workflow                Stop a workflow on a branch
  throttler                    Inspect and configure the tablet throttler
  vdiff                        Manage VDiff operations

Flags:
  -h, --help   help for vtctl

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

Use "pscale branch vtctl [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch vtctl get-keyspace-routing-rules

```text
Get live keyspace routing rules for a branch

Usage:
  pscale branch vtctl get-keyspace-routing-rules <database> <branch> [flags]

Flags:
  -h, --help   help for get-keyspace-routing-rules

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

## pscale branch vtctl apply-keyspace-routing-rules

```text
Replace live keyspace routing rules for a branch

Usage:
  pscale branch vtctl apply-keyspace-routing-rules <database> <branch> [flags]

Flags:
      --cells strings       Limit SrvVSchema rebuilding to these cells
  -h, --help                help for apply-keyspace-routing-rules
      --rules string        Keyspace routing rules as JSON
      --rules-file string   Path to keyspace routing rules JSON
      --skip-rebuild        Skip rebuilding SrvVSchema objects

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

## pscale branch vtctl throttler

```text
Inspect and configure the tablet throttler

Usage:
  pscale branch vtctl throttler [command]

Available Commands:
  check         Issue a throttler check against a single tablet
  status        Get the throttler status for a single tablet
  update-config Update the throttler configuration for a keyspace

Flags:
  -h, --help   help for throttler

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

Use "pscale branch vtctl throttler [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch vtctl throttler status

```text
Get the throttler status for a single tablet, identified by its alias. Discover tablet aliases with `pscale branch vtctl list-tablets`.

Usage:
  pscale branch vtctl throttler status <database> <branch> [flags]

Flags:
  -h, --help                  help for status
      --tablet-alias string   Alias of the tablet to probe (e.g. "zone1-0000000100") (required)

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

## pscale branch vtctl throttler check

```text
Issue a throttler check against a single tablet, identified by its alias. Discover tablet aliases with `pscale branch vtctl list-tablets`.

Usage:
  pscale branch vtctl throttler check <database> <branch> [flags]

Flags:
      --app-name string           App to issue the check on behalf of (e.g. "online-ddl"). Defaults to the throttler's default app.
  -h, --help                      help for check
      --ok-if-not-exists          Return OK even if the requested metric does not exist
      --scope string              Scope of the check, either "shard" or "self". Defaults to the throttler's default scope.
      --skip-request-heartbeats   Do not renew the throttler's heartbeat lease while serving this check
      --tablet-alias string       Alias of the tablet to check (e.g. "zone1-0000000100") (required)

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

## pscale branch vtctl throttler update-config

```text
Update the tablet throttler configuration for a keyspace. Omit --enabled to leave the keyspace enable state unchanged. Flag behavior mirrors vtctldclient UpdateThrottlerConfig: --throttle-app and --unthrottle-app are mutually exclusive; --app-name and --app-metrics are required together.

Usage:
  pscale branch vtctl throttler update-config <database> <branch> [flags]

Flags:
      --app-metrics strings              Metrics to check for --app-name (e.g. lag,loadavg)
      --app-name string                  App name for which to assign checked metrics (requires --app-metrics)
      --enabled                          Enable (true) or disable (false) the throttler for the keyspace. Omit to leave unchanged.
  -h, --help                             help for update-config
      --keyspace string                  Keyspace whose throttler config to update (required)
      --threshold float                  Replication lag threshold in seconds for the default check
      --throttle-app string              App name to throttle (e.g. "rowstreamer")
      --throttle-app-duration duration   Duration after which the --throttle-app rule expires (default 1h0m0s)
      --throttle-app-ratio float         Ratio to throttle the app specified by --throttle-app (0.00-1.00) (default 1)
      --unthrottle-app string            App name whose throttled-app rule should be removed

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

`--throttle-app` and `--unthrottle-app` are mutually exclusive. `--app-name` and `--app-metrics` are required together.

## pscale branch vtctl move-tables

The MoveTables parent, unchanged subcommands, and VDiff help fences below were re-captured from the same checksum-verified v0.339.0 binary. The changed `complete` and `cancel` fences were re-captured from the official, checksum-verified v0.341.0 macOS arm64 release binary after normalizing only trailing whitespace; that archive's SHA-256 is `422dbd3568e62c2167c0aa629658ce31cedd5a3595d8c801eff88f7653bc4323`.

```text
Manage MoveTables workflows

Usage:
  pscale branch vtctl move-tables [command]

Available Commands:
  cancel          Cancel a MoveTables workflow
  complete        Complete a MoveTables workflow
  create          Create a MoveTables workflow
  list            List MoveTables workflows
  reverse-traffic Reverse traffic for a MoveTables workflow
  show            Show details of a MoveTables workflow
  start           Start a MoveTables workflow
  status          Show the status of a MoveTables workflow
  stop            Stop a MoveTables workflow
  switch-traffic  Switch traffic for a MoveTables workflow

Flags:
  -h, --help   help for move-tables

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

Use "pscale branch vtctl move-tables [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch vtctl move-tables list

```text
List MoveTables workflows

Usage:
  pscale branch vtctl move-tables list <database> <branch> [flags]

Aliases:
  list, ls

Flags:
  -h, --help                     help for list
      --target-keyspace string   Filter by target keyspace (lists all keyspaces if omitted)

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

## pscale branch vtctl move-tables create

```text
Create a MoveTables workflow

Usage:
  pscale branch vtctl move-tables create <database> <branch> [flags]

Flags:
      --all-tables                               Move all tables from the source keyspace
      --atomic-copy                              Use atomic copy for the workflow
      --auto-start                               Automatically start the workflow after creation (default true)
      --cells strings                            Cells to restrict the workflow to (comma-separated)
      --defer-secondary-keys                     Defer secondary keys during the copy phase (default true)
      --exclude-tables strings                   Tables to exclude from the move (comma-separated)
      --global-keyspace string                   Unsharded keyspace in which to create the backing sequence tables when --sharded-auto-increment-handling is REPLACE
  -h, --help                                     help for create
      --on-ddl string                            DDL handling strategy (IGNORE, STOP, EXEC, EXEC_IGNORE)
      --sharded-auto-increment-handling string   Auto increment handling for sharded keyspaces
      --source-keyspace string                   Source keyspace (required)
      --source-time-zone string                  Source time zone
      --stop-after-copy                          Stop the workflow after the copy phase
      --tables strings                           Tables to move (comma-separated)
      --tablet-types strings                     Tablet types to use for the workflow (comma-separated)
      --target-keyspace string                   Target keyspace (required)
      --tenant-id string                         Tenant ID
      --workflow string                          Name of the workflow (required)

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

## pscale branch vtctl move-tables show

```text
Show details of a MoveTables workflow

Usage:
  pscale branch vtctl move-tables show <database> <branch> [flags]

Flags:
  -h, --help                     help for show
      --target-keyspace string   Target keyspace (required)
      --workflow string          Name of the workflow (required)

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

## pscale branch vtctl move-tables status

```text
Show the status of a MoveTables workflow

Usage:
  pscale branch vtctl move-tables status <database> <branch> [flags]

Flags:
  -h, --help                     help for status
      --target-keyspace string   Target keyspace (required)
      --workflow string          Name of the workflow (required)

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

## pscale branch vtctl move-tables start

```text
Start a MoveTables workflow

Usage:
  pscale branch vtctl move-tables start <database> <branch> [flags]

Flags:
  -h, --help                     help for start
      --target-keyspace string   Target keyspace (required)
      --workflow string          Name of the workflow (required)

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

## pscale branch vtctl move-tables stop

```text
Stop a MoveTables workflow

Usage:
  pscale branch vtctl move-tables stop <database> <branch> [flags]

Flags:
  -h, --help                     help for stop
      --target-keyspace string   Target keyspace (required)
      --workflow string          Name of the workflow (required)

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

## pscale branch vtctl move-tables switch-traffic

```text
Switch traffic for a MoveTables workflow

Usage:
  pscale branch vtctl move-tables switch-traffic <database> <branch> [flags]

Flags:
      --dry-run                           Only show what would be done
  -h, --help                              help for switch-traffic
      --initialize-target-sequences       Initialize target sequences
      --max-replication-lag-allowed int   Maximum replication lag allowed in seconds
      --tablet-types strings              Tablet types to switch traffic for (comma-separated) (required)
      --target-keyspace string            Target keyspace (required)
      --workflow string                   Name of the workflow (required)

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

## pscale branch vtctl move-tables reverse-traffic

```text
Reverse traffic for a MoveTables workflow

Usage:
  pscale branch vtctl move-tables reverse-traffic <database> <branch> [flags]

Flags:
      --dry-run                           Only show what would be done
  -h, --help                              help for reverse-traffic
      --max-replication-lag-allowed int   Maximum replication lag allowed in seconds
      --tablet-types strings              Tablet types to reverse traffic for (comma-separated)
      --target-keyspace string            Target keyspace (required)
      --workflow string                   Name of the workflow (required)

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

## pscale branch vtctl move-tables complete

```text
Complete a MoveTables workflow

Usage:
  pscale branch vtctl move-tables complete <database> <branch> [flags]

Flags:
      --dry-run                  Only show what would be done
  -h, --help                     help for complete
      --ignore-source-keyspace   Complete without touching the source keyspace. Only use this when the source keyspace has been deleted or is unavailable
      --keep-data                Keep the source tables instead of dropping them. Use this when the source is an external keyspace (required)
      --keep-routing-rules       Keep the routing rules (required)
      --rename-tables            Rename source tables instead of dropping them
      --target-keyspace string   Target keyspace (required)
      --workflow string          Name of the workflow (required)

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

## pscale branch vtctl move-tables cancel

```text
Cancel a MoveTables workflow

Usage:
  pscale branch vtctl move-tables cancel <database> <branch> [flags]

Flags:
  -h, --help                     help for cancel
      --ignore-source-keyspace   Cancel without touching the source keyspace. Only use this when the source keyspace has been deleted or is unavailable
      --keep-data                Keep the data copied into the target keyspace instead of deleting it (required)
      --keep-routing-rules       Keep the routing rules (required)
      --target-keyspace string   Target keyspace (required)
      --workflow string          Name of the workflow (required)

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

## pscale branch vtctl vdiff

```text
Manage VDiff operations

Usage:
  pscale branch vtctl vdiff [command]

Available Commands:
  create      Create a VDiff
  delete      Delete a VDiff
  list        List VDiffs
  resume      Resume a stopped VDiff
  show        Show details of a VDiff
  stop        Stop a VDiff

Flags:
  -h, --help   help for vdiff

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

Use "pscale branch vtctl vdiff [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch vtctl vdiff create

```text
Create a VDiff

Usage:
  pscale branch vtctl vdiff create <database> <branch> [flags]

Flags:
      --auto-retry                           Automatically retry on error (default true)
      --auto-start                           Automatically start the VDiff (default true)
      --debug-query                          Log the queries used for the VDiff
      --filtered-replication-wait-time int   Filtered replication wait time in seconds
  -h, --help                                 help for create
      --limit int                            Maximum number of rows to compare
      --max-extra-rows-to-compare int        Maximum extra rows to compare
      --max-report-sample-rows int           Maximum number of sample rows in report
      --only-pks                             Only compare primary keys
      --row-diff-column-truncate-at int      Truncate column values at this length in the report
      --tables strings                       Tables to compare (comma-separated)
      --tablet-selection-preference string   Tablet selection preference
      --tablet-types strings                 Tablet types to use (comma-separated)
      --target-keyspace string               Target keyspace (required)
      --update-table-stats                   Update table statistics before the VDiff
      --verbose                              Verbose output
      --workflow string                      Name of the workflow (required)

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

## pscale branch vtctl vdiff show

```text
Show details of a VDiff

Usage:
  pscale branch vtctl vdiff show <database> <branch> [flags]

Flags:
  -h, --help                     help for show
      --target-keyspace string   Target keyspace (required)
      --uuid string              UUID of the VDiff (required)
      --workflow string          Name of the workflow (required)

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

## pscale branch vtctl vdiff resume

```text
Resume a stopped VDiff

Usage:
  pscale branch vtctl vdiff resume <database> <branch> [flags]

Flags:
  -h, --help                     help for resume
      --target-keyspace string   Target keyspace (required)
      --target-shards strings    Target shards to resume (comma-separated)
      --uuid string              UUID of the VDiff (required)
      --workflow string          Name of the workflow (required)

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

## pscale branch vtctl get-shard

```text
Get a live shard record from the cluster via vtctld, including tablet controls and denied tables.

Usage:
  pscale branch vtctl get-shard <database> <branch> [flags]

Flags:
  -h, --help              help for get-shard
      --keyspace string   Keyspace name (required)
      --shard string      Shard name (e.g. "-" for unsharded) (required)

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

## pscale branch vtctl get-routing-rules

```text
Get live routing rules from the cluster via vtctld. This reads the current cluster state, unlike `pscale branch routing-rules get`, which reads from the schema snapshot.

Usage:
  pscale branch vtctl get-routing-rules <database> <branch> [flags]

Flags:
  -h, --help   help for get-routing-rules

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

## pscale branch create (v0.327.0)

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Create a new branch from a database

Usage:
  pscale branch create <source-database> <branch> [options] [flags]

Aliases:
  create, b

Flags:
      --cluster-size string    Cluster size for the branch. Defaults to PS_DEV for regular branches, or PS-10 for branches created from a backup or with seed-data. Use 'pscale size cluster list' to see the valid sizes.
      --from string            Parent branch to create the new branch from. Cannot be used with --restore unless --restore-point is set.
  -h, --help                   help for create
      --major-version string   For PostgreSQL databases, the PostgreSQL major version to use for the branch. Defaults to the major version of the parent branch if it exists or the database's default branch major version. Ignored for branches restored from backups.
      --max-storage int        Maximum storage size in bytes for autoscaling
      --min-storage int        Minimum storage size in bytes
      --region string          Region for the branch to be created in.
      --restore string         ID of Backup to restore into branch.
      --restore-point string   For PostgreSQL databases, restore from a point-in-time recovery timestamp (e.g. 2023-01-01T00:00:00Z). Requires --restore or --from.
      --seed-data              Add seed data using the Data Branching™ feature. This branch will be created with the same resources as the base branch.
      --wait                   Wait until the branch is ready

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

## pscale branch switchover (v0.327.0)

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Switch over the primary of a Postgres branch. Postgres only.

On a branch with replicas the primary steps down and a replica is promoted in
its place; use --candidate to pick the replica, otherwise one is selected
automatically. A branch running a single instance has nothing to promote, so
that instance is restarted in place and the branch is unreachable while it
comes back. Writes are briefly interrupted while the switch completes.

Usage:
  pscale branch switchover <database> <branch> [flags]
  pscale branch switchover [command]

Available Commands:
  list        List switchovers for a Postgres branch
  show        Show a switchover for a Postgres branch

Flags:
      --candidate string   Name of the replica to promote, as returned by 'branch infra'. Omit to select automatically. Only applies to branches with replicas
  -h, --help               help for switchover

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

Use "pscale branch switchover [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch switchover list

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
List switchovers for a Postgres branch

Usage:
  pscale branch switchover list <database> <branch> [flags]

Aliases:
  list, ls

Flags:
  -h, --help           help for list
      --page int       Page number to fetch
      --per-page int   Number of results per page (default 100)

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

## pscale branch switchover show

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Show a switchover for a Postgres branch

Usage:
  pscale branch switchover show <database> <branch> <id> [flags]

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

## Compatibility

Neki live connection kill actions, promote/demote sizing flags, and Postgres maintenance window/event commands require CLI v0.349.0 or later, plus API support/permissions. Replay remains read-only. New maintenance window/event help is in the standalone maintenance skill. Changed fences explicitly identify their v0.349.0 capture below or above; unchanged captures retain their original attribution.

## pscale branch promote

Complete help captured from the official, checksum-verified PlanetScale CLI v0.349.0 macOS arm64 binary, in an empty credential-free HOME/XDG/config working environment with `NO_COLOR=1` and `TERM=dumb`. Archive SHA-256: `1bdad82d821ab4eb65207672b38dfa063006460226715cb0937588ec671179a6`. Only terminal padding and trailing whitespace were normalized.

```text
Promote a branch to production.

This command is supported for MySQL databases and for enabled Postgres branches. Neki databases are not supported.

--cluster-size sets the cluster size to use. PS-DEV is not permitted. When
omitted, a PS-DEV Postgres branch uses the smallest production size. For
MySQL, the size applies to the default keyspace. Changing the size requires
the write_database permission.

--replicas sets the Postgres replica count, not including the primary. 0 is a
single node. 2 to 8 is high availability. Omit it to leave the count
unchanged. Changing the replica count requires the write_database permission.

Usage:
  pscale branch promote <database> <branch> [flags]

Examples:
  pscale branch promote mydb dev
  pscale branch promote mydb dev --cluster-size PS-10
  pscale branch promote mydb dev --cluster-size PS-10 --replicas 2

Flags:
      --cluster-size string   Cluster size to apply when promoting (for example, PS-10). PS-DEV is not permitted. Use 'pscale size cluster list' to see valid sizes.
  -h, --help                  help for promote
      --replicas int          Postgres replica count, not including the primary. 0 is a single node. 2 to 8 is high availability.

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

## pscale branch demote

Complete help captured from the official, checksum-verified PlanetScale CLI v0.349.0 macOS arm64 binary, in an empty credential-free HOME/XDG/config working environment with `NO_COLOR=1` and `TERM=dumb`. Archive SHA-256: `1bdad82d821ab4eb65207672b38dfa063006460226715cb0937588ec671179a6`. Only terminal padding and trailing whitespace were normalized.

```text
Demote a production branch to development.

This command is supported for MySQL databases and for enabled Postgres branches. Neki databases are not supported.

--cluster-size sets the Postgres cluster size to use. PS-DEV is allowed. Omit
it to leave the size unchanged. Changing the size requires the write_database
permission.

--replicas sets the Postgres replica count, not including the primary. 0 is a
single node. 2 to 8 is high availability. Omit it to leave the count
unchanged. Changing the replica count requires the write_database permission.

Vitess ignores both options.

Usage:
  pscale branch demote <database> <branch> [flags]

Examples:
  pscale branch demote mydb main
  pscale branch demote mydb main --cluster-size PS-DEV
  pscale branch demote mydb main --cluster-size PS-10 --replicas 0

Flags:
      --cluster-size string   Postgres cluster size to apply when demoting (for example, PS-DEV). Use 'pscale size cluster list' to see valid sizes.
  -h, --help                  help for demote
      --replicas int          Postgres replica count, not including the primary. 0 is a single node. 2 to 8 is high availability.

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
