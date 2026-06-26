#!/usr/bin/env python3
"""记忆导入/迁移：从 Markdown/JSON/文本批量导入"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from lib.filelock import safe_write

DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"


def import_markdown(filepath: Path, memory_dir: Path, date_override: str | None = None) -> int:
    """从 Markdown 文件导入"""
    content = filepath.read_text(encoding="utf-8")

    # 尝试从文件名提取日期
    date_str = date_override
    if not date_str:
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', filepath.stem)
        if date_match:
            date_str = date_match.group(1)
        else:
            date_str = datetime.now().strftime("%Y-%m-%d")

    conv_dir = memory_dir / "conversations"
    conv_dir.mkdir(parents=True, exist_ok=True)
    dest = conv_dir / f"{date_str}.md"

    # 如果目标已存在，追加
    if dest.exists():
        existing = dest.read_text(encoding="utf-8")
        safe_write(dest, existing + "\n\n" + content)
    else:
        safe_write(dest, f"# {date_str} 对话记录（导入自 {filepath.name}）\n" + content)

    return 1


def import_json(filepath: Path, memory_dir: Path) -> int:
    """从 JSON 文件导入"""
    data = json.loads(filepath.read_text(encoding="utf-8"))

    count = 0
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                date = item.get("date", item.get("file", datetime.now().strftime("%Y-%m-%d")))
                content = item.get("content", json.dumps(item, ensure_ascii=False))
                conv_dir = memory_dir / "conversations"
                conv_dir.mkdir(parents=True, exist_ok=True)
                dest = conv_dir / f"{date}.md"
                safe_write(dest, content)
                count += 1
    elif isinstance(data, dict):
        # 可能是 long-memory 导出格式
        for key in ["conversations", "summaries", "distillations"]:
            subdir = key.rstrip("s")
            for item in data.get(key, []):
                if isinstance(item, dict):
                    target_dir = memory_dir / key
                    target_dir.mkdir(parents=True, exist_ok=True)
                    dest = target_dir / item.get("file", "imported.md")
                    safe_write(dest, item.get("content", ""))
                    count += 1

    return count


def import_text(filepath: Path, memory_dir: Path, date_override: str | None = None) -> int:
    """从纯文本文件导入（按对话轮次分割）"""
    content = filepath.read_text(encoding="utf-8")
    date_str = date_override or datetime.now().strftime("%Y-%m-%d")

    lines = content.split("\n")
    messages = []
    current_speaker = None
    current_msg = []

    for line in lines:
        # 简单启发式：检测对话轮次
        user_match = re.match(r'(?:用户|我|You|U)\s*[：:>]\s*(.+)', line)
        assistant_match = re.match(r'(?:助手|AI|Bot|B)\s*[：:>]\s*(.+)', line)

        if user_match:
            if current_speaker and current_msg:
                messages.append((current_speaker, "\n".join(current_msg)))
            current_speaker = "用户"
            current_msg = [user_match.group(1)]
        elif assistant_match:
            if current_speaker and current_msg:
                messages.append((current_speaker, "\n".join(current_msg)))
            current_speaker = "助手"
            current_msg = [assistant_match.group(1)]
        elif current_speaker:
            current_msg.append(line)

    if current_speaker and current_msg:
        messages.append((current_speaker, "\n".join(current_msg)))

    if not messages:
        # 无法分割，整段作为一条消息
        messages = [("用户", content)]

    # 格式化为记忆格式
    formatted = f"# {date_str} 对话记录（导入自 {filepath.name}）\n\n"
    formatted += f"## [导入] Session: import\n### 话题：导入的对话\n\n"
    for speaker, msg in messages:
        label = "用户" if speaker == "用户" else "助手"
        formatted += f"**{label}：** {msg}\n\n"

    conv_dir = memory_dir / "conversations"
    conv_dir.mkdir(parents=True, exist_ok=True)
    dest = conv_dir / f"{date_str}.md"
    safe_write(dest, formatted)

    return 1


def import_directory(dir_path: Path, memory_dir: Path, pattern: str = "*.md") -> int:
    """批量导入目录"""
    count = 0
    for fp in sorted(dir_path.glob(pattern)):
        if fp.suffix == ".md":
            count += import_markdown(fp, memory_dir)
        elif fp.suffix == ".json":
            count += import_json(fp, memory_dir)
        elif fp.suffix == ".txt":
            count += import_text(fp, memory_dir)
        print(f"  ✅ 导入: {fp.name}")
    return count


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="记忆导入/迁移")
    sub = p.add_subparsers(dest="command")

    # 单文件导入
    imp = sub.add_parser("import", help="导入文件")
    imp.add_argument("file", help="文件路径")
    imp.add_argument("--memory-dir", default=None)
    imp.add_argument("--date", default=None, help="指定日期")
    imp.add_argument("--format", choices=["auto", "markdown", "json", "text"], default="auto")

    # 批量导入
    batch = sub.add_parser("batch", help="批量导入目录")
    batch.add_argument("directory", help="目录路径")
    batch.add_argument("--memory-dir", default=None)
    batch.add_argument("--pattern", default="*.md", help="文件匹配模式")

    args = p.parse_args()

    md = args.memory_dir if args.memory_dir else DEFAULT_MEMORY_DIR
    md = Path(md)

    if args.command == "import":
        fp = Path(args.file)
        fmt = args.format
        if fmt == "auto":
            fmt = "json" if fp.suffix == ".json" else "text" if fp.suffix == ".txt" else "markdown"

        if fmt == "markdown":
            count = import_markdown(fp, md, args.date)
        elif fmt == "json":
            count = import_json(fp, md)
        else:
            count = import_text(fp, md, args.date)

        print(f"✅ 导入完成：{count} 个文件")

    elif args.command == "batch":
        count = import_directory(Path(args.directory), md, args.pattern)
        print(f"✅ 批量导入完成：{count} 个文件")
    else:
        p.print_help()
