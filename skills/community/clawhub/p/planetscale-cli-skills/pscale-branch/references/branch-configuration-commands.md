# Branch extension and parameter commands

The complete `pscale branch parameters list` fence was re-executed and verified line-for-line unchanged against the official PlanetScale CLI v0.346.0 macOS arm64 release binary for the parameter-output refresh. Its original v0.344.0 capture provenance is retained below; this re-verification applies to the `parameters list` fence only. Published archive SHA-256: `6e8a3f064f45ad29f187ba3dda24ad3a45328bd11a200b89c200d06bdc5c3a6b`; only trailing whitespace was normalized. Related branch/parameters parents and resize/status help were also unchanged. The new `REQUIRES UPDATE` table column and nullable-string JSON contract are output behavior, not new help flags; see the parameter workflow in [../SKILL.md](../SKILL.md). Release history is in `VERSION`.

All help fences below are complete output from the official, checksum-verified PlanetScale CLI v0.344.0 macOS arm64 binary with `NO_COLOR=1`, normalizing only trailing whitespace. Archive SHA-256: `1b59b271590d9b49dd52aafbb0e5c0cd788b44c00a5627d6487cd0d18815cf53`. Other branch parent and capacity help surfaces are in [commands.md](commands.md).

## pscale branch extensions enable

```text
Enable an extension on a Postgres branch.

This queues an asynchronous branch change request and may restart the
database. Only extensions marked "can enable" in 'pscale branch extensions
list' can be toggled.

Usage:
  pscale branch extensions enable <database> <branch> <extension> [flags]

Flags:
  -h, --help                    help for enable
      --wait                    Wait for the change request to complete before returning.
      --wait-timeout duration   Maximum time to wait for the change request to complete with --wait. (default 10m0s)

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

## pscale branch extensions disable

```text
Disable an extension on a Postgres branch.

This queues an asynchronous branch change request and may restart the
database. Only extensions marked "can enable" in 'pscale branch extensions
list' can be toggled.

Usage:
  pscale branch extensions disable <database> <branch> <extension> [flags]

Flags:
  -h, --help                    help for disable
      --wait                    Wait for the change request to complete before returning.
      --wait-timeout duration   Maximum time to wait for the change request to complete with --wait. (default 10m0s)

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

## pscale branch parameters list

```text
List the configuration parameters of a Postgres branch, including their
current and default values. Values from a queued change request are reflected.

To change parameters, use 'pscale branch resize <database> <branch> --parameters namespace.name=value'.

Usage:
  pscale branch parameters list <database> <branch> [flags]

Flags:
      --extension          Only show parameters that configure an extension (--extension=false hides them).
  -h, --help               help for list
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

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch vtgate parameters

```text
List the VTGate parameters of a Vitess branch, including their current and default values.

To change parameters, use 'pscale branch vtgate update <database> <branch> --parameters vtgate.name=value'.

Usage:
  pscale branch vtgate parameters <database> <branch> [flags]

Aliases:
  parameters, params

Flags:
  -h, --help   help for parameters

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

## pscale branch vtgate update

```text
Change VTGate parameters on a Vitess branch. Pass each parameter as vtgate.name=value, and pass --reset vtgate.name to set a parameter back to its default.

The change is rolled out to the branch's VTGates. Use 'pscale branch vtgate changes list' to follow the rollout. To change the size or number of VTGates, use 'pscale branch vtgate resize'.

Usage:
  pscale branch vtgate update <database> <branch> [flags]

Examples:
  pscale branch vtgate update <database> <branch> \
    --parameters vtgate.max_memory_rows=500000 \
    --parameters vtgate.query-timeout=30000

  pscale branch vtgate update <database> <branch> --reset vtgate.query-timeout

Flags:
  -h, --help                     help for update
      --parameters stringArray   Set a parameter as vtgate.name=value (e.g. vtgate.max_memory_rows=500000). Repeatable. Use 'pscale branch vtgate parameters' to see available parameters.
      --reset stringArray        Set a parameter back to its default, as vtgate.name (e.g. vtgate.query-timeout). Repeatable.

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

## pscale branch vtgate changes

```text
Manage VTGate parameter changes for a Vitess branch

Usage:
  pscale branch vtgate changes [command]

Available Commands:
  cancel      Cancel a pending VTGate parameter change for a Vitess branch
  list        List VTGate parameter changes for a Vitess branch
  show        Show a VTGate parameter change for a Vitess branch

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

Use "pscale branch vtgate changes [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch vtgate changes list

```text
List VTGate parameter changes for a Vitess branch

Usage:
  pscale branch vtgate changes list <database> <branch> [flags]

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

## pscale branch vtgate changes show

```text
Show a VTGate parameter change for a Vitess branch

Usage:
  pscale branch vtgate changes show <database> <branch> <change-id> [flags]

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

## pscale branch vtgate changes cancel

```text
Cancel a pending VTGate parameter change for a Vitess branch

Usage:
  pscale branch vtgate changes cancel <database> <branch> <change-id> [flags]

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

Aliases re-run and verified identical to their canonical complete help: `branch extensions ls`, `branch params`, `branch vtgate params`, `branch vtgate changes ls`, and `branch vtgate changes get`.
