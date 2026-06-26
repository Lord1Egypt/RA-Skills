## pscale branch

```text
Create, delete, diff, and manage branches

Usage:
  pscale branch [command]

Available Commands:
  connections     Show and kill branch connections
  create          Create a new branch from a database
  delete          Delete a branch from a database
  demote          Demote a production branch to development
  diff            Show the diff of a branch
  lint            Lints the schema for a branch
  list            List all branches of a database
  promote         Promote a new branch from a database
  refresh-schema  Refresh the schema for a database branch
  routing-rules   Fetch or update your keyspace routing rules
  safe-migrations Enable or disable safe migrations on a branch
  schema          Show the schema of a branch
  show            Show a specific branch of a database
  switch          Switches the current project to use the specified branch

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

```

## pscale branch connections

```text
Show and kill branch connections.

Agent workflow:
  1. Run: pscale branch connections show <database> <branch> --format json
  2. Inspect query_id, transaction_id, and connection_id from the selected row.
  3. Explain the proposed action and wait for user approval before running it.
  4. Run exactly one action command with the matching ID.
  5. Run show again to verify the result.

Action semantics:
  kill <database> <branch> <query-id> --query        Cancels the listed query_id.
  kill-transaction <database> <branch> <transaction-id>
                                                     Postgres only. destructive. Terminates the listed transaction_id if it still matches server state.
  kill <database> <branch> <connection-id>           destructive. Terminates the listed connection_id.

Use --format json when an agent or script needs to inspect query_id,
transaction_id, and connection_id fields. Human output uses vertical records so
query text and action IDs are not truncated.

Usage:
  pscale branch connections [command]

Available Commands:
  kill             Kill a branch connection or query
  kill-transaction Kill a Postgres branch transaction
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

```

## pscale branch connections top

```text
Show live branch connection activity.

Run interactively in a terminal to launch the TUI. Pipe or redirect output to
run headlessly with --capture; --duration bounds either mode and without
--duration the command runs until interrupted. Pass --replay FILE to render a
previously captured trace in the TUI — actions are rejected in replay mode.

For Postgres, connections top shows session activity across instances. For
Vitess, pass --keyspace and --shard or run interactively to select them when
the server reports available targets.

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

```

## pscale branch connections kill

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

```

## pscale branch connections kill-transaction

```text
Kill a Postgres branch transaction.

This is destructive. Pass a transaction_id from connections show to terminate
the matching Postgres connection.

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

```

## pscale branch routing-rules

```text
Fetch or update your keyspace routing rules

Usage:
  pscale branch routing-rules [command]

Available Commands:
  get         Show the routing rules of a branch
  update      Update the routing rules of a branch

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

```

## pscale branch routing-rules get

```text
Show the routing rules of a branch

Usage:
  pscale branch routing-rules get <database> <branch> [flags]

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

```

## pscale branch routing-rules update

```text
Update the routing rules of a branch

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

```

## pscale branch vtctld

```text
Run vtctld commands against a branch. This command is only supported for Vitess databases.

Usage:
  pscale branch vtctld [command]

Available Commands:
  get-routing-rules      Get live routing rules for a branch
  list-keyspaces         List vtctld keyspaces for a branch
  list-tablets           List tablets for a branch, grouped by keyspace and shard
  list-workflows         List vtctld workflows for a branch
  lookup-vindex          Manage Lookup Vindex operations
  materialize            Manage Materialize workflows
  move-tables            Manage MoveTables workflows
  planned-reparent-shard Reparent a shard to a new primary
  start-workflow         Start a workflow on a branch
  stop-workflow          Stop a workflow on a branch
  throttler              Inspect and configure the tablet throttler
  vdiff                  Manage VDiff operations

Flags:
  -h, --help   help for vtctld

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

Use "pscale branch vtctld [command] --help" for more information about a command.

```

## pscale branch vtctld get-routing-rules

```text
Get live routing rules from the cluster via vtctld. This reads the current cluster state, unlike `pscale branch routing-rules get`, which reads from the schema snapshot.

Usage:
  pscale branch vtctld get-routing-rules <database> <branch> [flags]

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

```
