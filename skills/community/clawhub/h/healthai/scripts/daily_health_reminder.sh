#!/bin/bash

# ==============================================
# 每日健康运动提醒脚本 - 使用 curl 调用飞书 API
# ==============================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 查找 skill 目录（兼容多个可能的位置）
for dir in "$SCRIPT_DIR" "$SCRIPT_DIR/.." "$SCRIPT_DIR/../.."; do
    if [ -f "$dir/config/user_config.json" ] && [ -f "$dir/config/exercise_plan.json" ]; then
        CONFIG_DIR="$dir/config"
        break
    fi
done

if [ -z "$CONFIG_DIR" ]; then
    # 备用：使用硬编码路径
    CONFIG_DIR="/Users/amitabhama/.openclaw-autoclaw/skills/HealthSkill-1.0/config"
fi

# 飞书应用凭证
APP_ID="cli_a93be6affe785cd9"
APP_SECRET="JrMNdAdygP7JZsZOZWCMwcvRs8wisZRR"

# 1. 获取用户 ID
FEISHU_USER_ID="${FEISHU_USER_ID:-}"
if [ -z "$FEISHU_USER_ID" ]; then
    USER_CONFIG="$CONFIG_DIR/user_config.json"
    if [ -f "$USER_CONFIG" ]; then
        FEISHU_USER_ID=$(python3 -c "import json; print(json.load(open('$USER_CONFIG')).get('feishu_user_id',''))")
    fi
fi

if [ -z "$FEISHU_USER_ID" ] || [ "$FEISHU_USER_ID" = "ou_your_user_id_here" ]; then
    echo "Error: 未配置用户 ID"
    exit 1
fi

# 2. 获取飞书 token
TOKEN_RESPONSE=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
    -H "Content-Type: application/json" \
    -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}")

ACCESS_TOKEN=$(echo "$TOKEN_RESPONSE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('tenant_access_token',''))")

if [ -z "$ACCESS_TOKEN" ]; then
    echo "Error: 获取 token 失败"
    exit 1
fi

# 3. 构建消息
EXERCISE_PLAN="$CONFIG_DIR/exercise_plan.json"
MESSAGE=$(python3 -c "
import json
from datetime import datetime

with open('$EXERCISE_PLAN', 'r', encoding='utf-8') as f:
    plan = json.load(f)

day_map = {0:'周一', 1:'周二', 2:'周三', 3:'周四', 4:'周五', 5:'周六', 6:'周日'}
day_name = day_map[datetime.now().weekday()]

weekly = plan.get('weekly_plan', plan)
day_data = weekly.get(day_name, {})
morning = day_data.get('早上', {})
afternoon = day_data.get('下午', {})

msg = '🏃 每日运动提醒（' + day_name + '）'
msg += '\n\n早上：'
msg += '\n  运动：' + morning.get('运动', '休息')
msg += '\n  时长：' + morning.get('时长', '-')
msg += '\n  目的：' + morning.get('目的', '-')

video = morning.get('video', '')
if video:
    msg += '\n  视频：' + video

if afternoon.get('运动') and afternoon.get('运动') != '休息':
    msg += '\n\n下午：'
    msg += '\n  运动：' + afternoon.get('运动')
    msg += '\n  时长：' + afternoon.get('时长', '-')
    msg += '\n  目的：' + afternoon.get('目的', '-')

msg += '\n\n💪 坚持就是胜利！'
print(json.dumps(msg))
")

# 4. 发送消息
echo "发送运动提醒给用户: $FEISHU_USER_ID"

SEND_RESPONSE=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"receive_id\":\"$FEISHU_USER_ID\",\"msg_type\":\"text\",\"content\":$MESSAGE}")

CODE=$(echo "$SEND_RESPONSE" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('code',-1))")

if [ "$CODE" = "0" ]; then
    echo "✅ 消息发送成功"
else
    echo "❌ 消息发送失败: $SEND_RESPONSE"
fi
