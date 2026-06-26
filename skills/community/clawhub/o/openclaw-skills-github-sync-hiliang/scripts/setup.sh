#!/bin/bash

# OpenClaw Skills GitHub Sync - Interactive Setup for Linux/Mac

echo "=========================================="
echo "OpenClaw Skills GitHub Sync - 交互式配置向导"
echo "=========================================="
echo ""

# Check GitHub CLI
if ! command -v gh &> /dev/null; then
    echo "GitHub CLI 未安装"
    echo "请先安装:"
    echo "  Linux: sudo apt install gh"
    echo "  Mac: brew install gh"
    exit 1
fi

echo "1. GitHub 登录状态检查..."
if gh auth status &> /dev/null; then
    echo "   已登录 GitHub"
else
    echo "   请先登录 GitHub"
    echo "   运行: gh auth login"
    exit 1
fi

echo ""
echo "2. 设置私有 Skills 本地路径"
echo "   示例: ~/openclaw-skills-private"
read -p "   输入路径: " private_path

echo ""
echo "3. 设置公开 Skills 本地路径"
echo "   示例: ~/openclaw-skills-public"
read -p "   输入路径: " public_path

echo ""
echo "=========================================="
echo "配置完成！"
echo "=========================================="
echo ""
echo "私有 Skills: $private_path"
echo "公开 Skills: $public_path"
echo ""

# Save config
config_file="$(dirname "$0")/config.sh"

cat > "$config_file" << EOF
PRIVATE_PATH="$private_path"
PUBLIC_PATH="$public_path"
EOF

echo "配置已保存到: $config_file"

# Check Git repos
echo ""
echo "检查 Git 仓库..."

if [ -d "$private_path" ]; then
    cd "$private_path"
    if [ ! -d ".git" ]; then
        echo "   私有仓库未初始化，正在创建..."
        git init
        git config user.email "your@email.com"
        git config user.name "Your Name"
        echo "   请手动添加 remote: git remote add origin https://github.com/YOUR_USERNAME/your-repo.git"
    fi
fi

if [ -d "$public_path" ]; then
    cd "$public_path"
    if [ ! -d ".git" ]; then
        echo "   公开仓库未初始化，正在创建..."
        git init
        git config user.email "your@email.com"
        git config user.name "Your Name"
        echo "   请手动添加 remote: git remote add origin https://github.com/YOUR_USERNAME/your-repo.git"
    fi
fi

echo ""
echo "运行同步: bash $(dirname "$0")/sync.sh"
