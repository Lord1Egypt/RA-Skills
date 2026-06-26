#!/usr/bin/env bash
# Nex HealthCheck - Setup Script
# MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)
#
# Idempotent installer. Safe to run multiple times.
# Usage: bash setup.sh

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$HOME/.nex-healthcheck"
BIN_DIR="$HOME/.local/bin"
SERVICE_NAME="nex-healthcheck"

echo "============================================"
echo "  Nex HealthCheck - Setup"
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
echo "[1/4] Checking Python..."
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
echo "[2/4] Creating data directory..."
mkdir -p "$DATA_DIR"
if [ "$PLATFORM" != "windows" ]; then
    chmod 700 "$DATA_DIR"
fi
echo "  Data directory: $DATA_DIR"

# Step 3: Initialize database
echo "[3/4] Initializing database..."
PYTHONPATH="$SKILL_DIR/lib" $PYTHON -c "
import sys; sys.path.insert(0, '$SKILL_DIR/lib')
from storage import init_db
init_db()
print('  Database ready at $DATA_DIR/healthcheck.db')
"

# Step 4: Make CLI executable and create symlink
echo "[4/4] Setting up CLI tool..."
chmod +x "$SKILL_DIR/nex-healthcheck.py"

mkdir -p "$BIN_DIR"
cat > "$BIN_DIR/nex-healthcheck" << WRAPPER
#!/usr/bin/env bash
PYTHONPATH="$SKILL_DIR/lib" exec $PYTHON "$SKILL_DIR/nex-healthcheck.py" "\$@"
WRAPPER
chmod +x "$BIN_DIR/nex-healthcheck"
echo "  CLI installed to $BIN_DIR/nex-healthcheck"

# Check if ~/.local/bin is on PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo "  NOTE: Add $BIN_DIR to your PATH:"
    echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo "  Add this to your ~/.bashrc or ~/.zshrc"
fi

# Optional: Install systemd timer for periodic checks (Linux only)
if [ "$PLATFORM" = "linux" ]; then
    echo ""
    echo "Optional: Install systemd timer for automatic checks?"
    echo "This will run 'nex-healthcheck check' every 5 minutes."
    echo ""
    read -p "Install systemd timer? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        SYSTEMD_DIR="$HOME/.config/systemd/user"
        mkdir -p "$SYSTEMD_DIR"

        # Service file
        cat > "$SYSTEMD_DIR/$SERVICE_NAME.service" << SVCEOF
[Unit]
Description=Nex HealthCheck - Periodic Health Monitor
After=default.target

[Service]
Type=oneshot
ExecStart=$BIN_DIR/nex-healthcheck check
Environment=PYTHONPATH=$SKILL_DIR/lib

[Install]
WantedBy=default.target
SVCEOF

        # Timer file
        cat > "$SYSTEMD_DIR/$SERVICE_NAME.timer" << TIMEREOF
[Unit]
Description=Nex HealthCheck - Periodic Health Monitor Timer
Requires=$SERVICE_NAME.service

[Timer]
OnBootSec=1min
OnUnitActiveSec=5min
Persistent=true

[Install]
WantedBy=timers.target
TIMEREOF

        systemctl --user daemon-reload
        systemctl --user enable "$SERVICE_NAME.timer" 2>/dev/null || true
        systemctl --user start "$SERVICE_NAME.timer" 2>/dev/null || true
        echo "  Systemd timer installed and started."
        echo "  Check status: systemctl --user status $SERVICE_NAME.timer"
        echo "  View logs: journalctl --user -u $SERVICE_NAME -f"
    fi
fi

echo ""
echo "============================================"
echo "  Nex HealthCheck installed successfully!"
echo "  Built by Nex AI (nex-ai.be)"
echo "============================================"
echo ""
echo "Next steps:"
echo "  1. Add a service to monitor:"
echo "     nex-healthcheck add --name \"My Site\" --type http --target \"https://example.com\""
echo ""
echo "  2. Run a check:"
echo "     nex-healthcheck check"
echo ""
echo "  3. View dashboard:"
echo "     nex-healthcheck dashboard"
echo ""
echo "  4. (Optional) Configure Telegram notifications:"
echo "     export HEALTHCHECK_TELEGRAM_TOKEN=\"your_token\""
echo "     export HEALTHCHECK_TELEGRAM_CHAT=\"your_chat_id\""
echo "     nex-healthcheck notify"
echo ""
echo "For more help, see:"
echo "  nex-healthcheck --help"
echo "  cat $SKILL_DIR/SKILL.md"
echo ""
