#!/bin/bash
# Test version of publish.sh - does everything except push/publish

set -e

BUMP_TYPE=${1:-patch}

echo "════════════════════════════════════════════════════════════════"
echo "  Molt Motion Skill Release Pipeline (DRY RUN)"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Change to skill directory
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$SKILL_DIR"

# Show current version
echo "📦 Current version:"
CURRENT_VERSION=$(node -p "require('./package.json').version")
echo "   v$CURRENT_VERSION"
echo ""

# Test version bump (without modifying package.json)
echo "⬆️  Would bump $BUMP_TYPE version..."
NEW_VERSION=$(node -p "const semver = require('./package.json').version.split('.').map(Number); const [major, minor, patch] = semver; const type = '$BUMP_TYPE'; type === 'major' ? [major+1,0,0].join('.') : type === 'minor' ? [major,minor+1,0].join('.') : [major,minor,patch+1].join('.')")
echo "   New version would be: v$NEW_VERSION"
echo ""

# Test Git operations (without actually executing)
echo "📝 Would commit version bump:"
echo "   git add package.json"
echo "   git commit -m 'chore(skill): bump version to v$NEW_VERSION'"
echo ""

echo "🏷️  Would create Git tag:"
echo "   git tag -a 'moltmotion-skill-v$NEW_VERSION' -m 'Release moltmotion-skill v$NEW_VERSION'"
echo ""

echo "⬆️  Would push to GitHub:"
echo "   git push origin main"
echo "   git push origin 'moltmotion-skill-v$NEW_VERSION'"
echo ""

# Check GitHub CLI
echo "📦 Would create GitHub release:"
if command -v gh &> /dev/null; then
  echo "   ✓ gh CLI is installed"
  echo "   Would run: gh release create moltmotion-skill-v$NEW_VERSION ..."
else
  echo "   ⚠️  gh CLI not installed - would skip GitHub release"
  echo "   Install: brew install gh"
fi
echo ""

# Check ClawHub
echo "📤 Would publish to ClawHub:"
if command -v npx &> /dev/null; then
  echo "   ✓ npx is available"
  echo "   Would run: npx clawhub@latest publish \"$SKILL_DIR\" --slug molt-motion --name \"Molt Motion\" --version $NEW_VERSION"
else
  echo "   ⚠️  npx not found - would fail"
fi
echo ""

echo "════════════════════════════════════════════════════════════════"
echo "  ✅ Dry Run Complete! (No changes made)"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "To run for real:"
echo "   npm run publish-skill"
echo ""
echo "Prerequisites:"
if ! command -v gh &> /dev/null; then
  echo "   ⚠️  Install GitHub CLI: brew install gh"
else
  echo "   ✓ GitHub CLI installed"
fi

if ! command -v npx &> /dev/null; then
  echo "   ⚠️  Install npm/npx"
else
  echo "   ✓ npx available"
fi

echo ""
echo "📥 Users would install with:"
echo ""
echo "1️⃣  GitHub (Canonical Source):"
echo "   npx @anthropic-ai/claude-cli skills install molt-motion \\"
echo "     --github chefbc2k/MOLTSTUDIOS \\"
echo "     --path moltmotion-skill"
echo ""
echo "2️⃣  ClawHub Registry:"
echo "   npx clawhub install molt-motion --registry https://clawhub.ai"
echo ""
echo "3️⃣  skills.sh (Vercel):"
echo "   https://skills.sh/s/chefbc2k/molt-motion"
echo ""
