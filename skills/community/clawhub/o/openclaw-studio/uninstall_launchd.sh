#!/bin/zsh
set -euo pipefail

UID_NOW=$(id -u)
LAUNCH_DIR="$HOME/Library/LaunchAgents"
MONITOR_LABEL="com.studywest.openclaw.arcade-monitor"
AUTOHEAL_LABEL="com.studywest.openclaw.arcade-autoheal"
WATCHDOG_LABEL="com.studywest.openclaw.app-watchdog"

launchctl bootout "gui/$UID_NOW/$MONITOR_LABEL" >/dev/null 2>&1 || true
launchctl bootout "gui/$UID_NOW/$AUTOHEAL_LABEL" >/dev/null 2>&1 || true
launchctl bootout "gui/$UID_NOW/$WATCHDOG_LABEL" >/dev/null 2>&1 || true
rm -f "$LAUNCH_DIR/$MONITOR_LABEL.plist" "$LAUNCH_DIR/$AUTOHEAL_LABEL.plist" "$LAUNCH_DIR/$WATCHDOG_LABEL.plist"

echo "Uninstalled launchd services."
