#!/usr/bin/env python3
"""
Mapulse — Channel Setup Helper
频道创建后运行此脚本，设置频道简介并测试发送

使用:
  1. 手动在 Telegram 中创建频道 "Mapulse 한국주식 브리핑"
  2. 将 @Mapulse_bot 添加为频道管理员 (需要发消息权限)
  3. 获取频道 username (如 @mapulse_kr) 或 chat_id
  4. 运行: python3 setup_channel.py @mapulse_kr
"""

import os
import sys
import requests

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")

def test_channel(channel_id):
    """测试向频道发送消息"""
    print(f"\n🔍 Testing channel: {channel_id}")
    
    # Get chat info
    resp = requests.get(
        f"https://api.telegram.org/bot{TOKEN}/getChat",
        params={"chat_id": channel_id},
        timeout=10,
    )
    result = resp.json()
    if result.get("ok"):
        chat = result["result"]
        print(f"  ✅ Channel found: {chat.get('title', '?')}")
        print(f"  📝 Type: {chat.get('type')}")
        print(f"  🔗 Username: @{chat.get('username', 'N/A')}")
    else:
        print(f"  ❌ Cannot access channel: {result.get('description')}")
        print(f"  → Make sure @Mapulse_bot is added as admin with 'Post Messages' permission")
        return False

    # Test send
    test_msg = (
        "📊 <b>Mapulse 한국주식 브리핑</b> 채널 연동 완료!\n\n"
        "매일 3회 한국 증시 AI 분석을 이 채널에서 받아보세요.\n\n"
        "🕗 08:30 KST — 개장 전 브리핑\n"
        "🕛 12:20 KST — 오전장 정리\n"
        "🌙 20:50 KST — 해외 야간 브리핑\n\n"
        "💬 더 깊은 분석은 @Mapulse_bot 에서!\n"
        "1:1 AI 대화로 관심 종목 분석, 투자 전략 상담까지."
    )
    
    resp = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={
            "chat_id": channel_id,
            "text": test_msg,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        },
        timeout=10,
    )
    result = resp.json()
    if result.get("ok"):
        print(f"  ✅ Test message sent successfully!")
        print(f"\n  → 请将 CHANNEL_ID={channel_id} 写入 .env")
        return True
    else:
        print(f"  ❌ Send failed: {result.get('description')}")
        return False


if __name__ == "__main__":
    if not TOKEN:
        print("Set TELEGRAM_BOT_TOKEN environment variable first.")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Usage: python3 setup_channel.py <channel_id_or_username>")
        print("Example: python3 setup_channel.py @mapulse_kr")
        sys.exit(1)

    channel_id = sys.argv[1]
    test_channel(channel_id)
