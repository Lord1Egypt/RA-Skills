#!/bin/bash
# install_hook.sh: Install the SDLC pre-commit hook into the current repository.
# Usage: ./scripts/install_hook.sh [target_git_dir]

TARGET_DIR="${1:-.git}"
HOOK_SOURCE="$(dirname "$0")/pre-commit-payload.sh"

if [ ! -d "$TARGET_DIR" ]; then
    echo "ERROR: Target directory '$TARGET_DIR' is not a git directory."
    exit 1
fi

if [ ! -f "$HOOK_SOURCE" ]; then
    echo "ERROR: Hook source '$HOOK_SOURCE' not found."
    exit 1
fi

mkdir -p "$TARGET_DIR/hooks"
cp "$HOOK_SOURCE" "$TARGET_DIR/hooks/pre-commit"
chmod +x "$TARGET_DIR/hooks/pre-commit"

echo "✅ SDLC Pre-commit hook installed successfully into $TARGET_DIR/hooks/pre-commit"
