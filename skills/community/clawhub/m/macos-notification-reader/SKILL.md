# macOS Notification Reader

Reads the macOS notification center database and exports recent notifications to markdown files. Also supports automated **work notification summary** with filtering and delivery.

## Features

- 📱 **Multi-app support**: WeChat, Teams, Outlook, Mail, iMessage, Calendar, Reminders, and more
- ⏰ **Time filtering**: Fetch notifications from the last N minutes or hours
- 📅 **Date-organized output**: Exports to `memory/YYYY-MM-DD/computer_io/notification/`
- 🤖 **Cron scheduling**: Designed for automated periodic exports
- 📊 **Work notification summary**: Auto-filter work-related notifications (Teams/Outlook) and generate summaries
- 🔒 **Privacy-friendly**: Reads from local database only, no cloud upload

## Quick Start

### 1. Grant Full Disk Access (Required)

This skill requires Full Disk Access to read the macOS notification database.

```bash
# Verify permission
python3 -c "import os; print('OK' if os.access(os.path.expanduser('~/Library/Group Containers/group.com.apple.usernoted/db2/db'), os.R_OK) else 'FAIL')"
```

If it returns `FAIL`, follow these steps:

1. Open **System Settings** → **Privacy & Security** → **Full Disk Access**
2. Click the 🔒 lock and enter your password
3. Click **+**, press `Cmd+Shift+G`, enter `/usr/bin/python3`, click **Open**
4. Ensure the toggle is **ON**

> **Note**: If using a virtual environment, add the Python binary from that venv instead.

### 2. Test the Scripts

```bash
# Navigate to the skill directory
cd /path/to/macos-notification-reader

# Basic: Read notifications from the last 35 minutes
python3 scripts/read_notifications.py --minutes 35

# Basic: Read notifications from the last 24 hours
python3 scripts/read_notifications.py --hours 24

# Advanced: Generate work notification summary (every 30 min)
bash scripts/work-summary.sh
```

### 3. Set Up Cron Jobs (Recommended)

#### Option A: Basic Notification Export (every 30 min)

```bash
# Edit crontab
crontab -e

# Add this line:
*/30 * * * * /path/to/macos-notification-reader/scripts/export-notification.sh
```

#### Option B: Work Notification Summary (every 30 min)

This filters work-related notifications (Teams, Outlook) and generates a summary:

```bash
crontab -e

# Add this line:
*/30 * * * * /path/to/macos-notification-reader/scripts/work-summary.sh
```

Or use OpenClaw's built-in cron:

```bash
openclaw cron add --name "Work Notification Summary" --every "30m" --message "Run work-summary.sh"
```

## Scripts

| Script | Purpose |
|--------|---------|
| `read_notifications.py` | Core script - reads raw notifications from database |
| `export-notification.sh` | Exports all notifications to markdown |
| `work-summary.sh` | Filters work notifications and generates summary |

## Work Notification Summary

The `work-summary.sh` script does:

1. **Filters work apps**: Teams, Outlook, WeChat (work-related)
2. **Extracts action items**: Identifies pending tasks from message content
3. **Generates summary**: Creates a structured markdown report
4. **Saves to**: `memory/YYYY-MM-DD/computer_io/notification/work-summary-YYYYMMDD-HHMMSS.md`

### Summary Output Format

```markdown
# 工作通知摘要
- Lookback: 过去 35 分钟
- 总工作通知: 5 条

## 渠道分布
- Teams: 3
- Outlook: 2

## 待处理事项（自动提取）
- [时间] (app) 消息内容摘要

## 最近工作通知（去重后）
- [时间] (app) 消息内容
```

## Output Directory

By default, exports go to:
```
~/.openclaw/workspace/memory/YYYY-MM-DD/computer_io/notification/
```

To customize, edit the scripts and change the `OUTPUT_DIR` variable.

## Supported Apps

The script recognizes these apps by default:

| Bundle ID | Display Name |
|-----------|--------------|
| com.tencent.xinWeChat | WeChat |
| com.microsoft.teams2 | Teams |
| com.microsoft.Outlook | Outlook |
| com.apple.mail | Mail |
| com.apple.mobilesms | iMessage |
| com.apple.ical | Calendar |
| com.apple.reminders | Reminders |

To add more apps, edit the `simplify_app_name()` function in `read_notifications.py`.

## Limitations

- ⚠️ **macOS only**: This skill only works on macOS
- ⚠️ **Full Disk Access required**: Must be granted manually (see above)
- ⚠️ **Limited retention**: macOS automatically deletes notifications after ~3-7 days
- ⚠️ **Notification state**: Cannot read notifications that have been dismissed

## File Structure

```
macos-notification-reader/
├── SKILL.md                       # This file
├── _meta.json                     # Skill metadata
├── scripts/
│   ├── read_notifications.py      # Core script (file output)
│   ├── export-notification.sh     # Basic export wrapper
│   └── work-summary.sh            # Work notification summary (NEW)
└── references/
    └── permission-setup.md        # Detailed permission guide
```

## Use Cases

- 📊 **Review missed notifications**: See what you missed while away
- 🔍 **Debug notification issues**: Check if a specific app sent a notification
- 📝 **Daily logging**: Automatically archive notifications
- 💼 **Work summary**: Get incremental work notification summaries every 30 min
- 🤖 **Automation**: Integrate with other tools via markdown output

## Troubleshooting

### "Permission denied" error

Grant Full Disk Access. See [references/permission-setup.md](references/permission-setup.md).

### "Cannot find notification database"

- Ensure macOS 15.0 or later
- Check: `ls -la ~/Library/Group\ Containers/group.com.apple.usernoted/db2/`

### Notifications are empty

- macOS may have deleted old notifications
- Try reducing time window: `--minutes 10`

---

**Author**: OpenClaw Community  
**Version**: 1.1.0  
**Platform**: macOS 15.0+  
**License**: MIT
