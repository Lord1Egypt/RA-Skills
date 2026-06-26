#!/bin/bash

# OpenClaw Skills GitHub Sync Script for Linux/Mac
# ==== 配置加载 ====
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/config.sh"

if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
else
    # 默认配置
    PRIVATE_PATH="$HOME/openclaw-skills-private"
    PUBLIC_PATH="$HOME/openclaw-skills-public"
fi

echo "=========================================="
echo "OpenClaw Skills GitHub Sync"
echo "=========================================="

gitPath="git"

# Function to sync a repository
sync_repo() {
    local repo_path="$1"
    local repo_name="$2"
    
    if [ ! -d "$repo_path" ]; then
        echo "[SKIP] $repo_name not found"
        return
    fi
    
    cd "$repo_path"
    
    if [ ! -d ".git" ]; then
        echo "[SKIP] $repo_name - Not a git repository"
        return
    fi
    
    # 检查是否有 .gitignore
    if [ ! -f ".gitignore" ]; then
        echo "[WARN] No .gitignore found, creating..."
        cat > .gitignore << 'EOF'
# Credentials
credentials/
*.key
*.pem

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Temp
*.tmp
*.temp
EOF
    fi
    
    status=$(git status --porcelain)
    
    if [ -n "$status" ]; then
        echo "Changes in $repo_name:"
        echo "$status"
        
        echo ""
        echo "Run 'git status' to review changes before committing."
        echo "The following files will be added:"
        git diff --cached --name-only 2>/dev/null || echo "(no staged files)"
        
        read -p "Continue with sync? (y/n): " confirm
        if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
            echo "Sync cancelled."
            return
        fi
        
        git add -A
        git commit -m "Sync $(date '+%Y-%m-%d %H:%M')"
        git push origin main
        
        if [ $? -eq 0 ]; then
            echo "[OK] $repo_name synced"
        else
            echo "[FAIL] $repo_name sync failed"
        fi
    else
        echo "[OK] $repo_name - No changes"
    fi
}

# Sync private skills
echo ""
echo "--- Private Skills ---"
sync_repo "$PRIVATE_PATH" "Private"

# Sync public skills  
echo ""
echo "--- Public Skills ---"
sync_repo "$PUBLIC_PATH" "Public"

echo ""
echo "=========================================="
