# Homebase

A WhatsApp-based household coordinator for families, built as a native OpenClaw skill. The OpenClaw agent IS the intelligence — it reads messages, reasons about them, and calls Python data tools via bash. Homebase is model-agnostic: whichever model OpenClaw is configured with (Claude, Gemma, GPT, Llama, ...) does the reasoning. No LLM SDK is bundled in this skill.

Clone, edit `config.json`, authorize Google in the `gog` CLI, run. Zero Python code changes.

---

## What It Does

**Calendar & Schedule**
- Syncs Google Calendar into a local cache (`calendar_data/family_calendar.json`) through the `gog` CLI — 1 day back, 30 days forward, every `enabled` entry in `supported_calendars`
- **No calendar tools.** All eight (`get_events_for_date`, `get_events_for_range`, `get_next_event`, `get_tomorrow_events`, `check_calendar_for_date`, `add_calendar_event`, `update_calendar_event`, `delete_calendar_event`) were deleted on 2026-09-07 when Google access moved to `gog`. The agent reads and writes the calendar with the `gog` skill directly; homebase owns household state only
- The one calendar write left is `confirm_pending_school_events`, which creates school events the family has explicitly approved
- Morning briefing data (`get_morning_briefing`) and school-window hourly weather + UV + air quality + sun times (`get_weather_context`)
- Composition and delivery of the daily briefing happen OUTSIDE this skill — see "Morning briefing" below
- Output validation catches missing data (wrong calendar, missing weather, missing kid meals) before it reaches the family
- 60-day reliability tracker records daily briefing health (`household/briefing_reliability.json`)
- The 5:50 AM pre-flight health check is gone — deleted 2026-08-17 with the cron job it guarded (see "Scheduled Tasks")

**Meal Planning**
- Per-child meal rules defined in `config.json` (breakfast options, lunch options, dietary restrictions)
- Draft meal plan posted to the family WhatsApp group for approval; the agent applies revision requests, and the plan auto-locks after 2 revisions
- **On-demand only.** The Saturday-draft / Sunday-9-PM-auto-lock cadence was a pair of OpenClaw cron jobs and went with them on 2026-08-17. The flow works whenever it is called; nothing schedules it
- Tracks what kids actually ate (learned daily via morning check-in)

**School**
- Reads Gmail for school emails (domains configured in `config.json`) through the `gog` CLI, on the `school` runner's schedule — 8:07/12:07/16:07/20:07 Mon–Fri
- Extracts calendar events from email bodies and PDF attachments via the agent + pypdf
- Deduplicates against existing Google Calendar entries before proposing; since 2026-09-07 that lookup is a `gog calendar events` call in the runner, not a homebase tool
- Propose → family confirms → create: nothing reaches Google Calendar until the family replies

**Health — Medication & Symptom Tracker**
- Logs medication doses per child (Tylenol, Ibuprofen, and variants)
- Accepts doses in mL **or** mg — converts automatically using standard concentrations
- Safety checks: early-dose warnings, dosage range vs. child weight, 24-hour max dose count
- Logs fevers (confirmed temperature or subjective "feels warm"), symptoms (free-text)
- Health summary formatted for doctor visits
- `schedule_medication_reminder` returns a structured reminder payload for the next dose window; Python never schedules or sends anything — the agent creates the one-shot job and delivers it

**Kid Profiles & Trip Prep**
- Per-child observation log: food sensitivities, car-sickness notes, gear preferences, etc.
- Detects upcoming trips in Google Calendar (next 4 days)
- Infers environment tags (mountain, beach, desert, urban, flight) from event title + location
- Fetches live weather forecast for the destination (Open-Meteo geocoding API)
- The agent composes a per-child WhatsApp prep message (packing tips, relevant observations)
- Idempotent: prep message sent only once per trip event

**Groceries**
- Shopping list per store (general, Indian grocery, Costco)

**Restaurants**
- Logs restaurant visits (meal type, items, total, ratings)
- Rating reminders for unrated visits
- Recommendations based on meal type and past ratings

---

## Architecture

```
WhatsApp message
      ↓
  OpenClaw → agent        ← reads SKILL.md, references/agent.md (model-agnostic)
      ↓
  tools.py (CLI)          ← python3 tools.py <action> '<json>'
      ↓
  core/                   ← config_loader, gcal, gmail, pdf_attachments
  features/briefing/      ← morning_briefing, weather, daily_thought
  features/calendar/      ← calendar_aggregator, calendar_manager
  features/school/        ← school_email_monitor, school_calendar_sync, snack_manager
  features/meals/         ← meal_tracker, weekly_meal_planner
  features/trips/         ← trip_detector, travel_window
  features/health/        ← health_tracker
  features/shopping/      ← shopping_list
  features/dining/        ← restaurant_tracker, media_watcher
  features/bills/         ← watcher
      ↓
  household/*.json        ← local state files (no database)
```

`core/gcal.py` and `core/gmail.py` are the only modules that reach Google, and
they do it by shelling out to the `gog` CLI. Since 2026-09-07 nothing here
imports a Google client library or holds a credential —
The skill holds no credentials of its own; see `CHANGELOG.md`.

**The OpenClaw agent is the dispatcher.** Python scripts are pure data tools — they never call any LLM. `tools.py` stays at the root as the entry point. Feature modules are organized by domain in `features/`, with shared infrastructure in `core/`. The reasoning model is whatever OpenClaw is configured with; this skill has no opinion.

---

## Requirements

- **Python 3.12+** (uses `zoneinfo` and `__future__` annotations)
- **OpenClaw** installed and linked to a WhatsApp account — Homebase is a skill, not a standalone bot
- **The `gog` CLI** (gogcli.sh), authenticated for Gmail + Calendar. This is a binary dependency, not a pip one, and it is the only path to Google. It owns the OAuth refresh token in the macOS Keychain; homebase stores no credential of its own.

Python dependencies live in [pyproject.toml](pyproject.toml). Install with:

```bash
pip install -e .            # core
pip install -e ".[test]"    # + test runner
```

Image classification (receipts, snack schedules) is handled by the OpenClaw agent's native vision capability, not by this skill. Python only matches caption keywords and routes images into buckets the agent can act on.

---

## Setup

### 1. Install Python dependencies

```bash
cd ~/.openclaw/workspace/skills/homebase
pip install -e .
```

### 2. Configure `config.json`

```bash
cp config.example.json config.json
```

Key fields to set:
- `app.name` — display name for your Homebase instance
- `location.city`, `latitude`, `longitude`, `timezone`
- `whatsapp.group_id` — WhatsApp group JID (e.g. `"120363...@g.us"`)
- `family.members` — map of `{phone: name}` for the sender allowlist
- `family.kids` — kid names, emoji ("boy"/"girl"), ages, and meal rules
- `calendar.id` — Google Calendar ID
- `school.email_domains` — school email domains for the email monitor
- `stores` — grocery store names

**Do not put Google OAuth credentials in `config.json`.** Do not put them
anywhere in this skill — it holds none. `config.json` does hold PII (group jid,
phone numbers, kid names, calendar id), so `chmod 600 config.json`.
Homebase needs no LLM API key — the OpenClaw agent handles all reasoning.

### 3. Authorize Google in `gog`

```bash
gog auth add <your-google-account> --services gmail,calendar
gog auth status                     # verify
```

That is the whole credential story. **Homebase stores no credential of its
own** — no `.env`, no client id, no refresh token, no Keychain entry. `gog`
owns the refresh token and mints an access token per invocation, and
`core/gcal.py` / `core/gmail.py` reach Google only by exec'ing it. See
`CHANGELOG.md` for what this replaced.

### 4. Re-auth Google (when the token expires or is revoked)

```bash
gog auth status
gog auth add <your-google-account> --services gmail,calendar
```

The school email monitor will WhatsApp the family exactly once when a fetch
fails on auth, then go silent until it's fixed.

### 5. Gateway daemon — nothing to do

OpenClaw installs and owns its own launchd agent, `ai.openclaw.gateway`. Homebase
needs no daemon of its own and ships no plist. Check the real one:

```bash
launchctl list | grep ai.openclaw.gateway
openclaw gateway status --deep      # expect Runtime: running
```

### 6. Verify

```bash
python tools.py get_morning_briefing '{}'
python setup_check.py   # config + gog auth + live calendar read
python -m pytest -q     # all tests should pass
```

---

## Driving homebase from a scheduler

**Nothing in this skill schedules anything.** There is no cron job, no timer and
no daemon. Homebase returns data; a caller you write decides when to ask and
what to do with the answer.

The pattern that works: a small shell script, run by whatever scheduler your OS
provides (launchd, systemd, cron), that

1. pulls what it needs through `bin/homebase.sh` — one tool per call,
2. composes the message itself (or hands the JSON to a model with no tools),
3. sends it through whatever channel it owns, and
4. calls the matching `mark_*` tool **after** the send succeeds.

Step 4 is the one worth spelling out. `fetch_school_emails` and
`fetch_bill_emails` return work *unmarked* on purpose, because marking before
delivery means a failed send silently consumes the email. Fetch → deliver →
then mark.

Two things a scheduler must supply that an interactive shell gives you for free:

- **A full `PATH`.** launchd hands a process only `/usr/bin:/bin:/usr/sbin:/sbin`,
  which contains neither `gog` nor a modern `python3`. A runner without an
  explicit `PATH` dies at its first call and cannot even report it. Testing by
  running the script yourself proves nothing — invoke it the way the scheduler
  will.
- **The shim, not `tools.py`.** `bin/homebase.sh` pins the venv interpreter.
  `tools.py` can self-heal by re-exec, but not from every interpreter.

Scheduled callers never talk to the agent, so anything both must know — a trip,
for instance — belongs on the calendar rather than in a state file or a chat
message.

## Data Storage

All state is stored locally in JSON files — no external database. **Every write
goes through `utils.write_json_atomic()`** (tempfile + fsync + rename) so a
crash mid-write never leaves a corrupt file behind. All state files below are
gitignored — they live on your machine only:

| Path | Contents |
|------|----------|
| `config.json` | All configuration (see `config.example.json`) |
| `calendar_data/family_calendar.json` | Cached Google Calendar events |
| `calendar_data/processed_email_ids.json` | Gmail message IDs already sent to WhatsApp |
| `calendar_data/calendar_synced_ids.json` | Gmail message IDs already synced to calendar |
| `calendar_data/auth_error_state.json` | School auth-error notify-once state |
| `calendar_data/pending_school_events.json` | Proposed school events awaiting family confirmation |
| `calendar_data/last_sync.json` | Calendar sync marker |
| `household/shopping_list.json` | Per-store shopping list |
| `household/meal_history.json` | What kids actually ate |
| `household/meal_plan_pending.json` | Draft weekly plan (pending approval) |
| `household/weekly_meal_plan.json` | Locked weekly plan |
| `household/learned_catalog.json` | Per-installation meal catalog additions |
| `household/catalog_pending_review.json` | Off-catalog meals awaiting owner approval |
| `household/restaurants.json` | Restaurant visit log and ratings |
| `household/snack_schedule.json` | School snack schedule |
| `household/health_config.json` | Kid weights for dosage calculations |
| `household/health_log.json` | Append-only medication/fever/symptom log |
| `household/kid_profiles.json` | Per-child observation notes for trip prep |
| `household/trip_prep_sent.json` | Sent trip prep messages (idempotency) |
| `household/briefing_reliability.json` | 60-day morning briefing reliability tracker |
| `household/bills_processed.json` | One-way ledger of bills already delivered |
| `household/bills_auth_error_state.json` | Bills auth-error notify-once state |
| `household/media_watcher_state.json` | Directory-scanner triage state |

---

## Key Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Skill manifest — what the OpenClaw agent loads, plus the tool-invocation contract |
| `references/agent.md` | Full tool reference — what to call for every request type |
| `tools.py` | CLI tool library — `python3 tools.py <action> '<json>'` |
| `core/config_loader.py` | Centralized config — all settings from `config.json` |
| `core/gcal.py` | The only path to Google Calendar — shells out to the `gog` CLI, holds no credentials |
| `core/gmail.py` | The only path to Gmail — same, read-only by construction |
| `core/pdf_attachments.py` | MIME walk + `pypdf` text extraction for bill and school PDFs |
| `features/calendar/calendar_aggregator.py` | Google Calendar → local cache sync (1 day back, 30 forward) |
| `features/calendar/calendar_manager.py` | Calendar create/update/delete over `core/gcal.py`; owns the inclusive→exclusive all-day end-date conversion |
| `features/school/school_email_monitor.py` | Gmail monitoring for school emails |
| `features/school/school_calendar_sync.py` | Email/PDF → Google Calendar event sync |
| `features/health/health_tracker.py` | Medication, fever, and symptom tracker |
| `features/trips/trip_detector.py` | Trip detection (outputs JSON for the agent to compose) |
| `features/trips/travel_window.py` | Travel mode — is the household away on this date, and where |
| `features/bills/watcher.py` | Bill email fetch + PDF extraction (optional module) |
| `features/meals/weekly_meal_planner.py` | Weekly meal plan draft + approval flow |
| `features/meals/meal_tracker.py` | Per-child meal history and config-driven suggestions |
| `features/briefing/morning_briefing.py` | Briefing data aggregator with output validation and reliability tracking |
| `features/briefing/weather.py` | Open-Meteo weather fetch: current conditions, plus `fetch_weather_context()` for hourly school-window figures, UV, air quality and sun times |

---

## Running Tests

```bash
cd ~/.openclaw/workspace/skills/homebase
python -m pytest -q
```

587 tests cover: weather, meal planner, school email monitor, school roster,
school pending queue, morning briefing, briefing hardening (output validation,
reliability tracker, config regressions), restaurant tracker, shopping list,
health tracker, bills watcher, school calendar sync, calendar aggregator sync,
calendar manager, `core/gcal.py`, trip detector, travel window, media watcher,
the stdout contract, the docs-in-sync contract, and integration flows. All
external dependencies are mocked — since 2026-09-07 the Google seam is a patch
over `core.gcal` / `core.gmail` (i.e. over the `gog` subprocess) rather than
over a Google client library. The keychain-secrets tests went with the module
they covered.

## License

MIT
