Create, list, show, update, renew, and delete branch passwords.

Unless noted otherwise, help fences below are exact output from the official, checksum-verified PlanetScale CLI v0.324.0 macOS arm64 release binary after normalizing only trailing whitespace. Role surfaces are included because Postgres and Neki branches use roles instead of Vitess passwords.

For the default-role missing-credentials refresh, the complete `pscale role` parent, `default`, `reset-default`, and `list` help fences below were re-executed and verified line-for-line unchanged against the official PlanetScale CLI v0.347.0 macOS arm64 release binary (published archive SHA-256 `7f4dc8dbda90b5a7591c9ec07c0914e7eac378b0f352d7c661c71b2154edec5d`). Only trailing whitespace was normalized. These unchanged fences retain their original capture provenance; the new human/JSON error behavior is documented in [../SKILL.md](../SKILL.md), not in help flags. The `get` fence was subsequently recaptured at v0.350.0 and has its own adjacent attribution. Other fences are not covered by this re-verification.

## pscale password

```text
Create, list, update, and delete branch passwords.

This command is only supported for Vitess databases.

Usage:
  pscale password [command]

Available Commands:
  create      Create password to access a branch's data
  delete      Delete a branch password
  list        List all passwords of a database
  renew       Renew a branch password
  show        Show a branch password
  update      Update a branch password's name or IP restrictions

Flags:
  -h, --help         help for password
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

Use "pscale password [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale password create

```text
Create password to access a branch's data

Usage:
  pscale password create <database> <branch> <name> [flags]

Aliases:
  create, p

Flags:
  -h, --help                      help for create
      --read-only-region string   Create a password scoped to a Vitess read-only region (region slug, display name, or id). List regions with: pscale keyspace read-only-regions <database> <branch> <keyspace>.
      --replica                   When enabled, the password will route all reads to the branch's primary replicas and all read-only regions.
      --role string               Role defines the access level, allowed values are: reader, writer, readwriter, admin. Defaults to 'reader' for replica and read-only region passwords, otherwise defaults to 'admin'.
      --ttl duration              TTL defines the time to live for the password. Durations such as "30m", "24h", or bare integers such as "3600" (seconds) are accepted. The default TTL is 0s, which means the password will never expire. (default 0s)

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

`--read-only-region` and `--replica` are mutually exclusive. A region-scoped password defaults to `reader`, requires the selected region to be ready, and is labeled as a read-only-region credential in create output.

## pscale password list

```text
List all passwords of a database

Usage:
  pscale password list <database> [branch] [flags]

Aliases:
  list, ls

Flags:
  -h, --help            help for list
      --name string     Filter passwords by name using a substring match
      --page int        Page number to fetch
      --per-page int    Number of results per page (default 100)
      --status string   Filter passwords by status (active, renewable, or expired)
  -w, --web             List passwords in your web browser.

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

## pscale password show

```text
Show a branch password.

Only metadata is returned. The password itself is shown once, when it is
created or renewed, and cannot be retrieved afterwards.

Usage:
  pscale password show <database> <branch> [<password-id>] [flags]

Flags:
  -h, --help          help for show
      --name string   Show password by name instead of ID

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

## pscale password update

```text
Update a branch password's name or IP restrictions.

This does not change the password itself. To rotate a password, create a new
one and delete the old one.

Usage:
  pscale password update <database> <branch> [<password-id>] [flags]

Examples:
  pscale password update mydb main pscale_pw_xxx --new-name reporting
  pscale password update mydb main --name reporting --cidrs 10.0.0.0/8,192.168.1.1/32
  pscale password update mydb main --name reporting --cidrs ""

Flags:
      --cidrs strings     Replace the IP addresses and CIDR ranges allowed to use this password. Pass an empty value to remove all restrictions
  -h, --help              help for update
      --name string       Update password by name instead of ID
      --new-name string   New name for the password

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

## pscale password renew

```text
Renew a branch password

Usage:
  pscale password renew <database> <branch> <password-id> [flags]

Flags:
  -h, --help   help for renew

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

## pscale password delete

```text
Delete a branch password

Usage:
  pscale password delete <database> <branch> [<password-id>] [flags]

Aliases:
  delete, rm

Flags:
      --force         Delete a password without confirmation
  -h, --help          help for delete
      --name string   Delete password by name instead of ID

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

## pscale role

The role parent and role-create fences were re-verified against the official, checksum-verified PlanetScale CLI v0.337.0 macOS arm64 release binary with `NO_COLOR=1`, after normalizing only trailing whitespace. The archive SHA-256 is `4660b4606d0232076b7e54166d15e68e3030d59c2ae22b8b1c47677e506521d7`. Other role fences without their own capture note remain exact v0.332.0 captures; the current `get` fence has its own v0.350.0 attribution below.

```text
Manage database roles for a Postgres or Neki database branch.

This command is supported for Postgres or Neki databases.

Usage:
  pscale role [command]

Available Commands:
  create        Create a new role for a Postgres or Neki database branch
  default       Show the default postgres role
  delete        Delete a role
  get           Retrieve information about a specific role
  list          List all roles for a Postgres or Neki database branch
  reassign      Reassign objects owned by a role to another role
  renew         Renew a role's expiration
  reset         Reset a role's password
  reset-default Reset the credentials for the default `postgres` role
  update        Update a role's name

Flags:
  -h, --help         help for role
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

Use "pscale role [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale role list

```text
List all roles for a Postgres or Neki database branch

Usage:
  pscale role list <database> <branch> [flags]

Aliases:
  list, ls

Flags:
  -h, --help            help for list
      --name string     Filter roles by name using a substring match
      --page int        Page number to fetch
      --per-page int    Number of results per page (default 100)
      --status string   Filter roles by status (active, renewable, disabled, or expired)
  -w, --web             List roles in your web browser.

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

## pscale role get

Compatibility: `role show` aliases canonical `role get` starting with PlanetScale CLI v0.350.0; it takes the same arguments/flags and can return sensitive credentials. The CLI-generated role `database_url` uses `sslmode=verify-full&sslrootcert=system` starting with that release, including Postgres/Neki targets and PgBouncer URLs. The shared URL builder also serves role creation/reset output. Check `pscale version` before relying on these behaviors; use canonical `get` on an older CLI, and do not treat absence of `sslrootcert` in older output as corruption.

Client compatibility is separate from the CLI minimum. Libpq 16+ supports the special `system` value: it selects the SSL implementation's trusted CA roots (platform/OpenSSL configuration still matters), not a literal file named `system`. Non-libpq drivers have their own version-specific behavior; some instead try to read a file named `system`. Before reusing a URL, verify support in the actual consumer. For any consumer that does not support `sslrootcert=system`, keep `sslmode=verify-full` and replace `system` with an explicit approved trusted CA-bundle path supported by that consumer, or upgrade to verified support. Stop if certificate and hostname verification cannot be established; never drop TLS parameters or log the returned URL. See the [PostgreSQL 16 sslrootcert contract](https://www.postgresql.org/docs/16/libpq-connect.html#LIBPQ-CONNECT-SSLROOTCERT), immutable [node-postgres parser example](https://github.com/brianc/node-postgres/blob/95d7e620ef8b51743b4cbca05dd3c3ce858ecea7/packages/pg-connection-string/index.js), [pgx parser example](https://github.com/jackc/pgx/blob/572d7fff326f1befdbf9f36a0c0a2b6661432079/pgconn/config.go), and upstream [role URL builder](https://github.com/planetscale/cli/blob/38ad9f38efba35085dd84b6fa29a2b2c5e5a6964/internal/cmd/role/reset_default.go). These driver examples establish incompatible versions, not a blanket claim about every current driver. For node-postgres, do not casually mix URL TLS parameters with a separate `ssl` object: parsing can replace that object, as the [driver's SSL documentation](https://node-postgres.com/features/ssl#usage-with-connectionstring) explains.

The complete help fence below was captured from the official, checksum-verified PlanetScale CLI v0.350.0 macOS arm64 release binary (archive SHA-256 `aa17d5be045b30665d8ffaaf42159254fe3259186763c47304260af4f6aa56df`). `role show --help` was separately captured and matches canonical `get`. Only terminal padding/trailing whitespace was normalized. The parent, create, default, and reset-default help were re-executed and match their stored fences; their original provenance remains unchanged.

Previous capture note (superseded for this fence): The help fence below is exact output from the official, checksum-verified PlanetScale CLI v0.343.0 macOS arm64 release binary after normalizing only trailing whitespace. The archive SHA-256 is `98672666af6ca95e58a60f51fccebbb75294e428fc37d96ee372cac1b322acfe`.

```text
Retrieve information about a specific role

Usage:
  pscale role get <database> <branch> <role-id> [flags]

Aliases:
  get, show

Flags:
      --bouncer string                  Return connection details for a PgBouncer (name). Postgres only.
      --dedicated-read-replica string   Return connection details for a dedicated read replica (name). Postgres only.
  -h, --help                            help for get
      --replica                         Return connection details for a branch replica. On Neki this sets libpq options, not a username suffix.
      --router string                   Return connection details for a Neki router group (name). List routers with: pscale branch router list <database> <branch>.
      --shard string                    Return connection details that pin a Neki shard (name from pscale branch shard list).

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

## pscale role default

```text
Show the default postgres role for a branch.

This does not rotate credentials. Use 'pscale role reset-default' to issue a
new password for the default role.

Usage:
  pscale role default <database> <branch> [flags]

Flags:
  -h, --help   help for default

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

## pscale role reset-default

```text
This command resets the credentials for the default `postgres` role in the database, allowing you to reconfigure access. Any connections using the `postgres` role will need to be updated with the new credentials.

Usage:
  pscale role reset-default <database> <branch> [flags]

Flags:
      --force   Force reset without confirmation
  -h, --help    help for reset-default

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

## pscale role create

```text
Create a new role for a Postgres or Neki database branch

Usage:
  pscale role create <database> <branch> <name> [flags]

Examples:
  # Create a role with admin access
  pscale role create mydb main my-role --inherited-roles postgres

  # Create a role with REPLICATION privilege (requires the postgres inherited role)
  pscale role create mydb main replicator --inherited-roles postgres --with-replication

  # Neki: neki_viewer requires pg_read_all_data; neki_operator requires postgres
  pscale role create mydb main viewer --inherited-roles neki_viewer,pg_read_all_data
  pscale role create mydb main operator --inherited-roles neki_operator,postgres

Flags:
  -h, --help                     help for create
      --inherited-roles string   Comma-separated list of roles to inherit privileges from. Postgres: pg_read_all_data (read), pg_write_all_data (write), postgres (admin). Neki also accepts neki_viewer (requires pg_read_all_data) and neki_operator (requires postgres).
      --ttl duration             TTL defines the time to live for the role. Durations such as "30m", "24h", or bare integers such as "3600" (seconds) are accepted. The default TTL is 0s, which means the role will never expire. (default 0s)
      --with-replication         When enabled, the role is created with REPLICATION privilege for logical replication. Requires --inherited-roles to include 'postgres'.

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

## pscale role update

```text
Update a role's name

Usage:
  pscale role update <database> <branch> <role-id> [flags]

Flags:
  -h, --help          help for update
      --name string   New name for the role (required)

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

## pscale role renew

```text
Renew a role's expiration

Usage:
  pscale role renew <database> <branch> <role-id> [flags]

Flags:
  -h, --help   help for renew

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

## pscale role reset

```text
Reset a role's password

Usage:
  pscale role reset <database> <branch> <role-id> [flags]

Flags:
      --force   Reset password without confirmation
  -h, --help    help for reset

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

## pscale role delete

```text
Delete a role

Usage:
  pscale role delete <database> <branch> <role-id> [flags]

Aliases:
  delete, rm

Flags:
      --force              Delete a role without confirmation
  -h, --help               help for delete
      --successor string   Role to transfer ownership to before deletion. Usually 'postgres'.

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

## pscale role reassign

```text
Reassign objects owned by a role to another role

Usage:
  pscale role reassign <database> <branch> <role-id> [flags]

Examples:
  # List roles and copy the source role's id value
  pscale role list mydb main --org my-org

  # Reassign objects owned by role tq8hnwl1mlty to successor role pscale_api_stqrbvtoy367
  pscale role reassign mydb main tq8hnwl1mlty --successor pscale_api_stqrbvtoy367 --org my-org

Flags:
      --force              Reassign objects without confirmation
  -h, --help               help for reassign
      --successor string   Successor role to transfer ownership to (required) (required)

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
