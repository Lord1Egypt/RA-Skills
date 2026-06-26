#!/bin/bash
# sync-github.sh - 同步 Agent 最小化数据到 GitHub 私有仓库
set -e

REPO_URL="$1"
MODE="${2:-push}"
TEMP_DIR="/tmp/agent-sync-$(date +%s)"

if [ -z "$REPO_URL" ]; then
    echo "用法: $0 <repo-url> [--push|--pull]"
    echo "  示例: $0 git@github.com:xiage/my-agent.git --push"
    exit 1
fi

echo "[SYNC] GitHub 同步: $MODE"
echo "  仓库: $REPO_URL"

# 清理
trap "rm -rf $TEMP_DIR" EXIT
mkdir -p "$TEMP_DIR"

if [ "$MODE" == "push" ]; then
    echo "  → 推送到 GitHub..."
    
    # 克隆仓库
    git clone "$REPO_URL" "$TEMP_DIR/repo" 2>/dev/null || {
        echo "  仓库不存在，初始化新仓库..."
        mkdir -p "$TEMP_DIR/repo"
        cd "$TEMP_DIR/repo"
        git init
        git remote add origin "$REPO_URL"
        # 创建 README
        echo "# Agent Backup" > README.md
        git add README.md
        git commit -m "init"
        git push -u origin HEAD:main 2>/dev/null || git push -u origin HEAD:master 2>/dev/null || true
    }
    
    cd "$TEMP_DIR/repo"
    
    # 创建最小化备份结构
    echo "  → 收集 Agent 数据..."
    mkdir -p agent-backup
    
    # 1. 核心身份文件
    echo "    - 核心配置文件"
    for file in IDENTITY.md USER.md SOUL.md AGENTS.md TOOLS.md MEMORY.md BOOTSTRAP.md HEARTBEAT.md; do
        if [ -f "/home/node/.openclaw/workspace/$file" ]; then
            cp "/home/node/.openclaw/workspace/$file" agent-backup/ 2>/dev/null || true
        fi
    done
    
    # 2. memory 目录
    if [ -d "/home/node/.openclaw/workspace/memory" ]; then
        echo "    - 记忆文件"
        cp -r "/home/node/.openclaw/workspace/memory" agent-backup/ 2>/dev/null || true
    fi
    
    # 3. 已安装 skills 清单（只存名字，不存内容）
    echo "    - skills 清单"
    ls /usr/local/lib/node_modules/openclaw/skills/ > agent-backup/installed-skills.txt 2>/dev/null || true
    
    # 4. 自定义 skills（如果有）
    if [ -d "/home/node/.openclaw/skills" ]; then
        echo "    - 自定义 skills"
        mkdir -p agent-backup/custom-skills
        cp /home/node/.openclaw/skills/*.skill agent-backup/custom-skills/ 2>/dev/null || true
    fi
    
    # 5. 配置模板（脱敏）
    echo "    - 配置模板（脱敏）"
    if [ -f "/home/node/.openclaw/openclaw.json" ]; then
        jq 'walk(if type == "object" then 
            with_entries(if .value | type == "string" and (contains("key") or contains("token") or contains("secret")) 
            then .value = "***REMOVED***" else . end) 
        else . end)' "/home/node/.openclaw/openclaw.json" > agent-backup/openclaw.json.template 2>/dev/null || \
            echo "{}" > agent-backup/openclaw.json.template
    fi
    
    # 6. 创建恢复脚本
    cat > agent-backup/restore.sh << 'EOF'
#!/bin/bash
# 恢复 Agent 最小化备份
set -e

TARGET="${1:-$HOME/.openclaw}"
echo "[RESTORE] 恢复 Agent 到: $TARGET"

mkdir -p "$TARGET/workspace"

# 恢复核心文件
echo "  → 恢复配置文件..."
for file in IDENTITY.md USER.md SOUL.md AGENTS.md TOOLS.md MEMORY.md BOOTSTRAP.md HEARTBEAT.md; do
    if [ -f "$file" ]; then
        cp "$file" "$TARGET/workspace/"
        echo "    ✓ $file"
    fi
done

# 恢复 memory
if [ -d "memory" ]; then
    echo "  → 恢复记忆..."
    cp -r memory "$TARGET/workspace/"
fi

# 恢复自定义 skills
if [ -d "custom-skills" ]; then
    echo "  → 恢复自定义 skills..."
    mkdir -p "$TARGET/skills"
    cp custom-skills/* "$TARGET/skills/" 2>/dev/null || true
fi

# 提示
if [ -f "installed-skills.txt" ]; then
    echo ""
    echo "  📋 已安装 skills 清单（需手动安装）:"
    cat installed-skills.txt | while read skill; do
        echo "     - $skill"
    done
fi

if [ -f "openclaw.json.template" ]; then
    echo ""
    echo "  ⚠️  请手动配置 openclaw.json（模板已保存）"
    cp openclaw.json.template "$TARGET/openclaw.json"
fi

echo ""
echo "[RESTORE] ✅ 完成"
echo "  下一步: 1) 配置 API keys  2) 安装 skills  3) openclaw status"
EOF
    chmod +x agent-backup/restore.sh
    
    # 7. 创建清单
    cat > agent-backup/MANIFEST.json << EOF
{
  "sync_time": "$(date -Iseconds)",
  "source": "$(whoami)@$(hostname)",
  "version": "$(openclaw status 2>>1 | grep -i 'openclaw' | head -1 | awk '{print $2}' || echo 'unknown')",
  "files": $(ls -1 agent-backup/*.md 2>/dev/null | xargs -n1 basename | jq -R . | jq -s .),
  "memory_files": $(ls -1 agent-backup/memory/*.md 2>/dev/null | wc -l),
  "custom_skills": $(ls -1 agent-backup/custom-skills/*.skill 2>/dev/null | wc -l)
}
EOF
    
    # 提交推送
    git add -A
    git commit -m "Agent backup: $(date '+%Y-%m-%d %H:%M:%S')" || true
    
    echo "  → 推送到远程..."
    git push origin HEAD:main 2>/dev/null || git push origin HEAD:master 2>/dev/null || {
        echo "  尝试强制推送..."
        git push --force origin HEAD:main 2>/dev/null || git push --force origin HEAD:master 2>/dev/null
    }
    
    echo "[SYNC] ✅ 推送完成"
    echo "  备份位置: $REPO_URL"
    
elif [ "$MODE" == "pull" ]; then
    echo "  → 从 GitHub 拉取..."
    
    git clone "$REPO_URL" "$TEMP_DIR/repo"
    cd "$TEMP_DIR/repo/agent-backup"
    
    ./restore.sh
    
    echo "[SYNC] ✅ 拉取完成"
fi
