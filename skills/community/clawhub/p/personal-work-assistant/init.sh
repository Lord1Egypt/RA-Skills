#!/bin/bash
# 个人工作助理一键初始化向导
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "=========================================="
echo "🤖 欢迎使用 个人工作助理 (Personal Work Assistant)"
echo "=========================================="

if [ -f "config.yaml" ]; then
    read -p "⚠️ 检测到已有 config.yaml，是否重新配置？(y/N): " RECONFIG
    if [[ ! "$RECONFIG" =~ ^[Yy]$ ]]; then
        echo "已保留现有配置。"
        exit 0
    fi
fi

cp config.template.yaml config.yaml

echo ""
echo "📝 请输入你的基础信息："
read -p "1. 你的真实姓名 (例: 张三): " USER_NAME
read -p "2. 你的常用昵称/英文名 (逗号分隔, 例: San,三哥): " USER_ALIASES
read -p "3. 你的钉钉 User ID (可通过 dws contact user get-self 查看): " DING_USER_ID
read -p "4. 你的工作晨报接收目标 (钉钉个人通道 ID / User ID): " DING_TARGET

# 替换配置
sed -i "s/name: \"张三\"/name: \"$USER_NAME\"/" config.yaml
sed -i "s/your_dingtalk_user_id/$DING_USER_ID/g" config.yaml
sed -i "s/target_user_id: \"your_dingtalk_user_id\"/target_user_id: \"$DING_TARGET\"/" config.yaml

echo ""
read -p "5. 是否启用 Teambition 任务追踪？(y/N): " ENABLE_TB
if [[ "$ENABLE_TB" =~ ^[Yy]$ ]]; then
    read -p "   - 请输入 Teambition User Token: " TB_TOKEN
    read -p "   - 请输入 Teambition Org ID: " TB_ORG
    sed -i "s/enabled: true/enabled: true/" config.yaml
    sed -i "s/your_teambition_user_token/$TB_TOKEN/" config.yaml
    sed -i "s/your_teambition_org_id/$TB_ORG/" config.yaml
else
    sed -i "s/enabled: true/enabled: false/" config.yaml
fi

echo ""
echo "✅ 基础配置已生成到 config.yaml！"
echo "👉 如需添加重点监控群聊，请手动编辑 config.yaml 中的 rules.focused_groups。"
echo ""
read -p "是否现在一键挂载工作日 10:00 的定时任务 (Crontab)？(y/N): " SETUP_CRON
if [[ "$SETUP_CRON" =~ ^[Yy]$ ]]; then
    bash scripts/setup_cron.sh
fi

echo "🎉 初始化完成！"
