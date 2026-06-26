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