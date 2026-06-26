---
name: openstatus-cli
description: |
  OpenStatus CLI for incident management, status reports, and maintenance windows. Use this skill when the user wants to report an incident, create or update a status report, post an incident update, schedule or manage a maintenance window, check the status of an ongoing incident, resolve an incident, view the incident timeline, or communicate planned downtime to status page subscribers. Also trigger when the user says "our API is down", "create a status report", "post an incident update", "schedule maintenance", "maintenance window", "planned downtime", "resolve the incident", "what incidents are open", "notify subscribers", or mentions openstatus in the context of incident or maintenance management.
env:
  - OPENSTATUS_API_TOKEN: API token for authenticating with OpenStatus (optional if using `openstatus login`)
allowed-tools:
  - Bash(openstatus *)
metadata: {"openclaw":{"emoji":"🌎","requires":{"bins":[],"env":["OPENSTATUS_API_TOKEN", "OPENSTATUS_API_TOKEN"]}}}
---

# OpenStatus CLI — Incident Management

OpenStatus is an open-source monitoring platform. The CLI lets you manage incidents and maintenance directly from the terminal — create status reports, post updates through the full incident lifecycle, schedule maintenance windows, and notify your status page subscribers.

Run `openstatus --help` or `openstatus <command> --help` for full option details.

official website: https://www.openstatus.dev

## Prerequisites

The `openstatus` CLI must be installed before using this skill. Install via Homebrew:

```bash
brew install openstatusHQ/cli/openstatus --cask
```

For other installation methods, see the [OpenStatus CLI repository](https://github.com/openstatusHQ/cli).

## Authentication

You must authenticate before running any command:

```bash
openstatus whoami
```

If not authenticated:

```bash
openstatus login
```

Authentication can also be provided via the `--access-token` / `-t` flag or the `OPENSTATUS_API_TOKEN` environment variable.

## Command Overview

| Task | Command | When to use |
|------|---------|-------------|
| Create incident report | `status-report create` | Something is broken — notify users |
| Add update to incident | `status-report add-update <ID>` | Post a progress update on an ongoing incident |
| List incidents | `status-report list` | See active/recent incidents |
| Get incident details | `status-report info <ID>` | View full incident timeline |
| Update incident metadata | `status-report update <ID>` | Change title or affected components |
| Delete incident | `status-report delete <ID>` | Remove a status report |
| Create maintenance window | `maintenance create` | Schedule planned downtime |
| List maintenance windows | `maintenance list` | See scheduled/active/completed maintenance |
| Get maintenance details | `maintenance info <ID>` | View full details of a maintenance window |
| Update maintenance window | `maintenance update <ID>` | Change title, message, or time window |
| Delete maintenance window | `maintenance delete <ID>` | Remove a maintenance window |
| List status pages | `status-page list` | Find your page ID and components |
| Get status page details | `status-page info <ID>` | View page config, components, theme |

Command aliases: `status-report` = `sr`, `status-page` = `sp`, `maintenance` = `mt`.

## Quick Start: Report an Incident End-to-End

```bash
# 1. Find your status page and components
openstatus status-page list
openstatus status-page info <PAGE_ID>

# 2. Create the incident
openstatus status-report create \
  --title "API Degradation" \
  --status investigating \
  --message "Investigating increased error rates" \
  --page-id 123 \
  --component-ids "comp-1,comp-2" \
  --notify

# 3. Post updates as you learn more
openstatus status-report add-update 456 \
  --status identified \
  --message "Root cause: database connection pool exhaustion" \
  --notify

# 4. Resolve
openstatus status-report add-update 456 \
  --status resolved \
  --message "Connection pool limits increased, recovery confirmed" \
  --notify
```

## Quick Start: Schedule a Maintenance Window

```bash
# 1. Find your status page
openstatus status-page list

# 2. Create the maintenance window
openstatus maintenance create \
  --title "Database Migration" \
  --message "Scheduled migration to improve performance" \
  --from "2026-04-05T02:00:00Z" \
  --to "2026-04-05T04:00:00Z" \
  --page-id 123 \
  --component-ids "comp-1" \
  --notify
```

## Incident Lifecycle

Use status reports for **unplanned** outages and incidents.

Status reports follow a strict progression: `investigating` → `identified` → `monitoring` → `resolved`. These are the **only** valid status values — the CLI rejects anything else.

### Step 1: Look Up Your Status Page

Every incident must be attached to a status page. Find your page ID and component IDs first:

```bash
openstatus status-page list
openstatus status-page info <PAGE_ID>   # shows components grouped by section
```

### Step 2: Create the Incident

```bash
openstatus status-report create \
  --title "API Degradation" \
  --status investigating \
  --message "We are investigating increased error rates on the API" \
  --page-id 123 \
  --component-ids "comp-1,comp-2" \
  --notify
```

On success, the CLI prints the report ID and suggests the next command:
```
Status report created successfully (ID: 456)
To add updates, run: openstatus status-report add-update 456 --status identified --message '...'
```

**`create` flags:**

| Flag | Required | Description |
|------|----------|-------------|
| `--title` | yes | Incident title |
| `--status` | yes | `investigating`, `identified`, `monitoring`, or `resolved` |
| `--message` | yes | Initial message describing the incident |
| `--page-id` | yes | Status page ID (from `status-page list`) |
| `--component-ids` | no | Comma-separated component IDs in a single string: `"id1,id2"` |
| `--notify` | no | Send notification to status page subscribers |
| `--date` | no | RFC 3339 timestamp (e.g. `2026-03-25T10:00:00Z`), defaults to now (UTC) |

### Step 3: Post Updates

As the incident progresses, post status updates:

```bash
openstatus status-report add-update 456 \
  --status identified \
  --message "Root cause identified: database connection pool exhaustion" \
  --notify
```

**`add-update` flags:**

| Flag | Required | Description |
|------|----------|-------------|
| `--status` | yes | New status value |
| `--message` | yes | Update message |
| `--notify` | no | Notify subscribers |
| `--date` | no | RFC 3339 timestamp, defaults to now (UTC) |

### Step 4: Resolve

```bash
openstatus status-report add-update 456 \
  --status resolved \
  --message "Connection pool limits increased, monitoring confirms recovery" \
  --notify
```

When status is set to `resolved`, the CLI confirms: `Report resolved.`

### Update Metadata Without Changing Status

Change the title or affected components on an existing report:

```bash
openstatus status-report update 456 \
  --title "API Degradation - Resolved" \
  --component-ids "comp-1,comp-3"
```

At least one of `--title` or `--component-ids` must be provided. `--component-ids` **replaces** the entire list — it is not additive.

### View Incident Timeline

```bash
openstatus status-report info 456
```

Shows full metadata plus the **update timeline** — each update displayed as `<date> [status] <message>`.

### List and Filter Incidents

```bash
openstatus status-report list                          # all reports
openstatus status-report list --status investigating   # only active investigations
openstatus status-report list --limit 10               # last 10 reports
```

### Delete an Incident

```bash
openstatus status-report delete 456        # prompts for confirmation
openstatus status-report delete 456 -y     # skip confirmation
```

## Maintenance Windows

Use maintenance for **planned** downtime windows.

### Create a Maintenance Window

```bash
openstatus maintenance create \
  --title "Database Migration" \
  --message "Scheduled database migration to improve performance" \
  --from "2026-04-05T02:00:00Z" \
  --to "2026-04-05T04:00:00Z" \
  --page-id 123 \
  --component-ids "comp-1,comp-2" \
  --notify
```

On success, the CLI prints the maintenance ID:
```
Maintenance created successfully (ID: 789)
Run 'openstatus maintenance info 789' to see details
```

**`create` flags:**

| Flag | Required | Description |
|------|----------|-------------|
| `--title` | yes | Maintenance title |
| `--message` | yes | Description of the maintenance |
| `--from` | yes | Start time in RFC 3339 format (e.g. `2026-04-05T02:00:00Z`) |
| `--to` | yes | End time in RFC 3339 format |
| `--page-id` | yes | Status page ID (from `status-page list`) |
| `--component-ids` | no | Comma-separated component IDs: `"id1,id2"` |
| `--notify` | no | Notify status page subscribers |

Status is computed automatically based on the current time: `scheduled` (before `--from`), `in_progress` (between `--from` and `--to`), `completed` (after `--to`). There is no `--status` flag.

### Update a Maintenance Window

```bash
openstatus maintenance update <ID> \
  --title "Extended Maintenance" \
  --to "2026-04-05T06:00:00Z"
```

Only provided flags are updated. At least one of `--title`, `--message`, `--from`, `--to`, or `--component-ids` must be set. `--component-ids` replaces the entire list.

### List and Filter

```bash
openstatus maintenance list                        # all maintenance windows
openstatus maintenance list --page-id 123          # filter by page
openstatus maintenance list --limit 10             # limit results
```

### View Details

```bash
openstatus maintenance info <ID>
```

### Delete

```bash
openstatus maintenance delete <ID>       # prompts for confirmation
openstatus maintenance delete <ID> -y    # skip confirmation
```

## Global Flags

Every command supports these:

| Flag | Effect |
|------|--------|
| `--json` | Machine-readable JSON output |
| `--no-color` | Disable colored output |
| `--quiet` / `-q` | Suppress non-error output |
| `--debug` | Enable debug output |

Use `--json` when you need to parse output programmatically or pipe it to `jq`.

## Common Gotchas

- **Missing `--page-id`** — `status-report create` and `maintenance create` both require `--page-id`. Always run `openstatus status-page list` first to get it.
- **Invalid status values** — Status reports only accept `investigating`, `identified`, `monitoring`, `resolved`. The CLI rejects anything else.
- **`--component-ids` replaces, not appends** — On `update`, passing `--component-ids` replaces the entire list. Include all desired components in the new value.
- **`--component-ids` format** — Must be a single comma-separated string: `"id1,id2,id3"`. Do not pass multiple `--component-ids` flags.
- **Notification fatigue** — `--notify` emails all status page subscribers. Use it for `create` and `resolved`, but consider skipping it for intermediate updates.
- **Date format** — All dates must use RFC 3339 / ISO 8601 format: `"2026-04-05T02:00:00Z"`. Other formats will be rejected.
- **Auth errors** — Every command requires auth. If you get auth errors, run `openstatus whoami` to check, then `openstatus login` if needed.
