# Command Reference

Run `python "<skill-directory>/scripts/outlook_cal.py" <command> [arguments]`. Examples below use the shorter `python scripts/outlook_cal.py` from the project root. Only calendar commands require sign-in; see [configuration.md](configuration.md).

## Shared arguments and formats

- `--json`, `--lang zh|en`, and `--timezone "Area/City"` work before or after a command. Without `--timezone`, the CLI detects the effective local timezone, including `TZ`. Explicit timezone names must be valid IANA or current Windows names; invalid names fail instead of silently becoming UTC. An explicit IANA name retains its own regional rules.
- Date: exactly `YYYY-MM-DD`. Timed values: exactly `YYYY-MM-DD HH:MM` or `YYYY-MM-DDTHH:MM`. All numeric components must be zero-padded. Seconds, timezone suffixes, natural language, and extra whitespace are rejected. Timezone is a separate argument.
- Resolve user language in the agent. Obtain fresh `context` when needed, calculate dates, and retain the absolute values and named timezone for writes and retries. Examples dated September 2026 are hypothetical.
- Obtain event IDs from JSON `id` and `seriesMasterId`. Human output also has 🆔 and 🆕 anchors; stderr conflict warnings are not result IDs.
- `update`, `move`, and `delete` accept either an event ID or `--search "term"`. Search checks the past 7 days through the next 30 days; a unique match proceeds, zero/multiple matches fail with guidance. For other ranges or an identified target, query with `list` first and pass the returned ID.
- `-y` and `--json` skip CLI confirmation. Reuse existing user authorization for the identified action and scope.

## Local helpers

### context — current clock and timezone

```bash
python scripts/outlook_cal.py context --timezone Asia/Shanghai --json
```

Returns an object with `now` (offset-bearing datetime), `today` (date), `timezone` (effective name), `utc_offset`, `weekday` (lowercase English weekday), and `week_start` (Monday's date). It does not read calendar data or authenticate. A fresh result can be reused for related steps; refresh when elapsed time or a timezone change affects relative-date interpretation.

### date — deterministic calendar-day arithmetic

```bash
python scripts/outlook_cal.py date --base 2026-09-07 --days 4 --json
```

Returns `{"base":"2026-09-07","days":4,"date":"2026-09-11"}`. `--base` and signed integer `--days` are required; zero and negative offsets are valid. The helper neither reads a clock nor accesses the calendar. Invalid or overflowing dates fail.

Use `context.today` plus 1 for tomorrow, `context.week_start` plus 4 for this Friday, or plus 7 for next Monday. Complex month/year calculations can use Python `datetime`/`calendar` with the same explicit base.

## Read commands

### status

`status` reports connection state and account information. Unlike `context`, it checks account configuration.

### list

Choose exactly one query basis:

- `list --from YYYY-MM-DD [--days N]`: N calendar dates, default 7. N must be positive. The window begins at local midnight and ends at midnight after the final date, excluding that end. Timezone offsets are calculated for each boundary, including across DST.
- `list --created-after YYYY-MM-DD [--created-before YYYY-MM-DD]`: filter by creation time at or after the first date's local midnight and, optionally, before the second date's midnight. The upper date must be later. These filters concern creation, not the event's scheduled date. `--created-before` requires `--created-after`; creation filters cannot combine with `--from`.

`--search "term"` filters title/location/notes; `--category "name"` filters categories; `--reminders` limits to events with reminders. `--summary` counts returned events by scheduled start date, counting multi-day events once; omit it to obtain titles and times. In JSON mode the result is a date-to-count object such as `{"2026-09-11":2}`, or `{}` with no matches. Creation-filter results also include `createdDateTime`.

```bash
python scripts/outlook_cal.py list --from 2026-09-09 --days 7 --timezone Asia/Shanghai --json
python scripts/outlook_cal.py list --from 2026-09-07 --days 7 --search "meeting" --timezone Asia/Shanghai --json
python scripts/outlook_cal.py list --created-after 2026-09-08 --created-before 2026-09-09 --timezone Asia/Shanghai --json
```

The `today`, `tomorrow`, `week` commands and `--past` option have been removed. Normalize the desired interval and use `list --from`.

### read and next

`read <ID>` returns full event details, including creation time, organizer, reminder, recurrence, and series master ID where applicable. `next <ID>` finds the next occurrence of a recurring event within 365 days; ended series and non-recurring events have distinct results.

### free

`free YYYY-MM-DD [--from HH:MM] [--to HH:MM] [--days N]` requires a date. Time bounds default to 09:00–18:00 and N defaults to 1; agents should explicitly supply the user's requested bounds. N is positive and each daily end must be later than its start. `HH:MM` is zero-padded. Events marked free and cancelled events do not occupy time; busy all-day events occupy the whole day. A daily query window is rejected if an endpoint is nonexistent/ambiguous or if its UTC offset changes within the window. Resolve the intended UTC bounds and use `--timezone UTC`; plain `HH:MM` output cannot distinguish repeated local clock times.

```bash
python scripts/outlook_cal.py free 2026-09-11 --from 14:00 --to 17:00 --timezone Asia/Shanghai --json
```

## add — create an event

Timed: `add <subject> "YYYY-MM-DD HH:MM" "YYYY-MM-DD HH:MM"`. Both start and end are required, and end must be later. A date-only start without `--all-day` is an error.

All-day: `add <subject> YYYY-MM-DD [YYYY-MM-DD] --all-day`. The optional end date is inclusive; omitting it creates one all-day date. The backend converts this to Graph's exclusive next-midnight end. All-day writes use the mailbox timezone when available, otherwise the effective timezone.

| Option | Meaning |
|---|---|
| `-l` / `--location`, `-b` / `--body` | Location and notes |
| `--category "Work,Important"` | Comma-separated categories |
| `--remind N` | Timed: minutes before; all-day: days before |
| `--repeat-file <path>` or `--repeat '<JSON>'` | Validated Graph recurrence pattern; mutually exclusive |
| `--repeat-until YYYY-MM-DD` or `--repeat-times N` | Recurrence end condition, mutually exclusive; requires a pattern |
| `--importance low\|normal\|high`, `--private` | Importance and privacy |
| `--busy free\|tentative\|busy\|oof\|workingElsewhere` | Availability status |
| `--force` | Skip the conflict check |

Overlaps warn without blocking creation. Invalid, nonexistent, and ambiguous DST wall-clock times are rejected. For ambiguous local times, determine the intended instant and use explicit UTC bounds with `--timezone UTC`. The end time is never inferred from an omitted duration.

```bash
python scripts/outlook_cal.py add "Planning" "2026-09-11 15:00" "2026-09-11 15:30" --remind 10 --timezone Asia/Shanghai --json
python scripts/outlook_cal.py add "Trip" 2026-09-11 2026-09-13 --all-day --timezone Asia/Shanghai --json
```

## update — change specified fields

`update <ID> [options]` preserves fields not supplied. Available fields: `--subject`, `--start`, `--end`, `-l`/`--location`, `-b`/`--body`, `--category`, `--importance`, `--private`/`--no-private`, `--busy`, `--remind`/`--no-remind`, and recurrence options from `add`.

- Use an empty string to clear subject/location/body/categories. `--no-remind` disables reminders.
- Partial time changes are allowed when the event type stays the same; the resulting range must remain valid.
- Switching between timed and all-day with `--all-day`/`--no-all-day` requires **both** `--start` and `--end` in the new type's format. All-day end dates remain inclusive. No start/end is invented during conversion.
- Only an explicit `--repeat ''` removes recurrence. Empty or whitespace-only rule files are errors. Setting a rule requires a pattern object or file. Read [recurring-events.md](recurring-events.md) for occurrence/master scope and end-condition handling.
- Supplying no update fields returns an error without PATCH.

```bash
python scripts/outlook_cal.py update <ID> --no-all-day --start "2026-09-11 09:00" --end "2026-09-11 10:00" --timezone Asia/Shanghai --json
```

For recurrence, a file avoids shell-specific escaping. Save a UTF-8 `weekly.json` containing only this pattern object:

```json
{"type":"weekly","interval":1,"daysOfWeek":["wednesday"],"firstDayOfWeek":"monday"}
```

Then, for an authorized series change with the requested end condition:

```bash
python scripts/outlook_cal.py update <masterID> --repeat-file weekly.json --repeat-times 8 --timezone Asia/Shanghai --json
```

## move and delete

`move <ID> --to YYYY-MM-DD` or `move <ID> --days N` requires exactly one destination option. Signed `--days` shifts the scheduled date; `--to` chooses a specific scheduled date. Both preserve the time slot and duration, including all-day spans. Do not derive a move offset from the event's creation date.

`delete <ID> [-y] [--series]` deletes the identified event. For an occurrence, `-y`/`--json` defaults to that occurrence only; `--series` deletes its whole series. Interactive mode can ask which scope to delete. Verify the requested target and scope from the conversation.

## JSON contract

In `--json` operation mode stdout contains exactly one JSON value, with human diagnostics on stderr. `--help` is text. JSON uses ASCII escapes to preserve Unicode through narrow Windows pipes; parse before inspecting values.

| Command | Result |
|---|---|
| `context` | Clock/timezone object described above |
| `date` | `{base, days, date}` |
| `list` | Event array, or daily counts with `--summary` |
| `add`, `read`, `update`, `move` | Event object |
| `delete` | Object with `deleted`, `subject`, `series` |
| `free` | Per-day availability structure |
| Operation/argument error | `{"error": ..., "exit": 1}`, nonzero exit |
| Disconnected `status` | Connection object with `connected: false` |
