#!/bin/bash

# Proactive Daily Planner Skill Installer
# Installs the skill into OpenClaw skills directory

set -e

echo "📅 Installing Proactive Daily Planner Skill..."
echo "================================================"

# Check if OpenClaw directory exists
OPENCLAW_DIR="$HOME/.openclaw"
SKILLS_DIR="$OPENCLAW_DIR/workspace/skills"
INSTALL_DIR="$SKILLS_DIR/proactive-daily-planner"

if [ ! -d "$OPENCLAW_DIR" ]; then
    echo "❌ OpenClaw directory not found: $OPENCLAW_DIR"
    echo "Please install OpenClaw first."
    exit 1
fi

# Create skills directory if it doesn't exist
mkdir -p "$SKILLS_DIR"

# Copy skill files
echo "📁 Copying skill files..."
cp -r "$(dirname "$0")/../" "$INSTALL_DIR/"

# Make scripts executable
chmod +x "$INSTALL_DIR/planner.js"
chmod +x "$INSTALL_DIR/scripts/install.sh"

# Update configuration with user info
echo "⚙️  Configuring skill..."
USER_NAME=$(whoami)
TIMEZONE=$(timedatectl show --property=Timezone --value 2>/dev/null || echo "UTC")

# Create a default user config if config.json exists
if [ -f "$INSTALL_DIR/config.json" ]; then
    # Use jq if available, otherwise use sed
    if command -v jq >/dev/null 2>&1; then
        jq ".user.name = \"$USER_NAME\" | .user.timezone = \"$TIMEZONE\"" \
            "$INSTALL_DIR/config.json" > "$INSTALL_DIR/config.json.tmp"
        mv "$INSTALL_DIR/config.json.tmp" "$INSTALL_DIR/config.json"
    else
        echo "⚠️  jq not installed. Please manually update config.json with your name and timezone."
    fi
fi

# Create memory directory for planning data
MEMORY_DIR="$OPENCLAW_DIR/workspace/memory"
mkdir -p "$MEMORY_DIR"

# Test the skill
echo "🧪 Testing skill installation..."
cd "$INSTALL_DIR"
if node planner.js help >/dev/null 2>&1; then
    echo "✅ Skill test successful!"
else
    echo "⚠️  Skill test had issues, but installation completed."
fi

echo ""
echo "🎉 Installation Complete!"
echo "========================"
echo "Skill installed to: $INSTALL_DIR"
echo ""
echo "📋 Usage:"
echo "  cd $INSTALL_DIR"
echo "  node planner.js morning      # Create morning plan"
echo "  node planner.js progress     # Check progress"
echo "  node planner.js evening      # Evening review"
echo "  node planner.js auto         # Auto-detect based on time"
echo ""
echo "🔧 Configuration:"
echo "  Edit: $INSTALL_DIR/config.json"
echo "  Templates: $INSTALL_DIR/templates/"
echo ""
echo "📊 Planning data will be saved to:"
echo "  $MEMORY_DIR/daily-plan-YYYY-MM-DD.md"
echo ""
echo "🚀 To integrate with OpenClaw proactive system:"
echo "  Add to your HEARTBEAT.md or create a cron job"
echo ""
echo "💡 Pro tip: Set up a daily reminder:"
echo "  crontab -e"
echo "  # Add: 0 8 * * * cd $INSTALL_DIR && node planner.js morning"
echo "  # Add: 0 13 * * * cd $INSTALL_DIR && node planner.js progress"
echo "  # Add: 0 20 * * * cd $INSTALL_DIR && node planner.js evening"

echo ""
echo "✨ Happy planning! May your days be productive and fulfilling. 📅"