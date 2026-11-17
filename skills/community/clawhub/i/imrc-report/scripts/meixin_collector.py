#!/usr/bin/env python3
"""
美信消息收集脚本

收集装备所相关的美信消息，用于运营报告中的团队协作、技术分享、人员变动等摘要。
"""

import json
import os
import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# 配置路径
SKILL_DIR = Path(__file__).parent.parent
CONFIG_DIR = SKILL_DIR / "config"
PAGES_CONFIG = CONFIG_DIR / "pages.json"


def load_filter_config():
    """加载筛选配置"""
    with open(PAGES_CONFIG, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config.get("filter", "装备所|智能装备研究所|智能装备")


def get_data_dir():
    """获取数据存储目录"""
    workspace = Path(__file__).parent.parent.parent.parent
    data_dir = workspace / "memory" / "imrc_data" / "meixin"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def collect_meixin_messages(days=30, filter_keywords=None):
    """
    收集美信消息
    
    Args:
        days: 收集最近多少天的消息
        filter_keywords: 筛选关键词（正则表达式）
    
    Returns:
        list: 消息列表
    """
    if filter_keywords is None:
        filter_keywords = load_filter_config()
    
    print(f"[收集] 美信消息 (最近 {days} 天)")
    print(f"[筛选] 关键词: {filter_keywords}")
    
    # 模拟消息收集（实际使用时通过 tdai_conversation_search 或 API）
    messages = []
    
    # 消息分类
    categories = {
        "团队协作": [],
        "技术分享": [],
        "人员变动": [],
        "项目进展": [],
        "其他": []
    }
    
    result = {
        "collected_at": datetime.now().isoformat(),
        "days": days,
        "filter": filter_keywords,
        "total_count": len(messages),
        "categories": categories,
        "messages": messages
    }
    
    return result


def save_meixin_data(data, output_dir=None):
    """保存美信数据"""
    if output_dir is None:
        output_dir = get_data_dir()
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_file = output_dir / f"meixin_{date_str}.json"
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"  -> 已保存: {output_file}")
    return output_file


def generate_meixin_summary(data):
    """
    生成美信消息摘要
    
    Args:
        data: 美信消息数据
    
    Returns:
        str: Markdown 格式摘要
    """
    summary = "## 美信消息摘要\n\n"
    
    categories = data.get("categories", {})
    for cat_name, messages in categories.items():
        if messages:
            summary += f"### {cat_name}\n\n"
            for msg in messages[:5]:  # 每类最多5条
                summary += f"- {msg.get('title', '无标题')}\n"
            summary += "\n"
    
    if not any(categories.values()):
        summary += "暂无相关消息。\n"
    
    return summary


def main():
    parser = argparse.ArgumentParser(description="美信消息收集")
    parser.add_argument("--days", type=int, default=30, help="收集最近多少天的消息")
    parser.add_argument("--filter", type=str, help="筛选关键词（正则）")
    parser.add_argument("--output", type=str, help="输出目录")
    args = parser.parse_args()
    
    print("=== 美信消息收集 ===\n")
    
    data = collect_meixin_messages(days=args.days, filter_keywords=args.filter)
    save_meixin_data(data, output_dir=args.output)
    
    print(f"\n[完成] 共收集 {data['total_count']} 条消息")


if __name__ == "__main__":
    main()
