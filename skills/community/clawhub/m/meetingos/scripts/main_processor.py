"""
MeetingOS - 核心处理器
流程：转录 → 提取行动项 → 推送飞书 → 计费
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()


def send_feishu_text(webhook_url: str, text: str) -> bool:
    """
    发送文字到飞书群

    参数：
        webhook_url - 飞书机器人地址
        text        - 消息内容

    返回：
        True 发送成功
        False 发送失败
    """
    try:
        response = requests.post(
            webhook_url,
            json={"msg_type": "text", "content": {"text": text}},
            timeout=10,
        )
        return response.status_code == 200
    except Exception as error:
        print(f"飞书发送失败：{error}")
        return False


def extract_action_items(transcript: str) -> str:
    """
    从会议文字稿提取行动项

    参数：
        transcript - 会议文字内容

    返回：
        格式化的行动项字符串
    """
    lines    = transcript.strip().split("\n")
    actions  = []
    keywords = [
        "明天", "本周", "下周", "完成", "准备",
        "跟进", "负责", "提交", "发送", "安排",
        "确认", "review", "todo", "action"
    ]

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if any(word in line.lower() for word in keywords):
            actions.append(f"[ ] {line}")

    if not actions:
        return "本次会议无明确行动项"

    result = "会议行动项\n" + "\n".join(actions[:5])

    if len(actions) > 5:
        result += f"\n\n还有 {len(actions) - 5} 条行动项，升级 Pro 版查看全部"

    return result


def process_meeting(transcript: str = None, user_id: str = "default_user") -> dict:
    """
    核心处理函数

    参数：
        transcript - 会议文字稿，不填则用内置测试内容
        user_id    - 用户标识，用于 SkillPay 计费

    返回：
        包含处理结果的字典

    示例：
        result = process_meeting(
            transcript="张三：明天完成设计稿。李四：本周五提交报告。",
            user_id="user@example.com"
        )
    """
    print("MeetingOS 开始处理...")

    # 第一步：计费检查
    try:
        from skillpay_guard import require_tokens
        if not require_tokens(user_id):
            return {
                "success": False,
                "message": "余额不足，请充值后再试",
            }
    except ImportError:
        print("跳过计费检查")

    # 第二步：准备文字稿
    if not transcript:
        transcript = (
            "张三：明天把设计稿完成。\n"
            "李四：本周五前提交测试报告。\n"
            "王五：下周一跟进客户反馈。\n"
        )
        print("使用内置测试文字稿")

    # 第三步：提取行动项
    print("正在提取行动项...")
    action_summary = extract_action_items(transcript)
    print(f"提取结果：\n{action_summary}")

    # 第四步：推送飞书
    webhook = os.getenv("FEISHU_WEBHOOK_URL", "")
    if webhook:
        print("正在推送到飞书...")
        ok = send_feishu_text(webhook, f"会议行动项：\n{action_summary}")
        if ok:
            print("飞书推送成功")
        else:
            print("飞书推送失败，请检查 FEISHU_WEBHOOK_URL")
    else:
        print("未配置 FEISHU_WEBHOOK_URL，跳过飞书推送")

    return {
        "success":      True,
        "message":      "处理完成",
        "action_items": action_summary,
    }


# 测试代码，只有直接运行才执行
if __name__ == "__main__":
    import sys

    cmd = sys.argv[1] if len(sys.argv) > 1 else "test"

    if cmd == "test":
        result = process_meeting()
        print(f"\n结果：{result['message']}")

    elif cmd == "test_real":
        my_transcript = (
            "张三：我明天完成登录页面开发。\n"
            "李四：本周三前准备好测试报告。\n"
            "王五：下周一跟进客户意见。\n"
        )
        result = process_meeting(transcript=my_transcript, user_id="test@test.com")
        print(f"\n结果：{result}")

    else:
        print("使用方法：")
        print("  python main_processor.py           本地测试")
        print("  python main_processor.py test_real 真实文字测试")
```

---

## 第五件事：全局搜索确认没有真实 Key

在 VS Code 里按 `Ctrl + Shift + F`，逐一搜索以下内容：
```
sk_e9b7
```
```
bf65c3ac
```
```
secret_
```

如果搜索到任何结果，点开那个文件，把那行内容删掉。

---

## 第六件事：确认文件夹干净

打开 `meeting-os` 文件夹，确认：
```
有这些文件：
  SKILL.md
  requirements.txt
  scripts/ 文件夹
  templates/ 文件夹

没有这些文件：
  .env
  任何包含真实 Key 的文件