#!/bin/bash
# 安装依赖脚本

echo "🔧 安装初音未来悬浮球依赖..."

# 检查系统包管理器
if command -v apt &> /dev/null; then
    echo "📦 安装 GTK 依赖..."
    sudo apt update
    sudo apt install -y python3-gi python3-gi-cairo gir1.2-gtk-3.0
elif command -v dnf &> /dev/null; then
    echo "📦 安装 GTK 依赖..."
    sudo dnf install -y python3-gobject gtk3
elif command -v pacman &> /dev/null; then
    echo "📦 安装 GTK 依赖..."
    sudo pacman -S --noconfirm python-gobject gtk3
else
    echo "⚠️  未知的包管理器，请手动安装 python3-gi 和 gtk3"
fi

# 安装 Python 依赖
echo "🐍 安装 Python 包..."
pip3 install psutil pillow --break-system-packages 2>/dev/null || pip3 install psutil pillow

echo ""
echo "✅ 安装完成！"
echo ""
echo "启动方法:"
echo "  python3 scripts/hatsune-ball.py"
