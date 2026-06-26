"""
MeetingOS - 企业微信助手
功能：发送企业微信消息、卡片、群机器人通知、创建待办
"""

import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

# 从环境变量读取配置（只读取，不联网）
WECOM_CORP_ID      = os.getenv("WECOM_CORP_ID", "")
WECOM_AGENT_ID     = os.getenv("WECOM_AGENT_ID", "")
WECOM_AGENT_SECRET = os.getenv("WECOM_AGENT_SECRET", "")
WECOM_WEBHOOK_URL  = os.getenv("WECOM_WEBHOOK_URL", "")

BASE_URL = "https://qyapi.weixin.qq.com/cgi-bin"

# 令牌缓存
_token_cache = {"token": None, "expires_at": 0.0}


def get_access_token():
    """
    获取企业微信访问令牌
    有效期 2 小时，会自动刷新
    """
    now = time.time()

    # 还没过期就直接返回缓存的
    if _token_cache["token"] and now < _token_cache["expires_at"] - 60:
        return _token_cache["token"]

    if not WECOM_CORP_ID or not WECOM_AGENT_SECRET:
        raise ValueError(
            "❌ 缺少配置：请设置 WECOM_CORP_ID 和 WECOM_AGENT_SECRET"
        )

    response = requests.get(
        f"{BASE_URL}/gettoken",
        params={"corpid": WECOM_CORP_ID, "corpsecret": WECOM_AGENT_SECRET},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()

    if data.get("errcode", 0) != 0:
        raise RuntimeError(f"❌ 企业微信登录失败：{data.get('errmsg')}")

    _token_cache["token"]      = data["access_token"]
    _token_cache["expires_at"] = now + data.get("expires_in", 7200)
    return _token_cache["token"]


def send_text(content, to_users="@all"):
    """
    发送文字消息给企业微信成员

    参数：
        content  - 消息内容
        to_users - 接收人，"@all" 发给所有人，或传入 userid 列表

    示例：
        send_text("会议纪要已生成！")
        send_text("请查收任务", to_users=["zhangsan", "lisi"])
    """
    # 处理用户列表格式
    if isinstance(to_users, list):
        to_users = "|".join(to_users)

    payload = {
        "touser":  to_users,
        "msgtype": "text",
        "agentid": WECOM_AGENT_ID,
        "text":    {"content": content},
    }

    response = requests.post(
        f"{BASE_URL}/message/send",
        params={"access_token": get_access_token()},
        json=payload,
        timeout=15,
    )
    response.raise_for_status()
    result = response.json()

    if result.get("errcode", 0) != 0:
        raise RuntimeError(f"❌ 消息发送失败：{result.get('errmsg')}")

    print(f"✅ 企业微信消息已发送")
    return result


def send_markdown(content, to_users="@all"):
    """
    发送 Markdown 格式消息（适合发会议纪要）

    参数：
        content  - Markdown 格式的内容
        to_users - 接收人

    示例：
        send_markdown("## 今日纪要\\n\\n- 行动项1\\n- 行动项2")
    """
    if isinstance(to_users, list):
        to_users = "|".join(to_users)

    # 企业微信限制 4096 字节，超出截断
    if len(content.encode("utf-8")) > 4000:
        content = content.encode("utf-8")[:3900].decode("utf-8", errors="ignore")
        content += "\n\n> 内容过长已截断，请查看完整纪要链接"

    payload = {
        "touser":   to_users,
        "msgtype":  "markdown",
        "agentid":  WECOM_AGENT_ID,
        "markdown": {"content": content},
    }

    response = requests.post(
        f"{BASE_URL}/message/send",
        params={"access_token": get_access_token()},
        json=payload,
        timeout=15,
    )
    response.raise_for_status()
    result = response.json()

    if result.get("errcode", 0) != 0:
        raise RuntimeError(f"❌ Markdown 消息发送失败：{result.get('errmsg')}")

    print("✅ 企业微信 Markdown 消息已发送")
    return result


def send_meeting_card(meeting_title, meeting_date, participants,
                      action_count, decision_count, detail_url=""):
    """
    发送会议纪要图文卡片消息

    参数：
        meeting_title  - 会议标题
        meeting_date   - 会议时间
        participants   - 参会人列表
        action_count   - 行动项数量
        decision_count - 决策数量
        detail_url     - 点击查看完整纪要的链接
    """
    # 参会人展示
    people = "、".join(participants[:5])
    if len(participants) > 5:
        people += f" 等{len(participants)}人"

    description = (
        f"📅 {meeting_date}\n"
        f"👥 {people}\n"
        f"🎯 行动项 {action_count} 个 | ✅ 决策 {decision_count} 项\n"
        f"由 MeetingOS 🧠 自动生成"
    )

    jump_url = detail_url or "https://clawhub.ai/DTTNpole-commits/meetingos"

    payload = {
        "touser":  "@all",
        "msgtype": "news",
        "agentid": WECOM_AGENT_ID,
        "news": {
            "articles": [{
                "title":       f"🧠 {meeting_title} — 会议纪要",
                "description": description,
                "url":         jump_url,
            }]
        },
    }

    response = requests.post(
        f"{BASE_URL}/message/send",
        params={"access_token": get_access_token()},
        json=payload,
        timeout=15,
    )
    response.raise_for_status()
    result = response.json()

    if result.get("errcode", 0) != 0:
        raise RuntimeError(f"❌ 卡片消息发送失败：{result.get('errmsg')}")

    print(f"✅ 企业微信卡片消息已发送：{meeting_title}")
    return result


def webhook_send(content, at_userids=None):
    """
    通过群机器人 Webhook 发送消息（最简单的方式，不需要 CORP_ID）

    前提：在企业微信群里添加机器人，获取 Webhook URL
    设置：WECOM_WEBHOOK_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx

    参数：
        content     - 消息内容
        at_userids  - 要@的人的 userid 列表，如 ["zhangsan"]

    示例：
        webhook_send("纪要已生成！", at_userids=["zhangsan"])
    """
    if not WECOM_WEBHOOK_URL:
        raise ValueError("❌ 未设置 WECOM_WEBHOOK_URL")

    payload = {
        "msgtype": "text",
        "text": {
            "content":        content,
            "mentioned_list": at_userids or [],
        },
    }

    response = requests.post(WECOM_WEBHOOK_URL, json=payload, timeout=10)
    response.raise_for_status()
    result = response.json()

    if result.get("errcode", 0) != 0:
        raise RuntimeError(f"❌ Webhook 发送失败：{result.get('errmsg')}")

    print("✅ 企业微信 Webhook 消息已发送")
    return result


def webhook_markdown(content):
    """
    通过群机器人 Webhook 发送 Markdown 消息

    示例：
        webhook_markdown("## 会议结束\\n\\n行动项已推送 ✅")
    """
    if not WECOM_WEBHOOK_URL:
        raise ValueError("❌ 未设置 WECOM_WEBHOOK_URL")

    payload = {"msgtype": "markdown", "markdown": {"content": content}}

    response = requests.post(WECOM_WEBHOOK_URL, json=payload, timeout=10)
    response.raise_for_status()
    result = response.json()

    if result.get("errcode", 0) != 0:
        raise RuntimeError(f"❌ Webhook Markdown 发送失败：{result.get('errmsg')}")

    print("✅ 企业微信 Webhook Markdown 已发送")
    return result


# ══════════════════════════════════════════════
# 测试代码（只有直接运行才执行，导入时不执行）
# ══════════════════════════════════════════════
if __name__ == "__main__":
    import sys

    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"

    if cmd == "test_token":
        token = get_access_token()
        print(f"✅ 令牌获取成功：{token[:12]}...")

    elif cmd == "test_text":
        send_text("✅ MeetingOS 企业微信测试成功！")

    elif cmd == "test_webhook":
        webhook_markdown(
            "## ✅ MeetingOS 机器人测试\n\n**状态**：连接正常"
        )

    elif cmd == "test_card":
        send_meeting_card(
            meeting_title="产品周会测试",
            meeting_date="2025-06-15 14:00",
            participants=["张三", "李四"],
            action_count=5,
            decision_count=2,
        )

    else:
        print("使用方法：")
        print("  python wecom_helper.py test_token    测试获取令牌")
        print("  python wecom_helper.py test_text     测试发送文字")
        print("  python wecom_helper.py test_webhook  测试机器人")
        print("  python wecom_helper.py test_card     测试卡片消息")