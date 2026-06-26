#!/bin/bash
# Okki Go post-install initialization script
# Usage: bash scripts/post-install.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo ""
echo -e "${CYAN}🌐 Okki Go installation complete!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo -e "${GREEN}✅ Skill installed to:${NC} $SKILL_DIR"
echo ""

# Check if openclaw is available
if ! command -v openclaw &> /dev/null; then
    echo -e "${YELLOW}⚠️  OpenClaw not detected${NC}"
    echo ""
    echo "Please install OpenClaw first:"
    echo "  npm install -g openclaw"
    echo ""
    exit 0
fi

echo -e "${CYAN}📬 Would you like to enable update notifications?${NC}"
echo ""
echo "Once enabled, you will receive:"
echo "  • New version release alerts"
echo "  • Changelog previews"
echo "  • One-command update instructions"
echo ""
echo "Check frequency: Every Monday at 10:00 AM (customizable)"
echo ""

read -p "Enable? [Y/n] " confirm

if [[ "$confirm" =~ ^[Nn]$ ]]; then
    echo ""
    echo -e "${YELLOW}⏭️ Skipped${NC}"
    echo ""
    echo "You can enable it later by running:"
    echo "  bash scripts/enable-notifications.sh"
else
    echo ""
    echo "📝 Configuring..."
    bash "$SCRIPT_DIR/enable-notifications.sh"
fi

echo ""
echo -e "${CYAN}Next step: Configure your API Key${NC}"
echo ""
echo "1. Visit https://go.okki.ai to register an account"
echo "2. Create an API Key in the dashboard"
echo "3. Save it using the first method your agent supports:"
echo "   openclaw config set skills.entries.okkigo.apiKey 'sk-xxx'"
echo "   export OKKIGO_API_KEY='sk-xxx'"
echo "   ~/.config/okki-go/credentials.json with permissions 600"
echo ""
echo -e "${GREEN}🎉 All set! Start using Okki Go now!${NC}"
echo ""
