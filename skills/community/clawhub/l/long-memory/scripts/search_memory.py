#!/usr/bin/env python3
"""增强搜索：按时间范围、话题、标签组合筛选记忆"""

import argparse
import re
from datetime import datetime, timedelta
from pathlib import Path

DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"


def search(memory_dir: Path, query: str | None = None,
           topic: str | None = None, tag: str | None = None,
           start_date: str | None = None, end_date: str | None = None,
           days: int | None = None, max_results: int = 50) -> list[dict]:

    conv_dir = memory_dir / "conversations"
    summary_dir = memory_dir / "summaries"
    distill_dir = memory_dir / "distillations"

    # 确定日期范围
    if days:
        start = datetime.now() - timedelta(days=days)
        start_date = start.strftime("%Y-%m-%d")
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")

    results = []

    # 搜索对话文件
    if conv_dir.exists():
        for fp in sorted(conv_dir.glob("*.md")):
            if start_date and fp.stem < start_date:
                continue
            if fp.stem > end_date:
                continue
            content = fp.read_text(encoding="utf-8")

            # 标签过滤
            if tag:
                all_tags = re.findall(r'\*\*标签：\*\*\s*(.+)', content)
                found_tags = set()
                for tl in all_tags:
                    for t in tl.split("，"):
                        found_tags.add(t.strip())
                if tag.lower() not in " ".join(found_tags).lower():
                    continue

            # 话题过滤
            if topic:
                topics = re.findall(r'### 话题：(.+)', content)
                if not any(topic.lower() in t.lower() for t in topics):
                    continue

            # 关键词搜索
            if query:
                if query.lower() not in content.lower():
                    continue
                # 提取匹配的上下文（前后各 2 行）
                matches = find_context(content, query, max_results)
            else:
                matches = [{"line": line, "line_num": i}
                          for i, line in enumerate(content.split("\n"))
                          if line.strip() and not line.startswith("#")]

            if matches:
                results.append({
                    "file": fp.name,
                    "date": fp.stem,
                    "path": str(fp),
                    "matches": matches[:max_results],
                    "total_matches": len(matches),
                })

    # 搜索摘要
    if summary_dir.exists():
        for fp in sorted(summary_dir.glob("*.md")):
            if start_date and fp.stem < start_date:
                continue
            if fp.stem > end_date:
                continue
            content = fp.read_text(encoding="utf-8")
            if query and query.lower() not in content.lower():
                continue
            if tag or topic:
                continue  # 摘要不做精细过滤，避免重复
            results.append({
                "file": f"摘要/{fp.name}",
                "date": fp.stem,
                "path": str(fp),
                "matches": [{"line": l, "line_num": i}
                          for i, l in enumerate(content.split("\n"))
                          if l.strip()],
                "total_matches": 1,
            })

    return results


def find_context(content: str, query: str, max_results: int) -> list[dict]:
    """找到匹配行及其上下文"""
    lines = content.split("\n")
    matches = []
    seen_lines = set()

    for i, line in enumerate(lines):
        if query.lower() in line.lower():
            # 收集前后各 2 行
            for j in range(max(0, i - 2), min(len(lines), i + 3)):
                if j not in seen_lines:
                    seen_lines.add(j)
                    matches.append({"line": lines[j], "line_num": j})
            if len(matches) >= max_results:
                break

    return matches


def print_results(results: list[dict], query: str | None):
    if not results:
        print("📭 未找到匹配的记忆")
        return

    total_matches = sum(r["total_matches"] for r in results)
    print(f"找到 {len(results)} 个文件，{total_matches} 处匹配\n")

    for r in results:
        print(f"📄 {r['file']} ({r['total_matches']} 处匹配)")
        print(f"   路径：{r['path']}")
        for m in r["matches"][:10]:
            print(f"   L{m['line_num']:3d} │ {m['line'][:100]}")
        if r["total_matches"] > 10:
            print(f"   ... 还有 {r['total_matches'] - 10} 处")
        print()


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="增强搜索")
    p.add_argument("--memory-dir", default=None)
    p.add_argument("--query", "-q", default=None, help="关键词搜索")
    p.add_argument("--topic", "-t", default=None, help="按话题筛选")
    p.add_argument("--tag", default=None, help="按标签筛选")
    p.add_argument("--start", default=None, help="起始日期 YYYY-MM-DD")
    p.add_argument("--end", default=None, help="结束日期 YYYY-MM-DD")
    p.add_argument("--days", type=int, default=None, help="最近N天")
    p.add_argument("--max", type=int, default=50, help="最大结果数")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    md = args.memory_dir if args.memory_dir else DEFAULT_MEMORY_DIR
    md = Path(md)

    if not any([args.query, args.topic, args.tag, args.days]):
        print("❌ 请指定至少一个筛选条件：--query / --topic / --tag / --days")
        exit(1)

    results = search(md, args.query, args.topic, args.tag,
                    args.start, args.end, args.days, args.max)

    if args.json:
        import json
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print_results(results, args.query)
