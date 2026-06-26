#!/bin/zsh
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
UID_NOW=$(id -u)
LAUNCH_DIR="$HOME/Library/LaunchAgents"
mkdir -p "$LAUNCH_DIR"

MONITOR_PLIST="$LAUNCH_DIR/com.studywest.openclaw.arcade-monitor.plist"
AUTOHEAL_PLIST="$LAUNCH_DIR/com.studywest.openclaw.arcade-autoheal.plist"
WATCHDOG_PLIST="$LAUNCH_DIR/com.studywest.openclaw.app-watchdog.plist"

cat > "$MONITOR_PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.studywest.openclaw.arcade-monitor</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>-u</string>
    <string>$DIR/server.py</string>
  </array>
  <key>WorkingDirectory</key><string>$DIR</string>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>StandardOutPath</key><string>$DIR/launchd-monitor.out.log</string>
  <key>StandardErrorPath</key><string>$DIR/launchd-monitor.err.log</string>
</dict>
</plist>
EOF

cat > "$AUTOHEAL_PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.studywest.openclaw.arcade-autoheal</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>-u</string>
    <string>$DIR/autoheal.py</string>
  </array>
  <key>WorkingDirectory</key><string>$DIR</string>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>StandardOutPath</key><string>$DIR/launchd-autoheal.out.log</string>
  <key>StandardErrorPath</key><string>$DIR/launchd-autoheal.err.log</string>
</dict>
</plist>
EOF

cat > "$WATCHDOG_PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.studywest.openclaw.app-watchdog</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>-u</string>
    <string>$DIR/app_watchdog.py</string>
  </array>
  <key>WorkingDirectory</key><string>$DIR</string>
  <key>RunAtLoad</key><true/>
  <key>StartInterval</key><integer>30</integer>
  <key>StandardOutPath</key><string>$DIR/launchd-watchdog.out.log</string>
  <key>StandardErrorPath</key><string>$DIR/launchd-watchdog.err.log</string>
</dict>
</plist>
EOF

# unload if exists
launchctl bootout "gui/$UID_NOW/com.studywest.openclaw.arcade-monitor" >/dev/null 2>&1 || true
launchctl bootout "gui/$UID_NOW/com.studywest.openclaw.arcade-autoheal" >/dev/null 2>&1 || true
launchctl bootout "gui/$UID_NOW/com.studywest.openclaw.app-watchdog" >/dev/null 2>&1 || true

launchctl bootstrap "gui/$UID_NOW" "$MONITOR_PLIST"
launchctl bootstrap "gui/$UID_NOW" "$AUTOHEAL_PLIST"
launchctl bootstrap "gui/$UID_NOW" "$WATCHDOG_PLIST"
launchctl enable "gui/$UID_NOW/com.studywest.openclaw.arcade-monitor"
launchctl enable "gui/$UID_NOW/com.studywest.openclaw.arcade-autoheal"
launchctl enable "gui/$UID_NOW/com.studywest.openclaw.app-watchdog"
launchctl kickstart -k "gui/$UID_NOW/com.studywest.openclaw.arcade-monitor"
launchctl kickstart -k "gui/$UID_NOW/com.studywest.openclaw.arcade-autoheal"
launchctl kickstart -k "gui/$UID_NOW/com.studywest.openclaw.app-watchdog"

echo "Installed and started launchd services."
echo "- com.studywest.openclaw.arcade-monitor"
echo "- com.studywest.openclaw.arcade-autoheal"
echo "- com.studywest.openclaw.app-watchdog"
