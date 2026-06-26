#!/usr/bin/env python3
"""人物关系图谱：从对话中提取人脉关系"""

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

# 关系类型关键词
RELATION_PATTERNS = {
    "同事": ["同事", "工作伙伴", "搭档", "一起工作", "同一个团队", "同组"],
    "朋友": ["朋友", "哥们", "闺蜜", "兄弟", "好友", "铁子", "小伙伴"],
    "家人": ["家人", "爸妈", "爸爸", "妈妈", "老婆", "老公", "儿子", "女儿",
             "哥哥", "姐姐", "弟弟", "妹妹", "爷爷", "奶奶", "亲戚"],
    "领导": ["老板", "领导", "上司", "主管", "经理", "总监", "CEO", "老大"],
    "客户": ["客户", "甲方", "乙方", "用户", "买家", "消费者"],
    "合作": ["合作", "合作伙伴", "协作者", "联合", "一起做", "共同"],
    "认识": ["认识", "见过", "知道", "听说过", "了解", "介绍", "推荐"],
}

# 角色关键词
ROLE_PATTERNS = {
    "开发者": ["开发", "程序员", "工程师", "码农", "技术", "写代码", "Python", "JS"],
    "设计师": ["设计", "UI", "UX", "界面", "视觉", "美工"],
    "产品": ["产品", "需求", "功能", "体验", "用户研究"],
    "运营": ["运营", "推广", "营销", "增长", "数据分析"],
    "创业者": ["创业", "创始人", "CEO", "合伙", "启动", "融资"],
}


def extract_persons(content: str) -> list[dict]:
    """从对话中提取人物提及"""
    persons = []
    seen = set()

    # 匹配人物提及模式
    patterns = [
        r'我([的爸妈妈老婆老公朋友同事同学老师]?(?:叫|认识|有个)(.{1,10}?)[，。、])',
        r'(?:跟|和|给|找|问|帮)(.{1,10}?)(?:聊|说|谈|做|问|看|帮忙|处理)',
        r'(.{2,6}?)(?:说|觉得|认为|建议|告诉|表示|提到|推荐)',
    ]

    for pattern in patterns:
        for match in re.finditer(pattern, content):
            name = match.group(1).strip()
            # 过滤明显不是人名的
            if (len(name) >= 2 and len(name) <= 8
                and name not in {"用户", "助手", "这个", "那个", "什么", "怎么"}
                and not re.match(r'^[\d\W]+$', name)
                and name not in seen):
                seen.add(name)
                persons.append({"name": name, "context": match.group(0).strip()[:80]})

    # 匹配 "某某某" 格式的人名
    for match in re.finditer(r'(?<![a-zA-Z])([一-龥]{2,4})(?=[是的说在帮跟和给])', content):
        name = match.group(1)
        if name not in seen and name not in {"用户", "助手", "这个", "那个", "什么", "怎么",
                                              "可以", "已经", "应该", "可能", "没有", "不是"}:
            seen.add(name)
            persons.append({"name": name, "context": match.group(0).strip()[:80]})

    return persons


def extract_relations(content: str, persons: list[dict]) -> list[dict]:
    """提取关系"""
    relations = []
    for person in persons:
        name = person["name"]
        context = person.get("context", "") + " " + content[:500]

        for rel_type, keywords in RELATION_PATTERNS.items():
            for kw in keywords:
                if kw in context and name in context:
                    relations.append({
                        "person": name,
                        "relation": rel_type,
                        "keyword": kw,
                    })
                    break

        # 提取角色
        for role, keywords in ROLE_PATTERNS.items():
            for kw in keywords:
                if kw in context and name in context:
                    relations.append({
                        "person": name,
                        "relation": f"角色:{role}",
                        "keyword": kw,
                    })
                    break

    return relations


def build_person_graph(memory_dir: Path, days: int | None = None) -> dict:
    """构建人物关系图谱"""
    from datetime import timedelta
    conv_dir = memory_dir / "conversations"
    if not conv_dir.exists():
        return {"persons": [], "relations": [], "groups": {}}

    cutoff = datetime.now() - timedelta(days=days) if days else None

    person_data = defaultdict(lambda: {
        "mentions": 0, "dates": set(), "contexts": [], "relations": set(), "roles": set()
    })

    for fp in sorted(conv_dir.glob("*.md")):
        if cutoff:
            try:
                file_date = datetime.strptime(fp.stem, "%Y-%m-%d")
                if file_date < cutoff:
                    continue
            except ValueError:
                continue

        content = fp.read_text(encoding="utf-8")
        persons = extract_persons(content)
        relations = extract_relations(content, persons)

        for person in persons:
            pd = person_data[person["name"]]
            pd["mentions"] += 1
            pd["dates"].add(fp.stem)
            pd["contexts"].append(person.get("context", ""))

        for rel in relations:
            pd = person_data[rel["person"]]
            if ":" in rel["relation"]:
                pd["roles"].add(rel["relation"].split(":")[1])
            else:
                pd["relations"].add(rel["relation"])

    # 构建节点和边
    nodes = []
    for name, data in sorted(person_data.items(), key=lambda x: -x[1]["mentions"]):
        if data["mentions"] >= 1:
            nodes.append({
                "name": name,
                "mentions": data["mentions"],
                "dates": sorted(data["dates"]),
                "date_range": f"{min(data['dates'])} ~ {max(data['dates'])}" if data["dates"] else "",
                "relations": sorted(data["relations"]),
                "roles": sorted(data["roles"]),
                "sample_contexts": data["contexts"][:3],
            })

    return {
        "persons": nodes,
        "total_persons": len(nodes),
        "stats": {
            "total_mentions": sum(n["mentions"] for n in nodes),
            "date_range": f"{nodes[-1]['dates'][0]} ~ {nodes[0]['dates'][-1]}" if nodes else "无",
        },
    }


def print_graph(graph: dict, verbose: bool = False):
    print("=" * 60)
    print(f"👥 人物关系图谱（{graph['total_persons']} 人）")
    print("=" * 60)

    if not graph["persons"]:
        print("\n📭 未检测到明确的人物提及")
        return

    print(f"\n📊 统计：{graph['stats']['total_mentions']} 次提及")
    print(f"📅 时间范围：{graph['stats']['date_range']}")

    for person in graph["persons"]:
        print(f"\n👤 {person['name']}（提及 {person['mentions']} 次）")
        print(f"   📅 {person['date_range']}")
        if person["relations"]:
            print(f"   🔗 关系: {', '.join(person['relations'])}")
        if person["roles"]:
            print(f"   💼 角色: {', '.join(person['roles'])}")
        if verbose and person["sample_contexts"]:
            print(f"   💬 上下文:")
            for ctx in person["sample_contexts"]:
                print(f"      \"{ctx[:60]}...\"" if len(ctx) > 60 else f"      \"{ctx}\"")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="人物关系图谱")
    p.add_argument("--memory-dir", default=None)
    p.add_argument("--days", type=int, default=None)
    p.add_argument("--verbose", "-v", action="store_true")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    md = args.memory_dir if args.memory_dir else DEFAULT_MEMORY_DIR
    md = Path(md)
    graph = build_person_graph(md, args.days)

    if args.json:
        print(json.dumps(graph, ensure_ascii=False, indent=2))
    else:
        print_graph(graph, args.verbose)
