# Developer Guide

This guide describes the execution contract and the implementation choices that need to survive refactoring. Agent instructions are in [SKILL.md](SKILL.md); the complete interface is in [commands.md](references/commands.md).

## Responsibility boundary

The model resolves natural-language dates, recurrence wording, event identity, missing information, and occurrence/series scope. It supplies explicit values and verifies the requested result. Python provides deterministic date arithmetic, validates concrete inputs, handles calendar/timezone semantics, and calls Graph.

- `context --json` returns the effective clock and named timezone without calendar authentication. `date --base YYYY-MM-DD --days N --json` adds signed calendar days without reading a clock.
- `_parse_dt_arg` accepts only zero-padded `YYYY-MM-DD`, `YYYY-MM-DD HH:MM`, or `YYYY-MM-DDTHH:MM`. Date-only parameters reject times; seconds, offsets, extra whitespace, and language expressions are invalid. Graph response parsing is a separate, more tolerant path.
- `list` requires either `--from` or `--created-after`; `free` requires a date. Calendar windows use local midnight and an exclusive next-midnight end. `--created-before` is an exclusive creation-time upper bound.
- Timed creation requires both start and end. All-day creation requires `--all-day`; its optional inclusive end defaults to the start date. Type conversions require both new bounds. Partial updates preserve unspecified fields and validate the resulting range.
- Recurrence input is a Graph pattern JSON object, supplied inline or in a UTF-8 file. All applicable fields are explicit; unsupported, duplicate, missing, or irrelevant fields are rejected. The six supported pattern types and end conditions are documented in [recurring-events.md](references/recurring-events.md).
- Freeze normalized dates, times, timezone, target, and fields before writing. Verification or recovery should reuse those values even if the clock crosses midnight.

## Code map

| File | Responsibility |
|---|---|
| `scripts/outlook_cal.py` | Argument parsing, language pre-scan, repeat-file loading, command dispatch, per-command timezone override, structured errors |
| `scripts/ocal_context.py` | Offline clock context and calendar-day arithmetic |
| `scripts/ocal_time.py` | Default timezone detection, strict input dates, Graph timestamp conversion, all-day ranges |
| `scripts/ocal_recurrence.py` | Structured pattern validation, range construction, human descriptions, conservative occurrence numbering |
| `scripts/ocal_events.py` | Calendar commands, target resolution, conflict/free-time calculation, result rendering |
| `scripts/ocal_graph.py` | Graph requests, headers, retry/error handling, paging |
| `scripts/ocal_auth.py` | Token retrieval/renewal and cross-process locking |
| `scripts/outlook_setup.py` | Device-code sign-in; importing the module does not start authentication |
| `scripts/ocal_bootstrap.py` | Dependency checks and installation; standard library plus i18n only |
| `scripts/ocal_i18n.py`, `scripts/ocal_errors.py` | Bilingual messages and user-facing `CalError` |

Distribute the complete `scripts/` directory. Python 3.10+ is required. Bootstrap installs missing `requests`, `msal`, and `tzdata` before importing calendar modules; importing those modules first would prevent first-run installation from handling missing dependencies.

## Time and timezone semantics

1. The default timezone is detected when `ocal_time` loads: `TZ` → Windows registry → system timezone key → `/etc/timezone` → `/etc/localtime` symlink/content → offset fallback → UTC fallback. Offset/UTC fallbacks warn. An explicitly set but unparseable POSIX `TZ` uses the offset fallback rather than an unrelated system configuration.
2. `--timezone` validates an IANA or current Windows name and applies it consistently to context, input interpretation, API preferences, recurrence, and display. Detected and explicit IANA names keep their regional rules; do not replace it with a broader Windows alias. Dispatch restores previous module values afterwards so repeated in-process calls do not leak timezone changes.
3. Windows names map through the CLDR table. Legacy aliases remain useful when reading Graph responses. Keep `tzdata` available, especially on Windows, where the system often supplies no IANA database.
4. Timed writes reject both nonexistent and ambiguous DST wall-clock times. `_local_time_exists` checks an aware → UTC → local roundtrip; different fold offsets detect ambiguity. Resolve the intended instant first and use explicit UTC input when local time is ambiguous.
   Free-time queries also reject windows whose endpoints are nonexistent/ambiguous or whose UTC offset changes within the window: plain `HH:MM` slots cannot represent both occurrences of a repeated clock time. Resolve the intended UTC window and query with `--timezone UTC`. Ordinary windows that do not cross a transition remain valid.
5. All-day writes use the mailbox timezone when available, falling back to the effective timezone. CLI end dates are inclusive; Graph stores the following midnight as the exclusive end. Read all-day date spans without converting their date component through UTC. Recurrence ranges use the resulting event timezone too.
6. Query boundaries include their individual offsets, including across DST. Graph timestamps may have seven fractional digits; truncating fractions must retain a `Z` or numeric timezone suffix.

## Graph behavior to preserve

- Event requests use `Prefer: IdType="ImmutableId"`; never construct IDs from titles or time values. All generated URL paths quote IDs.
- Network failures after POST/PATCH have an uncertain result; do not blindly retry. Read back server state before resubmitting. GET/DELETE can retry transient network and 500/503 failures. For 429, follow `Retry-After`, falling back to bounded exponential backoff when absent.
- A timezone-specific 400 may retry once without `outlook.timezone`, through the same error/retry loop. A second rejection is reported normally.
- Calendar-window queries use `calendarView` so occurrences are expanded. Creation filters use `/me/events`, which supports `createdDateTime`; these results include that field. Follow `@odata.nextLink` for paging, with a defensive 200-page limit.
- `/instances` queries omit `$top` and `$orderby`; `next` takes the nearest returned occurrence within its search window. Local occurrence numbering is display-only: compute it only for supported daily patterns and weekly patterns with interval 1. Omit a number for more complex rules or dates that cannot be established reliably.
- Changing or deleting an occurrence affects that occurrence. Changing a series pattern targets the master and can reset exceptions. Pattern updates build a complete new recurrence range: omitting both end options means no end, so an agent preserving an existing cutoff/count must supply it explicitly.
- Conflict checking covers the full span of all-day events and an expanded window around timed events. `showAs=free` and cancelled events do not occupy time. `free` computes slots locally from events because personal accounts do not support `getSchedule`.
- Disable reminders with `isReminderOn: false`; a null minutes value is not a reliable way to clear them. Setting `--remind` also turns `isReminderOn` on. Reminder units follow the resulting event type: minutes for timed events, days for all-day events, with an all-day cap of 1826 days.
- Mailbox timezone lookup requests `MailboxSettings.Read`; unavailable permission falls back to the effective timezone. Sign-in also requests `Calendars.ReadWrite` and `User.Read`.
- Token renewal uses a cross-process lock and rechecks stored credentials to reduce concurrent refresh/write races. Importing authentication modules must not start device-code interaction.

## Output and i18n

JSON is the preferred agent interface. Each operation in `--json` mode writes one JSON value to stdout; diagnostics use stderr. Errors have `{"error": ..., "exit": 1}` and a nonzero exit; disconnected `status` retains its connection object. `--help` is text. JSON serialization uses ASCII escapes so Unicode survives Windows GBK pipes and is recovered by decoding.

Human output remains covered by structural tests. Result IDs use 🆔 with four leading spaces in lists, three in add, and none in read; read uses 🆕 plus a colon for a series master ID. Free slots use `HH:MM-HH:MM`. No listed slots alone cannot distinguish entirely busy from entirely free: use JSON. Conflict warnings can contain existing-event IDs and belong on stderr. In text mode, interactive prompts remain on stdout.

All user-visible messages go through `ocal_i18n.t()`. Language priority is `--lang` → `OCAL_LANG` → system detection. Fill both language tables; anchors and JSON keys are language-independent, while translated prose is not a parsing contract. Narrow-encoding text pipes replace unsupported emoji; do not rely on emoji extraction there.

Maintain documentation in English/default and Chinese/`.zh-CN` pairs. Both SKILL files keep the same English frontmatter description and metadata version. Use x.y.z: major for incompatible contracts, minor for new behavior, patch for maintenance. Sync examples and assertions when behavior changes; do not retain obsolete interface aliases solely for compatibility.

## Validation

Run from the project root with the dependencies and pytest installed:

```bash
python -m pytest tests/ -q
python -m compileall -q scripts
```

The offline suite mocks network/authentication. It covers strict dates, explicit timezone propagation and restoration, DST rejection, recurrence structure, query bounds, event operations, retry behavior, Unicode JSON, and i18n completeness. CI runs on Linux, Windows, and macOS with Python 3.10 and 3.13.

Agent-level evaluations are separate from unit tests: [trigger-eval.md](tests/trigger-eval.md) checks activation, [protocol-eval.md](tests/protocol-eval.md) checks extraction, and [skill-eval.md](tests/skill-eval.md) checks complete user outcomes in fresh sessions with a mock calendar. Record actual runs; a written evaluation set is not evidence that its scenarios passed.

The optional [live integration drill](tests/integration/README.md) uses `tests/integration/drill.py` against an explicitly named connected account:

```bash
python tests/integration/drill.py --account <expected-account-email> --confirm
```

It creates temporary test events and cleans up only IDs created by that run. It does not clear the account or discover deletion targets by title. Account checks and explicit confirmation protect the live entrypoint. This performs real writes and is separate from routine offline validation; consult its README before running it.

## API references

- [Event resource](https://learn.microsoft.com/en-us/graph/api/resources/event?view=graph-rest-1.0)
- [Calendar view](https://learn.microsoft.com/en-us/graph/api/calendar-list-calendarview?view=graph-rest-1.0)
- [Recurrence pattern](https://learn.microsoft.com/en-us/graph/api/resources/recurrencepattern?view=graph-rest-1.0) and [range](https://learn.microsoft.com/en-us/graph/api/resources/recurrencerange?view=graph-rest-1.0)
- [Event instances](https://learn.microsoft.com/en-us/graph/api/event-list-instances?view=graph-rest-1.0)
- [Timezone values](https://learn.microsoft.com/en-us/graph/api/resources/datetimetimezone?view=graph-rest-1.0)
- [Error handling](https://learn.microsoft.com/en-us/graph/errors) and [throttling](https://learn.microsoft.com/en-us/graph/throttling)
