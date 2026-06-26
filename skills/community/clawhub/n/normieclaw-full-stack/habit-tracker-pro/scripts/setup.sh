#!/usr/bin/env bash
set -euo pipefail

# Habit Tracker Pro — Setup Script
# Creates data directory and initializes default JSON files.

DATA_DIR="${HOME}/.normieclaw/habit-tracker-pro"
EXPORTS_DIR="${DATA_DIR}/exports"

echo "🦬 Habit Tracker Pro — Setup"
echo "----------------------------"

# Create directories
if [[ -d "$DATA_DIR" ]]; then
  echo "⚠️  Data directory already exists: ${DATA_DIR}"
  echo "   Skipping initialization to preserve existing data."
  echo "   Delete the directory manually if you want a fresh start."
  exit 0
fi

mkdir -p "$DATA_DIR"
mkdir -p "$EXPORTS_DIR"
echo "✅ Created data directory: ${DATA_DIR}"

# Initialize habits.json
cat > "${DATA_DIR}/habits.json" << 'EOF'
{
  "habits": [],
  "created_at": "",
  "version": "1.0.0"
}
EOF

# Stamp creation date
if command -v jq &> /dev/null; then
  NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  jq --arg now "$NOW" '.created_at = $now' "${DATA_DIR}/habits.json" > "${DATA_DIR}/habits.tmp" \
    && mv "${DATA_DIR}/habits.tmp" "${DATA_DIR}/habits.json"
fi

echo "✅ Initialized habits.json"

# Initialize completions.json
cat > "${DATA_DIR}/completions.json" << 'EOF'
{
  "completions": [],
  "version": "1.0.0"
}
EOF
echo "✅ Initialized completions.json"

# Initialize streaks.json
cat > "${DATA_DIR}/streaks.json" << 'EOF'
{
  "streaks": {},
  "version": "1.0.0"
}
EOF
echo "✅ Initialized streaks.json"

# Initialize patterns.json
cat > "${DATA_DIR}/patterns.json" << 'EOF'
{
  "patterns": {},
  "last_full_analysis": null,
  "version": "1.0.0"
}
EOF
echo "✅ Initialized patterns.json"

# Initialize stacks.json
cat > "${DATA_DIR}/stacks.json" << 'EOF'
{
  "stacks": [],
  "version": "1.0.0"
}
EOF
echo "✅ Initialized stacks.json"

# Copy default settings if config exists alongside this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_SOURCE="${SCRIPT_DIR}/../config/settings.json"

if [[ -f "$CONFIG_SOURCE" ]]; then
  cp "$CONFIG_SOURCE" "${DATA_DIR}/settings.json"
  echo "✅ Copied default settings.json"
else
  cat > "${DATA_DIR}/settings.json" << 'EOF'
{
  "checkin_schedule": {
    "morning": {"time": "08:00", "enabled": true},
    "evening": {"time": "21:00", "enabled": true}
  },
  "timezone": "America/Denver",
  "tone_level": 3,
  "weekly_report": {"enabled": true, "day": "sunday", "time": "19:00"},
  "streak_rules": {"grace_period_days": 0, "freeze_enabled": true, "count_only_scheduled_days": true}
}
EOF
  echo "✅ Created default settings.json"
fi

# Set permissions
chmod 700 "$DATA_DIR"
chmod 600 "${DATA_DIR}"/*.json
echo "✅ Set file permissions (700 dir, 600 files)"

echo ""
echo "🎯 Setup complete. Data directory: ${DATA_DIR}"
echo "   Next step: tell your agent what habits you want to track."
