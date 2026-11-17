# Troubleshooting

For connection setup see [configuration.md](configuration.md); for exact parameters see [commands.md](commands.md). Run the examples from the project root. In JSON mode, inspect the exit code and decoded error object; human diagnostics are on stderr.

## Connection and timezone

| Symptom | Action |
|---|---|
| Device code reports that the app was not found | For a custom app, check its client ID, supported account types, and public-client setting in [Azure setup](azure-app-setup.md). |
| Expired login, `invalid_grant`, or authentication failure | Re-run `python scripts/outlook_setup.py`. |
| 403 permission error | Check `Calendars.ReadWrite`; mailbox timezone lookup also needs `MailboxSettings.Read`. |
| Times differ by hours | Inspect `context --json` and `status --json`. Pass the intended named `--timezone` explicitly. If timezone data is missing, install `tzdata` with the same Python interpreter. |
| Explicit timezone is rejected | Use a valid IANA or current Windows name, such as `Asia/Shanghai` or `China Standard Time`; UTC offsets are not timezone names. |
| All-day dates appear across two days | Check mailbox timezone access. Reconnect to grant `MailboxSettings.Read`; all-day writes use the mailbox timezone when available. |
| Local time does not exist on a DST transition | The write is rejected. Choose a real local time consistent with the user's intent. The backend does not let the server silently adjust it. |
| Local time is ambiguous on a DST transition | The write is rejected. Determine which occurrence of that clock time the user intends, convert that instant to UTC, and supply explicit bounds with `--timezone UTC`. |
| A free-time query crosses an offset transition or has an invalid/ambiguous endpoint | Query the intended UTC interval using `--timezone UTC`; `HH:MM` slots cannot identify which repeated local time they represent. Ordinary windows that avoid the transition still work. |

## Input and query errors

| Input / symptom | Correction |
|---|---|
| `this friday`, `2026/09/11`, a missing zero, seconds, or a timezone suffix in a date argument | Resolve language in the model; pass exactly `YYYY-MM-DD`, `YYYY-MM-DD HH:MM`, or `YYYY-MM-DDTHH:MM`, as applicable. Supply timezone separately. |
| Timed creation omits the end, or uses a date-only start | Provide explicit start and end; use `--all-day` only when the user intends an all-day event. |
| Type conversion supplies only one bound | Both `--start` and `--end` are required when changing between timed and all-day events. |
| End is at/before start | Correct the resulting interval. For all-day events the CLI end date is inclusive. |
| `list` has no query basis, or mixes scheduled and creation dates | Supply exactly one of `--from` or `--created-after`. Use `--created-before` only with the latter; its upper date must be later. |
| A creation filter finds an event scheduled on a different date | Creation time and scheduled time are different fields. Use `--from` for the dates when events occur. |
| Invalid recurrence JSON or unsupported field/type | Use the exact pattern structure in [recurring-events.md](recurring-events.md). Prefer `--repeat-file` to avoid shell quoting problems. |
| `--repeat-times 0`, or cutoff before start | Use a positive integer count or an absolute cutoff on/after the event start date. Supply at most one end condition. |
| End/count without a pattern | Supply `--repeat` or `--repeat-file` together with the desired end condition. |
| Negative reminder or more than 1826 all-day reminder days | Use a nonnegative value within the all-day limit; timed reminder units are minutes. |
| Empty/nonexistent ID, both move options, or a zero-day move | Use a returned result ID; choose exactly one of `--days` or `--to`, with a nonzero actual shift. |

## Event operations

| Symptom | Action |
|---|---|
| A deleted recurring occurrence now reports “not found” | Query its explicit date window to verify absence; do not reuse the deleted occurrence ID. |
| Moving an occurrence crosses an adjacent occurrence | Choose a destination within Graph's allowed adjacent-occurrence boundary. |
| Earlier exceptions changed after a new series pattern | Changing a series pattern can reset exceptions. Establish this effect and the intended scope before applying the change. |
| A pattern update lost its previous end condition | A supplied pattern rebuilds the range; omitting both end options means no end. Read the existing cutoff/count and explicitly pass it when it should be preserved. |
| An existing event is missing from results | Check the account, named timezone, exact query window, and filters. Calendar-window queries expand occurrences; creation queries use a different endpoint. |
| No conflict warning when adding | `--force` skips conflict checking. Free/cancelled events do not count as occupied. |
| A create/update request times out | Its result may be unknown. Check the intended event's server state before resending the same normalized request. |

## Unexpected failures and unsupported features

A Python traceback is unexpected; record the command with sensitive data removed, the script path, and the error for diagnosis. Structured errors should normally explain invalid input or Graph failures.

Hourly recurrence and intervals counted in working days are not supported by the six Graph patterns. The tool also does not import `.ics` files or select among multiple calendars. It operates the default calendar of one connected account; reconnecting can switch that account.
