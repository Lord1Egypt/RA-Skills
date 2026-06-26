---
name: homebase
description: Family household coordinator. Aggregates Google Calendar, runs a daily morning briefing (weather, schedule, kids meals, school snacks), watches school Gmail for flyers and PDFs, tracks restaurant visits and ratings from receipt photos, manages a per-store grocery list, drafts a weekly meal plan with a Sat/Sun approval cycle, logs sick-kid medication doses, and proactively flags upcoming trips. All family-specific data lives in config.json — names, phones, calendar IDs, and structured per-kid meal catalogs are 100% config-driven.
metadata: {"openclaw": {"requires": {"env": ["GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET", "GOOGLE_REFRESH_TOKEN"], "bin": ["openclaw"]}, "primaryEnv": "GOOGLE_CLIENT_ID"}}
license: MIT
---

# Homebase

A unified household assistant that runs as an OpenClaw skill. Built for families
who want one place for the calendar, the meal plan, the grocery list, the
school inbox, and the morning routine — without writing any code per family.

## Features

- **Morning briefing** — daily 7 AM weather + schedule + kids meal + school snack digest. Pre-flight health check, output validation, 30-day reliability tracker.
- **Calendar** — Google Calendar sync + natural-language event creation.
- **Kids meals** — config-driven per-kid breakfast/lunch/snack rotation with allergy and texture rules. Avoids same-meal-twice patterns from history.
- **Weekly meal planner** — Saturday 6 PM draft, family revises by reply, Sunday 9 PM auto-lock. Max 2 revisions then auto-locks.
- **School email monitor** — every 2 hours during school, parses Gmail for school flyers + PDF attachments, dedupes, surfaces important items.
- **Receipt + media watcher** — receipt photos sent to WhatsApp get classified by caption keywords, then read by the OpenClaw agent's native vision and logged to a per-restaurant rating ledger.
- **Shopping list** — per-store ("Costco", "Indian", "Target") item lists with atomic writes.
- **Health tracker** — Tylenol/ibuprofen dose log per kid with weight-based safety limits and minimum-interval enforcement.
- **Trip detector** — scans the calendar for upcoming trips, classifies the destination (mountain/beach/desert/urban), pulls weather, composes prep notes from per-kid profiles.

## Architecture

Python tools return *data*. The OpenClaw agent (model-agnostic — Claude, Gemma,
GPT, Llama, whatever OpenClaw is configured with) composes and delivers all
user-facing messages. Python never sends WhatsApp and never calls any LLM. Every Python
state file is written atomically (tempfile + fsync + rename) so a mid-write
crash never leaves a corrupt JSON behind. Cron entry points have a top-level
try/except so a crash always emits a parseable status object instead of
silently swallowing the run.

## Secrets handling

This skill needs Google OAuth credentials (`GOOGLE_CLIENT_ID`,
`GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN`) to read your Google Calendar
and school Gmail. No other API keys, no LLM keys, no third-party tokens.

Credentials are read from environment variables. On macOS they can
optionally be migrated into the system Keychain via `migrate_to_keychain.py`
and then removed from `.env`. The skill never transmits credentials anywhere
except to Google's official OAuth endpoint via `google-auth-oauthlib`.

The only outbound network calls this skill makes are to documented services
required for its features:
- Google OAuth + Gmail + Calendar APIs (`*.googleapis.com`) for the calendar
  sync, school email monitor, and credential refresh
- Open-Meteo (`api.open-meteo.com`) for weather forecasts in the morning
  briefing and trip detector — no API key, no account, no PII sent

There is no telemetry, no analytics, no third-party tracking, no calls to
any other domain.

All household state (calendar cache, meal history, health log, kid profiles,
restaurant ratings, shopping list, briefing reliability tracker) is stored
as local JSON files in `household/` and `calendar_data/`. Nothing leaves
your machine.

**File permissions.** `.env` should be `chmod 600` (the included
`setup_check.py` verifies this). The `household/` and `calendar_data/`
JSON files inherit your user umask — they're owned by the user running
OpenClaw and not accessible to other local users on a default macOS or
Linux setup. If you're on a multi-user system, audit those paths.

## About the launchd plist

`com.openclaw.daemon.plist` in this repo is a **template for the OpenClaw
gateway daemon**, not for Homebase code. The plist runs
`/usr/local/bin/openclaw start --foreground`, which is what keeps the
WhatsApp bridge alive across logins. It does NOT run any Homebase Python
directly.

It's optional. You only need it if you want WhatsApp delivery to survive
a logout or reboot. Without it, OpenClaw runs only while your terminal
session is active. If you install it, it lives at
`~/Library/LaunchAgents/com.openclaw.daemon.plist` and can be removed at
any time with `launchctl unload`.

## Requirements

- Python 3.12+
- Google Cloud project with Gmail + Calendar APIs enabled
- WhatsApp delivery via OpenClaw (no direct integration in this skill)
- Image vision is handled by the OpenClaw agent's native capability — no local LLM dependency in this skill

## Setup

1. `cp config.example.json config.json` and fill in your family.
2. Set `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` / `GOOGLE_REFRESH_TOKEN` in your environment, or migrate them into the macOS Keychain via `python migrate_to_keychain.py`.
3. `pip install -e .` (uses pyproject.toml).
4. `python -m pytest` should report all tests passing.
5. `python setup_check.py` runs a config + auth sanity check.

## Limitations

- macOS Keychain integration is best-effort on macOS only; other platforms fall through to env vars.
- The daily briefing assumes one Google Calendar; multi-calendar merging is not yet supported.

## Troubleshooting

- **Briefing missing weather** — Open-Meteo rate limit. The reliability tracker in `household/briefing_reliability.json` will flag the day as `degraded`.
- **Gmail auth error** — `python core/reauth_google.py` to re-mint the refresh token. The school email monitor will WhatsApp you exactly once when this happens, then go silent until fixed.
- **JSON file corrupt** — atomic writes prevent this in normal operation. If it happens anyway (e.g., disk full), delete the file; the loader recreates an empty one.

## License

MIT
