#!/usr/bin/env python3
"""
LinkedIn Outreach Message Generator
AI算力销售LinkedIn外联消息生成器

Usage:
    python3 outreach.py --profile "张三, CEO at ABC AI" --type connection-note --purpose "介绍GPU云服务"
"""

import argparse
import sys
from typing import Optional

# LinkedIn消息模板库
TEMPLATES = {
    "connection-note": {
        "limit": 300,
        "templates": [
            "Hi {name}，看到{company}在{focus}方面的进展，我们的GPU集群可能对您有帮助。期待交流！",
            "{name}你好，关注{company}很久了，我们在{focus}领域有类似经验，希望能分享一些见解。",
            "Hi {name}，了解到{company}正在扩展{focus}团队，我们的H100/A100资源或许能支持您的项目。",
        ]
    },
    "inmail": {
        "limit": 2000,
        "templates": [
            """Hi {name}，

我是PANSP专业GPU云服务的销售顾问。关注到{company}在{focus}领域的发展，想与您交流一下我们的解决方案。

{purpose_context}

我们的GPU云服务特点：
• H100/A100/L40S等多种GPU型号可选
• 按需计费，灵活扩展
• 专业团队7x24技术支持

如有兴趣，欢迎进一步沟通。

Best,
[您的姓名]
PANSP GPU Cloud""",
            """Hi {name}，

注意到{company}在{focus}方面的投入，想分享一个可能对您有帮助的资源。

{purpose_context}

我们提供专业的GPU云服务，已服务多家AI公司，包括：
• 模型训练加速方案
• 推理部署优化
• 成本控制策略

期待与您交流。

[您的姓名]
PANSP GPU Cloud""",
        ]
    },
    "follow-up": {
        "limit": 1000,
        "templates": [
            """Hi {name}，

跟进我们之前关于{focus}的讨论。

{purpose_context}

如果您方便的话，我们可以安排一个15分钟的快速通话，深入探讨具体需求。

期待您的回复。

[您的姓名]""",
            """Hi {name}，

上次提到的{focus}方案，我们最近帮助一家类似规模的公司实现了显著成效。

{purpose_context}

不知道您这边进展如何？如有任何问题，随时联系我。

[您的姓名]""",
        ]
    }
}


def parse_profile(profile: str) -> dict:
    """解析profile字符串，提取姓名、公司、关注点等"""
    parts = [p.strip() for p in profile.split(",")]
    result = {
        "name": parts[0] if len(parts) > 0 else "朋友",
        "company": parts[1] if len(parts) > 1 else "贵公司",
        "focus": parts[2] if len(parts) > 2 else "AI技术",
    }
    return result


def generate_message(
    profile: str,
    msg_type: str,
    purpose: str
) -> str:
    """生成个性化LinkedIn消息"""
    
    parsed = parse_profile(profile)
    config = TEMPLATES.get(msg_type, TEMPLATES["connection-note"])
    
    # 添加purpose上下文
    purpose_context = f"这次联系您主要是：{purpose}"
    
    # 选择模板（简单起见用第一个）
    template = config["templates"][0]
    
    # 填充模板
    message = template.format(
        name=parsed["name"],
        company=parsed["company"],
        focus=parsed["focus"],
        purpose_context=purpose_context
    )
    
    # 检查长度限制
    if len(message) > config["limit"]:
        message = message[:config["limit"]-3] + "..."
    
    return message


def main():
    parser = argparse.ArgumentParser(
        description="LinkedIn Outreach Message Generator - AI算力销售LinkedIn外联消息生成器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 生成连接邀请附言
  %(prog)s --profile "张三, CEO at ABC AI, 关注大模型训练" --type connection-note --purpose "介绍GPU云服务"

  # 生成InMail
  %(prog)s --profile "李四, CTO at XYZ Tech, 推理部署" --type inmail --purpose "邀请技术交流"

  # 生成跟进消息
  %(prog)s --profile "王五, VP Engineering" --type follow-up --purpose "跟进上次讨论的H100需求"
"""
    )
    
    parser.add_argument(
        "--profile",
        required=True,
        help="目标人物信息，格式：姓名, 职位/公司, 关注点"
    )
    
    parser.add_argument(
        "--type",
        required=True,
        choices=["connection-note", "inmail", "follow-up"],
        help="消息类型：connection-note(连接邀请), inmail(私信), follow-up(跟进)"
    )
    
    parser.add_argument(
        "--purpose",
        required=True,
        help="发送目的/核心诉求"
    )
    
    args = parser.parse_args()
    
    # 生成消息
    message = generate_message(args.profile, args.type, args.purpose)
    
    # 计算字符数
    char_count = len(message)
    limit = TEMPLATES.get(args.type, {}).get("limit", 1000)
    
    # 输出
    type_labels = {
        "connection-note": "Connection Note (300字符限制)",
        "inmail": "InMail (2000字符限制)",
        "follow-up": "Follow-up (1000字符限制)"
    }
    
    print(f"\n=== {type_labels.get(args.type, args.type)} ===\n")
    print(message)
    print(f"\n[字符数: {char_count}/{limit}]")


if __name__ == "__main__":
    main()