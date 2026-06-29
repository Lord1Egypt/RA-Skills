#!/bin/bash
# Platform Monitor - macOS/Linux 一键安装脚本
# 用法: bash install.sh

echo "🚀 Platform Monitor - 安装向导"
echo "=========================================="
echo ""

# 1. 检查 Node.js
echo "【1/5】检查 Node.js..."
if ! command -v node &> /dev/null; then
    echo "  ❌ 未找到 Node.js，请先安装: https://nodejs.org/"
    echo "  macOS: brew install node"
    echo "  Ubuntu: sudo apt install nodejs npm"
    exit 1
fi
NODE_VERSION=$(node --version)
echo "  ✅ Node.js $NODE_VERSION 已安装"
echo ""

# 2. 安装依赖
echo "【2/5】安装依赖..."
npm install axios cheerio playwright
if [ $? -ne 0 ]; then
    echo "  ❌ 依赖安装失败"
    exit 1
fi
echo "  ✅ 依赖安装完成"
echo ""

# 3. 生成配置文件
echo "【3/5】生成配置文件..."
CONFIG_PATH="platform_monitor_config.json"
if [ -f "$CONFIG_PATH" ]; then
    echo "  ⚠️  配置文件已存在: $CONFIG_PATH"
else
    node monitor.js --init
fi
echo ""

# 4. 测试运行
echo "【4/5】测试运行..."
node monitor.js
if [ $? -eq 0 ] || [ $? -eq 2 ]; then
    echo "  ✅ 测试运行成功"
else
    echo "  ⚠️  测试运行失败，请检查配置"
fi
echo ""

# 5. 设置定时任务
echo "【5/5】设置定时任务..."
read -p "是否设置定时任务（每天9:00和21:00运行）？ (Y/n) " SETUP_CRON
if [ "$SETUP_CRON" != "n" ]; then
    # 创建 cron 任务
    CRON_CMD="0 9,21 * * * cd $(pwd) && node monitor.js >> monitor.log 2>&1"
    
    # 检查是否已存在
    if crontab -l 2>/dev/null | grep -q "monitor.js"; then
        echo "  ⚠️  cron 任务已存在"
    else
        # 添加新的 cron 任务
        (crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -
        echo "  ✅ 定时任务已创建"
        echo "     每天 09:00 和 21:00 运行"
    fi
fi
echo ""

echo "=========================================="
echo "✅ 安装完成！"
echo ""
echo "📝 下一步:"
echo "  1. 编辑 platform_monitor_config.json 填入你的配置"
echo "  2. 运行 node monitor.js 测试"
echo "  3. 运行 node monitor.js --report 查看报告"
echo ""
echo "📚 文档: https://github.com/your-repo/platform-monitor"
echo ""

read -p "按回车键退出..."
