#!/bin/bash
# Mac Clamshell Mode Configuration Tool
# Supports lid-closed operation WITHOUT external display/keyboard/mouse

set -e

echo "🔧 Mac 合盖运行助手 - 配置工具"
echo "================================"
echo ""
echo "💡 特点：无需外接显示器和键鼠，支持纯后台运行模式"
echo ""

# Get system information
MACOS_VERSION=$(sw_vers -productVersion)
ARCH=$(uname -m)

# Detect Mac model
if command -v system_profiler &> /dev/null; then
    MODEL_IDENTIFIER=$(system_profiler SPHardwareDataType | grep "Model Identifier" | awk '{print $3}' | head -n1)
elif [ -f "/System/Library/CoreServices/PlatformSupport.plist" ]; then
    MODEL_IDENTIFIER=$(defaults read /System/Library/CoreServices/PlatformSupport.plist ModelIdentifier 2>/dev/null || echo "Unknown")
else
    MODEL_IDENTIFIER="Unknown"
fi

# Fallback detection
if [[ "$MODEL_IDENTIFIER" == "Unknown" ]]; then
    if [[ "$ARCH" == "x86_64" ]] || [[ "$ARCH" == "arm64" ]]; then
        MODEL_IDENTIFIER="MacBook-Pro"
    fi
fi

echo "检测到 Mac 型号：$MODEL_IDENTIFIER"
echo "macOS 版本：$MACOS_VERSION"

# Check if it's a MacBook
if [[ "$MODEL_IDENTIFIER" == *"MacBook"* ]] || [[ "$MODEL_IDENTIFIER" == "MacBook-Pro" ]] || [[ "$MODEL_IDENTIFIER" == "MacBook-Air" ]] || [[ "$MODEL_IDENTIFIER" == "MacBook" ]]; then
    echo -e "\033[1;32m✅ 检测到 MacBook 型号，支持合盖运行\033[0m"
else
    echo -e "\033[1;33m⚠️  注意：检测到台式机型号，合盖功能可能不适用\033[0m"
    exit 1
fi

# Display current power settings
echo ""
echo "📊 当前电源设置:"
pmset -g | grep -E "(sleep|displaysleep|lidwake|acwake|disablesleep)" || true

# Check if Amphetamine is running
if pgrep -x "Amphetamine" > /dev/null; then
    echo -e "\033[1;32m✅ Amphetamine 正在运行\033[0m"
else
    echo -e "\033[1;33m⚠️  Amphetamine 未运行\033[0m"
fi

# Show configuration options
echo ""
echo "================================"
echo "选择配置模式:"
echo ""
echo "1️⃣  完整合盖模式（需要外接显示器 + 键鼠）"
echo "   - 标准 macOS 合盖模式"
echo "   - 最稳定，最省电"
echo ""
echo "2️⃣  强制合盖运行（无需外接设备）⭐ 推荐"
echo "   - 无需外接显示器"
echo "   - 无需外接键盘/鼠标"
echo "   - 修改系统电源设置"
echo "   - 适合后台跑任务"
echo ""
echo "3️⃣  临时运行模式（使用 caffeinate）"
echo "   - 无需修改系统设置"
echo "   - 临时阻止休眠"
echo "   - 适合短期任务"
echo ""
echo "4️⃣  仅检查状态（不修改设置）"
echo ""
echo "5️⃣  恢复默认设置"
echo ""

read -p "请选择 (1-5): " choice

case $choice in
    1)
        echo ""
        echo "⚙️  配置完整合盖模式..."
        echo ""
        
        # Check if external display is connected
        EXTERNAL_DISPLAYS=$(system_profiler SPDisplaysDataType 2>/dev/null | grep -c "Display Type" || echo "0")
        if [ "$EXTERNAL_DISPLAYS" -gt 1 ]; then
            echo -e "\033[1;32m✓ 检测到外接显示器\033[0m"
        else
            echo -e "\033[1;31m✗ 未检测到外接显示器\033[0m"
            echo "完整合盖模式需要外接显示器才能工作"
            echo "建议选择选项 2（强制合盖运行）"
            exit 1
        fi
        
        # Configure for proper clamshell mode
        if [[ $(echo "$MACOS_VERSION" | cut -d. -f1) -ge 13 ]]; then
            sudo pmset -a disablesleep 0
        fi
        sudo pmset -a lidwake 1
        sudo pmset -a acwake 1
        
        echo -e "\033[1;32m✅ 完整合盖模式配置完成\033[0m"
        echo ""
        echo "使用说明:"
        echo "1. 连接电源适配器"
        echo "2. 连接外接显示器"
        echo "3. 连接外接键盘/鼠标"
        echo "4. 合上笔记本盖子"
        ;;
        
    2)
        echo ""
        echo "⚙️  配置强制合盖运行模式（无需外接设备）..."
        echo ""
        echo "这将修改以下设置:"
        echo "  • 禁止合盖休眠"
        echo "  • 保持系统活跃"
        echo "  • 无需外接显示器/键鼠"
        echo ""
        echo -e "\033[1;33m⚠️  注意:\033[0m"
        echo "  • 建议连接电源适配器使用"
        echo "  • 电池模式下会加快耗电"
        echo "  • 任务完成后建议恢复默认设置"
        echo ""
        
        read -p "输入 'yes' 确认配置：" CONFIRM
        
        if [[ "$CONFIRM" != "yes" ]]; then
            echo -e "\033[1;31m❌ 取消配置\033[0m"
            exit 0
        fi
        
        # Apply settings for lid-closed operation without external display
        if [[ $(echo "$MACOS_VERSION" | cut -d. -f1) -ge 13 ]]; then
            echo "• 启用 disablesleep 模式..."
            sudo pmset -a disablesleep 1
        else
            echo "• 设置睡眠时间为 0..."
            sudo pmset -a sleep 0
            sudo pmset -a disksleep 0
            sudo pmset -a displaysleep 0
        fi
        
        echo "• 配置 lidwake 为 1..."
        sudo pmset -a lidwake 1
        
        echo "• 禁用自动关机..."
        sudo pmset -a autopoweroff 0
        
        echo ""
        echo -e "\033[1;32m✅ 强制合盖运行模式配置完成！\033[0m"
        echo ""
        echo "📋 使用说明:"
        echo "1. 连接电源适配器（推荐）"
        echo "2. 直接合上笔记本盖子"
        echo "3. 系统将继续运行任务"
        echo "4. 需要时开盖即可"
        echo ""
        echo -e "\033[1;33m⚠️  恢复默认设置:\033[0m"
        if [[ $(echo "$MACOS_VERSION" | cut -d. -f1) -ge 13 ]]; then
            echo "  sudo pmset -a disablesleep 0"
        else
            echo "  sudo pmset -a sleep 1"
        fi
        echo "  sudo pmset -a autopoweroff 1"
        ;;
        
    3)
        echo ""
        echo "⚙️  临时运行模式（使用 caffeinate）..."
        echo ""
        echo "caffeinate 命令参数说明:"
        echo "  -d  阻止显示器休眠"
        echo "  -i  阻止系统空闲休眠"
        echo "  -s  阻止系统睡眠"
        echo "  -t  指定超时时间（秒）"
        echo ""
        echo "运行方式:"
        echo ""
        echo "方式 1: 无限期运行（手动停止）"
        echo "  caffeinate -d -i -s"
        echo ""
        echo "方式 2: 指定时间（例如 1 小时）"
        echo "  caffeinate -d -i -s -t 3600"
        echo ""
        echo "方式 3: 阻止直到特定进程结束"
        echo "  caffeinate -w <PID>"
        echo ""
        echo -e "\033[1;36m💡 提示:\033[0m 保持终端窗口打开，然后合盖即可"
        ;;
        
    4)
        echo ""
        echo "📊 当前系统状态:"
        echo ""
        pmset -g
        echo ""
        
        # Check what's preventing sleep
        echo "🔍 阻止休眠的应用:"
        pmset -g assertions | grep -A 20 "Preventing Sleep" || true
        ;;
        
    5)
        echo ""
        echo "⚙️  恢复默认设置..."
        echo ""
        
        read -p "输入 'yes' 确认恢复：" CONFIRM
        
        if [[ "$CONFIRM" != "yes" ]]; then
            echo -e "\033[1;31m❌ 取消恢复\033[0m"
            exit 0
        fi
        
        # Restore default settings
        if [[ $(echo "$MACOS_VERSION" | cut -d. -f1) -ge 13 ]]; then
            echo "• 恢复 disablesleep 为默认值..."
            sudo pmset -a disablesleep 0
        fi
        
        echo "• 恢复睡眠时间为 1..."
        sudo pmset -a sleep 1
        
        echo "• 恢复显示器睡眠为 10..."
        sudo pmset -a displaysleep 10
        
        echo "• 恢复硬盘睡眠为 10..."
        sudo pmset -a disksleep 10
        
        echo "• 启用自动关机..."
        sudo pmset -a autopoweroff 1
        
        echo ""
        echo -e "\033[1;32m✅ 已恢复默认设置\033[0m"
        ;;
        
    *)
        echo -e "\033[1;31m❌ 无效选择\033[0m"
        exit 1
        ;;
esac

echo ""
echo -e "\033[1;32m================================\033[0m"
echo -e "\033[1;32m✅ Mac 合盖运行助手配置完成！\033[0m"
echo -e "\033[1;32m================================\033[0m"
