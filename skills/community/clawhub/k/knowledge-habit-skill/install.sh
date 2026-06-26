#!/bin/bash

# 知识工作习惯追踪器安装脚本

set -e

echo "📚 安装知识工作习惯追踪器..."
echo "================================"

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$SCRIPT_DIR"
TRACKER_DIR="$SKILL_DIR/tracker"

# 检查依赖
echo "📦 检查系统依赖..."
for cmd in node npm bash git; do
    if ! command -v $cmd &> /dev/null; then
        echo "❌ 缺少依赖: $cmd"
        echo "   请安装必要的依赖:"
        echo "   - Node.js 18+ 和 npm: https://nodejs.org/"
        echo "   - Git: https://git-scm.com/"
        exit 1
    fi
done

# 检查Node版本
NODE_VERSION=$(node -v | cut -d'v' -f2)
NODE_MAJOR=$(echo $NODE_VERSION | cut -d'.' -f1)
if [ $NODE_MAJOR -lt 18 ]; then
    echo "⚠️  Node.js版本过低: $NODE_VERSION (需要 >= 18)"
    echo "    请升级Node.js版本"
    exit 1
fi
echo "✅  Node.js版本: $NODE_VERSION"

# 检查npm版本
NPM_VERSION=$(npm -v)
echo "✅  npm版本: $NPM_VERSION"

# 检查源代码
if [ -d "$TRACKER_DIR" ]; then
    echo "✅  检测到已有的tracker目录: $TRACKER_DIR"
    echo "    将使用现有代码，跳过克隆步骤"
else
    echo "📥  未找到tracker目录，需要获取源代码..."
    echo ""
    echo "选项 1: 从GitHub克隆最新版本 (需要网络)"
    echo "选项 2: 手动指定已有源代码路径"
    echo ""
    read -p "请选择 (1 或 2): " choice
    
    case $choice in
        1)
            echo "🌐  从GitHub克隆知识习惯追踪器仓库..."
            git clone https://github.com/puppetcat-fire/knowledge-habit-tracker.git "$TRACKER_DIR"
            if [ $? -ne 0 ]; then
                echo "❌  克隆失败，请检查网络连接和Git配置"
                exit 1
            fi
            echo "✅  克隆完成"
            ;;
        2)
            read -p "请输入已有knowledge-habit-tracker目录的完整路径: " user_path
            if [ ! -d "$user_path" ]; then
                echo "❌  路径不存在或不是目录: $user_path"
                exit 1
            fi
            echo "🔗  创建符号链接..."
            ln -sf "$user_path" "$TRACKER_DIR"
            echo "✅  符号链接创建完成"
            ;;
        *)
            echo "❌  无效选择，安装中止"
            exit 1
            ;;
    esac
fi

# 进入tracker目录安装依赖
echo ""
echo "🔧  正在安装项目依赖..."
cd "$TRACKER_DIR"

# 检查package.json
if [ ! -f "package.json" ]; then
    echo "❌  tracker目录中缺少package.json"
    echo "    请确保源代码完整"
    exit 1
fi

# 安装npm依赖
if [ -f "package-lock.json" ]; then
    echo "📦  使用package-lock.json安装依赖..."
    npm ci --silent 2>/dev/null || npm install --silent
else
    echo "📦  安装npm依赖..."
    npm install --silent
fi

# 检查Electron依赖
if grep -q "electron" package.json; then
    echo "💻  检测到Electron依赖，安装可能需要一些时间..."
    # 继续静默安装
fi

echo "✅  依赖安装完成"

# 创建便捷启动脚本（如果尚未存在）
echo "🚀  创建便捷启动脚本..."

# 启动Web版的脚本
if [ ! -f "$SKILL_DIR/start-web.sh" ]; then
    cat > "$SKILL_DIR/start-web.sh" << 'EOF'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/tracker"
echo "🌐 启动知识习惯追踪器 (Web版)..."
echo "   访问: http://127.0.0.1:3000"
echo "   按 Ctrl+C 停止服务"
npm start
EOF
    chmod +x "$SKILL_DIR/start-web.sh"
fi

# 启动Electron桌面版的脚本
if [ ! -f "$SKILL_DIR/start-desktop.sh" ]; then
    cat > "$SKILL_DIR/start-desktop.sh" << 'EOF'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/tracker"
echo "💻 启动知识习惯追踪器 (Electron桌面版)..."
echo "   主窗口: 完整习惯记录器"
echo "   悬浮窗: 全局置顶计时窗"
echo "   快捷键:"
echo "     - Ctrl+Shift+T: 显示/隐藏悬浮窗"
echo "     - Ctrl+Shift+H: 唤起主窗口"
npm run desktop
EOF
    chmod +x "$SKILL_DIR/start-desktop.sh"
fi

# CLI工具脚本
if [ ! -f "$SKILL_DIR/habit-cli.sh" ]; then
    cat > "$SKILL_DIR/habit-cli.sh" << 'EOF'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRACKER_DIR="$SCRIPT_DIR/tracker"

help() {
    echo "📚 知识习惯追踪器 - 命令行工具"
    echo "使用方法: $0 [命令]"
    echo ""
    echo "命令:"
    echo "  start-web      启动Web版 (http://127.0.0.1:3000)"
    echo "  start-desktop  启动Electron桌面版"
    echo "  status         检查服务状态"
    echo "  backup         导出数据备份"
    echo "  help           显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 start-web"
    echo "  $0 status"
}

case "$1" in
    start-web)
        cd "$TRACKER_DIR"
        npm start
        ;;
    start-desktop)
        cd "$TRACKER_DIR"
        npm run desktop
        ;;
    status)
        echo "📊 知识习惯追踪器状态检查"
        echo "=========================="
        echo "tracker目录: $TRACKER_DIR"
        echo ""
        
        # 检查Node服务是否运行
        if pgrep -f "node.*server\.js" > /dev/null; then
            echo "✅ Web服务: 运行中"
        else
            echo "❌ Web服务: 未运行"
        fi
        
        # 检查Electron是否运行
        if pgrep -f "electron" > /dev/null; then
            echo "✅ Electron桌面版: 运行中"
        else
            echo "❌ Electron桌面版: 未运行"
        fi
        
        # 检查依赖
        echo ""
        echo "📦 依赖检查:"
        if command -v node > /dev/null; then
            echo "✅ Node.js: $(node -v)"
        else
            echo "❌ Node.js: 未安装"
        fi
        
        if command -v npm > /dev/null; then
            echo "✅ npm: $(npm -v)"
        else
            echo "❌ npm: 未安装"
        fi
        ;;
    backup)
        echo "💾 数据备份说明"
        echo "==============="
        echo "知识习惯追踪器使用浏览器localStorage存储数据。"
        echo "备份方法:"
        echo "1. 启动Web版: $0 start-web"
        echo "2. 打开 http://127.0.0.1:3000"
        echo "3. 在界面中点击'导出备份'按钮"
        echo "4. 保存生成的JSON文件"
        ;;
    help|*)
        help
        ;;
esac
EOF
    chmod +x "$SKILL_DIR/habit-cli.sh"
fi

# 创建环境配置示例
if [ ! -f "$SKILL_DIR/.env.example" ]; then
    cat > "$SKILL_DIR/.env.example" << 'EOF'
# 知识习惯追踪器环境配置
# 复制此文件为 .env 并修改配置

# Web服务配置
PORT=3000
HOST=127.0.0.1

# Electron配置
ELECTRON_DISABLE_SECURITY_WARNINGS=false

# 开发模式
NODE_ENV=development
DEBUG=knowledge-habit-tracker:*

# 数据目录
DATA_DIR=./data

# 备份配置
BACKUP_DIR=./backups
BACKUP_RETENTION_DAYS=30
EOF
fi

echo ""
echo "✅ 安装完成!"
echo ""
echo "📋 安装摘要:"
echo "  - tracker目录: $TRACKER_DIR"
echo "  - 技能工具: $SKILL_DIR"
echo "  - Node依赖: 已安装"
echo ""
echo "🚀 可用命令:"
echo "  1. 启动Web版: ./start-web.sh"
echo "  2. 启动桌面版: ./start-desktop.sh"
echo "  3. CLI工具: ./habit-cli.sh [command]"
echo ""
echo "📚 使用指南:"
echo "  - Web版: 在浏览器中打开 http://127.0.0.1:3000"
echo "  - 桌面版: 提供全局悬浮计时窗，快捷键控制"
echo "  - Android覆盖层: 查看 tracker/android-overlay/README.md"
echo ""
echo "🔒 隐私说明:"
echo "  所有习惯数据默认保存在浏览器本地，不会自动上传。"
echo "  只有在你主动启动本地服务时，反馈日志才会写入本机磁盘。"
echo ""
echo "🔄 更新说明:"
echo "  如需更新tracker代码，可进入tracker目录执行: git pull"
echo "  然后重新安装依赖: npm install"
echo ""
echo "================================"