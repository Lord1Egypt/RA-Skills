#!/bin/bash
# MoltCare-Open Installation Script

set -e

WORKSPACE="${HOME}/.openclaw/workspace"
MEMORY_DIR="${WORKSPACE}/memory"

echo "🦞 Installing MoltCare-Open Framework..."
echo ""
echo "⚠️  IMPORTANT: Files will be installed to:"
echo "   ${WORKSPACE}/"
echo "   (NOT in any subfolder like core/ or assets/)"
echo ""

# Create directories
mkdir -p "${WORKSPACE}"
mkdir -p "${MEMORY_DIR}"

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ASSETS_DIR="${SCRIPT_DIR}/../assets"

# Copy CORE templates (loaded by OpenClaw automatically)
echo "📄 Copying CORE templates (auto-loaded by OpenClaw)..."
cp "${ASSETS_DIR}/AGENTS.md" "${WORKSPACE}/"
cp "${ASSETS_DIR}/SOUL.md" "${WORKSPACE}/"
cp "${ASSETS_DIR}/USER.md" "${WORKSPACE}/"
cp "${ASSETS_DIR}/MEMORY.md" "${WORKSPACE}/"

# Copy OPTIONAL templates (loaded if exists)
echo "📄 Copying OPTIONAL templates..."
cp "${ASSETS_DIR}/IDENTITY.md" "${WORKSPACE}/"
cp "${ASSETS_DIR}/TOOLS.md" "${WORKSPACE}/"
cp "${ASSETS_DIR}/HEARTBEAT.md" "${WORKSPACE}/"
cp "${ASSETS_DIR}/TOKEN_AUDIT.md" "${WORKSPACE}/"
cp "${ASSETS_DIR}/CONFIG_CHECKLIST.md" "${WORKSPACE}/"

# Copy MEMORY templates (not auto-loaded, read on-demand)
echo "📝 Copying MEMORY templates (read on-demand)..."
cp "${ASSETS_DIR}/learning-debt.md" "${MEMORY_DIR}/"
cp "${ASSETS_DIR}/constraints.md" "${MEMORY_DIR}/"
cp "${ASSETS_DIR}/preferences.md" "${MEMORY_DIR}/"
cp "${ASSETS_DIR}/token-audit-template.md" "${MEMORY_DIR}/"

# Create today's memory file
TODAY=$(date +%Y-%m-%d)
if [ ! -f "${MEMORY_DIR}/${TODAY}.md" ]; then
    echo "📅 Creating today's memory file..."
    echo "# ${TODAY} Memory Flush" > "${MEMORY_DIR}/${TODAY}.md"
fi

# Configure weekly token audit cron (optional)
echo ""
echo "⏰ Configuring weekly token audit (optional)..."
if ! crontab -l 2>/dev/null | grep -q "检查token优化"; then
    (crontab -l 2>/dev/null; echo "0 3 * * 1 cd ${WORKSPACE} && echo '检查token优化' >> ${WORKSPACE}/.audit-trigger 2>&1") | crontab -
    echo "  ✅ Weekly token audit configured (Mondays 03:00)"
    echo "     Cron: 0 3 * * 1 (每周一凌晨3点)"
else
    echo "  ⏭️  Token audit already configured, skipping"
fi

echo ""
echo "✅ MoltCare-Open installed successfully!"
echo ""
echo "📁 CORE files (auto-loaded by OpenClaw):"
echo "   ${WORKSPACE}/AGENTS.md    - Operation manual"
echo "   ${WORKSPACE}/SOUL.md      - Agent principles"
echo "   ${WORKSPACE}/USER.md      - User profile"
echo "   ${WORKSPACE}/MEMORY.md    - Long-term memory"
echo ""
echo "📁 OPTIONAL files (loaded if exists):"
echo "   ${WORKSPACE}/IDENTITY.md          - Agent identity"
echo "   ${WORKSPACE}/TOOLS.md             - Environment tools"
echo "   ${WORKSPACE}/HEARTBEAT.md         - Health check system"
echo "   ${WORKSPACE}/TOKEN_AUDIT.md       - Weekly token audit config"
echo "   ${WORKSPACE}/CONFIG_CHECKLIST.md  - Post-install verification"
echo ""
echo "⚠️  IMPORTANT: After installation, read CONFIG_CHECKLIST.md:"
echo "   cat ${WORKSPACE}/CONFIG_CHECKLIST.md"
echo ""
echo "📁 MEMORY templates (read on-demand):"
echo "   ${MEMORY_DIR}/learning-debt.md"
echo "   ${MEMORY_DIR}/constraints.md"
echo "   ${MEMORY_DIR}/preferences.md"
echo "   ${MEMORY_DIR}/token-audit-template.md"
echo ""
echo "⏰ Automated tasks:"
echo "   Weekly token audit: Mondays 03:00 (cron)"
echo ""
echo "📖 Reference docs (in skill/assets/, not auto-loaded):"
echo "   BEST_PRACTICES.md - Efficiency guide (read when needed)"
echo ""
echo "Next steps:"
echo "1. Edit ${WORKSPACE}/USER.md to configure your profile"
echo "2. Edit ${WORKSPACE}/MEMORY.md to add high-signal memories"
echo "3. Weekly token audit runs automatically (Mondays 03:00)"
echo "   Or trigger manually: say \"检查token优化\""
