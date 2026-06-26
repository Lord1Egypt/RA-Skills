---
name: macos-applescript-fallback
description: Reliable macOS AppleScript fallback for creating Apple Reminders, Apple Notes, Apple Calendar events, and sending iMessage when direct tool/plugin routes are unavailable or flaky (especially on older macOS versions). Use when users ask to create reminders/notes/calendar events or send a message to their own phone via Messages, and prioritize shell+osascript execution with robust compatibility fallbacks and permission troubleshooting.
---

# macOS AppleScript Fallback

Use local shell + AppleScript for 4 tasks:
1. Create reminder (Reminders)
2. Create note (Notes)
3. Create calendar event (Calendar)
4. Send iMessage (Messages)

Prefer bundled scripts in `scripts/` over ad-hoc inline AppleScript for consistency and compatibility.

## Quick Start

Run these scripts directly:

```bash
# reminder
./scripts/create_reminder.sh "今晚8点吃晚饭" "2026-03-22 20:00:00"

# note (HTML body required)
./scripts/create_note.sh "<h1>武汉三日游</h1><p>Day1 黄鹤楼...</p>" "iCloud"

# calendar
./scripts/create_calendar_event.sh "跑步" "个人" "2026-03-23 08:00:00" "2026-03-23 08:30:00"

# iMessage
./scripts/send_imessage.sh "zhangqianyi1995@icloud.com" "武汉下周末天气：..."
```

## Workflow

### Step 1: Clarify user intent + required fields

- Reminder: title, optional datetime
- Note: title/body content (render as HTML), optional account name
- Calendar: title, calendar name, start datetime, end datetime
- iMessage: recipient (phone or Apple ID), message text

If missing required fields, ask one concise follow-up question.

### Step 2: Execute script (not plugin)

Always call the corresponding script in `scripts/`.

Why:
- avoids low-version parser differences
- centralizes fallback logic
- easier to debug and publish

### Step 3: Confirm result to user

- If script returns an object/id or `sent`, report success.
- If no output but exit code is 0, still report success and suggest user verify in app UI.

### Step 4: On failure, diagnose quickly

Use checks from `references/troubleshooting.md`.

Most frequent root causes:
- macOS Automation permission prompt not approved
- locale-dependent date parsing format
- Messages iMessage service/account not initialized
- target calendar/account name mismatch

## Compatibility Rules (important)

1. **Avoid locale-fragile date strings** where possible.
2. **Messages**: resolve service by `service type = iMessage`, not by hard-coded service name.
3. **Calendar**: if named calendar doesn’t exist, fallback to first calendar.
4. **Notes**: if account `iCloud` is missing, fallback to default account.
5. **Notes body uses HTML** (`<h1>`, `<p>`) for stable rendering.

## Output style to user

Keep concise and concrete:
- what was created/sent
- key details (time/target)
- returned ID (if any)
- one-line next step if verification needed

## Bundled Resources

### scripts/

- `create_reminder.sh`
  - args: `<title> ["YYYY-MM-DD HH:MM:SS"]`
- `create_note.sh`
  - args: `<html-body> [account-name]`
- `create_calendar_event.sh`
  - args: `<title> <calendar-name> <start> <end>`
- `send_imessage.sh`
  - args: `<buddy(phone/appleid)> <message>`

### references/

- `troubleshooting.md`
  - permission/automation prompts
  - date parsing and locale issues
  - Messages service/account init
  - calendar/account fallback checks
  - diagnostic commands
