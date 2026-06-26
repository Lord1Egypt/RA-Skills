# iCalendar Sync for OpenClaw

Secure iCloud Calendar integration for OpenClaw agents.

[![Version](https://img.shields.io/badge/version-2.4-blue.svg)](https://github.com/h8kxrfp68z-lgtm/iCalendar-Sync/releases)
[![Security](https://img.shields.io/badge/security-A-brightgreen.svg)](SECURITY.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)

## What It Does

- List calendars
- Get events by time window
- Create events (including alarms and RRULE)
- Update events
- Update recurring events in modes: `single`, `all`, `future`
- Delete events
- Store credentials in OS keyring or secure YAML file (`0600`)
- Smart provider behavior in `auto` mode (tries CalDAV first, falls back to `macos-native` on macOS)
- Explicit provider enforcement (`--provider caldav` will not silently switch to native)
- Optional keyring bypass for debugging (`--ignore-keyring`)

## Requirements

- Python 3.9+
- iCloud App-Specific Password (not Apple ID primary password)
- Network access to iCloud CalDAV for `caldav` provider
- macOS only for `macos-native` provider (AppleScript bridge to Calendar.app)

## Installation

From source:

```bash
git clone https://github.com/h8kxrfp68z-lgtm/iCalendar-Sync.git
cd iCalendar-Sync
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
```

With dev dependencies:

```bash
pip install -e '.[dev]'
```

## Quick Start

### 1. Configure credentials

Interactive (recommended for local usage):

```bash
python -m icalendar_sync setup --username user@icloud.com
```

Headless / automation:

```bash
export ICLOUD_USERNAME="user@icloud.com"
export ICLOUD_APP_PASSWORD="xxxx-xxxx-xxxx-xxxx"
python -m icalendar_sync setup --non-interactive
```

If keyring is unavailable:

```bash
python -m icalendar_sync setup --non-interactive --storage file --config ~/.openclaw/icalendar-sync.yaml
```

### 2. Run commands

```bash
python -m icalendar_sync list
python -m icalendar_sync get --calendar "Personal" --days 7
```

Or use installed script:

```bash
icalendar-sync list
```

## Provider Modes

- `--provider auto`
  - Tries CalDAV first on all OSes
  - On macOS only, may fall back to native bridge (`macos-native`) if CalDAV connection/auth fails
- `--provider caldav`: force direct CalDAV (no fallback)
- `--provider macos-native`: force Apple Calendar bridge (macOS only)

For CalDAV troubleshooting:

```bash
--debug-http --user-agent "your-agent/1.0"
```

Force CalDAV + ignore keychain (debug mode):

```bash
python -m icalendar_sync list --provider caldav --ignore-keyring --storage env
```

## CLI Examples

List calendars:

```bash
python -m icalendar_sync list
```

Get events:

```bash
python -m icalendar_sync get --calendar "Work" --days 14
```

Create event:

```bash
python -m icalendar_sync create --calendar "Work" --json '{
  "summary": "Team Meeting",
  "dtstart": "2026-03-10T14:00:00+03:00",
  "dtend": "2026-03-10T15:00:00+03:00",
  "description": "Q1 planning",
  "location": "Conference Room A"
}'
```

Update event:

```bash
python -m icalendar_sync update --calendar "Work" --uid "event-uid" --json '{
  "summary": "Updated Meeting",
  "location": "Room B"
}'
```

Update one recurring instance:

```bash
python -m icalendar_sync update \
  --calendar "Work" \
  --uid "series-uid" \
  --recurrence-id "2026-03-20T09:00:00+03:00" \
  --mode single \
  --json '{"summary":"One-off change"}'
```

Update all recurring instances:

```bash
python -m icalendar_sync update \
  --calendar "Work" \
  --uid "series-uid" \
  --mode all \
  --json '{"summary":"Series title update"}'
```

Update this and future instances:

```bash
python -m icalendar_sync update \
  --calendar "Work" \
  --uid "series-uid" \
  --recurrence-id "2026-04-01T09:00:00+03:00" \
  --mode future \
  --json '{"dtstart":"2026-04-01T10:00:00+03:00","dtend":"2026-04-01T10:30:00+03:00"}'
```

Delete event:

```bash
python -m icalendar_sync delete --calendar "Work" --uid "event-uid"
```

## Input Contract (`create`)

Required:

- `summary` (string)
- `dtstart` (ISO datetime)
- `dtend` (ISO datetime; must be later than `dtstart`)

Optional:

- `description`
- `location`
- `status`
- `priority` (0..9)
- `alarms` (array)
- `rrule` (object)

## Environment Variables

Credential-related:

- `ICLOUD_USERNAME`
- `ICLOUD_APP_PASSWORD`
- `ICALENDAR_SYNC_STORAGE` (`auto|keyring|env|file`)
- `ICALENDAR_SYNC_IGNORE_KEYRING` (`1|true|yes|on`) to force env/config credentials over keychain
- `ICALENDAR_SYNC_CONFIG` (path to YAML file)

Runtime-related:

- `ICALENDAR_SYNC_PROVIDER` (`auto|caldav|macos-native`)
- `ICALENDAR_SYNC_USER_AGENT`
- `ICALENDAR_SYNC_DEBUG_HTTP` (`1|true|yes|on`)
- `LOG_LEVEL` (`DEBUG|INFO|WARNING|ERROR`)

## Security Notes

- Use App-Specific Passwords only.
- Credentials are redacted in logs.
- Input size and calendar names are validated.
- TLS verification is enabled for CalDAV.
- File-based credentials are stored with strict permissions (`0600`).

## Development

Run tests:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'
pytest -q
```

## License

MIT
