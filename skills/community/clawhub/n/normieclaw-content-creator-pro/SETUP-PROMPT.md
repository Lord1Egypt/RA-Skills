# Content Creator Pro — First-Run Setup

Welcome to **Content Creator Pro**! Let's get you set up in under 2 minutes.

---

## Step 1: Create Your Data Directories

Run these commands to create the data structure with proper permissions:

```bash
# Create data directories (chmod 700 — owner only)
mkdir -p data/content-calendar config scripts
chmod 700 data data/content-calendar
```

## Step 2: Copy Config & Scripts from Skill Package

```bash
# Find the skill package directory
SKILL_DIR=$(find "$HOME" -path "*/skills/content-creator-pro/config/content-config.json" -type f 2>/dev/null | head -1 | sed 's|/config/content-config.json||')

if [ -z "$SKILL_DIR" ]; then
  echo "⚠️ Could not find Content Creator Pro skill package."
  echo "Set SKILL_DIR manually to the content-creator-pro directory path, then re-run Step 2."
else
  cp "$SKILL_DIR/config/content-config.json" config/content-config.json
  chmod 600 config/content-config.json

  cp "$SKILL_DIR/scripts/export-calendar.sh" scripts/export-calendar.sh
  chmod 700 scripts/export-calendar.sh
  echo "✅ Config and scripts copied from $SKILL_DIR"
fi
```

## Step 3: Initialize Empty Data Files

```bash
# Initialize data files with empty/default content (chmod 600 — sensitive)
echo '{}' > data/brand-profile.json
echo '[]' > data/content-pillars.json
echo '[]' > data/voice-learnings.json
echo '[]' > data/idea-bank.json
echo '[]' > data/content-history.json
echo '[]' > data/engagement-log.json
echo '{}' > data/pillar-tracking.json
echo '[]' > data/competitor-notes.json

# Lock down sensitive files
chmod 600 data/*.json
```

## Step 4: Verify Installation

```bash
echo "=== Content Creator Pro — Installation Check ==="
echo ""

# Check directories
for dir in data data/content-calendar config scripts; do
  if [ -d "$dir" ]; then
    echo "✅ Directory: $dir"
  else
    echo "❌ Missing directory: $dir"
  fi
done

# Check files
for file in config/content-config.json scripts/export-calendar.sh; do
  if [ -f "$file" ]; then
    echo "✅ File: $file"
  else
    echo "❌ Missing file: $file"
  fi
done

# Check data files
for file in brand-profile.json content-pillars.json idea-bank.json content-history.json engagement-log.json; do
  if [ -f "data/$file" ]; then
    echo "✅ Data: $file"
  else
    echo "❌ Missing data: $file"
  fi
done

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "Next step: Tell me about your brand! Say something like:"
echo '  "I run a SaaS company that helps remote teams collaborate."'
echo ""
echo "I'll ask you 2 more quick questions, then generate your content pillars."
echo "Time to first content: under 3 minutes. 🚀"
```

---

## What Happens Next

After setup, the agent will:

1. **Start the Brand Interview** — 3 simple questions about your business, audience, and voice.
2. **Generate Content Pillars** — 4 recurring themes for your content, based on your answers.
3. **You're ready to create** — Drop an idea, ask for a calendar, or upload a photo. Content Creator Pro takes it from there.

---

## File Structure After Setup

```
data/
  brand-profile.json         — Your brand identity (populated during interview)
  content-pillars.json       — Your content themes
  voice-learnings.json       — Voice refinement history
  idea-bank.json             — Saved content ideas
  content-history.json       — What you've posted
  engagement-log.json        — Performance metrics
  pillar-tracking.json       — Pillar distribution balance
  competitor-notes.json      — Competitive insights
  content-calendar/
    YYYY-MM-DD.json          — Weekly content calendars
config/
  content-config.json        — Platform settings, schedules, defaults
scripts/
  export-calendar.sh         — Export calendars to CSV/markdown
```
