#!/bin/bash
# OpenClaw Guardian - 自检脚本

# 确保 HOME 变量存在
if [ -z "$HOME" ]; then
    export HOME=$(eval echo ~)
fi

LOG_FILE="${HOME}/.openclaw/skills/openclaw-guardian/guardian.log"
BASELINE_FILE="${HOME}/.openclaw/skills/openclaw-guardian/skill-baseline.txt"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "🛡️ OpenClaw 自检开始"
echo "----------------"

# 0. Skills 目录检查
SKILLS_DIR="${HOME}/.openclaw/skills"
if [ -d "$SKILLS_DIR" ]; then
    SKILL_COUNT=$(ls -d "$SKILLS_DIR"/*/ 2>/dev/null | wc -l)
    echo "✅ Skills 目录: 存在 ($SKILL_COUNT 个)"

    # 检查关键 skill 文件
    MISSING_SKILL_MD=$(find "$SKILLS_DIR" -maxdepth 2 -name "SKILL.md" 2>/dev/null | wc -l)
    echo "   - SKILL.md 文件: $MISSING_SKILL_MD 个"

    # 基线对比（首次运行时创建基线）
    if [ ! -f "$BASELINE_FILE" ]; then
        echo "$SKILL_COUNT" > "$BASELINE_FILE"
        echo "   - 基线已创建"
    else
        BASELINE_COUNT=$(cat "$BASELINE_FILE")
        if [ "$SKILL_COUNT" -lt "$BASELINE_COUNT" ]; then
            echo "   - ⚠️ Skills 数量减少: $BASELINE_COUNT -> $SKILL_COUNT"
        fi
    fi
else
    echo "❌ Skills 目录不存在!"
fi

echo "----------------"

# 0.5. Channels 检查
CONFIG_FILE="${HOME}/.openclaw/openclaw.json"
if [ -f "$CONFIG_FILE" ]; then
    # 统计启用的 channels（更精确的方式）
    ENABLED_CHANNELS=$(python3 -c "import json; c=json.load(open('${CONFIG_FILE}')); print(len(c.get('channels',{})))" 2>/dev/null || echo "N/A")
    echo "✅ Channels: $ENABLED_CHANNELS 个已启用"

    # 检查 extensions 目录
    EXTENSIONS_DIR="${HOME}/.openclaw/extensions"
    if [ -d "$EXTENSIONS_DIR" ]; then
        EXT_COUNT=$(ls -d "$EXTENSIONS_DIR"/*/ 2>/dev/null | wc -l)
        echo "   - Extensions: $EXT_COUNT 个"
    fi
else
    echo "⚠️ 配置文件不存在"
fi

echo "----------------"

# 检测环境信息
if command -v pnpm &> /dev/null; then
    PM="pnpm"
elif command -v npm &> /dev/null; then
    PM="npm"
else
    PM="unknown"
fi
echo "🔧 包管理器: $PM"

echo "----------------"

# 检测 openclaw 命令 - 优先使用本地项目
OC_CMD=""
if [ -f "${HOME}/openclaw-cn/openclaw.mjs" ]; then
    OC_CMD="node ${HOME}/openclaw-cn/openclaw.mjs"
elif command -v openclaw &> /dev/null; then
    OC_CMD="openclaw"
fi

if [ -z "$OC_CMD" ]; then
    echo "   -> 未找到 openclaw"
fi

# 1. Gateway 状态
if [ -z "$OC_CMD" ]; then
    echo "⚠️ openclaw 命令未找到，请检查安装"
else
    echo "Gateway 状态:"
    $OC_CMD gateway status 2>&1 | head -20
fi

# 2. 进程检查
PID=$(pgrep -f "openclaw gateway" | head -1)
if [ -n "$PID" ]; then
    echo "✅ 进程运行中 (PID: $PID)"
elif [ -n "$OC_CMD" ]; then
    echo "❌ 进程未运行"
    echo "🔧 尝试启动 Gateway..."
    $OC_CMD gateway start
    sleep 2
    if pgrep -f "openclaw gateway" > /dev/null; then
        echo "✅ 自救成功！"
    else
        echo "❌ 自救失败，请手动检查"
    fi
fi

# 3. 内存使用
MEM_USAGE=$(free -m | awk 'NR==2{printf "%.0f", $3*100/$2}')
echo "----------------"
echo "内存使用: ${MEM_USAGE}%"

# 4. 磁盘使用
DISK_USAGE=$(df -h / | awk 'NR==2{print $5}' | sed 's/%//')
echo "磁盘使用: ${DISK_USAGE}%"

echo "----------------"
echo "自检完成"
