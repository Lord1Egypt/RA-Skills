#!/usr/bin/env python3
"""记忆关联图谱：话题之间的关联关系"""

import argparse
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from lib.filelock import safe_read

DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"


def build_graph(memory_dir: Path) -> dict:
    """构建话题关联图"""
    conv_dir = memory_dir / "conversations"
    if not conv_dir.exists():
        return {"nodes": [], "edges": [], "stats": {}}

    # 收集所有话题及其共现关系
    topic_dates = defaultdict(list)  # topic -> [dates]
    topic_tags = defaultdict(set)    # topic -> {tags}
    topic_keywords = defaultdict(set)  # topic -> {keywords}
    cooccurrence = defaultdict(int)   # (topic1, topic2) -> count
    all_topics = set()

    for fp in sorted(conv_dir.glob("*.md")):
        date_str = fp.stem
        content = fp.read_text(encoding="utf-8")

        # 提取当天所有话题
        topics = []
        for match in re.finditer(r'###\s*话题[：:]\s*(.+)', content):
            topic = match.group(1).strip().rstrip(".")
            topics.append(topic)
            all_topics.add(topic)
            topic_dates[topic].append(date_str)

        # 提取标签
        tags = set()
        for tl in re.findall(r'\*\*标签[：:]\*\*\s*(.+)', content):
            for t in tl.split("，"):
                t = t.strip()
                if t:
                    tags.add(t)

        # 提取关键词
        keywords = set()
        for msg in re.findall(r'\*\*用户[：:]\*\*\s*(.+)', content):
            words = re.findall(r'[\u4e00-\u9fff]{2,4}', msg)
            keywords.update(words)

        for topic in topics:
            topic_tags[topic].update(tags)
            topic_keywords[topic].update(keywords)

        # 共现
        for i in range(len(topics)):
            for j in range(i + 1, len(topics)):
                pair = tuple(sorted([topics[i], topics[j]]))
                cooccurrence[pair] += 1

    # 归一化话题
    aliases = {
        "long-memory": ["long-memory", "long memory", "记忆系统", "长记忆", "记忆skill"],
        "小说": ["小说", "novel"],
        "部署": ["部署", "推送", "git"],
        "迭代": ["迭代", "升级"],
    }
    
    normalized = {}
    for topic in all_topics:
        norm = topic
        for canonical, variants in aliases.items():
            if any(v in topic.lower() for v in variants):
                norm = canonical
                break
        if norm not in normalized:
            normalized[norm] = []
        if topic != norm:
            normalized[norm].append(topic)

    # 构建节点
    nodes = []
    for topic in sorted(all_topics):
        norm = topic
        for canonical, variants in aliases.items():
            if any(v in topic.lower() for v in variants):
                norm = canonical
                break
        nodes.append({
            "id": topic,
            "label": topic,
            "normalized": norm,
            "dates": topic_dates.get(topic, []),
            "count": len(topic_dates.get(topic, [])),
            "tags": sorted(topic_tags.get(topic, set())),
            "keywords": sorted(list(topic_keywords.get(topic, set()))[:20]),
        })

    # 构建边
    edges = []
    for (t1, t2), count in cooccurrence.items():
        edges.append({
            "source": t1,
            "target": t2,
            "weight": count,
        })

    return {
        "nodes": nodes,
        "edges": edges,
        "stats": {
            "total_topics": len(nodes),
            "total_edges": len(edges),
            "most_connected": sorted(
                [(n["label"], n["count"]) for n in nodes],
                key=lambda x: -x[1]
            )[:10],
        },
    }


def print_graph(graph: dict, verbose: bool = False):
    stats = graph["stats"]
    print("=" * 60)
    print(f"🕸️  记忆关联图谱（{stats['total_topics']} 个话题，{stats['total_edges']} 条关联）")
    print("=" * 60)

    if stats["most_connected"]:
        print("\n📊 热度排名：")
        for topic, count in stats["most_connected"]:
            bar = "█" * min(count * 3, 30)
            print(f"  {topic:25s} {count:2d}次 {bar}")

    if graph["edges"]:
        print("\n🔗 话题关联（共现关系）：")
        for edge in sorted(graph["edges"], key=lambda x: -x["weight"]):
            w = edge["weight"]
            connector = "━━" * min(w, 5)
            print(f"  {edge['source']} {connector} {edge['target']} ({w})")

    if verbose:
        print("\n📖 话题详情：")
        for node in graph["nodes"]:
            dates = node["dates"]
            date_range = f"{min(dates)} ~ {max(dates)}" if dates else "无"
            print(f"\n  📌 {node['label']} [{node['normalized']}]")
            print(f"     📅 {date_range}（{node['count']}次）")
            if node["tags"]:
                print(f"     🏷️  {', '.join(node['tags'])}")
            if node["keywords"]:
                print(f"     🔑 {', '.join(node['keywords'][:10])}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="记忆关联图谱")
    p.add_argument("--memory-dir", default=None)
    p.add_argument("--verbose", "-v", action="store_true")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    md = args.memory_dir if args.memory_dir else DEFAULT_MEMORY_DIR
    md = Path(md)
    graph = build_graph(md)

    if args.json:
        print(json.dumps(graph, ensure_ascii=False, indent=2))
    else:
        print_graph(graph, args.verbose)
