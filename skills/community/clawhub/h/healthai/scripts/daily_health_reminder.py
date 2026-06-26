#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
每日健康运动提醒脚本 - 使用飞书 API
"""

import os
import json
import subprocess
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 查找 config 目录
CONFIG_DIR = None
for base in [SCRIPT_DIR, os.path.dirname(SCRIPT_DIR), os.path.dirname(os.path.dirname(SCRIPT_DIR))]:
    config_path = os.path.join(base, "config")
    if os.path.exists(os.path.join(config_path, "user_config.json")):
        CONFIG_DIR = config_path
        break

if not CONFIG_DIR:
    CONFIG_DIR = "/Users/amitabhama/.openclaw-autoclaw/skills/HealthSkill-1.0/config"

# 飞书凭证
APP_ID = "cli_a93be6affe785cd9"
APP_SECRET = "JrMNdAdygP7JZsZOZWCMwcvRs8wisZRR"

def get_token():
    """获取飞书 token"""
    cmd = [
        'curl', '-s', '-X', 'POST',
        'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
        '-H', 'Content-Type: application/json',
        '-d', json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET})
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    return data.get('tenant_access_token', '')

def send_message(user_id, message):
    """发送消息"""
    token = get_token()
    if not token:
        print("❌ 获取 token 失败")
        return False
    
    # content 需要双重 JSON 序列化
    content = json.dumps({"text": message})
    
    cmd = [
        'curl', '-s', '-X', 'POST',
        f'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id',
        '-H', f'Authorization: Bearer {token}',
        '-H', 'Content-Type: application/json',
        '-d', json.dumps({
            "receive_id": user_id,
            "msg_type": "text",
            "content": content
        })
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    
    if data.get('code') == 0:
        return True
    else:
        print(f"❌ 发送失败: {data}")
        return False

def main():
    # 1. 获取用户 ID
    user_id = os.environ.get("FEISHU_USER_ID", "")
    if not user_id:
        config_path = os.path.join(CONFIG_DIR, "user_config.json")
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                user_id = json.load(f).get("feishu_user_id", "")
    
    if not user_id or user_id == "ou_your_user_id_here":
        print("❌ 未配置用户 ID")
        return
    
    # 2. 读取运动计划
    plan_path = os.path.join(CONFIG_DIR, "exercise_plan.json")
    with open(plan_path, "r", encoding="utf-8") as f:
        plan = json.load(f)
    
    day_map = {0:"周一", 1:"周二", 2:"周三", 3:"周四", 4:"周五", 5:"周六", 6:"周日"}
    day_name = day_map[datetime.now().weekday()]
    
    weekly = plan.get("weekly_plan", plan)
    day_data = weekly.get(day_name, {})
    morning = day_data.get("早上", {})
    afternoon = day_data.get("下午", {})
    
    # 3. 构建消息
    msg = f"🏃 每日运动提醒（{day_name}）\n\n"
    msg += f"早上：\n"
    msg += f"  运动：{morning.get('运动', '休息')}\n"
    msg += f"  时长：{morning.get('时长', '-')}\n"
    msg += f"  目的：{morning.get('目的', '-')}"
    
    video = morning.get("video", "")
    if video:
        msg += f"\n  视频：{video}"
    
    if afternoon.get("运动") and afternoon.get("运动") != "休息":
        msg += f"\n\n下午：\n"
        msg += f"  运动：{afternoon.get('运动')}\n"
        msg += f"  时长：{afternoon.get('时长', '-')}\n"
        msg += f"  目的：{afternoon.get('目的', '-')}"
    
    msg += f"\n\n💪 坚持就是胜利！"
    
    # 4. 发送
    print(f"发送运动提醒给用户: {user_id}")
    if send_message(user_id, msg):
        print("✅ 消息发送成功")
    else:
        print("❌ 消息发送失败")

if __name__ == "__main__":
    main()
