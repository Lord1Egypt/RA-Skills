#!/usr/bin/env python3
"""归档对话到 memory/conversations/YYYY-MM-DD.md"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"


def resolve_memory_dir(memory_dir: str | None) -> Path:
    if memory_dir:
        return Path(memory_dir)
    if DEFAULT_MEMORY_DIR.exists():
        return DEFAULT_MEMORY_DIR
    # 向上查找 workspace
    p = Path.cwd()
    for _ in range(5):
        if (p / "memory").is_dir():
            return p / "memory"
        p = p.parent
    return DEFAULT_MEMORY_DIR


def archive(date_str: str, session: str, topic: str, content: str | None,
            memory_dir: Path, metadata: dict | None = None):
    conv_dir = memory_dir / "conversations"
    conv_dir.mkdir(parents=True, exist_ok=True)
    filepath = conv_dir / f"{date_str}.md"
    now = datetime.now().strftime("%H:%M")

    entry = f"\n## [{now}] Session: {session}\n### 话题：{topic}\n\n"
    if metadata:
        entry += f"**标签：** {', '.join(metadata.get('tags', []))}\n\n"
    if content:
        entry += content
    else:
        entry += "(等待对话内容填充)\n"

    if filepath.exists():
        existing = filepath.read_text(encoding="utf-8")
        filepath.write_text(existing + entry, encoding="utf-8")
    else:
        filepath.write_text(f"# {date_str} 对话记录\n{entry}", encoding="utf-8")

    print(f"✅ 已归档到 {filepath}")
    return str(filepath)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="归档对话")
    p.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"))
    p.add_argument("--session", required=True)
    p.add_argument("--topic", required=True)
    p.add_argument("--input", help="对话内容文件路径")
    p.add_argument("--memory-dir", default=None, help="记忆目录路径")
    p.add_argument("--tags", default="", help="标签，逗号分隔")
    args = p.parse_args()

    content = None
    if args.input:
        content = Path(args.input).read_text(encoding="utf-8")
    elif not sys.stdin.isatty():
        content = sys.stdin.read()

    metadata = {"tags": [t.strip() for t in args.tags.split(",") if t.strip()]} if args.tags else None
    md = resolve_memory_dir(args.memory_dir)
    archive(args.date, args.session, args.topic, content, md, metadata)
