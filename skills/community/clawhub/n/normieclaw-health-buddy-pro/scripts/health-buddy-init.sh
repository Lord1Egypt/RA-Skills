#!/bin/bash
# Health Buddy Pro — Data Directory Initializer
# Creates the required directory structure with secure permissions.
# Run from the workspace root (the directory containing your skills/ folder).

set -euo pipefail
umask 077

# --- Workspace Root Detection ---
# Look for common workspace root markers
SKILL_DIR=""
SEARCH_DIR="$(pwd)"
while [ "$SEARCH_DIR" != "/" ]; do
    # Skill directory detection (stay within skill boundary)
    SKILL_DIR="$SEARCH_DIR"
    break
  fi
  SEARCH_DIR="$(dirname "$SEARCH_DIR")"
done

if [ -z "$SKILL_DIR" ]; then
  echo "⚠️  Could not detect workspace root. Using current directory."
  SKILL_DIR="$(pwd)"
fi

SKILL_DIR="$SKILL_DIR/skills/health-buddy-pro"

if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
  echo "❌ SKILL.md not found at $SKILL_DIR/SKILL.md"
  echo "   Make sure Health Buddy Pro is installed in your skills directory."
  exit 1
fi

# Reject symlinked critical paths to prevent writes escaping the skill directory.
for path in "$SKILL_DIR" "$SKILL_DIR/config"; do
  if [ -L "$path" ]; then
    echo "❌ Refusing to use symlinked path: $path"
    exit 1
  fi
done

for path in "$SKILL_DIR/data" "$SKILL_DIR/data/weekly-summaries"; do
  if [ -e "$path" ] && [ -L "$path" ]; then
    echo "❌ Refusing to use symlinked path: $path"
    exit 1
  fi
done

echo "📁 Initializing Health Buddy Pro data directories..."
echo "   Skill directory: $SKILL_DIR"

# Create data directories
mkdir -p "$SKILL_DIR/data/weekly-summaries"

# Set directory permissions
chmod 700 "$SKILL_DIR/data"
chmod 700 "$SKILL_DIR/data/weekly-summaries"
chmod 700 "$SKILL_DIR/config"

# Initialize empty data files (only if they don't exist — never overwrite)
for f in nutrition-log.json hydration-log.json supplement-log.json activity-log.json custom-metrics.json; do
  TARGET="$SKILL_DIR/data/$f"
  if [ -L "$TARGET" ]; then
    echo "❌ Refusing to write to symlinked file: $TARGET"
    exit 1
  fi
  if [ ! -e "$TARGET" ]; then
    TMP_FILE="$(mktemp "$SKILL_DIR/data/.${f}.tmp.XXXXXX")"
    printf "[]\n" > "$TMP_FILE"
    chmod 600 "$TMP_FILE"
    mv "$TMP_FILE" "$TARGET"
    echo "   Created: data/$f"
  else
    echo "   Exists:  data/$f (skipped)"
  fi
  chmod 600 "$TARGET"
done

# Secure config file
if [ -L "$SKILL_DIR/config/health-config.json" ]; then
  echo "❌ Refusing to chmod symlinked config file: $SKILL_DIR/config/health-config.json"
  exit 1
fi
chmod 600 "$SKILL_DIR/config/health-config.json"

echo ""
echo "✅ Health Buddy Pro initialized successfully!"
echo "   Data directory: $SKILL_DIR/data/"
echo "   Config:         $SKILL_DIR/config/health-config.json"
echo ""
echo "   Tell your agent: \"Let's set up Health Buddy Pro\" to begin onboarding."
