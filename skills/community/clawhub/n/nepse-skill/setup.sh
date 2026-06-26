#!/bin/bash
# NEPSE Skill Setup Script for OpenClaw on Pop OS 24.04
# Run this once to install and configure the skill.
# Usage: bash setup.sh

set -e

SKILL_NAME="nepse_analyst"
OPENCLAW_WORKSPACE="${HOME}/.openclaw/workspace"
SKILLS_DIR="${OPENCLAW_WORKSPACE}/skills"
TARGET_DIR="${SKILLS_DIR}/${SKILL_NAME}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== NEPSE Analyst Skill Setup ==="
echo ""

# 1. install python deps
echo "[1/4] Installing Python dependencies..."
pip3 install requests beautifulsoup4 numpy --break-system-packages --quiet
echo "  ✓ Python deps installed"

# 2. create skill directory in openclaw workspace
echo "[2/4] Creating skill directory at ${TARGET_DIR}..."
mkdir -p "${TARGET_DIR}/scripts"
mkdir -p "${TARGET_DIR}/data"

# 3. copy files
echo "[3/4] Copying skill files..."
cp "${SCRIPT_DIR}/SKILL.md" "${TARGET_DIR}/SKILL.md"
cp "${SCRIPT_DIR}/scripts/nepse_fetch.py" "${TARGET_DIR}/scripts/nepse_fetch.py"
chmod +x "${TARGET_DIR}/scripts/nepse_fetch.py"
echo "  ✓ Files copied"

# 4. set up env vars (Telegram)
echo "[4/4] Telegram configuration..."
echo ""
echo "  Enter your Telegram Bot Token (leave blank to skip):"
read -r BOT_TOKEN
echo "  Enter your Telegram Chat ID (leave blank to skip):"
read -r CHAT_ID

if [ -n "$BOT_TOKEN" ] && [ -n "$CHAT_ID" ]; then
    OPENCLAW_JSON="${HOME}/.openclaw/openclaw.json"
    echo ""
    echo "  Add these to your openclaw.json under 'skills.entries.nepse_analyst.env':"
    echo ""
    echo '  "skills": {'
    echo '    "entries": {'
    echo '      "nepse_analyst": {'
    echo '        "enabled": true,'
    echo '        "env": {'
    echo "          \"TELEGRAM_BOT_TOKEN\": \"${BOT_TOKEN}\","
    echo "          \"TELEGRAM_CHAT_ID\": \"${CHAT_ID}\""
    echo '        }'
    echo '      }'
    echo '    }'
    echo '  }'
    echo ""
    echo "  Or export them in your shell: add to ~/.bashrc:"
    echo "  export TELEGRAM_BOT_TOKEN=\"${BOT_TOKEN}\""
    echo "  export TELEGRAM_CHAT_ID=\"${CHAT_ID}\""
fi

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Directory structure created:"
echo "  ${TARGET_DIR}/"
echo "  ├── SKILL.md"
echo "  ├── data/          (watchlist.json, alerts.json stored here)"
echo "  └── scripts/"
echo "      └── nepse_fetch.py"
echo ""
echo "Next steps:"
echo "  1. Restart OpenClaw gateway: openclaw gateway restart"
echo "     OR send /new in your Telegram chat"
echo "  2. Test: ask 'analyze NABIL' in your Telegram chat"
echo "  3. For cron alerts: set up a scheduled task in OpenClaw Control UI"
echo "     Schedule: 0 15 * * 1-5 (3pm NPT, Mon-Fri)"
echo "     Command:  python3 ${TARGET_DIR}/scripts/nepse_fetch.py cron-check"
echo ""
echo "Quick test right now:"
echo "  python3 ${TARGET_DIR}/scripts/nepse_fetch.py price NABIL"
