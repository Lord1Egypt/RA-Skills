# Sands → Chronicle Sync

## When to Use

Run `sands.chronicle.sync` to push calendar events into Chronicle as persistent facts.
Called by cron weekly, or manually after significant calendar changes (new travel, appointments added).

## What Gets Synced

| Chronicle predicate | Event criteria |
|---|---|
| `traveling_to` | Multi-day events with non-SF location, OR events with travel keywords (flight, hotel, trip, stay, vacation, visit) + location |
| `had_appointment` | Medical appointments (keywords: doctor, Dr., UCSF, appointment, visit, video visit, patient, therapy, dentist, sleep study) |
| `attended_event` | Significant personal events (birthday, anniversary, celebration, wedding, concert, show, graduation) |

**Skip**: recurring work meetings, all-day busy/blocked/focus markers, cancelled events, generic logistics (payday, tax), duplicates (same summary+date).

## Lookback / Lookforward Window

- Past: 18 months from today
- Future: 6 months from today
- Total window: ~24 months centered on today (weighted toward future for upcoming travel)

## Execution Pattern (Cron-Safe)

Since `execute_code` is blocked in cron and MCP tools are unavailable in isolated sessions,
use **direct Python OAuth** + `write_file` + `terminal`:

```
Step 1: Write a query+classify script to /tmp/sands_chronicle_query.py
  - Import google_auth_mcp.get_service from <hermes-home>/scripts
  - Query all 3 calendars (personal, <third-party-name>, family) via Calendar API v3
  - Time window: 18 months back → 6 months forward from today
  - singleEvents=True, orderBy='startTime', maxResults=250, paginate
  - Deduplicate by summary + start time across calendars
  - Classify each event (see criteria table + pitfalls above)
  - Output JSON to stdout

Step 2: Run the script
  terminal("python3 /tmp/sands_chronicle_query.py > /tmp/sands_events_for_chronicle.json")

Step 3: Extract events array (wrapper outputs {events, errors, stats})
  terminal("python3 -c \"import json; d=json.load(open('/tmp/sands_events_for_chronicle.json')); json.dump(d['events'], open('/tmp/sands_events_clean.json','w'), indent=2)\"")

Step 4: Run ingest script
  terminal("python3 <hermes-home>/scripts/sands_chronicle_sync.py /tmp/sands_events_clean.json")

Step 5: Update config.json last_chronicle_sync timestamp + count
  - last_chronicle_sync = current timestamp
  - last_chronicle_sync_count = number of events imported

Step 6: Write evidence + action journal entries
  - evidence.jsonl: record result, counts, any errors
  - action.jsonl: record run_id, action, result, counts by type
```

**Timezone note:** Always use the correct DST offset for the target date when building
timeMin/timeMax. June = PDT (-07:00), January = PST (-08:00).

## Value Text Format

**traveling_to**: `"Trip to {location} — {date_range} — {hotel_or_event}. {context}."`
  Example: `"Trip to Provincetown, MA — Jul 1–5, 2026 — AWOL Hotel Provincetown. Shannon's birthday trip. Flights UA 2356 (SFO→BOS) and UA 2400 (BOS→SFO)."`

**had_appointment**: `"{appointment_type} with {provider} ({org}) — {date} — {location}"`
  Example: `"New patient visit with Dr. Emily Eng (UCSF Ophthalmology) — Apr 15, 2024 — 490 Illinois St, San Francisco"`

**attended_event**: `"{event_name} — {date} — {location_if_any}"`
  Example: `"Wedding Anniversary — Jul 6, 2026"`

## Input JSON Schema

```json
[{
  "google_event_id": "...",          // Google Calendar event ID
  "chronicle_type": "travel",        // travel | medical | personal | professional
  "predicate": "traveling_to",       // traveling_to | had_appointment | attended_event
  "value": "...",                    // Human-readable fact text
  "valid_from": "YYYY-MM-DD",        // Event start date
  "valid_until": "YYYY-MM-DD",       // Event end date (null for single-day)
  "confidence": 0.9,                 // 0.0–1.0
  "location": "...",                 // Raw location string (or null)
  "source_summary": "...",
  "source_calendar": "personal|<third-party-name>|family"            // Original calendar event title
}]
```

## Deduplication

The ingest script deactivates all prior `external_sands` facts for the predicates in the batch before re-importing. This means each sync is a clean re-import of the current window — no stale facts accumulate.

## Chronicle DB

`<hermes-home>/profiles/indigo/commons/db/chronicle/chronicle.db`
Script: `<hermes-home>/scripts/sands_chronicle_sync.py`

## Auth Note: Cron vs. Interactive Sessions

**Cron jobs (isolated sessions):** Use **direct Python OAuth** via `google_auth_mcp.get_service`.
MCP tools (`mcp_google_workspace_get_events`) are NOT available in isolated cron sessions.
The direct fallback at `<hermes-home>/scripts/google_auth.py` reads the same credential store
(`<gworkspace-creds>/credentials/`) and works reliably in cron mode.

**Interactive sessions:** Can use either MCP tools or direct Python. Both auth paths work.

The Python ingest script (`sands_chronicle_sync.py`) only writes to Chronicle DB — it does NOT need calendar auth.

## Classification Pitfalls (Learned from 2026-06-28 sync)

Keyword-based classification produces false positives from overlapping vocabulary:

1. **"Visit" is ambiguous** — Events like "Appointment: Visit at Watercourse Way Bath House Spa" contain
   both "visit" (travel keyword) AND "appointment" (medical keyword), AND have a location. These get
   classified as travel because travel has priority. **Fix: medical keywords should take priority over
   travel when the event title explicitly says "appointment" or a provider name appears.**

2. **Event titles that mention medical-sounding words but aren't medical** — "Milo's band Presidio Jazz Lab"
   was classified as medical because "appointment" appeared in the title on the family calendar. Always
   check whether the event is a calendar placeholder for a booking reminder vs. actual medical content.

3. **Birthday all-day events** — These generate a large volume of `attended_event` facts (196 of 455
   classified). They're accurate but may be noise-heavy. Consider whether ALL birthdays need Chronicle
   facts or just family/close-friend birthdays.

4. **Multi-day all-day events at non-SF locations** — These correctly classify as travel, but the
   "location" field is sometimes missing for all-day events, making the fact text less useful
   ("Trip to Unknown location"). When location is missing, try to infer from the summary.

## Calendars to Query

| Calendar | ID |
|---|---|
| Personal | `<user-google-email>` |
| <third-party-name> | `<third-party-email>` |
| Family | `<family-calendar-id>@group.calendar.google.com` |

Skip: Work (`<user-handle>@<employer>.com`) — read-only free/busy only, no event details.
