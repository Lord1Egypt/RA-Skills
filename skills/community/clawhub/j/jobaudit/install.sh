#!/usr/bin/env bash
# install.sh — Install SIGNAL_LOOM_TOOL skill
SKILL_NAME="jobaudit"
SKILL_SLUG="jobaudit"
VERSION="1.0.2"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OPENCLAW_SKILLS="${HOME}/.openclaw/skills"
LOCAL_BIN="${HOME}/.local/bin"

echo "Installing ${SKILL_NAME}..."
mkdir -p "$OPENCLAW_SKILLS" "$LOCAL_BIN"

# Symlink into OpenClaw skills dir
ln -sf "$SCRIPT_DIR" "$OPENCLAW_SKILLS/${SKILL_NAME}"
echo "  -> ~/.openclaw/skills/${SKILL_NAME}"

# Add to PATH
grep -q '~/.local/bin' "${HOME}/.zshrc" 2>/dev/null || echo 'export PATH="$HOME/.local/bin:$PATH"' >> "${HOME}/.zshrc"

# Fire install ping (no auth needed — tracks community installs)
curl -s -m 5 -X POST "https://api.signalloomai.com/v1/analytics/install" \
  -H "Content-Type: application/json" \
  -d "{\"skill\":\"${SKILL_SLUG}\",\"version\":\"${VERSION}\",\"source\":\"clawhub\"}" &

echo ""
echo "Done! Set your API key:"
echo "  export SL_API_KEY=your_key_here"
echo ""
echo "Get a free key: https://signalloomai.com/signup"
echo ""
echo "To use: /${SKILL_NAME} in any OpenClaw chat"
