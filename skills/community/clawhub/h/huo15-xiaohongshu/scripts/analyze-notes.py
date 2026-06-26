#!/usr/bin/env python3
"""离线分析已抓取的笔记数据集。

输入：scrape-note / scrape-user / 手工整理后得到的 JSON / JSONL。
输出：Markdown 报告（默认），或者完整 JSON。

    python3 analyze-notes.py --input notes.jsonl --format md --out report.md
    python3 analyze-notes.py --input notes.json --format json --out report.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from xhs_analyzer import (  # noqa: E402
    full_report,
    load_notes,
    report_to_markdown,
)


def main() -> int:
    ap = argparse.ArgumentParser(description="离线分析小红书笔记数据集")
    ap.add_argument("--input", "-i", required=True, help="JSON 数组或 JSONL 文件")
    ap.add_argument("--format", choices=["md", "json"], default="md")
    ap.add_argument("--out", "-o", default="", help="输出路径；省略则 stdout")
    args = ap.parse_args()

    notes = load_notes(args.input)
    if not notes:
        print("输入数据为空或解析失败。", file=sys.stderr)
        return 1

    # 支持 {"results": [...]} 这种 wrapper
    if isinstance(notes, list) and notes and isinstance(notes[0], dict) and "results" in notes[0] and "note_id" not in notes[0]:
        notes = notes[0]["results"]

    report = full_report(notes)

    if args.format == "json":
        output = json.dumps(report, ensure_ascii=False, indent=2)
    else:
        output = report_to_markdown(report)

    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"✓ 报告已写入 {args.out}（样本 {report['sample_size']} 条）")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
