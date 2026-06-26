#!/bin/bash
# MCP Server 启动脚本示例
#
# 本脚本展示如何配置和启动 Lann MCP Server
# 注意：实际的 lann-mcp-server 需要根据官方文档安装

print_usage() {
    echo "============================================================"
    echo "  Lann MCP Server 启动脚本"
    echo "============================================================"
    echo ""
    echo "使用方法:"
    echo "  ./start_mcp.sh [mode]"
    echo ""
    echo "模式:"
    echo "  stdio          - 本地 stdio 模式（默认）"
    echo "  http           - HTTP streamableHttp 模式"
    echo "  config         - 生成客户端配置文件"
    echo "  help           - 显示此帮助信息"
    echo ""
    echo "环境变量:"
    echo "  API_ENDPOINT   - API Endpoint (默认: https://open.lannlife.com/mcp/book/create)"
    echo "  PORT           - HTTP 服务端口 (默认: 3000)"
    echo "  HOST           - HTTP 服务主机 (默认: localhost)"
    echo ""
}

# 检查依赖
check_dependencies() {
    echo "检查依赖..."

    if ! command -v node &> /dev/null; then
        echo "❌ 未找到 Node.js，请先安装 Node.js 16+"
        echo "   下载地址: https://nodejs.org/"
        exit 1
    fi

    echo "✅ Node.js 版本: $(node --version)"

    if ! command -v npm &> /dev/null; then
        echo "❌ 未找到 npm"
        exit 1
    fi

    echo "✅ npm 版本: $(npm --version)"
}

# 安装 MCP Server
install_mcp_server() {
    echo ""
    echo "安装 lann-mcp-server..."
    echo ""

    # 如果目录不存在，创建项目目录
    if [ ! -d "lann-mcp-server" ]; then
        echo "克隆或下载 lann-mcp-server 到当前目录..."
        echo "注意：请从官方仓库获取 lann-mcp-server 代码"
        echo ""
        echo "示例命令："
        echo "  git clone <repository-url> lann-mcp-server"
        echo "  cd lann-mcp-server"
        echo "  npm install"
        return 1
    fi

    cd lann-mcp-server

    if [ ! -f "package.json" ]; then
        echo "❌ 未找到 package.json，请确认 lann-mcp-server 代码完整"
        return 1
    fi

    npm install
    echo "✅ 依赖安装完成"

    cd ..
}

# 启动 stdio 模式
start_stdio_mode() {
    echo ""
    echo "启动 stdio 模式..."
    echo ""
    echo "stdio 模式通过标准输入输出与客户端通信。"
    echo "通常由 MCP Client 直接启动，不需要手动运行此脚本。"
    echo ""
    echo "客户端配置示例："
    cat <<'EOF'
{
  "mcpServers": {
    "lann-booking": {
      "command": "npx",
      "args": ["-y", "lann-mcp-server"],
      "env": {
        "API_ENDPOINT": "https://open.lannlife.com/mcp/book/create"
      }
    }
  }
}
EOF
}

# 启动 HTTP 模式
start_http_mode() {
    local port=${PORT:-3000}
    local host=${HOST:-localhost}
    local api_endpoint=${API_ENDPOINT:-https://open.lannlife.com/mcp/book/create}

    echo ""
    echo "启动 HTTP streamableHttp 模式..."
    echo ""
    echo "主机: $host"
    echo "端口: $port"
    echo "API Endpoint: $api_endpoint"
    echo ""
    echo "访问地址: http://$host:$port"
    echo ""

    # 设置环境变量并启动服务
    export API_ENDPOINT="$api_endpoint"
    export PORT="$port"
    export HOST="$host"

    if [ -d "lann-mcp-server" ]; then
        cd lann-mcp-server
        npm start
    else
        echo "❌ 未找到 lann-mcp-server 目录"
        echo "   请先安装 MCP Server（运行: $0 install）"
    fi
}

# 生成客户端配置
generate_config() {
    local mode=${1:-stdio}

    echo ""
    echo "生成客户端配置文件..."
    echo ""

    if [ "$mode" = "stdio" ]; then
        cat > mcp-config.json <<EOF
{
  "mcpServers": {
    "lann-booking": {
      "command": "npx",
      "args": ["-y", "lann-mcp-server"],
      "env": {
        "API_ENDPOINT": "https://open.lannlife.com/mcp/book/create"
      }
    }
  }
}
EOF
        echo "✅ 已生成 stdio 模式配置: mcp-config.json"

    elif [ "$mode" = "http" ]; then
        cat > mcp-config.json <<EOF
{
  "mcpServers": {
    "lann-booking": {
      "url": "https://open.lannlife.com/mcp",
      "type": "streamableHttp"
    }
  }
}
EOF
        echo "✅ 已生成 HTTP 模式配置: mcp-config.json"
    fi

    echo ""
    echo "配置内容:"
    cat mcp-config.json
}

# 主函数
main() {
    local mode=${1:-stdio}

    case "$mode" in
        stdio)
            check_dependencies
            start_stdio_mode
            ;;
        http)
            check_dependencies
            start_http_mode
            ;;
        install)
            check_dependencies
            install_mcp_server
            ;;
        config)
            generate_config "stdio"
            echo ""
            generate_config "http"
            ;;
        help|--help|-h)
            print_usage
            ;;
        *)
            echo "❌ 未知模式: $mode"
            echo ""
            print_usage
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@"
