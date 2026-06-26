#!/usr/bin/env bash
set -euo pipefail

# Meeting Scheduler Pro — Setup Script
# Validates prerequisites and initializes configuration

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_DIR="$PACKAGE_DIR/config"
NOTES_DIR="$PACKAGE_DIR/meeting-notes"

echo "========================================="
echo "  Meeting Scheduler Pro — Setup"
echo "========================================="
echo ""

# Check gog CLI
echo "Checking gog CLI..."
if ! command -v gog &>/dev/null; then
    echo "❌ gog CLI not found."
    echo "   Install it via OpenClaw or run: npm install -g gog"
    exit 1
fi
echo "✅ gog CLI found: $(command -v gog)"

# Check gog auth
echo ""
echo "Checking Google Calendar authentication..."
if gog calendar list &>/dev/null; then
    echo "✅ Google Calendar connected."
    echo ""
    echo "Available calendars:"
    gog calendar list
else
    echo "⚠️  Google Calendar not authenticated."
    echo "   Run: gog auth login"
    echo "   Then re-run this setup script."
    exit 1
fi

# Ensure config exists
echo ""
echo "Checking configuration..."
if [[ -f "$CONFIG_DIR/settings.json" ]]; then
    echo "✅ config/settings.json exists."
    echo "   Edit it to customize your availability and preferences."
else
    echo "⚠️  config/settings.json not found. Creating default..."
    mkdir -p "$CONFIG_DIR"
    cat > "$CONFIG_DIR/settings.json" << 'DEFAULTCONFIG'
{
  "availability": {
    "working_hours": {
      "start": "09:00",
      "end": "17:00",
      "timezone": "America/New_York"
    },
    "buffer_minutes": 15,
    "no_meeting_blocks": [],
    "preferred_times": {
      "external_calls": "morning",
      "internal_meetings": "afternoon"
    },
    "max_meetings_per_day": 6,
    "lunch_block": {
      "start": "12:00",
      "end": "13:00"
    }
  },
  "meeting_defaults": {
    "duration_minutes": 30,
    "video_link": "",
    "reminder_minutes": 10
  },
  "prep": {
    "auto_prep": true,
    "include_web_search": true,
    "include_email_context": true
  },
  "followup": {
    "auto_prompt": true,
    "create_tasks": true,
    "draft_email": true
  },
  "notes_directory": "meeting-notes",
  "integrations": {
    "relationship_buddy": false,
    "project_manager_pro": false
  }
}
DEFAULTCONFIG
    echo "✅ Default config created at config/settings.json"
fi

# Create notes directory
echo ""
NOTES_PATH=$(python3 -c "import json; print(json.load(open('$CONFIG_DIR/settings.json'))['notes_directory'])" 2>/dev/null || echo "meeting-notes")
NOTES_FULL="$PACKAGE_DIR/$NOTES_PATH"
if [[ ! -d "$NOTES_FULL" ]]; then
    mkdir -p "$NOTES_FULL"
    echo "✅ Created meeting notes directory: $NOTES_PATH/"
else
    echo "✅ Meeting notes directory exists: $NOTES_PATH/"
fi

# Set script permissions
echo ""
echo "Setting script permissions..."
chmod 700 "$SCRIPT_DIR/setup.sh"
chmod 700 "$SCRIPT_DIR/export-schedule.sh"
chmod 700 "$SCRIPT_DIR/weekly-agenda.sh"
echo "✅ Scripts set to chmod 700."

# Check optional integrations
echo ""
echo "Checking optional integrations..."

# Relationship Buddy
if [[ -d "$PACKAGE_DIR/../relationship-buddy" ]] || [[ -d "$HOME/.openclaw/skills/relationship-buddy" ]]; then
    echo "✅ Relationship Buddy detected — meeting prep will include contact history."
    python3 -c "
import json
f = '$CONFIG_DIR/settings.json'
c = json.load(open(f))
c['integrations']['relationship_buddy'] = True
json.dump(c, open(f, 'w'), indent=2)
" 2>/dev/null || true
else
    echo "ℹ️  Relationship Buddy not found. Install it for richer meeting prep."
fi

# Project Manager Pro
if [[ -d "$PACKAGE_DIR/../project-manager-pro" ]] || [[ -d "$HOME/.openclaw/skills/project-manager-pro" ]]; then
    echo "✅ Project Manager Pro detected — follow-up tasks will sync."
    python3 -c "
import json
f = '$CONFIG_DIR/settings.json'
c = json.load(open(f))
c['integrations']['project_manager_pro'] = True
json.dump(c, open(f, 'w'), indent=2)
" 2>/dev/null || true
else
    echo "ℹ️  Project Manager Pro not found. Install it for task management integration."
fi

echo ""
echo "========================================="
echo "  ✅ Setup Complete"
echo "========================================="
echo ""
echo "Next steps:"
echo "  1. Edit config/settings.json with your availability"
echo "     (or chat with your agent — it'll walk you through it)"
echo "  2. Try: \"What meetings do I have tomorrow?\""
echo "  3. Try: \"Schedule a call with [name] next week\""
echo ""
