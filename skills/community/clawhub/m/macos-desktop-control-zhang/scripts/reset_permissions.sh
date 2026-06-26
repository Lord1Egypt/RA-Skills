#!/bin/bash
# 权限重置和授权脚本
# 用法：sudo bash reset_permissions.sh

echo "🔐 macOS 权限重置工具"
echo ""
echo "⚠️  此脚本将重置终端相关权限，然后需要手动重新授权"
echo ""

# 检查是否 root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ 请使用 sudo 运行："
    echo "   sudo bash $0"
    exit 1
fi

# 重置权限
echo "正在重置权限..."
echo ""

echo "1. 重置辅助功能权限..."
tccutil reset Accessibility com.apple.Terminal
tccutil reset Accessibility com.microsoft.VSCode
tccutil reset Accessibility org.alacritty
tccutil reset Accessibility com.googlecode.iterm2

echo "2. 重置自动化权限..."
tccutil reset AppleEvents com.apple.Terminal
tccutil reset AppleEvents com.microsoft.VSCode
tccutil reset AppleEvents org.alacritty
tccutil reset AppleEvents com.googlecode.iterm2

echo "3. 重置屏幕录制权限..."
tccutil reset ScreenCapture com.apple.Terminal
tccutil reset ScreenCapture com.microsoft.VSCode
tccutil reset ScreenCapture org.alacritty
tccutil reset ScreenCapture com.googlecode.iterm2

echo ""
echo "✅ 权限重置完成！"
echo ""
echo "📋 下一步："
echo "1. 完全退出所有终端应用（Cmd+Q）"
echo "2. 重新打开设置页面进行授权"
echo "3. 授权后重启终端应用"
echo ""
echo "是否现在打开设置页面？(y/n)"
read -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # 以当前用户身份打开设置
    sudo -u "$SUDO_USER" open "x-apple.systempreferences:com.apple.preference.security"
fi
