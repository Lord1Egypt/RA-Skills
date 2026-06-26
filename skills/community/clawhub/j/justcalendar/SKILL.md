---
name: justcalendar
description: Use this skill when a user needs to install, authenticate, or operate the Just Calendar CLI against https://justcalendar.ai, including generating an agent token in the web UI and performing calendar/day-data management from terminal commands.
---

# JustCalendar CLI Skill

## Purpose

This skill provides complete operational guidance for `justcalendar`, a Node.js CLI that manages Just Calendar data in Google Drive through:

1. Backend-issued Google Drive access tokens from `https://justcalendar.ai`
2. Direct Google Drive API reads/writes for calendar data files

Use this skill for setup, login, troubleshooting, and day-to-day CLI operations.

## When To Use This Skill

Use this skill when user asks to:

- Install or update `justcalendar`
- Login with a token generated in Just Calendar web interface
- Add, list, rename, remove, or select calendars
- Set/get/delete day values from calendars
- Run bulk data operations from terminal
- Troubleshoot token/auth/permission errors

## Prerequisites

- Node.js `>=18`
- `npm`
- Access to `https://justcalendar.ai`
- A Google Drive-connected session in the web app (required to generate token and use Drive-backed operations)

## Installation

Global install from npm:

```bash
npm install -g justcalendar
justcalendar --help
```

From local project path:

```bash
cd ~/justcalendar-cli
npm install
npm install -g .
justcalendar --help
```

If installing from GitHub:

```bash
git clone git@github.com:AndredAlmeida/justcalendar-cli.git
cd justcalendar-cli
npm install
npm install -g .
justcalendar --help
```

## Authentication Workflow (Web -> CLI)

### Step 1: Generate token on website

1. Open `https://justcalendar.ai`
2. Login/connect Google Drive in the app
3. Click **Connect to your Agent** (OpenClaw button)
4. Click **Generate New Token**
5. Copy token immediately

Important:

- Token is shown once
- Generating a new token invalidates the previous token
- If popup says token already exists but hidden, generate a new one to get a visible token

### Step 2: Login CLI with token

```bash
justcalendar login --token <YOUR_TOKEN> --url https://justcalendar.ai
```

Verify:

```bash
justcalendar status
```

Expected status includes backend URL, token state, and current calendars (if authenticated).

## CLI Data Model Notes

- Calendar selector can be **calendar id** or **calendar name**
- Date format is strict `YYYY-MM-DD`
- Data is stored under `JustCalendar.ai` folder in Google Drive
- Main config file: `justcalendar.json`
- Calendar data files: `<account-id>_<calendar-id>.json`
- CLI local config: `~/.justcalendar-cli/config.json`

## Command Reference

### Session / Auth

```bash
justcalendar login --token <TOKEN> --url https://justcalendar.ai
justcalendar logout
justcalendar status
```

### Calendars

```bash
justcalendar calendars list
justcalendar calendars add "Workout" --type score --color red --display heatmap --pinned
justcalendar calendars rename "Workout" "Workout Intensity"
justcalendar calendars remove "Workout Intensity"
justcalendar calendars select "Energy Tracker"
```

Calendar type options:

- `signal-3`
- `score`
- `check`
- `notes`

Color options:

- `green`, `red`, `orange`, `yellow`, `cyan`, `blue`

Score display options (for `score` type):

- `number`, `heatmap`, `number-heatmap`

### Day Data - Set

Single set:

```bash
justcalendar data set "Energy Tracker" 2026-03-01 green
```

Bulk set (multiple `<date> <value>` pairs in one call):

```bash
justcalendar data set "Energy Tracker" 2026-03-01 green 2026-03-02 yellow 2026-03-03 red
```

### Day Data - Delete

Single delete:

```bash
justcalendar data delete "TODOs" 2026-03-01
```

Bulk delete (multiple dates in one call):

```bash
justcalendar data delete "TODOs" 2026-03-01 2026-03-02 2026-03-03
```

### Day Data - Get

Single get:

```bash
justcalendar data get "Sleep" 2026-03-01
```

Bulk get (multiple dates in one call):

```bash
justcalendar data get "Sleep" 2026-03-01 2026-03-02 2026-03-03
```

## Bulk-First Rule (Multi-Day Operations)

When handling more than one date, prefer **one bulk command** over looping per-day commands.

Use these bulk patterns by default:

- `justcalendar data set <calendar> <date1> <value1> <date2> <value2> ...`
- `justcalendar data delete <calendar> <date1> <date2> ...`
- `justcalendar data get <calendar> <date1> <date2> ...`

Use bulk whenever request scope is more than one day, including:

- Date ranges
- Whole week or whole month operations
- Backfills
- Batch fixes

Fall back to per-day commands only when:

- Bulk command length would exceed shell/OS command length limits
- Per-day retries are required for a failed subset

Single-day requests stay unchanged: use the existing single-date command forms.

### Bulk Examples

Week update in one `data set` call:

```bash
justcalendar data set "Energy Tracker" \
  2026-03-02 green 2026-03-03 yellow 2026-03-04 red \
  2026-03-05 green 2026-03-06 green 2026-03-07 yellow 2026-03-08 green
```

Month delete in one `data delete` call:

```bash
justcalendar data delete "TODOs" \
  2026-02-01 2026-02-02 2026-02-03 2026-02-04 2026-02-05 2026-02-06 2026-02-07 \
  2026-02-08 2026-02-09 2026-02-10 2026-02-11 2026-02-12 2026-02-13 2026-02-14 \
  2026-02-15 2026-02-16 2026-02-17 2026-02-18 2026-02-19 2026-02-20 2026-02-21 \
  2026-02-22 2026-02-23 2026-02-24 2026-02-25 2026-02-26 2026-02-27 2026-02-28
```

Multi-day verification in one `data get` call:

```bash
justcalendar data get "Sleep" \
  2026-03-01 2026-03-02 2026-03-03 2026-03-04 2026-03-05 2026-03-06 2026-03-07
```

Performance + consistency note:

- Bulk commands reduce CLI/API overhead and reduce partial-write risk versus many per-day calls.

## Value Rules By Calendar Type

### `signal-3`

Accepted values for `data set`:

- `red`
- `yellow`
- `green`
- `x`
- `clear` / `unset` / `none` (removes value)

### `score`

Accepted values:

- Integers from `-1` to `10`
- `-1` means unset/remove

### `check`

Accepted truthy values:

- `true`, `1`, `yes`, `on`, `checked`

Falsy/unset values:

- `false`, `0`, `no`, `off`, `unchecked`, `clear`, `unset`, `none`

### `notes`

Accepted:

- Any non-empty text string (quote if spaces)

Unset:

- Empty/blank value (or use `data delete`)

## Recommended Operating Sequence

1. Check connectivity:

```bash
justcalendar status
```

2. List calendars:

```bash
justcalendar calendars list
```

3. Apply desired calendar/data changes

4. Re-check specific days:

```bash
justcalendar data get "<Calendar>" <date1> <date2> ...
```

## Troubleshooting

### `Not logged in. Run: justcalendar login ...`

- Run login again with valid token

### `invalid_agent_token` / `missing_agent_token`

- Generate new token in web app popup
- Re-run:

```bash
justcalendar login --token <NEW_TOKEN> --url https://justcalendar.ai
```

### `missing_drive_scope`

- In web app, reconnect Google Drive and approve Drive access (`drive.file`)
- Generate new agent token
- Login again in CLI

### `token_refresh_failed` / `not_connected`

- Drive session on server is expired/disconnected
- Reconnect Google Drive on website, generate new token, and login again

### Date format errors

- Use exact `YYYY-MM-DD`
- Ensure calendar date is valid (for example, `2026-02-30` is invalid)

### Ambiguous calendar name

- Use calendar id from:

```bash
justcalendar calendars list
```

## Safety / Behavior Notes

- `calendars remove` is destructive for that calendar and its associated data file
- Bulk `data set`/`data delete` operations issue a single final write per command invocation
- Keep agent tokens secret; treat like credentials
- Rotate token by generating a new one (old token is invalidated)

## Quick Start Example

```bash
justcalendar login --token jca_... --url https://justcalendar.ai
justcalendar calendars list
justcalendar calendars add "Hydration" --type check --color cyan
justcalendar data set "Hydration" 2026-03-01 true 2026-03-02 true 2026-03-03 false
justcalendar data get "Hydration" 2026-03-01 2026-03-02 2026-03-03
```
