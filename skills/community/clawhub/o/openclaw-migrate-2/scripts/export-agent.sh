#!/bin/bash
# export-agent.sh - 导出完整 Agent 状态
set -e

EXPORT_NAME="${1:-export_$(date +%Y%m%d_%H%M%S)}"
EXPORT_DIR="/tmp/agent-export-$EXPORT_NAME"
FULL_MODE=false

if [ "$2" == "--full" ]; then
    FULL_MODE=true
fi

echo "[EXPORT] 开始导出: $EXPORT_NAME"
mkdir -p "$EXPORT_DIR"

# 1. 导出 workspace
echo "  → 导出 workspace..."
tar czf "$EXPORT_DIR/workspace.tar.gz" -C /home/node/.openclaw workspace \
    --exclude='*.log' --exclude='node_modules' --exclude='.git' 2>/dev/null || true

# 2. 导出配置
echo "  → 导出配置..."
mkdir -p "$EXPORT_DIR/config"
cp /home/node/.openclaw/openclaw.json "$EXPORT_DIR/config/" 2>/dev/null || true

# 3. 导出自定义 skills（如果有）
if [ -d "/home/node/.openclaw/skills" ]; then
    echo "  → 导出自定义 skills..."
    tar czf "$EXPORT_DIR/skills.tar.gz" -C /home/node/.openclaw skills 2>/dev/null || true
fi

# 4. 导出 extensions（如果有）
if [ -d "/home/node/.openclaw/extensions" ]; then
    echo "  → 导出 extensions..."
    tar czf "$EXPORT_DIR/extensions.tar.gz" -C /home/node/.openclaw \
        --exclude='node_modules' --exclude='*.log' --exclude='dist' \
        extensions 2>/dev/null || true
fi

# 5. Full mode: 包含 session 数据
if [ "$FULL_MODE" = true ]; then
    echo "  → 导出 sessions (full mode)..."
    tar czf "$EXPORT_DIR/sessions.tar.gz" -C /home/node/.openclaw agents 2>/dev/null || true
fi

# 6. 创建清单
cat > "$EXPORT_DIR/manifest.json" << EOF
{
  "export_name": "$EXPORT_NAME",
  "export_time": "$(date -Iseconds)",
  "source_host": "$(hostname)",
  "openclaw_version": "$(openclaw status 2>>1 | head -5 | grep -i version || echo 'unknown')",
  "full_mode": $FULL_MODE,
  "components": {
    "workspace": true,
    "config": true,
    "skills": $(test -f "$EXPORT_DIR/skills.tar.gz" && echo true || echo false),
    "extensions": $(test -f "$EXPORT_DIR/extensions.tar.gz" && echo true || echo false),
    "sessions": $FULL_MODE
  }
}
EOF

# 7. 创建自恢复脚本
cat > "$EXPORT_DIR/restore.sh" << 'RESTORE_SCRIPT'
#!/bin/bash
# Self-contained restore script
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${1:-$HOME/.openclaw}"

echo "[RESTORE] 恢复 Agent 到: $TARGET_DIR"
mkdir -p "$TARGET_DIR"

# 恢复 workspace
if [ -f "$SCRIPT_DIR/workspace.tar.gz" ]; then
    echo "  → 恢复 workspace..."
    tar xzf "$SCRIPT_DIR/workspace.tar.gz" -C "$TARGET_DIR"
fi

# 恢复配置
if [ -f "$SCRIPT_DIR/config/openclaw.json" ]; then
    echo "  → 恢复配置..."
    cp "$SCRIPT_DIR/config/openclaw.json" "$TARGET_DIR/"
fi

# 恢复 skills
if [ -f "$SCRIPT_DIR/skills.tar.gz" ]; then
    echo "  → 恢复 skills..."
    tar xzf "$SCRIPT_DIR/skills.tar.gz" -C "$TARGET_DIR"
fi

# 恢复 extensions
if [ -f "$SCRIPT_DIR/extensions.tar.gz" ]; then
    echo "  → 恢复 extensions..."
    tar xzf "$SCRIPT_DIR/extensions.tar.gz" -C "$TARGET_DIR"
fi

echo "[RESTORE] 完成. 请检查配置并运行: openclaw status"
RESTORE_SCRIPT

chmod +x "$EXPORT_DIR/restore.sh"

# 8. 打包最终导出
cd /tmp
FINAL_ARCHIVE="agent-export-$EXPORT_NAME.tar.gz"
tar czf "$FINAL_ARCHIVE" "agent-export-$EXPORT_NAME"

echo ""
echo "[EXPORT] 完成!"
echo "  导出目录: $EXPORT_DIR"
echo "  压缩包: /tmp/$FINAL_ARCHIVE"
echo ""
echo "传输到目标服务器:"
echo "  scp /tmp/$FINAL_ARCHIVE user@server:/tmp/"
echo ""
echo "在目标服务器恢复:"
echo "  tar xzf /tmp/$FINAL_ARCHIVE -C /tmp/"
echo "  cd /tmp/agent-export-$EXPORT_NAME && ./restore.sh"
