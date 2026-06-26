#!/bin/bash
# hg-to-git-large.sh - Convert large Mercurial repository to Git with progress
# Usage: hg-to-git-large.sh <hg-repo-path> [git-repo-path]

set -e

HG_REPO="${1:-}"
GIT_REPO="${2:-}"

if [ -z "$HG_REPO" ]; then
    echo "Usage: $0 <hg-repo-path> [git-repo-path]"
    exit 1
fi

if [ ! -d "$HG_REPO/.hg" ]; then
    echo "Error: $HG_REPO is not a valid Mercurial repository"
    exit 1
fi

HG_REPO=$(cd "$HG_REPO" && pwd)

if [ -z "$GIT_REPO" ]; then
    GIT_REPO="${HG_REPO}-git"
fi

# Check dependencies
for cmd in hg git; do
    if ! command -v $cmd &> /dev/null; then
        echo "Error: $cmd is not installed"
        exit 1
    fi
done

echo "=== Large Repository Conversion ==="
echo "Source: $HG_REPO"
echo "Target: $GIT_REPO"
echo ""

# Get revision count
HG_COUNT=$(hg log -r 'all()' --template '.' | wc -c)
echo "Total revisions in Mercurial: $HG_COUNT"
echo ""

# Setup fast-export
FAST_EXPORT_CMD=""
if command -v hg-fast-export &> /dev/null; then
    FAST_EXPORT_CMD="hg-fast-export"
elif command -v hg-fast-export.sh &> /dev/null; then
    FAST_EXPORT_CMD="hg-fast-export.sh"
else
    FAST_EXPORT_DIR="${HOME}/.local/share/hg-fast-export"
    if [ ! -d "$FAST_EXPORT_DIR" ]; then
        echo "Installing hg-fast-export..."
        mkdir -p "$(dirname "$FAST_EXPORT_DIR")"
        git clone --depth 1 https://github.com/frej/fast-export.git "$FAST_EXPORT_DIR"
    fi
    FAST_EXPORT_CMD="${FAST_EXPORT_DIR}/hg-fast-export.sh"
fi

# Create git repo
if [ -d "$GIT_REPO" ]; then
    echo "Removing existing $GIT_REPO..."
    rm -rf "$GIT_REPO"
fi

mkdir -p "$GIT_REPO"
cd "$GIT_REPO"
git init

echo ""
echo "Starting conversion with progress output..."
echo "This will show '.' for each 100 revisions processed"
echo ""

# Run conversion with feedback
"$FAST_EXPORT_CMD" -r "$HG_REPO" --force 2>&1 | while read line; do
    if [[ $line == *"revision"* ]]; then
        echo -n "."
    else
        echo "$line"
    fi
done

echo ""
echo "Checking out files..."
git checkout HEAD 2>&1 | head -20

echo ""
echo "=== Conversion Complete ==="
echo "Git repository: $GIT_REPO"
echo ""
git log --oneline -5
echo "..."
echo ""
echo "Total commits: $(git rev-list --all --count)"
