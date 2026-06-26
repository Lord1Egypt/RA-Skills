#!/bin/bash
#
# hermes-memory-bridge / install_v2.sh
# Hermes-WorkBuddy 事件驱动架构 v2.0 部署脚本
#
# 用法：
#   bash install_v2.sh          # 安装到 ~/.hermes/shared/（默认）
#   bash install_v2.sh /path/to  # 指定 Hermes 根目录
#
# 执行内容：
#   1. 创建必要的目录结构
#   2. 设置文件权限
#   3. 配置 launchd 守护进程（macOS）
#   4. 验证安装
#

set -e

HERMES_HOME="${1:-$HOME/.hermes}"
SHARED_DIR="$HERMES_HOME/shared"
SIGNAL_DIR="$SHARED_DIR/signals"
QUEUE_DIR="$SHARED_DIR/queue"
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "========================================"
echo "  Hermes-WorkBuddy v2.0 安装脚本"
echo "========================================"
echo "Hermes 目录: $HERMES_HOME"
echo ""

# ─── 1. 创建目录 ───────────────────────────────────────────────────
echo "📁 创建目录结构..."
mkdir -p "$SIGNAL_DIR"
mkdir -p "$QUEUE_DIR"
mkdir -p "$SHARED_DIR/feedback"
mkdir -p "$HERMES_HOME/memories"
echo "   ✅ $SIGNAL_DIR"
echo "   ✅ $QUEUE_DIR"
echo "   ✅ $SHARED_DIR/feedback"
echo "   ✅ $HERMES_HOME/memories"

# ─── 2. 复制/链接事件驱动模块到 Hermes 侧 ─────────────────────────
echo ""
echo "📦 部署事件驱动模块到 Hermes 侧..."
cp "$SKILL_DIR/event_signaler.py" "$HERMES_HOME/event_signaler.py"
cp "$SKILL_DIR/communication_queue.py" "$HERMES_HOME/communication_queue.py"
cp "$SKILL_DIR/task_processor.py" "$HERMES_HOME/task_processor.py"
cp "$SKILL_DIR/feedback_writer.py" "$HERMES_HOME/feedback_writer.py"
chmod +x "$HERMES_HOME/event_signaler.py"
echo "   ✅ event_signaler.py    → $HERMES_HOME/"
echo "   ✅ communication_queue.py → $HERMES_HOME/"
echo "   ✅ task_processor.py    → $HERMES_HOME/"
echo "   ✅ feedback_writer.py   → $HERMES_HOME/"

# ─── 3. 创建 Hermes 环境变量配置（可选）────────────────────────────
echo ""
echo "⚙️  配置环境变量..."
ENV_FILE="$HERMES_HOME/.env"
if [ -f "$ENV_FILE" ]; then
    echo "   ℹ️  $ENV_FILE 已存在，跳过"
else
    cat > "$ENV_FILE" << 'EOF'
# Hermes-WorkBuddy Bridge v2.0 环境变量
# 由 install_v2.sh 自动生成

# Hermes 根目录（通常无需修改）
HERMES_HOME=~/.hermes

# WorkBuddy 根目录
WORKBUDDY_HOME=~/WorkBuddy

# 桥接日志级别：DEBUG | INFO | WARNING | ERROR
BRIDGE_LOG_LEVEL=INFO

# 信号/队列文件保留时长（秒）
SIGNAL_TTL=21600
QUEUE_TTL=604800
EOF
    echo "   ✅ $ENV_FILE"
fi

# ─── 4. 配置 launchd 守护进程（macOS）─────────────────────────────
echo ""
echo "🚀 配置守护进程（macOS launchd）..."

LAUNCHD_DIR="$HOME/Library/LaunchAgents"
PLIST_NAME="com.workbuddy.hermes-watcher.plist"
PLIST_PATH="$LAUNCHD_DIR/$PLIST_NAME"

mkdir -p "$LAUNCHD_DIR"

cat > "$PLIST_PATH" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.workbuddy.hermes-watcher</string>

    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>${SKILL_DIR}/event_watcher.py</string>
    </array>

    <key>WorkingDirectory</key>
    <string>${SHARED_DIR}</string>

    <key>EnvironmentVariables</key>
    <dict>
        <key>BRIDGE_LOG_LEVEL</key>
        <string>INFO</string>
    </dict>

    <key>RunAtLoad</key>
    <true/>

    <key>KeepAlive</key>
    <true/>

    <key>StandardOutPath</key>
    <string>/tmp/hermes-watcher.log</string>

    <key>StandardErrorPath</key>
    <string>/tmp/hermes-watcher.err</string>

    <key>ProcessType</key>
    <string>Background</string>
</dict>
</plist>
EOF

echo "   ✅ $PLIST_PATH"
echo "   ℹ️  启动守护进程：launchctl load $PLIST_PATH"
echo "   ℹ️  停止守护进程：launchctl unload $PLIST_PATH"

# ─── 5. 验证安装 ───────────────────────────────────────────────────
echo ""
echo "🔍 验证安装..."
ERRORS=0

for f in "$SIGNAL_DIR" "$QUEUE_DIR" "$SHARED_DIR/feedback" "$HERMES_HOME/memories" \
         "$HERMES_HOME/event_signaler.py" "$HERMES_HOME/communication_queue.py" \
         "$HERMES_HOME/task_processor.py" "$HERMES_HOME/feedback_writer.py"; do
    if [ -e "$f" ]; then
        echo "   ✅ $f"
    else
        echo "   ❌ 缺失: $f"
        ERRORS=$((ERRORS + 1))
    fi
done

# ─── 6. 完成 ──────────────────────────────────────────────────────
echo ""
echo "========================================"
if [ $ERRORS -eq 0 ]; then
    echo "  ✅ 安装完成！"
else
    echo "  ⚠️  安装完成，但有 $ERRORS 个问题"
fi
echo "========================================"
echo ""
echo "下一步："
echo "  1. 启动守护进程（WorkBuddy 后台任务处理器）："
echo "     launchctl load $PLIST_PATH"
echo ""
echo "  2. 测试信号发射（从 Hermes）："
echo "     python3 $HERMES_HOME/event_signaler.py emit task_done '测试信号'"
echo ""
echo "  3. 测试命令任务（让 WorkBuddy 执行命令）："
echo "     python3 $HERMES_HOME/event_signaler.py send_task echo '{\"message\":\"ping\"}'"
echo ""
echo "  4. 轮询 WorkBuddy 处理结果："
echo "     python3 $HERMES_HOME/event_signaler.py feedback"
echo ""
echo "  5. 查看信号统计："
echo "     python3 $HERMES_HOME/event_signaler.py stats"
echo ""
echo "  6. 查看 WorkBuddy 守护日志："
echo "     tail -f /tmp/hermes-watcher.log"
echo ""
