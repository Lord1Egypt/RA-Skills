---
name: myclub
description: Fetch accounts' sports schedules, practices, games, and events from myclub.fi. Auto-discovers accounts and clubs from your myclub.fi account. Use for checking practice times and locations, finding upcoming games and matches, viewing club events, or getting schedule summaries. Requires myclub.fi credentials (stored locally).
metadata:
  clawdbot:
    version: "1.0.0"
    author: "hanninen"
    homepage: "https://github.com/hanninen/myclub-skill"
requires:
  runtime: "python3"
  python: ">=3.10"
files: ["scripts/*"]
---

# myclub Skill

Fetch sports schedules from myclub.fi, including practice times, game dates, locations, and registration status.

## External Endpoints

This skill connects to the following external services:

- `id.myclub.fi` — Authentication (login via form POST with CSRF token)
- `*.myclub.fi` — Fetching club pages and event schedules (each club has its own subdomain)

No other external services are contacted.

## Security & Privacy

- **Credentials**: Your myclub.fi email and password are stored locally in `~/.myclub-config.json` with owner-only permissions (`0600`). They are never sent anywhere other than `id.myclub.fi` for authentication.
- **Data flow**: Login credentials are sent to `id.myclub.fi` over HTTPS. Schedule data is fetched from `*.myclub.fi` over HTTPS. No data is sent to any third party.
- **No telemetry**: This skill does not collect analytics, telemetry, or usage data.
- **Local only**: All parsed schedule data is returned to the calling agent and is not stored or transmitted elsewhere.

## Trust Statement

Data that leaves your machine: your myclub.fi email and password are sent to `id.myclub.fi` for authentication. Schedule data is fetched from `*.myclub.fi`. No data is sent to any other service. Only install this skill if you trust myclub.fi with your credentials.

## Setup (one-time)

```bash
python3 scripts/fetch_myclub.py setup --username your_email@example.com --password your_password
```

Credentials are stored in `~/.myclub-config.json` with owner-only permissions (`600`).

## Commands

### discover

List all available accounts and their clubs.

```bash
python3 scripts/fetch_myclub.py discover [--json]
```

**`--json`**: Output JSON instead of formatted text

### fetch

```bash
python3 scripts/fetch_myclub.py fetch --account "Account Name" [--period PERIOD | --start DATE [--end DATE]] [--json]
```

**`--period`** values: `this week` (default), `next week`, `this month`, `next month`
**`--start` / `--end`**: Custom date range in `YYYY-MM-DD` format (overrides `--period`)
**`--json`**: Output JSON instead of formatted text

## Event Fields

| Field | Description |
|-------|-------------|
| `id` | Unique event identifier |
| `name` | Event description |
| `group` | Team or group (e.g., "P2015 Black") |
| `venue` | Location |
| `month` | First day of event's month (YYYY-MM-DD) |
| `day` | Day in Finnish format (e.g., "15.3."), or `null` if unavailable |
| `time` | Time range (e.g., "17:00 - 18:00"), or `null` if unavailable |
| `event_category` | `Harjoitus` (training), `Ottelu` (game), `Turnaus` (tournament), `Muu` (other) |
| `type` | Inferred: `training`, `game`, `tournament`, `meeting`, `other` |
| `registration_status` | Registration status text from myclub.fi, or `"unknown"` |

## Troubleshooting

- **"No .myclub-config.json found"** — Run `setup` first
- **"Unknown account 'Name'"** — Run `discover` to check exact spelling (case-sensitive)
- **Timeout / auth errors** — Verify credentials with `discover`; check internet connection
- **JSON parsing fails** — myclub.fi page structure may have changed; check for `data-events` attribute on the calendar page

## Requirements

Python 3.10+ (no external dependencies — uses only standard library).
