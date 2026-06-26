#!/bin/bash
# Kai Skill Creator Helper Script
# Creates a new skill from template with proper structure
# Usage: ./create_skill.sh <SKILL_NAME> [--bins "bin1,bin2"] [--emoji "🎯"]

set -e

SKILL_NAME="$1"
shift || true

# Parse optional arguments
BINS=""
EMOJI="🛠️"
WORKSPACE="$HOME/.openclaw/workspace/skills"
GLOBAL="$HOME/.openclaw/skills"

while [[ $# -gt 0 ]]; do
    case $1 in
        --bins)
            BINS="$2"
            shift 2
            ;;
        --emoji)
            EMOJI="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

if [ -z "$SKILL_NAME" ]; then
    echo "Kai Skill Creator - Create new OpenClaw skills"
    echo ""
    echo "Usage: $0 <SKILL_NAME> [--bins 'bin1,bin2'] [--emoji '🎯']"
    echo ""
    echo "Example:"
    echo "  $0 my-new-skill --bins 'curl,jq' --emoji '📦'"
    echo ""
    echo "Options:"
    echo "  --bins   Comma-separated list of required binaries"
    echo "  --emoji  Emoji for the skill (default: 🛠️)"
    exit 1
fi

# Sanitize skill name (only allow alphanumeric and hyphens)
SAFE_NAME=$(echo "$SKILL_NAME" | sed 's/[^a-zA-Z0-9-]/_/g')

if [ "$SAFE_NAME" != "$SKILL_NAME" ]; then
    echo "⚠️  Skill name contained special characters. Sanitized to: $SAFE_NAME"
    SKILL_NAME="$SAFE_NAME"
fi

SKILL_DIR="$WORKSPACE/$SKILL_NAME"
GLOBAL_DIR="$GLOBAL/$SKILL_NAME"

# Check if skill already exists
if [ -d "$SKILL_DIR" ]; then
    echo "❌ Error: Skill '$SKILL_NAME' already exists at $SKILL_DIR"
    exit 1
fi

# Check if template exists
TEMPLATE_DIR="$WORKSPACE/kai-minimax-tts"
if [ ! -d "$TEMPLATE_DIR" ]; then
    echo "❌ Error: Template 'kai-minimax-tts' not found at $TEMPLATE_DIR"
    echo "Please ensure kai-minimax-tts skill is installed."
    exit 1
fi

echo "Creating skill: $SKILL_NAME"
echo "📁 Location: $SKILL_DIR"

# Copy template
cp -r "$TEMPLATE_DIR" "$SKILL_DIR"

# Rename internal references
if [ -f "$SKILL_DIR/scripts/kai_tts.sh" ]; then
    mv "$SKILL_DIR/scripts/kai_tts.sh" "$SKILL_DIR/scripts/${SKILL_NAME}.sh" 2>/dev/null || true
fi

# Create SKILL.md with proper metadata
cat > "$SKILL_DIR/SKILL.md" << EOF
---
name: $SKILL_NAME
description: TODO - Add description of what this skill does
metadata:
  openclaw:
    requires:
      bins:
$(for bin in $(echo $BINS | tr ',' ' '); do echo "        - $bin"; done)
---

# $SKILL_NAME Skill

TODO - Describe what this skill does and when to use it.

## Usage

\`\`\`bash
bash {baseDir}/scripts/${SKILL_NAME}.sh
\`\`\`

## Configuration

TODO - Add any configuration instructions
EOF

chmod +x "$SKILL_DIR/scripts/*.sh" 2>/dev/null || true

echo ""
echo "✅ Skill created at: $SKILL_DIR"
echo ""
echo "Next steps:"
echo "  1. Edit $SKILL_DIR/SKILL.md with your skill description"
echo "  2. Edit $SKILL_DIR/scripts/${SKILL_NAME}.sh with your script"
echo "  3. chmod +x $SKILL_DIR/scripts/${SKILL_NAME}.sh"
echo "  4. Copy to global: cp -r $SKILL_DIR $GLOBAL_DIR"
echo "  5. Add to config: skills.entries.$SKILL_NAME"
echo "  6. Restart gateway"
echo "  7. Publish: npx clawhub publish skills/$SKILL_NAME --slug $SKILL_NAME --version 1.0.0"
