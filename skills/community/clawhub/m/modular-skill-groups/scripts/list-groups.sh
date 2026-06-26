#!/bin/bash
# list-groups.sh
# Shows all skill groups, their skills, and the currently active one

GROUP_FILE="$HOME/.openclaw/active_skill_group"
SKILL_GROUPS="$HOME/.openclaw/workspace/skills/modular-skill-groups/references/SKILL_GROUPS.md"

ACTIVE=$(cat "$GROUP_FILE" 2>/dev/null || echo "minimal")

echo "═══════════════════════════════════════"
echo "  SKILL GROUPS"
echo "═══════════════════════════════════════"
echo ""

CURRENT=""
while IFS= read -r line; do
    if [[ "$line" =~ ^##\ GROUP:\ *(.*) ]]; then
        if [ -n "$CURRENT" ]; then
            echo "───────────────────────────────────────"
        fi
        NAME="${BASH_REMATCH[1]}"
        if [ "$NAME" = "$ACTIVE" ]; then
            echo "▶ $NAME (ACTIVE)"
        else
            echo "  $NAME"
        fi
        echo ""
        CURRENT="$NAME"
    elif [[ "$line" =~ ^-\  ]] && [ -n "$CURRENT" ]; then
        echo "    $line"
    fi
done < "$SKILL_GROUPS"

echo "───────────────────────────────────────"
echo ""
echo "CORE (always loaded): self-improving, proactivity, sub-agent-orchestrator, research-assistant, elite-longterm-memory, qdrant-memory"
