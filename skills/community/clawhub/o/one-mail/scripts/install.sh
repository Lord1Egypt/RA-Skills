#!/bin/bash
# one-mail 安装脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="/usr/local/bin"

echo "🔧 one-mail 安装"
echo "==============="
echo ""

# 检查权限
if [ ! -w "$INSTALL_DIR" ]; then
    echo "⚠️  需要 sudo 权限安装到 $INSTALL_DIR"
    USE_SUDO="sudo"
else
    USE_SUDO=""
fi

# 创建符号链接
echo "创建符号链接: $INSTALL_DIR/onemail -> $SCRIPT_DIR/onemail"
$USE_SUDO ln -sf "$SCRIPT_DIR/onemail" "$INSTALL_DIR/onemail"

# 验证安装
if command -v onemail &> /dev/null; then
    echo "✅ 安装成功！"
    echo ""
    echo "现在可以使用以下命令:"
    echo "  onemail setup      # 初始化配置"
    echo "  onemail fetch      # 收取邮件"
    echo "  onemail send       # 发送邮件"
    echo "  onemail accounts   # 账户管理"
    echo "  onemail stats      # 邮件统计"
    echo "  onemail help       # 查看帮助"
    echo ""
    echo "快速开始:"
    echo "  onemail setup"
else
    echo "❌ 安装失败"
    exit 1
fi
