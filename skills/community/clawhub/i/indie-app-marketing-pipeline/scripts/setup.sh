#!/usr/bin/env bash
# setup.sh — Indie App Marketing Pipeline
#
# Run from the directory where you want to set up the pipeline:
#   bash /path/to/skills/indie-app-marketing-pipeline/scripts/setup.sh
#
# What it does:
#   1. Creates directory structure (plans/, logs/)
#   2. Copies template files (content-templates.json, sample content bank)
#   3. Prompts for env vars and writes .env + config.json
#   4. Creates posting-history.json
#   5. Creates a sample fb-brand-content-bank.json

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_DIR="${1:-$(pwd)}"

# ── Colors ──────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo ""
echo "=================================================="
echo " Indie App Marketing Pipeline — Setup"
echo "=================================================="
echo "Installing into: $TARGET_DIR"
echo ""

# ── Prompt helper ────────────────────────────────────────────────────────────
prompt() {
  local label="$1"
  local default="$2"
  local varname="$3"

  if [ -n "$default" ]; then
    printf "${CYAN}%s${NC} [%s]: " "$label" "$default"
  else
    printf "${CYAN}%s${NC}: " "$label"
  fi

  read -r input
  if [ -z "$input" ] && [ -n "$default" ]; then
    eval "$varname='$default'"
  else
    eval "$varname='$input'"
  fi
}

# ── Gather app info ──────────────────────────────────────────────────────────
echo "── App Info ───────────────────────────────────────"
prompt "App name (e.g. MyApp)"          ""          APP_NAME
prompt "Social handle (e.g. @myapp)"   "@${APP_NAME,,}" APP_HANDLE
prompt "App Store URL"                 ""          APP_STORE_URL
prompt "Website URL"                   "$APP_STORE_URL" WEBSITE_URL
prompt "Topic category (e.g. productivity, finance, health)" "productivity" TOPIC_CATEGORY
prompt "Default hashtags (space-separated)" "#${APP_NAME} #IndieApp #AppStore" DEFAULT_HASHTAGS
prompt "Default CTA"                   "${APP_NAME} — available on the App Store" DEFAULT_CTA

echo ""
echo "── Postiz Setup ────────────────────────────────────"
echo "  Get your API key from: https://app.postiz.com/settings (or your self-hosted instance)"
prompt "Postiz API URL"                "https://api.postiz.com/public/v1" POSTIZ_URL
prompt "Postiz API key"                ""          POSTIZ_KEY

echo ""
echo "  Integration IDs: in Postiz UI → Settings → Integrations → copy the ID for each platform"
echo "  Leave blank if you haven't connected that platform yet."
prompt "TikTok integration ID"         ""          TIKTOK_INTEGRATION_ID
prompt "YouTube integration ID"        ""          YOUTUBE_INTEGRATION_ID
prompt "X / Twitter integration ID"    ""          X_INTEGRATION_ID
prompt "Facebook integration ID"       ""          FB_INTEGRATION_ID

echo ""
echo "── Timezone ─────────────────────────────────────────"
prompt "Timezone offset (e.g. -05:00 for EST, -08:00 for PST, +00:00 for UTC)" "-05:00" TZ_OFFSET

# ── Create directories ────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}Creating directories...${NC}"
mkdir -p "$TARGET_DIR/plans"
mkdir -p "$TARGET_DIR/logs"
echo "  ✓ plans/"
echo "  ✓ logs/"

# ── Copy template files ───────────────────────────────────────────────────────
echo -e "${GREEN}Copying template files...${NC}"

if [ ! -f "$TARGET_DIR/content-templates.json" ]; then
  cp "$SKILL_DIR/assets/content-templates.json" "$TARGET_DIR/content-templates.json"
  echo "  ✓ content-templates.json"
else
  echo "  → content-templates.json already exists, skipping"
fi

if [ ! -f "$TARGET_DIR/content-bank.json" ]; then
  cp "$SKILL_DIR/assets/sample-content-bank.json" "$TARGET_DIR/content-bank.json"
  echo "  ✓ content-bank.json (sample — replace with your angles!)"
else
  echo "  → content-bank.json already exists, skipping"
fi

# ── Write posting-history.json ───────────────────────────────────────────────
if [ ! -f "$TARGET_DIR/posting-history.json" ]; then
  cat > "$TARGET_DIR/posting-history.json" << 'EOF'
{
  "posted": [],
  "postedFbBrand": [],
  "lastApp": null,
  "_note": "Tracks which content bank angles have been used. Do not edit manually."
}
EOF
  echo "  ✓ posting-history.json"
else
  echo "  → posting-history.json already exists, skipping"
fi

# ── Write sample fb-brand-content-bank.json ──────────────────────────────────
if [ ! -f "$TARGET_DIR/fb-brand-content-bank.json" ]; then
  cat > "$TARGET_DIR/fb-brand-content-bank.json" << FBEOF
[
  {
    "id": "fb-behind-scenes-1",
    "pattern": "behind-the-scenes",
    "content": "Building ${APP_NAME} as a solo developer means wearing every hat.\n\nThis week I fixed a bug that took 3 days to track down, redesigned the onboarding flow based on user feedback, and shipped a new feature I've been excited about for months.\n\nThe indie dev life is chaotic and exhausting and I wouldn't trade it.\n\nWhat's the hardest part of your work week? Drop it below."
  },
  {
    "id": "fb-user-story-1",
    "pattern": "user-story",
    "content": "Got a message from a user this week that made my whole month.\n\nThey said ${APP_NAME} helped them finally get on top of something they'd been struggling with for years.\n\nThat's the whole reason I build this stuff. Not the downloads, not the revenue — that message.\n\nIf you've got a moment, I'd love to hear how you're using ${APP_NAME}. Reply here or hit the feedback button in the app."
  },
  {
    "id": "fb-tip-1",
    "pattern": "tip",
    "content": "Quick tip for getting the most out of ${APP_NAME}:\n\nStart small. Most people try to do everything at once and then burn out.\n\nPick one thing. Do that one thing consistently for a week. Then add another.\n\nThe app is designed around this idea — small wins compound.\n\nWhat's one thing you're working on right now?"
  }
]
FBEOF
  echo "  ✓ fb-brand-content-bank.json (3 sample posts)"
else
  echo "  → fb-brand-content-bank.json already exists, skipping"
fi

# ── Write .env ────────────────────────────────────────────────────────────────
echo -e "${GREEN}Writing .env...${NC}"
cat > "$TARGET_DIR/.env" << ENVEOF
# Indie App Marketing Pipeline — environment variables
# Generated by setup.sh

POSTIZ_API_KEY=${POSTIZ_KEY}
ENVEOF
echo "  ✓ .env"

# ── Write config.json ─────────────────────────────────────────────────────────
echo -e "${GREEN}Writing config.json...${NC}"
cat > "$TARGET_DIR/config.json" << CONFIGEOF
{
  "app": {
    "name":             "${APP_NAME}",
    "handle":           "${APP_HANDLE}",
    "appStoreUrl":      "${APP_STORE_URL}",
    "websiteUrl":       "${WEBSITE_URL}",
    "topicCategory":    "${TOPIC_CATEGORY}",
    "defaultHashtags":  "${DEFAULT_HASHTAGS}",
    "defaultCta":       "${DEFAULT_CTA}"
  },
  "postiz": {
    "url":    "${POSTIZ_URL}",
    "apiKey": "\$POSTIZ_API_KEY",
    "integrationIds": {
      "tiktok":    "${TIKTOK_INTEGRATION_ID}",
      "youtube":   "${YOUTUBE_INTEGRATION_ID}",
      "x":         "${X_INTEGRATION_ID}",
      "facebook":  "${FB_INTEGRATION_ID}"
    }
  },
  "schedule": {
    "timezoneOffset": "${TZ_OFFSET}",
    "anglesPerDay": 3,
    "fbDays": [1, 3, 5]
  },
  "paths": {
    "plans":         "plans",
    "logs":          "logs",
    "contentBank":   "content-bank.json",
    "fbContentBank": "fb-brand-content-bank.json",
    "history":       "posting-history.json",
    "templates":     "content-templates.json"
  },
  "videoGen": {
    "script": null,
    "_note": "Set to path of your video gen script, relative to this config.json. Leave null to use --text-only mode."
  }
}
CONFIGEOF
echo "  ✓ config.json"

# ── Done ───────────────────────────────────────────────────────────────────────
echo ""
echo "=================================================="
echo -e "${GREEN} Setup complete!${NC}"
echo "=================================================="
echo ""
echo "Next steps:"
echo ""
echo "  1. Edit content-bank.json with your app's angles"
echo "     → See references/content-bank-guide.md for strategy"
echo ""
echo "  2. Run a dry-run to preview the first week:"
echo "     node scripts/weekly-planner.js --dry-run"
echo ""
echo "  3. Generate the real plan:"
echo "     node scripts/weekly-planner.js"
echo ""
echo "  4. Test the publisher:"
echo "     node scripts/daily-publisher.js --dry-run"
echo ""
echo "  5. Schedule the daily publisher at 7 AM:"
echo "     crontab -e"
echo "     # Add: 0 7 * * * cd $TARGET_DIR && node scripts/daily-publisher.js >> logs/cron.log 2>&1"
echo ""
echo -e "${YELLOW}  NOTE: content-bank.json contains sample angles.${NC}"
echo -e "${YELLOW}  Replace them with angles specific to your app.${NC}"
echo ""
