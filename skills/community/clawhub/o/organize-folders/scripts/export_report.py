#!/usr/bin/env python3
"""整合扫描、规则、计划、日志和目录说明表为最终报告。"""

from __future__ import annotations

import argparse
from pathlib import Path

from orglib import configure_stdout, now_iso


def main() -> None:
    configure_stdout()
    parser = argparse.ArgumentParser(description="导出文件夹整理报告。")
    parser.add_argument("--title", default="文件夹整理报告")
    parser.add_argument("--section", action="append", default=[], help="章节，格式：标题=文件路径")
    parser.add_argument("--output", required=True, help="输出 Markdown 文件")
    args = parser.parse_args()

    lines = [f"# {args.title}", "", f"- 生成时间：`{now_iso()}`", ""]
    for value in args.section:
        if "=" not in value:
            raise SystemExit(f"--section 格式错误：{value}")
        title, file_path = value.split("=", 1)
        path = Path(file_path)
        lines.extend([f"## {title}", ""])
        if path.exists():
            lines.append(path.read_text(encoding="utf-8"))
        else:
            lines.append(f"> 文件不存在：`{path}`")
        lines.append("")

    Path(args.output).write_text("\n".join(lines), encoding="utf-8")
    print(f"报告已生成：{args.output}")


if __name__ == "__main__":
    main()
