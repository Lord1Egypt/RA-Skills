#!/usr/bin/env python3
"""
从对话中提取文字并转语音
用法: tts_from_chat.py "<用户消息文本>" <发送者open_id> [被回复的消息ID]

触发词：转语音 / 转成语音 / 说一遍 / 语音
"""

import sys
import os
import re

# 添加 scripts 目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

API_KEY = os.environ.get("MINIMAX_API_KEY", "")
FEISHU_APP_ID = os.environ.get("FEISHU_APP_ID", "")
FEISHU_APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "")

LAST_MSG_FILE = "/tmp/last_miss_m_message.txt"


# 触发词
TRIGGERS = ["转语音", "转成语音", "变成语音", "说一遍", "语音播放"]


def is_triggered(user_text: str) -> bool:
    """检查是否包含触发词"""
    text = user_text.strip().lower()
    return any(t in text for t in TRIGGERS)


def get_feishu_token():
    """获取飞书 access token"""
    import requests
    r = requests.post(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        json={"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET},
        timeout=10
    )
    return r.json().get("tenant_access_token", "")


def get_message_content(message_id: str, token: str) -> str:
    """获取指定消息的内容"""
    import requests
    try:
        r = requests.get(
            f"https://open.feishu.cn/open-apis/im/v1/messages/{message_id}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        data = r.json()
        if data.get("code") == 0:
            items = data.get("data", {}).get("items", [])
            if items:
                return items[0].get("body", {}).get("content", "")
    except Exception as e:
        print(f"获取消息失败: {e}", file=sys.stderr)
    return ""


def get_last_message() -> str:
    """获取我最后发的那条消息"""
    try:
        if os.path.exists(LAST_MSG_FILE):
            with open(LAST_MSG_FILE, "r", encoding="utf-8") as f:
                return f.read().strip()
    except Exception:
        pass
    return ""


def save_last_message(text: str):
    """保存最后一条消息"""
    try:
        with open(LAST_MSG_FILE, "w", encoding="utf-8") as f:
            f.write(text)
    except Exception:
        pass


def extract_and_speak(user_text: str, user_open_id: str = None, reply_message_id: str = None) -> dict:
    """
    主函数：检测触发词，提取文字，生成语音
    """
    if not is_triggered(user_text):
        return {"triggered": False}
    
    text_to_speak = ""
    
    # 优先：获取被回复的消息内容
    if reply_message_id:
        token = get_feishu_token()
        content = get_message_content(reply_message_id, token)
        if content:
            text_to_speak = content
            print(f"使用被回复消息 {reply_message_id}: {content[:50]}...", file=sys.stderr)
    
    # 其次：使用我最后发的那条消息
    if not text_to_speak:
        text_to_speak = get_last_message()
        if text_to_speak:
            print(f"使用最后消息: {text_to_speak[:50]}...", file=sys.stderr)
    
    if not text_to_speak:
        return {"triggered": True, "error": "找不到要转语音的文字"}
    
    # 生成并发送语音
    from tts import tts_and_send
    result = tts_and_send(text_to_speak, user_open_id=user_open_id)
    return {"triggered": True, "text": text_to_speak, "result": result}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        # 无参数：保存最后一条消息
        print("用法:")
        print("  tts_from_chat.py save <消息文本>  # 保存最后消息")
        print("  tts_from_chat.py trigger <用户消息> <发送者open_id> [被回复消息ID]  # 触发转语音")
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "save" and len(sys.argv) >= 3:
        # 保存最后一条消息
        save_last_message(sys.argv[2])
        print(f"已保存: {sys.argv[2][:50]}...")
    
    elif cmd == "trigger" and len(sys.argv) >= 3:
        user_text = sys.argv[2]
        user_open_id = sys.argv[3] if len(sys.argv) > 3 else None
        reply_message_id = sys.argv[4] if len(sys.argv) > 4 else None
        
        result = extract_and_speak(user_text, user_open_id, reply_message_id)
        print(result)
    
    else:
        print(f"未知命令或参数不足: {cmd}", file=sys.stderr)
        sys.exit(1)
