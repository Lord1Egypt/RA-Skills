#!/usr/bin/env bash
# deploy-workspace.sh — Deploy Jarvis Chief of AI Staff workspace files
# Author: Yogesh Huja (https://www.linkedin.com/in/yogeshhuja/)
# Powered by: Gignaati (https://gignaati.com)
# License: MIT

set -euo pipefail

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "============================================"
echo " Jarvis — Chief of AI Staff"
echo " Workspace Deployment"
echo " Powered by Gignaati"
echo "============================================"
echo ""

# --- Safety: confirm before overwriting ---
if [ -f "$WORKSPACE/SOUL.md" ]; then
    echo "⚠️  Existing workspace detected at: $WORKSPACE"
    echo "   A backup will be created before any changes."
    BACKUP_DIR="$WORKSPACE.backup.$TIMESTAMP"
    cp -r "$WORKSPACE" "$BACKUP_DIR"
    echo "✅ Backup created: $BACKUP_DIR"
    echo ""
fi

# --- Create directory structure ---
echo "📁 Creating workspace structure..."
mkdir -p "$WORKSPACE/memory/people"
mkdir -p "$WORKSPACE/memory/projects"
mkdir -p "$WORKSPACE/memory/topics"
mkdir -p "$WORKSPACE/memory/decisions"
echo "   ✅ Directory structure ready"

# --- Deploy core files ---
echo ""
echo "📝 Deploying Jarvis persona files..."

deploy_file() {
    local filename="$1"
    local source="$SKILL_DIR/templates/$filename"
    local dest="$WORKSPACE/$filename"

    if [ ! -f "$source" ]; then
        echo "   ⚠️  Template not found: $filename (skipping)"
        return
    fi

    if [ -f "$dest" ]; then
        echo "   🔄 Updating: $filename"
    else
        echo "   ✨ Creating: $filename"
    fi
    cp "$source" "$dest"
}

deploy_file "SOUL.md"
deploy_file "IDENTITY.md"
deploy_file "USER.md"
deploy_file "MEMORY.md"
deploy_file "AGENTS.md"
deploy_file "HEARTBEAT.md"
deploy_file "TOOLS.md"

# --- Create initial daily memory file ---
TODAY=$(date +%Y-%m-%d)
DAILY_FILE="$WORKSPACE/memory/$TODAY.md"
if [ ! -f "$DAILY_FILE" ]; then
    cat > "$DAILY_FILE" << DAILY
# $TODAY — Jarvis Deployment Day

## Events
- Jarvis Chief of AI Staff persona deployed via gignaati/jarvis-chief-of-ai-staff skill
- Workspace files created: SOUL.md, IDENTITY.md, USER.md, MEMORY.md, AGENTS.md, HEARTBEAT.md, TOOLS.md
- Memory directory structure initialized (people, projects, topics, decisions)

## System
- Hardware: $(uname -srm)
- GPU: $(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>/dev/null || echo "Not detected")
- OpenClaw: $(openclaw --version 2>/dev/null || echo "Version unknown")

## Pending
- [ ] Personalize USER.md with actual owner details
- [ ] Configure LLM backend (Ollama or LM Studio)
- [ ] Enable web search (SearXNG or Brave)
- [ ] Run security hardening script
- [ ] Test persona via WhatsApp or dashboard
- [ ] Initialize git backup for workspace
DAILY
    echo "   ✨ Creating: memory/$TODAY.md"
fi

# --- Summary ---
echo ""
echo "============================================"
echo " ✅ Deployment Complete!"
echo "============================================"
echo ""
echo " Workspace: $WORKSPACE"
echo " Files deployed: 7 core + 1 daily memory"
echo ""
echo " NEXT STEPS:"
echo " 1. Edit USER.md with your details:"
echo "    nano $WORKSPACE/USER.md"
echo ""
echo " 2. Restart OpenClaw gateway:"
echo "    sudo systemctl restart openclaw"
echo ""
echo " 3. Verify files are loaded:"
echo "    Send '/context list' to Jarvis"
echo ""
echo " 4. Run security hardening:"
echo "    bash $SKILL_DIR/scripts/security-harden.sh"
echo ""
echo " For more: https://www.invisible-enterprises.com/"
echo " By Yogesh Huja | Powered by Gignaati"
echo "============================================"
