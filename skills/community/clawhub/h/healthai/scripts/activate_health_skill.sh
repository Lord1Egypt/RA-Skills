#!/bin/bash

# ==============================================
# HealthSkill 1.0 一键激活脚本
# 用户运行此脚本即可完成全部配置
# ==============================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_DIR="$SKILL_DIR/config"

echo "🏥 HealthSkill 1.0 激活向导"
echo "=============================="
echo ""

# -------------------------
# Step 1: 获取用户飞书 ID
# -------------------------
echo "📱 Step 1: 获取飞书用户 ID"
echo "请在飞书对话框中发送以下任意一条消息："
echo "  - '激活健康打卡'"
echo "  - '启用健康提醒'"
echo ""
echo "发送后我会自动获取你的 ID 并保存。"
echo ""
read -p "已发送请按回车继续..."

# 检查配置文件是否已有 ID
USER_CONFIG="$CONFIG_DIR/user_config.json"
SAVED_ID=$(python3 -c "import json; print(json.load(open('$USER_CONFIG')).get('feishu_user_id',''))" 2>/dev/null)

if [ -n "$SAVED_ID" ] && [ "$SAVED_ID" != "ou_your_user_id_here" ]; then
    echo "✅ 已获取到用户 ID: $SAVED_ID"
    FEISHU_USER_ID="$SAVED_ID"
else
    echo "❌ 未找到用户 ID"
    echo "请先在飞书发送'激活健康打卡'消息，然后告诉我你的 ID（以 ou_ 开头）"
    read -p "或直接粘贴你的飞书 ID: " FEISHU_USER_ID
    
    if [ -n "$FEISHU_USER_ID" ]; then
        # 保存到配置
        python3 -c "
import json
config = json.load(open('$USER_CONFIG'))
config['feishu_user_id'] = '$FEISHU_USER_ID'
json.dump(config, open('$USER_CONFIG', 'w'), indent=2)
"
        echo "✅ 已保存用户 ID: $FEISHU_USER_ID"
    fi
fi

# -------------------------
# Step 2: 配置 cron 任务
# -------------------------
echo ""
echo "⏰ Step 2: 配置每日自动提醒"
echo ""
echo "将添加以下定时任务："
echo "  每天早上 9:00 自动推送运动计划"
echo ""

# 生成 cron 任务行
SCRIPT_PATH="$SCRIPT_DIR/daily_health_reminder.sh"
LOG_DIR="$SKILL_DIR/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/health_reminder.log"

CRON_LINE="0 9 * * 1-0 $SCRIPT_PATH >> $LOG_FILE 2>&1"

# 检查是否已存在
if crontab -l 2>/dev/null | grep -q "daily_health_reminder"; then
    echo "⚠️ 定时任务已存在，跳过添加"
else
    # 添加 cron 任务
    (crontab -l 2>/dev/null; echo "$CRON_LINE") | crontab -
    echo "✅ 已添加定时任务"
fi

# -------------------------
# Step 3: 测试发送
# -------------------------
echo ""
echo "🧪 Step 3: 测试发送"
echo ""
read -p "是否发送测试消息？(y/n): " TEST_CHOICE

if [ "$TEST_CHOICE" = "y" ] || [ "$TEST_CHOICE" = "Y" ]; then
    echo "发送测试消息..."
    $SCRIPT_PATH
fi

# -------------------------
# 完成
# -------------------------
echo ""
echo "🎉 激活完成！"
echo ""
echo "配置信息："
echo "  - 用户 ID: $FEISHU_USER_ID"
echo "  - 定时任务: 每天 9:00"
echo "  - 脚本路径: $SCRIPT_PATH"
echo ""
echo "如需取消每日提醒，请运行："
echo "  crontab -e"
echo "  删除包含 daily_health_reminder 的行"
echo ""

