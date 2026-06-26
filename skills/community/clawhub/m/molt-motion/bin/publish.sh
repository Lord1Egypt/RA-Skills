#!/bin/bash
set -e

# Default to patch version bump if no argument provided
BUMP_TYPE=${1:-patch}

echo "════════════════════════════════════════════════════════════════"
echo "  Molt Motion Skill Release Pipeline"
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

# Bump version
echo "⬆️  Bumping $BUMP_TYPE version..."
npm version $BUMP_TYPE --no-git-tag-version

# Extract new version
NEW_VERSION=$(node -p "require('./package.json').version")
echo "   New version: v$NEW_VERSION"
echo ""

# Commit version bump
echo "📝 Committing version bump..."
git add package.json
git commit -m "chore(skill): bump version to v$NEW_VERSION" || echo "   (No changes to commit)"
echo ""

# Create and push Git tag
echo "🏷️  Creating Git tag..."
git tag -a "moltmotion-skill-v$NEW_VERSION" -m "Release moltmotion-skill v$NEW_VERSION"
echo "   Tag: moltmotion-skill-v$NEW_VERSION"
echo ""

echo "⬆️  Pushing to GitHub..."
git push origin main
git push origin "moltmotion-skill-v$NEW_VERSION"
echo "   ✓ Pushed commit and tag"
echo ""

# Create GitHub release
echo "📦 Creating GitHub release..."
if command -v gh &> /dev/null; then
  gh release create "moltmotion-skill-v$NEW_VERSION" \
    --title "Molt Motion Skill v$NEW_VERSION" \
    --notes "## Installation

### Option 1: Direct from GitHub (Recommended)
\`\`\`bash
npx @anthropic-ai/claude-cli skills install molt-motion \\
  --github chefbc2k/MOLTSTUDIOS \\
  --path moltmotion-skill
\`\`\`

### Option 2: Via ClawHub
\`\`\`bash
npx clawhub install molt-motion --registry https://clawhub.ai
\`\`\`

### Option 3: Via skills.sh (Vercel)
Visit [skills.sh/s/chefbc2k/molt-motion](https://skills.sh/s/chefbc2k/molt-motion) for installation instructions.

## What's Changed
See commit history for detailed changes in this release.

## Documentation
- [SKILL.md](https://github.com/chefbc2k/MOLTSTUDIOS/blob/main/moltmotion-skill/SKILL.md)
- [Platform API](https://github.com/chefbc2k/MOLTSTUDIOS/blob/main/moltmotion-skill/PLATFORM_API.md)
" \
    --repo chefbc2k/MOLTSTUDIOS
  echo "   ✓ GitHub release created"
else
  echo "   ⚠️  gh CLI not installed, skipping GitHub release"
  echo "   Install gh CLI: https://cli.github.com/"
fi
echo ""

# Publishing to ClawHub
echo "📤 Publishing to ClawHub..."
PUBLISH_ERR_FILE="$(mktemp)"
if npx clawhub@latest publish "$SKILL_DIR" --slug molt-motion --name "Molt Motion" --version "$NEW_VERSION" 2>"$PUBLISH_ERR_FILE"; then
  echo "   ✓ Published to ClawHub registry (CLI)"
else
  PUBLISH_ERR_MSG="$(cat "$PUBLISH_ERR_FILE")"
  if echo "$PUBLISH_ERR_MSG" | grep -q "acceptLicenseTerms"; then
    echo "   ⚠️  CLI publish rejected by registry (missing acceptLicenseTerms). Using API fallback..."
    TOKEN_FILE="$HOME/Library/Application Support/clawhub/config.json"
    if [ ! -f "$TOKEN_FILE" ]; then
      echo "   ✖ ClawHub token file not found: $TOKEN_FILE"
      exit 1
    fi
    CLAWHUB_TOKEN="$(jq -r '.token' "$TOKEN_FILE")"
    if [ -z "$CLAWHUB_TOKEN" ] || [ "$CLAWHUB_TOKEN" = "null" ]; then
      echo "   ✖ Missing token in ClawHub config"
      exit 1
    fi

    PAYLOAD_JSON="$(printf '{"slug":"molt-motion","displayName":"Molt Motion","version":"%s","changelog":"Release %s","tags":["latest"],"acceptLicenseTerms":true}' "$NEW_VERSION" "$NEW_VERSION")"
    RESPONSE_FILE="$(mktemp)"

    FILE_ARGS=()
    while IFS= read -r -d '' file; do
      rel="${file#"$SKILL_DIR"/}"
      FILE_ARGS+=(-F "files=@$file;type=text/plain;filename=$rel")
    done < <(find "$SKILL_DIR/bin" "$SKILL_DIR/schemas" "$SKILL_DIR/api" -type f -print0)
    while IFS= read -r -d '' file; do
      rel="${file#"$SKILL_DIR"/}"
      FILE_ARGS+=(-F "files=@$file;type=text/plain;filename=$rel")
    done < <(find "$SKILL_DIR" -maxdepth 1 -type f \( -name "*.md" -o -name "*.json" \) -print0)

    if ! curl -sS -X POST "https://clawhub.ai/api/v1/skills" \
      -H "Authorization: Bearer $CLAWHUB_TOKEN" \
      -F "payload=$PAYLOAD_JSON" \
      "${FILE_ARGS[@]}" >"$RESPONSE_FILE"; then
      echo "   ✖ ClawHub API fallback request failed"
      exit 1
    fi

    if jq -e '.ok == true' "$RESPONSE_FILE" >/dev/null 2>&1; then
      echo "   ✓ Published to ClawHub registry (API fallback)"
    else
      echo "   ✖ ClawHub API fallback failed: $(cat "$RESPONSE_FILE")"
      exit 1
    fi
  else
    echo "   ✖ ClawHub publish failed: $PUBLISH_ERR_MSG"
    exit 1
  fi
fi
rm -f "$PUBLISH_ERR_FILE"
echo ""

# Print installation instructions
echo "════════════════════════════════════════════════════════════════"
echo "  ✅ Release v$NEW_VERSION Complete!"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "📥 Installation Instructions:"
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
echo "📄 View release:"
echo "   https://github.com/chefbc2k/MOLTSTUDIOS/releases/tag/moltmotion-skill-v$NEW_VERSION"
echo ""
