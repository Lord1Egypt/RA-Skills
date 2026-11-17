Manage branch backups and backup policies

Usage:
  pscale backup [command]

Available Commands:
  create      Backup a branch's data and schema
  delete      Delete a branch backup
  list        List all backups of a branch
  policy      Create, list, show, update, and delete backup policies
  restore     Restore a backup to a new branch
  show        Show a specific backup of a branch

Flags:
  -h, --help         help for backup
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

Use "pscale backup [command] --help" for more information about a command.

## pscale backup policy

All help fences below are exact output from the official, checksum-verified PlanetScale CLI v0.324.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Manage scheduled backup policies for a database.

Backup policies define automatic backup frequency, schedule, and retention for
production or development branches. This is separate from one-off branch
backups created with 'pscale backup create'.

Usage:
  pscale backup policy [command]

Available Commands:
  create      Create a backup policy
  delete      Delete a backup policy
  list        List backup policies for a database
  show        Show a backup policy
  update      Update a backup policy

Flags:
  -h, --help   help for policy

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

Use "pscale backup policy [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

### pscale backup policy create

```text
Create a scheduled backup policy for production or development branches.

Custom schedules beyond the included defaults may incur additional backup storage charges.

Usage:
  pscale backup policy create <database> [flags]

Flags:
      --frequency-unit string   Frequency unit: hour, day, week, or month (required) (required)
      --frequency-value int     Frequency value (required) (required)
  -h, --help                    help for create
      --name string             Optional name for the backup policy
      --retention-unit string   Retention unit: hour, day, week, month, or year (required) (required)
      --retention-value int     Retention period value (required) (required)
      --schedule-day int        Day of week (0=Sunday … 6=Saturday); used for weekly/monthly schedules
      --schedule-time string    Schedule time of day in HH:MM format (required) (required)
      --schedule-week int       Week of month (0=first … 3=fourth); used for monthly schedules
      --target string           Branch target: production or development (required) (required)

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

### pscale backup policy update

```text
Update a backup policy.

Only flags you pass are sent to the API. Required system policies may reject
some changes.

Usage:
  pscale backup policy update <database> <policy-id> [flags]

Flags:
      --frequency-unit string   Frequency unit: hour, day, week, or month
      --frequency-value int     Frequency value
  -h, --help                    help for update
      --name string             Name for the backup policy
      --retention-unit string   Retention unit: hour, day, week, month, or year
      --retention-value int     Retention period value
      --schedule-day int        Day of week (0=Sunday … 6=Saturday)
      --schedule-time string    Schedule time of day in HH:MM format
      --schedule-week int       Week of month (0=first … 3=fourth)
      --target string           Branch target: production or development

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

### pscale backup policy delete

```text
Delete a custom backup policy. Required default system policies cannot be deleted.

Usage:
  pscale backup policy delete <database> <policy-id> [flags]

Aliases:
  delete, rm

Flags:
      --force   Delete a backup policy without confirmation
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

Create usage is `pscale backup policy create <database>` and requires target, frequency value/unit, schedule time, and retention value/unit. Update usage is `pscale backup policy update <database> <policy-id>` and sends only supplied flags. Delete usage is `pscale backup policy delete <database> <policy-id>`; `--force` skips confirmation, and required default system policies cannot be deleted.

## pscale backup update

All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

```text
Update a backup's protected status.

--protected must be passed. Use --protected=false to disable protection.

Usage:
  pscale backup update <database> <branch> <backup-id> [flags]

Examples:
  pscale backup update mydb main backup-id --protected
  pscale backup update mydb main backup-id --protected=false

Flags:
  -h, --help        help for update
      --protected   Protect the backup from deletion (use --protected=false to disable)

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

## pscale backup parent with update

Previous capture note (superseded for this fence): All help fences in this section are exact output from the official, checksum-verified PlanetScale CLI v0.327.0 macOS arm64 release binary after normalizing only trailing whitespace.

Complete help captured from the official, checksum-verified PlanetScale CLI v0.349.0 macOS arm64 binary, in an empty credential-free HOME/XDG/config working environment with `NO_COLOR=1` and `TERM=dumb`. Archive SHA-256: `1bdad82d821ab4eb65207672b38dfa063006460226715cb0937588ec671179a6`. Only terminal padding and trailing whitespace were normalized.

```text
Manage branch backups, backup policies, and restores

Usage:
  pscale backup [command]

Available Commands:
  create      Backup a branch's data and schema
  delete      Delete a branch backup
  list        List all backups of a branch
  policy      Create, list, show, update, and delete backup policies
  restore     Restore a backup to a new branch
  show        Show a specific backup of a branch
  update      Update a backup's protected status

Flags:
  -h, --help         help for backup
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

Use "pscale backup [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale backup restore

Help fences below are exact output from the official, checksum-verified PlanetScale CLI v0.332.0 macOS arm64 release binary with `NO_COLOR=1`, after normalizing only trailing whitespace. The archive SHA-256 is `61eadf71c9d5e6423587fbf01fd698800d8a944775a06519a1c2ac38fcb89287`.

```text
Restore a backup to a new branch.

<new-branch> is the name of the branch to create. It must not already exist.
The backup is identified by id; the source branch is not a restore argument.
Preview Neki restore sizes from the source branch with:

  pscale backup restore show <database> <source-branch> <backup>

Usage:
  pscale backup restore <database> <new-branch> <backup> [flags]
  pscale backup restore [command]

Available Commands:
  show        Show the sizes a Neki backup restore will use if you do not override them

Flags:
      --cluster-size pscale size cluster list   Cluster size for restored backup branch. For Neki, omitted unless set so the source default profile size is used. Use pscale size cluster list to see the valid sizes. (default "PS-10")
      --config-profile stringArray              For Neki backup restores, size and replica count for one configuration profile as name=<profile>[,cluster-size=<size>][,replicas=<n>]. Repeatable. Omitted profiles inherit the source. List names with 'pscale branch config-profile list' on the source branch.
  -h, --help                                    help for restore
      --replicas int                            Number of additional replicas for a PostgreSQL restore. 0 creates a single-node branch; omit to use the target cluster size default.
      --router stringArray                      For Neki backup restores, size and replica count for one router as name=<router>[,size=<sku>][,replicas-per-cell=<n>]. Repeatable. Omitted routers inherit the source. List names with 'pscale branch router list' on the source branch.

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

Use "pscale backup restore [command] --help" for more information about a command.

Agents: run "pscale --skill" to print the installable agent skill, "pscale agent-guide --format json" for machine-readable guidance, or "pscale help agents" to read the full guide.
```

## pscale backup restore show

```text
Show the configuration profile and router sizes a Neki backup restore will use.

These values come from the live source branch, the same source the dashboard
pickers use. They are not stored on the backup. If the source branch was resized
after the backup, this command shows the current sizes.

<branch> is the source branch the backup belongs to, same as backup show.

Usage:
  pscale backup restore show <database> <branch> <backup> [flags]

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

## Compatibility

Emergency backup create flags require CLI v0.349.0 or later; the API determines target eligibility. The `b` alias has been executed and matches create help. Older unchanged child captures retain their recorded attribution.

## pscale backup create

Complete help captured from the official, checksum-verified PlanetScale CLI v0.349.0 macOS arm64 binary, in an empty credential-free HOME/XDG/config working environment with `NO_COLOR=1` and `TERM=dumb`. Archive SHA-256: `1bdad82d821ab4eb65207672b38dfa063006460226715cb0937588ec671179a6`. Only terminal padding and trailing whitespace were normalized.

```text
Backup a branch's data and schema.

--emergency requests an emergency backup, which clones data from a live
tablet instead of waiting for the next scheduled backup. --emergency-source
selects which tablet type to clone from (primary or replica) and is required
with --emergency (and rejected otherwise). rdonly is not accepted.

Usage:
  pscale backup create <database> <branch> [flags]

Aliases:
  create, b

Flags:
      --emergency                 Request an emergency backup that clones data from a live tablet instead of waiting for the next scheduled backup. Requires --emergency-source.
      --emergency-source string   Tablet type to clone from for an emergency backup: primary or replica. Required with --emergency; rejected otherwise.
  -h, --help                      help for create
      --name string               Optional name for the backup

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
