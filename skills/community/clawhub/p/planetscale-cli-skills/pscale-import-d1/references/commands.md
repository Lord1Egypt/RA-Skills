## pscale import

All help fences below are exact output from the official, checksum-verified PlanetScale CLI v0.324.0 macOS arm64 release binary after normalizing only trailing whitespace; all nine surfaces were re-verified line-for-line unchanged against the checksum-verified v0.339.0 binary. The v0.339.0 archive SHA-256 is `1e396701709cd49d1d1cccca252e2bd81f224b2830ca189a84a16983bde182e8`.

```text
Import databases from external sources into PlanetScale Postgres.

Available sources:
  d1  Import from Cloudflare D1 using an offline SQLite export

Usage:
  pscale import [command]

Available Commands:
  d1          Import Cloudflare D1 into PlanetScale Postgres

Flags:
  -h, --help         help for import
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

Use "pscale import [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale import d1

```text
Offline import from Cloudflare D1 (SQLite) to PlanetScale Postgres.

Export your D1 database with wrangler (wrangler d1 export <name> --remote --output ./d1-export.sql),
lint the dump, then start the import (use --dry-run to preview).
All commands support --format json for machine-readable output.

Branch-scoped commands use the same positional form as other PlanetScale CLI commands:
  pscale import d1 start <database> [branch] --input ./d1-export.sql
Org comes from your pscale config (pscale org).

Usage:
  pscale import d1 [command]

Available Commands:
  complete       Mark a D1 migration as complete in local state
  convert-schema Convert SQLite schema in a D1 export to PostgreSQL DDL
  doctor         Check prerequisites for D1 migration
  lint           Analyze a D1 SQL export for migration issues
  start          Start importing a D1 export (lint + plan, then load)
  status         Show local migration state
  verify         Verify D1 import (row counts, sequences, coercion, content checks)

Flags:
  -h, --help   help for d1

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

Use "pscale import d1 [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale import d1 doctor

```text
Check prerequisites for D1 migration

Usage:
  pscale import d1 doctor [flags]

Flags:
  -h, --help   help for doctor

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

## pscale import d1 lint

```text
Analyze a D1 SQL export for migration issues

Usage:
  pscale import d1 lint [flags]

Examples:
  pscale import d1 lint --input ./d1-export.sql --format json

Flags:
  -h, --help           help for lint
      --input string   Path to D1 SQL export (required)

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

## pscale import d1 convert-schema

```text
Convert SQLite schema in a D1 export to PostgreSQL DDL

Usage:
  pscale import d1 convert-schema [flags]

Flags:
  -h, --help            help for convert-schema
      --input string    Path to D1 SQL export (required)
      --output string   Output PostgreSQL schema file

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

## pscale import d1 start

```text
Runs lint and builds an import plan, then loads data into PlanetScale Postgres.
Requires pgloader on PATH — run import d1 doctor to verify prerequisites.

Use --dry-run to lint and save migration state without touching Postgres.

Usage:
  pscale import d1 start <database> [branch] [flags]

Examples:
  # Preview lint + plan and get a migration ID
  pscale import d1 start mydb --input ./d1-export.sql --dry-run --format json

  # Run the import on a specific branch (human TTY prompts to confirm)
  pscale import d1 start mydb dev --input ./d1-export.sql --method pgloader --format json

Flags:
      --dbname string         Destination PostgreSQL database name (default "postgres")
      --dry-run               Lint and build import plan without loading Postgres
      --force                 Skip confirmation prompt
  -h, --help                  help for start
      --input string          Path to D1 SQL export (required)
      --method string         Import method: pgloader (≥1GB) or psql (<1GB; schema via psql, data via pgloader)
      --migration-id string   Existing migration ID from a prior start --dry-run

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

## pscale import d1 status

```text
Show local migration state

Usage:
  pscale import d1 status <database> [branch] [flags]

Examples:
  pscale import d1 status mydb --migration-id abc123

Flags:
  -h, --help                  help for status
      --migration-id string   Migration ID (required)

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

## pscale import d1 verify

```text
Verify D1 import (row counts, sequences, coercion, content checks)

Usage:
  pscale import d1 verify <database> [branch] [flags]

Examples:
  pscale import d1 verify mydb --migration-id abc123 --input ./d1-export.sql
  pscale import d1 verify mydb dev --migration-id abc123 --input ./d1-export.sql --format json

Flags:
      --dbname string         Destination PostgreSQL database name (default "postgres")
  -h, --help                  help for verify
      --input string          Path to original D1 SQL export
      --migration-id string   Migration ID from plan/import (required)
      --sqlite string         Path to local SQLite file for source counts

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

## pscale import d1 complete

```text
Mark a D1 migration as complete in local state

Usage:
  pscale import d1 complete <database> [branch] [flags]

Aliases:
  complete, teardown

Examples:
  pscale import d1 complete mydb --migration-id abc123
  pscale import d1 complete mydb --migration-id abc123 --format json

Flags:
      --force                 Skip confirmation prompt
  -h, --help                  help for complete
      --migration-id string   Migration ID (required)

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
