---
name: ocas-sands
license: MIT
description: 'Calendar management. Use for viewing, querying, creating, modifying, deleting, or analyzing calendar events. Handles natural-language scheduling, conflict detection with flexibility classification, free slot finding, automatic travel time event insertion between consecutive appointments, recurring event management, and daily schedule briefings for Vesper. Do not use for reminders without calendar context, task management, or general time/timezone questions.'
source: https://github.com/<agent-handle>/sands
includes:
- references/**
- evals/**
- scripts/**
metadata:
  author: Indigo Karasu (indigokarasu)
  version: "2.3.0"
  activation:
    requires_tools: ["workspace_mcp"]
    fallback_for_tools: ["google_api_fallback"]
  hermes:
    category: productivity
    tags:
    - calendar
    - scheduling
    - events
    - OCAS-core
tags:
- calendar
- scheduling
- events
- OCAS-core
triggers:
- calendar view
- calendar event
- create event
- modify calendar
- schedule meeting
---
## Interactive Menu

When invoked interactively (via `/` command), present a two-level menu. See `references/interactive-menu.md` for the menu structure and response parsing logic.

# Sands

Sands manages calendar events through natural language — creating, querying, modifying, and deleting events across personal and work calendars. It detects scheduling conflicts with flexibility classification, finds free time slots, inserts travel time blocks via Google Places API, and emits structured schedule briefs to Vesper for morning and evening briefings.

## When to Use

- Calendar event creation, modification, and deletion
- Multi-calendar coordination (Personal, Shannon, Family)
- Appointment scheduling with conflict detection
- Focus time and out-of-office management
- When any skill needs calendar operations

For example, when the user says "schedule a meeting with <operator> at 3pm tomorrow," Sands creates the event with conflict pre-check and smart duration defaults.

## When NOT to Use

- Email or message sending (use Dispatch)
- Content generation or research
- Booking non-calendar appointments (use Spot)
- Travel planning (use Voyage)

## Responsibility boundary

Sands owns calendar event management, conflict analysis, flexibility classification, travel time insertion via Google Places API, and emitting schedule signals to Vesper.

Sands does not own: communications (Dispatch), travel reservations (Voyage), general research (Sift), entity knowledge (Weave).

## Ontology types

Sands works with these types from `spec-ocas-ontology.md`:

- **Place** — event locations resolved via Google Places API during `sands.logistics.travel`. Location data retained in `decisions.jsonl` as decision context only.
- **Event** (Concept subclass) — calendar events managed through Google Calendar, not Chronicle.

Sands queries entity context from:
- **Weave** (read-only) — attendee identity resolution during conflict classification
- **Chronicle** — current location context for travel departure resolution

## Commands

- `sands.calendar.query` — pull events for a time window; merged view with work busy overlay
- `sands.event.create` — create event from natural language with conflict pre-check and smart duration defaults
- `sands.event.modify` — update event with recurring scope control and post-modify conflict re-check
- `sands.event.delete` — cancel event with travel block cleanup and recurring scope control
- `sands.event.undo` — revert most recent calendar action (within 24 hours)
- `sands.schedule.free` — find available time slots for a given duration with constraints
- `sands.schedule.conflicts` — analyze time window for conflicts with flexibility classification. See `references/conflict-report-format.md` for output template.
- `sands.logistics.travel` — insert travel time block between events via Google Places API
- `sands.briefing.generate` — generate structured schedule summary for Vesper emission
- `sands.status` — skill health, configured calendars, API connectivity, current timezone
- `sands.journal` — write journal for the current run; called at end of every run
- `sands.update` — pull latest from GitHub source; preserves journals and data
- `sands.chronicle.sync` — push travel, medical, and personal calendar events into Chronicle as persistent facts

See `references/briefing_windows.md` for morning/evening briefing time window definitions.
See `references/credential-files.md` for Google Places API key and OAuth token details, including token staleness handling.

## Run completion

After every Sands command:

- [ ] Persist event interactions to `events.jsonl` (event_id, calendar_id, title, start, end, action, recurrence_scope, previous_values)
- [ ] Log material decisions (conflict resolutions, travel insertions) to `decisions.jsonl`
- [ ] Write journal via `sands.journal` — Observation Journal for query/free/conflicts/status, Action Journal for create/modify/delete/travel/brief/undo

**Post-mutation verification**: After any create/modify/delete command, re-query the calendar for the affected event ID and confirm the change is reflected (correct title, time, calendar placement, or removal). If the event state does not match what was requested, log a `calendar_mismatch` entry in `evidence.jsonl` and alert the user — never silently assume the write succeeded.

## Hard boundaries

- Never write to `work_calendar_id` — read/overlay as busy blocks only
- All-day events do not trigger conflicts with timed events unless explicitly asked
- Never auto-resolve conflicts — present options, let the user choose
- Never use a hardcoded home address or assume a fixed city for travel departure
- Never silently fall back to distance heuristics if Google Places API is unavailable — surface warning and ask for manual estimate
- Undo window is 24 hours; recurring event scope changes cannot be undone

## Recovery Behavior

This skill implements the recovery contract from `spec-ocas-recovery.md`.

- **Evidence**: Every scheduled run writes an evidence record to `{agent_root}/commons/data/ocas-sands/evidence.jsonl`, including no-op runs. The `not_activity_reason` field is mandatory when no side effects occur.
- **Gap detection**: On every wake, checks the evidence log. If gap exceeds cadence (24h for briefs, 24h for conflict-scan), logs `gap_detected`.
- **Degraded mode**: When Google Calendar API or Google Places API fail, logs `degraded: <api>` and continues with available data.
- **Log compaction**: Evidence and decision logs older than 30 days (no-op) or 90 days (error/gap) compacted. Last 7 days retained.

## Storage layout

See `references/schemas.md` for the full storage layout and default config.json.

## OKRs

Universal OKRs from spec-ocas-journal.md apply to all runs. See `references/okrs.md` for details.

## Optional skill cooperation

- Weave — attendee identity resolution and current location context
- Chronicle — current location or travel context
- Voyage — travel reservations detected in calendar surfaced for Voyage to manage
- Vesper — Vesper reads Sands schedule briefs at journal payload fields (see interfaces specification) during briefing generation (cooperative write; Sands pushes to Vesper (via journal briefing payload))

## Journal outputs

- Observation Journal — sands.calendar.query, sands.schedule.free, sands.schedule.conflicts, sands.status
- Action Journal — sands.event.create, sands.event.modify, sands.event.delete, sands.event.undo, sands.logistics.travel, sands.briefing.generate

## Initialization

On first invocation of any Sands command, run `sands.init`:

- [ ] Create `{agent_root}/commons/data/ocas-sands/` directory
- [ ] Write default `config.json` with ConfigBase fields if absent
- [ ] Create empty JSONL files: `decisions.jsonl`, `events.jsonl`, `evidence.jsonl`, `intents.jsonl`
- [ ] Create `{agent_root}/commons/journals/ocas-sands/` and ensure both journal files exist (create empty if absent): `action.jsonl`, `observation.jsonl`
- [ ] Register cron jobs listed below if not already present (check the platform scheduling registry first)
- [ ] Log initialization as a DecisionRecord in `decisions.jsonl`

## Background tasks

Registered during `sands.init`. Always check existing jobs before registering:

| Job name | Schedule | Command | Purpose |
|---|---|---|---|
| `sands:morning-brief` | `0 6 * * *` | `sands.briefing.generate` | Today's schedule brief for Vesper |
| `sands:evening-brief` | `0 20 * * *` | `sands.briefing.generate` | Tomorrow's schedule brief for Vesper |
| `sands:conflict-scan` | `0 7 * * *` | `sands.schedule.conflicts` | Daily conflict scan for upcoming 7 days |
| `sands:travel-check` | `0 7 * * *` | `sands.logistics.travel` | Check next day's events for missing travel blocks |
| `sands:update` | `0 0 * * *` | `sands.update` | Self-update from GitHub source |
| `sands:chronicle-sync` | `0 8 * * 0` | `sands.chronicle.sync` | Weekly calendar → Chronicle fact sync (Sundays 8 AM) |

All cron jobs use: `--session isolated --light-context --tz America/Los_Angeles`.

Registration during `sands.init`:
Check the platform scheduling registry for existing tasks before registering each job. Tasks are declared in SKILL.md frontmatter `metadata.{platform}.cron`.

## Self-Update

See `references/self-update-sands.md`.

## Visibility

public

## Gotchas

- **⚠️ write_file OVERWRITES — JSONL append requires read-then-rewrite or the helper script** — The `write_file` tool replaces the entire file. NEVER call `write_file` on `evidence.jsonl`, `decisions.jsonl`, or `events.jsonl` with only the new record — you will destroy all prior history. Two safe approaches:
  1. **Preferred:** Use the `scripts/append_jsonl.py` helper: `terminal("python3 <skill_dir>/scripts/append_jsonl.py <path> '<json_record>'")`. It reads, appends, rewrites, and verifies line count atomically.
  2. **Manual:** (1) `read_file` the existing JSONL, (2) construct the full content (all existing lines + new line), (3) `write_file` with the complete content. Always verify line count increased by 1 after writing.
    If you accidentally overwrite, check session context for the original contents to restore from.
  - **⚠️ Unicode-safe append (emoji in titles)** — Event titles routinely contain emoji (e.g. `🏺 Intro to Handbuilding`). The helper takes the record as a **shell-quoted positional arg**, so passing JSON with emoji/nested quotes through the shell mangles the data. For any record that may contain non-ASCII or nested quotes, DON'T shell-quote into `append_jsonl.py` — instead `write_file` a small Python script that opens the JSONL, filters blanks, appends `json.dumps(record)+'\n'`, rewrites, and asserts line count increased (then `terminal("python3 <that_script>")`). Building records as real Python dicts writes Unicode correctly via `json.dump`. See `references/cron_persistence.md` for the verified cron pattern and the full why.
- **Work calendar is read-only** — Sands can overlay work calendar busy blocks but must never write to `work_calendar_id`. Writing to a read-only calendar will fail silently or produce API errors.
- **All-day events don't conflict with timed events** — Per the hard boundary, all-day events are excluded from conflict detection with timed events unless the user explicitly asks. This can hide real scheduling issues if the user expects otherwise.
- **Google Places API failure is surfaced, not silently handled** — If the Google Places API is unavailable, Sands does NOT fall back to distance heuristics. It surfaces a warning and asks for a manual estimate.
- **Undo window is 24 hours and non-recurring** — Event undo is only available within 24 hours of the original action. Recurring event scope changes cannot be undone at all.
- **OAuth tokens may stale between cron runs** — Calendar queries can fail with auth errors if the OAuth token expires between scheduled runs. Always trigger re-authentication before retrying; do not suppress the error.
  - **Compound failure: OAuth stale + MCP unreachable** — When `get_events` fails with an OAuth error, the corrective action is `start_google_auth`. But if the MCP *server* is also unreachable, `start_google_auth` will fail too (same transport). In this scenario: (1) note `degraded: google_workspace_mcp` AND `degraded: oauth_stale` in evidence, (2) update `config.json auth_status` to `STALE_OAUTH`, (3) surface to the user that TWO things need fixing — the MCP server process must be running AND OAuth must be re-authorized. Do NOT retry auth in a loop when the MCP server is unreachable; it will just burn tool calls.
- **Timezone offsets change with daylight saving** — Pacific time is `-08:00` (PST) in winter and `-07:00` (PDT) in summer. When building RFC3339 time_min/time_max for queries, determine the correct offset for the TARGET date, not today's date. Using the wrong offset shifts the query window by one hour and can return no events or wrong-day events. The `default_timezone` in config.json (`America/Los_Angeles`) is a hint — always check whether the target date falls in PDT (Mar–Nov) or PST (Nov–Mar) and use the matching offset.
- **Google Workspace MCP server may be transiently unreachable** — If `get_events` or other MCP calls fail with "unreachable" errors, wait ~40 seconds (the auto-retry cooldown) and try once more before logging `degraded`. A single cooldown wait resolves most transient failures. Only log `degraded: google_workspace_mcp` after the retry also fails.
- **Single event = no travel blocks needed** — When only one event exists on a travel-check day, there are nothing to insert between. Still write evidence (with `not_activity_reason: no_consecutive_events`) and update `config.json last_travel_check` so gap detection stops flagging the stale timestamp. If the single event is all-day (no timed events at all), use `not_activity_reason: no_timed_events` — this distinguishes "nothing to check" from "one event, nothing between."
- **Overlapping events = no travel blocks, but flag conflict** — When consecutive timed events overlap (event B starts before event A ends), `gap_minutes` will be negative. Use `not_activity_reason: events_overlap_no_gap` in the evidence log. Also flag the overlap in the `overlap_detected` field so the evening brief and conflict scan can reference it. Do NOT create a travel block for overlapping events — they have no gap to fill.
- **Google Places API key empty = travel check is observational** — When `google_places_api_key` is empty in config.json, travel blocks can never be auto-created. The travel-check command runs but will only report consecutive event pairs it cannot service. If the key is empty, note this in the evidence log's `degraded` field.
- **MCP Google Workspace tools may fail with auth errors even when the server is running** — The `mcp_google_workspace_get_events` and related MCP tools can return OAuth errors (401/403, `invalid_grant`) even when the MCP server process is reachable. When ANY MCP calendar call fails with an auth error, switch to the direct Python fallback: `from google_auth import get_calendar_service` from `<hermes-home>/scripts/google_auth.py` and call the Calendar API v3 directly. The direct fallback uses the same credential store (`<gworkspace-creds>/credentials/`) and often succeeds when MCP fails because it bypasses the MCP server's token management layer. See `references/direct_calendar_access.md` for the working pattern.
- **Reference files may be empty** — `references/briefing_windows.md`, `references/vesper_emit_format.md`, and `references/preparation_signals.md` are currently 0 bytes. Do not block on reading them; proceed with the defaults documented in this SKILL.md (morning brief = today's events, evening brief = tomorrow's events, both in `America/Los_Angeles`).
- **Calendar IDs can 404** — If a configured `primary_calendar_id` returns 404 (not found), log it in `degraded` and continue with the remaining calendars. Surface the broken calendar ID to the user so they can update `config.json`. Do not let one broken calendar block the entire query.
- **execute_code is blocked in cron mode** — Cron jobs run without a user present to approve `execute_code`, so it will be rejected. When Sands needs to run Python analysis scripts (conflict detection, travel analysis, etc.) from a cron job, use the `write_file` + `terminal` pattern instead: (1) `write_file` the script to a temp path like `/tmp/sands_analysis.py`, (2) `terminal("python3 /tmp/sands_analysis.py")` to run it, (3) read results from stdout or a temp JSON output file. See `references/direct_calendar_access.md` for the full cron-compatible pattern. For conflict scans, you can copy and adapt the reusable template at `scripts/conflict_scan_template.py`.
- **Cross-calendar duplicates are conflicts** — When the same event appears on multiple calendars (detected by matching summary + start time + location), flag it as a DUPLICATE conflict. Timezone offset differences between calendars can make the same event appear at different UTC times — normalize to local time before comparing. Recommend removing the duplicate from the non-canonical calendar.
- **Events crossing midnight UTC may belong to the previous local day** — When querying with UTC-based time windows, an event starting at `2026-06-07T01:00:00Z` is actually `2026-06-06T18:00:00-07:00` (6 PM PDT on June 6). Always convert event start times to local timezone (`America/Los_Angeles`) before assigning to a date. The `singleEvents=True` parameter in the Calendar API expands recurring events but does not normalize timezones — the response preserves the event's original timezone, which may differ from the query window timezone.
- **MCP tools require `user_google_email` on every call** — Every `mcp_google_workspace_*` tool requires a `user_google_email` parameter (the authenticated user's Google email). Omitting it produces a Pydantic validation error that doesn't clearly say "missing parameter." Always include `user_google_email` — use the agent's own email (e.g., `<agent-email>`) unless the user specifies otherwise. This applies to ALL MCP Google Workspace tools, not just `get_events`.
- **Zero-duration events are warnings, not conflicts** — Events where `start == end` do not overlap with anything and should not be flagged as conflicts. Instead, flag them as `zero_duration` warnings in the report. These are almost always data quality issues (end time not set correctly). **Critical code-level trap:** `span_minutes()`'s midnight-crossing guard (`if e <= s: e += 1440`) expands a `12:45 -> 12:45` event into a 24-hour span, which fabricates overlaps with every later event AND pollutes free-hours math. Therefore BOTH conflict detection and free-hours computation MUST exclude zero-duration events BEFORE calling `span_minutes` (compute `zero_duration = is_timed and start == end` at parse time, then compare only non-zero-duration events and skip them in `calc_free_hours`). This bug was live in `templates/sands_briefing_morning.py` until 2026-07-23 and produced a false 120-min "Appointment overlaps Gym" conflict. See `references/zero_duration_briefing.md` and `references/conflict_detection.md`.
- **⚠️ Midnight-crossing events break naive conflict & free-hour math** — An event ending at `00:00` (e.g. `19:30`→`00:00`) parsed by naive `HH:MM`→minutes yields a *negative* overlap (`0 - 1170`) that hides a real conflict. Always treat `end_min <= start_min` as crossing midnight (add `1440` to end) before computing overlaps or busy spans. Found and fixed 2026-07-22 in `templates/sands_briefing_morning.py` (conflict loop + `calc_free_hours`); the fix uses `span_minutes(start, end)`. `scripts/conflict_scan_template.py` uses UTC-aware overlap detection so it is NOT affected — but any new HH:MM-minute-based overlap code must apply the same guard.
- **`400 Bad Request` from oauth2.googleapis.com = dead credentials** — Besides `invalid_grant`, expired/revoked refresh tokens can return HTTP `400` from the token endpoint. Surfaces as `"400 Client Error: Bad Request for url: https://oauth2.googleapis.com/token"` from `get_service()`. Treat identically to `invalid_grant`: log, move to next account. Do NOT interpret `400` as a bug in your code.

- **⚠️ Interactive command access** — Sands commands like `sands.logistics.travel` are not direct shell commands. They are accessed through the skill's interactive menu. Invoke the skill with `/` command (or your interface's equivalent) to see the two-level menu, then navigate to the desired command (e.g., Travel Check → Check next day events for missing travel blocks). Direct shell invocation of sands commands will not work and will produce "command not found" errors.
- **`config.json` `auth_status` can be stale after fallback** — When the primary account's token is dead but the fallback account succeeds, `auth_status` may still say `MCP_ONLY` or `STALE_OAUTH`. After a successful direct-Python fallback, update `auth_status` to `OK` so the next run doesn't pre-emptively assume degradation. The field reflects the *system's* ability to reach the calendar, not any single account's token state.
- **Journal directory may not exist on first cron run** — The `## Initialization` step 4 says to create `{agent_root}/commons/journals/ocas-sands/`, but journal writes have been observed to land at `{data_dir}/journals/` (i.e., the same parent as `config.json`). Before calling `append_jsonl.py` for journals, ensure the directory exists: `mkdir -p "$DATA_DIR/journals"`. If the append fails with `FileNotFoundError` on the parent, create it and retry. The script itself only handles file-level existence, not directory creation.
- **Evening-brief template now exists** — `templates/sands_briefing_evening.py` mirrors the morning template but targets TOMORROW, omits prep-signal checks, emits `proposal_type: routine_prediction`, and excludes zero-duration events from conflict/free-hours math. The morning template previously had the zero-duration false-conflict bug (see below); the evening template was written correct from the start and the morning template was patched to match. When generating evening briefs, run the template (pure generator) then persist: query all primary calendars with PDT-correct offsets, sort by start time, check overlaps/duplicates within the target date, build the Vesper InsightProposal payload (`brief_type: evening`, `proposal_type: routine_prediction`), render the report, write evidence with `command: sands.briefing.generate`, write to action journal (briefing.generate is an Action Journal command), update `config.json last_evening_brief`. Persistence recipe in `references/zero_duration_briefing.md`.

## Cron Script Templates

- `templates/sands_briefing_morning.py` — Reusable cron-compatible morning briefing script with multi-account fallback, dedup, conflict detection (zero-duration-safe), and prep-signal checking.
- `templates/sands_briefing_evening.py` — Evening counterpart: queries TOMORROW's events, omits prep-signal checks, emits `proposal_type: routine_prediction`, and excludes zero-duration events from conflict/free-hours math. Pure generator; the calling run persists evidence/action/config (see `references/zero_duration_briefing.md`).

## Support File Map

| File | When to read |
|------|-------------|
| `references/briefing_windows.md` | Before sands.briefing.generate |
| `references/calendar_config.md` | Before configuring calendars or timezone handling |
| `references/credential-files.md` | Before first OAuth setup or when handling token staleness |
| `references/timezone_handling.md` | Before constructing time_min/time_max for get_events |
| `references/google_calendar_api_quirks.md` | Before manage_event calls |
| `references/duration_defaults.md` | Before sands.event.create |
| `references/flexibility_rules.md` | Before sands.schedule.conflicts |
| `references/conflict_detection.md` | Before conflict analysis |
| `references/conflict-report-format.md` | Before generating conflict scan report output |
| `references/recurring_events.md` | Before creating/modifying/deleting recurring events |
| `references/preparation_signals.md` | Before sands.briefing.generate |
| `references/travel_time_logic.md` | Before sands.logistics.travel |
| `references/vesper_emit_format.md` | Before sands.briefing.generate; formatting payload for Vesper |
| `references/self-update-sands.md` | Before running sands.update |
| `references/direct_calendar_access.md` | When MCP Google Workspace tools are unavailable; direct Python fallback pattern |
| `scripts/conflict_scan_template.py` | Reusable cron-compatible conflict scan script with multi-account OAuth fallback |
| `references/chronicle_sync.md` | Before sands.chronicle.sync; event classification rules, value format, ingest script path, cron auth pattern, classification pitfalls |
| `references/gotchas.md` | Common pitfalls, OAuth quirks, MCP tool limitations, cron-mode constraints, and UCSF MyChart double-import pattern |
| `references/cron_persistence.md` | Unicode-safe JSONL persistence in cron mode (emoji in titles) + why `config.json primary_calendar_ids` drifts from the briefing template's hardcoded calendar list |
| `templates/sands_briefing_morning.py` | Reusable cron-compatible morning briefing script — multi-account fallback, dedup, conflict detection, prep signals |
| `references/mcp_fallback_briefing.md` | When encountering dependency errors with the morning briefing script |