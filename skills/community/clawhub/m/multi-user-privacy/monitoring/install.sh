#!/bin/bash

# OpenClaw 监控告警系统安装脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="$HOME/.openclaw/workspace"
MONITORING_DIR="$WORKSPACE/monitoring"

echo "🔧 OpenClaw 监控告警系统安装"
echo "═══════════════════════════════════════"

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 错误：未找到 Node.js，请先安装 Node.js"
    exit 1
fi

echo "✅ Node.js 版本：$(node -v)"

# 创建目录
echo ""
echo "📁 创建监控目录..."
mkdir -p "$MONITORING_DIR"
mkdir -p "$WORKSPACE/logs"

# 复制文件
echo "📋 复制配置文件..."
if [ -f "$SCRIPT_DIR/alert-config.json" ]; then
    cp "$SCRIPT_DIR/alert-config.json" "$MONITORING_DIR/"
    echo "   ✅ 配置文件已复制"
else
    echo "   ⚠️  配置文件不存在，将使用默认配置"
fi

if [ -f "$SCRIPT_DIR/monitor.js" ]; then
    cp "$SCRIPT_DIR/monitor.js" "$MONITORING_DIR/"
    chmod +x "$MONITORING_DIR/monitor.js"
    echo "   ✅ 监控脚本已复制"
else
    echo "   ❌ 监控脚本不存在"
    exit 1
fi

# 配置 systemd 服务（可选）
echo ""
echo "⚙️  配置系统服务..."

if command -v systemctl &> /dev/null; then
    echo "   检测到 systemd，配置自动启动..."
    
    # 复制服务文件
    if [ -f "$SCRIPT_DIR/openclaw-monitor.service" ]; then
        sudo cp "$SCRIPT_DIR/openclaw-monitor.service" "/etc/systemd/system/openclaw-monitor@.service"
        echo "   ✅ 服务文件已复制"
        
        # 重新加载 systemd
        sudo systemctl daemon-reload
        
        # 启用服务（但不启动，让用户手动启动）
        sudo systemctl enable "openclaw-monitor@$(whoami).service" 2>/dev/null || true
        echo "   ✅ 服务已启用（开机自启）"
    fi
else
    echo "   ℹ️  未检测到 systemd，跳过服务配置"
fi

# 测试运行
echo ""
echo "🧪 测试监控系统..."
cd "$MONITORING_DIR"
if node monitor.js check > /dev/null 2>&1; then
    echo "   ✅ 监控检查成功"
else
    echo "   ⚠️  监控检查失败，请检查配置"
fi

# 显示状态
echo ""
echo "📊 当前监控状态:"
node monitor.js status

# 完成
echo ""
echo "═══════════════════════════════════════"
echo "✅ 安装完成！"
echo ""
echo "📖 使用方法:"
echo "   cd $MONITORING_DIR"
echo "   node monitor.js check    # 执行一次检查"
echo "   node monitor.js status   # 查看状态"
echo "   node monitor.js start    # 启动监控服务"
echo ""
echo "📝 查看文档:"
echo "   cat $MONITORING_DIR/README.md"
echo ""

if command -v systemctl &> /dev/null; then
    echo "🔧 系统服务管理:"
    echo "   sudo systemctl start openclaw-monitor@$(whoami).service"
    echo "   sudo systemctl status openclaw-monitor@$(whoami).service"
    echo "   sudo systemctl stop openclaw-monitor@$(whoami).service"
    echo ""
fi

echo "🎉 祝使用愉快！"
