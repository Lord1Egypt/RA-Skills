# Troubleshooting (macOS low-version friendly)

## 1) Script hangs then SIGTERM

Most common cause: macOS privacy prompt is waiting for approval.

Do this once on the Mac UI:
- System Settings → Privacy & Security → Automation
- Allow terminal/host app to control: Reminders, Notes, Calendar, Messages
- Also allow Full Disk Access if your environment requires it

Then rerun the same command.

## 2) Calendar date parsing fails (-1728)

Avoid locale-dependent date strings like `"March 23, 2026 08:00:00"`.
Use either:
- `date "YYYY-MM-DD HH:MM:SS"` (script argv form), or
- `current date` + set day/time arithmetic in AppleScript.

## 3) Messages cannot find account/service

Do not assume service name text.
Use:
- `first service whose service type = iMessage`

If still failing:
- open Messages app once manually
- ensure iMessage account is logged in
- send one manual message to initialize account state

## 4) Notes account "iCloud" not found

Some systems use different account labels.
Use fallback logic:
- if `account "iCloud"` exists, use it
- else create note in default Notes account

## 5) Chinese calendar name missing

Calendar may not have `"个人"`.
Use fallback:
- if target calendar exists, use it
- else use `calendar 1`

## 6) Quick diagnostics

```bash
osascript -e 'tell application "Calendar" to get name of every calendar'
osascript -e 'tell application "Messages" to get service type of every service'
osascript -e 'tell application "Reminders" to count reminders'
osascript -e 'tell application "Notes" to count notes'
```
