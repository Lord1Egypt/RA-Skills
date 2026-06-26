"""
MeetingOS - 飞书助手
功能：发送飞书群消息、创建任务、写入多维表格
"""

# 导入需要的工具包（只是声明，不会执行任何操作）
import os
import json
import requests
from dotenv import load_dotenv

# 读取 .env 文件里的配置（只读取，不联网）
load_dotenv()

# 从环境变量读取配置（这里只是读取变量，不会发起任何网络请求）
FEISHU_APP_ID        = os.getenv("FEISHU_APP_ID", "")
FEISHU_APP_SECRET    = os.getenv("FEISHU_APP_SECRET", "")
FEISHU_CHAT_ID       = os.getenv("FEISHU_CHAT_ID", "")
FEISHU_BITABLE_TOKEN = os.getenv("FEISHU_BITABLE_TOKEN", "")
FEISHU_BITABLE_TABLE = os.getenv("FEISHU_BITABLE_TABLE", "")

# 飞书 API 的基础地址
BASE_URL = "https://open.feishu.cn/open-apis"

# 用来缓存登录令牌（避免重复登录）
_token_cache = {"token": None, "expires_at": 0.0}


def get_tenant_token():
    """
    获取飞书登录令牌（相当于登录飞书获取通行证）
    有效期 2 小时，自动续期
    """
    import time

    now = time.time()

    # 如果令牌还没过期，直接返回缓存的令牌
    if _token_cache["token"] and now < _token_cache["expires_at"] - 60:
        return _token_cache["token"]

    # 检查必要配置是否存在
    if not FEISHU_APP_ID or not FEISHU_APP_SECRET:
        raise ValueError(
            "❌ 缺少配置：请在 .env 文件里设置 FEISHU_APP_ID 和 FEISHU_APP_SECRET"
        )

    # 向飞书服务器请求令牌
    response = requests.post(
        f"{BASE_URL}/auth/v3/tenant_access_token/internal",
        json={"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()

    # 检查是否成功
    if data.get("code") != 0:
        raise RuntimeError(f"❌ 飞书登录失败：{data.get('msg')}")

    # 保存令牌到缓存
    _token_cache["token"]      = data["tenant_access_token"]
    _token_cache["expires_at"] = now + data.get("expire", 7200)

    return _token_cache["token"]


def get_auth_headers():
    """返回带登录令牌的请求头（每次发请求都需要带上）"""
    return {
        "Authorization": f"Bearer {get_tenant_token()}",
        "Content-Type":  "application/json; charset=utf-8",
    }


def send_group_text(content, chat_id=None):
    """
    发送文字消息到飞书群

    参数：
        content  - 消息内容（字符串）
        chat_id  - 群 ID，不填则使用 .env 里的 FEISHU_CHAT_ID

    示例：
        send_group_text("今日会议纪要已生成，请查收！")
    """
    # 确定发送目标群
    target_chat = chat_id or FEISHU_CHAT_ID
    if not target_chat:
        raise ValueError("❌ 未设置群 ID，请在 .env 里填写 FEISHU_CHAT_ID")

    # 构建消息内容
    payload = {
        "receive_id": target_chat,
        "msg_type":   "text",
        "content":    json.dumps({"text": content}),
    }

    # 发送请求
    response = requests.post(
        f"{BASE_URL}/im/v1/messages",
        headers=get_auth_headers(),
        params={"receive_id_type": "chat_id"},
        json=payload,
        timeout=15,
    )
    response.raise_for_status()
    result = response.json()

    if result.get("code") != 0:
        raise RuntimeError(f"❌ 消息发送失败：{result.get('msg')}")

    print(f"✅ 飞书消息已发送到群 {target_chat}")
    return result


def send_meeting_summary_card(meeting_title, meeting_date, participants,
                               action_items, decisions, detail_url=""):
    """
    发送会议纪要卡片消息到飞书群（样式美观，有按钮）

    参数：
        meeting_title  - 会议标题，如 "产品周会 2025-06-15"
        meeting_date   - 会议时间，如 "2025-06-15 14:00"
        participants   - 参会人列表，如 ["张三", "李四"]
        action_items   - 行动项列表（字典列表）
        decisions      - 决策列表（字典列表）
        detail_url     - 查看完整纪要的链接（可以是 Notion 链接）

    示例：
        send_meeting_summary_card(
            meeting_title="产品周会",
            meeting_date="2025-06-15 14:00",
            participants=["张三", "李四"],
            action_items=[{"who": "张三", "what": "完成设计稿", "when": "6/18"}],
            decisions=[{"decision": "采用方案 B"}],
        )
    """
    if not FEISHU_CHAT_ID:
        raise ValueError("❌ 未设置 FEISHU_CHAT_ID")

    # 参会人展示（超过6人省略）
    people = "、".join(participants[:6])
    if len(participants) > 6:
        people += f" 等{len(participants)}人"

    # 优先级颜色映射
    color_map = {"high": "red", "medium": "orange", "low": "green"}

    # 构建行动项列表（最多显示5条）
    action_elements = []
    for i, item in enumerate(action_items[:5], 1):
        color = color_map.get(item.get("priority", "medium"), "grey")
        action_elements.append({
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": (
                    f"**{i}. {item.get('what', '')}**\n"
                    f"👤 {item.get('who', '待定')} ｜ "
                    f"📅 {item.get('when', '未设定')} ｜ "
                    f"<font color='{color}'>"
                    f"{item.get('priority', 'medium').upper()}</font>"
                ),
            },
        })

    # 超出5条时添加提示
    if len(action_items) > 5:
        action_elements.append({
            "tag": "note",
            "elements": [{
                "tag":     "plain_text",
                "content": f"还有 {len(action_items) - 5} 个行动项，点击下方按钮查看",
            }],
        })

    # 决策摘要（最多3条）
    decision_lines = "\n".join(
        f"• {d.get('decision', '')}" for d in decisions[:3]
    ) or "本次会议无明确决策"

    # 卡片跳转链接
    jump_url = detail_url or "https://clawhub.ai/DTTNpole-commits/meetingos"

    # 构建完整卡片
    card = {
        "config": {"wide_screen_mode": True},
        "header": {
            "title":    {"tag": "plain_text", "content": f"🧠 {meeting_title}"},
            "template": "purple",
        },
        "elements": [
            {
                "tag": "div",
                "fields": [
                    {"is_short": True, "text": {
                        "tag": "lark_md", "content": f"**📅 时间**\n{meeting_date}",
                    }},
                    {"is_short": True, "text": {
                        "tag": "lark_md", "content": f"**👥 参会人**\n{people}",
                    }},
                ],
            },
            {"tag": "hr"},
            {
                "tag": "div",
                "fields": [
                    {"is_short": True, "text": {
                        "tag": "lark_md",
                        "content": f"**🎯 行动项**\n{len(action_items)} 个",
                    }},
                    {"is_short": True, "text": {
                        "tag": "lark_md",
                        "content": f"**✅ 决策**\n{len(decisions)} 项",
                    }},
                ],
            },
            {"tag": "hr"},
            {"tag": "div", "text": {"tag": "lark_md", "content": "**🎯 行动项清单**"}},
            *action_elements,
            {"tag": "hr"},
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**✅ 决策事项**\n{decision_lines}",
                },
            },
            {"tag": "hr"},
            {
                "tag": "action",
                "actions": [{
                    "tag":  "button",
                    "text": {"tag": "plain_text", "content": "📄 查看完整纪要"},
                    "type": "primary",
                    "url":  jump_url,
                }],
            },
            {
                "tag": "note",
                "elements": [{
                    "tag":     "plain_text",
                    "content": "由 MeetingOS 🧠 自动生成",
                }],
            },
        ],
    }

    # 发送卡片消息
    payload = {
        "receive_id": FEISHU_CHAT_ID,
        "msg_type":   "interactive",
        "content":    json.dumps(card),
    }

    response = requests.post(
        f"{BASE_URL}/im/v1/messages",
        headers=get_auth_headers(),
        params={"receive_id_type": "chat_id"},
        json=payload,
        timeout=15,
    )
    response.raise_for_status()
    result = response.json()

    if result.get("code") != 0:
        raise RuntimeError(f"❌ 卡片发送失败：{result.get('msg')}")

    print(f"✅ 飞书卡片消息已发送：{meeting_title}")
    return result


def create_task(title, assignee_open_id, due_ms=None, description=""):
    """
    在飞书里创建一个任务（并分配给指定成员）

    参数：
        title            - 任务标题，如 "完成 API 优化"
        assignee_open_id - 负责人的飞书 ID（ou_开头的字符串）
        due_ms           - 截止时间（毫秒时间戳，可不填）
        description      - 任务备注说明

    示例：
        create_task("完成设计稿", "ou_xxx", description="参见会议纪要")
    """
    payload = {
        "summary":     title,
        "description": description,
        "members": [{
            "id":   assignee_open_id,
            "type": "user",
            "role": "assignee",
        }],
        "can_edit": True,
    }

    # 如果有截止时间就加上
    if due_ms:
        payload["due"] = {"timestamp": str(due_ms // 1000)}

    response = requests.post(
        f"{BASE_URL}/task/v2/tasks",
        headers=get_auth_headers(),
        json=payload,
        timeout=15,
    )
    response.raise_for_status()
    result = response.json()

    if result.get("code") != 0:
        raise RuntimeError(f"❌ 创建任务失败：{result.get('msg')}")

    task_id = result.get("data", {}).get("task", {}).get("guid", "未知")
    print(f"✅ 飞书任务已创建：{title}（ID: {task_id}）")
    return result


def write_to_bitable(records, app_token=None, table_id=None):
    """
    把行动项批量写入飞书多维表格

    参数：
        records    - 要写入的数据列表（每个元素是一个字典，对应表格的一行）
        app_token  - 多维表格的 App Token（不填则用环境变量）
        table_id   - 数据表 ID（不填则用环境变量）

    records 示例：
        [
            {
                "任务名称": "完成 API 优化",
                "优先级":   "高",
                "状态":     "待处理",
                "来源会议": "产品周会 2025-06-15",
            }
        ]
    """
    # 确定使用哪个表格
    atoken = app_token or FEISHU_BITABLE_TOKEN
    tbl    = table_id  or FEISHU_BITABLE_TABLE

    if not atoken or not tbl:
        raise ValueError(
            "❌ 缺少多维表格配置，请设置 FEISHU_BITABLE_TOKEN 和 FEISHU_BITABLE_TABLE"
        )

    url     = f"{BASE_URL}/bitable/v1/apps/{atoken}/tables/{tbl}/records/batch_create"
    payload = {"records": [{"fields": r} for r in records]}

    response = requests.post(
        url,
        headers=get_auth_headers(),
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    result = response.json()

    if result.get("code") != 0:
        raise RuntimeError(f"❌ 写入多维表格失败：{result.get('msg')}")

    count = len(result.get("data", {}).get("records", []))
    print(f"✅ 已写入 {count} 条记录到飞书多维表格")
    return result


# ══════════════════════════════════════════════
# 以下是测试代码，只有直接运行这个文件才会执行
# 导入这个文件时不会自动执行（这是修复安全扫描的关键！）
# ══════════════════════════════════════════════
if __name__ == "__main__":
    import sys

    # 读取命令行参数决定运行哪个测试
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"

    if cmd == "test_token":
        # 测试能否成功获取飞书令牌
        token = get_tenant_token()
        print(f"✅ 令牌获取成功：{token[:16]}...")

    elif cmd == "test_text":
        # 测试发送文字消息
        send_group_text("✅ MeetingOS 飞书连接测试成功！")

    elif cmd == "test_card":
        # 测试发送卡片消息
        send_meeting_summary_card(
            meeting_title="测试会议 2025-06-15",
            meeting_date="2025-06-15 14:00",
            participants=["张三", "李四", "王五"],
            action_items=[
                {"who": "张三", "what": "完成设计稿", "when": "6/18", "priority": "high"},
                {"who": "李四", "what": "接口优化",   "when": "6/20", "priority": "medium"},
            ],
            decisions=[{"decision": "采用方案 B"}],
        )

    else:
        print("使用方法：")
        print("  python feishu_helper.py test_token   测试获取令牌")
        print("  python feishu_helper.py test_text    测试发送文字")
        print("  python feishu_helper.py test_card    测试发送卡片")