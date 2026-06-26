# iCloud Calendar Skill for OpenClaw

Add events to iCloud Calendar via CalDAV. Automatically syncs to iPhone with alarm reminders.

## Features

- ✅ Add events to iCloud Calendar
- ✅ iPhone push notifications via calendar alerts
- ✅ Customizable reminder times (default 15 minutes + 5 minutes before)
- ✅ Works with any iCloud account
- ✅ Simple Python script, no external dependencies

## Setup

### 1. Get iCloud App Specific Password

1. Go to [appleid.apple.com](https://appleid.apple.com)
2. Sign in → "Sign-In and Security"
3. Click "App-Specific Passwords" → "+"
4. Create a new password and save it

### 2. Configure the Script

Edit `scripts/add_event.py` and replace the credentials:

```python
ICLOUD_EMAIL = "your-email@icloud.com"
ICLOUD_PASSWORD = "your-app-specific-password"
```

### 3. Find Your Calendar Home Path

The script includes a discovery feature to find your calendar path automatically.

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

## Integration with OpenClaw

This skill works with OpenClaw AI assistant. Once installed, you can add events using natural language:

> "明天上午10点有个会议"  
> "每天早上8点跑步提醒"

## Technical Details

- Uses iCloud CalDAV API
- Calendar path format: `/<user_id>/calendars/home/`
- Creates iCalendar (.ics) events with VALARM reminders
- Supports multiple alarm triggers

## Troubleshooting

### 400 Bad Request Error

This usually means the calendar path is wrong. The script will auto-discover the correct path. Make sure your App Specific Password is valid.

### Events Not Showing on iPhone

- Check iCloud Calendar is enabled in Settings
- Ensure Calendar syncing is turned on
- Verify the event was created successfully in the response

## License

MIT License

## Author

Created for OpenClaw personal AI assistant
