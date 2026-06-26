#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_NAME="humanos"
OPENCLAW_DIR="${HOME}/.openclaw"
SKILLS_DIR="${OPENCLAW_DIR}/skills"
CONFIG_FILE="${OPENCLAW_DIR}/openclaw.json"

echo "Installing ${SKILL_NAME} skill for OpenClaw..."

# Create skills directory if needed
mkdir -p "$SKILLS_DIR"

# Remove existing symlink if present
if [[ -L "${SKILLS_DIR}/${SKILL_NAME}" ]]; then
  rm "${SKILLS_DIR}/${SKILL_NAME}"
  echo "  Removed existing symlink"
fi

# Create symlink
ln -s "$SKILL_DIR" "${SKILLS_DIR}/${SKILL_NAME}"
echo "  Linked ${SKILL_DIR} -> ${SKILLS_DIR}/${SKILL_NAME}"

# Create minimal config if missing
if [[ ! -f "$CONFIG_FILE" ]]; then
  cat > "$CONFIG_FILE" << 'JSONEOF'
{
  "skills": {
    "entries": {
      "humanos": {
        "enabled": true,
        "env": {
          "VIA_API_KEY": "REPLACE_WITH_YOUR_API_KEY",
          "VIA_SIGNATURE_SECRET": "REPLACE_WITH_YOUR_SECRET"
        }
      }
    }
  }
}
JSONEOF
  echo "  Created ${CONFIG_FILE} — edit it with your API credentials"
else
  echo "  Config already exists at ${CONFIG_FILE}"
  echo "  Make sure it has VIA_API_KEY and VIA_SIGNATURE_SECRET for the humanos skill"
fi

# Check for openclaw CLI
if ! command -v openclaw &>/dev/null; then
  echo ""
  echo "  WARNING: openclaw CLI not found in PATH"
  echo "  Install it from https://openclaw.ai or https://clawhub.ai"
fi

echo ""
echo "Next steps:"
echo "  1. Edit ${CONFIG_FILE} with your VIA API credentials from https://app.humanos.id"
echo "  2. Restart OpenClaw or run: openclaw skills list --eligible"
echo "  3. Test with: openclaw run 'I need approval from someone@example.com for a payment'"
