#!/usr/bin/env bash
set -euo pipefail

# Language Tutor Pro — Setup Script
# Creates data directories and initializes the learner profile.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="$SKILL_DIR/data"

echo "🎓 Language Tutor Pro — Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Create data directories
echo "Creating data directories..."
mkdir -p "$DATA_DIR/conversations"

# Initialize learner profile if it doesn't exist
PROFILE="$DATA_DIR/learner-profile.json"
if [[ -f "$PROFILE" ]]; then
    echo "✅ Learner profile already exists at $PROFILE"
    echo "   Delete it and re-run this script to start fresh."
else
    # Read settings from config
    CONFIG="$SKILL_DIR/config/settings.json"
    if [[ ! -f "$CONFIG" ]]; then
        echo "❌ Config file not found at $CONFIG"
        echo "   Please ensure config/settings.json exists before running setup."
        exit 1
    fi

    # Validate config has required fields
    if ! command -v python3 &>/dev/null; then
        echo "❌ python3 is required to parse config. Please install Python 3."
        exit 1
    fi

    NATIVE=$(python3 -c "import json; print(json.load(open('$CONFIG'))['native_language'])" 2>/dev/null || echo "")
    TARGET=$(python3 -c "import json; print(json.load(open('$CONFIG'))['target_language'])" 2>/dev/null || echo "")
    LEVEL=$(python3 -c "import json; print(json.load(open('$CONFIG'))['current_level'])" 2>/dev/null || echo "")

    if [[ -z "$NATIVE" || -z "$TARGET" || -z "$LEVEL" ]]; then
        echo "❌ Config file is missing required fields."
        echo "   Ensure native_language, target_language, and current_level are set in config/settings.json"
        exit 1
    fi

    VALID_LANGUAGES="Spanish French German Italian Portuguese Japanese Mandarin Korean"
    if [[ ! " $VALID_LANGUAGES " =~ " $TARGET " ]]; then
        echo "❌ Unsupported target language: $TARGET"
        echo "   Supported: $VALID_LANGUAGES"
        exit 1
    fi

    VALID_LEVELS="A1 A2 B1 B2 C1 C2"
    if [[ ! " $VALID_LEVELS " =~ " $LEVEL " ]]; then
        echo "❌ Invalid CEFR level: $LEVEL"
        echo "   Valid levels: $VALID_LEVELS"
        exit 1
    fi

    # Read optional fields
    GOALS=$(python3 -c "import json; print(json.dumps(json.load(open('$CONFIG')).get('learning_goals', [])))" 2>/dev/null || echo "[]")
    INTERESTS=$(python3 -c "import json; print(json.dumps(json.load(open('$CONFIG')).get('interests', [])))" 2>/dev/null || echo "[]")
    DURATION=$(python3 -c "import json; print(json.load(open('$CONFIG')).get('session_duration_minutes', 20))" 2>/dev/null || echo "20")
    ERROR_MODE=$(python3 -c "import json; print(json.load(open('$CONFIG')).get('error_correction', 'inline'))" 2>/dev/null || echo "inline")
    FORMALITY=$(python3 -c "import json; print(json.load(open('$CONFIG')).get('formality', 'informal'))" 2>/dev/null || echo "informal")

    TODAY=$(date -u +"%Y-%m-%d")

    cat > "$PROFILE" <<EOF
{
  "native_language": "$NATIVE",
  "target_languages": [
    {
      "language": "$TARGET",
      "current_level": "$LEVEL",
      "started": "$TODAY",
      "goals": $GOALS,
      "focus_areas": [],
      "session_preferences": {
        "default_duration_minutes": $DURATION,
        "error_correction": "$ERROR_MODE",
        "formality": "$FORMALITY"
      }
    }
  ],
  "interests": $INTERESTS,
  "weak_spots": [],
  "total_sessions": 0,
  "current_streak_days": 0,
  "longest_streak_days": 0,
  "last_session_date": null
}
EOF

    echo "✅ Learner profile created at $PROFILE"
    echo "   Native language: $NATIVE"
    echo "   Target language: $TARGET ($LEVEL)"
fi

# Create empty data files if they don't exist
touch "$DATA_DIR/vocabulary.jsonl"
touch "$DATA_DIR/grammar.jsonl"
touch "$DATA_DIR/sessions.jsonl"

echo ""
echo "✅ Setup complete!"
echo ""
echo "📁 Data directory: $DATA_DIR"
echo "📋 Learner profile: $DATA_DIR/learner-profile.json"
echo "📚 Vocabulary: $DATA_DIR/vocabulary.jsonl"
echo "🔤 Grammar: $DATA_DIR/grammar.jsonl"
echo "📝 Sessions: $DATA_DIR/sessions.jsonl"
echo "💬 Conversations: $DATA_DIR/conversations/"
echo ""
echo "Tell your agent \"Let's practice $TARGET\" to start your first session!"
