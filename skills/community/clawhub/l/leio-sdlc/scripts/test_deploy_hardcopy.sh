#!/bin/bash
set -e

echo "=== Running Hard-Copy Deploy & Rollback Integration Test ==="

# 1. Define a mock HOME directory
MOCK_HOME="/tmp/mock_home_$$"
export HOME_MOCK="$MOCK_HOME"

# Clean up any previous run
rm -rf "$MOCK_HOME"

SKILL_NAME="test-skill"
MOCK_SKILL_SRC="$MOCK_HOME/src/$SKILL_NAME"
MOCK_SKILLS_DIR="$MOCK_HOME/.openclaw/skills"
MOCK_RELEASES_DIR="$MOCK_HOME/.openclaw/.releases/$SKILL_NAME"

# 2. Create dummy skills directory and src
mkdir -p "$MOCK_SKILL_SRC"

# Create dummy content
echo "v1" > "$MOCK_SKILL_SRC/version.txt"

# Provide deploy and rollback scripts
# Using the main deploy.sh and scripts/rollback.sh which we just updated
cp "$PWD/deploy.sh" "$MOCK_SKILL_SRC/deploy.sh"
cp "$PWD/scripts/rollback.sh" "$MOCK_SKILL_SRC/rollback.sh"
chmod +x "$MOCK_SKILL_SRC/deploy.sh" "$MOCK_SKILL_SRC/rollback.sh"

# 3. Run deploy.sh with the mock HOME exported
cd "$MOCK_SKILL_SRC"
./deploy.sh

# 4. Assert 1: Check it is NOT a symlink
if [ -L "$MOCK_SKILLS_DIR/$SKILL_NAME" ]; then
    echo "❌ Assertion Failed: $MOCK_SKILLS_DIR/$SKILL_NAME is a symlink!"
    exit 1
fi

# 5. Assert 2: Check it is a directory
if [ ! -d "$MOCK_SKILLS_DIR/$SKILL_NAME" ]; then
    echo "❌ Assertion Failed: $MOCK_SKILLS_DIR/$SKILL_NAME is not a directory!"
    exit 1
fi

# Assert content is correct
if [ "$(cat "$MOCK_SKILLS_DIR/$SKILL_NAME/version.txt")" != "v1" ]; then
    echo "❌ Assertion Failed: Version content mismatch!"
    exit 1
fi

# Now let's simulate a second deploy to generate a backup
sleep 1
echo "v2" > "version.txt"
./deploy.sh

if [ "$(cat "$MOCK_SKILLS_DIR/$SKILL_NAME/version.txt")" != "v2" ]; then
    echo "❌ Assertion Failed: Version content mismatch after second deploy!"
    exit 1
fi

# 6. Assert 3: Verify a backup_*.tar.gz exists in the mock .releases directory
BACKUP_COUNT=$(ls -1 "$MOCK_RELEASES_DIR"/backup_*.tar.gz 2>/dev/null | wc -l)
if [ "$BACKUP_COUNT" -lt 1 ]; then
    echo "❌ Assertion Failed: No backup tarball found in $MOCK_RELEASES_DIR"
    exit 1
fi

# 7. Run rollback.sh and verify directory is correctly restored
./rollback.sh

if [ "$(cat "$MOCK_SKILLS_DIR/$SKILL_NAME/version.txt")" != "v1" ]; then
    echo "❌ Assertion Failed: Rollback failed. Expected v1 but got $(cat "$MOCK_SKILLS_DIR/$SKILL_NAME/version.txt")"
    exit 1
fi

# Clean up
rm -rf "$MOCK_HOME"

echo "✅ Hard-Copy Deploy & Rollback Integration Test PASSED"
