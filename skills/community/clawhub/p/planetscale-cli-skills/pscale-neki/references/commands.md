Unless a later adjacent capture note applies, exact help output below was captured from the official, checksum-verified PlanetScale CLI v0.332.0 macOS arm64 release binary with `NO_COLOR=1` (archive SHA-256 `61eadf71c9d5e6423587fbf01fd698800d8a944775a06519a1c2ac38fcb89287`) after normalizing only trailing whitespace. The branch-wide change-request surfaces are separately identified as v0.334.0 captures.

For the parameter-output refresh, the complete `config-profile`, `sidecar`, and `admin` parent, `parameters`, `show`, and `update` fences below were re-executed and verified line-for-line unchanged against the official PlanetScale CLI v0.346.0 macOS arm64 release binary. All three `params` aliases were independently executed and matched their canonical parameter help. Published archive SHA-256: `6e8a3f064f45ad29f187ba3dda24ad3a45328bd11a200b89c200d06bdc5c3a6b`; only trailing whitespace was normalized. The new `REQUIRES UPDATE` column and nullable-string JSON field are output behavior, not new help flags; see [../SKILL.md](../SKILL.md). Other fences retain their earlier provenance; release history is in `VERSION`.

Read-only-replica refresh verification used the official PlanetScale CLI v0.347.0 macOS arm64 release binary (published archive SHA-256 `7f4dc8dbda90b5a7591c9ec07c0914e7eac378b0f352d7c661c71b2154edec5d`), normalizing only trailing whitespace. The `pscale branch config-profile create` and `update` fences have new capture provenance directly above each block, superseding the older update verification in the introduction. The complete `pscale branch config-profile` parent, list, show, default, set-default, parameters (including the `params` alias), and `pscale branch config-profile changes` parent/list/show/cancel fences were re-executed and are unchanged. The separate `pscale branch changes` parent/list/show/cancel fences were also re-executed and are unchanged; they retain the original v0.334.0 capture provenance below. Only the two affected complete fences were replaced. Role re-verification is recorded beside the stored fences in [../../pscale-password/references/commands.md](../../pscale-password/references/commands.md).

Of the 61 complete Neki help fences in this file, the 60 other than `data-topology get` retain their line-for-line unchanged verification against the official, checksum-verified v0.348.0 macOS arm64 binary (archive SHA-256 `528bb8951d4d93f7ca869850787163f5d49ba405acc58d4146b9b3427e83b7e7`), after trailing-whitespace normalization. The `data-topology get` fence was subsequently recaptured at v0.350.0 with its own attribution below and is not covered by this unchanged-output claim. The `config-profile`, legacy `sidecar`, and `admin` `params` aliases were also executed. `branch sidecar` is deprecated and absent from branch-parent help, although its explicit help remains available. These fences are stdout help, not a claim that operational deprecation warnings or resource output are unchanged. Prefer `config-profile update --parameters sidecar.<name>=<value>` for new sidecar-setting workflows; see [../SKILL.md](../SKILL.md). Original unchanged fence provenance is retained below.

## Role client compatibility

`role show` and CLI-generated role URLs containing `sslmode=verify-full&sslrootcert=system` require PlanetScale CLI v0.350.0 or newer. Check `pscale version` before relying on either behavior; use canonical `role get` on older CLIs and do not treat an older URL without `sslrootcert` as malformed. Libpq 16+ supports the special `system` value; non-libpq driver support is version-specific. For any consumer that does not support it, retain `sslmode=verify-full` with an explicit approved trusted CA-bundle path, or upgrade to verified support. Never disable certificate or hostname verification or expose the URL. This minimum local contract ships with selective Neki installs; detailed driver examples and the immutable role URL source are in [pscale-password's reference](../../pscale-password/references/commands.md#pscale-role-get) when that separate skill is available.

## pscale branch changes

The four branch-wide change-request help fences below are exact output from the official, checksum-verified PlanetScale CLI v0.334.0 macOS arm64 release binary after normalizing only trailing whitespace. The archive SHA-256 is `16b156fa969edb36ec6ebde28b40165cbeb928ae07ba97110d3359fb588245bd`.

```text
List, show, and cancel change requests across a Neki branch.

This includes admin, cluster, configuration profile, router, and sidecar
changes. Per-resource commands still exist under admin, config-profile,
router, and sidecar. This command is only supported for Neki databases.

Usage:
  pscale branch changes [command]

Aliases:
  changes, neki-changes

Available Commands:
  cancel      Cancel a pending Neki branch change request
  list        List change requests for a Neki branch
  show        Show a Neki branch change request

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

Use "pscale branch changes [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch changes list

```text
List change requests for a Neki branch

Usage:
  pscale branch changes list <database> <branch> [flags]

Aliases:
  list, ls

Flags:
      --completed-at string   Only show changes completed in this time range
  -h, --help                  help for list
      --page int              Page number to fetch
      --per-page int          Number of results per page (default 100)
      --period string         Only show changes from this period
      --state strings         Filter by state (repeat or comma-separate)
      --target-id string      Filter by target ID. Requires --target-type
      --target-type strings   Filter by target type: admin, cluster, config-profile, router, or sidecar

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

## pscale branch changes show

```text
Show a Neki branch change request

Usage:
  pscale branch changes show <database> <branch> <change-id> [flags]

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

## pscale branch changes cancel

```text
Cancel a pending Neki branch change request

Usage:
  pscale branch changes cancel <database> <branch> <change-id> [flags]

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

## pscale branch data-topology

```text
Fetch or update the data topology of a Neki branch

Usage:
  pscale branch data-topology [command]

Available Commands:
  get         Show the data topology of a Neki branch
  ls          Show the relationships in a Neki branch's data topology
  update      Update the data topology of a Neki branch from standard input

Flags:
  -h, --help   help for data-topology

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

Use "pscale branch data-topology [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch data-topology get

Compatibility: `data-topology show` aliases `data-topology get` starting with PlanetScale CLI v0.350.0. Both read the same cached Neki topology with the same refresh/staleness semantics; neither replaces `data-topology update`. Unknown non-runnable subcommands now point to `pscale branch data-topology --help`, including JSON `UNKNOWN_COMMAND` next steps; inspect help rather than automatically executing operational suggestions.

This complete fence has been recaptured from the official, checksum-verified v0.350.0 macOS arm64 binary (archive SHA-256 `aa17d5be045b30665d8ffaaf42159254fe3259186763c47304260af4f6aa56df`), normalizing only terminal padding/trailing whitespace. It replaces both the introductory v0.332.0 capture attribution and the v0.348.0 unchanged-output verification for `data-topology get`; neither claim covers this current fence. The `show` alias was separately captured and matches canonical `get`; the data-topology and branch parent help were also captured. The stored data-topology parent remains unchanged. Other fences retain their original provenance.

```text
Show the data topology of a Neki branch

Usage:
  pscale branch data-topology get <database> <branch> [flags]

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

## pscale branch data-topology ls

```text
Show the relationships in a Neki branch's data topology

Usage:
  pscale branch data-topology ls <database> <branch> [flags]

Examples:
  pscale branch data-topology ls mydb main --org my-org --format json
  pscale branch data-topology ls mydb main --org my-org --shards --format json

Flags:
  -h, --help     help for ls
      --shards   Group data by the physical shards that host it

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

## pscale branch data-topology update

```text
Update the data topology of a Neki branch from standard input

Usage:
  pscale branch data-topology update <database> <branch> [flags]

Examples:
  pscale branch data-topology update mydb main --org my-org --format json < data-topology.json

Flags:
  -h, --help   help for update

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

## pscale branch shard

```text
Manage shards for a Neki database branch.

This command is only supported for Neki databases.

Usage:
  pscale branch shard [command]

Available Commands:
  assign      Assign shards to a Neki configuration profile
  create      Create shards in a Neki configuration profile
  delete      Delete a shard from a Neki database branch
  list        List shards for a Neki database branch
  show        Show a shard for a Neki database branch
  update      Update a Neki shard's display name

Flags:
  -h, --help   help for shard

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

Use "pscale branch shard [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch shard list

```text
List shards for a Neki database branch

Usage:
  pscale branch shard list <database> <branch> [flags]

Aliases:
  list, ls

Flags:
      --config-profile string           List shards assigned to this configuration profile
      --exclude-config-profile string   Exclude shards assigned to this configuration profile
  -h, --help                            help for list
      --page int                        Page number to fetch
      --per-page int                    Number of results per page (default 100)
  -q, --query string                    Search by shard name, display name, or configuration profile

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

## pscale branch shard show

```text
Show a shard for a Neki database branch

Usage:
  pscale branch shard show <database> <branch> <shard-id> [flags]

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

## pscale branch shard create

```text
Create shards in a Neki configuration profile

Usage:
  pscale branch shard create <database> <branch> [flags]

Flags:
      --config-profile string   Configuration profile that will host the new shards (required)
      --count int               Number of shards to create (default 1)
  -h, --help                    help for create

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

## pscale branch shard assign

```text
Assign shards to a Neki configuration profile

Usage:
  pscale branch shard assign <database> <branch> <shard-id>... [flags]

Flags:
      --config-profile string   Configuration profile to assign the shards to (required)
  -h, --help                    help for assign

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

## pscale branch shard update

```text
Update a Neki shard's display name

Usage:
  pscale branch shard update <database> <branch> <shard-id> [flags]

Flags:
      --display-name string   New display name; pass an empty string to clear it (required)
  -h, --help                  help for update

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

## pscale branch shard delete

```text
Delete a shard from a Neki database branch

Usage:
  pscale branch shard delete <database> <branch> <shard-id> [flags]

Aliases:
  delete, rm

Flags:
      --force   Delete the shard without confirmation
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

## pscale branch config-profile

```text
Manage configuration profiles for a Neki database branch.

This command is only supported for Neki databases.

Usage:
  pscale branch config-profile [command]

Available Commands:
  changes     Manage changes to a Neki configuration profile
  create      Create a Neki configuration profile
  default     Show the default Neki configuration profile
  delete      Delete a Neki configuration profile
  extensions  List extensions for a Neki configuration profile
  list        List configuration profiles for a Neki branch
  maintenance Run maintenance for one or more Neki configuration profiles
  parameters  List parameters for a Neki configuration profile
  set-default Set the default Neki configuration profile
  show        Show a Neki configuration profile
  update      Update a Neki configuration profile

Flags:
  -h, --help   help for config-profile

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

Use "pscale branch config-profile [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch config-profile list

```text
List configuration profiles for a Neki branch

Usage:
  pscale branch config-profile list <database> <branch> [flags]

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

## pscale branch config-profile show

```text
Show a Neki configuration profile

Usage:
  pscale branch config-profile show <database> <branch> <name> [flags]

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

## pscale branch config-profile create

The complete help fence below is captured from the official, checksum-verified PlanetScale CLI v0.347.0 macOS arm64 binary. Archive SHA-256: `7f4dc8dbda90b5a7591c9ec07c0914e7eac378b0f352d7c661c71b2154edec5d`. Only trailing whitespace was normalized.

```text
Create a Neki configuration profile

Usage:
  pscale branch config-profile create <database> <branch> <name> [flags]

Flags:
      --cluster-size string             Cluster size for shards in the profile
  -h, --help                            help for create
      --max-storage int                 Maximum storage size in bytes for autoscaling
      --min-storage int                 Minimum storage size in bytes
      --postgres-major-version string   PostgreSQL major version
      --postgres-minor-version string   PostgreSQL minor version
      --read-only-replicas int          Number of read-only replicas per shard (0-8; defaults to 0)
      --replicas int                    Number of replicas for shards in the profile
      --storage-autoscaling             Enable storage autoscaling
      --storage-iops int                Storage IOPS
      --storage-throughput int          Storage throughput in MiB/s

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

## pscale branch config-profile update

The complete help fence below is captured from the official, checksum-verified PlanetScale CLI v0.347.0 macOS arm64 binary. Archive SHA-256: `7f4dc8dbda90b5a7591c9ec07c0914e7eac378b0f352d7c661c71b2154edec5d`. Only trailing whitespace was normalized.

```text
Update a Neki configuration profile

Usage:
  pscale branch config-profile update <database> <branch> <name> [flags]

Flags:
      --cluster-size string             New cluster size for shards in the profile
      --extensions strings              Extensions to enable; replaces the current set. Use --extensions= to disable extensions
  -h, --help                            help for update
      --max-storage int                 Maximum storage size in bytes for autoscaling
      --min-storage int                 Minimum storage size in bytes
      --name string                     New name for the configuration profile
      --parameters stringArray          Set a parameter as namespace.name=value; repeatable
      --postgres-major-version string   PostgreSQL major version
      --postgres-minor-version string   PostgreSQL minor version
      --read-only-replicas int          New number of read-only replicas per shard (0-8; 0 removes them)
      --replicas int                    New number of replicas for shards in the profile
      --storage-autoscaling             Enable storage autoscaling
      --storage-iops int                Storage IOPS
      --storage-throughput int          Storage throughput in MiB/s

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

## pscale branch config-profile delete

```text
Delete a Neki configuration profile

Usage:
  pscale branch config-profile delete <database> <branch> <name> [flags]

Aliases:
  delete, rm

Flags:
      --force   Delete the configuration profile without confirmation
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

## pscale branch config-profile default

```text
Show the default Neki configuration profile

Usage:
  pscale branch config-profile default <database> <branch> [flags]

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

## pscale branch config-profile set-default

```text
Set the default Neki configuration profile

Usage:
  pscale branch config-profile set-default <database> <branch> <name> [flags]

Flags:
  -h, --help   help for set-default

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

## pscale branch config-profile parameters

```text
List parameters for a Neki configuration profile

Usage:
  pscale branch config-profile parameters <database> <branch> <name> [flags]

Aliases:
  parameters, params

Flags:
      --extension          Only show extension parameters
  -h, --help               help for parameters
      --internal           Only show internal parameters
      --namespace string   Only show parameters in this namespace

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

## pscale branch config-profile maintenance

```text
Run maintenance for one or more Neki configuration profiles, updating them
to the latest available image.

The upgrade is applied to the replicas first, followed by a switchover from the
old primary to an upgraded replica. That failover leads to a short period of
database unavailability (seconds), and all direct connections to those shards
are terminated.

Use 'pscale branch maintenance run' to maintain every profile on the branch.

Usage:
  pscale branch config-profile maintenance <database> <branch> <name>... [flags]

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

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch config-profile extensions

```text
List extensions for a Neki configuration profile

Usage:
  pscale branch config-profile extensions <database> <branch> <name> [flags]
  pscale branch config-profile extensions [command]

Available Commands:
  disable     Disable an extension for a Neki configuration profile
  enable      Enable an extension for a Neki configuration profile

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

Use "pscale branch config-profile extensions [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch config-profile extensions enable

```text
Enable an extension for a Neki configuration profile

Usage:
  pscale branch config-profile extensions enable <database> <branch> <name> <extension> [flags]

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

## pscale branch config-profile extensions disable

```text
Disable an extension for a Neki configuration profile

Usage:
  pscale branch config-profile extensions disable <database> <branch> <name> <extension> [flags]

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

## pscale branch config-profile changes

```text
Manage changes to a Neki configuration profile

Usage:
  pscale branch config-profile changes [command]

Available Commands:
  cancel      Cancel a pending change to a Neki configuration profile
  list        List changes for a Neki configuration profile
  show        Show a change to a Neki configuration profile

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

Use "pscale branch config-profile changes [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch config-profile changes list

```text
List changes for a Neki configuration profile

Usage:
  pscale branch config-profile changes list <database> <branch> <name> [flags]

Aliases:
  list, ls

Flags:
      --completed-at string   Only show changes completed at this time
  -h, --help                  help for list
      --page int              Page number to fetch
      --per-page int          Number of results per page (default 100)
      --period string         Only show changes from this period

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

## pscale branch config-profile changes show

```text
Show a change to a Neki configuration profile

Usage:
  pscale branch config-profile changes show <database> <branch> <name> <change-id> [flags]

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

## pscale branch config-profile changes cancel

```text
Cancel a pending change to a Neki configuration profile

Usage:
  pscale branch config-profile changes cancel <database> <branch> <name> <change-id> [flags]

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

## pscale branch router

```text
Manage routers for a Neki database branch.

This command is only supported for Neki databases.

Usage:
  pscale branch router [command]

Available Commands:
  changes     Manage changes to a Neki router
  create      Create a router for a Neki database branch
  delete      Delete a router from a Neki database branch
  list        List routers for a Neki database branch
  show        Show a router for a Neki database branch
  sizes       List available router sizes for a Neki database branch
  update      Update a router for a Neki database branch

Flags:
  -h, --help   help for router

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

Use "pscale branch router [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch router list

```text
List routers for a Neki database branch

Usage:
  pscale branch router list <database> <branch> [flags]

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

## pscale branch router show

```text
Show a router for a Neki database branch

Usage:
  pscale branch router show <database> <branch> <name> [flags]

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

## pscale branch router create

```text
Create a router for a Neki database branch

Usage:
  pscale branch router create <database> <branch> <name> [flags]

Flags:
  -h, --help                    help for create
      --replicas-per-cell int   Number of replicas in each cell
      --size string             Router size SKU (e.g. NKR-5); the API picks a default if omitted

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

## pscale branch router update

```text
Update a router for a Neki database branch.

Changes are requested and applied asynchronously; the router state shows progress.

Usage:
  pscale branch router update <database> <branch> <name> [flags]

Flags:
      --autoscaling                  Whether the router scales horizontally within each cell
  -h, --help                         help for update
      --max-replicas-per-cell int    Maximum number of replicas in each cell when autoscaling
      --parameters stringArray       Set a parameter as namespace.name=value; repeatable
      --replicas-per-cell int        New number of replicas in each cell
      --size string                  New router size SKU (e.g. NKR-5)
      --target-cpu-utilization int   Target average CPU utilization percentage when autoscaling

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

## pscale branch router delete

```text
Delete a router from a Neki database branch

Usage:
  pscale branch router delete <database> <branch> <name> [flags]

Aliases:
  delete, rm

Flags:
      --force   Delete the router without confirmation
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

## pscale branch router sizes

```text
List available router sizes for a Neki database branch

Usage:
  pscale branch router sizes <database> <branch> [flags]

Aliases:
  sizes, size-skus

Flags:
  -h, --help   help for sizes

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

## pscale branch router changes

```text
Manage changes to a Neki router

Usage:
  pscale branch router changes [command]

Available Commands:
  cancel      Cancel a pending change to a Neki router
  list        List changes for a Neki router
  show        Show a change to a Neki router

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

Use "pscale branch router changes [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch router changes list

```text
List changes for a Neki router

Usage:
  pscale branch router changes list <database> <branch> <router> [flags]

Aliases:
  list, ls

Flags:
      --completed-at string   Only show changes completed at this time
  -h, --help                  help for list
      --page int              Page number to fetch
      --per-page int          Number of results per page (default 100)
      --period string         Only show changes from this period

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

## pscale branch router changes show

```text
Show a change to a Neki router

Usage:
  pscale branch router changes show <database> <branch> <router> <change-id> [flags]

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

## pscale branch router changes cancel

```text
Cancel a pending change to a Neki router

Usage:
  pscale branch router changes cancel <database> <branch> <router> <change-id> [flags]

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

## pscale branch sidecar

```text
Manage sidecars for a Neki database branch.

Each configuration profile has one sidecar. Sidecars are created and deleted with their profile. This command is only supported for Neki databases.

Usage:
  pscale branch sidecar [command]

Available Commands:
  changes     Manage changes to a Neki sidecar
  list        List sidecars for a Neki database branch
  parameters  List parameters for a Neki sidecar
  show        Show a sidecar for a Neki database branch
  update      Update a sidecar for a Neki database branch

Flags:
  -h, --help   help for sidecar

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

Use "pscale branch sidecar [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch sidecar list

```text
List sidecars for a Neki database branch

Usage:
  pscale branch sidecar list <database> <branch> [flags]

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

## pscale branch sidecar show

```text
Show a sidecar for a Neki database branch.

<sidecar> is the sidecar ID from `sidecar list`, or the configuration profile name.

Usage:
  pscale branch sidecar show <database> <branch> <sidecar> [flags]

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

## pscale branch sidecar update

```text
Update a sidecar for a Neki database branch.

<sidecar> is the sidecar ID from `sidecar list`, or the configuration profile name.
Changes are requested and applied asynchronously; the sidecar state shows progress.

Usage:
  pscale branch sidecar update <database> <branch> <sidecar> [flags]

Flags:
  -h, --help                     help for update
      --parameters stringArray   Set a parameter as namespace.name=value; repeatable

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

## pscale branch sidecar parameters

```text
List parameters for a Neki sidecar.

<sidecar> is the sidecar ID from `sidecar list`, or the configuration profile name.

Usage:
  pscale branch sidecar parameters <database> <branch> <sidecar> [flags]

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

## pscale branch sidecar changes

```text
Manage changes to a Neki sidecar

Usage:
  pscale branch sidecar changes [command]

Available Commands:
  cancel      Cancel a pending change to a Neki sidecar
  list        List changes for a Neki sidecar
  show        Show a change to a Neki sidecar

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

Use "pscale branch sidecar changes [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch sidecar changes list

```text
List changes for a Neki sidecar

Usage:
  pscale branch sidecar changes list <database> <branch> <sidecar> [flags]

Aliases:
  list, ls

Flags:
      --completed-at string   Only show changes completed at this time
  -h, --help                  help for list
      --page int              Page number to fetch
      --per-page int          Number of results per page (default 100)
      --period string         Only show changes from this period

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

## pscale branch sidecar changes show

```text
Show a change to a Neki sidecar

Usage:
  pscale branch sidecar changes show <database> <branch> <sidecar> <change-id> [flags]

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

## pscale branch sidecar changes cancel

```text
Cancel a pending change to a Neki sidecar

Usage:
  pscale branch sidecar changes cancel <database> <branch> <sidecar> <change-id> [flags]

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

## pscale branch admin

```text
Manage the admin config for a Neki database branch.

Each cluster has one admin. The admin is created and deleted with the cluster. This command is only supported for Neki databases.

Usage:
  pscale branch admin [command]

Available Commands:
  changes     Manage changes to a Neki admin
  parameters  List parameters for a Neki admin
  show        Show the admin for a Neki database branch
  sizes       List available admin sizes for a Neki database branch
  update      Update the admin for a Neki database branch

Flags:
  -h, --help   help for admin

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

Use "pscale branch admin [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch admin show

```text
Show the admin for a Neki database branch.

Each cluster has one admin.

Usage:
  pscale branch admin show <database> <branch> [flags]

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

## pscale branch admin update

```text
Update the admin for a Neki database branch.

Changes are requested and applied asynchronously; the admin state shows progress.

Usage:
  pscale branch admin update <database> <branch> [flags]

Flags:
  -h, --help                     help for update
      --parameters stringArray   Set a parameter as namespace.name=value; repeatable
      --size string              New admin size SKU (e.g. NKA-0)

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

## pscale branch admin parameters

```text
List parameters for a Neki admin.

Each cluster has one admin.

Usage:
  pscale branch admin parameters <database> <branch> [flags]

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

## pscale branch admin sizes

```text
List available admin sizes for a Neki database branch

Usage:
  pscale branch admin sizes <database> <branch> [flags]

Aliases:
  sizes, size-skus

Flags:
  -h, --help   help for sizes

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

## pscale branch admin changes

```text
Manage changes to a Neki admin

Usage:
  pscale branch admin changes [command]

Available Commands:
  cancel      Cancel a pending change to a Neki admin
  list        List changes for a Neki admin
  show        Show a change to a Neki admin

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

Use "pscale branch admin changes [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch admin changes list

```text
List changes for a Neki admin

Usage:
  pscale branch admin changes list <database> <branch> [flags]

Aliases:
  list, ls

Flags:
      --completed-at string   Only show changes completed at this time
  -h, --help                  help for list
      --page int              Page number to fetch
      --per-page int          Number of results per page (default 100)
      --period string         Only show changes from this period

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

## pscale branch admin changes show

```text
Show a change to a Neki admin

Usage:
  pscale branch admin changes show <database> <branch> <change-id> [flags]

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

## pscale branch admin changes cancel

```text
Cancel a pending change to a Neki admin

Usage:
  pscale branch admin changes cancel <database> <branch> <change-id> [flags]

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

## Cross-Skill Command Ownership

Neki workflows touch several shared command families whose exact help is owned elsewhere. Do not duplicate their help fences here; read the owning reference before running them:

- `pscale size cluster list`, `pscale database create`, and `pscale shell`: [../../pscale-database/references/commands.md](../../pscale-database/references/commands.md)
- `pscale branch`, `pscale logs`, and branch-wide `pscale branch maintenance`: [../../pscale-branch/references/commands.md](../../pscale-branch/references/commands.md)
- `pscale backup restore` and `pscale backup restore show`: [../../pscale-backup/references/commands.md](../../pscale-backup/references/commands.md)
- `pscale sql`: [../../pscale-sql/references/commands.md](../../pscale-sql/references/commands.md)
- `pscale role` creation, lookup, reset, deletion, renewal, update, and reassignment: [../../pscale-password/references/commands.md](../../pscale-password/references/commands.md)

## Compatibility

Use CLI v0.349.0 or later for the current Neki change-request endpoints. The CLI command names remain `branch changes` and resource `changes`; branch-wide, config-profile, router, and admin requests now use `change-requests` internally. Legacy sidecar endpoints are unchanged. Do not substitute endpoint paths or use raw API calls to overcome a failure. Relevant parent/list/show/cancel help and list aliases were re-executed unchanged against the checksum-verified v0.349.0 binary (archive SHA-256 `1bdad82d821ab4eb65207672b38dfa063006460226715cb0937588ec671179a6`), retaining original capture attribution. Neki live connection actions also require this minimum; use `pscale-branch` for their ID, permission, and approval gates.
