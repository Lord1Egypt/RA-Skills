---
name: icloud-calendar
description: Add events to iCloud Calendar via CalDAV. Syncs to iPhone automatically with alarm reminders.
homepage: https://github.com/TeenLucifer/icloud-calendar-skill
metadata:
  clawdbot:
    emoji: "📅"
    requires:
      env: ["ICLOUD_EMAIL", "ICLOUD_PASSWORD"]
      bins: ["python3"]
    primaryEnv: "ICLOUD_EMAIL"
    files: ["scripts/*"]
---

# iCloud Calendar

Add events to iCloud Calendar via CalDAV. Automatically syncs to iPhone with alarm reminders.

## Features

- ✅ Add events to iCloud Calendar
- ✅ iPhone push notifications via calendar alerts  
- ✅ Customizable reminder times (default 15 min + 5 min)
- ✅ Works with any iCloud account
- ✅ Credentials stored in local .env file

## Setup

### 1. Get iCloud App Specific Password

1. Go to [appleid.apple.com](https://appleid.apple.com)
2. Sign in → "Sign-In and Security"
3. Click "App-Specific Passwords" → "+"
4. Create a new password and save it

### 2. Configure Credentials

```bash
cp secrets/.env.example secrets/.env
# Edit secrets/.env with your credentials
```

Or set environment variables directly:

```bash
export ICLOUD_EMAIL="your-email@icloud.com"
export ICLOUD_PASSWORD="your-app-specific-password"
```

## Usage

```bash
python3 scripts/add_event.py "Event Title" "YYYY-MM-DDTHH:MM:SS" "YYYY-MM-DDTHH:MM:SS" "Description"
```

### Examples

```bash
# Add a simple event
python3 scripts/add_event.py "团队会议" "2026-03-10T14:00:00" "2026-03-10T15:00:00" "讨论项目进度"

# Add event with default 1 hour duration
python3 scripts/add_event.py "医生预约" "2026-03-15T09:00:00"
```

## Security & Privacy

- **Credentials**: Stored locally in `secrets/.env` (gitignored, never committed)
- **Data in transit**: Credentials sent only to Apple's iCloud CalDAV servers
- **No external services**: Only communicates with `caldav.icloud.com`
- **User control**: Users must provide their own iCloud credentials

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| `https://caldav.icloud.com` | iCloud email + App-Specific Password (Base64 auth), Event data (.ics) | Create calendar events |

## Trust Statement

This skill sends your iCloud credentials to Apple's iCloud servers to create calendar events. Only install if you trust Apple with your iCloud account. The skill does not store or exfiltrate any data beyond direct communication with iCloud.


## Technical Details

- Uses iCloud CalDAV API (PROPFIND + PUT methods)
- Calendar path format: `/<user_id>/calendars/home/`
- Creates iCalendar (.ics) events with VALARM reminders
- Supports multiple alarm triggers

## License

MIT License