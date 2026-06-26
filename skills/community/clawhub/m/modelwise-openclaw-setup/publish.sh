#!/bin/bash
# ClawHub Skill Publishing Script
# Usage: ./publish.sh

set -e

SKILL_DIR="./openclaw-setup"
SKILL_SLUG="openclaw-setup"
SKILL_NAME="OpenClaw Setup"
SKILL_VERSION="1.0.0"

echo "🦞 ClawHub Publishing Script"
echo "=============================="
echo ""

# Check if clawhub is installed
if ! command -v clawhub &> /dev/null; then
    echo "📦 Installing clawhub CLI..."
    npm i -g clawhub
fi

# Check login status
echo "🔐 Checking authentication..."
if ! clawhub whoami &> /dev/null; then
    echo "Please login first:"
    echo "  clawhub login"
    exit 1
fi

echo "✓ Authenticated as: $(clawhub whoami)"
echo ""

# Validate skill structure
echo "📋 Validating skill structure..."
if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
    echo "✗ SKILL.md not found in $SKILL_DIR"
    exit 1
fi

echo "✓ SKILL.md found"
echo ""

# Show skill info
echo "📦 Skill to publish:"
echo "  Slug: $SKILL_SLUG"
echo "  Name: $SKILL_NAME"
echo "  Version: $SKILL_VERSION"
echo "  Directory: $SKILL_DIR"
echo ""

# Ask for changelog
read -p "📝 Enter changelog (press Enter for default): " CHANGELOG
CHANGELOG=${CHANGELOG:-"Release v$SKILL_VERSION"}

echo ""
echo "🚀 Publishing to ClawHub..."

# Publish
clawhub publish "$SKILL_DIR" \
    --slug "$SKILL_SLUG" \
    --name "$SKILL_NAME" \
    --version "$SKILL_VERSION" \
    --tags latest \
    --changelog "$CHANGELOG"

echo ""
echo "✅ Published successfully!"
echo ""
echo "🔗 View at: https://clawhub.com/skills/$SKILL_SLUG"
echo ""
echo "📥 Others can install with:"
echo "  clawhub install $SKILL_SLUG"
