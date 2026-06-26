#!/usr/bin/env bash
# Nex Life Logger - Setup Script
# MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
#
# Idempotent installer. Safe to run multiple times.
# Usage: bash setup.sh

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$HOME/.life-logger"
VENV_DIR="$DATA_DIR/venv"
BIN_DIR="$HOME/.local/bin"
SERVICE_NAME="nex-life-logger"

echo "============================================"
echo "  Nex Life Logger - Setup"
echo "  Built by Nex AI (nex-ai.be)"
echo "============================================"
echo ""

# Detect OS
OS="$(uname -s)"
case "$OS" in
    Linux*)  PLATFORM="linux";;
    Darwin*) PLATFORM="macos";;
    MINGW*|CYGWIN*|MSYS*) PLATFORM="windows";;
    *)       PLATFORM="unknown";;
esac
echo "Platform: $PLATFORM"
echo "Skill directory: $SKILL_DIR"
echo ""

# Step 1: Check Python
echo "[1/7] Checking Python..."
if command -v python3 &>/dev/null; then
    PYTHON="python3"
elif command -v python &>/dev/null; then
    PYTHON="python"
else
    echo "ERROR: Python 3 is required but not found." >&2
    echo "Install Python 3.9+ from https://python.org" >&2
    exit 1
fi

PY_VERSION="$($PYTHON --version 2>&1)"
echo "  Found: $PY_VERSION"

# Step 2: Create data directory
echo "[2/7] Creating data directory..."
mkdir -p "$DATA_DIR"
if [ "$PLATFORM" != "windows" ]; then
    chmod 700 "$DATA_DIR"
fi
echo "  Data directory: $DATA_DIR"

# Step 3: Create virtual environment
echo "[3/7] Setting up Python virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
    $PYTHON -m venv "$VENV_DIR"
    echo "  Created venv at $VENV_DIR"
else
    echo "  Venv already exists at $VENV_DIR"
fi

# Activate venv and install deps
VENV_PIP="$VENV_DIR/bin/pip"
VENV_PYTHON="$VENV_DIR/bin/python"
if [ "$PLATFORM" = "windows" ]; then
    VENV_PIP="$VENV_DIR/Scripts/pip"
    VENV_PYTHON="$VENV_DIR/Scripts/python"
fi

echo "[4/7] Installing Python dependencies..."
"$VENV_PIP" install --quiet --upgrade pip
"$VENV_PIP" install --quiet \
    "openai>=1.0" \
    "psutil>=5.9" \
    "youtube-transcript-api>=0.6"
echo "  Dependencies installed."

# Step 5: Initialize database
echo "[5/7] Initializing database..."
PYTHONPATH="$SKILL_DIR/lib" "$VENV_PYTHON" -c "
import sys; sys.path.insert(0, '$SKILL_DIR/lib')
from storage import init_db
init_db()
print('  Database ready at $DATA_DIR/activity.db')
"

# Step 6: Make CLI executable and create symlink
echo "[6/7] Setting up CLI tool..."
chmod +x "$SKILL_DIR/nex-life-logger.py"
chmod +x "$SKILL_DIR/lib/collector_headless.py"

# Create wrapper script that uses the venv python
mkdir -p "$BIN_DIR"
cat > "$BIN_DIR/nex-life-logger" << WRAPPER
#!/usr/bin/env bash
exec "$VENV_PYTHON" "$SKILL_DIR/nex-life-logger.py" "\$@"
WRAPPER
chmod +x "$BIN_DIR/nex-life-logger"
echo "  CLI installed to $BIN_DIR/nex-life-logger"

# Check if ~/.local/bin is on PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo "  NOTE: Add $BIN_DIR to your PATH:"
    echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo "  Add this to your ~/.bashrc or ~/.zshrc"
fi

# Step 7: Install service files
echo "[7/7] Installing background service..."
if [ "$PLATFORM" = "linux" ]; then
    SYSTEMD_DIR="$HOME/.config/systemd/user"
    mkdir -p "$SYSTEMD_DIR"

    # Write service file with correct paths
    cat > "$SYSTEMD_DIR/$SERVICE_NAME.service" << SVCEOF
[Unit]
Description=Nex Life Logger - Background Activity Collector
After=default.target

[Service]
Type=simple
ExecStart=$VENV_PYTHON $SKILL_DIR/lib/collector_headless.py
Restart=always
RestartSec=10
Environment=PYTHONUNBUFFERED=1
Environment=PYTHONPATH=$SKILL_DIR/lib

[Install]
WantedBy=default.target
SVCEOF

    systemctl --user daemon-reload
    systemctl --user enable "$SERVICE_NAME" 2>/dev/null || true
    systemctl --user start "$SERVICE_NAME" 2>/dev/null || true
    echo "  Systemd service installed and started."
    echo "  Check status: systemctl --user status $SERVICE_NAME"

elif [ "$PLATFORM" = "macos" ]; then
    AGENTS_DIR="$HOME/Library/LaunchAgents"
    mkdir -p "$AGENTS_DIR"
    PLIST="$AGENTS_DIR/com.nexai.life-logger.plist"

    cat > "$PLIST" << PLISTEOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.nexai.life-logger</string>
    <key>ProgramArguments</key>
    <array>
        <string>$VENV_PYTHON</string>
        <string>$SKILL_DIR/lib/collector_headless.py</string>
    </array>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PYTHONUNBUFFERED</key>
        <string>1</string>
        <key>PYTHONPATH</key>
        <string>$SKILL_DIR/lib</string>
    </dict>
    <key>KeepAlive</key>
    <true/>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>$DATA_DIR/collector.log</string>
    <key>StandardErrorPath</key>
    <string>$DATA_DIR/collector.log</string>
</dict>
</plist>
PLISTEOF

    launchctl unload "$PLIST" 2>/dev/null || true
    launchctl load "$PLIST"
    echo "  LaunchAgent installed and started."
    echo "  Check status: launchctl list | grep nexai"

else
    echo "  Service auto-start is available on Linux and macOS."
    echo "  On Windows, run manually:"
    echo "    $VENV_PYTHON $SKILL_DIR/lib/collector_headless.py"
fi

echo ""
echo "============================================"
echo "  Nex Life Logger installed successfully!"
echo "  Built by Nex AI (nex-ai.be)"
echo "============================================"
echo ""
echo "Next steps:"
echo "  1. Configure your LLM provider:"
echo "     nex-life-logger config set-api-key"
echo "     nex-life-logger config set-provider openai"
echo ""
echo "  2. Check collector status:"
echo "     nex-life-logger service status"
echo ""
echo "  3. View your data:"
echo "     nex-life-logger stats"
echo "     nex-life-logger activities --last 2h"
echo "     nex-life-logger search \"docker\""
echo ""
