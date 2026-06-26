#!/usr/bin/env python3
"""
每日成长任务生成器 | Daily Task Generator

基于六条标准，每日生成3个可执行的"新青年任务"
"""

import random
from datetime import date

# 新青年六条标准的每日任务
DAILY_TASKS = {
    "自主": [
        "今天至少对一个权威观点提出质疑（可以是新闻、专家意见、或者'大家都这么说'）",
        "自己做一个小决定（吃什么、穿什么、去哪里），不询问别人意见",
        "写下来最近一个'大家都这么说'的观点，然后思考：真的是这样吗？",
    ],
    "进步": [
        "今天学习一个你完全不了解的领域的知识点（哪怕只有10分钟）",
        "读一篇和你现有观点不同的文章，试着理解对方的逻辑",
        "把一个旧习惯稍作改进，而不是全盘推翻",
    ],
    "进取": [
        "主动联系一个人，推进一件你一直在搁置的事情",
        "今天不做'等明天'的事情，哪怕只往前走一小步",
        "主动承担一个小责任（比如主动在会议上发言）",
    ],
    "世界": [
        "阅读一篇关于另一个国家的深度报道",
        "和一个不同背景的人深入交流（哪怕是在网上）",
        "了解一个你完全不了解的文化习俗",
    ],
    "实利": [
        "把脑子里一个'想做的事'变成'今天可以做的第一件事'",
        "完成一件你拖延超过一周的事情（哪怕只是第一步）",
        "把一个模糊的想法写下来，越具体越好",
    ],
    "科学": [
        "用数据或事实验证一个你日常持有的观点",
        "今天遇到问题时，先查资料再下结论",
        "记录一个你的假设，然后思考如何验证它",
    ],
}


def get_day_seed() -> int:
    """根据日期生成随机种子，确保同一天任务一致"""
    today = date.today()
    return today.year * 10000 + today.month * 100 + today.day


def generate_daily_tasks() -> list:
    """生成每日任务"""
    seed = get_day_seed()
    random.seed(seed)
    
    # 每天随机选择3个不同维度
    dimensions = list(DAILY_TASKS.keys())
    selected_dims = random.sample(dimensions, 3)
    
    tasks = []
    for dim in selected_dims:
        task = random.choice(DAILY_TASKS[dim])
        tasks.append((dim, task))
    
    return tasks


def format_output(tasks: list) -> str:
    """格式化输出"""
    lines = [
        "=" * 40,
        "🌱 新青年每日任务",
        f"日期：{date.today().strftime('%Y年%m月%d日')}",
        "=" * 40,
        "",
        "今天推荐完成以下3个任务：",
        "",
    ]
    
    for i, (dim, task) in enumerate(tasks, 1):
        lines.append(f"【{dim}】")
        lines.append(f"  {i}. {task}")
        lines.append("")
    
    lines.append("-" * 40)
    lines.append("💡 提示：完成任务后记录感受，明天会有新的任务哦！")
    lines.append("=" * 40)
    
    return "\n".join(lines)


if __name__ == "__main__":
    tasks = generate_daily_tasks()
    print(format_output(tasks))
