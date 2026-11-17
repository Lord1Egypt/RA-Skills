---
name: pscale-maintenance
description: Inspect PlanetScale maintenance schedules and history, and manage Postgres branch maintenance windows and events with approval. Use for planned maintenance, deadlines, window changes, event rescheduling, and pending Vitess or MySQL versions. Triggers on maintenance schedule, maintenance window, pending Vitess version, pending MySQL version, pscale maintenance, branch maintenance window, branch maintenance event, planned maintenance, or maintenance reschedule.
---

# pscale maintenance

Inspect database maintenance schedules and historical windows for Vitess Enterprise databases, or manage Postgres branch weekly windows and scheduled events. For immediate Postgres/Neki image maintenance, use `pscale-branch`; for Neki profile maintenance, use `pscale-neki`. The branch `window` and `event` commands are Postgres-only.

## Prerequisites

- Authenticate with `pscale auth check --format json`.
- Identify the exact organization, database engine, and branch when applicable.
- Pass `--org` explicitly rather than relying on the configured default organization.
- Prefer `--format json` for automation and preserve schedule IDs as opaque values.

## Inspect database schedules

```bash
# Discover schedules and stable IDs
pscale maintenance list <database> \
  --org <org> \
  --format json

# Inspect one schedule in full
pscale maintenance show <database> <schedule-id> \
  --org <org> \
  --format json
```

Schedule human/CSV output includes a `branch` column. JSON preserves the API model, including nullable `database_branch` identity (`id`, `name`, `created_at`, `updated_at`, `deleted_at`); it is not a full branch object. Schedule output can include whether the schedule is enabled or required, frequency, day/week/hour, duration, next and last window times, pending Vitess/MySQL versions, expiry, and deadline metadata. Treat all timestamps in JSON as authoritative API values; do not infer a local timezone from human table output.

Monthly schedules include a week-of-month value. Non-monthly table rows show a dash for week because the field does not apply.

## Inspect maintenance windows

```bash
pscale maintenance windows <database> <schedule-id> \
  --org <org> \
  --format json
```

Windows are historical or active instances associated with the selected schedule. Use their start and finish timestamps to distinguish completed work from a future schedule. An empty result means no windows currently exist for that schedule; it does not prove maintenance is disabled.

## Safe review workflow

1. Run `pscale database show <database> --org <org> --format json` and confirm the database engine and identity.
2. List schedules and select the exact schedule ID from live output.
3. Show the schedule before interpreting pending versions, expiry, or deadline fields.
4. List its windows and report schedule metadata separately from observed window history.
5. Do not claim these read-only commands reschedule, approve, or cancel maintenance; the top-level `maintenance` commands only list and show records. Postgres scheduling writes use the separate branch commands below.

## Postgres weekly windows and events

First confirm the engine and exact branch. Read the weekly window and page through events before proposing a change:

```bash
pscale branch maintenance window show <database> <branch> --org <org> --format json
pscale branch maintenance event list <database> <branch> --org <org> --format json --page 1 --per-page 100
pscale branch maintenance event show <database> <branch> <event-id> --org <org> --format json
```

Increment `--page` until an empty page for a complete inventory; a short or filtered page does not establish absence. Optional `--state` accepts `scheduled`, `in_progress`, `completed`, `canceled`, or `expired`; `list` also has the `ls` alias. Events are listed latest scheduled time first. Keep IDs opaque. Show/reschedule verifies that the event belongs to the supplied branch.

Window JSON is the original schedule object: numeric `day` (0 Sunday through 6 Saturday), `hour` in UTC, `duration` in hours, `next_window_datetime`, and `database_branch`. Human/CSV fields such as `hour_utc`, `duration_hours`, and `next_window_local` are display fields, not JSON keys. Window lookup automatically pages database schedules, selects a weekly schedule for the live branch, and excludes deleted branches and one-time schedules.

Event JSON preserves `state`, `what`, `why`, `expected_impact`, nullable `scheduled_at` and `completed_at`, `not_after`, `reschedules_remaining`, nested `branch`, and `available_times`. Read the reason, expected impact, deadline, and offered times together; a schedule change is not completed maintenance. Do not invent times or interpret `canceled` as a supported cancellation command.

### Approved scheduling changes

Window set and event reschedule have no confirmation prompt. Before either write, obtain explicit approval for the exact org/database/branch, event ID when applicable, and UTC day/hour or timestamp. Review dependencies, expected restart/connection interruption, maintenance staffing, deadlines, remaining reschedules, and a verified recovery plan. Re-read immediately before acting; stop if the approved state or available time has changed.

```bash
# After approval for this exact weekly window
pscale branch maintenance window set <database> <branch> --org <org> --format json --day sunday --hour 3
pscale branch maintenance window show <database> <branch> --org <org> --format json
pscale branch maintenance event list <database> <branch> --org <org> --format json --page 1 --per-page 100

# Separate approved action: copy an offered RFC 3339 time from fresh event show
pscale branch maintenance event reschedule <database> <branch> <event-id> --org <org> --format json --to <available-time>
pscale branch maintenance event show <database> <branch> <event-id> --org <org> --format json
```

Run only the approved action. `window set` requires at least one of `--day` (full day name, case-insensitive, or 0–6) and `--hour` (0–23); an omitted field keeps its current value, and an identical request is a no-op. Changing the window moves scheduled maintenance, so re-inventory events afterward. The API refuses changes while the window is open or when they would move scheduled work beyond its deadline.

Reschedule requires `--to` in RFC 3339, equal to one of that event's fresh `available_times`; the request is sent in UTC. Reschedules are limited, and started events or an open window cannot be rescheduled. No offered times, exhausted reschedules, unavailable features, permission failures, or deadline/window refusals mean stop and investigate. Never cancel maintenance, add force/bypass flags, automatically repeat a write, or change permissions to overcome a refusal. Service-token writes require `write_database`; a not-found response may reflect scope or permissions. After an ambiguous response, inspect state before considering a separately approved retry. Verify the persisted schedule/event and later completion and service health separately.

## Troubleshooting

- **Command unavailable:** update `pscale` and verify live `pscale maintenance --help`.
- **Not found:** re-run the list against the exact organization/database and copy the schedule ID without modification.
- **No schedules/window:** confirm the engine and applicable feature. A missing Postgres weekly window is not permission to create a schedule or force maintenance.
- **Unexpected day/week:** inspect JSON fields and frequency together; week-of-month applies only to monthly schedules.

See [references/commands.md](references/commands.md) for checksum-verified command help.
