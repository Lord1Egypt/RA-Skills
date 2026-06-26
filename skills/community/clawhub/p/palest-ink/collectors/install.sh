#!/bin/bash
# Palest Ink (淡墨) - Installation Script
# 好记性不如烂笔头

set -e

PALEST_INK_DIR="$HOME/.palest-ink"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

info() { echo -e "${GREEN}[palest-ink]${NC} $1"; }
warn() { echo -e "${YELLOW}[palest-ink]${NC} $1"; }
error() { echo -e "${RED}[palest-ink]${NC} $1"; }

# Step 1: Create data directories
info "Creating data directories..."
mkdir -p "$PALEST_INK_DIR"/{data,reports,hooks,bin,tmp}

# Step 2: Write default config if not exists
if [ ! -f "$PALEST_INK_DIR/config.json" ]; then
    info "Writing default configuration..."
    cat > "$PALEST_INK_DIR/config.json" << 'CONFIGEOF'
{
  "version": 1,
  "chrome_last_visit_id": 0,
  "safari_last_visit_id": 0,
  "shell_last_line": 0,
  "vscode_last_ts": 0,
  "git_scan_last_ts": "",
  "tracked_repos": [],
  "app_last_app": "",
  "app_last_window": "",
  "app_last_ts": "",
  "app_last_record_line": -1,
  "collectors": {
    "chrome": true,
    "safari": true,
    "shell": true,
    "vscode": true,
    "git_hooks": true,
    "git_scan": true,
    "content": true,
    "app": true,
    "fsevent": true
  },
  "exclude_patterns": {
    "urls": [
      "chrome://",
      "chrome-extension://",
      "about:",
      "file://"
    ],
    "commands": [
      "^ls$",
      "^cd ",
      "^clear$",
      "^pwd$",
      "^exit$",
      "^history"
    ]
  },
  "content_fetch": {
    "max_urls_per_run": 50,
    "summary_max_chars": 800,
    "timeout_seconds": 10
  },
  "app": {
    "min_focus_seconds": 600,
    "exclude": ["loginwindow", "Dock", "SystemUIServer", "Finder", "ScreenSaverEngine"]
  },
  "app_categories": {
    "development": ["Cursor", "Code", "Xcode", "Terminal", "iTerm2", "Warp"],
    "browser": ["Google Chrome", "Safari", "Firefox", "Arc"],
    "communication": ["Slack", "WeChat", "Discord", "Zoom"]
  },
  "watched_dirs": []
}
CONFIGEOF
else
    info "Configuration already exists, skipping."
fi

# Step 3: Install git hooks
info "Installing git hooks..."

# Backup existing core.hooksPath if set
EXISTING_HOOKS_PATH=$(git config --global core.hooksPath 2>/dev/null || echo "")
if [ -n "$EXISTING_HOOKS_PATH" ] && [ "$EXISTING_HOOKS_PATH" != "$PALEST_INK_DIR/hooks" ]; then
    warn "Existing global hooksPath found: $EXISTING_HOOKS_PATH"
    warn "Backing up to config.json"
    python3 -c "
import json
with open('$PALEST_INK_DIR/config.json', 'r') as f:
    cfg = json.load(f)
cfg['previous_hooks_path'] = '$EXISTING_HOOKS_PATH'
with open('$PALEST_INK_DIR/config.json', 'w') as f:
    json.dump(cfg, f, indent=2)
"
fi

# Copy hook scripts
for hook in post-commit post-merge post-checkout pre-push; do
    cp "$SCRIPT_DIR/git_hook.sh" "$PALEST_INK_DIR/hooks/$hook"
    chmod +x "$PALEST_INK_DIR/hooks/$hook"
done

git config --global core.hooksPath "$PALEST_INK_DIR/hooks"
info "Git hooks installed (core.hooksPath -> $PALEST_INK_DIR/hooks)"

# Step 4: Copy collector scripts to bin
info "Copying collector scripts..."
cp "$SCRIPT_DIR"/collect_*.py "$PALEST_INK_DIR/bin/"
cp "$SCRIPT_DIR/cleanup.py" "$PALEST_INK_DIR/bin/"
cp "$SCRIPT_DIR/cron_collect.sh" "$PALEST_INK_DIR/bin/"
chmod +x "$PALEST_INK_DIR/bin/cron_collect.sh"

# Step 5: Install launchd agent (every 15 seconds)
info "Setting up launchd agent (every 15 seconds)..."
PLIST_LABEL="com.palest-ink.collector"
PLIST_PATH="$HOME/Library/LaunchAgents/${PLIST_LABEL}.plist"

# Remove old cron job if present
if crontab -l 2>/dev/null | grep -q "palest-ink"; then
    warn "Removing old cron job..."
    crontab -l 2>/dev/null | grep -v "palest-ink" | crontab -
fi

# Unload existing plist if present
if launchctl list | grep -q "$PLIST_LABEL" 2>/dev/null; then
    launchctl unload "$PLIST_PATH" 2>/dev/null || true
fi

cat > "$PLIST_PATH" << PLISTEOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${PLIST_LABEL}</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>${PALEST_INK_DIR}/bin/cron_collect.sh</string>
    </array>
    <key>StartInterval</key>
    <integer>15</integer>
    <key>StandardOutPath</key>
    <string>${PALEST_INK_DIR}/cron.log</string>
    <key>StandardErrorPath</key>
    <string>${PALEST_INK_DIR}/cron.log</string>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
PLISTEOF

launchctl load "$PLIST_PATH"
info "launchd agent installed (every 15 seconds)."

# Step 6: Check permissions for Safari
if [ -f "$HOME/Library/Safari/History.db" ]; then
    if ! cp "$HOME/Library/Safari/History.db" "$PALEST_INK_DIR/tmp/safari_test.db" 2>/dev/null; then
        warn "Cannot access Safari history. Please grant Full Disk Access to Terminal:"
        warn "  System Settings > Privacy & Security > Full Disk Access > Terminal.app"
    else
        rm -f "$PALEST_INK_DIR/tmp/safari_test.db"
        info "Safari history access: OK"
    fi
fi

# Step 6b: Accessibility permission notice for app focus tracking
warn ""
warn "App Focus Tracking requires Accessibility permission:"
warn "  System Settings > Privacy & Security > Accessibility > Terminal.app (enable)"
warn "Without this, collect_app.py will not be able to detect the frontmost app."

# Step 7: Check Chrome
if [ -f "$HOME/Library/Application Support/Google/Chrome/Default/History" ]; then
    info "Chrome history found: OK"
else
    warn "Chrome history not found (Chrome may not be installed)"
fi

# Step 8: Record project path for skill reference
echo "$PROJECT_DIR" > "$PALEST_INK_DIR/project_path"

info ""
info "============================================"
info "  Palest Ink installed successfully! 淡墨"
info "============================================"
info ""
info "Data directory: $PALEST_INK_DIR"
info "Git hooks: active (post-commit, post-merge, post-checkout, pre-push)"
info "launchd agent: every 15 seconds"
info ""
info "Try making a git commit — then check:"
info "  cat $PALEST_INK_DIR/data/\$(date +%Y)/\$(date +%m)/\$(date +%d).jsonl"
