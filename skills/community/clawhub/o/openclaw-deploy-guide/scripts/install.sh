#!/bin/bash
# OpenClaw 一键安装脚本
# 支持 macOS、Linux

set -e

REPO="Markovmodcn/openclaw-china"
INSTALL_DIR="$HOME/.nexusbot"

echo "🚀 OpenClaw (NEUXSBOT) 安装脚本"
echo "================================"
echo ""

# 检测操作系统
OS=$(uname -s)
ARCH=$(uname -m)

echo "📋 系统信息:"
echo "  OS: $OS"
echo "  Arch: $ARCH"
echo ""

# 检查依赖
check_dependencies() {
    echo "🔍 检查依赖..."

    if ! command -v curl &> /dev/null; then
        echo "❌ 未找到 curl，请先安装"
        exit 1
    fi

    echo "  ✅ curl 已安装"
}

# macOS 安装
install_macos() {
    echo "🍎 检测到 macOS"
    echo ""

    # 检查是否已安装
    if [ -d "/Applications/NEUXSBOT.app" ]; then
        echo "⚠️  检测到已安装 NEUXSBOT"
        read -p "是否重新安装? (y/N): " confirm
        if [[ $confirm != [yY] ]]; then
            echo "取消安装"
            exit 0
        fi
    fi

    # 下载 DMG
    echo "📥 下载安装包..."
    DOWNLOAD_URL="https://github.com/${REPO}/releases/latest/download/NEUXSBOT.dmg"
    TEMP_DMG="/tmp/NEUXSBOT.dmg"

    curl -L -o "$TEMP_DMG" "$DOWNLOAD_URL"

    echo "📦 挂载 DMG..."
    MOUNT_POINT=$(hdiutil attach "$TEMP_DMG" | grep "Volumes" | awk '{print $3}')

    echo "📋 安装应用..."
    cp -R "$MOUNT_POINT/NEUXSBOT.app" /Applications/

    echo "🔧 卸载 DMG..."
    hdiutil detach "$MOUNT_POINT"
    rm "$TEMP_DMG"

    echo "✅ 安装完成！"
    echo ""
    echo "🚀 启动方式:"
    echo "  1. 在 Applications 中找到 NEUXSBOT"
    echo "  2. 右键点击 → 打开（首次运行）"
    echo "  或运行: open /Applications/NEUXSBOT.app"
}

# Linux 安装
install_linux() {
    echo "🐧 检测到 Linux"
    echo ""

    # 检测发行版
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        DISTRO=$ID
    else
        echo "❌ 无法检测发行版"
        exit 1
    fi

    echo "  发行版: $DISTRO"
    echo ""

    case $DISTRO in
        ubuntu|debian)
            install_deb
            ;;
        centos|rhel|fedora)
            echo "⚠️  请手动下载 RPM 包安装"
            echo "下载地址: https://github.com/${REPO}/releases/latest"
            ;;
        *)
            echo "⚠️  使用通用安装方式"
            install_generic
            ;;
    esac
}

# Debian/Ubuntu 安装
install_deb() {
    echo "📦 使用 DEB 包安装"
    echo ""

    # 下载
    echo "📥 下载安装包..."
    DOWNLOAD_URL="https://github.com/${REPO}/releases/latest/download/nexusbot_amd64.deb"
    TEMP_DEB="/tmp/nexusbot_amd64.deb"

    curl -L -o "$TEMP_DEB" "$DOWNLOAD_URL"

    # 安装
    echo "📋 安装..."
    sudo dpkg -i "$TEMP_DEB" || {
        echo "🔧 修复依赖..."
        sudo apt-get install -f -y
    }

    rm "$TEMP_DEB"

    echo "✅ 安装完成！"
    echo ""
    echo "🚀 启动方式:"
    echo "  命令行: nexusbot"
    echo "  或: sudo systemctl start nexusbot"
}

# 通用安装
install_generic() {
    echo "📦 使用通用脚本安装"
    echo ""

    # 创建安装目录
    mkdir -p "$INSTALL_DIR"

    # 下载最新 release
    echo "📥 下载最新版本..."
    LATEST_URL=$(curl -s "https://api.github.com/repos/${REPO}/releases/latest" | grep "browser_download_url.*linux.*tar.gz" | cut -d '"' -f 4)

    if [ -z "$LATEST_URL" ]; then
        echo "❌ 无法找到下载地址"
        exit 1
    fi

    TEMP_TAR="/tmp/nexusbot-linux.tar.gz"
    curl -L -o "$TEMP_TAR" "$LATEST_URL"

    # 解压
    echo "📦 解压..."
    tar -xzf "$TEMP_TAR" -C "$INSTALL_DIR" --strip-components=1
    rm "$TEMP_TAR"

    # 创建软链接
    sudo ln -sf "$INSTALL_DIR/nexusbot" /usr/local/bin/nexusbot

    echo "✅ 安装完成！"
    echo ""
    echo "🚀 启动方式:"
    echo "  命令行: nexusbot"
}

# 配置向导
setup_config() {
    echo ""
    echo "⚙️  配置向导"
    echo "==========="
    echo ""

    CONFIG_FILE="$HOME/.nexusbot/config.yaml"
    mkdir -p "$HOME/.nexusbot"

    # 检查是否已有配置
    if [ -f "$CONFIG_FILE" ]; then
        read -p "检测到已有配置，是否重新配置? (y/N): " reconfig
        if [[ $reconfig != [yY] ]]; then
            return
        fi
    fi

    # AI 模型选择
    echo "🤖 选择 AI 模型:"
    echo "  1) 本地模型 (Ollama) - 推荐"
    echo "  2) DeepSeek (在线)"
    echo "  3) Kimi (在线)"
    echo "  4) 跳过配置"

    read -p "请选择 (1-4): " ai_choice

    case $ai_choice in
        1)
            setup_ollama
            ;;
        2)
            read -p "输入 DeepSeek API Key: " api_key
            cat > "$CONFIG_FILE" << EOF
ai:
  provider: deepseek
  deepseek:
    api_key: $api_key
    model: deepseek-chat
EOF
            ;;
        3)
            read -p "输入 Kimi API Key: " api_key
            cat > "$CONFIG_FILE" << EOF
ai:
  provider: kimi
  kimi:
    api_key: $api_key
    model: moonshot-v1-8k
EOF
            ;;
        4)
            echo "⏭️  跳过配置"
            ;;
    esac

    echo "✅ 配置已保存到 $CONFIG_FILE"
}

# 设置 Ollama
setup_ollama() {
    echo ""
    echo "🔧 配置 Ollama"

    # 检查是否已安装
    if ! command -v ollama &> /dev/null; then
        echo "📥 安装 Ollama..."
        curl -fsSL https://ollama.com/install.sh | sh
    fi

    # 拉取模型
    echo "📥 下载模型 (qwen2.5:7b)..."
    ollama pull qwen2.5:7b

    # 创建配置
    cat > "$HOME/.nexusbot/config.yaml" << EOF
ai:
  provider: ollama
  ollama:
    host: http://localhost:11434
    model: qwen2.5:7b
    temperature: 0.7
EOF

    echo "✅ Ollama 配置完成"
    echo "   模型: qwen2.5:7b"
    echo "   启动命令: ollama serve"
}

# 主流程
main() {
    check_dependencies

    case $OS in
        Darwin)
            install_macos
            ;;
        Linux)
            install_linux
            ;;
        *)
            echo "❌ 不支持的操作系统: $OS"
            exit 1
            ;;
    esac

    setup_config

    echo ""
    echo "🎉 安装完成！"
    echo ""
    echo "📚 下一步:"
    echo "  1. 启动应用"
    echo "  2. 配置消息平台 (钉钉/飞书/企微)"
    echo "  3. 开始使用"
    echo ""
    echo "📖 文档: https://www.neuxsbot.com/docs"
    echo "🐛 反馈: https://github.com/Markovmodcn/openclaw-china/issues"
}

main "$@"
