#!/usr/bin/env python3
"""新 session 预加载：生成最近记忆摘要，供 session 启动时快速恢复上下文"""

import argparse
import re
from datetime import datetime, timedelta
from pathlib import Path

DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
CONTEXT_FILE = Path.home() / ".openclaw" / "workspace" / "memory" / "recent_context.md"


def generate_recent_context(memory_dir: Path, days: int = 7) -> str:
    """生成最近 N 天的记忆摘要"""
    conv_dir = memory_dir / "conversations"
    summary_dir = memory_dir / "summaries"
    memory_md = memory_dir.parent / "MEMORY.md"

    cutoff = datetime.now() - timedelta(days=days)
    context_parts = [f"# 最近 {days} 天记忆摘要（自动生成）\n"]
    context_parts.append(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

    # 1. 优先加载已有的摘要
    if summary_dir.exists():
        for fp in sorted(summary_dir.glob("*.md")):
            try:
                file_date = datetime.strptime(fp.stem, "%Y-%m-%d")
            except ValueError:
                continue
            if file_date >= cutoff:
                context_parts.append(f"\n## {fp.stem}\n")
                content = fp.read_text(encoding="utf-8")
                # 提取摘要部分
                in_summary = False
                for line in content.split("\n"):
                    if line.startswith("## 摘要"):
                        in_summary = True
                        continue
                    if in_summary and line.startswith("## "):
                        break
                    if in_summary:
                        context_parts.append(line)

    # 2. 对话文件中提取关键信息（补充摘要没有的日期）
    if conv_dir.exists():
        for fp in sorted(conv_dir.glob("*.md"), reverse=True):
            try:
                file_date = datetime.strptime(fp.stem, "%Y-%m-%d")
            except ValueError:
                continue
            if file_date >= cutoff:
                # 检查是否已有摘要
                summary_fp = summary_dir / fp.name if summary_dir.exists() else None
                if summary_fp and summary_fp.exists():
                    continue

                content = fp.read_text(encoding="utf-8")
                topics = re.findall(r'### 话题：(.+)', content)
                tags = re.findall(r'\*\*标签：\*\*\s*(.+)', content)
                decisions = [l.strip() for l in content.split("\n")
                           if l.strip().startswith("**关键决策")]

                context_parts.append(f"\n## {fp.stem}\n")
                if topics:
                    unique = []
                    for t in topics:
                        if t.strip() not in unique:
                            unique.append(t.strip())
                    context_parts.append(f"话题：{', '.join(unique)}")
                if tags:
                    all_tags = set()
                    for tl in tags:
                        for t in tl.split("，"):
                            t = t.strip()
                            if t:
                                all_tags.add(t)
                    context_parts.append(f"标签：{', '.join(sorted(all_tags))}")
                if decisions:
                    context_parts.append("决策：")
                    for d in decisions[:3]:
                        context_parts.append(f"  {d}")

    # 3. 追加 MEMORY.md 的前 20 行（长期记忆概览）
    if memory_md.exists():
        context_parts.append("\n## 长期记忆概览\n")
        lines = memory_md.read_text(encoding="utf-8").split("\n")[:20]
        context_parts.extend(lines)

    return "\n".join(context_parts)


def save_context(context: str, memory_dir: Path):
    """保存上下文文件"""
    CONTEXT_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONTEXT_FILE.write_text(context, encoding="utf-8")
    print(f"✅ 上下文已生成 → {CONTEXT_FILE}")
    print(f"   大小：{len(context)} 字符")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="生成最近记忆上下文")
    p.add_argument("--memory-dir", default=None)
    p.add_argument("--days", type=int, default=7, help="最近N天（默认7）")
    p.add_argument("--output", "-o", default=None, help="输出文件路径")
    args = p.parse_args()

    md = args.memory_dir if args.memory_dir else DEFAULT_MEMORY_DIR
    md = Path(md)

    context = generate_recent_context(md, args.days)

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(context, encoding="utf-8")
        print(f"✅ 上下文已生成 → {out}")
    else:
        save_context(context, md)
