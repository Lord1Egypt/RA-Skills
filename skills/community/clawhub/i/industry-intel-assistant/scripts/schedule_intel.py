#!/usr/bin/env python3
"""
Schedule Intel Task — 创建定时情报推送任务
用法: python3 schedule_intel.py --query "<关键词>" --schedule "<cron表达式>" --channel <wecom|feishu|ddingtalk>
"""

import argparse
import os
import subprocess
import sys


INTEL_CRON_TEMPLATE = (
    'openclaw cron add '
    '--name "行业情报推送" '
    '--schedule "{schedule}" '
    '--tz {timezone} '
    '--session-target isolated '
    '--payload-kind agentTurn '
    '--payload-message "请用 Tavily 搜索今日{行业关键词}行业最新动态，返回3-5条重要资讯（标题+摘要+链接），用中文简洁输出。搜索关键词：{query}" '
    '--delivery-mode announce '
    "--enabled"
)

SUPPORTED_CHANNELS = ["wecom", "feishu", "ddingtalk"]


def create_cron_task(query: str, schedule: str, channel: str, timezone: str = "Asia/Shanghai"):
    """通过 openclaw cron 命令创建定时情报推送任务。"""
    industry = detect_industry(query)
    cmd = (
        f'openclaw cron add '
        f'--name "【{industry}】情报简报" '
        f'--schedule "{schedule}" '
        f'--tz {timezone} '
        f'--session-target isolated '
        f'--payload-kind agentTurn '
        f'--payload-message "请用 Tavily 搜索今日{industry}行业最新动态，关键词：{query}。返回3-5条重要资讯，每条包含标题、50字摘要和来源链接，用中文输出。" '
        f'--delivery-mode announce '
        f'--channel {channel} '
        f'--enabled'
    )
    print(f"执行命令: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result


def detect_industry(query: str) -> str:
    query_lower = query.lower()
    industries = {
        "AI": ["AI", "人工智能", "LLM", "GPT", "大模型", "AIGC", "生成式"],
        "电商": ["电商", "跨境", "Shopify", "亚马逊"],
        "科技": ["科技", "互联网", "IT", "软件"],
        "金融": ["金融", "银行", "保险", "投资"],
        "医疗": ["医疗", "健康", "医药"],
        "教育": ["教育", "培训"],
    }
    for industry, keywords in industries.items():
        if any(kw.lower() in query_lower for kw in keywords):
            return industry
    return "综合"


def main():
    parser = argparse.ArgumentParser(description="创建定时情报推送任务")
    parser.add_argument("--query", required=True, help="搜索关键词")
    parser.add_argument("--schedule", required=True,
                        help="Cron 表达式，例如 '0 9 * * *' 表示每天9点")
    parser.add_argument("--channel", default="wecom",
                        choices=SUPPORTED_CHANNELS,
                        help="推送渠道")
    parser.add_argument("--timezone", default="Asia/Shanghai",
                        help="时区")
    args = parser.parse_args()

    print(f"将为以下任务创建定时推送:")
    print(f"  关键词: {args.query}")
    print(f"  执行时间: {args.schedule} ({args.timezone})")
    print(f"  推送渠道: {args.channel}")
    print()

    result = create_cron_task(args.query, args.schedule, args.channel, args.timezone)

    if result.returncode == 0:
        print("定时任务创建成功!")
        print(result.stdout)
    else:
        print("创建失败:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
