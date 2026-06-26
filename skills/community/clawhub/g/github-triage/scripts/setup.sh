#!/usr/bin/env bash
# github-triage setup: create sub-mailbox and configure email channel
# Usage: setup.sh [prefix]
#
# Requires: mail-cli with API key configured
set -euo pipefail

PREFIX="${1:-ghbot}"

# Resolve main email dynamically
MAIN_EMAIL=$(mail-cli clawemail master-user 2>/dev/null || true)
if [[ -z "$MAIN_EMAIL" ]]; then
  echo "❌ Cannot resolve master user email. Ensure mail-cli auth is configured."
  exit 1
fi

# Derive workspace prefix from current default profile
DEFAULT_USER=$(mail-cli clawemail info --json 2>/dev/null | jq -r '.email // empty' || true)
if [[ -z "$DEFAULT_USER" ]]; then
  echo "❌ Cannot detect workspace email. Ensure mail-cli auth is configured."
  exit 1
fi

SUB_EMAIL="${DEFAULT_USER%%@*}.${PREFIX}@claw.163.com"
# Normalize: if default user already has dots, the sub prefix appends after last segment
WORKSPACE_PREFIX="${DEFAULT_USER%%@*}"
SUB_EMAIL="${WORKSPACE_PREFIX}.${PREFIX}@claw.163.com"

echo "📧 GitHub Triage Setup"
echo "  Main email:  $MAIN_EMAIL"
echo "  Sub mailbox: $SUB_EMAIL"
echo ""

# Check if sub-mailbox already exists
EXISTING=$(mail-cli clawemail list --json 2>/dev/null | jq -r --arg uid "$SUB_EMAIL" '.[] | select(.email == $uid) | .email' || true)
if [[ -n "$EXISTING" ]]; then
  echo "✅ Sub-mailbox $SUB_EMAIL already exists, skipping creation."
else
  echo "🔧 Creating sub-mailbox '$PREFIX'..."
  mail-cli clawemail create --prefix "$PREFIX" --type sub --display-name "GitHub 通知助手"
  echo ""
  echo "⚠️  请保存上面显示的 auth code！仅显示一次。"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "  1. Go to GitHub → Settings → Notifications → Custom routing"
echo "  2. Set notification email to: $SUB_EMAIL"
echo "  3. Add email channel account in openclaw config for $SUB_EMAIL"
echo "  4. Verify: send a test email to $SUB_EMAIL"
