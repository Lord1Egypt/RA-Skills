Except for the separately attributed detach section, help fences below are exact output from the official, checksum-verified PlanetScale CLI v0.343.0 macOS arm64 release binary after normalizing only trailing whitespace. The archive SHA-256 is `98672666af6ca95e58a60f51fccebbb75294e428fc37d96ee372cac1b322acfe`.

`pscale dedicated-read-replica` is the canonical command. The hidden `pscale read-only-replica` compatibility alias remains available but prints a deprecation warning on stderr when invoked.

## `pscale dedicated-read-replica`

```text
Manage dedicated read replicas for a PostgreSQL database branch.

Dedicated read replicas provide dedicated capacity for queries that can
tolerate replication lag. They accept read traffic only.

This command is only available for PostgreSQL databases.

Usage:
  pscale dedicated-read-replica [command]

Available Commands:
  create      Create a dedicated read replica
  delete      Delete a dedicated read replica
  list        List dedicated read replicas for a Postgres branch
  show        Show a dedicated read replica
  update      Update a dedicated read replica

Flags:
  -h, --help         help for dedicated-read-replica
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

Use "pscale dedicated-read-replica [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## `pscale dedicated-read-replica list`

```text
List dedicated read replicas for a Postgres branch

Usage:
  pscale dedicated-read-replica list <database> <branch> [flags]

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

## `pscale dedicated-read-replica show`

```text
Show a dedicated read replica

Usage:
  pscale dedicated-read-replica show <database> <branch> <name> [flags]

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

## `pscale dedicated-read-replica create`

```text
Create a dedicated read replica for a PostgreSQL database branch.

Region is required. The replica count defaults to 1 and the cluster size
defaults to the primary cluster size when those flags are omitted.

Usage:
  pscale dedicated-read-replica create <database> <branch> <name> [flags]

Flags:
      --cluster-size string   Cluster size SKU; defaults to the primary cluster size
  -h, --help                  help for create
      --region string         Region slug for the dedicated read replica (required)
      --replicas int          Number of instances serving reads (default 1)

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

## `pscale dedicated-read-replica update`

```text
Update a dedicated read replica's cluster size, instance count, and/or
PostgreSQL configuration parameters. Parameter values must be greater than or
equal to the primary branch's corresponding values.

Usage:
  pscale dedicated-read-replica update <database> <branch> <name> [flags]

Examples:
  pscale dedicated-read-replica update mydb main analytics --replicas 2
  pscale dedicated-read-replica update mydb main analytics --cluster-size PS_20_GCP_X86
  pscale dedicated-read-replica update mydb main analytics --parameters pgconf.max_connections=300

Flags:
      --cluster-size string      New cluster size SKU
  -h, --help                     help for update
      --parameters stringArray   Set a parameter as namespace.name=value (for example pgconf.max_connections=300); repeatable
      --replicas int             Desired number of instances serving reads

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

## `pscale dedicated-read-replica delete`

```text
Delete a dedicated read replica

Usage:
  pscale dedicated-read-replica delete <database> <branch> <name> [flags]

Aliases:
  delete, rm

Flags:
      --force   Delete a dedicated read replica without confirmation
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

## Compatibility

The hidden, feature-gated `dedicated-read-replica detach` command requires CLI v0.349.0 or later and API availability. Existing parent/list/show/create/update/delete captures remain unchanged with their original v0.343.0 attribution; the parent intentionally does not list detach.

## pscale dedicated-read-replica detach

Complete help captured from the official, checksum-verified PlanetScale CLI v0.349.0 macOS arm64 binary, in an empty credential-free HOME/XDG/config working environment with `NO_COLOR=1` and `TERM=dumb`. Archive SHA-256: `1bdad82d821ab4eb65207672b38dfa063006460226715cb0937588ec671179a6`. Only terminal padding and trailing whitespace were normalized.

```text
Detach a dedicated read replica from its branch and promote it to a
standalone branch of the database.

The new branch keeps the replica's name, region, cluster size, replica count,
storage configuration, and parameters, and receives a copy of the source
branch's roles. The dedicated read replica no longer exists once it is
detached. This cannot be undone.

The replica must be ready with no pending changes, and any dedicated
PgBouncers attached to it must be deleted first.

This command is only available for PostgreSQL databases.

Usage:
  pscale dedicated-read-replica detach <database> <branch> <name> [flags]

Flags:
      --force   Detach a dedicated read replica without confirmation
  -h, --help    help for detach

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
