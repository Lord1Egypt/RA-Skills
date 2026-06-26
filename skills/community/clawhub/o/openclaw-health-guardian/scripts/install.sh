#!/bin/bash
# OpenClaw Health Guardian - 一键安装脚本
# 功能：自动部署 OpenClaw 健康守护方案（含冷却机制和限流保护）

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查系统
if [[ "$OSTYPE" != "darwin"* ]]; then
    log_error "本脚本仅支持 macOS 系统"
    exit 1
fi

# 获取用户目录
USER_HOME="$HOME"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

log_info "开始安装 OpenClaw Health Guardian..."
log_info "安装目录: $USER_HOME/.openclaw"

# 1. 创建必要目录
log_info "创建目录结构..."
mkdir -p "$USER_HOME/.openclaw/scripts"
mkdir -p "$USER_HOME/.openclaw/state"
mkdir -p "$USER_HOME/.openclaw/logs"

# 2. 复制健康检查脚本
log_info "安装健康检查脚本..."
if [ -f "$SCRIPT_DIR/openclaw-health-check.sh" ]; then
    cp "$SCRIPT_DIR/openclaw-health-check.sh" "$USER_HOME/.openclaw/scripts/"
    chmod +x "$USER_HOME/.openclaw/scripts/openclaw-health-check.sh"
else
    log_error "找不到脚本文件: openclaw-health-check.sh"
    exit 1
fi

# 3. 创建 LaunchAgent
log_info "配置 LaunchAgent 服务..."
LAUNCH_AGENT_DIR="$USER_HOME/Library/LaunchAgents"
mkdir -p "$LAUNCH_AGENT_DIR"

# 使用变量直接注入，避免硬编码
cat > "$LAUNCH_AGENT_DIR/com.openclaw.healthcheck.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.openclaw.healthcheck</string>
    <key>ProgramArguments</key>
    <array>
        <string>$USER_HOME/.openclaw/scripts/openclaw-health-check.sh</string>
    </array>
    <key>StartInterval</key>
    <integer>300</integer>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>$USER_HOME/.openclaw/logs/health-check-daemon.log</string>
    <key>StandardErrorPath</key>
    <string>$USER_HOME/.openclaw/logs/health-check-daemon-error.log</string>
    <key>KeepAlive</key>
    <dict>
        <key>Crashed</key>
        <true/>
        <key>NonEmpty</key>
        <false/>
    </dict>
    <key>ProcessType</key>
    <string>Background</string>
    <key>ThrottleInterval</key>
    <integer>60</integer>
</dict>
</plist>
EOF

# 4. 加载并启动服务
log_info "加载健康检查服务..."
launchctl unload "$LAUNCH_AGENT_DIR/com.openclaw.healthcheck.plist" 2>/dev/null || true
sleep 1
launchctl load "$LAUNCH_AGENT_DIR/com.openclaw.healthcheck.plist"

# 5. 验证安装
log_info "验证安装..."
sleep 2

if launchctl list | grep -q "com.openclaw.healthcheck"; then
    PID=$(launchctl list | grep "com.openclaw.healthcheck" | awk '{print $1}')
    log_info "✅ 健康检查服务已启动 (PID: $PID)"
else
    log_warn "⚠️ 服务可能未正确加载，请手动检查"
fi

if [ -f "$USER_HOME/.openclaw/scripts/openclaw-health-check.sh" ]; then
    log_info "✅ 健康检查脚本已安装"
else
    log_error "❌ 脚本安装失败"
    exit 1
fi

# 6. 显示信息
echo ""
echo "========================================"
echo "  OpenClaw Health Guardian 安装完成"
echo "========================================"
echo ""
echo "📁 安装位置:"
echo "   脚本: $USER_HOME/.openclaw/scripts/openclaw-health-check.sh"
echo "   日志: $USER_HOME/.openclaw/logs/health-check.log"
echo "   状态: $USER_HOME/.openclaw/state/"
echo ""
echo "⚙️  配置参数:"
echo "   检查间隔: 5分钟"
echo "   冷却时间: 180秒"
echo "   每小时限流: 5次"
echo ""
echo "🔧 常用命令:"
echo "   查看日志: tail -f ~/.openclaw/logs/health-check.log"
echo "   手动检查: bash ~/.openclaw/scripts/openclaw-health-check.sh"
echo "   停止服务: launchctl unload ~/Library/LaunchAgents/com.openclaw.healthcheck.plist"
echo "   启动服务: launchctl load ~/Library/LaunchAgents/com.openclaw.healthcheck.plist"
echo "   查看状态: launchctl list | grep openclaw"
echo ""
echo "📊 首次检查将在 5 分钟内自动执行"
echo ""
log_info "安装完成！"
