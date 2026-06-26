#!/usr/bin/env python3
"""标签体系优化：合并相似标签，统计标签热度"""

import argparse
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"

# 已知的标签归一化映射
TAG_ALIASES = {
    "日常": ["日常", "闲聊"],
    "skill": ["skill", "技能包", "skills"],
    "记忆": ["记忆", "memory", "long-memory"],
    "小说": ["小说", "novel", "novel-writer"],
    "代码": ["代码", "code", "脚本", "开发"],
    "部署": ["部署", "deploy", "git", "github"],
    "决策": ["决策", "decision"],
    "赚钱": ["赚钱", "商业化", "变现"],
    "技术方案": ["技术方案", "技术", "方案"],
}


def load_all_tags(memory_dir: Path) -> tuple[Counter, dict]:
    """加载所有标签及其出现日期"""
    counter = Counter()
    tag_dates = defaultdict(set)

    conv_dir = memory_dir / "conversations"
    if not conv_dir.exists():
        return counter, tag_dates

    for fp in sorted(conv_dir.glob("*.md")):
        date_str = fp.stem
        content = fp.read_text(encoding="utf-8")
        for tag_line in re.findall(r'\*\*标签：\*\*\s*(.+)', content):
            for tag in tag_line.split("，"):
                tag = tag.strip()
                if tag:
                    counter[tag] += 1
                    tag_dates[tag].add(date_str)

    return counter, tag_dates


def normalize_tag(tag: str) -> str:
    """归一化标签"""
    tag_lower = tag.lower().strip()
    for canonical, aliases in TAG_ALIASES.items():
        for alias in aliases:
            if tag_lower == alias.lower():
                return canonical
    return tag


def get_merge_suggestions(counter: Counter, tag_dates: dict) -> list[dict]:
    """生成标签合并建议"""
    # 按归一化分组
    groups = defaultdict(list)
    for tag, count in counter.items():
        norm = normalize_tag(tag)
        groups[norm].append((tag, count))

    suggestions = []
    for canonical, variants in groups.items():
        if len(variants) > 1:
            total = sum(c for _, c in variants)
            dates = set()
            for tag, _ in variants:
                dates.update(tag_dates.get(tag, set()))
            suggestions.append({
                "canonical": canonical,
                "variants": [(t, c) for t, c in variants],
                "total_count": total,
                "date_range": f"{min(dates)} ~ {max(dates)}" if dates else "未知",
            })

    return sorted(suggestions, key=lambda x: -x["total_count"])


def apply_normalization(memory_dir: Path, dry_run: bool = True):
    """应用标签归一化"""
    conv_dir = memory_dir / "conversations"
    if not conv_dir.exists():
        print("📭 没有对话记录")
        return

    changes = 0
    for fp in sorted(conv_dir.glob("*.md")):
        content = fp.read_text(encoding="utf-8")
        original = content

        for line in content.split("\n"):
            if "**标签：**" not in line:
                continue
            tag_match = re.match(r'(\*\*标签：\*\*\s*)(.+)', line)
            if not tag_match:
                continue
            prefix = tag_match.group(1)
            tags = [t.strip() for t in tag_match.group(2).split("，") if t.strip()]
            normalized = []
            for tag in tags:
                norm = normalize_tag(tag)
                if norm != tag:
                    changes += 1
                normalized.append(norm)
            # 去重
            seen = set()
            unique = []
            for t in normalized:
                if t not in seen:
                    seen.add(t)
                    unique.append(t)
            new_line = f"{prefix}{', '.join(unique)}"
            content = content.replace(line, new_line)

        if content != original:
            if dry_run:
                print(f"  [预览] {fp.name}: {changes} 处标签变更")
            else:
                fp.write_text(content, encoding="utf-8")
                print(f"  ✅ {fp.name}: {changes} 处标签变更")

    if changes == 0:
        print("✅ 所有标签已规范化，无需变更")
    elif dry_run:
        print(f"\n🔍 发现 {changes} 处标签变更（使用 --execute 应用）")


def print_stats(counter: Counter, tag_dates: dict, suggestions: list):
    print("=" * 60)
    print("🏷️  标签体系分析")
    print("=" * 60)

    print(f"\n📊 标签总数：{len(counter)} 个")
    total = sum(counter.values())
    print(f"📌 标签使用：{total} 次")

    print(f"\n🔥 热度排名：")
    for tag, count in counter.most_common():
        dates = tag_dates.get(tag, set())
        date_range = f"{min(dates)} ~ {max(dates)}" if dates else "-"
        bar = "█" * min(count, 30)
        print(f"  {tag:15s} {count:3d}次 {bar}  ({date_range})")

    if suggestions:
        print(f"\n💡 合并建议（{len(suggestions)} 组）：")
        for s in suggestions:
            variants_str = "、".join(f"{t}({c})" for t, c in s["variants"])
            print(f"  → {s['canonical']}: {variants_str}")
            print(f"    合计 {s['total_count']} 次，{s['date_range']}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="标签体系优化")
    p.add_argument("--memory-dir", default=None)
    p.add_argument("--apply", "--execute", action="store_true", help="应用归一化")
    p.add_argument("--dry-run", action="store_true", default=True)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    md = args.memory_dir if args.memory_dir else DEFAULT_MEMORY_DIR
    md = Path(md)

    counter, tag_dates = load_all_tags(md)
    suggestions = get_merge_suggestions(counter, tag_dates)

    if args.json:
        import json
        print(json.dumps({
            "total_tags": len(counter),
            "total_usages": sum(counter.values()),
            "counter": dict(counter.most_common()),
            "suggestions": suggestions,
        }, ensure_ascii=False, indent=2))
    else:
        print_stats(counter, tag_dates, suggestions)
        if args.apply:
            print()
            apply_normalization(md, dry_run=False)
        elif suggestions:
            print()
            apply_normalization(md, dry_run=True)
