# Health Buddy Pro — Setup Prompt

Copy and paste this entire message to your AI agent to install Health Buddy Pro.

---

**SETUP INSTRUCTIONS — Please follow these steps exactly:**

## Step 1: Copy Skill Files

Locate the Health Buddy Pro skill files and copy them to your workspace skills directory:

```bash
set -euo pipefail

# Find and copy the skill directory to your workspace
# Files are installed by clawhub install — no manual copy needed

if [ -z "$SKILL_SRC" ]; then
  echo "❌ Could not find Health Buddy Pro skill files. Make sure they're extracted somewhere in the current directory tree."
  exit 1
fi

# Basic source validation (avoid copying an unexpected directory)
if [ "$(basename "$SKILL_SRC")" != "health-buddy-pro" ] || [ -L "$SKILL_SRC" ] || [ ! -f "$SKILL_SRC/config/health-config.json" ]; then
  echo "❌ Found an invalid skill source directory: $SKILL_SRC"
  exit 1
fi

# Create destination in your workspace skills directory
mkdir -p skills/health-buddy-pro
cp -RP "$SKILL_SRC"/. skills/health-buddy-pro/
echo "✅ Skill files copied to skills/health-buddy-pro/"
```

## Step 2: Initialize Data Directories

```bash
set -euo pipefail
umask 077

# Create data directories with secure permissions
if [ -e "skills/health-buddy-pro/data" ] && [ -L "skills/health-buddy-pro/data" ]; then
  echo "❌ Refusing to initialize symlinked path: skills/health-buddy-pro/data"
  exit 1
fi
if [ -e "skills/health-buddy-pro/config" ] && [ -L "skills/health-buddy-pro/config" ]; then
  echo "❌ Refusing to initialize symlinked path: skills/health-buddy-pro/config"
  exit 1
fi
mkdir -p skills/health-buddy-pro/data/weekly-summaries
chmod 700 skills/health-buddy-pro/data
chmod 700 skills/health-buddy-pro/data/weekly-summaries

# Set secure permissions on config
chmod 700 skills/health-buddy-pro/config
if [ -L "skills/health-buddy-pro/config/health-config.json" ]; then
  echo "❌ Refusing to chmod symlinked file: skills/health-buddy-pro/config/health-config.json"
  exit 1
fi
chmod 600 skills/health-buddy-pro/config/health-config.json

# Initialize empty data files
for f in nutrition-log.json hydration-log.json supplement-log.json activity-log.json custom-metrics.json; do
  TARGET="skills/health-buddy-pro/data/$f"
  if [ -L "$TARGET" ]; then
    echo "❌ Refusing to write symlinked file: $TARGET"
    exit 1
  fi
  if [ ! -e "$TARGET" ]; then
    TMP=$(mktemp "skills/health-buddy-pro/data/.${f}.tmp.XXXXXX")
    printf "[]\n" > "$TMP"
    mv "$TMP" "$TARGET"
  fi
  chmod 600 "skills/health-buddy-pro/data/$f"
done

echo "✅ Data directories initialized with secure permissions"
```

## Step 3: Set Script Permissions (if applicable)

```bash
set -euo pipefail

if [ -d "skills/health-buddy-pro/scripts" ]; then
  chmod 700 skills/health-buddy-pro/scripts
  find skills/health-buddy-pro/scripts -maxdepth 1 -type f -name "*.sh" -exec chmod 700 {} \;
  echo "✅ Script permissions set"
fi
```

## Step 4: Verify Installation

```bash
set -euo pipefail

echo "=== Health Buddy Pro Installation Check ==="

# Check SKILL.md exists
[ -f "skills/health-buddy-pro/SKILL.md" ] && echo "✅ SKILL.md" || echo "❌ SKILL.md missing"

# Check config
[ -f "skills/health-buddy-pro/config/health-config.json" ] && echo "✅ health-config.json" || echo "❌ health-config.json missing"

# Check data files
for f in nutrition-log.json hydration-log.json supplement-log.json activity-log.json custom-metrics.json; do
  [ -f "skills/health-buddy-pro/data/$f" ] && echo "✅ data/$f" || echo "❌ data/$f missing"
done

# Check data directory permissions
PERMS=$(stat -f "%Lp" skills/health-buddy-pro/data 2>/dev/null || stat -c "%a" skills/health-buddy-pro/data 2>/dev/null)
[ "$PERMS" = "700" ] && echo "✅ Data directory permissions (700)" || echo "⚠️ Data directory permissions: $PERMS (expected 700)"

echo ""
echo "=== Installation Complete ==="
echo "Now send me a food photo to get started! 📸🍕"
```

## Step 5: First Run

After installation, say: **"Let's set up Health Buddy Pro"**

Your agent will:
1. Display the medical disclaimer
2. Walk you through the Goal Setting Wizard (4-5 quick questions)
3. Save your personalized config
4. Ask you to snap a photo of food for the "wow moment"

**You're all set!** 🎉

---

## Troubleshooting

- **"File not found" errors:** Make sure you extracted the skill files before running the setup. The `find` command looks for them in the current directory tree.
- **Permission denied:** Run the chmod commands in Step 2 again.
- **Data files empty:** That's expected! They start as empty JSON arrays `[]` and fill up as you use the skill.
- **Agent doesn't recognize the skill:** Make sure SKILL.md is in your agent's skills directory and restart your agent session.
