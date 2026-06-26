#!/usr/bin/env python3
"""
飞书卡片消息发送工具
独立模块，不依赖外部路径
"""
import requests
import json
import sys
import os

# 从环境变量读取配置（安全方式）
APP_ID = os.environ.get("FEISHU_APP_ID", "")
APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "")

def get_token():
    """获取飞书 tenant_access_token"""
    if not APP_ID or not APP_SECRET:
        print("❌ 未配置飞书应用信息，请设置环境变量 FEISHU_APP_ID 和 FEISHU_APP_SECRET", file=sys.stderr)
        return None
    
    r = requests.post(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        json={"app_id": APP_ID, "app_secret": APP_SECRET}
    )
    return r.json().get("tenant_access_token")

def send_card(receive_id, card, receive_id_type=None, reply_to=None):
    """
    发送飞书卡片消息
    
    Args:
        receive_id: 接收者ID（chat_id 或 open_id）
        card: 卡片JSON对象
        receive_id_type: open_id / chat_id（自动推断）
        reply_to: 回复的消息ID（可选）
    
    Returns:
        message_id 或 None
    """
    token = get_token()
    if not token:
        return None
    
    # 自动推断 receive_id_type
    if not receive_id_type:
        if receive_id.startswith("oc_"):
            receive_id_type = "chat_id"
        elif receive_id.startswith("ou_"):
            receive_id_type = "open_id"
        else:
            receive_id_type = "chat_id"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    if reply_to:
        # 回复消息
        url = f"https://open.feishu.cn/open-apis/im/v1/messages/{reply_to}/reply"
        body = {"msg_type": "interactive", "content": json.dumps(card)}
    else:
        # 新消息
        url = f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type={receive_id_type}"
        body = {"receive_id": receive_id, "msg_type": "interactive", "content": json.dumps(card)}

    r = requests.post(url, headers=headers, json=body)
    result = r.json()
    
    if result.get("code") == 0:
        msg_id = result.get("data", {}).get("message_id", "")
        return msg_id
    else:
        print(f"❌ 发送失败: {result.get('msg', 'unknown')}", file=sys.stderr)
        return None


if __name__ == "__main__":
    # 测试用
    print("飞书卡片发送模块 - 请设置环境变量 FEISHU_APP_ID 和 FEISHU_APP_SECRET")
    print("使用方式: from feishu_card import send_card")