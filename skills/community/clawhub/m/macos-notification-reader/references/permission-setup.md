# Permission Setup Guide

## Required: Full Disk Access

This skill requires **Full Disk Access** permission to read the macOS notification database.

### Why?

The notification database is stored in a protected location:
```
~/Library/Group Containers/group.com.apple.usernoted/db2/db
```

Without Full Disk Access, you will get:
```
PermissionError: [Errno 1] Operation not permitted
```

### How to Grant

#### Method 1: Via System Settings (Recommended)

1. Open **System Settings**
2. Go to **Privacy & Security**
3. Scroll down and click **Full Disk Access**
4. Click the 🔒 lock icon in the bottom left, enter your password to unlock
5. Click **+**
6. Press `Cmd + Shift + G`
7. Enter `/usr/bin/python3` and press Enter
8. Click **Open**
9. Make sure the toggle is **ON** ✅

#### Method 2: Via Terminal (Advanced)

```bash
# Add python3 to Full Disk Access (requires sudo and may vary by system)
# Research the correct command for your macOS version
sudo dscl . append ~/Library/Preferences/com.apple.security.common file /usr/bin/python3
```

Note: Method 2 may not work on newer macOS versions. Use Method 1 for reliability.

### Verify Permission

Run:
```bash
python3 -c "import os; print('OK' if os.access(os.path.expanduser('~/Library/Group Containers/group.com.apple.usernoted/db2/db'), os.R_OK) else 'FAIL')"
```

If it prints `OK`, permission is granted. If `FAIL`, you need to add the permission.

### Troubleshooting

#### Still getting permission error?

1. Make sure you've added `/usr/bin/python3`, not just `python3`
2. If using a virtual environment, add the Python binary from the venv:
   ```bash
   which python3  # Get the actual path
   # Add that path instead
   ```

#### Permission granted but still not working?

1. Restart Terminal or IDE
2. If running via cron or launchd, you may need to restart the service

#### How to Check Current Permission Status

```bash
# Check if python3 can access the database
python3 -c "
from pathlib import Path
p = Path.home() / 'Library' / 'Group Containers' / 'group.com.apple.usernoted' / 'db2' / 'db'
print('Exists:', p.exists())
print('Readable:', p.is_file())
"
```

## Database Location

| macOS Version | Path |
|--------------|------|
| 15+ (Sequoia) | `~/Library/Group Containers/group.com.apple.usernoted/db2/db` |
| 14 and earlier | `~/Library/Group Containers/group.com.apple.usernoted/db2/db` or `/var/folders/xx/.../com.apple.notificationcenter/db2/db` |

## Data Retention

- macOS automatically deletes notifications after ~3-7 days
- Cannot be configured by users
- This skill can only access notifications that still exist in the database
