## pscale sql

The help fence below is exact output from the official, checksum-verified PlanetScale CLI v0.332.0 macOS arm64 release binary with `NO_COLOR=1`, after normalizing only trailing whitespace. The archive SHA-256 is `61eadf71c9d5e6423587fbf01fd698800d8a944775a06519a1c2ac38fcb89287`.

```text
Execute a single SQL query against a database branch using ephemeral credentials.

Use --format json for machine-readable output. This command is intended for agents and scripts;
for interactive sessions use pscale shell instead.

Access flags match pscale shell: --role (reader, writer, readwriter, admin) and --replica.
Unlike shell, the default role is reader. Pass --role admin (or writer/readwriter) for writes.

Destructive SQL containing DELETE, DROP, or TRUNCATE is blocked unless --force is passed.
Agents must ask the user for approval before using --force.

MySQL (Vitess) databases use the primary keyspace by default (same as pscale shell -D @primary).
Pass --keyspace when targeting a specific keyspace in a multi-keyspace database. A keyspace may
include a shard and tablet type (mykeyspace/-80, mykeyspace/-80@replica) to pin the connection to
one shard; enumerate shards with SHOW VITESS_SHARDS.

Postgres or Neki databases use --dbname (default postgres).

Human output prints rows as a table. Pass --vertical (or end the query with \G,
like the mysql client) to print one column per line, which is easier to read for
wide results such as SHOW REPLICA STATUS.

Place flags after positional arguments (see Usage). --org is required:

  pscale sql <database> <branch> --org <org> --format json --query "SELECT 1"

Usage:
  pscale sql <database> <branch> [flags]

Examples:
  # Read query (default reader role)
  pscale sql <database> <branch> --org <org> --format json --query "SELECT 1"

  # Read from replica
  pscale sql <database> <branch> --org <org> --format json --replica --query "SELECT 1"

  # MySQL — keyspace optional (@primary default)
  pscale sql <database> <branch> --org <org> --format json --keyspace <keyspace> --query "SELECT 1"

  # Vertical output for wide rows (--vertical, or end the query with \G)
  pscale sql <database> <branch> --org <org> --replica --query "SHOW REPLICA STATUS\G"

Flags:
      --dbname string     Postgres or Neki database name (default "postgres")
      --force             Allow destructive SQL (DELETE, DROP, TRUNCATE). Only use after the user explicitly approves.
  -h, --help              help for sql
      --keyspace string   Vitess keyspace, optionally with a shard and tablet type (e.g. mykeyspace, mykeyspace/-80, mykeyspace/-80@replica). List shards with --query "SHOW VITESS_SHARDS". Defaults to @primary, same as pscale shell.
      --org string        The organization for the current user
      --query string      SQL query to execute (required)
      --replica           When enabled, the password will route all reads to the branch's primary replicas and all read-only regions.
      --role string       Role defines the access level, allowed values are: reader, writer, readwriter, admin. Defaults to reader (use --role admin for writes).
      --vertical          Print each row vertically, one column per line. Same as ending the query with \G in the mysql client.

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
