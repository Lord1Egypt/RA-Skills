#!/bin/bash
# Git Backup Script for OpenClaw Agents
# Backs up core workspace files to Gitee repository
#
# Usage: ./backup-to-gitee.sh [commit-message]

set -e

# Configuration (can be overridden by environment variables)
WORKSPACE_DIR="${WORKSPACE_DIR:-$HOME/.openclaw/workspace}"
BACKUP_DIR="${BACKUP_DIR:-$HOME/.openclaw/backup-temp}"
GITEE_REPO="${GITEE_REPO:-}"           # e.g., https://gitee.com/username/openclaw-agent-name.git
GITEE_TOKEN="${GITEE_TOKEN:-}"         # Personal Access Token
AGENT_NAME="${AGENT_NAME:-agent}"      # For commit signature

# Files to backup (relative to workspace)
BACKUP_FILES=(
    "AGENTS.md"
    "SOUL.md"
    "IDENTITY.md"
    "USER.md"
    "MEMORY.md"
    "TOOLS.md"
    "HEARTBEAT.md"
)

# Directories to backup (relative to workspace)
BACKUP_DIRS=(
    "memory"
    "skills"
)

# Validate configuration
if [[ -z "$GITEE_REPO" ]]; then
    echo "Error: GITEE_REPO not set. Run setup-gitee.sh first or export GITEE_REPO=<repo-url>"
    exit 1
fi

if [[ -z "$GITEE_TOKEN" ]]; then
    echo "Error: GITEE_TOKEN not set. Export GITEE_TOKEN=<your-token>"
    exit 1
fi

# Prepare backup directory
rm -rf "$BACKUP_DIR"
mkdir -p "$BACKUP_DIR"

echo "=== OpenClaw Git Backup ==="
echo "Agent: $AGENT_NAME"
echo "Workspace: $WORKSPACE_DIR"
echo "Repo: $GITEE_REPO"
echo ""

# Clone or initialize repo
if [[ -d "$BACKUP_DIR/.git" ]]; then
    cd "$BACKUP_DIR"
    git pull
else
    # Clone with token authentication
    AUTH_REPO="${GITEE_REPO/https:\/\//https:\/\/oauth2:${GITEE_TOKEN}@}"
    git clone "$AUTH_REPO" "$BACKUP_DIR" 2>/dev/null || {
        # If clone fails, repo might not exist - initialize new
        mkdir -p "$BACKUP_DIR"
        cd "$BACKUP_DIR"
        git init
        git remote add origin "$AUTH_REPO"
    }
fi

cd "$BACKUP_DIR"

# Configure git
git config user.name "$AGENT_NAME"
git config user.email "${AGENT_NAME}@openclaw.local"

# Copy files
echo "Copying files..."
for file in "${BACKUP_FILES[@]}"; do
    src="$WORKSPACE_DIR/$file"
    if [[ -f "$src" ]]; then
        cp "$src" "$BACKUP_DIR/"
        echo "  ✓ $file"
    fi
done

# Copy directories
for dir in "${BACKUP_DIRS[@]}"; do
    src="$WORKSPACE_DIR/$dir"
    if [[ -d "$src" ]]; then
        rm -rf "$BACKUP_DIR/$dir"
        cp -r "$src" "$BACKUP_DIR/"
        echo "  ✓ $dir/"
    fi
done

# Create .gitignore for backup
cat > "$BACKUP_DIR/.gitignore" << 'EOF'
# Secrets and sensitive files
.env
*.key
*.pem
*_token*
*_secret*
.secrets/

# Node modules
node_modules/

# Temporary files
*.tmp
*.log
*.bak
EOF

# Check for changes
if [[ -z $(git status --porcelain) ]]; then
    echo ""
    echo "No changes to backup."
    exit 0
fi

# Commit message
COMMIT_MSG="${1:-Backup: $(date '+%Y-%m-%d %H:%M:%S')}"

# Stage and commit
git add -A
git commit -m "$COMMIT_MSG"

# Push
git push -u origin main 2>/dev/null || git push -u origin master 2>/dev/null || {
    echo "Push failed, trying force..."
    git push -f origin main 2>/dev/null || git push -f origin master
}

echo ""
echo "✅ Backup complete: $COMMIT_MSG"
echo "   Files: $(git diff-tree --no-commit-id --name-only -r HEAD | wc -l) changed"