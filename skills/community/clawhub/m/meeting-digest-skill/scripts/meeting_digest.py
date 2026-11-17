#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""会议周报/复盘自动生成器 - 离线聚合脚本。

读取一个目录下的多份会议纪要素材(.md/.txt)，抽取结论/决策/行动项/风险，
做跨会议去重与归并，输出 Markdown 周报、复盘或行动项清单。

纯标准库实现，零第三方依赖。用于支撑 meeting-digest-skill 的"可独立运行"。
"""

import argparse
import os
import re
import sys
from collections import defaultdict
from datetime import date, timedelta


def read_notes(input_dir):
    """读取目录下所有 .md/.txt 纪要素材，返回 [(文件名, 文本)]。"""
    notes = []
    for name in sorted(os.listdir(input_dir)):
        if name.lower().endswith((".md", ".txt")):
            path = os.path.join(input_dir, name)
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                notes.append((name, f.read()))
    return notes


def split_sections(text):
    """按 Markdown 标题切分，返回 {标题: 内容}。"""
    sections = {}
    cur_title = "(无标题)"
    cur_lines = []
    for line in text.splitlines():
        m = re.match(r"^#{1,6}\s+(.*)$", line)
        if m:
            sections[cur_title] = "\n".join(cur_lines).strip()
            cur_title = m.group(1).strip()
            cur_lines = []
        else:
            cur_lines.append(line)
    sections[cur_title] = "\n".join(cur_lines).strip()
    return sections


def body_lines(section_text):
    """提取段落中的非标题条目行，去掉列表符号。"""
    items = []
    for line in section_text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        s = re.sub(r"^[-*]\s*", "", s)
        s = re.sub(r"^\d+[.、]\s*", "", s)
        if s:
            items.append(s)
    return items


def collect(notes):
    """从所有素材中按章节标题归类抽取结构化信息。"""
    conclusions, decisions, actions, risks = [], [], [], []
    meeting_titles = []
    for fname, text in notes:
        meeting_titles.append(fname)
        sections = split_sections(text)
        for title, body in sections.items():
            t = title
            if any(k in t for k in ("结论", "要点", "总结", "产出")):
                conclusions += body_lines(body)
            if any(k in t for k in ("决策", "决定", "拍板")):
                decisions += body_lines(body)
            if any(k in t for k in ("行动项", "待办", "跟进")) or "todo" in t.lower():
                actions += body_lines(body)
            if any(k in t for k in ("风险", "问题", "阻塞", "待决", "待确认", "升级")):
                risks += body_lines(body)
    return {
        "meetings": meeting_titles,
        "conclusions": conclusions,
        "decisions": decisions,
        "actions": actions,
        "risks": risks,
    }


def dedupe(items):
    """简单去重：忽略空白与只差标点的重复。"""
    seen = set()
    out = []
    for it in items:
        key = re.sub(r"\s+", "", it)
        if key and key not in seen:
            seen.add(key)
            out.append(it)
    return out


def render_weekly(data, title):
    lines = [f"# {title}", ""]
    lines.append("## 一、本周概览")
    lines.append(f"- 共汇总会议素材 {len(data['meetings'])} 份：{', '.join(data['meetings'])}")
    lines.append(f"- 关键结论 {len(data['conclusions'])} 条，行动项 {len(data['actions'])} 条，风险 {len(data['risks'])} 条")
    lines.append("")
    lines.append("## 二、关键结论")
    for c in data["conclusions"][:8]:
        lines.append(f"- {c}")
    lines.append("")
    lines.append("## 三、行动项（去重后）")
    for a in dedupe(data["actions"])[:15]:
        lines.append(f"- {a}  （待确认来源）" if "待确认" not in a else f"- {a}")
    lines.append("")
    lines.append("## 四、风险与待决")
    for r in dedupe(data["risks"])[:10]:
        lines.append(f"- {r}")
    lines.append("")
    lines.append("## 五、下周重点")
    lines.append("- 由上述行动项与开放问题推导，建议负责人在周会上对齐 DDL。")
    lines.append("")
    lines.append("> 本报表由 meeting-digest-skill 自动聚合，标注「待确认」的项请人工核对来源后再发出。")
    return "\n".join(lines)


def render_retrospective(data, title):
    lines = [f"# {title}", ""]
    lines.append("## 进展")
    for c in data["conclusions"][:8]:
        lines.append(f"- {c}")
    lines.append("")
    lines.append("## 决策")
    for d in dedupe(data["decisions"])[:8]:
        lines.append(f"- {d}")
    lines.append("")
    lines.append("## 行动项（去重）")
    for a in dedupe(data["actions"])[:15]:
        lines.append(f"- {a}")
    lines.append("")
    lines.append("## 风险与待决")
    for r in dedupe(data["risks"])[:10]:
        lines.append(f"- {r}")
    lines.append("")
    lines.append("> 复盘由 meeting-digest-skill 自动生成，结论请以原始纪要为准。")
    return "\n".join(lines)


def render_actions(data, title):
    lines = [f"# {title}", ""]
    lines.append("| 行动项 | 备注 |")
    lines.append("|--------|------|")
    for a in dedupe(data["actions"])[:20]:
        lines.append(f"| {a} | 待确认负责人/DDL |")
    lines.append("")
    return "\n".join(lines)


def default_title(mode):
    today = date.today()
    if mode == "weekly":
        monday = today - timedelta(days=today.weekday())
        sunday = monday + timedelta(days=6)
        return f"周报 · {monday} ~ {sunday}"
    if mode == "retrospective":
        return f"复盘报告 · {today}"
    return f"行动项清单 · {today}"


def main():
    ap = argparse.ArgumentParser(description="会议纪要素材聚合器")
    ap.add_argument("--input-dir", default=".", help="纪要素材目录")
    ap.add_argument("--mode", choices=["weekly", "retrospective", "actions"], default="weekly")
    ap.add_argument("--output", default="digest.md")
    ap.add_argument("--title", default=None)
    args = ap.parse_args()

    if not os.path.isdir(args.input_dir):
        print(f"错误：目录不存在 {args.input_dir}", file=sys.stderr)
        sys.exit(1)

    notes = read_notes(args.input_dir)
    if not notes:
        print(f"错误：{args.input_dir} 下未找到 .md/.txt 素材", file=sys.stderr)
        sys.exit(1)

    data = collect(notes)
    title = args.title or default_title(args.mode)
    if args.mode == "weekly":
        out = render_weekly(data, title)
    elif args.mode == "retrospective":
        out = render_retrospective(data, title)
    else:
        out = render_actions(data, title)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"已生成 {args.mode} 报告：{args.output}（素材 {len(notes)} 份）")


if __name__ == "__main__":
    main()
