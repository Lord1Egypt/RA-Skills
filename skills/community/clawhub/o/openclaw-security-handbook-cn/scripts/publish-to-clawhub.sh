#!/bin/bash
# Publish openclaw-security skill to ClawHub

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== OpenClaw Security Skill Publish Script ===${NC}"
echo

# Check if we're in the right directory
if [ ! -f "SKILL.md" ]; then
    echo -e "${RED}Error: Must run from skill directory${NC}"
    echo "Usage: cd /root/.openclaw/skills/openclaw-security"
    exit 1
fi

# Check if skill is already packaged
if [ ! -f "/tmp/openclaw-security.skill" ]; then
    echo -e "${YELLOW}Skill not packaged yet. Packaging...${NC}"
    python3 /root/.local/share/pnpm/global/5/.pnpm/openclaw@2026.3.24_@napi-rs+canvas@0.1.97/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py . /tmp
fi

# Get version from package.json if exists, or use current date
if [ -f "package.json" ]; then
    VERSION=$(grep '"version"' package.json | sed 's/.*"version": "\([^"]*\)".*/\1/')
else
    VERSION="1.0.0"
fi

echo -e "${GREEN}Skill Details:${NC}"
echo "  Name: openclaw-security"
echo "  Version: ${VERSION}"
echo "  Package: /tmp/openclaw-security.skill"
echo "  Size: $(ls -lh /tmp/openclaw-security.skill | awk '{print $5}')"
echo

# Confirm before publishing
read -p "Publish openclaw-security v${VERSION} to ClawHub? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Publish cancelled.${NC}"
    exit 0
fi

echo -e "${GREEN}Publishing to ClawHub...${NC}"
echo

# Publish using clawhub CLI
clawhub publish . \
  --slug openclaw-security-handbook-cn \
  --name "OpenClaw Security Handbook (CN)" \
  --version "${VERSION}" \
  --changelog "Initial release: Comprehensive security audit and hardening tool based on ZAST.AI Security Handbook (Chinese version)" \
  --description "基于 ZAST.AI 安全手册的 OpenClaw 安全审计与加固技能。运行全面安全诊断（内置 audit + 手册补充项），生成结构化报告，提供交互式修复引导，支持定时审计调度。"

echo
echo -e "${GREEN}✅ Skill published successfully!${NC}"
echo
echo "Install with:"
echo "  clawhub install openclaw-security"
echo
echo "Or from local file:"
echo "  openclaw skill install /tmp/openclaw-security.skill"
echo
echo "Usage:"
echo "  openclaw security on"
echo "  # or mention 'security audit', 'hardening', 'vulnerability check' in conversation"
