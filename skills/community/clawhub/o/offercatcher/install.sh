#!/bin/bash
# OfferCatcher 一键安装脚本
# 用法: curl -sSL https://raw.githubusercontent.com/NissonCX/offercatcher/main/install.sh | bash

set -e

SKILLS_DIR="$HOME/.openclaw/workspace/skills"
SKILL_NAME="offercatcher"
SKILL_PATH="$SKILLS_DIR/$SKILL_NAME"
CONFIG_FILE="$HOME/.openclaw/offercatcher.yaml"

echo "🚀 OfferCatcher 安装脚本"
echo ""

# 1. 确保 skills 目录存在
mkdir -p "$SKILLS_DIR"

# 2. 克隆或更新 skill
if [ -d "$SKILL_PATH" ]; then
    echo "📦 检测到已安装，正在更新..."
    cd "$SKILL_PATH"
    git pull -q
else
    echo "📦 克隆 skill 到 $SKILL_PATH..."
    git clone -q https://github.com/NissonCX/offercatcher.git "$SKILL_PATH"
fi

# 3. 创建默认配置文件（如果不存在）
if [ ! -f "$CONFIG_FILE" ]; then
    echo "📝 创建配置文件 $CONFIG_FILE"
    cat > "$CONFIG_FILE" << 'EOF'
# OfferCatcher 配置
# 配置优先级: 命令行 > 环境变量 > 此文件 > 默认值

mail_account: ""        # Apple Mail 账号名，如 "谷歌"
mailbox: INBOX          # 邮箱目录
days: 2                 # 扫描最近 N 天
max_results: 60         # 最多扫描 N 封邮件
EOF
    echo ""
    echo "⚠️  请编辑 $CONFIG_FILE 设置你的 mail_account"
fi

# 4. 检查 PyYAML（可选依赖）
if ! python3 -c "import yaml" 2>/dev/null; then
    echo ""
    echo "💡 提示: 安装 PyYAML 可启用配置文件支持"
    echo "   pip3 install pyyaml"
fi

echo ""
echo "✅ 安装完成！"
echo ""
echo "📋 使用方式："
echo "   1. 扫描邮件：python3 $SKILL_PATH/scripts/recruiting_sync.py --scan-only"
echo "   2. OpenClaw LLM 解析邮件内容"
echo "   3. 应用结果：python3 $SKILL_PATH/scripts/recruiting_sync.py --apply-events /tmp/events.json"