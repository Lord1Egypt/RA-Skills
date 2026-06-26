#!/usr/bin/env python3
"""生成对话摘要：从全量对话中提取 3-5 句精华摘要"""

import argparse
import re
from datetime import datetime
from pathlib import Path

DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"


def load_conversation(date_str: str, memory_dir: Path) -> str | None:
    fp = memory_dir / "conversations" / f"{date_str}.md"
    if fp.exists():
        return fp.read_text(encoding="utf-8")
    return None


def extract_user_messages(text: str) -> list[str]:
    """提取所有用户消息"""
    msgs = []
    for line in text.split("\n"):
        if "**用户：**" in line:
            clean = re.sub(r'\*\*用户：\*\*\s*', '', line).strip()
            if clean and len(clean) > 2:
                msgs.append(clean)
    return msgs


def extract_assistant_key_points(text: str) -> list[str]:
    """提取助手的关键结论"""
    points = []
    in_decision = False
    for line in text.split("\n"):
        line = line.strip()
        if "**关键决策" in line or "**重要" in line:
            in_decision = True
            points.append(line)
        elif in_decision:
            if line.startswith("- ") or line.startswith("**"):
                points.append(line)
            elif line.startswith("##") or line.startswith("#"):
                in_decision = False
        # 提取 ✅ 或确认类回复
        if "搞定" in line or "完成" in line or "已推送" in line or "已创建" in line:
            clean = re.sub(r'\*\*助手[：:]\*\*\s*', '', line).strip()
            if clean:
                points.append(clean)
    return points


def generate_summary(text: str) -> dict:
    """生成结构化摘要"""
    user_msgs = extract_user_messages(text)
    key_points = extract_assistant_key_points(text)

    # 提取话题
    topics = re.findall(r'### 话题：(.+)', text)

    # 提取标签
    tags = set()
    for tag_line in re.findall(r'\*\*标签：\*\*\s*(.+)', text):
        for tag in tag_line.split("，"):
            tag = tag.strip()
            if tag:
                tags.add(tag)

    # 提取待办
    todos = []
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("- [ ]"):
            todos.append(line)

    # 生成 3-5 句摘要
    summaries = []

    # 话题概述
    if topics:
        unique_topics = []
        for t in topics:
            t = t.strip()
            if t not in unique_topics:
                unique_topics.append(t)
        if unique_topics:
            summaries.append(f"讨论了 {len(unique_topics)} 个话题：{'、'.join(unique_topics)}")

    # 关键决策
    if key_points:
        for kp in key_points[:3]:
            clean = re.sub(r'[\*\#]', '', kp).strip()
            if len(clean) <= 80:
                summaries.append(clean)

    # 用户意图（从用户消息推断）
    if user_msgs:
        intents = []
        intent_keywords = {"要求": ["要", "搞", "帮我", "给我", "我想", "能不能"],
                         "提问": ["？", "?", "什么是", "怎么", "为什么", "是不是"],
                         "决策": ["决定", "选", "确定", "拍板", "就用"]}
        for msg in user_msgs:
            for intent, kws in intent_keywords.items():
                if any(kw in msg for kw in kws) and len(msg) <= 50:
                    intents.append(f"{intent}：{msg}")
                    break
            if len(intents) >= 2:
                break
        summaries.extend(intents)

    # 待办提示
    if todos:
        summaries.append(f"产生 {len(todos)} 个待办事项")

    # 限制 3-5 句
    summaries = summaries[:5]
    if not summaries:
        summaries = ["(无明显关键内容，主要为日常对话)"]

    return {
        "topics": [t.strip() for t in topics],
        "tags": sorted(tags),
        "summaries": summaries,
        "key_decisions": key_points[:5],
        "todos": todos,
        "user_messages_count": len(user_msgs),
        "sessions_count": text.count("## ["),
    }


def write_summary(date_str: str, summary: dict, memory_dir: Path):
    """写入摘要文件"""
    summary_dir = memory_dir / "summaries"
    summary_dir.mkdir(parents=True, exist_ok=True)
    fp = summary_dir / f"{date_str}.md"

    lines = [f"# {date_str} 对话摘要\n"]
    lines.append(f"**话题：** {', '.join(summary['topics']) or '无'}")
    lines.append(f"**标签：** {', '.join(summary['tags']) or '无'}")
    lines.append(f"**对话数：** {summary['sessions_count']} 段")
    lines.append(f"**用户消息：** {summary['user_messages_count']} 条\n")
    lines.append("## 摘要\n")
    for s in summary['summaries']:
        lines.append(f"- {s}")
    if summary['key_decisions']:
        lines.append("\n## 关键决策\n")
        for d in summary['key_decisions']:
            lines.append(f"- {d}")
    if summary['todos']:
        lines.append("\n## 待办\n")
        for t in summary['todos']:
            lines.append(t)
    lines.append("")

    fp.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ 摘要已生成 → {fp}")
    return str(fp)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="生成对话摘要")
    p.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"))
    p.add_argument("--memory-dir", default=None)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    md = args.memory_dir if args.memory_dir else DEFAULT_MEMORY_DIR
    md = Path(md)

    text = load_conversation(args.date, md)
    if not text:
        print(f"⚠️ 未找到 {args.date} 的对话记录")
        exit(1)

    summary = generate_summary(text)

    if args.json:
        import json
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        write_summary(args.date, summary, md)
