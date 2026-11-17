# Calendar, schedule, time

Three distinct surfaces that all happen to involve time:

- **`huly calendar …`** — calendar events (one-off and recurring) and the calendar objects (containers) themselves.
- **`huly schedule …`** — owner-availability schedules (working hours, meeting duration).
- **`huly time …`** — time tracking on issues (billable hours).

---

## Decision: which calendar command do I want?

This is the most-named-confused surface:

| You say…                                         | Use                                                         |
| ------------------------------------------------ | ----------------------------------------------------------- |
| "show my calendars" / "list available calendars" | `huly calendar calendars`                                   |
| "list events" / "what's on my calendar today"    | `huly calendar list`                                        |
| "get event X"                                    | `huly calendar get X` (returns the EVENT, not the calendar) |
| "create an event"                                | `huly calendar create`                                      |
| "create a calendar (the container)"              | `huly calendar create-calendar`                             |
| "list recurring events"                          | `huly calendar recurring`                                   |
| "show instances of a recurring event"            | `huly calendar recurring-instances <ref>`                   |
| "define my working hours / availability"         | `huly schedule create`                                      |
| "log time on TSK-1" / "I spent 30 min on…"       | `huly time log --issue TSK-1`                               |

**Critical naming trap:** `huly calendar get <ref>` returns an **EVENT**, not a calendar object. To get a calendar by id, use `huly calendar calendars --json | jq '.[] | select(._id == "<id>")'`.

---

## Calendar commands (events)

### Discover

```bash
huly calendar calendars                          # list calendar objects (not events)
huly calendar calendars --json | jq -r '.[] | "\(.name)\t\(._id)"'

huly calendar list --json                        # all events
huly calendar list --start "$(date -u +%Y-%m-%dT00:00:00Z)" --end "$(date -u -d 'tomorrow' +%Y-%m-%dT00:00:00Z)" --json
huly calendar list --calendar "Work" --json      # filter by calendar (name or id)
huly calendar list --limit 50 --offset 0 --json

huly calendar get <event-id> --json
huly calendar get <event-id> --markdown

huly calendar recurring --json
huly calendar recurring-instances <recurring-event-id> --json
huly calendar recurring-instances <recurring-event-id> --start ... --end ... --limit 100 --json
```

`--start` / `--end` filter by `startDate >= AND dueDate <=` (overlap semantics).

### Create an event

```bash
huly calendar create \
  --title "Sprint planning" \
  --start 2026-07-08T14:00:00Z \
  --end   2026-07-08T15:00:00Z \
  --calendar-id "Work" \
  --attendee alice@example.com \
  --location "Room 4" \
  --description "agenda" \
  --body $'# Agenda\n- …'
```

**Required:** `--title`, `--start`, `--end`. The CLI parses dates with `new Date(value).getTime()`; throws `Validation` on NaN.

**Defaults:**

- `--calendar-id` falls through: `calendar:class:PrimaryCalendar` first, else first non-hidden Calendar, else throws `no calendars available`.
- `attachedTo`: defaults to current user's Person (`attachedToClass = contact:class:Person`) so the event shows in the user's calendar.
- `access: 'owner'`, `visibility: 'public'`, `blockTime: false`.
- `eventId: random base36 timestamp`.

**`--rrule`** for recurring events:

```bash
huly calendar create \
  --title "Daily standup" \
  --start 2026-07-08T09:00:00Z \
  --end   2026-07-08T09:15:00Z \
  --rrule "FREQ=DAILY;COUNT=14"
```

Recognized RFC 5545 keys: `FREQ`, `INTERVAL`, `COUNT`, `UNTIL` (date), `BYDAY, BYMONTH, BYHOUR, BYMINUTE, BYSECOND, BYMONTHDAY, BYYEARDAY, BYWEEKNO, BYSETPOS` (numeric arrays). Unknown keys pass through as strings.

`--time-zone` defaults to `UTC`. **There is NO `--time-zone` flag exposed on `huly calendar create`** — it's read via `--set time-zone=...` (raw), or live with the default `UTC`.

**`--all-day`:** boolean. Sets `allDay: true`; `blockTime: false` automatically.

**EXDATE/RDATE always empty.** The CLI initializes `exdate: []` and `rdate: []` on every new recurring event (`resources/calendar.ts:463-464`), but exposes no flag to add entries, so skipping individual occurrences of a recurring series isn't possible via the CLI.

### Update

```bash
huly calendar update <event-id> --title "New title"
huly calendar update <event-id> --start 2026-07-08T15:00:00Z
huly calendar update <event-id> --location "Room 5"
huly calendar update <event-id> --attendee bob@example.com
```

**Note:** the CLI does NOT expose `--rrule`, `--calendar-id`, `--time-zone`, or `--visibility` as update flags. **These fields are only settable via raw RPC.** Confirm with the user out loud before invoking `huly ws updateDoc`; the recipe is the only path but bypasses CLI safety checks.

```bash
# Advanced — confirm with user first
huly ws updateDoc '["calendar:class:Event", "<space>", "<id>", {"$set":{"visibility":"freeBusy"}}]'
```

`--start` update writes BOTH `date` AND `startDate` (a bug fix; older versions only wrote `startDate`).

### Delete

```bash
huly calendar delete <event-id>                            # single
huly calendar delete <e1> <e2> <e3> --yes                 # REQUIRED --yes for multiple
```

Tries `calendar:class:Event` first, falls back to `calendar:class:ReccuringEvent`.

---

## Calendar containers

```bash
huly calendar create-calendar --name "Work" --description "…" --private false --access public
huly calendar delete-calendar "Work"
```

**Defaults:** `visibility: 'public'`, `access: 'owner'` (note: help text says `owner|team|public` but the CLI hard-codes `owner` if `--access` is omitted), `private: false`, `hidden: false`, `description: ''`.

Always creates a new Calendar doc — no `find-or-create` path. If you want idempotency, check first:

```bash
huly calendar calendars --json | jq -r '.[] | select(.name == "Work") | ._id'
```

---

## Recurring event model

| Concept                             | Class                                                      | Notes                                                                     |
| ----------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------- |
| Recurring event definition          | `calendar:class:ReccuringEvent` (typo preserved in source) | Has `rules[]`, `originalStartTime`, `timeZone`, `exdate: []`, `rdate: []` |
| Recurring instance (per-occurrence) | `calendar:class:ReccuringInstance`                         | Has `recurringEventId`, `originalStartTime`, `virtual`, `isCancelled`     |
| One-off event                       | `calendar:class:Event`                                     | Plain event                                                               |

**Always-empty arrays:** the CLI initializes `exdate: []` and `rdate: []` on every new recurring event. EXDATE/RDATE have NO CLI exposure.

**List recurring definitions:**

```bash
huly calendar recurring --json
huly calendar recurring-instances <recRef> --json
```

---

## Schedule (owner availability)

```bash
huly schedule list --json
huly schedule get <ref> --json
huly schedule create \
  --title "Alice's working hours" \
  --owner <alice-person-uuid> \
  --time-zone "America/Los_Angeles" \
  --description "9-5 weekdays" \
  --duration 30 \
  --interval 15
huly schedule update <ref> --title "…" --time-zone "Europe/Berlin" --duration 45
huly schedule delete <ref>
```

**Required on create:** `--title`, `--owner <person-uuid>`, `--time-zone`.

**Critical:** `--owner` here is a **Person UUID**, NOT an email. This differs from `huly action create --owner` (which takes an email). Get the UUID via `huly user get --json | jq -r '._id'`.

**Defaults:** `--duration 30` (minutes), `--interval 15` (minutes).

**Common pitfall:** Schedule (availability) ≠ `action schedule` (which creates a WorkSlot on a todo). Different namespaces entirely.

---

## Time tracking

See `references/issues-and-todos.md` for the full state-machine context. Quick reference:

```bash
huly time list --issue TSK-1 --json
huly time list --start 2026-06-01T00:00:00Z --end 2026-06-30T23:59:59Z --json
huly time log --issue TSK-1 --minutes 30 --description "wired up CI"
huly time log --issue TSK-1 --hours 2 --description "pair prog"
huly time log --issue TSK-1 --minutes 30 --date 2026-06-15T14:00:00Z    # backdate
huly time report TSK-1                            # alias for `time list --issue`, per-issue only
huly time delete <entry-ref>
huly time delete <e1> <e2> --yes                  # REQUIRED --yes for multiple
```

**Critical: time stored as man-hours.** Value is `minutes / 60`.

**Parent chain recompute is automatic.** Logging time on a sub-issue updates `reportedTime` / `remainingTime` on the sub-issue AND walks up the parent chain to the issue's ancestor. No opt-out.

**`time report <issue>`** is per-issue only; there is no workspace-wide or date-range rollup. Use `time list --start ... --end ... --json | jq` for aggregates.

**Confusion:** passing both `--hours` and `--minutes` throws `Validation: pass only one of --minutes or --hours` (`resources/time.ts:86-88`). Pick one.

---

## Visibility for Google Calendar sync (FYI)

The platform maps `visibility ↔ Google transparency`:

- Google `transparency:transparent` ↔ Huly `visibility:freeBusy`
- Huly `private` ↔ Google `private`

The CLI sets `visibility: 'public'` by default. **To set `freeBusy` or `private`, only raw RPC works** (`huly ws updateDoc`); confirm with the user first — see the `calendar update` notes above.

---

## Common task recipes

### Schedule a meeting and invite someone

```bash
# Create the event with attendee
huly calendar create \
  --title "1:1 with Alice" \
  --start 2026-07-08T15:00:00Z \
  --end 2026-07-08T15:30:00Z \
  --attendee alice@example.com \
  --location "Zoom"
```

If the user wants this to block their calendar:

```bash
# CLI sets blockTime:false by default; flip via raw update.
# Advanced — confirm with the user first; raw RPC bypasses CLI safety checks.
huly ws updateDoc '["calendar:class:Event", "calendar:space:Calendar", "<id>", {"$set":{"blockTime":true}}]'
```

### Daily standup at 9am for two weeks

```bash
huly calendar create \
  --title "Daily standup" \
  --start 2026-07-08T09:00:00Z \
  --end 2026-07-08T09:15:00Z \
  --rrule "FREQ=DAILY;COUNT=14"

# Verify what got generated
huly calendar recurring --json
huly calendar recurring-instances <rec-id> --json | jq 'length'
# Should be 14.
```

### "Skip next Monday's standup"

> **Advanced — confirm with the user before invoking.** There is no CLI surface for this. EXDATE is silently ignored. The raw-RPC fallback below is irreversible and bypasses CLI safety checks.

Options:

- Delete the one instance via `huly ws findAll '["calendar:class:ReccuringInstance",{"recurringEventId":"<id>","originalStartTime":<ms>}]'` and `huly ws tx` with a `removeDoc`. **Confirm with the user out loud before invoking; there is no CLI confirmation prompt on raw RPC.**
- Or accept that all instances will exist.

### "Show me everything happening today"

```bash
START="$(date -u +%Y-%m-%dT00:00:00Z)"
END="$(date -u -d 'tomorrow' +%Y-%m-%dT00:00:00Z)"
huly calendar list --start "$START" --end "$END" --json \
  | jq -r '.[] | "\(.startDate / 1000 | strftime("%H:%M"))\t\(.title)\t\(.location // "")"'
```

### Log time and check the parent chain recomputed

```bash
huly time log --issue TSK-1 --minutes 30 --description "wired up buildkite"

# Sub-issue TSK-1 should show 30min reported
huly issue get TSK-1 --json | jq '.reportedTime'

# If TSK-1 has a parent issue TSK-0, check it too:
huly issue get TSK-0 --json | jq '.reportedTime'
# Should also have been recomputed (no opt-out).
```

---

## Gotchas

- **`calendar get <ref>` returns an event, NOT a calendar object.** Most common mistake.
- **`calendar create-calendar` always creates a new doc.** No `find-or-create`. Use `calendar calendars --json | jq` to check first.
- **`--rrule` parses multi-value keys as comma-separated numeric arrays.** Unrecognized keys pass through as strings; the server validates them.
- **EXDATE/EXRULE — silently ignored.** No way to skip one occurrence of a recurring event.
- **`--all-day` events do NOT block time** (`blockTime: !allDay` in the underlying create).
- **`--time-zone` not exposed as a flag on `calendar create`.** Defaults to `UTC`. Override via raw update.
- **Schedule `--owner` is a Person UUID, not an email.** Different from `action --owner` which is email.
- **Time value stored as man-hours.** So a 30-minute entry shows up as 0.5h.
- **`time report` is per-issue only.** Don't try to scope it to a date range, project, or workspace — it'll fail silently and return the same as `time list --issue`.
- **No calendar "settings" or "preferences" command on the CLI.** Access via `huly ws`.
- **Visibility on calendar events**: always 'public' by default; 'freeBusy' and 'private' exist but require raw update to set.
- **Meeting slot creation:** `action schedule` (todo scheduler) and `schedule create` (owner availability) are TWO different things, both named "schedule" in CLI help text. Don't conflate.
- **`huly calendar delete` cascade-deletes events inside recurring instances?** No — recurring instances are separate docs. The delete only removes the parent (Event or ReccuringEvent).
- **`huly calendar recurring-instances`** filters by `date` field, not `startDate`. For consistency with `calendar list`, this is mildly confusing.
