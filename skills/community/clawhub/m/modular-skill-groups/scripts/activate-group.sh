#!/bin/bash
# activate-group.sh <group-name>
# Switches the active skill group

GROUP_FILE="$HOME/.openclaw/active_skill_group"
SKILL_GROUPS="$HOME/.openclaw/workspace/skills/modular-skill-groups/references/SKILL_GROUPS.md"

if [ -z "$1" ]; then
    echo "Usage: activate-group.sh <group-name>"
    echo ""
    echo "Available groups:"
    grep "^## GROUP:" "$SKILL_GROUPS" | sed 's/## GROUP: /  - /'
    echo ""
    echo "Current active group:"
    cat "$GROUP_FILE" 2>/dev/null || echo "  (none set)"
    exit 1
fi

TARGET="$1"
VALID=$(grep "^## GROUP:" "$SKILL_GROUPS" | sed 's/## GROUP: //')

if ! echo "$VALID" | grep -qx "$TARGET"; then
    echo "Unknown group: $TARGET"
    echo "Valid groups:"
    echo "$VALID" | sed 's/^/  /'
    exit 1
fi

echo "$TARGET" > "$GROUP_FILE"
echo "✅ Switched to group: $TARGET"
cat "$GROUP_FILE"
