List, show, switch, and update organizations; manage organization SSO, members, and teams. The complete SSO command family is documented in [`sso-commands.md`](sso-commands.md).

Unless a section says otherwise, help fences below are exact output from the official, checksum-verified PlanetScale CLI v0.324.0 macOS arm64 release binary after normalizing only trailing whitespace.

## pscale org

This help fence is exact output from the official, checksum-verified PlanetScale CLI v0.328.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Manage organizations

Usage:
  pscale org [command]

Available Commands:
  list        List the currently active organizations
  member      List, show, update, and remove organization members
  show        Display the currently active organization
  sso         Manage organization SSO
  switch      Switch the currently active organization
  team        Manage organization teams
  update      Update an organization's settings

Flags:
  -h, --help   help for org

Global Flags:
      --api-token string          The API token to use for authenticating against the PlanetScale API.
      --api-url string            The base URL for the PlanetScale API. (default "https://api.planetscale.com/")
      --config string             Config file (default is $HOME/.config/planetscale/pscale.yml)
      --debug                     Enable debug mode
  -f, --format string             Show output in a specific format. Possible values: [human, json, csv] (default "human")
      --no-color                  Disable color output
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Use "pscale org [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale org list

```text
List the currently active organizations

Usage:
  pscale org list [flags]

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
      --service-token string      Service Token for authenticating.
      --service-token-id string   The Service Token ID for authenticating.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale org show

```text
Display the currently active organization

Usage:
  pscale org show [flags]

Flags:
  -h, --help   help for show

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

## pscale org switch

```text
Switch the currently active organization

Usage:
  pscale org switch <organization> [flags]

Flags:
  -h, --help                 help for switch
      --save-config string   Path to store the organization. By default the configuration is deducted automatically based on where pscale is executed.

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

## pscale org member

```text
Manage organization members and their roles.

show, update, and remove take an email or a user id (the USER_ID column from
'org member list'). Email is usually the easiest.

Only organization admins can change another member's role or remove someone
else. Nobody can change their own role. Members can still leave the organization
themselves.

Usage:
  pscale org member [command]

Available Commands:
  list        List members of an organization
  remove      Remove a member from an organization
  show        Show an organization member
  update      Update an organization member's role

Flags:
  -h, --help         help for member
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

Use "pscale org member [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale org member list

```text
List members of an organization.

Results are paginated: 100 members per page by default. Use --page and
--per-page to walk organizations with more members than one page holds.

Usage:
  pscale org member list [flags]

Aliases:
  list, ls

Flags:
  -h, --help           help for list
      --page int       Page number to fetch
      --per-page int   Number of results per page (default 100)
      --query string   Filter members by name or email prefix

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

## pscale org member show

```text
Show an organization member by email or user id.

'org member list' prints both EMAIL and USER_ID.

Usage:
  pscale org member show <email|user-id> [flags]

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

## pscale org member update

```text
Update another member's organization role.

Identify the member by email or by the USER_ID from 'org member list'.
Only organization admins can do this. You cannot change your own role.
Assignable roles: admin, member, analyst.

Usage:
  pscale org member update <email|user-id> [flags]

Flags:
  -h, --help          help for update
      --role string   Role to assign: admin, member, or analyst

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

## pscale org member remove

```text
Remove a member from an organization.

Identify the member by email or by the USER_ID from 'org member list'.
Removing someone else requires organization admin. You can remove yourself
(leave) without being an admin. The last admin cannot be removed.

Usage:
  pscale org member remove <email|user-id> [flags]

Aliases:
  remove, rm

Flags:
      --delete-passwords        Delete passwords created by the member. Cannot be used when removing yourself.
      --delete-service-tokens   Delete service tokens created by the member. Cannot be used when removing yourself.
      --force                   Remove the member without confirmation
  -h, --help                    help for remove

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

## pscale org update

This help fence is exact output from the official, checksum-verified PlanetScale CLI v0.328.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Update an organization's settings

Usage:
  pscale org update [flags]

Flags:
      --billing-email string     The billing email for the organization
  -h, --help                     help for update
      --idp-managed-roles        Whether the identity provider manages organization roles through directory sync
      --idp-sso-managed-roles    Whether the identity provider manages organization roles through SSO
      --org string               The organization for the current user (required)
      --spend-alert              Enable or disable billing spend alerts
      --spend-alert-amount int   Monthly spend amount that triggers spend alerts

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

## pscale org team

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Manage organization teams

Usage:
  pscale org team [command]

Available Commands:
  create      Create an organization team
  delete      Delete an organization team
  list        List organization teams
  member      Manage organization team members
  show        Show an organization team
  update      Update an organization team

Flags:
  -h, --help         help for team
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

Use "pscale org team [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale org team list

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
List organization teams.

Results are paginated: 100 teams per page by default. Use --page and
--per-page to walk organizations with more teams than one page holds.

Usage:
  pscale org team list [flags]

Aliases:
  list, ls

Flags:
  -h, --help           help for list
      --page int       Page number to fetch
      --per-page int   Number of results per page (default 100)
      --query string   Filter teams by name

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

## pscale org team show

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Show an organization team

Usage:
  pscale org team show <team-id-or-name> [flags]

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

## pscale org team create

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Create an organization team

Usage:
  pscale org team create [flags]

Flags:
      --description string   Description of the team
  -h, --help                 help for create
      --name string          Name of the team (required)

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

## pscale org team update

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Update an organization team

Usage:
  pscale org team update <team> [flags]

Flags:
      --description string   New description for the team
  -h, --help                 help for update
      --name string          New name for the team

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

## pscale org team delete

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Delete an organization team

Usage:
  pscale org team delete <team> [flags]

Aliases:
  delete, rm

Flags:
      --force   Delete the team without confirmation
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

## pscale org team member

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Manage organization team members

Usage:
  pscale org team member [command]

Available Commands:
  add         Add an organization member to a team
  list        List members of an organization team
  remove      Remove a member from an organization team

Flags:
  -h, --help   help for member

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

Use "pscale org team member [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale org team member list

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
List members of an organization team.

Results are paginated: 100 members per page by default. Use --page and
--per-page to walk teams with more members than one page holds.

Usage:
  pscale org team member list <team> [flags]

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

## pscale org team member add

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Add an organization member to a team

Usage:
  pscale org team member add <team> <email-or-id> [flags]

Flags:
  -h, --help   help for add

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

## pscale org team member remove

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Remove a member from an organization team

Usage:
  pscale org team member remove <team> <email-or-id> [flags]

Aliases:
  remove, rm

Flags:
      --delete-passwords   Delete passwords created through this team
      --force              Remove the team member without confirmation
  -h, --help               help for remove

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
