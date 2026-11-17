# pscale maintenance command reference

> The top-level `pscale maintenance` help fences below are exact output from the official, checksum-verified PlanetScale CLI v0.324.0 macOS arm64 release binary after normalizing only trailing whitespace.

## pscale maintenance

```text
List and show maintenance schedules for a Vitess database.

Maintenance schedules define when PlanetScale can perform planned maintenance
(for example version updates). Available for Vitess databases on Enterprise plans.

Usage:
  pscale maintenance [command]

Available Commands:
  list        List maintenance schedules for a database
  show        Show a maintenance schedule
  windows     List maintenance windows for a schedule

Flags:
  -h, --help         help for maintenance
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

Use "pscale maintenance [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale maintenance list

```text
List maintenance schedules for a database

Usage:
  pscale maintenance list <database> [flags]

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

## pscale maintenance show

```text
Show a maintenance schedule

Usage:
  pscale maintenance show <database> <schedule-id> [flags]

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

## pscale maintenance windows

```text
List maintenance windows for a schedule

Usage:
  pscale maintenance windows <database> <schedule-id> [flags]

Flags:
  -h, --help   help for windows

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

## Compatibility

Postgres branch `maintenance window` and `maintenance event` require CLI v0.349.0 or later and API feature availability. Immediate `maintenance run` is a separate Postgres/Neki operation. Earlier top-level maintenance fences above retain their original capture attribution and were verified unchanged; their Vitess-specific help wording is upstream text. The source schedule model also supports Postgres branch identity.

## pscale branch maintenance window

Complete help captured from the official, checksum-verified PlanetScale CLI v0.349.0 macOS arm64 binary, in an empty credential-free HOME/XDG/config working environment with `NO_COLOR=1` and `TERM=dumb`. Archive SHA-256: `1bdad82d821ab4eb65207672b38dfa063006460226715cb0937588ec671179a6`. Only terminal padding and trailing whitespace were normalized.

```text
Show and set the weekly maintenance window of a Postgres branch. Postgres only.

The maintenance window is the day and hour, in UTC, when scheduled maintenance
for the branch is allowed to start.

Usage:
  pscale branch maintenance window [command]

Available Commands:
  set         Change the maintenance window of a Postgres branch
  show        Show the maintenance window of a Postgres branch

Flags:
  -h, --help   help for window

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

Use "pscale branch maintenance window [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch maintenance window show

Complete help captured from the official, checksum-verified PlanetScale CLI v0.349.0 macOS arm64 binary, in an empty credential-free HOME/XDG/config working environment with `NO_COLOR=1` and `TERM=dumb`. Archive SHA-256: `1bdad82d821ab4eb65207672b38dfa063006460226715cb0937588ec671179a6`. Only terminal padding and trailing whitespace were normalized.

```text
Show the weekly maintenance window of a Postgres branch: its day, its hour in
UTC, how long it lasts, and when it next opens.

Usage:
  pscale branch maintenance window show <database> <branch> [flags]

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

## pscale branch maintenance window set

Complete help captured from the official, checksum-verified PlanetScale CLI v0.349.0 macOS arm64 binary, in an empty credential-free HOME/XDG/config working environment with `NO_COLOR=1` and `TERM=dumb`. Archive SHA-256: `1bdad82d821ab4eb65207672b38dfa063006460226715cb0937588ec671179a6`. Only terminal padding and trailing whitespace were normalized.

```text
Set the day and hour, in UTC, when the weekly maintenance window of a Postgres
branch opens. At least one of --day and --hour is required; the one you leave
out keeps its current value.

Scheduled maintenance moves to the new window. Check it afterwards with
'pscale branch maintenance event list'.

You can't change the window while it is open, or if the change would push
scheduled maintenance past its deadline.

Usage:
  pscale branch maintenance window set <database> <branch> [flags]

Examples:
  pscale branch maintenance window set mydb main --day sunday --hour 3
  pscale branch maintenance window set mydb main --hour 14

Flags:
      --day string   Day of the week the window opens, in UTC: a day name or a number from 0 (Sunday) to 6 (Saturday)
  -h, --help         help for set
      --hour int     Hour of the day the window opens, in UTC (0-23)

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

## pscale branch maintenance event

Complete help captured from the official, checksum-verified PlanetScale CLI v0.349.0 macOS arm64 binary, in an empty credential-free HOME/XDG/config working environment with `NO_COLOR=1` and `TERM=dumb`. Archive SHA-256: `1bdad82d821ab4eb65207672b38dfa063006460226715cb0937588ec671179a6`. Only terminal padding and trailing whitespace were normalized.

```text
List, show, and reschedule maintenance events for a Postgres branch.
Postgres only.

A maintenance event is an update PlanetScale has scheduled for a branch, such
as an image update that restarts it. It runs in the branch's maintenance window
and must run by its deadline (not_after).

Usage:
  pscale branch maintenance event [command]

Available Commands:
  list        List maintenance events for a Postgres branch
  reschedule  Reschedule a maintenance event for a Postgres branch
  show        Show a maintenance event for a Postgres branch

Flags:
  -h, --help   help for event

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

Use "pscale branch maintenance event [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale branch maintenance event list

Complete help captured from the official, checksum-verified PlanetScale CLI v0.349.0 macOS arm64 binary, in an empty credential-free HOME/XDG/config working environment with `NO_COLOR=1` and `TERM=dumb`. Archive SHA-256: `1bdad82d821ab4eb65207672b38dfa063006460226715cb0937588ec671179a6`. Only terminal padding and trailing whitespace were normalized.

```text
List maintenance events for a Postgres branch, latest scheduled time first. Use
--state to only list events in one state.

Usage:
  pscale branch maintenance event list <database> <branch> [flags]

Aliases:
  list, ls

Examples:
  pscale branch maintenance event list mydb main --state scheduled

Flags:
  -h, --help           help for list
      --page int       Page number to fetch
      --per-page int   Number of results per page (default 100)
      --state string   Only list events in this state: scheduled, in_progress, completed, canceled, expired

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

## pscale branch maintenance event show

Complete help captured from the official, checksum-verified PlanetScale CLI v0.349.0 macOS arm64 binary, in an empty credential-free HOME/XDG/config working environment with `NO_COLOR=1` and `TERM=dumb`. Archive SHA-256: `1bdad82d821ab4eb65207672b38dfa063006460226715cb0937588ec671179a6`. Only terminal padding and trailing whitespace were normalized.

```text
Show a maintenance event for a Postgres branch: what it changes, why, the
impact to expect, when it is scheduled, its deadline, and the times it can be
rescheduled to.

Usage:
  pscale branch maintenance event show <database> <branch> <id> [flags]

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

## pscale branch maintenance event reschedule

Complete help captured from the official, checksum-verified PlanetScale CLI v0.349.0 macOS arm64 binary, in an empty credential-free HOME/XDG/config working environment with `NO_COLOR=1` and `TERM=dumb`. Archive SHA-256: `1bdad82d821ab4eb65207672b38dfa063006460226715cb0937588ec671179a6`. Only terminal padding and trailing whitespace were normalized.

```text
Move a maintenance event to another of its available times: the branch's
upcoming maintenance windows before the event's deadline. Run
'pscale branch maintenance event show' to list them.

An event can be rescheduled a limited number of times, and not once it has
started or while the maintenance window is open.

Usage:
  pscale branch maintenance event reschedule <database> <branch> <id> [flags]

Examples:
  # Show the times the event can be moved to
  pscale branch maintenance event show mydb main x8k2m4p9q1rz

  # Move it to one of them
  pscale branch maintenance event reschedule mydb main x8k2m4p9q1rz --to 2026-11-08T03:00:00Z

Flags:
  -h, --help        help for reschedule
      --to string   Time to move the event to, in RFC 3339 (e.g. 2026-11-08T03:00:00Z). Must be one of the event's available times (required)

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
