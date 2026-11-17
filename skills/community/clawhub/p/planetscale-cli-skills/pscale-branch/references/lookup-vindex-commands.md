# Lookup Vindex command reference

All help fences below were re-captured from the official, checksum-verified PlanetScale CLI v0.339.0 macOS arm64 release binary after normalizing only trailing whitespace. The archive SHA-256 is `1e396701709cd49d1d1cccca252e2bd81f224b2830ca189a84a16983bde182e8`.

## pscale branch vtctl lookup-vindex

```text
Manage Lookup Vindex operations

Usage:
  pscale branch vtctl lookup-vindex [command]

Available Commands:
  cancel      Cancel a Lookup Vindex creation
  complete    Complete a Lookup Vindex creation
  create      Create a Lookup Vindex
  externalize Externalize a Lookup Vindex
  internalize Internalize a Lookup Vindex
  show        Show details of a Lookup Vindex

Flags:
  -h, --help   help for lookup-vindex

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

Use "pscale branch vtctl lookup-vindex [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch vtctl lookup-vindex create

```text
Create a Lookup Vindex

Usage:
  pscale branch vtctl lookup-vindex create <database> <branch> [flags]

Flags:
      --cells strings                      Cells to replicate from (comma-separated)
      --continue-after-copy-with-owner     Keep the backfill workflow running after the copy phase when the vindex has an owner (default true)
  -h, --help                               help for create
      --ignore-nulls                       Ignore null values
      --keyspace string                    Keyspace of the owner table, where the lookup vindex is defined
      --name string                        Name of the Lookup Vindex (required)
      --table-keyspace string              Keyspace where the lookup table and its backfill workflow are created (required)
      --table-name string                  Name of the lookup table
      --table-owner string                 Owner table name
      --table-owner-columns strings        Owner table columns (comma-separated)
      --table-vindex-type string           Vindex type on the owner table
      --tablet-types strings               Tablet types to replicate from (comma-separated)
      --tablet-types-in-preference-order   Use tablet types in preference order
      --type string                        Type of the vindex

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

## pscale branch vtctl lookup-vindex show

```text
Show details of a Lookup Vindex

Usage:
  pscale branch vtctl lookup-vindex show <database> <branch> [flags]

Flags:
  -h, --help                    help for show
      --name string             Name of the Lookup Vindex (required)
      --table-keyspace string   Keyspace where the lookup table and its workflow live (required)

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

## pscale branch vtctl lookup-vindex externalize

```text
Externalize a Lookup Vindex

Usage:
  pscale branch vtctl lookup-vindex externalize <database> <branch> [flags]

Flags:
      --delete                  Delete the workflow after externalizing
  -h, --help                    help for externalize
      --keyspace string         Keyspace of the owner table, where the lookup vindex is defined
      --name string             Name of the Lookup Vindex (required)
      --table-keyspace string   Keyspace where the lookup table and its workflow live (required)

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

## pscale branch vtctl lookup-vindex internalize

```text
Internalize a Lookup Vindex

Usage:
  pscale branch vtctl lookup-vindex internalize <database> <branch> [flags]

Flags:
  -h, --help                    help for internalize
      --keyspace string         Keyspace of the owner table, where the lookup vindex is defined
      --name string             Name of the Lookup Vindex (required)
      --table-keyspace string   Keyspace where the lookup table and its workflow live (required)

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

## pscale branch vtctl lookup-vindex cancel

```text
Cancel a Lookup Vindex creation

Usage:
  pscale branch vtctl lookup-vindex cancel <database> <branch> [flags]

Flags:
  -h, --help                    help for cancel
      --name string             Name of the Lookup Vindex (required)
      --table-keyspace string   Keyspace where the lookup table and its workflow live (required)

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

## pscale branch vtctl lookup-vindex complete

```text
Complete a Lookup Vindex creation

Usage:
  pscale branch vtctl lookup-vindex complete <database> <branch> [flags]

Flags:
  -h, --help                    help for complete
      --keyspace string         Keyspace of the owner table, where the lookup vindex is defined
      --name string             Name of the Lookup Vindex (required)
      --table-keyspace string   Keyspace where the lookup table and its workflow live (required)

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
