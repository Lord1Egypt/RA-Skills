---
name: outlook-calendar-management
description: "View, find, add, update, move, and delete Outlook / Microsoft calendar events, including recurring events and free-time queries. Use when the user names Outlook calendar or the conversation already establishes it as the calendar to manage. Does not handle email or other calendar products."
license: "MIT"
metadata:
  version: 3.0.0
---

# Outlook Calendar Management

Manage the connected account's default Outlook calendar. Interpret the user's language and context, then pass explicit values to the bundled Python CLI. The backend validates dates and recurrence patterns, handles timezone conversion, and calls Microsoft Graph; it does not interpret natural-language dates or recurrence rules.

## Run the CLI

Resolve paths relative to this skill directory. Use the available Python 3.10+ interpreter (`python` or `python3`):

```bash
python "<skill-directory>/scripts/outlook_cal.py" context --json --lang en
```

Examples below omit this prefix. Prefer `--json`; JSON keys do not change with language. Use `--lang zh` for Chinese conversations and `--lang en` otherwise; respond in the user's language. `--json`, `--lang`, and `--timezone` work before or after any command.

For first connection or account changes, read [configuration.md](references/configuration.md). Authentication uses `scripts/outlook_setup.py`. For an isolated test login, follow the separate `OCAL_TOKEN_PATH` configuration and verify the intended account before writes. Login and calendar commands install missing requests/msal/tzdata dependencies automatically. `context` and `date` do not access the calendar, authenticate, or install packages; named regional timezones need system timezone data or tzdata.

## Resolve intent before execution

- When resolving relative dates, get `context --json` unless fresh current time and effective timezone are already available. It returns `now`, `today`, `timezone`, `utc_offset`, lowercase English `weekday`, and Monday's `week_start`. If the user specifies a timezone, pass it to `context --timezone "Area/City" --json`. Reuse that named timezone explicitly in subsequent calendar commands; UTC offsets alone do not describe daylight-saving rules.
- Turn relative language into a precise date using `date --base YYYY-MM-DD --days N --json` or Python `datetime`/`calendar` arithmetic. The helper adds signed calendar days without reading a clock. For this Friday, add 4 to `context.week_start`; for next Monday, add 7. Resolve ambiguous intent from context or ask only for missing information that affects the operation.
- Calendar inputs accept only zero-padded `YYYY-MM-DD`, `YYYY-MM-DD HH:MM`, or `YYYY-MM-DDTHH:MM`; date-only arguments reject times. Supply timezone separately. Timed creation needs both start and end; all-day creation requires `--all-day`. Do not invent a duration or turn a missing time into an all-day event.
- Before a write, retain the normalized target, absolute dates/times, timezone, and requested fields. Reuse these values for verification and any retry, including across midnight; do not reinterpret the original relative phrase.

## Choose and carry out the operation

| Task | Command |
|---|---|
| Events on a date / date range | `list --from YYYY-MM-DD --days N --json` |
| Filter that range | Add `--search "term"`, `--category "name"`, or `--reminders` |
| Events created in a date interval | `list --created-after YYYY-MM-DD --created-before YYYY-MM-DD --json` |
| Details / next recurring occurrence | `read <ID>` / `next <ID>` |
| Create / edit / move / delete | `add` / `update` / `move` / `delete` |
| Free slots / connection state | `free YYYY-MM-DD --from HH:MM --to HH:MM` / `status` |

`list` requires an explicit `--from` or `--created-after`. Its `--days N` spans N calendar dates with an exclusive end at the next midnight. Creation filters are independent of scheduled dates; `--created-before` is exclusive. For an unspecified schedule range, a reasonable initial query is seven days from `context.today`; state the range when reporting it. `--summary` gives daily counts only, so use normal JSON for titles and times.

Use returned `id` and `seriesMasterId` values. Before editing or deleting, obtain the relevant existing fields through `read` or reuse fresh complete results. Resolve multiple matches and distinguish one occurrence from the whole recurring series. Existing authorization for an identified target and scope remains valid; `--json`/`-y` only skip CLI prompts. Prefer an explicit ID after identifying the target; `--search` is a convenience with a bounded search window.

After a write, read back once and verify the requested fields. After deletion, query the relevant window and confirm absence. Report actual before/after values. For an uncertain write, check server state before resubmitting the frozen request; a failed verification is not evidence that the write failed. Retry a transient read once; diagnose authentication and permission errors with `status` and [troubleshooting.md](references/troubleshooting.md). If recovery fails, explain what remains unresolved.

## Examples of normalization

These dates are hypothetical: assume `context` reports **2026-09-09, Asia/Shanghai**, with `week_start` **2026-09-07**. Derive real dates from the current context rather than copying these values.

- **"Move what I added yesterday to today."** Calculate yesterday with `date --base 2026-09-09 --days -1 --json`. Find candidates using `list --created-after 2026-09-08 --created-before 2026-09-09 --timezone Asia/Shanghai --json`, then identify the event and use `move <ID> --to 2026-09-09 --timezone Asia/Shanghai --json`. Its original scheduled date may be in the future; creation date does not determine the move offset.
- **"Add a half-hour meeting this Friday at 15:00, remind me 10 minutes before."** Calculate Friday with `date --base 2026-09-07 --days 4 --json`, then use `add "Meeting" "2026-09-11 15:00" "2026-09-11 15:30" --remind 10 --timezone Asia/Shanghai --json`.
- **"Am I free this Friday 14:00–17:00?"** After the same date calculation, use `free 2026-09-11 --from 14:00 --to 17:00 --timezone Asia/Shanghai --json`.
- **"Change the weekly sync to Wednesday."** Establish occurrence versus series scope. For a series rule, read [recurring-events.md](references/recurring-events.md), construct a Graph pattern JSON file, and use `update <seriesMasterId> --repeat-file <pattern-file> --timezone <resolved-zone> --json`. Preserve or intentionally change the existing end condition; explain the effect on exceptions before applying an authorized series change.

## Output and references

In JSON operation mode stdout contains one JSON value; diagnostics go to stderr. Check the exit code: errors use `{"error": ..., "exit": 1}`; disconnected `status` returns its connection object with `connected: false`. `--help` remains text. Parse decoded JSON, including Unicode escapes. For free time, use JSON because human output without listed slots may mean entirely free or entirely busy.

| Read when | Reference |
|---|---|
| Parameters, explicit time formats, reminders, query boundaries, or JSON shapes | [commands.md](references/commands.md) |
| Recurrence pattern fields, end conditions, occurrences, or whole series | [recurring-events.md](references/recurring-events.md) |
| Connecting, switching accounts, or Azure app setup | [configuration.md](references/configuration.md) |
| Authentication, installation, timezone errors, or unexpected results | [troubleshooting.md](references/troubleshooting.md) |

Timed events use the selected effective timezone. All-day dates are written in the mailbox timezone when available, falling back to the effective timezone; this preserves their calendar dates in Outlook. Investigate timezone/permission discrepancies before repeating a write.
