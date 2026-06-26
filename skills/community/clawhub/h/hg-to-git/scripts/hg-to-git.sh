#!/bin/bash
# hg-to-git.sh - Convert Mercurial repository to Git
# Usage: hg-to-git.sh <hg-repo-path> [git-repo-path]

set -e

HG_REPO="${1:-}"
GIT_REPO="${2:-}"

if [ -z "$HG_REPO" ]; then
    echo "Usage: $0 <hg-repo-path> [git-repo-path]"
    echo "Example: $0 /path/to/hg-repo /path/to/git-repo"
    exit 1
fi

if [ ! -d "$HG_REPO/.hg" ]; then
    echo "Error: $HG_REPO is not a valid Mercurial repository"
    exit 1
fi

# Resolve to absolute path
HG_REPO=$(cd "$HG_REPO" && pwd)

# Default git repo path
if [ -z "$GIT_REPO" ]; then
    GIT_REPO="${HG_REPO}-git"
fi

# Check dependencies
if ! command -v hg &> /dev/null; then
    echo "Error: hg (Mercurial) is not installed"
    exit 1
fi

if ! command -v git &> /dev/null; then
    echo "Error: git is not installed"
    exit 1
fi

echo "=== Converting Mercurial to Git ==="
echo "Source: $HG_REPO"
echo "Target: $GIT_REPO"
echo ""

# Check for hg-fast-export
if ! command -v hg-fast-export &> /dev/null && ! command -v hg-fast-export.sh &> /dev/null; then
    echo "Installing hg-fast-export..."
    
    # Try different installation methods
    if command -v apt-get &> /dev/null; then
        sudo apt-get update && sudo apt-get install -y hg-fast-export 2>/dev/null || true
    elif command -v brew &> /dev/null; then
        brew install hg-fast-export 2>/dev/null || true
    fi
    
    # If still not found, clone from source
    if ! command -v hg-fast-export &> /dev/null && ! command -v hg-fast-export.sh &> /dev/null; then
        FAST_EXPORT_DIR="${HOME}/.local/share/hg-fast-export"
        if [ ! -d "$FAST_EXPORT_DIR" ]; then
            mkdir -p "$(dirname "$FAST_EXPORT_DIR")"
            git clone https://github.com/frej/fast-export.git "$FAST_EXPORT_DIR"
        fi
        export PATH="$FAST_EXPORT_DIR:$PATH"
    fi
fi

# Determine fast-export command
if command -v hg-fast-export &> /dev/null; then
    FAST_EXPORT_CMD="hg-fast-export"
elif command -v hg-fast-export.sh &> /dev/null; then
    FAST_EXPORT_CMD="hg-fast-export.sh"
elif [ -f "${HOME}/.local/share/hg-fast-export/hg-fast-export.sh" ]; then
    FAST_EXPORT_CMD="${HOME}/.local/share/hg-fast-export/hg-fast-export.sh"
else
    echo "Error: hg-fast-export not found. Please install it manually."
    echo "See: https://github.com/frej/fast-export"
    exit 1
fi

# Create git repo
if [ -d "$GIT_REPO" ]; then
    echo "Warning: $GIT_REPO already exists"
    read -p "Remove it? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$GIT_REPO"
    else
        echo "Aborted"
        exit 1
    fi
fi

mkdir -p "$GIT_REPO"
cd "$GIT_REPO"
git init

# Perform conversion
echo ""
echo "Converting... (this may take a while for large repos)"
"$FAST_EXPORT_CMD" -r "$HG_REPO" --force

# Checkout files
git checkout HEAD

echo ""
echo "=== Conversion Complete ==="
echo "Git repository: $GIT_REPO"
echo ""
echo "Branches:"
git branch -a
echo ""
echo "Tags:"
git tag -l
