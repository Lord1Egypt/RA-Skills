#!/bin/bash
# Memory Plus Sync 2.0 环境设置脚本

echo "=========================================="
echo "Memory Plus Sync 2.0 环境设置"
echo "=========================================="

# 检查 Python 环境
echo "1. 检查 Python 环境..."
python3 --version
if [ $? -eq 0 ]; then
    echo "✅ Python 3 已安装"
else
    echo "❌ Python 3 未安装"
    exit 1
fi

# 检查依赖
echo ""
echo "2. 检查依赖..."
REQUIRED_PACKAGES=("watchdog" "fastapi" "uvicorn" "pydantic" "requests" "pyyaml")
for pkg in "${REQUIRED_PACKAGES[@]}"; do
    python3 -c "import $pkg" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "✅ $pkg 已安装"
    else
        echo "⚠️  $pkg 未安装，正在安装..."
        pip3 install $pkg
    fi
done

# 设置环境变量
echo ""
echo "3. 设置环境变量..."
export MEMORY_PLUS_WORKSPACE="$HOME/.openclaw/workspace/memory-plus"
export MEMORY_PLUS_DB="$HOME/.openclaw/memory/main.sqlite"
export MEMORY_PLUS_CONFIG="$HOME/.hermes/skills/openclaw-imports/memory-plus-sync/config.yaml"

echo "   MEMORY_PLUS_WORKSPACE=$MEMORY_PLUS_WORKSPACE"
echo "   MEMORY_PLUS_DB=$MEMORY_PLUS_DB"
echo "   MEMORY_PLUS_CONFIG=$MEMORY_PLUS_CONFIG"

# 创建必要的目录
echo ""
echo "4. 创建必要的目录..."
mkdir -p "$HOME/.openclaw/workspace/memory-plus/storage/l1"
mkdir -p "$HOME/.openclaw/workspace/memory-plus/storage/l2"
mkdir -p "$HOME/.openclaw/workspace/memory-plus/storage/l3"
mkdir -p "$HOME/.openclaw/workspace/memory-plus/logs"
mkdir -p "$HOME/.openclaw/workspace/memory-plus/metrics"

echo "✅ 目录创建完成"

# 测试数据库连接
echo ""
echo "5. 测试数据库连接..."
if [ -f "$MEMORY_PLUS_DB" ]; then
    echo "✅ 数据库文件存在: $MEMORY_PLUS_DB"
    DB_SIZE=$(du -h "$MEMORY_PLUS_DB" | cut -f1)
    echo "   数据库大小: $DB_SIZE"
else
    echo "⚠️  数据库文件不存在: $MEMORY_PLUS_DB"
    echo "   将使用默认配置创建新数据库"
fi

# 生成环境配置文件
echo ""
echo "6. 生成环境配置文件..."
ENV_FILE="$HOME/.hermes/skills/openclaw-imports/memory-plus-sync/.env"
cat > "$ENV_FILE" << EOF
# Memory Plus Sync 2.0 环境配置
# 生成时间: $(date)

# 路径配置
MEMORY_PLUS_WORKSPACE=$MEMORY_PLUS_WORKSPACE
MEMORY_PLUS_DB=$MEMORY_PLUS_DB
MEMORY_PLUS_CONFIG=$MEMORY_PLUS_CONFIG

# MCP 服务器配置
MCP_SERVER_HOST=0.0.0.0
MCP_SERVER_PORT=8000
MCP_SERVER_WORKERS=2

# 记忆系统配置
MEMORY_SYNC_ENABLED=true
MEMORY_SYNC_CHANNELS=feishu,voice
MEMORY_SYNC_HOURS=24

# 监控配置
MONITOR_ENABLED=true
MONITOR_INTERVAL=60
ALERT_ON_STALE=true
STALE_THRESHOLD_HOURS=1

# 三代理配置（可选）
# KIMI_API_KEY=your_kimi_api_key_here
# BAILIAN_API_KEY=your_bailian_api_key_here
EOF

echo "✅ 环境配置文件已生成: $ENV_FILE"

echo ""
echo "=========================================="
echo "环境设置完成！"
echo "=========================================="
echo ""
echo "下一步操作:"
echo "1. 启动 MCP 服务器:"
echo "   cd ~/.hermes/skills/openclaw-imports/memory-plus-sync"
echo "   python mcp_server.py"
echo ""
echo "2. 测试基本功能:"
echo "   python main.py health"
echo "   python main.py sync"
echo "   python main.py monitor"
echo ""
echo "3. 运行完整测试:"
echo "   python test_full_workflow.py"
echo ""
echo "4. 查看文档:"
echo "   cat README.md"
echo "   cat SKILL.md"