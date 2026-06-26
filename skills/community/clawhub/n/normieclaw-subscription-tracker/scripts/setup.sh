#!/usr/bin/env bash
set -euo pipefail

# Subscription Tracker — Setup Script
# Creates directory structure and initializes default config

ST_DIR="$HOME/.normieclaw/subscription-tracker"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_DIR="$(dirname "$SCRIPT_DIR")"

echo "🔧 Setting up Subscription Tracker..."
echo ""

# Create directory structure
mkdir -p "$ST_DIR"/{statements,exports,logs,scripts}
echo "  ✅ Created directory: $ST_DIR"
echo "  ✅ Created subdirectories: statements, exports, logs, scripts"

# Initialize subscriptions database if it doesn't exist
if [[ ! -f "$ST_DIR/subscriptions.json" ]]; then
  cat > "$ST_DIR/subscriptions.json" << 'DBEOF'
{
  "version": "1.0.0",
  "last_updated": null,
  "subscriptions": [],
  "trials": [],
  "cancelled": [],
  "settings": {
    "alert_days_before": [3, 7],
    "monthly_summary_day": 1,
    "annual_audit_month": 1,
    "currency": "USD"
  }
}
DBEOF
  echo "  ✅ Initialized subscriptions database"
else
  echo "  ⏭️  Subscriptions database already exists — skipping"
fi

# Copy config if not present
if [[ ! -f "$ST_DIR/config/settings.json" ]]; then
  mkdir -p "$ST_DIR/config"
  if [[ -f "$PACKAGE_DIR/config/settings.json" ]]; then
    cp "$PACKAGE_DIR/config/settings.json" "$ST_DIR/config/settings.json"
    echo "  ✅ Copied default settings"
  else
    echo "  ⚠️  No default settings.json found in package — create manually"
  fi
else
  echo "  ⏭️  Settings already exist — skipping"
fi

# Copy scripts
for script in export-subs.sh renewal-check.sh; do
  if [[ -f "$PACKAGE_DIR/scripts/$script" ]]; then
    cp "$PACKAGE_DIR/scripts/$script" "$ST_DIR/scripts/$script"
    chmod 700 "$ST_DIR/scripts/$script"
    echo "  ✅ Installed script: $script"
  fi
done

# Set permissions
chmod 700 "$ST_DIR"
chmod 600 "$ST_DIR/subscriptions.json"
find "$ST_DIR/scripts" -name "*.sh" -exec chmod 700 {} \; 2>/dev/null || true
echo "  ✅ Set directory permissions (700) and database permissions (600)"

echo ""
echo "📂 Installation directory: $ST_DIR"
echo ""
echo "✅ Setup complete! Next steps:"
echo "   1. Tell your agent about your alert preferences"
echo "   2. Drop a bank/credit card statement (CSV preferred)"
echo "   3. Say 'scan my statement' to find your subscriptions"
echo ""
