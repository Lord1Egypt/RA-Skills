#!/usr/bin/env python3
"""生成新目录说明表。"""

from __future__ import annotations

import argparse
from pathlib import Path

from orglib import configure_stdout, default_directory_rows, markdown_table


def build_markdown(root: str | None) -> str:
    title = "# 新目录说明表"
    lines = [title, ""]
    if root:
        lines.append(f"- 根目录：`{root}`")
        lines.append("")
    lines.append(markdown_table(["目录", "中文名称", "用途", "放什么", "不放什么", "维护周期"], default_directory_rows()))
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    configure_stdout()
    parser = argparse.ArgumentParser(description="生成新目录说明表。")
    parser.add_argument("--root", help="目录根路径")
    parser.add_argument("--output", help="输出文件")
    args = parser.parse_args()

    text = build_markdown(args.root)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
