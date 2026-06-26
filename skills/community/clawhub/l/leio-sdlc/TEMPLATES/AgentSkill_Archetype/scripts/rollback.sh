#!/bin/bash
set -e

SLUG=$(basename "$PWD")
# Allow tests to override HOME
HOME_DIR="${HOME_MOCK:-$HOME}"
OPENCLAW_DIR="$HOME_DIR/.openclaw"
SKILLS_DIR="$OPENCLAW_DIR/skills"
RELEASES_DIR="$OPENCLAW_DIR/.releases/$SLUG"
PROD_LINK="$SKILLS_DIR/$SLUG"

echo "⏪ Initiating instant rollback for $SLUG..."

if [ ! -L "$PROD_LINK" ]; then
    echo "❌ Error: $PROD_LINK is not a symlink. Cannot rollback."
    exit 1
fi

CURRENT_TARGET=$(readlink "$PROD_LINK")
CURRENT_RELEASE=$(basename "$CURRENT_TARGET")

# Get list of releases sorted by time (newest first)
RELEASES=($(ls -dt "$RELEASES_DIR"/* 2>/dev/null | grep -E '/[0-9]{8}_[0-9]{6}$' || true))

if [ ${#RELEASES[@]} -lt 2 ]; then
    echo "❌ Error: Not enough releases to perform a rollback."
    exit 1
fi

PREVIOUS_RELEASE_PATH=""
FOUND_CURRENT=false

for rel in "${RELEASES[@]}"; do
    rel_name=$(basename "$rel")
    if [ "$rel_name" = "$CURRENT_RELEASE" ]; then
        FOUND_CURRENT=true
        continue
    fi
    if [ "$FOUND_CURRENT" = true ]; then
        PREVIOUS_RELEASE_PATH="$rel"
        break
    fi
done

if [ -z "$PREVIOUS_RELEASE_PATH" ]; then
    # If current release wasn't found in the list (maybe it was deleted), or it's the oldest
    # Just rollback to the newest available release that is not the current one
    if [ "$FOUND_CURRENT" = false ]; then
        PREVIOUS_RELEASE_PATH="${RELEASES[0]}"
    else
        echo "❌ Error: Could not identify a previous release."
        exit 1
    fi
fi

echo "🔄 Rolling back from $CURRENT_RELEASE to $(basename "$PREVIOUS_RELEASE_PATH")"

# Atomic swap
ln -snf "$PREVIOUS_RELEASE_PATH" "$RELEASES_DIR/current_tmp"
mv -T "$RELEASES_DIR/current_tmp" "$PROD_LINK"

# Gateway Reload
if [ -z "$HOME_MOCK" ]; then
    echo "🔄 Restarting OpenClaw gateway..."
    openclaw gateway restart || echo "⚠️ Gateway restart failed or not available."
fi

echo "✅ ROLLBACK SUCCESS: $SLUG is now running $(basename "$PREVIOUS_RELEASE_PATH")."
