#!/bin/bash
# linkedin-autopilot/scripts/setup.sh — Initialize config and data directories

set -euo pipefail

CONFIG_DIR="${LINKEDIN_AUTOPILOT_DIR:-$HOME/.config/linkedin-autopilot}"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "🤝 LinkedIn Autopilot Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Create config directory
mkdir -p "$CONFIG_DIR"
echo "✓ Created $CONFIG_DIR"

# Copy example config if none exists
if [ ! -f "$CONFIG_DIR/config.json" ]; then
  cp "$SKILL_DIR/config.example.json" "$CONFIG_DIR/config.json"
  echo "✓ Created config.json (from example — edit with your targets and sequences)"
else
  echo "• config.json already exists (skipped)"
fi

# Initialize data files
for file in posts-queue.json engagement-history.json dm-sequences.json connections.json analytics.json activity-log.json; do
  if [ ! -f "$CONFIG_DIR/$file" ]; then
    case "$file" in
      posts-queue.json)
        echo '{"posts":[]}' > "$CONFIG_DIR/$file"
        ;;
      engagement-history.json)
        echo '{"engagements":{}}' > "$CONFIG_DIR/$file"
        ;;
      dm-sequences.json)
        echo '{"sequences":{}}' > "$CONFIG_DIR/$file"
        ;;
      connections.json)
        echo '{"connections":{}}' > "$CONFIG_DIR/$file"
        ;;
      analytics.json)
        echo '{"history":[]}' > "$CONFIG_DIR/$file"
        ;;
      activity-log.json)
        echo '[]' > "$CONFIG_DIR/$file"
        ;;
    esac
    echo "✓ Created $file"
  else
    echo "• $file already exists (skipped)"
  fi
done

# Check for credentials
SECRETS_FILE="$HOME/.clawdbot/secrets.env"
if [ -f "$SECRETS_FILE" ]; then
  if grep -q "LINKEDIN_EMAIL" "$SECRETS_FILE" 2>/dev/null && grep -q "LINKEDIN_PASSWORD" "$SECRETS_FILE" 2>/dev/null; then
    echo "✓ LINKEDIN_EMAIL and LINKEDIN_PASSWORD found in secrets.env"
  else
    echo "⚠ LinkedIn credentials not found in secrets.env"
    echo "  Add:"
    echo "  LINKEDIN_EMAIL=your-email@example.com"
    echo "  LINKEDIN_PASSWORD=your-password"
    echo "  to $SECRETS_FILE"
  fi
else
  echo "⚠ $SECRETS_FILE not found"
  echo "  Create it and add your LinkedIn credentials."
fi

echo ""
echo "Next steps:"
echo "  1. Edit $CONFIG_DIR/config.json with your identity, targets, and content"
echo "  2. Ensure your LinkedIn credentials are in $SECRETS_FILE"
echo "  3. Test with: $(dirname "$0")/engage.sh --dry-run"
echo ""
echo "🚀 LinkedIn Autopilot is ready to engage."
