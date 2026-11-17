# `pscale traffic-control` command reference

All help fences below are exact output from the official, checksum-verified PlanetScale CLI v0.324.0 macOS arm64 release binary after normalizing only trailing whitespace.

## `pscale traffic-control`

```text
Manage Database Traffic Control™ budgets and rules for a Postgres database branch.

This command is only supported for Postgres databases.

Usage:
  pscale traffic-control [command]

Available Commands:
  budget      Manage traffic budgets
  rule        Manage traffic rules

Flags:
  -h, --help         help for traffic-control
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

Use "pscale traffic-control [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## `pscale traffic-control budget`

```text
Manage traffic budgets

Usage:
  pscale traffic-control budget [command]

Available Commands:
  create      Create a traffic budget
  delete      Delete a traffic budget
  list        List traffic budgets for a branch
  show        Show a traffic budget
  update      Update a traffic budget

Flags:
  -h, --help   help for budget

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

Use "pscale traffic-control budget [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## `pscale traffic-control budget list`

```text
List traffic budgets for a branch

Usage:
  pscale traffic-control budget list <database> <branch> [flags]

Aliases:
  list, ls

Flags:
      --fingerprint string   Only list budgets with a rule for this query fingerprint
  -h, --help                 help for list

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

## `pscale traffic-control budget show`

```text
Show a traffic budget

Usage:
  pscale traffic-control budget show <database> <branch> <budget-id> [flags]

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

## `pscale traffic-control budget create`

```text
Create a traffic budget

Usage:
  pscale traffic-control budget create <database> <branch> [flags]

Flags:
      --burst int               Maximum capacity a single query can consume (0-6000). Unlimited when not set.
      --capacity int            Maximum capacity that can be banked (0-6000). Unlimited when not set.
      --concurrency int         Percentage of available worker processes (0-100). Unlimited when not set.
  -h, --help                    help for create
      --mode string             Mode of the budget: enforce, warn, or off (default "warn")
      --name string             Name of the traffic budget (required) (required)
      --rate int                Rate at which capacity refills, as a percentage of server resources (0-100). Unlimited when not set.
      --warning-threshold int   Percentage (0-100) of capacity, burst, or concurrency at which to emit warnings for enforced budgets.

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

## `pscale traffic-control budget update`

```text
Update a traffic budget

Usage:
  pscale traffic-control budget update <database> <branch> <budget-id> [flags]

Flags:
      --burst int               Maximum capacity a single query can consume (0-6000). Unlimited when not set.
      --capacity int            Maximum capacity that can be banked (0-6000). Unlimited when not set.
      --concurrency int         Percentage of available worker processes (0-100). Unlimited when not set.
  -h, --help                    help for update
      --mode string             Mode of the budget: enforce, warn, or off
      --name string             Name of the traffic budget
      --rate int                Rate at which capacity refills, as a percentage of server resources (0-100). Unlimited when not set.
      --warning-threshold int   Percentage (0-100) of capacity, burst, or concurrency at which to emit warnings for enforced budgets.

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

## `pscale traffic-control budget delete`

```text
Delete a traffic budget

Usage:
  pscale traffic-control budget delete <database> <branch> <budget-id> [flags]

Aliases:
  delete, rm

Flags:
      --force   Delete a budget without confirmation
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

## `pscale traffic-control rule`

```text
Manage traffic rules

Usage:
  pscale traffic-control rule [command]

Available Commands:
  create      Create a traffic rule on a budget
  delete      Delete a traffic rule from a budget

Flags:
  -h, --help   help for rule

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

Use "pscale traffic-control rule [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## `pscale traffic-control rule create`

```text
Create a traffic rule on a budget

Usage:
  pscale traffic-control rule create <database> <branch> <budget-id> [flags]

Flags:
      --fingerprint string   SQL fingerprint to match
  -h, --help                 help for create
      --keyspace string      Keyspace to match
      --kind string          Kind of rule (default "match")
      --tag stringArray      Tag in the format key=<key>,value=<value>,source=<source> (repeatable)

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

## `pscale traffic-control rule delete`

```text
Delete a traffic rule from a budget

Usage:
  pscale traffic-control rule delete <database> <branch> <budget-id> <rule-id> [flags]

Aliases:
  delete, rm

Flags:
      --force   Delete a rule without confirmation
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

## Scope and safety

- All commands are Postgres-only and require `--org` unless an organization is already configured.
- `budget list` and `budget show` are read-only. Create/update/delete budget and create/delete rule are writes.
- `budget show` returns the budget and its rules; use the returned IDs for later operations.
- Start ordinary rollouts in `warn`, observe behavior, and require explicit approval before `enforce`.
- Use `--force` only for an already-approved non-interactive deletion, then verify with `budget list` or `budget show`.
