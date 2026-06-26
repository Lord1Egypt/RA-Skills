#!/usr/bin/env python3
"""Meeting Minutes Extractor — 会议纪要整理"""
import argparse, sys, re
from datetime import datetime

def extract_minutes(text: str) -> str:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    sections = {"讨论": [], "决议": [], "待办": []}
    current = None
    for line in lines:
        lower = line.lower()
        if any(k in lower for k in ["讨论", "discuss", "议程"]):
            current = "讨论"
        elif any(k in lower for k in ["决议", "决定", "conclusion"]):
            current = "决议"
        elif any(k in lower for k in ["待办", "todo", "action", "任务"]):
            current = "待办"
        elif current:
            sections[current].append(f"- {line}")
    today = datetime.now().strftime("%Y-%m-%d")
    out = [f"# 会议纪要\n", f"**日期**: {today}\n", f"## 讨论\n"]
    out += sections["讨论"] or ["（未识别到讨论内容）"]
    out += ["\n## 决议\n"] + (sections["决议"] or ["（无明确决议）"])
    out += ["\n## 待办\n"] + (sections["待办"] or ["（无待办事项）"])
    out += [f"\n---\n*由 meeting-minutes-assistant 生成*"]
    return "\n".join(out)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, help="输入文件")
    p.add_argument("--output", default="", help="输出文件")
    args = p.parse_args()
    with open(args.input, encoding="utf-8") as f:
        text = f.read()
    result = extract_minutes(text)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"纪要已保存: {args.output}")
    else:
        print(result)
