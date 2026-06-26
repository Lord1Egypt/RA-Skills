#!/usr/bin/env bash
set -euo pipefail

# Writing Coach Pro — Setup Script
# Creates data directories and initializes default config

SKILL_DIR="${HOME}/.openclaw/skills/writing-coach-pro"
CONFIG_DIR="${SKILL_DIR}/config"
DATA_DIR="${SKILL_DIR}/data"
SESSION_DIR="${DATA_DIR}/session-history"
REPORTS_DIR="${SKILL_DIR}/reports"

echo "Writing Coach Pro — Setup"
echo "========================="
echo ""

# Check that the skill directory exists
if [ ! -d "${SKILL_DIR}" ]; then
    echo "Error: Skill directory not found at ${SKILL_DIR}"
    echo "Make sure you've copied writing-coach-pro/ into ~/.openclaw/skills/"
    exit 1
fi

# Create data directories
echo "Creating data directories..."
mkdir -p "${DATA_DIR}"
mkdir -p "${SESSION_DIR}"
mkdir -p "${REPORTS_DIR}"

# Set permissions — owner only
chmod 700 "${DATA_DIR}"
chmod 700 "${SESSION_DIR}"
chmod 700 "${REPORTS_DIR}"

# Initialize learning log if it doesn't exist
LEARNING_LOG="${DATA_DIR}/learning-log.json"
if [ ! -f "${LEARNING_LOG}" ]; then
    echo "Initializing learning log..."
    cat > "${LEARNING_LOG}" << 'EOF'
{
  "suggestions": [],
  "sessions": [],
  "created": "TIMESTAMP",
  "version": "1.0.0"
}
EOF
    # Replace timestamp
    if command -v date &>/dev/null; then
        TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
        if [[ "$OSTYPE" == "darwin"* ]]; then
            sed -i '' "s/TIMESTAMP/${TIMESTAMP}/" "${LEARNING_LOG}"
        else
            sed -i "s/TIMESTAMP/${TIMESTAMP}/" "${LEARNING_LOG}"
        fi
    fi
    chmod 600 "${LEARNING_LOG}"
    echo "  → Created ${LEARNING_LOG}"
else
    echo "  → Learning log already exists, skipping"
fi

# Check that settings.json exists
if [ ! -f "${CONFIG_DIR}/settings.json" ]; then
    echo ""
    echo "Warning: settings.json not found in ${CONFIG_DIR}/"
    echo "Your style profile may need to be re-created."
    echo "Tell your agent: 'set up my writing profile'"
else
    echo "  → Style profile found at ${CONFIG_DIR}/settings.json"
fi

echo ""
echo "Setup complete."
echo ""
echo "Next steps:"
echo "  1. Start (or restart) your OpenClaw session"
echo "  2. Paste some text and say 'review this'"
echo "  3. Say 'set up my writing profile' to customize preferences"
echo ""
echo "For full instructions, see SETUP-PROMPT.md"
