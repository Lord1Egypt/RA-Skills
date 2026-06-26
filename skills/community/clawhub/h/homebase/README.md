# Homebase

A WhatsApp-based household coordinator for families, built as a native OpenClaw skill. The OpenClaw agent IS the intelligence — it reads messages, reasons about them, and calls Python data tools via bash. Homebase is model-agnostic: whichever model OpenClaw is configured with (Claude, Gemma, GPT, Llama, ...) does the reasoning. No LLM SDK is bundled in this skill.

Clone, edit `config.json`, add Google credentials, run. Zero Python code changes.

---

## What It Does

**Calendar & Schedule**
- Syncs with Google Calendar (read + write) via OAuth
- Adds, edits, and deletes events via WhatsApp chat
- Daily morning briefing at 7 AM with weather, clothing suggestions for kids, events, meal plan, and snack schedule
- Pre-flight health check at 6:45 AM validates Google auth, calendar ID, weather API, and WhatsApp gateway before the briefing runs
- Output validation catches missing data (wrong calendar, missing weather, missing kid meals) before it reaches the family
- 30-day reliability tracker records daily briefing health (`household/briefing_reliability.json`)

**Meal Planning**
- Per-child meal rules defined in `config.json` (breakfast options, lunch options, dietary restrictions)
- Saturday evening draft meal plan sent to family WhatsApp group for approval
- The agent applies revision requests directly; auto-locks at 9 PM Sunday if no reply
- Tracks what kids actually ate (learned daily via morning check-in)

**School**
- Monitors Gmail for school emails (domains configured in `config.json`) every 2 hours (weekdays)
- Extracts calendar events from email bodies and PDF attachments via the agent + pypdf
- Deduplicates against existing Google Calendar entries before adding

**Health — Medication & Symptom Tracker**
- Logs medication doses per child (Tylenol, Ibuprofen, and variants)
- Accepts doses in mL **or** mg — converts automatically using standard concentrations
- Safety checks: early-dose warnings, dosage range vs. child weight, 24-hour max dose count
- Logs fevers (confirmed temperature or subjective "feels warm"), symptoms (free-text)
- Health summary formatted for doctor visits
- `at`-command reminder when the next dose window opens

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
  OpenClaw → agent        ← reads SOUL.md, agent.md (model-agnostic)
      ↓
  tools.py (CLI)          ← python3 tools.py <action> '<json>'
      ↓
  core/                   ← config_loader, keychain_secrets, whatsapp
  features/briefing/      ← morning_briefing, weather, preflight
  features/calendar/      ← calendar_aggregator, calendar_manager
  features/school/        ← school_email_monitor, snack_manager
  features/meals/         ← meal_tracker, weekly_meal_planner
  features/trips/         ← trip_detector
  features/health/        ← health_tracker
  features/shopping/      ← shopping_list
  features/dining/        ← restaurant_tracker, media_watcher
      ↓
  household/*.json        ← local state files (no database)
```

**The OpenClaw agent is the dispatcher.** Python scripts are pure data tools — they never call any LLM. `tools.py` stays at the root as the entry point. Feature modules are organized by domain in `features/`, with shared infrastructure in `core/`. The reasoning model is whatever OpenClaw is configured with; this skill has no opinion.

---

## Requirements

- **Python 3.12+** (uses `zoneinfo` and `__future__` annotations)
- **OpenClaw** installed and linked to a WhatsApp account — Homebase is a skill, not a standalone bot
- **Google Cloud project** with Calendar API + Gmail API enabled
- **macOS Keychain** is optional. On macOS, secrets can be stored in Keychain via `migrate_to_keychain.py`. On other platforms, the skill reads secrets from environment variables.

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

**Do not put Google OAuth credentials in `config.json`.** Use `.env` and/or Keychain. Homebase needs no LLM API key — the OpenClaw agent handles all reasoning.

### 3. Add secrets to `.env`

```
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REFRESH_TOKEN=your-refresh-token
```

Get these from Google Cloud Console → APIs & Services → Credentials → OAuth 2.0
Client ID. Make sure Calendar API and Gmail API are both enabled in your project.
Run `python core/reauth_google.py` once to mint the refresh token.

On macOS, optionally migrate the credentials into Keychain so `.env` can be deleted:
```bash
python migrate_to_keychain.py
python migrate_to_keychain.py --check   # verify
```

### 4. Re-auth Google OAuth (when tokens expire)

```bash
python core/reauth_google.py
```

The school email monitor will WhatsApp the family exactly once when the
refresh token expires, then go silent until it's fixed.

### 5. Install the launchd daemon *(run once)*

```bash
cp ~/.openclaw/workspace/skills/homebase/com.openclaw.daemon.plist \
   ~/Library/LaunchAgents/com.openclaw.daemon.plist

launchctl load ~/Library/LaunchAgents/com.openclaw.daemon.plist
```

Check it's running:
```bash
launchctl list | grep openclaw
tail -f /tmp/openclaw/openclaw-launchd.log
```

### 6. Verify

```bash
python tools.py get_todays_events
python setup_check.py   # full dependency + auth check
python -m pytest -q     # all tests should pass
```

---

## Scheduled Tasks (OpenClaw)

Six tasks are managed by OpenClaw (see the Scheduled section in sidebar):

| Task ID | Schedule (PT) | Description |
|---------|--------------|-------------|
| `homebase-briefing-preflight` | 6:45 AM daily | Pre-flight health check: auth, calendar, weather, gateway |
| `homebase-morning-briefing` | 7:00 AM daily | Agent composes briefing from `--data-only` output |
| `homebase-school-emails` | Every 2h, 8 AM–6 PM, weekdays | Scan Gmail for school updates |
| `homebase-rating-reminders` | Every 2 hours | Rating reminders for unrated restaurant visits |
| `homebase-meal-plan-draft` | 6:00 PM Saturday | Generate and send draft meal plan |
| `homebase-trip-detector` | 9:00 AM daily | Check for trips; agent composes prep message |

---

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
| `calendar_data/auth_error_state.json` | Auth-error notify-once state |
| `household/shopping_list.json` | Per-store shopping list |
| `household/meal_history.json` | What kids actually ate |
| `household/meal_plan_pending.json` | Saturday draft plan (pending approval) |
| `household/weekly_meal_plan.json` | Locked weekly plan |
| `household/restaurants.json` | Restaurant visit log and ratings |
| `household/snack_schedule.json` | School snack schedule |
| `household/health_config.json` | Kid weights for dosage calculations |
| `household/health_log.json` | Append-only medication/fever/symptom log |
| `household/kid_profiles.json` | Per-child observation notes for trip prep |
| `household/trip_prep_sent.json` | Sent trip prep messages (idempotency) |
| `household/briefing_reliability.json` | 30-day morning briefing reliability tracker |

---

## Key Files

| File | Purpose |
|------|---------|
| `SOUL.md` | Agent's household assistant rules and photo handling |
| `agent.md` | Full tool reference — what to call for every request type |
| `tools.py` | CLI tool library — `python3 tools.py <action> '<json>'` |
| `core/config_loader.py` | Centralized config — all settings from `config.json` |
| `core/keychain_secrets.py` | Secure credential loader (macOS Keychain + .env fallback) |
| `core/whatsapp.py` | WhatsApp message sending via OpenClaw CLI |
| `features/calendar/calendar_manager.py` | Google Calendar API integration |
| `features/school/school_email_monitor.py` | Gmail monitoring for school emails |
| `features/school/school_calendar_sync.py` | Email/PDF → Google Calendar event sync |
| `features/health/health_tracker.py` | Medication, fever, and symptom tracker |
| `features/trips/trip_detector.py` | Trip detection (outputs JSON for the agent to compose) |
| `features/meals/weekly_meal_planner.py` | Saturday meal plan draft + approval flow |
| `features/meals/meal_tracker.py` | Per-child meal history and config-driven suggestions |
| `features/briefing/morning_briefing.py` | Briefing data aggregator with output validation and reliability tracking |
| `features/briefing/briefing_preflight.py` | Pre-flight health check (runs 15 min before briefing) |
| `features/briefing/weather.py` | Open-Meteo weather fetch |

---

## Running Tests

```bash
cd ~/.openclaw/workspace/skills/homebase
python -m pytest -q
```

297 tests cover: weather, meal planner, school email monitor, keychain secrets,
morning briefing, briefing hardening (output validation, reliability tracker,
config regressions, preflight checks), restaurant tracker, shopping list,
health tracker, school calendar sync, trip detector, media watcher, and
integration flows. All external dependencies (Google APIs, network) are mocked.

## License

MIT
