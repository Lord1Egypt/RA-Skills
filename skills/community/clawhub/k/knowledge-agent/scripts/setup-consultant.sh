#!/bin/bash
# Create workspace directory structure for a knowledge consultant Agent
#
# Usage:
#   ./setup-consultant.sh <agentId> <domain> [workspace-base]
#
# Example:
#   ./setup-consultant.sh douyin-consultant "Douyin Operations"
#   ./setup-consultant.sh legal-advisor "Legal Consulting" /custom/path
#
# Creates:
#   <workspace>/
#   ├── AGENTS.md      (from template, with placeholders replaced)
#   ├── SOUL.md        (from template)
#   ├── IDENTITY.md    (from template)
#   ├── MEMORY.md      (from template)
#   ├── TOOLS.md       (basic tool notes)
#   └── knowledge/     (empty directory for reference materials)

set -e

if [ $# -lt 2 ]; then
  echo "Usage: ./setup-consultant.sh <agentId> <domain> [workspace-base]"
  echo ""
  echo "Arguments:"
  echo "  agentId       — Agent identifier (e.g., douyin-consultant)"
  echo "  domain        — Domain description (e.g., 'Douyin Operations')"
  echo "  workspace-base — Base directory (default: ~/.openclaw)"
  echo ""
  echo "Example:"
  echo "  ./setup-consultant.sh douyin-consultant 'Douyin Operations'"
  exit 1
fi

AGENT_ID="$1"
DOMAIN="$2"
BASE="${3:-$HOME/.openclaw}"
WORKSPACE="$BASE/workspace-$AGENT_ID"
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TEMPLATE_DIR="$SCRIPT_DIR/templates"

echo "Creating workspace for Agent: $AGENT_ID"
echo "Domain: $DOMAIN"
echo "Workspace: $WORKSPACE"
echo ""

# Create directory structure
mkdir -p "$WORKSPACE/knowledge"
echo "[OK] Created workspace directory"

# Copy and fill templates
for tmpl in AGENTS SOUL IDENTITY MEMORY; do
  SRC="$TEMPLATE_DIR/${tmpl}.template.md"
  DST="$WORKSPACE/${tmpl}.md"

  if [ -f "$SRC" ]; then
    sed \
      -e "s/{{AGENT_ID}}/$AGENT_ID/g" \
      -e "s/{{AGENT_NAME}}/$AGENT_ID/g" \
      -e "s/{{DOMAIN}}/$DOMAIN/g" \
      -e "s|{{WORKSPACE_PATH}}|$WORKSPACE|g" \
      -e "s/{{DISPLAY_NAME}}/$DOMAIN Consultant/g" \
      -e "s/{{PUBLIC_TITLE}}/$DOMAIN Expert Consultant/g" \
      -e "s/{{DOMAIN_DESCRIPTION}}/$DOMAIN consulting and guidance/g" \
      "$SRC" > "$DST"
    echo "[OK] Created $tmpl.md"
  else
    echo "[!!] Template not found: $SRC"
  fi
done

# Create basic TOOLS.md
cat > "$WORKSPACE/TOOLS.md" << 'TOOLSEOF'
# TOOLS.md

## Important Notes
- Do NOT read AGENTS.md — it is already auto-injected into your context
- All tool calls must include required parameters
- Use `web_fetch` for search: web_fetch({"url": "https://www.google.com/search?q=QUERY"})
TOOLSEOF
echo "[OK] Created TOOLS.md"

echo ""
echo "========================================="
echo "Workspace created at: $WORKSPACE"
echo ""
echo "Next steps:"
echo "  1. Edit $WORKSPACE/AGENTS.md — fill in domain knowledge"
echo "  2. Edit $WORKSPACE/SOUL.md — customize personality"
echo "  3. Edit $WORKSPACE/IDENTITY.md — set display name and emoji"
echo "  4. Add reference documents to $WORKSPACE/knowledge/"
echo "  5. Register the agent: openclaw agents add $AGENT_ID"
echo "  6. Configure Feishu delivery in openclaw.json"
echo "  7. Restart gateway: openclaw gateway restart"
echo "========================================="
