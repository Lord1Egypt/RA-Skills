#!/bin/bash
# Deploy skill to ClawHub (and optionally MCP server to npm)
# Usage: sh deploy.sh          — ClawHub only
#        sh deploy.sh --npm    — ClawHub + npm

set -e
cd "$(dirname "$0")"

# Read version from SKILL.md frontmatter
VERSION=$(grep '^version:' SKILL.md | head -1 | awk '{print $2}')
if [ -z "$VERSION" ]; then
	echo "ERROR: No version found in SKILL.md frontmatter"
	exit 1
fi

# Bump patch version
IFS='.' read -r MAJOR MINOR PATCH <<< "$VERSION"
NEW_PATCH=$((PATCH + 1))
NEW_VERSION="$MAJOR.$MINOR.$NEW_PATCH"

echo "Current version: $VERSION"
echo "New version:     $NEW_VERSION"
echo ""

# Update SKILL.md frontmatter
sed -i '' "s/^version: $VERSION/version: $NEW_VERSION/" SKILL.md
echo "Updated SKILL.md -> $NEW_VERSION"

# Publish to ClawHub
echo ""
echo "Publishing to ClawHub..."
clawhub publish . --version "$NEW_VERSION" --slug playasia
echo "ClawHub: playasia@$NEW_VERSION"

# Publish to npm (if --npm flag)
if [ "$1" = "--npm" ]; then
	echo ""
	echo "Publishing to npm..."
	sed -i '' "s/\"version\": \".*\"/\"version\": \"$NEW_VERSION\"/" package.json
	npm run build
	npm publish --access public
	echo "npm: @playasia/mcp@$NEW_VERSION"
fi

echo ""
echo "Done: $NEW_VERSION"
