The v0.344.0 help captures (`pscale deploy-request` below and `deploy-request retry` in [retry-command.md](retry-command.md)) come from the official, checksum-verified PlanetScale CLI v0.344.0 macOS arm64 binary with `NO_COLOR=1`, normalizing only trailing whitespace. Archive SHA-256: `1b59b271590d9b49dd52aafbb0e5c0cd788b44c00a5627d6487cd0d18815cf53`.

Create, review, diff, inspect, throttle, revert, and manage deploy requests.

Except for the v0.344.0 captures identified above and sections with their own provenance, help fences below are exact output from the official, checksum-verified PlanetScale CLI v0.324.0 macOS arm64 release binary after normalizing only trailing whitespace.

## pscale deploy-request

```text
Create, review, diff, revert, and manage deploy requests.

This command is only supported for Vitess databases.

Usage:
  pscale deploy-request [command]

Aliases:
  deploy-request, dr

Available Commands:
  apply         Apply changes to a gated deploy request
  cancel        Cancel a deploy request
  close         Close a deploy request
  create        Create a deploy request from a branch
  deploy        Deploy a specific deploy request
  deployment    Show the deployment for a deploy request
  diff          Show the diff of a deploy request
  force-cutover Force cutover when a migration is delayed by a table lock
  list          List all deploy requests for a database
  operations    List deploy operations for a deploy request
  queue         Show the deploy queue for a database
  retry         Retry failed operations on a deploy request
  revert        Revert a deployed deploy request
  review        Review a deploy request (approve, comment, etc...)
  reviews       List reviews for a deploy request
  show          Show a specific deploy request
  skip-revert   Skip and close a pending deploy request revert
  storage-check Check storage readiness for a deploy request
  throttler     Show or update deploy request throttler configuration
  unblock       Unblock the deploy queue after a failed deploy or revert
  update        Update a deploy request

Flags:
  -h, --help         help for deploy-request
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

Use "pscale deploy-request [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale deploy-request create

Complete help capture from the official, checksum-verified PlanetScale CLI v0.345.0 macOS arm64 binary, executed with `env -i`, an empty credential-free `HOME`, minimal `PATH`, and `NO_COLOR=1`. Only trailing whitespace was normalized. Archive SHA-256: `d774eb31cd764dee4c01a1671f3ea17e1d3cb9b8aefe829e82cce2c3358fe028`.

```text
Create a deploy request from a branch

Usage:
  pscale deploy-request create <database> <branch> [flags]

Flags:
      --aggressive-cutover   Cut this deploy request over aggressively: Vitess kills blocking queries and transactions on the first cutover attempt instead of retrying for up to an hour. Does not change the database setting. Other deploy requests are unaffected.
      --auto-delete-branch   Delete the branch after the deploy request completes.
      --disable-auto-apply   Disable auto-apply. The deploy request will wait for your confirmation before swapping to the new schema. Use 'deploy-request apply' to apply the changes manually.
      --enable-auto-apply    Enable auto-apply. The deploy request will automatically swap over to the new schema once ready.
  -h, --help                 help for create
      --into string          Branch to deploy into. By default, it's the parent branch (if present) or the database's default branch.
      --notes string         Notes to include with the deploy request.

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

## pscale deploy-request update

Complete help capture from the official, checksum-verified PlanetScale CLI v0.345.0 macOS arm64 binary, executed with `env -i`, an empty credential-free `HOME`, minimal `PATH`, and `NO_COLOR=1`. Only trailing whitespace was normalized. Archive SHA-256: `d774eb31cd764dee4c01a1671f3ea17e1d3cb9b8aefe829e82cce2c3358fe028`.

```text
Update settings on a deploy request.

Use --enable-auto-apply / --disable-auto-apply to control gated cutover,
--auto-delete-branch to control whether the source branch is deleted after a
successful deploy (same flag as 'deploy-request create'), and
--aggressive-cutover to opt this deploy request into aggressive cutover.
At least one setting must be passed; unset flags are not sent.

Usage:
  pscale deploy-request update <database> <number> [flags]

Aliases:
  update, edit

Flags:
      --aggressive-cutover   Cut this deploy request over aggressively: Vitess kills blocking queries and transactions on the first cutover attempt instead of retrying for up to an hour. Does not change the database setting. Other deploy requests are unaffected. Pass --aggressive-cutover=false to clear the opt-in.
      --auto-delete-branch   Delete the branch after the deploy request completes. Pass --auto-delete-branch=false to keep it.
      --disable-auto-apply   Disable auto-apply. The deploy request will wait for your confirmation before swapping to the new schema. Use 'deploy-request apply' to apply the changes manually.
      --enable-auto-apply    Enable auto-apply. The deploy request will automatically swap over to the new schema once ready.
  -h, --help                 help for update

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

`pscale deploy-request edit --help` prints the same help block; `edit` is an alias of `update`.

## pscale deploy-request unblock

```text
Unblock the deploy queue after a failed deploy or revert.

When a deployment or revert errors, PlanetScale blocks the queue as a
precaution. This is the same action as "Unblock deploy queue" in the dashboard.
It does not apply a gated deploy (use 'deploy-request apply' for that) and it
does not fix a schema that failed deploy checks.

The API decides whether the failure was a deploy or a revert.

Usage:
  pscale deploy-request unblock <database> <number> [flags]

Flags:
  -h, --help   help for unblock

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

## pscale deploy-request deploy

```text
Deploy a specific deploy request

Usage:
  pscale deploy-request deploy <database> <number|branch> [flags]

Flags:
  -h, --help              help for deploy
      --instant           If enabled, the schema migrations from this deploy request will be applied using MySQL’s built-in ALGORITHM=INSTANT option. Deployment will be faster, but cannot be reverted.
      --strategy string   Deployment strategy: "serial" (default) or "parallel".
      --wait              wait until the branch is deployed

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

## pscale deploy-request force-cutover

```text
Force cutover when a deploy request is delayed waiting for a table lock.

The final step of a migration requires a brief table lock. Long-running
transactions can block that lock and delay completion. PlanetScale keeps
retrying for up to 1 hour, then forces cutover automatically.

Use this command to skip the wait: force cutover kills long-running
transactions that are blocking the table lock so the migration can finish.

Only allowed when the deployment state is in_progress_cutover.

Usage:
  pscale deploy-request force-cutover <database> <number> [flags]

Flags:
      --force   Skip the confirmation prompt and force cutover now.
  -h, --help    help for force-cutover

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

## pscale deploy-request show

Complete help capture from the official, checksum-verified PlanetScale CLI v0.345.0 macOS arm64 binary, executed with `env -i`, an empty credential-free `HOME`, minimal `PATH`, and `NO_COLOR=1`. Only trailing whitespace was normalized. Archive SHA-256: `d774eb31cd764dee4c01a1671f3ea17e1d3cb9b8aefe829e82cce2c3358fe028`.

```text
Show a specific deploy request

Usage:
  pscale deploy-request show <database> <number|branch> [flags]

Flags:
  -h, --help   help for show
      --web    Open in your web browser

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

## pscale deploy-request queue

```text
Show the deploy queue for a database

Usage:
  pscale deploy-request queue <database> [flags]

Flags:
  -h, --help   help for queue

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

## pscale deploy-request deployment

```text
Show the deployment for a deploy request

Usage:
  pscale deploy-request deployment <database> <number> [flags]

Flags:
  -h, --help   help for deployment

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

## pscale deploy-request operations

```text
List deploy operations for a deploy request

Usage:
  pscale deploy-request operations <database> <number> [flags]

Flags:
  -h, --help   help for operations

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

## pscale deploy-request reviews

```text
List reviews for a deploy request

Usage:
  pscale deploy-request reviews <database> <number> [flags]

Flags:
  -h, --help   help for reviews

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

## pscale deploy-request storage-check

```text
Check storage readiness for a deploy request

Usage:
  pscale deploy-request storage-check <database> <number> [flags]

Flags:
  -h, --help   help for storage-check

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

## pscale deploy-request throttler

```text
Show or update deploy request throttler configuration.

This is per deploy request, not the database-level throttler.

Usage:
  pscale deploy-request throttler [command]

Available Commands:
  show        Show throttler configuration for a deploy request
  update      Update throttler configuration for a deploy request

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

Use "pscale deploy-request throttler [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale deploy-request throttler show

```text
Show throttler configuration for a deploy request

Usage:
  pscale deploy-request throttler show <database> <number> [flags]

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

## pscale deploy-request throttler update

```text
Update throttler configuration for a deploy request.

Use --ratio to apply one ratio (0-95) to all eligible keyspaces.
Use --configuration keyspace=ratio (repeatable) for per-keyspace ratios.
Pass exactly one of these modes. 0 effectively disables throttling; 95 slows migrations the most.

Usage:
  pscale deploy-request throttler update <database> <number> [flags]

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
