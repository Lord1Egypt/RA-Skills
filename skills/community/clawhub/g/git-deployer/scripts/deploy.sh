#!/bin/bash
# git-deployer — Deploy static site content to a git remote
# Usage: deploy.sh <site_path> <remote_url> [branch]
# Example: deploy.sh /home/tim/site-build git@github.com:user/repo.git main

set -e

SITE_PATH="$1"
REMOTE_URL="$2"
BRANCH="${3:-main}"

if [[ -z "$SITE_PATH" || -z "$REMOTE_URL" ]]; then
    echo "ERROR: Missing required arguments"
    echo "Usage: deploy.sh <site_path> <remote_url> [branch]"
    exit 1
fi

if [[ ! -d "$SITE_PATH" ]]; then
    echo "ERROR: Site path does not exist or is not a directory: $SITE_PATH"
    exit 1
fi

# Extract repo name from URL for /tmp directory
REPO_NAME=$(basename "$REMOTE_URL" .git)
TMP_CLONE="/tmp/$REPO_NAME"
TIMESTAMP=$(date -u "+%Y-%m-%d %H:%M:%S")
COMMIT_MSG="Deploy: $TIMESTAMP UTC"

echo "=== git-deployer ==="
echo "Site path: $SITE_PATH"
echo "Remote:    $REMOTE_URL"
echo "Branch:    $BRANCH"
echo "Timestamp: $TIMESTAMP"
echo ""

# Clone or init
if [[ -d "$TMP_CLONE" ]]; then
    echo "[1/5] Clone exists at $TMP_CLONE — pulling latest..."
    cd "$TMP_CLONE"
    git fetch origin
    git checkout "$BRANCH" || git checkout -b "$BRANCH"
    git pull origin "$BRANCH"
else
    echo "[1/5] Cloning fresh repo..."
    git clone "$REMOTE_URL" "$TMP_CLONE"
    cd "$TMP_CLONE"
    git checkout "$BRANCH" 2>/dev/null || git checkout -b "$BRANCH"
fi

# Copy files (rsync-like behavior: mirror contents)
echo "[2/5] Copying site files to clone..."
rsync -av --delete "$SITE_PATH/" "$TMP_CLONE/"

# Stage all changes
echo "[3/5] Staging files..."
git add -A

# Check if there are changes to commit
if git diff --staged --quiet; then
    echo "No changes to commit — repository is up to date."
    echo "Nothing to push."
    exit 0
fi

# Commit
echo "[4/5] Committing..."
git commit -m "$COMMIT_MSG"
COMMIT_HASH=$(git rev-parse HEAD)
echo "Committed: $COMMIT_HASH"

# Force push
echo "[5/5] Force-pushing to $BRANCH..."
git push -u origin "$BRANCH" --force

echo ""
echo "=== Deploy Complete ==="
echo "Commit:    $COMMIT_HASH"
echo "Remote:    $REMOTE_URL"
echo "Branch:    $BRANCH"
echo "Clone:     $TMP_CLONE"
