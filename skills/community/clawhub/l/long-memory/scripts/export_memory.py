#!/usr/bin/env python3
"""记忆导出：支持 JSON / Markdown / 纯文本格式"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"


def load_all(memory_dir: Path) -> dict:
    """加载所有记忆数据"""
    data = {
        "conversations": [],
        "summaries": [],
        "distillations": [],
        "memory_md": "",
    }

    for subdir, key in [("conversations", "conversations"),
                        ("summaries", "summaries"),
                        ("distillations", "distillations")]:
        d = memory_dir / subdir
        if d.exists():
            for fp in sorted(d.glob("*.md")):
                data[key].append({
                    "file": fp.stem,
                    "content": fp.read_text(encoding="utf-8"),
                    "size": fp.stat().st_size,
                })

    memory_md = memory_dir.parent / "MEMORY.md"
    if memory_md.exists():
        data["memory_md"] = memory_md.read_text(encoding="utf-8")

    return data


def export_json(data: dict, output: Path):
    """导出为 JSON"""
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ JSON 导出 → {output} ({output.stat().st_size} bytes)")


def export_markdown(data: dict, output: Path):
    """导出为单个 Markdown"""
    lines = [f"# 记忆导出\n生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n"]

    # MEMORY.md
    if data["memory_md"]:
        lines.append("## MEMORY.md（长期记忆）\n")
        lines.append(data["memory_md"])
        lines.append("")

    # 摘要
    if data["summaries"]:
        lines.append("## 对话摘要\n")
        for s in data["summaries"]:
            lines.append(f"### {s['file']}\n")
            lines.append(s["content"])
            lines.append("")

    # 蒸馏
    if data["distillations"]:
        lines.append("## 周蒸馏\n")
        for d in data["distillations"]:
            lines.append(f"### {d['file']}\n")
            lines.append(d["content"])
            lines.append("")

    # 全量对话
    if data["conversations"]:
        lines.append("## 全量对话\n")
        for c in data["conversations"]:
            lines.append(f"### {c['file']}\n")
            lines.append(c["content"])
            lines.append("")

    output.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ Markdown 导出 → {output} ({output.stat().st_size} bytes)")


def export_text(data: dict, output: Path):
    """导出为纯文本（去掉 markdown 格式）"""
    lines = [f"记忆导出 - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
             "=" * 60, ""]

    # MEMORY.md
    if data["memory_md"]:
        lines.append("【长期记忆】")
        clean = re.sub(r'[#*\[\]]', '', data["memory_md"])
        lines.append(clean.strip())
        lines.append("")

    # 摘要
    if data["summaries"]:
        lines.append("【对话摘要】")
        for s in data["summaries"]:
            lines.append(f"--- {s['file']} ---")
            clean = re.sub(r'[#*\[\]]', '', s["content"])
            lines.append(clean.strip())
            lines.append("")

    # 对话
    if data["conversations"]:
        lines.append("【全量对话】")
        for c in data["conversations"]:
            lines.append(f"--- {c['file']} ---")
            clean = re.sub(r'[#*\[\]]', '', c["content"])
            lines.append(clean.strip())
            lines.append("")

    output.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ 纯文本导出 → {output} ({output.stat().st_size} bytes)")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="记忆导出")
    p.add_argument("--memory-dir", default=None)
    p.add_argument("--format", "-f", choices=["json", "md", "txt"], default="json")
    p.add_argument("--output", "-o", required=True, help="输出文件路径")
    args = p.parse_args()

    md = args.memory_dir if args.memory_dir else DEFAULT_MEMORY_DIR
    md = Path(md)
    data = load_all(md)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    exporters = {"json": export_json, "md": export_markdown, "txt": export_text}
    exporters[args.format](data, output)
