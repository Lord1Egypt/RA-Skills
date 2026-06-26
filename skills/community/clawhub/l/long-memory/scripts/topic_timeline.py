#!/usr/bin/env python3
"""话题时间线：按话题聚合对话，展示完整讨论脉络"""

import argparse
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path

DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"


def build_timeline(memory_dir: Path, topic_filter: str | None = None,
                   days: int | None = None) -> dict:
    """构建话题时间线"""
    conv_dir = memory_dir / "conversations"
    if not conv_dir.exists():
        return {}

    timeline = defaultdict(list)

    for fp in sorted(conv_dir.glob("*.md")):
        date_str = fp.stem

        # 按天数过滤
        if days:
            try:
                file_date = datetime.strptime(date_str, "%Y-%m-%d")
                cutoff = datetime.now() - __import__("datetime").timedelta(days=days)
                if file_date < cutoff:
                    continue
            except ValueError:
                continue

        content = fp.read_text(encoding="utf-8")
        current_topic = "未知"
        current_time = ""
        current_messages = []
        current_tags = []

        for line in content.split("\n"):
            # 检测 session 头
            if line.startswith('## ['):
                time_match = re.match(r'##\s*\[(\d{2}:\d{2})\]', line)
                if time_match and current_messages and current_topic != "未知":
                    save_topic(timeline, date_str, current_time, current_topic,
                              current_tags, current_messages)
                if time_match:
                    current_time = time_match.group(1)
                current_messages = []
                current_tags = []
                continue

            # 检测话题头（在 session 头的下一行）
            if line.startswith('### 话题：'):
                current_topic = re.sub(r'^###\s*话题：\s*', '', line).strip()
                continue

            # 检测标签
            tag_match = re.match(r'\*\*标签：\*\*\s*(.+)', line)
            if tag_match:
                current_tags = [t.strip() for t in tag_match.group(1).split("，") if t.strip()]
                continue

            # 收集消息
            if "**用户：**" in line or "**助手：**" in line:
                clean = re.sub(r'\*\*(用户|助手)[：:]\*\*\s*', r'\1：', line).strip()
                if clean:
                    current_messages.append(f"[{current_time}] {clean}")

        # 保存最后一段
        if current_messages and current_topic != "未知":
            save_topic(timeline, date_str, current_time, current_topic,
                      current_tags, current_messages)

    # 按话题过滤
    if topic_filter:
        filtered = {}
        for topic, entries in timeline.items():
            if topic_filter.lower() in topic.lower():
                filtered[topic] = entries
            else:
                matching = [e for e in entries
                           if topic_filter.lower() in " ".join(e.get("tags", [])).lower()]
                if matching:
                    filtered[topic] = matching
        timeline = filtered

    return dict(sorted(timeline.items()))


def save_topic(timeline: dict, date: str, time: str, topic: str,
               tags: list, messages: list):
    # 合并相似话题
    normalized = normalize_topic(topic)
    key = normalized if normalized else topic

    timeline[key].append({
        "date": date,
        "time": time,
        "original_topic": topic,
        "tags": tags,
        "messages": messages,
    })


def normalize_topic(topic: str) -> str:
    """归一化相似话题"""
    topic_lower = topic.lower()
    # 已知的归一化映射
    mappings = {
        "long-memory": ["long-memory skill", "记忆系统", "长记忆", "记忆 skill", "long memory"],
        "小说": ["小说", "novel-writer", "novel writer", "写作"],
        "赚钱": ["赚钱", "商业化", "变现"],
        "部署": ["部署", "推送", "github", "git push"],
        "迭代": ["迭代", "升级", "v2", "v3"],
    }
    for canonical, variants in mappings.items():
        for v in variants:
            if v in topic_lower:
                return canonical
    # 去掉末尾的省略号
    return topic.rstrip(".")


def print_timeline(timeline: dict, verbose: bool = False):
    if not timeline:
        print("📭 没有找到相关话题的记录")
        return

    print("=" * 60)
    print(f"📋 话题时间线（共 {len(timeline)} 个话题）")
    print("=" * 60)

    for topic, entries in timeline.items():
        dates = sorted(set(e["date"] for e in entries))
        print(f"\n📌 {topic}")
        print(f"   📅 {dates[0]} ~ {dates[-1]}（{len(entries)} 次讨论）")

        all_tags = set()
        for e in entries:
            all_tags.update(e["tags"])
        if all_tags:
            print(f"   🏷️  {', '.join(sorted(all_tags))}")

        if verbose:
            for e in entries:
                print(f"\n   [{e['date']} {e['time']}] {e['original_topic']}")
                for msg in e["messages"]:
                    print(f"      {msg}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="话题时间线")
    p.add_argument("--memory-dir", default=None)
    p.add_argument("--topic", "-t", default=None, help="按话题筛选")
    p.add_argument("--days", type=int, default=None, help="最近N天")
    p.add_argument("--verbose", "-v", action="store_true", help="显示完整对话")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    md = args.memory_dir if args.memory_dir else DEFAULT_MEMORY_DIR
    md = Path(md)
    timeline = build_timeline(md, args.topic, args.days)

    if args.json:
        import json
        print(json.dumps(timeline, ensure_ascii=False, indent=2, default=str))
    else:
        print_timeline(timeline, args.verbose)
