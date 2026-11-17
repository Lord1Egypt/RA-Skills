The `pscale keyspace update-settings` help fence is a complete current capture from the official, checksum-verified PlanetScale CLI v0.344.0 macOS arm64 binary with `NO_COLOR=1`, normalizing only trailing whitespace. Archive SHA-256: `1b59b271590d9b49dd52aafbb0e5c0cd788b44c00a5627d6487cd0d18815cf53`. Other sections retain their stated earlier provenance.

> Help fences in this file have mixed provenance. Each section states the release binary used for its exact capture or verification. v0.333.0 captures use the official macOS arm64 release archive SHA-256 `6544cc6fa5d82dc78744579cc3a54204c1cfde352bf13ceae340bd7df5799771`, after normalizing only trailing whitespace.

## pscale database

The help fence below is exact output from the official, checksum-verified PlanetScale CLI v0.333.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Create, read, update, delete, and dump/restore databases

Usage:
  pscale database [command]

Aliases:
  database, db

Available Commands:
  aggressive-cutover Show or change aggressive cutover for a database
  create             Create a database instance
  delete             Delete a database instance
  dump               Backup and dump your database (Vitess databases only)
  ip-restriction     Manage Postgres IP restrictions
  list               List databases
  read-only-regions  List read-only regions for a database
  regions            List regions available to a database
  restore-dump       Restore your database from a local dump directory (Vitess databases only)
  show               Retrieve information about a database, including settings
  throttler          Show or update database throttler configuration
  update             Update a database's settings

Flags:
  -h, --help         help for database
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

Use "pscale database [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```


## pscale database create

The help fence below is exact output from the official, checksum-verified PlanetScale CLI v0.332.0 macOS arm64 release binary with `NO_COLOR=1`, after normalizing only trailing whitespace. The archive SHA-256 is `61eadf71c9d5e6423587fbf01fd698800d8a944775a06519a1c2ac38fcb89287`.

```text
Create a database instance

Usage:
  pscale database create <database> [flags]

Flags:
      --cluster-size pscale size cluster list   cluster size for Scaler Pro databases. Use pscale size cluster list to see the valid sizes.
      --engine string                           The database engine for the database. Supported values: mysql, postgresql, neki. Defaults to mysql. (default "mysql")
  -h, --help                                    help for create
      --major-version string                    For Postgres or Neki databases, the Postgres major version to use. Defaults to the latest available major version.
      --max-storage int                         Maximum storage size in bytes for autoscaling
      --min-storage int                         Minimum storage size in bytes
      --region string                           region for the database
      --replicas int                            number of replicas for Postgres or Neki databases. Use 0 for single-node Postgres or 2 or more for HA.
      --wait                                    Wait until the database is ready

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

## pscale database aggressive-cutover

```text
Show, enable, or disable aggressive cutover for a Vitess database.

When enabled, future deploy requests on this database cut over more
aggressively when waiting on table locks. This is a database-level setting,
not the same as forcing cutover on a single deploy request
(pscale deploy-request force-cutover).

See https://planetscale.com/docs/vitess/schema-changes/aggressive-cutover

Usage:
  pscale database aggressive-cutover [command]

Available Commands:
  disable     Disable aggressive cutover for a database
  enable      Enable aggressive cutover for a database
  show        Show whether aggressive cutover is enabled

Flags:
  -h, --help   help for aggressive-cutover

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

Use "pscale database aggressive-cutover [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale database aggressive-cutover show

```text
Show whether aggressive cutover is enabled

Usage:
  pscale database aggressive-cutover show <database> [flags]

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

## pscale database aggressive-cutover enable

```text
Enable aggressive cutover for a database

Usage:
  pscale database aggressive-cutover enable <database> [flags]

Flags:
  -h, --help   help for enable

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

## pscale database aggressive-cutover disable

```text
Disable aggressive cutover for a database

Usage:
  pscale database aggressive-cutover disable <database> [flags]

Flags:
  -h, --help   help for disable

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

## pscale database throttler

This parent and its `show`/`update` help fences were re-captured from the official, checksum-verified PlanetScale CLI v0.339.0 macOS arm64 release binary after normalizing only trailing whitespace. The archive SHA-256 is `1e396701709cd49d1d1cccca252e2bd81f224b2830ca189a84a16983bde182e8`.

```text
Show or update database-level Vitess migration throttler configuration.

This sets the default throttler for future deploy requests on the database.
It is not the per-deploy-request throttler (pscale deploy-request throttler)
and not the tablet/vtctl throttler (pscale branch vtctl throttler).

Usage:
  pscale database throttler [command]

Available Commands:
  show        Show database throttler configuration
  update      Update database throttler configuration

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

Use "pscale database throttler [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale database throttler show

```text
Show database throttler configuration

Usage:
  pscale database throttler show <database> [flags]

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

## pscale database throttler update

```text
Update database-level Vitess migration throttler configuration.

Use --ratio to apply one ratio (0-95) to all eligible keyspaces.
Use --configuration keyspace=ratio (repeatable) for per-keyspace ratios.
Pass exactly one of these modes. 0 effectively disables throttling; 95 slows migrations the most.

This is the database default for future deploy requests, not a single deploy request.

Usage:
  pscale database throttler update <database> [flags]

Flags:
      --configuration stringArray   Per-keyspace ratio as keyspace=ratio (repeatable)
  -h, --help                        help for update
      --ratio int                   Throttler ratio 0-95 applied to all eligible keyspaces

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

## pscale keyspace read-only-regions

```text
List read-only regions configured for a Vitess keyspace.

This command is only supported for Vitess databases.

Usage:
  pscale keyspace read-only-regions <database> <branch> <keyspace> [flags]
  pscale keyspace read-only-regions [command]

Available Commands:
  add         Add a read-only region to a keyspace
  remove      Remove a read-only region from a keyspace
  update      Update a keyspace's read-only region

Flags:
  -h, --help   help for read-only-regions

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

Use "pscale keyspace read-only-regions [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

JSON output includes each region's identifying fields plus cluster size and replica count. Use a ready region's slug, display name, or ID with `database dump --read-only-region`.

## pscale database dump

The help fence below is exact output from the official, checksum-verified PlanetScale CLI v0.333.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Backup and dump your database.

This command is only supported for Vitess databases. For Postgres databases, use standard PostgreSQL tools like pg_dump. See: https://planetscale.com/docs/postgres/imports/postgres-migrate-dumprestore

Usage:
  pscale database dump <database> <branch> [options] [flags]

Flags:
      --columns stringArray         Columns to include for specific tables (format: 'table:col1,col2'). Can be specified multiple times for different tables.
  -h, --help                        help for dump
      --keyspace string             Optionally target a specific keyspace to be dumped. Useful for sharded databases.
      --local-addr string           Local address to bind and listen for connections. By default the proxy binds to 127.0.0.1 with a random port.
      --output string               Output directory of the dump. By default the dump is saved to a folder in the current directory.
      --output-format string        Output format for data: sql (for MySQL, default), json, or csv. (default "sql")
      --rdonly                      Dump from a rdonly tablet in the primary region (if available; will fail if not). Not for separate read-only regions — use --read-only-region instead.
      --read-only-region string     Dump from a Vitess read-only region (region slug, display name, or id). List regions with: pscale database read-only-regions list <database>.
      --remote-addr hostname:port   PlanetScale Database remote network address. By default the remote address is populated automatically from the PlanetScale API. (format: hostname:port)
      --replica                     Dump from a replica tablet in the primary region (if available; will fail if not).
      --schema-only                 Only dump schema, skip table data.
      --shard string                Optional shard to target, must be used with keyspace
      --tables string               Comma separated string of tables to dump. By default all tables are dumped.
      --threads int                 Number of concurrent threads to use to dump the database. (default 16)
      --wheres string               Comma separated string of WHERE clauses to filter the tables to dump. Only used when you specify tables to dump. Default is not to filter dumped tables.

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

`--read-only-region` cannot be combined with `--rdonly` or `--replica`. The command rejects regions that are not ready and creates a short-lived reader credential scoped to the selected region; it does not fall back to the primary region.

## pscale database update

```text
Update a database's settings.

Only flags you pass are sent to the API. Boolean flags must be set explicitly,
for example --insights-raw-queries=true or --insights-raw-queries=false.

Flags marked "Vitess only" are rejected for PostgreSQL databases.

Usage:
  pscale database update <database> [flags]

Flags:
      --allow-data-branching            Allow seeding branches with data (Vitess only)
      --allow-foreign-key-constraints   Allow foreign key constraints (Vitess only)
      --automatic-migrations            Copy migration data to new branches and deploy requests (Vitess only)
      --default-branch string           The default branch of the database (PostgreSQL and Vitess)
  -h, --help                            help for update
      --insights-raw-queries            Collect full SQL queries for Insights (Vitess only; PostgreSQL uses pgconf.pginsights.raw_queries)
      --migration-framework string      Migration framework for the database (Vitess only)
      --migration-table-name string     Migration table name for the database (Vitess only)
      --new-name string                 Rename the database (PostgreSQL and Vitess)
      --production-branch-web-console   Allow the web console on the production branch (PostgreSQL and Vitess)
      --require-approval-for-deploy     Require admin approval for deploy requests (Vitess only)
      --restrict-branch-region          Limit branch creation to the database region (PostgreSQL and Vitess)

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

Only supplied flags are sent. Set booleans explicitly, for example `--require-approval-for-deploy=true` or `=false`.

## pscale database ip-restriction

```text
Manage IP restrictions for a PostgreSQL database.

IP restrictions limit which IPv4 addresses or ranges can connect. Rules can
optionally be scoped to a specific Postgres schema and/or role. This command
is only available for PostgreSQL databases.

Usage:
  pscale database ip-restriction [command]

Aliases:
  ip-restriction, cidr, cidrs

Available Commands:
  create      Create an IP restriction entry
  delete      Delete an IP restriction entry
  list        List IP restriction entries for a Postgres database
  show        Show an IP restriction entry
  update      Update an IP restriction entry

Flags:
  -h, --help   help for ip-restriction

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

Use "pscale database ip-restriction [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

Create requires `--cidrs` with repeatable or comma-separated IPv4 CIDRs; optional `--schema`, `--role`, and `--description` scope the entry. Update replaces only supplied fields. Delete accepts `--force` but should be treated as destructive because entries apply across all database branches.

## pscale keyspace read-only-regions add

```text
Add a read-only region to a Vitess keyspace.

<region> is a PlanetScale region slug. List available slugs with: pscale region list.

Usage:
  pscale keyspace read-only-regions add <database> <branch> <keyspace> <region> [flags]

Flags:
      --cluster-size pscale size cluster list   cluster size for the keyspace in this read-only region. Use pscale size cluster list to get a list of valid sizes.
  -h, --help                                    help for add
      --replicas int                            number of replicas per shard in this read-only region

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

## pscale keyspace read-only-regions update

```text
Update cluster size or replicas for a keyspace's read-only region.

<region> is a PlanetScale region slug already configured on the keyspace. List configured regions with: pscale keyspace read-only-regions <database> <branch> <keyspace>.

Usage:
  pscale keyspace read-only-regions update <database> <branch> <keyspace> <region> [flags]

Flags:
      --cluster-size pscale size cluster list   cluster size for the keyspace in this read-only region. Use pscale size cluster list to get a list of valid sizes.
  -h, --help                                    help for update
      --replicas int                            number of replicas per shard in this read-only region

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

## pscale keyspace read-only-regions remove

```text
Remove a read-only region from a Vitess keyspace.

<region> is a PlanetScale region slug already configured on the keyspace. List configured regions with: pscale keyspace read-only-regions <database> <branch> <keyspace>.

Usage:
  pscale keyspace read-only-regions remove <database> <branch> <keyspace> <region> [flags]

Flags:
  -h, --help   help for remove

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

These commands are Vitess-only. `add` uses a slug from `pscale region list`; update/remove require a region already configured on the keyspace. Verify the resulting list after every write.

## pscale keyspace

The keyspace parent help block below is exact output from the official, checksum-verified PlanetScale CLI v0.343.0 macOS arm64 release binary after normalizing only trailing whitespace. The archive SHA-256 is `98672666af6ca95e58a60f51fccebbb75294e428fc37d96ee372cac1b322acfe`. The list, show, and delete help blocks remain exact v0.324.0 captures and were re-verified line-for-line unchanged with that v0.343.0 binary.

```text
List, show, and manage keyspaces.

This command is only supported for Vitess databases.

Usage:
  pscale keyspace [command]

Available Commands:
  create            Create a new keyspace within a branch
  create-external   Create an external keyspace on a branch
  delete            Delete a keyspace from a branch
  list              List all keyspaces within a branch
  parameters        List and change the VTTablet and MySQL parameters of a keyspace
  read-only-regions List read-only regions for a keyspace
  resize            Resize a keyspace within a branch
  rollout-status    Show keyspace rollout status per shard
  settings          Show the settings for a keyspace
  show              Show a keyspace within a branch
  update-settings   Update the settings for a keyspace
  vschema           Update or show the VSchema of a branch

Flags:
  -h, --help         help for keyspace
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

Use "pscale keyspace [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale keyspace parameters

All keyspace-parameter help fences below are exact output from the official, checksum-verified PlanetScale CLI v0.343.0 macOS arm64 release binary after normalizing only trailing whitespace. The archive SHA-256 is `98672666af6ca95e58a60f51fccebbb75294e428fc37d96ee372cac1b322acfe`.

```text
List the VTTablet and MySQL parameters of a keyspace, including their current and default values.

To change parameters, use 'pscale keyspace parameters set <database> <branch> <keyspace> --parameters namespace.name=value'.

Usage:
  pscale keyspace parameters <database> <branch> <keyspace> [flags]
  pscale keyspace parameters [command]

Aliases:
  parameters, params

Available Commands:
  changes     Manage parameter changes to a keyspace
  list        List the VTTablet and MySQL parameters of a keyspace
  set         Change the VTTablet and MySQL parameters of a keyspace

Flags:
  -h, --help               help for parameters
      --namespace string   Only show parameters in this namespace: vttablet or mysqld.

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

Use "pscale keyspace parameters [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale keyspace parameters list

```text
List the VTTablet and MySQL parameters of a keyspace, including their current and default values.

To change parameters, use 'pscale keyspace parameters set <database> <branch> <keyspace> --parameters namespace.name=value'.

Usage:
  pscale keyspace parameters list <database> <branch> <keyspace> [flags]

Flags:
  -h, --help               help for list
      --namespace string   Only show parameters in this namespace: vttablet or mysqld.

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

## pscale keyspace parameters set

```text
Change VTTablet or MySQL parameters on a keyspace. Pass each parameter as namespace.name=value, where namespace is vttablet or mysqld, and pass --reset namespace.name to set a parameter back to its default.

All changes are submitted together and rolled out to the keyspace. Use 'pscale keyspace parameters changes list' to follow the rollout.

Usage:
  pscale keyspace parameters set <database> <branch> <keyspace> [flags]

Examples:
  pscale keyspace parameters set <database> <branch> <keyspace> \
    --parameters vttablet.vreplication-parallel-insert-workers=4 \
    --parameters vttablet.vreplication_max_time_to_retry_on_error=720h

  pscale keyspace parameters set <database> <branch> <keyspace> \
    --reset vttablet.vreplication-parallel-insert-workers

Flags:
  -h, --help                     help for set
      --parameters stringArray   Set a parameter as namespace.name=value, where namespace is vttablet or mysqld (e.g. vttablet.vreplication-parallel-insert-workers=4). Repeatable. Use 'pscale keyspace parameters list' to see available parameters.
      --reset stringArray        Set a parameter back to its default, as namespace.name (e.g. vttablet.vreplication-parallel-insert-workers). Repeatable.

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

## pscale keyspace parameters changes

```text
Manage parameter changes to a keyspace

Usage:
  pscale keyspace parameters changes [command]

Available Commands:
  cancel      Cancel a pending parameter change to a keyspace
  list        List parameter changes to a keyspace
  show        Show a parameter change to a keyspace

Flags:
  -h, --help   help for changes

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

Use "pscale keyspace parameters changes [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale keyspace parameters changes list

```text
List parameter changes to a keyspace

Usage:
  pscale keyspace parameters changes list <database> <branch> <keyspace> [flags]

Aliases:
  list, ls

Flags:
  -h, --help           help for list
      --page int       Page number to fetch
      --per-page int   Number of results per page (default 25)

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

## pscale keyspace parameters changes show

```text
Show a parameter change to a keyspace

Usage:
  pscale keyspace parameters changes show <database> <branch> <keyspace> <change-id> [flags]

Aliases:
  show, get

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

## pscale keyspace parameters changes cancel

```text
Cancel a pending parameter change to a keyspace

Usage:
  pscale keyspace parameters changes cancel <database> <branch> <keyspace> <change-id> [flags]

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

## pscale keyspace create-external

The help fence below is exact output from the official, checksum-verified PlanetScale CLI v0.341.0 macOS arm64 release binary after normalizing only trailing whitespace. The archive SHA-256 is `422dbd3568e62c2167c0aa629658ce31cedd5a3595d8c801eff88f7653bc4323`.

```text
Create an external keyspace by connecting a branch to an existing MySQL database.

--source-database is the remote MySQL database name, not the PlanetScale
database. --cluster-size is optional and selects the external tablet size;
when omitted, PlanetScale chooses a size from the source storage. Managed
organizations should pass a size from pscale size cluster list.

Usage:
  pscale keyspace create-external <database> <branch> <keyspace> [flags]

Flags:
      --cluster-size pscale size cluster list   External tablet size. Optional; defaults from source storage. Use pscale size cluster list for valid sizes.
      --dry-run                                 Check compatibility with the external database without creating the keyspace
  -h, --help                                    help for create-external
      --host string                             Host name of the external database (required)
      --min-tls-version string                  Minimum TLS version
      --password string                         Password to connect to the external database (required)
      --port int                                Port number to connect to the external database (default 3306)
      --skip-lint-errors                        Create even if datasource lint reports errors, when the organization allows it
      --source-database string                  Name of the database on the external MySQL server (required)
      --ssl-certificate-authority string        CA certificate chain, or a path to a PEM file
      --ssl-client-certificate string           Client certificate, or a path to a PEM file
      --ssl-client-key string                   Client private key, or a path to a PEM file
      --ssl-mode string                         SSL verification mode, allowed values: disabled, preferred, required, verify_ca, verify_identity (required)
      --ssl-server-name string                  SSL server name override
      --tablet-cell string                      Cell where the external tablet runs
      --username string                         Username to connect to the external database (required)
      --wait                                    Wait until the keyspace is ready

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

## pscale keyspace list

```text
List all keyspaces within a branch

Usage:
  pscale keyspace list <database> <branch> [flags]

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

## pscale keyspace show

```text
Show a keyspace within a branch

Usage:
  pscale keyspace show <database> <branch> <keyspace> [flags]

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

## pscale keyspace delete

```text
Delete a keyspace from a branch

Usage:
  pscale keyspace delete <database> <branch> <keyspace> [flags]

Aliases:
  delete, rm

Flags:
      --force   Delete a keyspace without confirmation
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

## pscale keyspace settings

The `pscale keyspace settings` help fence below is exact output from the official, checksum-verified PlanetScale CLI v0.341.0 macOS arm64 release binary after normalizing only trailing whitespace. The archive SHA-256 is `422dbd3568e62c2167c0aa629658ce31cedd5a3595d8c801eff88f7653bc4323`.

```text
Show the settings for a keyspace

Usage:
  pscale keyspace settings <database> <branch> <keyspace> [flags]

Flags:
  -h, --help   help for settings

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

## pscale keyspace update-settings

```text
Update the settings for a keyspace

Usage:
  pscale keyspace update-settings <database> <branch> <keyspace> [flags]

Flags:
      --disk-scaling-strategy string                         The disk scaling strategy (grow, disable, shrink). 'grow' lets dedicated disks grow automatically up to --max-storage; 'disable' turns autoscaling off; 'shrink' recreates disks at --storage and then disables autoscaling. (default "grow")
  -h, --help                                                 help for update-settings
  -i, --interactive                                          Run the command in interactive mode
      --max-rollout int                                      Maximum number of shards to roll out changes to concurrently (1-32). (default 1)
      --max-storage string                                   The maximum size that dedicated disks may autoscale to, in bytes or with a unit such as 200GiB or 1TiB. Must be at least 12 GiB and no smaller than the current disk size. Cannot be raised above the organization default (4 TiB, or 16 TiB for managed tenancy). Read-only while PlanetScale staff have raised it above that default.
      --replication-durability-constraints-strategy string   By default, replication is configured to maximize safety and data integrity. This setting may be relaxed to favor increased performance and reduced replication lag. Options: maximum, dynamic, minimum (default "maximum")
      --storage string                                       The disk size to recreate disks at, in bytes or with a unit such as 200GiB or 1TiB. Must be a multiple of 1 GiB. Only accepted when the disk scaling strategy is shrink, either passed with --disk-scaling-strategy or already set on the keyspace.
      --throttler-enabled                                    Pause schema migrations and VReplication workflows when replication lag rises above the threshold. (default true)
      --throttler-threshold float                            Replication lag in seconds above which migrations and workflows are paused. (default 5)
      --vreplication-batch-replication-events                When enabled, sends fewer queries to MySQL to improve performance.
      --vreplication-enable-noblob-binlog-mode               When enabled, omits changed BLOB and TEXT columns from replication events, which reduces binlog sizes. (default true)
      --vreplication-optimize-inserts                        When enabled, skips sending INSERT events for rows that have yet to be replicated. (default true)

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

## pscale database regions

The help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.333.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
List regions available to a database

Usage:
  pscale database regions [command]

Available Commands:
  list        List regions available to a database

Flags:
  -h, --help   help for regions

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

Use "pscale database regions [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale database regions list

```text
List regions available to a database

Usage:
  pscale database regions list <database> [flags]

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

## pscale database read-only-regions

The help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.333.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
List read-only regions for a database's default branch.

This command is only supported for Vitess databases.

Usage:
  pscale database read-only-regions [command]

Available Commands:
  list        List read-only regions for a database

Flags:
  -h, --help   help for read-only-regions

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

Use "pscale database read-only-regions [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale database read-only-regions list

```text
List read-only regions for a database

Usage:
  pscale database read-only-regions list <database> [flags]

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

## pscale shell

The help fence below is exact output from the official, checksum-verified PlanetScale CLI v0.332.0 macOS arm64 release binary with `NO_COLOR=1`, after normalizing only trailing whitespace. The archive SHA-256 is `61eadf71c9d5e6423587fbf01fd698800d8a944775a06519a1c2ac38fcb89287`.

```text
Open a shell instance to a database and branch

Usage:
  pscale shell [database] [branch] [db-name] [flags]

Examples:
The shell subcommand opens a secure shell instance to your database.

For MySQL databases, it uses the MySQL command-line client ("mysql").
For Postgres databases, it uses the Postgres command-line client ("psql").

By default, if no branch names are given and there is only one branch, it
automatically opens a shell to that branch:

  pscale shell mydatabase

If there are multiple branches for the given database, you'll be prompted to
choose one. To open a shell instance to a specific branch, pass the branch as a
second argument:

  pscale shell mydatabase mybranch

For Postgres databases, you can optionally specify the logical database
to connect to using --db-name (or as a third argument):

  pscale shell production main --db-name my_db
  pscale shell production main my_db

Flags:
      --db-name string              Postgres logical database name to connect to (default: postgres). Only supported for Postgres databases.
  -h, --help                        help for shell
      --local-addr string           Local address to bind and listen for connections. By default the proxy binds to 127.0.0.1 with a random port.
      --org string                  The organization for the current user
      --remote-addr hostname:port   PlanetScale Database remote network address. By default the remote address is populated automatically from the PlanetScale API. (format: hostname:port)
      --replica                     When enabled, the password will route all reads to the branch's primary replicas and all read-only regions.
      --role string                 Role defines the access level, allowed values are: reader, writer, readwriter, admin. Defaults to 'reader' for replica passwords, otherwise defaults to 'admin'.
      --router string               Connect through the named router group. Only supported for Neki databases.

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

## pscale size cluster list

The help fence below is exact output from the official, checksum-verified PlanetScale CLI v0.337.0 macOS arm64 release binary with `NO_COLOR=1`, after normalizing only trailing whitespace. The archive SHA-256 is `4660b4606d0232076b7e54166d15e68e3030d59c2ae22b8b1c47677e506521d7`.

```text
List the sizes that are available for a PlanetScale database. By default, shows all clusters for all engines. Use --engine to filter by a specific engine type.

Usage:
  pscale size cluster list [flags]

Aliases:
  list, ls

Flags:
      --engine string   Filter cluster sizes by database engine. Supported values: mysql, postgresql, neki. If not specified, shows all clusters for all engines.
      --external        view cluster sizes for external keyspaces
  -h, --help            help for list
      --metal           view cluster sizes and rates for clusters with metal storage
      --region string   view cluster sizes and rates for a specific region

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
