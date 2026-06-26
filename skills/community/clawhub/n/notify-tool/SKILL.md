---
name: notify-tool
description: Send desktop notifications from command line scripts and automated tasks. Use for alerts, reminders, and process completion notifications.
---
# Notify - Desktop Alert Utility

Display system notifications with customizable title, message, and urgency level. Integrates with desktop notification daemons for visual alerts.

## Usage
```bash
notify-tool [options] <message>
```

## Options

- `-t title`: Set notification title
- `-u level`: Urgency (low, normal, critical)
- `-e`: Expire notification after timeout

## Examples

```bash
# Simple notification
notify-tool "Task complete!"

# With title
notify-tool -t "Backup" "Backup finished successfully"

# Critical alert
notify-tool -u critical "Disk space low!"
```