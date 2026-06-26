#!/usr/bin/env bash
# setup.sh — Initialize Party Planner Pro data directories and template files
# Usage: bash scripts/setup.sh
# Run from the party-planner-pro skill directory or any parent workspace directory.

set -euo pipefail
umask 077

# --- Workspace root detection ---
find_skill_dir() {
    local dir="$PWD"
    # Check if we're inside the skill directory
    if [ -f "$dir/SKILL.md" ] && grep -q "Party Planner Pro" "$dir/SKILL.md" 2>/dev/null; then
        echo "$dir"
        return 0
    fi
    # Check for skill in skills/ subdirectory
    if [ -d "$dir/skills/party-planner-pro" ]; then
        echo "$dir/skills/party-planner-pro"
        return 0
    fi
    # Walk up looking for workspace root, then check skills/ there
    while [ "$dir" != "/" ]; do
        if [ -f "$dir/AGENTS.md" ] || [ -f "$dir/SOUL.md" ]; then
            if [ -d "$dir/skills/party-planner-pro" ]; then
                echo "$dir/skills/party-planner-pro"
                return 0
            fi
            break
        fi
        dir="$(dirname "$dir")"
    done
    # Fallback: script's own parent directory
    echo "$(cd "$(dirname "$0")/.." && pwd)"
    return 0
}

SKILL_DIR="$(find_skill_dir)"
DATA_DIR="$SKILL_DIR/data"

echo "🎉 Party Planner Pro — Setup"
echo "Skill directory: $SKILL_DIR"
echo ""

# --- Create data directories ---
echo "Creating data directories..."
mkdir -p "$DATA_DIR/events"
mkdir -p "$DATA_DIR/templates"

# --- Set directory permissions ---
echo "Setting permissions..."
chmod 700 "$DATA_DIR"
chmod 700 "$DATA_DIR/events"
chmod 700 "$DATA_DIR/templates"

# --- Create default template files ---
if [ ! -f "$DATA_DIR/templates/birthday-template.json" ]; then
    cat > "$DATA_DIR/templates/birthday-template.json" << 'TMPL'
{
  "template_name": "Birthday Party",
  "type": "birthday",
  "default_formality": "casual",
  "suggested_themes": [
    "Classic Celebration",
    "Decade Theme (pick your era)",
    "Favorite Color Explosion",
    "Garden Party",
    "Game Night Bash"
  ],
  "default_budget_split": "birthday",
  "default_courses": ["appetizers", "main", "sides", "cake", "drinks"],
  "typical_duration_hours": 4,
  "notes": "Customize for milestone birthdays (21, 30, 40, 50) with extra flair"
}
TMPL
    chmod 600 "$DATA_DIR/templates/birthday-template.json"
fi

if [ ! -f "$DATA_DIR/templates/dinner-party-template.json" ]; then
    cat > "$DATA_DIR/templates/dinner-party-template.json" << 'TMPL'
{
  "template_name": "Dinner Party",
  "type": "dinner_party",
  "default_formality": "semi-formal",
  "suggested_themes": [
    "Italian Night",
    "Wine & Cheese Tasting",
    "Farm-to-Table",
    "Tapas & Cocktails",
    "Seasonal Harvest"
  ],
  "default_budget_split": "dinner_party",
  "default_courses": ["appetizers", "salad", "main", "sides", "dessert", "drinks"],
  "typical_duration_hours": 3,
  "notes": "Focus budget on food quality over decorations"
}
TMPL
    chmod 600 "$DATA_DIR/templates/dinner-party-template.json"
fi

# --- Verify setup ---
echo ""
echo "--- Verification ---"
test -d "$DATA_DIR/events" && echo "✅ data/events/" || echo "❌ data/events/ MISSING"
test -d "$DATA_DIR/templates" && echo "✅ data/templates/" || echo "❌ data/templates/ MISSING"
test -f "$DATA_DIR/templates/birthday-template.json" && echo "✅ birthday template" || echo "❌ birthday template MISSING"
test -f "$DATA_DIR/templates/dinner-party-template.json" && echo "✅ dinner party template" || echo "❌ dinner party template MISSING"
test -f "$SKILL_DIR/config/settings.json" && echo "✅ config/settings.json" || echo "⚠️  config/settings.json not found (copy from package)"

echo ""
echo "✅ Party Planner Pro data directories initialized!"
echo "Start planning: 'Help me plan a party' or 'I'm hosting a birthday for 30 people.'"
