# Mac Reminders Agent

**v1.2.0** | macOS Reminders app integration skill for OpenClaw/Claude agents.

## Features

- 📋 List reminders (today/week/all) with unique IDs
- ➕ Add new reminders with due dates
- ✏️ **Edit reminders** by ID (title, due date, notes)
- 🗑️ **Delete reminders** by ID
- ✅ **Complete reminders** by ID
- 🔄 **Native Recurrence**: Weekly, daily, monthly, yearly repeating reminders (single reminder, not duplicates)
- 🌍 Multi-language support (en, ko, ja, zh)
- ⏰ Cron-compatible for scheduled checks
- ☁️ **iCloud Sync**: Reminders sync automatically to all devices (iPhone, iPad, Mac) logged into the same Apple ID

## iCloud Sync

When you add or modify reminders using this skill on your Mac, they **automatically sync to all your Apple devices** (iPhone, iPad, Apple Watch, other Macs) logged into the same Apple ID via iCloud.

This means:
- ✅ Add a reminder via agent → appears on your iPhone instantly
- ✅ Complete a reminder on iPhone → reflected in agent queries
- ✅ No manual sync required

> **Note**: Ensure iCloud Reminders is enabled in System Settings → Apple ID → iCloud → Reminders

## Requirements

- **macOS only** (uses AppleScript + EventKit)
- Node.js 18+
- `applescript` npm module
- Swift (included with Xcode Command Line Tools)
- iCloud Reminders enabled (for cross-device sync)

> **Note**: Swift is required for native recurrence support. It's pre-installed on macOS with Xcode Command Line Tools. Run `xcode-select --install` if missing.

## Installation

### 1. Install to OpenClaw workspace

```bash
# Copy skill to workspace
cp -r mac-reminders-agent ~/clawd/skills/

# Install dependency
cd ~/clawd && npm install applescript
```

### 2. Or install via ClawHub (after publishing)

```bash
clawhub install mac-reminders-agent
```

## Usage

### List Reminders

```bash
# Today's reminders (English)
node skills/mac-reminders-agent/cli.js list --scope today

# This week's reminders (Korean)
node skills/mac-reminders-agent/cli.js list --scope week --locale ko

# All reminders (Japanese)
node skills/mac-reminders-agent/cli.js list --scope all --locale ja
```

**Output:**
```json
{
  "locale": "ko",
  "labels": {
    "list_header_incomplete": "미완료 미리알림",
    "list_header_completed": "완료됨"
  },
  "items": [
    { "title": "회의", "due": "2026년 2월 5일 09:00:00" },
    { "title": "보고서 제출", "due": null }
  ]
}
```

### Add Reminder

```bash
# Basic (English)
node skills/mac-reminders-agent/cli.js add --title "Meeting"

# With due date (Korean)
node skills/mac-reminders-agent/cli.js add \
  --title "회의" \
  --due "2026-02-05T09:00:00+09:00" \
  --locale ko

# With note
node skills/mac-reminders-agent/cli.js add \
  --title "Call John" \
  --due "2026-02-05T15:00:00+09:00" \
  --note "Discuss project timeline"
```

### Edit Reminder

```bash
# First, list reminders to get the ID
node skills/mac-reminders-agent/cli.js list --scope today --locale ko

# Edit title
node skills/mac-reminders-agent/cli.js edit --id "ABC123" --title "Updated Meeting" --locale ko

# Edit due date
node skills/mac-reminders-agent/cli.js edit --id "ABC123" --due "2026-03-01T10:00:00+09:00"
```

### Delete Reminder

```bash
node skills/mac-reminders-agent/cli.js delete --id "ABC123" --locale ko
```

### Complete Reminder

```bash
node skills/mac-reminders-agent/cli.js complete --id "ABC123" --locale ko
```

### Recurring Reminders (Native Recurrence)

```bash
# Weekly reminder
node skills/mac-reminders-agent/cli.js add \
  --title "Weekly standup" \
  --due "2026-02-10T09:00:00+09:00" \
  --repeat weekly

# Bi-weekly reminder
node skills/mac-reminders-agent/cli.js add \
  --title "Sprint review" \
  --due "2026-02-10T14:00:00+09:00" \
  --repeat weekly \
  --interval 2

# Monthly reminder with end date
node skills/mac-reminders-agent/cli.js add \
  --title "Monthly report" \
  --due "2026-02-28T17:00:00+09:00" \
  --repeat monthly \
  --repeat-end 2026-12-31
```

> **Why Swift?** macOS Reminders AppleScript doesn't expose the `recurrence` property. Native recurrence requires EventKit (Swift). This creates a **single reminder with repeat rule**, not multiple duplicates.

**Output:**
```json
{
  "ok": true,
  "title": "회의",
  "due": "2026-02-05T09:00:00+09:00",
  "locale": "ko",
  "message": "'회의' 미리알림을 추가했어요 (2026-02-05T09:00:00+09:00)."
}
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--scope` | No | `today`, `week`, `all` (default: `week`) |
| `--id` | Yes (edit/delete/complete) | Reminder ID from list output |
| `--title` | Yes (add) | Reminder title |
| `--due` | No | ISO 8601 format: `YYYY-MM-DDTHH:mm:ss+09:00` |
| `--note` | No | Additional notes |
| `--repeat` | No | `daily`, `weekly`, `monthly`, `yearly` |
| `--interval` | No | Repeat interval (default: 1). e.g., `2` = every 2 weeks |
| `--repeat-end` | No | End date: `YYYY-MM-DD` |
| `--locale` | No | `en`, `ko`, `ja`, `zh` (default: `en`) |

## Customization

### Adding New Languages

Edit `locales.json` to add new languages:

```json
{
  "es": {
    "name": "Español",
    "triggers": {
      "list": ["¿Qué tengo que hacer hoy?"],
      "add": ["Añadir un recordatorio para mañana"]
    },
    "responses": {
      "added": "Recordatorio '{title}' añadido{due_text}.",
      "added_no_due": " sin fecha límite",
      "added_with_due": " para {due}",
      "list_header_incomplete": "Recordatorios pendientes",
      "list_header_completed": "Completados",
      "no_reminders": "No se encontraron recordatorios.",
      "error_access": "Hubo un problema al acceder a la app Recordatorios.",
      "ask_when": "¿Cuándo necesitas este recordatorio?"
    }
  }
}
```

### Changing Default Reminder List

By default, reminders are added to the **default list**. To change this, edit `reminders/apple-bridge.js`:

```applescript
# Find this line:
tell default list

# Change to specific list:
tell list "Work"
```

### Timezone Configuration

Default timezone is `+09:00` (KST). To change, edit `reminders/apple-bridge.js`:

```javascript
// Find parseISO function, modify the regex:
const m = dueISO.match(/^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):\d{2}\+09:00$/);

// Change +09:00 to your timezone, e.g., +00:00 for UTC
```

## Cron Usage Examples

### OpenClaw Cron Integration

Add to your OpenClaw cron configuration (`~/.openclaw/openclaw.json`):

```json
{
  "cron": {
    "jobs": [
      {
        "name": "morning-reminders",
        "schedule": "0 9 * * *",
        "command": "Check today's reminders and summarize priorities",
        "agent": "main"
      },
      {
        "name": "weekly-review",
        "schedule": "0 18 * * 5",
        "command": "Review this week's completed reminders and plan for next week",
        "agent": "main"
      }
    ]
  }
}
```

### Direct Cron (crontab)

```bash
# Edit crontab
crontab -e

# Morning reminder check (9 AM daily)
0 9 * * * cd ~/clawd && node skills/mac-reminders-agent/cli.js list --scope today --locale ko >> /tmp/reminders.log 2>&1

# Weekly summary (Friday 6 PM)
0 18 * * 5 cd ~/clawd && node skills/mac-reminders-agent/cli.js list --scope week --locale ko >> /tmp/weekly-reminders.log 2>&1
```

### Telegram Bot Cron Example

Configure OpenClaw to send reminders via Telegram:

```json
{
  "cron": {
    "jobs": [
      {
        "name": "telegram-morning-brief",
        "schedule": "0 8 * * *",
        "command": "오늘 미리알림 확인해서 텔레그램으로 요약해줘",
        "agent": "main",
        "channel": "telegram"
      }
    ]
  }
}
```

### LaunchAgent (macOS Native)

Create `~/Library/LaunchAgents/com.reminders.daily.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.reminders.daily</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/node</string>
        <string>/Users/YOUR_USERNAME/clawd/skills/mac-reminders-agent/cli.js</string>
        <string>list</string>
        <string>--scope</string>
        <string>today</string>
        <string>--locale</string>
        <string>ko</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/tmp/reminders-daily.log</string>
</dict>
</plist>
```

Load with:
```bash
launchctl load ~/Library/LaunchAgents/com.reminders.daily.plist
```

## Agent Prompts Examples

### Morning Brief (Korean)
```
오늘 미리알림 확인해서 우선순위 정리해줘.
긴급한 것 먼저, 그다음 중요한 것 순서로.
```

### Weekly Planning (English)
```
Check this week's reminders and create a daily breakdown.
Group by work vs personal, and highlight any overdue items.
```

### Add via Natural Language
```
내일 오전 10시에 "팀 미팅" 미리알림 추가해줘
```

## Troubleshooting

### "applescript module not found"
```bash
cd ~/clawd && npm install applescript
```

### "Reminders app access denied"
Grant Terminal/iTerm automation permissions:
1. System Preferences → Privacy & Security → Automation
2. Enable "Reminders" for Terminal

### Reminders not showing
- Check if reminders are in the **default list**
- Verify date range with `--scope all`

### "swift: command not found" (recurring reminders)
Swift is required for native recurrence. Install Xcode Command Line Tools:
```bash
xcode-select --install
```

### Recurrence not working
- Verify Swift is available: `swift --version`
- Check `reminders/eventkit-bridge.swift` exists
- Ensure Reminders app has proper permissions

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for version history.

## License

MIT License - Free to use, modify, and distribute (including commercial use). See [LICENSE](./LICENSE).

## Author

**swancho**
