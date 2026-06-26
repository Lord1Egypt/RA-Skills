# macOS LaunchDaemon (alternative to cron)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>ai.openclaw.watchdog</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>/Users/USERNAME/.openclaw/watchdog.sh</string>
  </array>
  <key>StartInterval</key>
  <integer>60</integer>
  <key>RunAtLoad</key>
  <true/>
  <key>StandardOutPath</key>
  <string>/Users/USERNAME/.openclaw/watchdog-launchd.log</string>
  <key>StandardErrorPath</key>
  <string>/Users/USERNAME/.openclaw/watchdog-launchd.log</string>
</dict>
</plist>
```

Save as `~/Library/LaunchAgents/ai.openclaw.watchdog.plist`, then:

```bash
# Replace USERNAME in the plist first
sed -i '' "s/USERNAME/$(whoami)/g" ~/Library/LaunchAgents/ai.openclaw.watchdog.plist

launchctl load ~/Library/LaunchAgents/ai.openclaw.watchdog.plist
```
